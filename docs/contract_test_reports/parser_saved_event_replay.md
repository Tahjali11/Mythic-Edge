# Parser Saved Event Replay Contract-Test Report

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/54

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch reviewed: `codex/parser-module-audit-suite`

## Source Artifacts

- `docs/agent_constitution.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/contracts/parser_saved_event_replay.md`
- `docs/implementation_handoffs/parser_saved_event_replay_comparison.md`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tests/test_saved_event_replay.py`

## Role Performed

Codex E: Module Reviewer / contract-test thread.

## Implementation Under Test

The Codex C comparison pass added focused tests in
`tests/test_saved_event_replay.py` and produced
`docs/implementation_handoffs/parser_saved_event_replay_comparison.md`.

No runtime replay code changed in `src/mythic_edge_parser/app/saved_event_replay.py`.

## Findings

No blocking findings.

The comparison and test-only updates satisfy the saved-event replay contract for
the current v1 behavior. The runtime replay implementation was not changed, and
the new tests lock the contract-covered behavior for public interfaces,
latest-file selection, event kind mapping, timestamp handling, raw-hash dedupe,
stats counting, unknown-kind behavior, callback exception visibility, and replay
metadata hashing.

## Confirmed Contract Matches

- `ReplayStats`, `EVENT_CLASS_BY_KIND`, `latest_jsonl_files()`,
  `event_from_saved_record()`, and `replay_latest_saved_events()` remain
  import-compatible.
- `latest_jsonl_files()` still recursively selects one highest-version JSONL
  file per parent directory, treats unversioned files as lower priority than
  versioned files, and orders selected files by parent directory name.
- `EVENT_CLASS_BY_KIND` still contains exactly the seven contracted supported
  kinds: `ClientAction`, `DetailedLoggingStatus`, `EventLifecycle`,
  `GameResult`, `GameState`, `MatchState`, and `Rank`.
- Unsupported, missing, differently cased, or whitespace-padded event kinds
  return `None` from `event_from_saved_record()` and are skipped by replay.
- Missing, falsey, or blank timestamps reconstruct as `None`; invalid nonblank
  timestamps fail fast.
- `event.metadata.raw_bytes` and `event.metadata.raw_bytes_hash` are derived
  from the saved JSONL line passed into `event_from_saved_record()`, while
  replay dedupe uses the stored `raw_bytes_hash` field.
- Nonblank raw-hash dedupe remains global across one replay call and across all
  selected files.
- Blank or missing raw hashes do not participate in dedupe.
- Blank JSONL lines are ignored without affecting stats.
- Duplicate hashes and unknown event kinds increment `events_skipped`.
- `events_processed` increments only after the callback returns normally.
- Invalid JSON and callback exceptions remain fail-fast and visible to the
  caller.
- Replay remains callback-driven and does not directly mutate parser state,
  write workbook rows, post webhooks, change Apps Script behavior, or update
  runtime status.

## Contract Mismatches

None found.

## Missing Tests Or Non-Blocking Gaps

- Equal-version tie behavior for two files in the same parent directory remains
  dependent on `Path.rglob()` discovery order. The contract identifies this as
  an unknown/suspected gap, not required v1 behavior.
- Ordering can still be ambiguous when two selected files live under different
  nested paths with the same final parent directory name. The contract preserves
  current ordering by `path.parent.name`.
- Non-dict top-level JSON and non-dict nested `payload` fail-fast behavior are
  documented but not directly covered by the new focused tests.
- Replay still reconstructs only the seven contracted kinds, while the archive
  producer can keep additional event kinds. The contract treats this as an
  unresolved completeness question rather than an implementation mismatch.
- No parser-state integration replay test feeds reconstructed `MatchState` or
  `GameResult` events into state. The contract leaves that as an open question
  for a future issue or contract update.

## Drift Classification

- Repo drift: none found inside the reviewed saved-event replay scope.
- Workbook drift: not inspected; out of scope for this replay utility review.
- Deployment drift: not inspected; no Apps Script or deployed behavior changed.
- Local-data drift: not inspected; no raw logs, generated data, runtime status
  files, failed posts, workbook exports, or archive JSONL producer output were
  touched.

## Forbidden Scope

Forbidden scope was not touched.

This review found no changes to parser behavior outside
`saved_event_replay.py`, parser state final reconciliation, workbook schema,
webhook payload shape, Apps Script behavior, parser event classes, match
identity, game identity, production deduplication semantics outside replay,
secrets, environment variables, raw logs, generated data, runtime status files,
failed posts, workbook exports, or archive JSONL shape produced by runtime code.

This thread did not target `main`, open a PR, close issue #54, or mark tracker
#5 complete.

## Validation

```powershell
py -m pytest -q tests\test_saved_event_replay.py
```

Result:

```text
23 passed in 0.15s
```

```powershell
py -m pytest -q tests\test_saved_event_replay.py tests\test_parser_regressions.py
```

Result:

```text
25 passed in 0.27s
```

```powershell
py -m ruff check src tests
```

Result:

```text
All checks passed!
```

```powershell
git diff --check -- docs/contracts/parser_saved_event_replay.md docs/implementation_handoffs/parser_saved_event_replay_comparison.md docs/contract_test_reports/parser_saved_event_replay.md src/mythic_edge_parser/app/saved_event_replay.py tests/test_saved_event_replay.py
```

Result:

```text
Passed with no output.
```

## Recommendation

Approve this contract-test pass and route to Codex F: Module Submitter.

Rationale: no blocking findings remain, the implementation did not change
runtime replay behavior, the focused tests cover the required v1 contract
behavior, and remaining gaps are explicitly documented as future policy or
contract decisions.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for https://github.com/Tahjali11/Mythic-Edge/issues/54.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Submit the saved-event replay contract-test/comparison work from the current branch to a PR targeting codex/parser-module-audit-suite.

Source artifacts:
- docs/contracts/parser_saved_event_replay.md
- docs/implementation_handoffs/parser_saved_event_replay_comparison.md
- docs/contract_test_reports/parser_saved_event_replay.md
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_saved_event_replay.py

Reviewer result:
- No blocking findings.
- No runtime replay behavior changed.
- Focused test-only updates satisfy the saved-event replay contract.
- Forbidden scope was not touched.
- Remaining gaps are non-blocking future contract/policy questions: equal-version tie behavior, duplicate parent-name ordering ambiguity, non-dict malformed-record direct tests, unsupported archived event-kind completeness, and parser-state replay integration coverage.

Before submitting:
1. Inspect git status and the full diff.
2. Confirm only issue #54 artifacts are staged.
3. Do not include raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, environment variables, or unrelated local artifacts.
4. Do not target main. Target codex/parser-module-audit-suite.

Run:
py -m pytest -q tests\test_saved_event_replay.py
py -m pytest -q tests\test_saved_event_replay.py tests\test_parser_regressions.py
py -m ruff check src tests
git diff --check

If validation passes, commit, push, and open a draft PR. Do not close issue #54, do not mark tracker #5 complete, and do not merge.

Final handoff must include:
- role performed
- issue and tracker
- branch name
- PR URL
- files committed
- validation result
- forbidden scope confirmation
- residual non-blocking gaps
- next recommended role
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/54"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/parser_saved_event_replay.md"
  reviewed_artifacts:
    - "docs/implementation_handoffs/parser_saved_event_replay_comparison.md"
    - "src/mythic_edge_parser/app/saved_event_replay.py"
    - "tests/test_saved_event_replay.py"
  produced_artifact: "docs/contract_test_reports/parser_saved_event_replay.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  recommendation: "approve and submit"
  validation:
    - "py -m pytest -q tests\\test_saved_event_replay.py -> 23 passed in 0.15s"
    - "py -m pytest -q tests\\test_saved_event_replay.py tests\\test_parser_regressions.py -> 25 passed in 0.27s"
    - "py -m ruff check src tests -> All checks passed!"
    - "git diff --check -- reviewed files -> passed with no output"
  stop_conditions:
    - "Do not target main."
    - "Do not close issue #54."
    - "Do not mark tracker #5 complete."
    - "Do not change parser behavior outside saved_event_replay.py."
    - "Do not change protected downstream surfaces."
```
