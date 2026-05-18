# Parser Diagnostics Mode Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/49

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed parser reliability issue:
https://github.com/Tahjali11/Mythic-Edge/issues/107

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/108

Previous merge commit: `5d80789c24e2a5783f97f2ff9c5c9e147547d4c0`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Related contracts and decisions:

- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/parser_gsm_truncation.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Branch target: `codex/parser-reliability-intelligence`

This is a contract artifact only. It does not implement code, target `main`,
close tracker #47, close issue #11, change parser behavior, or change protected
runtime/workbook/webhook/App Script surfaces.

## Purpose

Parser diagnostics mode is a local observer and acceptance-report harness for a
fresh MTGA game. It should help answer:

- Did the parser keep receiving and routing log evidence during the run?
- Which event families were observed?
- Which expected event families were missing, unknown, degraded, or failed?
- Did parser-owned data-loss evidence such as `Truncation` appear?
- Did parser health look different from webhook, workbook, Apps Script, or
  transport health?
- What should a human review next, using sanitized local evidence?

Diagnostics mode is not a second parser. It must use existing parser, router,
state, drift, replay, and runtime surfaces as evidence. It must not reinterpret
raw logs independently, reconstruct missing GameState data, infer match/game
facts from incomplete evidence, or become parser truth.

## Owning Layer

Primary owner: parser reliability and local diagnostics reporting.

Truth boundary:

- `src/mythic_edge_parser/parsers/**`, `router.py`, `events.py`, and
  `app/state.py` remain the source of parser-owned interpretation and
  match/game facts.
- Diagnostics mode observes and classifies evidence from those layers.
- `app/log_drift_sensor.py` remains a routing/drift evidence helper, not a
  replacement parser.
- Workbook formulas, dashboard logic, Apps Script, webhook transport, and AI
  output remain downstream consumers and must not become diagnostic truth.
- The diagnostics report may say `pass`, `review`, `fail`, or `unknown` for
  local acceptance categories. Those labels are advisory and local; they are
  not CI gates, merge readiness, deploy readiness, tracker completion, parser
  truth, workbook truth, or AI truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_diagnostics_mode.md`

Future implementation files authorized by this contract:

- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `docs/implementation_handoffs/parser_diagnostics_mode_comparison.md`

Related files that may be read or lightly integrated without changing their
truth semantics:

- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/events.py`
- `tests/test_diagnostics.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_status_api.py`
- `tests/test_runner.py`
- `tests/test_parser_regressions.py`
- `tests/test_saved_event_replay.py`
- `tests/test_gsm_truncation_parser.py`

Out of scope unless a later contract explicitly authorizes it:

- `src/mythic_edge_parser/app/state.py` semantic changes
- parser event class changes
- workbook schema files
- webhook payload construction
- Apps Script code
- environment variable contracts
- generated local report outputs committed to the repo

## Observed Current Behavior

Observed from the current branch:

- `app/diagnostics.py` owns runtime logging, runtime status writes, webhook
  success/failure counters, event/router failure records, URL redaction, and
  safe JSON normalization.
- `app/log_drift_sensor.py` can replay a `Player.log` or log slice through
  `LineBuffer` and `Router`, returning routed/unknown counts, header counts,
  routed event kinds, unknown signatures, unmatched API names, baseline deltas,
  timestamp-missing counts, and timestamp-parse-failure counts.
- `app/status_api.py` exposes local status and runtime artifact views, but it
  does not build an acceptance report.
- `app/runner.py` updates parser state, diagnostics status, gameplay surfaces,
  analytics sidecar, local archives, debug rows, Game Log rows, MatchSummary
  rows, and Match Log rows in the live parser loop.
- `app/transforms.py` currently keeps `Truncation` events in the local archive,
  returns no sheet rows for `Truncation`, and summarizes truncation from
  normalized payload fields.
- `events.py`, `router.py`, and `parsers/truncation.py` now support
  `TruncationEvent` from issue #107.
- There is no dedicated parser diagnostics mode report artifact, no diagnostics
  report schema, and no live-game acceptance checklist encoded in the repo.

## Public Interface

Recommended public module:

`src/mythic_edge_parser/app/parser_diagnostics.py`

Required public functions:

```python
def build_parser_diagnostics_report(
    source_log: Path,
    *,
    profile: str = "live_game",
    runtime_status: dict[str, Any] | None = None,
    drift_baseline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def write_parser_diagnostics_report(
    *,
    source_log: Path,
    report_path: Path | None = None,
    profile: str = "live_game",
    drift_baseline_path: Path | None = None,
) -> ParserDiagnosticsResult:
    ...
```

Required result object:

```python
@dataclass(slots=True)
class ParserDiagnosticsResult:
    report_path: Path
    report: dict[str, Any]

    def summary_line(self) -> str:
        ...
```

Required command entrypoint:

- The module should support `python3 -m mythic_edge_parser.app.parser_diagnostics`
  or an equivalent local tool wrapper.
- Do not add a new package script to `pyproject.toml` in the first
  implementation unless Codex C finds that the repo already has an established
  local-tool pattern requiring it.
- Do not add new environment variables or change existing environment variable
  contracts.

Default output:

- If `report_path` is omitted, write to a local-only ignored artifact under
  existing `data/status/`, recommended:
  `data/status/parser_diagnostics_latest.json`.
- The report path itself is a generated local artifact and must not be
  committed.
- This default must not change the existing `manasight_status_latest.json`
  schema.

## Run Modes

### `fixture`

Purpose: deterministic test and contract validation from sanitized committed
fixtures.

Rules:

- Input must be a sanitized fixture log or synthetic log slice.
- Output may be asserted in focused tests after volatile fields are normalized.
- No raw private logs may be committed as fixtures.

### `local_log`

Purpose: local-only diagnostics against a private `Player.log` or manually
captured private log slice.

Rules:

- The source log stays local.
- The report may be written under ignored `data/status/`.
- The report must redact local paths, URLs, long tokens, UUIDs, and private
  markers.
- The report must not copy raw log lines.

### `live_game`

Purpose: after or during a fresh MTGA game, produce a local acceptance report
from current local evidence.

Rules:

- The v1 implementation should prefer a report tool that consumes the local log
  and selected local runtime status evidence rather than changing the live
  parser loop.
- If a later implementation adds a runner flag, that flag must be a wrapper
  around existing parser outputs and this report builder; it must not alter
  parser interpretation, event classes, state final reconciliation, workbook
  rows, webhook payloads, Apps Script behavior, match/game identity, or
  deduplication.
- Live-game diagnostics reports are local review artifacts, not CI gates.

## Inputs

Required inputs:

| Input | Type | Source | Notes |
| --- | --- | --- | --- |
| `source_log` | `Path` | local `Player.log` or sanitized fixture | May be private in local runs; committed tests must use sanitized fixtures. |
| `profile` | `str` | CLI/function argument | Allowed values: `fixture`, `local_log`, `live_game`. |

Optional inputs:

| Input | Type | Source | Notes |
| --- | --- | --- | --- |
| `runtime_status` | `dict[str, Any] | None` | selected fields from current runtime status | Must be sanitized and field-limited. |
| `drift_baseline` | `dict[str, Any] | None` | previous sanitized drift report | Used only to flag newly unknown signatures/API names. |
| `drift_baseline_path` | `Path | None` | local JSON file | Must be local and redacted in report output. |
| `report_path` | `Path | None` | CLI/function argument | Defaults to ignored local status path. |

Invalid inputs:

- unreadable `source_log`
- non-file `source_log`
- unknown `profile`
- malformed JSON baseline

Invalid input must produce a report with status `fail` when possible, or return
a nonzero CLI exit after printing a sanitized error. Invalid input must not
write raw log excerpts or mutate parser state.

## Report Schema

The v1 JSON report must use this logical shape:

```yaml
object: "mythic_edge_parser_diagnostics_report"
schema_version: "parser_diagnostics.v1"
generated_at: "2026-05-18T00:00:00+00:00"
profile: "live_game"
overall_status: "pass|review|fail|unknown"
summary:
  parser_status: "pass|review|fail|unknown"
  transport_status: "pass|review|fail|unknown"
  event_families_seen: 0
  routed_entries: 0
  unknown_entries: 0
  truncation_events: 0
  parser_failures: 0
  transport_failures: 0
source:
  log_display_name: "Player.log"
  source_kind: "fixture|local_log|live_game"
  source_path_redacted: "Player.log"
privacy:
  redaction_applied: true
  raw_log_lines_included: false
  raw_payloads_included: false
  webhook_urls_included: false
parser_health:
  status: "pass|review|fail|unknown"
  reasons: []
  entry_counts: {}
  timestamp_anomalies: {}
  failures: []
event_family_coverage:
  status: "pass|review|fail|unknown"
  counts_by_kind: {}
  expected_families: []
  missing_expected_families: []
  optional_families_seen: []
truncation_and_data_loss:
  status: "pass|review|fail|unknown"
  truncation_count: 0
  data_loss_events: []
unknowns_and_degradation:
  status: "pass|review|fail|unknown"
  unknown_signatures: []
  unmatched_api_names: []
  unmatched_request_api_names: []
  drift_flags: []
final_reconciliation:
  status: "pass|review|fail|unknown"
  evidence_present: []
  evidence_missing: []
  notes: []
transport_health:
  status: "pass|review|fail|unknown"
  webhook_successes: 0
  webhook_failures: 0
  failed_post_artifacts_seen: false
  notes: []
workbook_and_appscript:
  status: "unknown|review|pass|fail"
  checked: false
  notes: []
manual_checklist:
  before_run: []
  during_run: []
  after_run: []
validation_evidence:
  commands: []
  fixture_policy: "sanitized_only"
```

Field order in serialized JSON should be stable enough for tests, but consumers
must depend on keys, not raw formatting.

## Status Vocabulary

Allowed statuses:

- `pass`: no review-required evidence found for that category.
- `review`: parser continued, but evidence deserves human review.
- `fail`: local evidence indicates parser/report failure or missing critical
  acceptance evidence.
- `unknown`: the category was not checked or source evidence was unavailable.

`overall_status` rules:

- `fail` if any parser-health or input category is `fail`.
- `review` if no parser-health failure exists but any category is `review`.
- `pass` only when checked categories satisfy the selected profile.
- `unknown` only when insufficient evidence exists to classify the run.

These statuses are acceptance-report labels only. They must not fail CI, mark a
PR ready, mark a deploy ready, close an issue, close a tracker, or override
parser truth.

## Event-Family Coverage

Diagnostics mode must count every emitted event kind observed through the
existing parser/router path.

Required event-family handling:

- `GameState`: parser coverage and live game progression evidence.
- `GameResult`: game-over/result evidence when a completed game is present.
- `MatchState`: match start/completion evidence when emitted by Arena.
- `ClientAction`: client-response evidence; tracked but not universally
  required because not every diagnostic slice will contain each action.
- `Truncation`: data-loss evidence; presence must trigger `review`.
- `DetailedLoggingStatus`: runtime detailed-logging evidence.
- `ConnectionError`, `MatchConnectionState`, `TcpConnectionClose`,
  `WebSocketClosed`, and `LogFileRotated`: connection/runtime evidence.
- `EventLifecycle`, `Rank`, `Collection`, `DeckCollection`, `Inventory`,
  draft event kinds, and other durable events: optional coverage unless a
  profile or fixture expects them.

Default `live_game` expected families:

- At least one of `GameState` or `Truncation`.
- At least one game-completion evidence family for a completed-game run:
  `GameResult` or a match-completion `MatchState`.
- `DetailedLoggingStatus` should be reported when observed or inferred, but its
  absence alone is `review`, not `fail`.

Because MTGA log emission can drift, absence of a family should produce a
clear `missing_expected_event_family` drift flag before implementation treats
it as a hard failure.

## Truncation And Data-Loss Reporting

Diagnostics mode must understand the `Truncation` event from issue #107.

Required behavior:

- Count `Truncation` events separately from unknown entries.
- Include only normalized `TruncationEvent.payload` fields and metadata hashes.
- Report `data_loss=True` events under `truncation_and_data_loss`.
- Preserve `recoverable=False` as a warning that missing GameState content was
  not reconstructed.
- Aggregate `game_object_count` and `annotation_count` only as marker evidence.
- Never create recovered game objects, annotations, actions, zones, match
  identity, game identity, winners, or final reconciliation facts.

Any truncation event should make `truncation_and_data_loss.status = "review"`
unless a future contract defines a stricter acceptance profile.

## Unknown, Degraded, And Failure Classification

Diagnostics mode must classify issues without hiding uncertainty.

### Unknown

Unknown means the parser did not recognize or could not classify a signal.

Examples:

- `RouterStats.unknown > 0`
- nonempty `top_unknown_signatures`
- nonempty `top_unmatched_api_names`
- nonempty `top_unmatched_request_api_names`
- missing expected event families

Unknown evidence should usually produce `review`.

### Degraded

Degraded means the parser produced output, but evidence quality dropped.

Examples:

- `Truncation` data-loss events
- `timestamp_missing` or `timestamp_parse_failure`
- `missing_expected_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `fixture_gap`
- low-confidence or unknown field evidence from future evidence-ledger work

Degraded evidence should produce `review` unless the selected profile defines
that degradation as an acceptance failure.

### Failure

Failure means the parser/report could not complete a critical local acceptance
path.

Examples:

- unreadable source log
- report builder exception
- router failures recorded by diagnostics
- event failures recorded by diagnostics
- no routed parser events in a live-game profile after input was available
- invariant failure in final reconciliation evidence, if a future implementation
  can observe it from parser-owned outputs

Failure should produce `fail` for the affected parser-health category.

## Parser Health Versus Transport Health

Diagnostics mode must separate parser-health evidence from output transport.

Parser-health signals include:

- routed versus unknown entries
- event family coverage
- parser exceptions
- router exceptions
- timestamp anomalies
- truncation/data-loss evidence
- missing expected parser evidence
- final reconciliation evidence when available from parser-owned outputs

Transport-health signals include:

- webhook success/failure counters
- failed-post artifacts observed locally
- invalid or missing webhook target status
- status API availability
- local runtime output artifacts

Rules:

- A webhook failure is not a parser-truth failure.
- A workbook/App Script issue is not a parser-truth failure unless parser-owned
  evidence also failed.
- Transport failures may set `transport_health.status = "review"` or `"fail"`
  and `overall_status = "review"`, but they must not set
  `parser_health.status = "fail"`.
- Diagnostics must not query or mutate the live workbook or Apps Script in v1.

## Final Reconciliation Reporting

Diagnostics mode may report final reconciliation evidence only from
parser-owned outputs.

Allowed evidence:

- observed `GameResult` events
- observed match-completion `MatchState` events
- saved local event records produced by `to_serializable()`
- local match/game summary outputs produced by existing parser state/model
  code, if available without changing schema

Forbidden behavior:

- inferring a winner because the game ended
- reconstructing missing game results from truncation
- deciding match/game identity from workbook rows
- using AI, dashboard formulas, Apps Script, or webhook responses to correct
  parser final reconciliation

If final reconciliation evidence is incomplete, report `review` or `unknown`;
do not guess.

## Privacy And Redaction Rules

Diagnostics reports must be local-first and privacy-preserving.

Required rules:

- Do not include raw log lines.
- Do not include raw private payload bodies.
- Do not include webhook URLs, API keys, tokens, credentials, or environment
  variable values.
- Redact URLs using the existing redaction behavior from `app/diagnostics.py`.
- Store local paths as project-relative paths, basenames, or explicitly
  redacted display strings.
- Limit unknown signatures to sanitized signatures produced by drift tooling.
- Do not copy failed-post rows into the diagnostics report; include counts and
  redacted error summaries only.
- Do not commit generated diagnostics reports.
- Do not commit private `Player.log` files or private slices.

The report may include:

- event kind counts
- sanitized unknown signatures
- raw-bytes hashes
- redacted source names
- normalized parser payload fields that are already safe for local event
  archives

## Sanitized Fixture Policy

Tests must use sanitized committed fixtures or synthetic log snippets.

Allowed committed fixture content:

- synthetic MTGA-like headers
- minimized GRE payloads that contain no account, token, deck, or private
  identifiers
- synthetic `"[Message summarized"` truncation marker snippets
- expected report snapshots with volatile fields normalized

Forbidden committed fixture content:

- raw private `Player.log` excerpts
- local user paths
- webhook URLs
- account identifiers
- authentication tokens
- failed-post artifacts
- runtime status files from a real run
- workbook exports

Sanitized fixture tests should prove both positive and negative cases:

- healthy routed run
- unknown-entry review
- truncation/data-loss review
- router/event failure classification
- transport failure separated from parser failure
- redaction of paths and URLs

## Manual Live-Game Checklist

The implementation handoff should include this checklist, and the CLI should
make it easy to follow.

Before the run:

- Confirm the working branch is `codex/parser-reliability-intelligence`.
- Confirm no raw local logs or generated reports are staged.
- Start the normal parser runtime.
- Verify the runtime status file is updating locally.
- Decide whether the run is intended to check parser only or parser plus
  transport.

During the run:

- Play a fresh MTGA game long enough to exercise GameState evidence.
- If possible, let the game reach normal completion.
- Do not copy raw log excerpts into notes or repo files.
- Note only human-safe context such as profile, rough game count, and whether
  the parser stayed running.

After the run:

- Run diagnostics mode against the local log or selected private local slice.
- Save the generated report under ignored local `data/status/` or another
  ignored local path.
- Review `overall_status`, `parser_health`, `event_family_coverage`,
  `truncation_and_data_loss`, `unknowns_and_degradation`, and
  `transport_health` separately.
- If findings are based on private evidence, summarize them without pasting raw
  private log text.
- Route parser behavior problems to a new issue/contract rather than fixing
  them inside diagnostics mode.

## Error Behavior

Diagnostics mode must fail closed and report uncertainty.

- Missing source log: report or return `fail` with sanitized message.
- Malformed baseline JSON: continue with `review` and a sanitized warning.
- Report write failure: nonzero CLI exit with sanitized message.
- Router exception during replay: record parser-health `fail` and include
  sanitized exception type/message.
- Event processing exception in diagnostics-only aggregation: record
  parser-health `fail` and continue if possible.
- Unknown event kind in saved replay: classify as `review` unless the profile
  says it is expected to be skipped.
- Missing optional artifacts: classify as `unknown`, not `fail`.

No error path may post webhooks, update workbook rows, change parser state
final reconciliation, alter existing runtime status schema, or write raw logs
to committed paths.

## Side Effects

Allowed v1 side effects:

- Write one local diagnostics JSON report to an ignored local path.
- Print one sanitized summary line to stdout.
- Read local `Player.log` or sanitized fixture input.
- Read selected local runtime status/drift baseline files.

Forbidden v1 side effects:

- Post webhooks.
- Edit Google Sheets or Apps Script.
- Modify `manasight_status_latest.json` schema.
- Modify failed-post artifacts.
- Modify workbook exports.
- Add or change environment variables.
- Create parser event classes.
- Change parser behavior, state final reconciliation, match/game identity, or
  deduplication.
- Call OpenAI or any model provider.
- Create GitHub issues automatically.
- Mark PRs, deploys, CI, issues, or trackers ready/complete.

## Dependency Order

Codex C should work in this order:

1. Compare current diagnostics, drift, status, runner, replay, and truncation
   behavior against this contract.
2. Add report schema constants/builders in the new diagnostics module.
3. Add sanitized fixture/unit tests for report construction and classification.
4. Add the CLI/module entrypoint without changing environment variable
   contracts.
5. Add privacy/redaction tests.
6. Add implementation handoff.
7. Run focused validation.

Do not start by changing parser modules, state final reconciliation, workbook
schema, webhook output, Apps Script, event classes, match/game identity, or
deduplication.

## Compatibility

Diagnostics mode must preserve current behavior:

- Existing parser events and payloads keep their shapes.
- Existing `Truncation` behavior from #107 remains intact.
- Existing log drift reports continue to work.
- Existing runtime status file schema remains intact.
- Existing status API endpoints remain intact.
- Existing workbook row generation remains intact.
- Existing webhook behavior remains intact.
- Existing tests that do not mention diagnostics mode should keep their
  meaning.

## Tests Required

Focused tests:

```bash
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py
```

Regression and adjacent parser reliability tests:

```bash
python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py
```

Lint and documentation checks:

```bash
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
```

If branch-local selector or secret-scanner tools are unavailable, record them
as unavailable. If available, run:

```bash
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

Required test behaviors:

- healthy fixture report returns `overall_status = "pass"`
- unknown signatures produce `review`
- `Truncation` events produce data-loss `review`
- unreadable source log produces `fail`
- webhook failure affects transport health, not parser health
- missing optional runtime status produces `unknown`, not parser failure
- report output redacts local paths and webhook URLs
- report output does not include raw log lines
- generated report schema has stable v1 keys
- CLI writes a local report and prints a sanitized summary

## Acceptance Criteria

- `docs/contracts/parser_diagnostics_mode.md` exists and names truth
  boundaries, report schema, privacy rules, validation, and handoff.
- Implementation adds a local diagnostics report builder without changing
  parser behavior.
- The report separates parser health from transport/workbook/App Script health.
- Event-family coverage includes `Truncation` and data-loss reporting.
- Unknown, degraded, failure, and unavailable evidence are visibly distinct.
- Sanitized fixtures cover pass/review/fail paths.
- No raw private logs, generated reports, runtime status files, failed posts,
  workbook exports, secrets, or webhook URLs are committed.
- Diagnostics mode remains advisory and local; it is not a CI gate, merge gate,
  deploy gate, parser truth source, workbook truth source, or AI truth source.

## Open Questions

- Whether a later implementation should add a runner flag after the report
  tool has stabilized. V1 should prefer an external report command.
- Which final-reconciliation evidence should be considered mandatory for
  Best-of-1 versus Best-of-3 live-game profiles.
- Whether future evidence-ledger implementation will provide richer
  field-level confidence and finality details for this report.
- Whether a future golden replay harness should share the same report schema
  or remain separate.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #49 and docs/contracts/parser_diagnostics_mode.md.

  Goal:
  Implement the smallest coherent local parser diagnostics report harness needed to satisfy the contract. Diagnostics mode must observe existing parser/runtime evidence and produce a local-only acceptance report; it must not become a second parser or a truth source.

  Use:
    - https://github.com/Tahjali11/Mythic-Edge/issues/49
    - https://github.com/Tahjali11/Mythic-Edge/issues/47
    - https://github.com/Tahjali11/Mythic-Edge/issues/11
    - docs/contracts/parser_diagnostics_mode.md
    - docs/contracts/player_log_evidence_ledger.md
    - docs/contracts/parser_gsm_truncation.md
    - docs/agent_constitution.md
    - docs/agent_rules.yml
    - docs/codex_module_workflow.md
    - src/mythic_edge_parser/app/diagnostics.py
    - src/mythic_edge_parser/app/log_drift_sensor.py
    - src/mythic_edge_parser/app/status_api.py
    - src/mythic_edge_parser/app/runner.py
    - src/mythic_edge_parser/app/runtime_surfaces.py
    - src/mythic_edge_parser/app/saved_event_replay.py
    - src/mythic_edge_parser/app/transforms.py
    - src/mythic_edge_parser/stream.py
    - tests/test_diagnostics.py
    - tests/test_log_drift_sensor.py
    - tests/test_status_api.py
    - tests/test_runner.py
    - tests/test_gsm_truncation_parser.py

  Do:
    - Compare current behavior against the contract before editing.
    - Add a local diagnostics report builder with the contracted v1 schema.
    - Use existing parser/router/drift/runtime evidence; do not create a second parser.
    - Add sanitized fixture/unit tests for pass, review, fail, data-loss, transport separation, and privacy redaction.
    - Keep generated diagnostics reports local-only and ignored.
    - Produce docs/implementation_handoffs/parser_diagnostics_mode_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

  Do not:
    - Target main directly.
    - Close tracker #47 or related issue #11.
    - Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data committed to the repo, runtime status file schema, failed posts, or workbook exports.
    - Reconstruct missing GameState data or infer match/game facts from incomplete evidence.
    - Make diagnostics a CI gate, merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_diagnostics_mode.md"
  target_artifact: "docs/implementation_handoffs/parser_diagnostics_mode_comparison.md"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/108"
  previous_merge_commit: "5d80789c24e2a5783f97f2ff9c5c9e147547d4c0"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py tests/test_status_api.py tests/test_runner.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_saved_event_replay.py tests/test_gsm_truncation_parser.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47 or related issue #11."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data committed to the repo, runtime status file schema, failed posts, or workbook exports."
    - "Do not reconstruct missing GameState data or infer match/game facts from incomplete evidence."
    - "Do not make diagnostics a CI gate, merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source."
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_diagnostics_mode.md"
  target_artifact: "docs/implementation_handoffs/parser_diagnostics_mode_comparison.md"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/108"
  previous_merge_commit: "5d80789c24e2a5783f97f2ff9c5c9e147547d4c0"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "git diff --check"
    - "rg -n \"[[:blank:]]$\" docs/contracts/parser_diagnostics_mode.md"
    - "printf '%s\\n' docs/contracts/parser_diagnostics_mode.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47 or related issue #11."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data committed to the repo, runtime status file schema, failed posts, or workbook exports."
    - "Do not reconstruct missing GameState data or infer match/game facts from incomplete evidence."
    - "Do not make diagnostics a CI gate, merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source."
