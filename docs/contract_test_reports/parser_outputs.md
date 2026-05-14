# Parser Outputs Contract Test Report

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/40

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Contract: `docs/contracts/parser_outputs.md`

Implementation handoff: `docs/implementation_handoffs/parser_outputs_comparison.md`

Branch: `codex/parser-module-audit-suite`

Role: Codex E: Module Reviewer

Risk tier: High

## Findings First

No blocking findings.

The Module Implementer patch is scoped to the parser outputs boundary:

- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_app_outputs.py`
- `docs/contracts/parser_outputs.md`
- `docs/implementation_handoffs/parser_outputs_comparison.md`

No parser behavior, parser state final reconciliation, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes, extractor behavior,
match identity, game identity, deduplication semantics, secrets, environment
variables, raw logs, generated data, runtime status file schema, failed-post
schema, or workbook exports changed.

## Contract-Test Verdict

Pass.

The implementation matches the parser outputs contract for the reviewed
transport/local archive boundary. The patch can move to Codex F: Module
Submitter.

## Confirmed Contract Matches

- `outputs.py` remains a transport/local archive module and does not own parser
  truth, workbook row meaning, match/game identity, final reconciliation, or
  Apps Script compatibility.
- `reset_outputs_runtime_state()` clears queued work, completed results, and
  pending keys without invoking queued or completed dispatch callbacks in the
  covered reset paths.
- The reset fix does not change normal `stop_webhook_dispatcher()` callback
  delivery; clean stop still drains completed results through callback-capable
  result draining.
- `append_local_jsonl()` writes pre-serialized string rows exactly as supplied
  plus a newline.
- `append_local_jsonl()` preserves current dict compatibility for existing
  runner callers while adding the contracted serialized-string boundary.
- Missing `WEBHOOK_URL` returns `False` without failed-post artifacts or webhook
  failure status.
- Successful synchronous posting marks success with the observed attempt count.
- Retryable network and HTTP failures retry according to the contract.
- Nonretryable HTTP failure does not retry and records a failed post.
- Terminal retryable HTTP failure records failed-post response text bounded to
  the current 500-character limit.
- Async pending-row dedupe remains deterministic for reordered dict keys.
- Duplicate pending submit returns `False` and does not register duplicate
  callbacks.
- Async submit still shallow-copies only the top-level row.
- Success and failure callbacks run only from result draining or
  callback-capable shutdown draining, not from submit or the worker thread.
- Callback exceptions continue to propagate from `drain_webhook_results()`.
- Dispatcher runtime status active/inactive updates remain visible.
- Daily archive labels, runtime-state path cache reuse, rollover, and newline
  append behavior match the contract.

## Contract Mismatches

None.

## Missing Tests

No blocking missing tests remain for the contract-required output boundary.

Focused coverage now includes:

- missing webhook URL behavior
- success attempt counts
- retryable network success
- retryable HTTP success
- terminal retryable HTTP failure response truncation
- nonretryable HTTP terminal failure
- configured and explicit webhook URL redaction
- pending-row dedupe and duplicate callback suppression
- top-level async shallow copy behavior
- success/failure result callback routing
- callback exception propagation
- worker-thread completion before result draining
- dispatcher active/inactive status flags
- reset without callbacks
- clean stop callback delivery and requeue behavior
- local JSONL string preservation, dict compatibility, same-day cache reuse, and
  next-day rollover

## Drift Classification

- Repo drift: none found. Tracked diffs are limited to `outputs.py` and
  `tests/test_app_outputs.py`; untracked artifacts are the issue #40 contract
  and implementation handoff.
- Parser/runtime protected-surface drift: none found outside the authorized
  outputs module.
- Workbook schema drift: none found.
- Webhook payload shape drift: none found.
- Apps Script drift: none found.
- Runtime status schema drift: none found.
- Failed-post schema drift: none found.
- Local generated-data/raw-log drift: none found.
- Tracker drift: tracker #5 was not marked complete.
- Branch drift: review was performed on `codex/parser-module-audit-suite`, not
  `main`.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_app_outputs.py
```

Result:

```text
19 passed in 0.35s
```

```bash
python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py
```

Result:

```text
44 passed in 0.74s
```

```bash
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py
```

Result:

```text
40 passed in 0.14s
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

```bash
python3 -m pytest -q
```

Result:

```text
535 passed in 1.43s
```

Protected-surface spot checks:

```bash
git diff --name-only
```

Result:

```text
src/mythic_edge_parser/app/outputs.py
tests/test_app_outputs.py
```

```bash
git ls-files --others --exclude-standard
```

Result:

```text
docs/contracts/parser_outputs.md
docs/implementation_handoffs/parser_outputs_comparison.md
```

```bash
git diff --name-only -- src/mythic_edge_parser/app/state.py src/mythic_edge_parser/app/transforms.py src/mythic_edge_parser/app/sheet_exports.py src/mythic_edge_parser/app/runtime_surfaces.py src/mythic_edge_parser/events.py src/mythic_edge_parser/parsers .github tools data workbook_exports exports
```

Result: passed with no output.

## Remaining Non-Blocking Gaps

- Live Google Sheets / Apps Script webhook delivery was not exercised locally.
- Live MTGA parser stream output was not exercised locally.
- Dispatcher stop-timeout behavior was not forced with a synthetic stuck thread.
- GitHub Actions and Windows CI were not run locally.
- `append_local_jsonl()` keeps dict input as documented transitional
  compatibility for current runner callers; new callers should prefer the
  contracted pre-serialized string boundary.

## Next Recommended Role

Codex F: Module Submitter.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/40"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_outputs.md"
  target_artifact: "PR for issue #40 on codex/parser-module-audit-suite"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  verdict: "No blocking findings. Ready for Codex F: Module Submitter."
  validation:
    - "python3 -m pytest -q tests/test_app_outputs.py -> 19 passed in 0.35s"
    - "python3 -m pytest -q tests/test_app_outputs.py tests/test_runner.py tests/test_diagnostics.py tests/test_status_api.py -> 44 passed in 0.74s"
    - "python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py -> 40 passed in 0.14s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed"
    - "python3 -m pytest -q -> 535 passed in 1.43s"
  stop_conditions:
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication semantics, secrets, environment variables, raw logs, generated data, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not move parser-owned truth into output transport, workbook formulas, dashboard logic, Apps Script, webhook delivery, or AI-generated interpretation."
    - "Do not target main for module PR work."
    - "Do not mark tracker #5 complete."
```
