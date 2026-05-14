# Parser Outputs Implementation Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/40

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Source contract: `docs/contracts/parser_outputs.md`

Target branch: `codex/parser-module-audit-suite`

Role: Codex C: Module Implementer

Risk tier: High

## Summary Of Implementation Comparison

The current `outputs.py` implementation already matched the parser outputs
contract for webhook target redaction, synchronous POST retry classification,
failed-post delegation, pending-row dedupe identity, callback delivery through
result draining, dispatcher start/stop lifecycle, and daily archive path
selection.

This comparison found two clear contract mismatches in the output boundary:

- `reset_outputs_runtime_state()` could invoke completed dispatch callbacks
  when it reached the callback-capable stop/drain path.
- `append_local_jsonl()` only accepted dict rows and always serialized them,
  while the contract requires already serialized JSONL row strings to be
  appended without parsing or rewriting.

Both mismatches were fixed inside `outputs.py`, and focused tests were added in
`tests/test_app_outputs.py`. No parser truth, workbook schema, webhook payload
shape, Apps Script behavior, parser state final reconciliation, extractor
behavior, match/game identity, deduplication semantics, secrets, environment
variables, raw logs, runtime status schema, failed-post schema, or workbook
exports were changed.

Changed files:

- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_app_outputs.py`
- `docs/implementation_handoffs/parser_outputs_comparison.md`

Referenced source artifact already present in the worktree:

- `docs/contracts/parser_outputs.md`

Repository hygiene note:

- `docs/contracts/parser_outputs.md` was already untracked at the start of this
  pass and remains the source artifact for issue #40.
- No files were staged or committed.

## Findings First

### Resolved: reset could invoke callbacks

Contract requirement:

- Reset clears queued jobs, completed results, and pending keys without invoking
  success or failure callbacks.

Initial state:

- `reset_outputs_runtime_state()` called `stop_webhook_dispatcher(wait_for_queue=False)`.
- When no dispatcher thread existed, `stop_webhook_dispatcher()` drained
  completed results through `drain_webhook_results()`, which invokes callbacks.

Resolution:

- `reset_outputs_runtime_state()` now performs reset-specific queue/result
  cleanup.
- It drains queued work without processing, sends a sentinel only when a live
  dispatcher thread exists, drains completed results without callbacks, clears
  pending keys, clears the thread reference, and marks the dispatcher inactive.
- Added a focused regression test proving reset does not invoke callbacks.

### Resolved: local JSONL append did not support pre-serialized rows

Contract requirement:

- `append_local_jsonl(local_row, event_dt)` must append an already serialized
  JSONL row string plus a newline without parsing, enriching, validating, or
  rewriting it.

Initial state:

- `append_local_jsonl()` accepted a dict and always called
  `json.dumps(local_row, ensure_ascii=False)`.

Resolution:

- `append_local_jsonl()` now accepts `str | dict[str, Any]`.
- String input is written exactly as provided plus the terminating newline.
- Dict input keeps the existing serialization behavior for current callers such
  as `runner.py`.
- Added focused tests for exact string preservation, same-day cache reuse,
  next-day rollover, and legacy dict compatibility.

### Resolved: focused outputs coverage gaps

Contract requirement:

- Add or verify focused tests for missing webhook URL, success attempt counts,
  retryable HTTP behavior, terminal response truncation, pending-row dedupe,
  callback timing, reset semantics, dispatcher status flags, and daily archive
  behavior.

Initial state:

- Existing tests covered failed-post capture, retryable network success, explicit
  webhook redaction, dispatcher stop drain/requeue, reset queue clearing, and
  one diagnostics active-deck artifact path.
- The contract-required edge cases above were missing or weakly covered.

Resolution:

- Added focused tests for all blocking gaps that are practical without live
  network, live Apps Script, or generated local artifacts.

## Confirmed Matches

- `outputs.py` remains a transport/local archive module, not a parser truth
  owner.
- Synchronous posting sends the caller-provided row object through
  `requests.post(WEBHOOK_URL, json=row, timeout=10)`.
- Missing `WEBHOOK_URL` returns `False`, logs a skip path, does not create
  failed-post artifacts, and remains distinguishable from terminal failures.
- Successful synchronous POST marks webhook success diagnostics with the
  observed attempt count.
- Retryable network failures retry and can eventually mark success.
- Retryable HTTP failures retry and can eventually mark success.
- Nonretryable HTTP failures do not retry, record failed posts, mark failure,
  and return `False`.
- Terminal retryable HTTP failure records failed-post response text bounded to
  the current 500-character limit.
- Webhook target display goes through diagnostics redaction for explicit and
  configured URLs.
- `_row_dispatch_key()` remains deterministic for equivalent dict rows with
  different insertion order.
- Async submission still uses shallow top-level row copies and does not deep-copy
  nested mutable values.
- Duplicate pending submissions return `False` and do not register duplicate
  callbacks.
- Success and failure callbacks remain tied to result draining, not submission
  or worker-thread execution.
- Callback exceptions still propagate from `drain_webhook_results()`.
- `stop_webhook_dispatcher(wait_for_queue=True)` drains queued work and completed
  results through the callback-capable shutdown path.
- Dispatcher runtime status updates still mark active on start and inactive on
  clean stop/reset.
- Daily archive labels remain `"%m_%d_%y"`, use the runtime-state cache, and roll
  over to a new path for a new event date.

## Contract Mismatches

No unresolved contract mismatch is known after this pass.

Resolved mismatches:

- Reset no longer invokes completed-result callbacks.
- Local JSONL append now supports contracted pre-serialized string input without
  rewriting it.

## Missing Safeguards

No blocking missing safeguard remains in the reviewed `outputs.py` scope.

Safeguards added or strengthened:

- Reset-specific cleanup avoids callback-capable drain paths.
- Reset discards completed results without calling success or failure callbacks.
- Pre-serialized local archive rows are not parsed or rewritten by `outputs.py`.

Behavior deliberately left unchanged:

- `post_row_to_google_sheets()` still catches `requests.HTTPError` and
  `requests.RequestException`, not arbitrary serialization/runtime exceptions.
- Async shallow copy behavior remains top-level only.
- Dispatcher stop timeout behavior remains as documented by the contract.
- `runner.py` still passes dict rows to `append_local_jsonl()`; the output
  function keeps that compatibility while also satisfying the string contract.

## Missing Or Weak Tests

Blocking test gaps from the contract were addressed in
`tests/test_app_outputs.py`.

Added or strengthened coverage:

- Missing webhook URL returns `False` without failed-post artifacts.
- Successful sync POST marks attempt count.
- Retryable HTTP failures retry and eventually succeed.
- Terminal retryable HTTP failure records truncated response text.
- Nonretryable HTTP failures do not retry.
- Configured webhook URL redaction.
- Async pending-row dedupe for reordered dict keys.
- Duplicate pending submit does not register duplicate callbacks.
- Async submit shallow-copies top-level row fields only.
- Drained success/failure results clear pending and invoke only matching
  callbacks.
- Callback exceptions propagate from result draining.
- Worker thread completion does not invoke callbacks before result drain.
- Dispatcher status flags update on start, clean stop, and reset.
- Reset clears queues/results/pending without callbacks.
- Live-dispatcher reset discards completed results without callbacks.
- Daily archive string preservation, newline append, cache reuse, rollover, and
  legacy dict compatibility.

Remaining non-blocking gaps:

- Dispatcher stop-timeout branch was not forced with a synthetic stuck thread.
- Tests do not perform live Google Sheets or Apps Script webhook posts.
- Tests do not run a live MTGA parser stream.
- Windows CI/GitHub Actions were not run locally.

## Validation Evidence

Commands run:

```bash
python3 -m pytest -q tests/test_app_outputs.py
```

Result:

```text
19 passed in 0.12s
```

```bash
python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py
```

Result:

```text
44 passed in 0.80s
```

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

```bash
git diff --check
```

Result: passed with no output.

## Still-Unverified Layers

- Live MTGA log ingestion was not executed.
- Live webhook delivery to Google Apps Script was not executed.
- Workbook updates and Apps Script behavior were not exercised.
- GitHub Actions/Windows CI was not executed.
- Submitter/deployer PR checks have not run.
- Tracker #5 was not marked complete.

## Reviewer Focus

Ask Codex E to verify:

- `reset_outputs_runtime_state()` cannot invoke queued or completed dispatch
  callbacks in the no-thread and live-thread reset paths.
- The reset change does not accidentally change normal
  `stop_webhook_dispatcher()` callback delivery.
- `append_local_jsonl()` preserves pre-serialized string rows exactly and keeps
  existing dict behavior for current callers.
- Focused tests assert transport behavior without moving parser-owned truth into
  outputs, runner, workbook formulas, dashboard logic, Apps Script, webhook
  delivery, or AI interpretation.
- No protected parser/runtime/workbook/App Script surfaces changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #40:
https://github.com/Tahjali11/Mythic-Edge/issues/40

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_outputs.md
- docs/implementation_handoffs/parser_outputs_comparison.md
- src/mythic_edge_parser/app/outputs.py
- tests/test_app_outputs.py
- src/mythic_edge_parser/app/runner.py
- tests/test_runner.py
- src/mythic_edge_parser/app/diagnostics.py
- tests/test_diagnostics.py
- src/mythic_edge_parser/app/status_api.py
- tests/test_status_api.py
- any directly referenced output-adjacent files or focused tests named by the contract

Goal:
Verify the Module Implementer changes against the parser outputs contract.

Confirm:
- outputs.py remains a transport/local archive boundary and does not own parser truth.
- reset_outputs_runtime_state() clears queued work, completed results, and pending keys without invoking callbacks.
- reset behavior does not change normal stop_webhook_dispatcher() callback delivery.
- append_local_jsonl() writes pre-serialized string rows exactly as provided plus a newline.
- append_local_jsonl() preserves current dict compatibility for existing runner callers.
- Missing WEBHOOK_URL returns False without failed-post artifacts.
- Successful sync POST marks success attempt counts.
- Retryable network and HTTP failures retry according to the contract.
- Terminal HTTP failure records failed posts with response_text bounded to 500 characters.
- Async pending-row dedupe remains deterministic for reordered dict keys.
- Duplicate pending submit returns False and does not register duplicate callbacks.
- Callbacks run only during result draining or callback-capable shutdown draining.
- Callback exceptions propagate from drain_webhook_results().
- Dispatcher runtime status active/inactive updates remain visible.
- Daily archive labels, path cache reuse, rollover, and newline append behavior match the contract.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication semantics, secrets, environment variables, raw logs, generated data, runtime status file schema, failed-post schema, or workbook exports changed.
- Parser-owned truth was not moved into output transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or AI-generated interpretation.

Validation:
Run:
python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m ruff check src tests
git diff --check

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication semantics, secrets, environment variables, raw logs, generated data, runtime status file schema, failed-post schema, or workbook exports.
Do not move parser-owned truth into output transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or AI-generated interpretation.
Do not stage, commit, merge, target main, or mark tracker #5 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/40"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_outputs.md"
  target_artifact: "docs/implementation_handoffs/parser_outputs_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_app_outputs.py"
    - "python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication semantics, secrets, environment variables, raw logs, generated data, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not move parser-owned truth into output transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or AI-generated interpretation."
    - "Do not target main for module PR work."
    - "Do not mark tracker #5 complete."
```
