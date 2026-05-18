# Corpus Regression Parity With Manasight

## Summary

Mythic Edge already has strong parser reliability foundations: golden replay,
schema snapshots, feature-equity corpus reporting, parser diagnostics, drift
detection, and protected-surface governance. Manasight is still ahead in one
specific discipline area: corpus-style regression tracking over a broad real-log
corpus with per-file parser/event counts, ratchet semantics, smoke-test CI, and
field-rich parser coverage reports.

This artifact lists the corpus regression additions Mythic Edge would need to
reach parity with Manasight's corpus discipline, and where it can reasonably
exceed Manasight by using Mythic-specific parser truth, workbook schema, and
evidence-ledger layers.

This is a planning artifact only. It does not authorize parser behavior changes,
fixture imports, CI gates, baseline refreshes, raw log commits, or production
workflow changes.

## Source Request

Source request: add a fully comprehensive list of corpus regression additions
needed for Mythic Edge to be at parity with Manasight to the
`codex/polish-and-discipline-suite` branch.

Related suite artifacts:

- `docs/problem_representations/polish_and_discipline_suite.md`
- `docs/problem_representations/polish_installer_setup_parity_audit.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`

## Source Artifacts Inspected

Manasight reference checkout:

- `smoke-baseline.json`
- `.github/workflows/smoke-test.yml`
- `tests/smoke_common/mod.rs`
- `tests/smoke_parsers.rs`
- `tests/smoke_ratchet.rs`
- `tests/smoke_router.rs`
- `tests/smoke_stream.rs`
- `tests/stream_integration.rs`
- `tests/corpus_flush_timing.rs`
- `tests/corpus_prev_game_state_id.rs`
- `tests/truncation_integration.rs`
- `src/events.rs`
- `src/router.rs`
- `src/log/entry.rs`
- `src/stream.rs`
- parser modules under `src/parsers/`

Mythic Edge current polish branch:

- `docs/problem_representations/polish_and_discipline_suite.md`
- `docs/problem_representations/polish_installer_setup_parity_audit.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
- `tests/fixtures/golden_replay/`
- `.github/workflows/repo-checks.yml`

## Manasight Corpus Regression Reference

Manasight's corpus regression system has several distinct pieces:

1. A broad real-log smoke baseline committed as `smoke-baseline.json`.
2. An opt-in real-log source path using `MANASIGHT_TEST_LOGS`.
3. Parser-only smoke attribution over each log file.
4. Router-level smoke coverage.
5. Stream-level smoke coverage.
6. Ratchet comparison logic where count decreases are regressions and count
   increases are improvements.
7. An explicit bless/update path using `SMOKE_BLESS=1`.
8. CI that downloads a released corpus, runs smoke tests, uploads the report,
   writes a job summary, and can open a baseline update PR.

The inspected Manasight `smoke-baseline.json` currently contains:

- 44 corpus files.
- 52,239 total entries.
- 6,335 unclaimed entries.
- Nonzero event totals for `ClientAction`, `DeckCollection`,
  `DetailedLoggingStatus`, `DraftBot`, `DraftComplete`, `DraftHuman`,
  `EventLifecycle`, `GameResult`, `GameState`, `Inventory`, `MatchState`,
  `Rank`, and `Session`.
- Nonzero draft coverage:
  - `DraftBot`: 78
  - `DraftHuman`: 118
  - `DraftComplete`: 4

The baseline is not semantic proof that every parse is correct. It is a durable
coverage and regression ratchet: if a future parser change stops recognizing
previously recognized event families, the count delta is visible.

## Mythic Edge Current State

Mythic Edge currently has a narrower committed feature-equity corpus baseline:

- 2 golden replay manifests.
- Nonzero event counts for `ClientAction`, `GameResult`, `GameState`,
  `MatchState`, and `Rank`.
- Zero committed corpus counts for `Collection`, `ConnectionError`,
  `DeckCollection`, `DetailedLoggingStatus`, `DraftBot`, `DraftComplete`,
  `DraftHuman`, `EventLifecycle`, `Inventory`, `LogFileRotated`,
  `MatchConnectionState`, `Session`, `TcpConnectionClose`, `Truncation`, and
  `WebSocketClosed`.

That is not a parser bug by itself. It means Mythic Edge has strong focused
tests and schema snapshots, but it does not yet have Manasight-style broad
corpus regression evidence for every parser family.

## Parity Definition

Corpus regression parity means Mythic Edge can answer the same classes of
questions Manasight's smoke system answers:

- Which parser families claimed each corpus file?
- Which event families were emitted?
- Did any parser claim count or event count decrease against a reviewed
  baseline?
- Did any parser family improve by claiming newly recognized events?
- Did any file become unreadable or produce parser/router failures?
- Did unclaimed entries, timestamp failures, or double claims change?
- Do specific GameState subfield metrics still appear in real or sanitized
  replay data?
- Can a human explicitly bless a baseline update without auto-blessing drift?
- Can CI or local commands produce a durable report without exposing raw logs?

Parity does not require copying Manasight code, matching Rust internals, or
treating Manasight as a truth owner. It means Mythic Edge has equivalent
regression evidence for its own Python parser and richer downstream pipeline.

## Comprehensive Addition List

### 1. Corpus Source Policy

Add a contract for corpus source classes:

- committed sanitized fixtures
- committed synthetic fixtures
- local private corpus, never committed
- optional public released corpus, if license/privacy review approves it
- generated reports, report-only unless explicitly approved

Each corpus source should declare:

- source type
- privacy class
- allowed storage location
- whether raw log text may be committed
- whether expected outputs may be committed
- whether baseline deltas may be used as review evidence

### 2. Corpus Registry

Add a registry or manifest index that can list all corpus inputs in a stable
order. It should support:

- golden replay manifest paths
- direct sanitized log slices
- local private corpus directories
- optional public corpus release metadata
- corpus tag or local snapshot id
- source file count
- source file hashes or redacted fingerprints

### 3. Privacy And Sanitizer Preflight

Before any corpus input is used for committed fixtures or reports, run a
privacy preflight that checks:

- no raw private Player.log files are committed
- no webhook URLs, bearer tokens, account ids, local paths, or credentials
  appear
- sanitizer metadata is present for committed sanitized logs
- local private corpus paths are redacted in reports
- report output does not contain raw log lines

This should connect to the repo's protected-surface and secret/private-marker
scanner work instead of inventing a second safety system.

### 4. Parser-Only Corpus Smoke Runner

Add a Manasight-style parser-only smoke runner that offers each entry to the
registered parser modules independently, before router priority hides overlap.

It should count:

- per-parser claims
- per-event-family emissions
- total entries
- unclaimed entries
- double claims
- allowed overlaps
- parser exceptions
- timestamp parse failures
- read errors

This differs from the normal router path. It is diagnostic attribution, not
runtime behavior.

### 5. Parser Registry For Smoke Attribution

Create a deliberate corpus-smoke parser registry. At parity it should cover:

- metadata / detailed logging status
- session
- match state
- GRE
- client actions
- draft bot
- draft human
- draft complete
- inventory
- collection
- deck collection
- rank
- event lifecycle
- truncation
- connection state
- connection close
- connection error

Manasight's current smoke parser registry does not include every newer
connection parser, but Mythic Edge should include its connection families
because they are first-class Mythic parser surfaces.

### 6. Event-Family Count Matrix

The corpus report should count every Mythic Edge event family:

- `GameState`
- `ClientAction`
- `MatchState`
- `Truncation`
- `DraftBot`
- `DraftHuman`
- `DraftComplete`
- `EventLifecycle`
- `Session`
- `Rank`
- `Collection`
- `DeckCollection`
- `Inventory`
- `GameResult`
- `LogFileRotated`
- `DetailedLoggingStatus`
- `MatchConnectionState`
- `TcpConnectionClose`
- `WebSocketClosed`
- `ConnectionError`

Zero counts should be explicit, not omitted.

### 7. Payload-Type Count Matrix

For each emitted event, count `event.kind + payload["type"]` when a payload type
exists. This should catch regressions where an event family still exists but a
specialized payload subtype disappears.

Examples:

- `ClientAction:mulligan_resp`
- `ClientAction:select_n_resp`
- `ClientAction:submit_deck_resp`
- `GameState:game_state_message`
- `GameState:queued_game_state_message`
- `GameState:connect_resp`
- `GameResult:game_result`
- `DraftBot:bot_draft_status`
- `DraftBot:bot_draft_pick`
- future `DraftHuman:*`
- future `DraftComplete:*`

### 8. Per-File Baseline

Add a per-file baseline format comparable to Manasight's `smoke-baseline.json`.
It should include:

- schema version
- baseline id
- corpus tag or snapshot id
- source privacy class
- generated-from commit
- per-file total entries
- per-file parser counts
- per-file event-family counts
- per-file payload-type counts
- per-file unclaimed count
- per-file double-claim count
- per-file timestamp-failure count
- per-file read-error status

### 9. Aggregate Baseline

In addition to per-file data, include aggregate totals:

- total files
- total entries
- total routed or claimed entries
- total unknown/unclaimed entries
- parser totals
- event-family totals
- payload-type totals
- timestamp anomaly totals
- data-loss/truncation totals
- parser exception totals

Manasight's baseline is strongly per-file; Mythic Edge can exceed parity by
also making aggregate summaries first-class.

### 10. Ratchet Comparator

Add a ratchet comparator with explicit policy:

- decreased parser counts are regressions unless explained by contract
- decreased event-family counts are regressions unless explained by contract
- increased counts are improvements or review items
- new files are improvements/review items
- missing files are skipped or reported according to corpus source policy
- new event families are improvements requiring baseline review
- new parser families are improvements requiring baseline review

The comparator should sort diffs deterministically and produce readable output.

### 11. Bless Or Baseline Update Policy

Add an explicit baseline update path equivalent to Manasight's `SMOKE_BLESS=1`,
but adapted to Mythic Edge's stronger governance:

- no automatic local baseline mutation by default
- no baseline refresh without explicit command flag
- no committed baseline update without an issue or PR note
- baseline updates explain why count changes are expected
- private corpus baselines stay local unless converted into sanitized committed
  evidence
- CI may propose baseline updates only after the workflow is proven stable

### 12. Report-Only First Policy

All new corpus regression machinery should start report-only.

It should not become a failing CI gate until the project has:

- stable corpus input policy
- reviewed baseline schema
- low-noise local reports
- documented update policy
- at least one successful manual baseline update cycle

### 13. CI Smoke Workflow

Add a future CI workflow analogous to Manasight's smoke workflow, staged in
levels:

1. Committed sanitized fixture smoke, report-only.
2. Golden replay plus feature-equity corpus report in CI.
3. Optional scheduled smoke using approved public corpus, if one exists.
4. Artifact upload for smoke reports.
5. GitHub job summary with per-file and aggregate tables.
6. Optional baseline update PR creation only after explicit approval.

The workflow must not download or publish private local logs.

### 14. Local Private Corpus Command

Add a local-only command for the user's private `data/match_logs/` corpus.

It should:

- accept a local path argument
- redact paths in the output
- write reports under runtime/status or another ignored generated-data path
- never commit report outputs by default
- optionally compare to a local baseline
- optionally emit a sanitized summary suitable for issue comments

This is the practical bridge between the user's historical logs and future
analytics confidence.

### 15. Parser Exception And Failure Tracking

Count exceptions separately from unknown/unclaimed entries:

- parser exception count
- router exception count
- file read error count
- malformed JSON count, when distinguishable
- callback or stream failure count, for stream smoke

These should be treated as failures or review items, not silently absorbed into
unknown counts.

### 16. Double-Claim Detection

Track entries claimed by more than one parser in parser-only mode.

The report should include:

- total double claims
- parser pairs involved
- example redacted signatures
- allowed overlap policy

Known allowed overlap may include shared `StartHook` payloads that legitimately
feed collection, deck collection, and inventory surfaces. Every allowed overlap
should be documented rather than hidden.

### 17. Unknown And Unclaimed Signature Tracking

For unclaimed entries, emit redacted signature summaries:

- header family
- first safe method/API marker
- first safe line signature
- count
- whether the signature is new against baseline
- whether it resembles an unsupported parser family

This should interoperate with `log_drift_sensor.py` and not create a competing
drift vocabulary.

### 18. Timestamp Failure Tracking

Track timestamp anomalies:

- missing timestamp
- parse failure
- nonstandard timestamp prefix
- per-file counts
- aggregate counts

Timestamp failures should remain diagnostic unless a contract escalates them.

### 19. Line Buffer Corpus Regression

Add or extend corpus tests around line buffering:

- single-line headers flush immediately when appropriate
- multiline JSON entries flush correctly
- final partial entries flush at EOF
- truncation marker blocks remain intact
- headerless orphan lines do not corrupt neighboring entries
- large JSON bodies do not force waiting for the next header if a brace-depth
  or equivalent flush policy exists

This is the Python equivalent of Manasight's corpus flush-timing tests.

### 20. Router-Level Corpus Smoke

Add a router-level corpus smoke report that runs:

```text
LineBuffer -> Router -> event stream
```

It should count:

- routed entries
- unknown entries
- timestamp anomalies
- event-family sequence summaries
- parser priority effects
- no-double-routing expectations where applicable

This proves the normal parser path, not just parser-only attribution.

### 21. Stream-Level Corpus Smoke

Add a stream/tailer-level smoke pass for local files:

```text
FileTailer or stream reader -> LineBuffer -> Router -> event bus/subscriber
```

It should verify:

- stream startup reads expected input mode
- subscriber receives events in order
- log rotation signals are emitted when simulated
- detailed logging status is emitted when simulated
- shutdown does not drop buffered events

This can start with synthetic or sanitized fixture files before any real-log
CI workflow exists.

### 22. GameState Field Richness Metrics

Add field-rich counters for `GameState` payloads:

- `GameStateMessage` count
- `QueuedGameStateMessage` count
- `ConnectResp` count
- turn info present/absent
- annotations present
- total annotations
- annotation type counts
- persistent annotations present
- timers present
- total timers
- timer type counts
- diff/update snapshots
- previous game state id present/missing
- diff deleted instance ids present/total
- diff deleted annotation ids present/total
- degraded or review-required GameState outputs

These are coverage signals, not semantic truth guarantees.

### 23. Previous GameState ID Invariants

Add a corpus check for previous-state linkage:

- diff/incremental GSM events should expose `prev_game_state_id` when the log
  evidence contains it
- complete/full snapshots may reasonably lack previous-state ids
- missing linkage should be counted and reviewed

This maps directly to Manasight's `corpus_prev_game_state_id.rs` concern.

### 24. Truncation And Data-Loss Metrics

Track truncation/data-loss explicitly:

- truncation event count
- fixtures/files with truncation
- object count from truncation marker
- annotation count from truncation marker
- affected message type
- data-loss markers
- downstream diagnostics status

The report should preserve the rule that truncated GSM bodies cannot be
recovered from `Player.log`; the parser can only surface the evidence-loss
signal.

### 25. DeckCollection Invariants

Add corpus invariants for deck collection payloads:

- `DeckSummaries` exists in raw evidence when expected
- `Decks` exists in raw evidence when expected
- parsed deck count matches raw summary count when both are present
- every summarized deck id has a matching raw deck list when evidence exists
- parsed deck entries preserve or expose their source list
- malformed or partial deck evidence is counted as degraded/review, not hidden

Mythic Edge should also include `Collection` and `Inventory` snapshot metrics,
because it has first-class surfaces beyond Manasight's deck collection focus.

### 26. Draft Corpus Coverage

After `DraftBot`, `DraftHuman`, and `DraftComplete` are implemented, add
corpus coverage for:

- draft event-family counts
- draft payload-type counts
- draft id presence
- event id/name presence
- pack number presence
- pick number presence
- pack card id counts
- picked card id presence
- request/response direction
- false-positive separation between bot, human, and complete markers
- per-file draft session counts

This is required for Manasight parity because Manasight's baseline contains
nonzero counts for all three draft families.

### 27. Connection Corpus Coverage

Because Mythic Edge treats connection events as first-class parser surfaces,
the corpus report should include:

- `MatchConnectionState` counts
- `TcpConnectionClose` counts
- `WebSocketClosed` counts
- `ConnectionError` counts
- connection error subtype counts
- reconnect result/outcome counts
- redacted connection signatures

This likely exceeds Manasight's current smoke parser registry, but it matches
Mythic Edge's actual parser scope.

### 28. Session, Rank, Inventory, And Event Lifecycle Coverage

Add corpus coverage for small durable event families:

- session account update
- session authenticated
- session logout
- rank snapshot
- inventory snapshot
- event join
- event claim prize
- event enter pairing
- other event lifecycle payload types

These are common in Manasight's corpus baseline and should not remain zero in
Mythic Edge's long-term feature-equity corpus.

### 29. Client Action Subtype Coverage

Add richer client action counters:

- mulligan response
- select-N response
- submit deck response
- choose starting player response
- generic client action
- UI/noise message classification
- malformed payload tolerance

This protects sideboarding, mulligans, opening hand, and future analytics.

### 30. Game Result And Final Reconciliation Coverage

Add corpus metrics that connect event coverage to Mythic-specific final facts:

- game result events
- match result events or final match-state events
- game summary rows produced
- match summary rows produced
- provisional/live rows vs final rows
- final reconciliation status
- parser-owned row readiness

This exceeds Manasight's parser-library scope and is important for Mythic Edge.

### 31. Saved Event Replay Coverage

Add corpus regression coverage for `saved_event_replay.py`:

- every event family saved by the parser can be reconstructed when intended
- unsupported saved kinds are explicitly skipped
- draft, collection, inventory, connection, rotation, and detailed-status
  families are either supported or intentionally documented as unsupported
- replay deduplicates raw hashes without losing valid events

This is a current Mythic-specific gap relative to the broader parser surface.

### 32. Schema Snapshot Cross-Check

Corpus reports should cross-check against schema snapshots:

- every event family in `events.py` is present in the corpus baseline schema
- every payload type in the parser payload snapshot has a count slot
- zero-count payload types are explicit
- new payload keys require normal schema snapshot approval

This prevents a new parser from being added without regression visibility.

### 33. Golden Replay Integration

The corpus ratchet should consume golden replay manifests as one supported
input type. It should not duplicate golden replay semantics.

Golden replay owns:

- fixture expected outputs
- final parser-owned row checks
- fixture-local pass/diff/degraded status

Corpus ratchet owns:

- coverage counts across many fixtures
- baseline count comparison
- regression/improvement reporting

### 34. Drift Sensor Integration

Corpus regression should consume or align with drift sensor vocabulary:

- unknown signatures
- unmatched API names
- unmatched request API names
- baseline deltas
- new/resolved signatures

Do not create a second drift taxonomy unless a future evidence-ledger contract
requires it.

### 35. Output Formats

Add both machine-readable and human-readable outputs:

- JSON report for tooling
- Markdown summary for PR comments or issue comments
- concise terminal output for local runs
- GitHub Actions job summary for CI

Reports should include privacy metadata and protected-surface disclaimers.

### 36. Validation Selector Integration

Once the validation selector exists on the active branch, add corpus commands
to the selector:

- focused fixture replay
- full committed corpus ratchet
- local private corpus report
- smoke workflow dry-run where feasible

The selector should choose corpus checks when parser modules, router, line
buffer, stream, event classes, schema snapshots, golden replay, or corpus
baseline files change.

### 37. CI Artifact Retention

Add artifact upload behavior for CI smoke reports:

- full smoke output
- JSON report
- Markdown summary
- baseline diff
- redacted unknown signatures

Retention should be long enough for review, but not a substitute for committed
reviewed baselines.

### 38. Baseline PR Automation, Deferred

Manasight can auto-open a baseline update PR when counts improve. Mythic Edge
should defer this until manual baseline refreshes are boring and safe.

Future automation may:

- run only on approved branches
- open a draft PR
- include diff summary and privacy checks
- never include raw logs
- require human review before merge

### 39. Acceptance Tests For The Corpus System Itself

Add tests for the corpus tooling:

- baseline exact match
- count decrease regression
- count increase improvement
- new file handling
- missing file handling
- malformed baseline failure
- privacy failure
- local path redaction
- deterministic diff ordering
- no auto-update without explicit flag
- explicit update/bless behavior

### 40. Documentation And Operator Commands

Add durable local commands for Windows and macOS:

- run committed corpus smoke
- run local private corpus report
- compare against a baseline
- write report to an ignored path
- refresh a baseline only when explicitly requested

The docs should explain that corpus regression proves coverage shape, not
semantic correctness.

## Recommended Issue Queue

### Issue 1: Corpus Regression Parity Contract

Suggested title:

```text
[polish] Corpus regression parity with Manasight
```

Expected artifact:

```text
docs/contracts/polish_corpus_regression_parity_with_manasight.md
```

Scope:

- define source classes
- define report and baseline schemas
- define ratchet semantics
- define privacy policy
- define advisory vs gate behavior
- define validation commands
- define out-of-scope parser behavior changes

### Issue 2: Corpus Smoke Runner Implementation

Suggested title:

```text
[polish] Implement report-only corpus smoke runner
```

Expected scope:

- parser-only attribution
- router-level report
- JSON and terminal output
- no CI gate
- no raw private log commits

### Issue 3: Baseline And Ratchet Comparator

Suggested title:

```text
[polish] Implement corpus baseline and ratchet comparator
```

Expected scope:

- baseline schema
- comparator
- deterministic diff sorting
- regression/improvement labels
- explicit refresh flag
- tests for comparator behavior

### Issue 4: Field-Rich Corpus Metrics

Suggested title:

```text
[polish] Add field-rich corpus metrics for parser coverage
```

Expected scope:

- GameState field richness
- truncation/data loss
- deck collection invariants
- draft metrics after draft parser completion
- connection metrics
- final reconciliation counters

### Issue 5: Smoke CI And Artifact Reporting

Suggested title:

```text
[polish] Add report-only corpus smoke CI artifacts
```

Expected scope:

- run committed sanitized corpus only
- upload report artifacts
- write GitHub summary
- keep failures advisory until contract escalation
- do not auto-open baseline PRs initially

### Issue 6: Local Private Corpus Operator Command

Suggested title:

```text
[polish] Add local private corpus report command
```

Expected scope:

- accept local path
- redact local paths
- write ignored report output
- compare to local baseline
- produce issue-comment-safe summary

## Recommended Ordering

1. Write the corpus regression parity contract.
2. Implement parser-only and router-level report-only corpus runner.
3. Add baseline and ratchet comparator.
4. Add field-rich metrics.
5. Add committed sanitized fixture expansion for zero-count families.
6. Add local private corpus command.
7. Add report-only CI artifacts.
8. Consider baseline PR automation only after several manual cycles.

## Protected Surfaces

This planning artifact does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event class names
- event kind values
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- raw private logs
- generated card or tier data
- runtime status files
- failed posts
- workbook exports
- secrets, credentials, tokens, API keys, or webhook URLs
- production deployment behavior
- failing CI gates

## Open Questions

- Should Mythic Edge use the existing feature-equity corpus report as the base,
  or create a separate `smoke_corpus` tool and later merge them?
- Should the first broad baseline be committed sanitized fixtures only, or a
  local private baseline that stays ignored?
- Should optional public corpus use be considered, and if so, what license and
  privacy review is required?
- Should connection event coverage be required for parity even though Manasight's
  current smoke parser registry does not appear to include connection parsers?
- Should draft corpus coverage wait until `DraftHuman` and `DraftComplete` are
  implemented, or should `DraftBot` get a smaller first fixture pass?
- Should CI remain advisory until all parser families have nonzero committed
  sanitized coverage?

## Next Workflow Action

Recommended next role:

- Codex B for the corpus regression parity contract.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the Polish and Discipline suite.

Module:
Corpus regression parity with Manasight

Source artifacts:
- docs/problem_representations/polish_and_discipline_suite.md
- docs/problem_representations/polish_installer_setup_parity_audit.md
- docs/problem_representations/polish_corpus_regression_parity_with_manasight.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/code_hardening_drift_detector_baseline_policy.md

Task:
Create docs/contracts/polish_corpus_regression_parity_with_manasight.md.

Define the contract for Manasight-parity corpus regression tracking in Mythic
Edge. Distinguish parser-only smoke attribution, router-level corpus smoke,
stream-level smoke, baseline schema, ratchet semantics, field-rich metrics,
privacy policy, report-only/advisory behavior, CI artifact behavior, and local
private corpus handling.

Do not implement code.
Do not add fixtures, baselines, CI workflows, or parser behavior changes.
Do not commit raw Player.log files, generated data, runtime status files,
failed posts, workbook exports, secrets, credentials, webhook URLs, or local-only
machine artifacts.
Do not change parser state final reconciliation, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes, match/game identity,
deduplication, or production behavior.
```

```yaml
workflow_handoff:
  issue: "recommended new child issue: [polish] Corpus regression parity with Manasight"
  tracker: "recommended tracker: [polish] Setup polish and Python type-discipline suite"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "docs/problem_representations/polish_corpus_regression_parity_with_manasight.md"
  target_artifact: "docs/contracts/polish_corpus_regression_parity_with_manasight.md"
  risk_tier: "Medium"
  branch: "codex/polish-and-discipline-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not implement corpus tooling in the contract thread."
    - "Do not commit raw Player.log files or private corpus data."
    - "Do not add failing CI gates until a later contract explicitly escalates them."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, generated data, runtime status files, failed posts, workbook exports, or production behavior."
```
