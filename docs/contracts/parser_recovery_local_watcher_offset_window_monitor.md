# Parser Recovery Local Watcher Offset-Window Monitor Contract

## Module

Local watcher and offset-window monitor boundary for parser recovery planning.

Plain English: this contract defines how a future Mythic Edge helper may
observe an explicitly selected local source label and track file metadata for
approved windows without copying raw Player.log or UTC_Log content into the
repository. The monitor may describe source generations, offset windows,
rotation, truncation, recreation, archive, stale windows, buffering pressure,
and non-blocking watcher errors. It must not read private logs in this
contract pass, run private checks, promote fixtures, change parser behavior,
or claim watcher correctness or parser readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/452
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/451
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/538
- Previous merge commit: `892843a35cfd201fc10e6c6a68549c609817dd4f`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- The local `main` checkout was one commit behind `origin/main` and had an
  unrelated untracked copy of the #451 contract artifact. To avoid overwriting
  unrelated local state, this pass inspected `origin/main` directly instead of
  pulling.
- `origin/main` was
  `892843a35cfd201fc10e6c6a68549c609817dd4f`.
- Issue #452 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Issue #451 was closed and PR #538 was merged into `main`.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #452
- Tracker #388
- Parent issue #434
- Issue #451 and PR #538
- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `src/mythic_edge_parser/log/tailer.py`
- `tests/test_tailer.py`
- adjacent watcher, drift, runtime-surface, UTC_Log adapter, local-harvest,
  field-evidence, and private-evidence files by focused path search

No private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop,
packet, OS/router, diagnostics, drift, watcher, tailer, or private smoke data
was run, read, tailed, hashed, copied, summarized, or inspected.

## Observed Current Behavior

Issue #451 added a static Field Recovery Matrix helper:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`

The matrix is report-only metadata. It preserves:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
```

Existing tailer behavior:

- `FileTailer.open_from_start(...)` and `FileTailer.open_from_end(...)`
  establish content-reading offsets.
- `FileTailer.poll_once()` reads bytes from the selected path and parses log
  entries.
- `FileTailer` detects a size decrease as rotation and resets buffered parser
  line state.
- Existing tests cover synthetic temporary files, rotation by truncation, UTF-8
  replacement, partial entry buffering, sanitized missing-file errors, and
  offloaded file checks.

Existing local app watcher contracts define browser-visible readiness,
process-control safeguards, and live diagnostics. Those contracts are
reference-only for this issue. They do not authorize this parser-recovery
contract to start a live watcher, tail private logs, start the parser runner,
write SQLite rows, expose browser controls, or alter local app behavior.

Existing private-evidence offset-window work defines process vocabulary for
future approved private windows, but its first implementation was docs-only
and did not add executable offset capture.

No dedicated parser-recovery local watcher / offset-window monitor module,
schema, tests, or report artifact exists before this contract.

## Problem

The parser evidence-pipeline and recovery workflow need a safe way to describe
which bytes were newly available during an approved local source window. That
requires file metadata and source-generation tracking, but the surrounding
surface is high risk because it sits next to private logs, live watchers,
tailing, parser runtime behavior, drift reports, and fixture promotion.

Without a contract, a future implementation could accidentally:

- use an active private Player.log or UTC_Log checkout without approval;
- read raw private log content while trying to collect offsets;
- print exact private paths, offsets, file sizes, timestamps, hashes, or raw
  line snippets into committed artifacts;
- treat a watcher event as parser truth or recovery proof;
- treat rotation, truncation, or stale-window detection as live watcher
  correctness;
- promote a recovery packet, fixture, corpus row, or parser behavior claim;
- change `FileTailer`, parser runtime, local app live watcher behavior, or
  downstream workbook/analytics surfaces.

The first bad value is any watcher or offset-window metadata being used as
parser truth, fixture-promotion proof, corpus status movement, private smoke
success, recovery readiness, release readiness, production behavior, analytics
truth, AI truth, or coaching truth.

## Scope Decision

This contract approves a future synthetic-only metadata implementation.

Codex C may implement a side-effect-light helper and focused tests that model
local source metadata and offset-window status using synthetic temporary files
or in-memory metadata only. The implementation may define source labels,
source generations, window start/end metadata, rotation/truncation/recreate
classifiers, buffer-pressure status, and validation errors.

Codex C must not run against real private Player.log, UTC_Log, app-data, live
MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, watcher,
tailer, or private smoke sources.

Codex C must not integrate the helper into parser runtime, `FileTailer`,
`MtgaEventStream`, local app live watcher controls, diagnostics reports,
corpus metadata, fixture promotion, workbook transport, analytics, AI,
coaching, CI gates, release gates, or production behavior.

This contract does not authorize:

- private source discovery;
- private source content reads;
- active watcher startup;
- parser runner startup;
- local app endpoint changes;
- local offset-state file writing;
- recovery packet writing;
- fixture creation or promotion;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Parser Reliability and Quality /
Governance support.

Corpus / Provenance owns the recovery-window metadata vocabulary, local-only
artifact boundary, and relationship to future harvest/review/fixture-promotion
workflows.

Parser owns log entry interpretation, parser events, routing, parser state,
match/game identity, deduplication, final reconciliation, and existing
`FileTailer` behavior.

Generated / Local Artifacts owns any future local-only source selection,
offset state, recovery packet, or private review output if separately
authorized.

Quality / Governance owns workflow routing, stop conditions, protected-surface
checks, secret/private-marker checks, and review gates.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser Reliability, for existing tailer and drift concepts.
- Generated / Local Artifacts, for future local-only offset state.
- Quality / Governance, for validation and protected-surface policy.

This contract is not a live parser capture contract, not a local app watcher
contract, not a diagnostics report contract, not a fixture-promotion contract,
not a workbook/transport contract, not an analytics contract, not an AI or
coaching contract, not a CI gate, and not a release/deploy/production gate.

## Truth Owner

Truth owner for parser log entry and live tailing behavior remains:

- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- their focused tests and future scoped parser contracts

Truth owner for field recovery category policy remains:

- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`

Truth owner for private evidence execution boundaries remains:

- issue #434;
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`;
- later explicit private-evidence issues, contracts, privacy reviews, and user
  approvals.

This contract owns only recovery-window metadata vocabulary and allowed future
synthetic validation scope. It does not own parser facts, private evidence,
fixture expected output, corpus status, local app status, runtime status,
merge readiness, deploy readiness, release readiness, production behavior,
analytics truth, AI truth, coaching truth, or tracker completion.

## Bridge-Code Status

`deferred_future_boundary`

This Codex B pass authorizes no bridge code.

If later implemented, the helper may become shared support from Generated /
Local Artifacts and Corpus / Provenance to future recovery review workflows.

Allowed future data flow:

```text
explicit symbolic source selection + synthetic or approved local file metadata
  -> local watcher / offset-window metadata object
  -> future harvest candidate or recovery review packet, if separately authorized
```

Forbidden reverse flow:

```text
offset-window monitor
  -/-> parser value overwrite
  -/-> FileTailer behavior change
  -/-> live watcher startup
  -/-> workbook or webhook shape change
  -/-> diagnostics or drift truth
  -/-> analytics / AI / coaching truth
  -/-> fixture promotion
  -/-> corpus status promotion
  -/-> #388 activation
```

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`

Future Codex C files authorized by this contract:

- `src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py`
- `tests/test_local_watcher_offset_window_monitor.py`
- `docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md`

Expected future Codex E review artifact:

- `docs/contract_test_reports/parser_recovery_local_watcher_offset_window_monitor.md`

Files Codex C may read but must not modify in this slice:

- `src/mythic_edge_parser/log/tailer.py`
- `tests/test_tailer.py`
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
- `tests/test_field_recovery_matrix.py`
- existing parser-evidence, private-evidence, live-app watcher, diagnostics,
  drift, runtime-surface, and local-harvest contracts and tests

Not owned by this contract:

- raw Player.log files;
- raw or normalized UTC_Log files;
- local private offset state;
- private app-data contents;
- live watcher outputs;
- runtime status files;
- diagnostics or drift reports;
- recovery packets;
- fixture files;
- golden replay manifests;
- expected-output files;
- corpus manifest or session ledger files;
- workbook exports;
- SQLite files;
- screenshots;
- raw hashes;
- exact private paths;
- exact private offsets, byte sizes, or timestamps from real local sources;
- secrets, credentials, tokens, API keys, or webhook URLs.

## Public Interface

The future helper interface should be internal Python metadata support only. It
must not add a CLI, web route, environment variable, local app browser surface,
runtime status shape, parser event, workbook column, webhook payload, Apps
Script surface, corpus status, or fixture schema.

Recommended future object constants:

- `LOCAL_WATCHER_OFFSET_WINDOW_OBJECT`
- `LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION`
- `LOCAL_WATCHER_SOURCE_OBJECT`
- `LOCAL_WATCHER_WINDOW_OBJECT`
- `LOCAL_WATCHER_EVENT_OBJECT`

Recommended future functions:

```python
describe_source_selection(...)
start_offset_window(...)
finish_offset_window(...)
classify_source_transition(...)
summarize_update_buffer(...)
validate_offset_window_monitor_report(...)
```

Those names are guidance, not a required signature. Codex C may choose a
smaller interface if it preserves the contract vocabulary and tests.

## Inputs

Allowed inputs for Codex C:

- synthetic temporary files created inside tests;
- in-memory source metadata dictionaries;
- symbolic source labels such as `player_log_primary` or
  `utc_log_candidate_a`;
- coarse source classes: `player_log`, `normalized_utc_log`,
  `synthetic_player_log`, `synthetic_utc_log`;
- synthetic file metadata: size, modification-time label, generation label,
  inode-like synthetic token, archive marker, and deletion marker;
- synthetic update event records from tests;
- reduced local-harvest and field-recovery metadata objects;
- public issue, PR, contract, handoff, and test references.

Forbidden inputs:

- private Player.log or UTC_Log content;
- exact private local paths;
- raw private hashes;
- exact private offsets, sizes, timestamps, inode values, filesystem IDs, or
  archive names from real local sources;
- private app-data contents;
- live MTGA sources;
- network, firewall/drop, packet, OS/router, or private smoke evidence;
- diagnostics, drift, watcher, or tailer runs against private data;
- workbook exports, SQLite databases, screenshots, decklists, strategy notes,
  generated card data, credentials, tokens, API keys, or webhook URLs.

## Source Selection Requirements

Every source selection must be explicit and symbolic.

Required source fields:

- `source_label`: public-safe symbolic label, not a path;
- `source_class`: `player_log`, `normalized_utc_log`, `synthetic_player_log`,
  or `synthetic_utc_log`;
- `privacy_class`: `synthetic`, `public_fixture`, `private_local`, or
  `local_only_redacted`;
- `selection_mode`: `synthetic_test`, `operator_selected_local`,
  `approved_private_window`, or `blocked_missing_approval`;
- `approval_issue`: required for any non-synthetic local source;
- `contents_read`: always false for metadata-only monitor objects;
- `raw_path_included`: always false for committed objects;
- `raw_hash_included`: always false for committed objects.

If a non-synthetic source lacks approval, the monitor must return
`blocked_missing_approval` or raise a closed-form error before collecting
metadata.

## Offset-Window Metadata

A future monitor may track start and end metadata for a source window.

Allowed committed or test-safe fields:

- `window_id`: symbolic label;
- `source_label`: symbolic label;
- `source_generation`: symbolic generation token;
- `window_mode`: `read_from_start`, `tail_from_now`, `offset_bounded`,
  `metadata_only`, or `blocked`;
- `start_marker_status`;
- `end_marker_status`;
- `offset_range_status`;
- `source_transition_status`;
- `stale_window_status`;
- `buffer_status`;
- `backpressure_status`;
- `error_status`;
- `contents_read`: false;
- `local_state_written`: false unless a later contract explicitly authorizes
  local-only state writing.

Local-only fields that must not be committed from real private sources:

- exact start offset;
- exact end offset;
- exact file size;
- exact modification timestamp;
- exact inode, file ID, or filesystem generation ID;
- exact private archive name;
- exact private path;
- raw hash;
- raw byte range;
- raw log line;
- raw payload.

## Status Vocabulary

Source generation statuses:

- `new_source_generation`
- `same_source_generation`
- `rotated_generation`
- `truncated_generation`
- `recreated_generation`
- `archived_generation`
- `deleted_or_unavailable`
- `unknown_generation`

Window statuses:

- `window_ready`
- `window_in_progress`
- `window_closed`
- `window_unavailable`
- `window_stale`
- `window_degraded`
- `window_blocked_missing_approval`
- `window_manual_review_required`

Offset range statuses:

- `offset_range_valid`
- `offset_range_empty`
- `offset_range_unavailable`
- `offset_range_reversed`
- `offset_range_crosses_generation`
- `offset_range_manual_review_required`

File transition statuses:

- `file_unchanged`
- `file_appended`
- `file_size_decreased`
- `file_recreated`
- `file_rotated_or_archived`
- `file_deleted`
- `file_metadata_unavailable`

Watcher update statuses:

- `update_observed`
- `update_coalesced`
- `update_dropped_due_to_backpressure`
- `update_skipped_stale_window`
- `update_blocked_missing_approval`
- `update_manual_review_required`

Backpressure statuses:

- `buffer_ok`
- `buffer_near_limit`
- `buffer_over_limit_degraded`
- `buffer_dropped_updates`
- `buffer_unknown`

Error statuses:

- `no_error`
- `non_blocking_error`
- `permission_denied`
- `source_disappeared`
- `metadata_unavailable`
- `event_stream_unavailable_polling`
- `polling_unavailable`
- `manual_review_required`

## Read From Start Versus Tail From Now Policy

The monitor must keep replay/harvest and live-watch concepts separate.

- `read_from_start` may be used only for synthetic tests or later explicitly
  approved local replay/harvest windows.
- `tail_from_now` may be used only for synthetic tests or future explicitly
  approved local monitoring windows.
- The default for private local sources must be `blocked_missing_approval`,
  not `read_from_start`.
- A helper must not call `FileTailer.open_from_start(...)`,
  `FileTailer.open_from_end(...)`, or tailer polling methods in this slice.
- A helper must not read source bytes to decide its mode.

## File-System Event And Polling Policy

The contract allows a future design to model both file-system events and
polling fallback, but Codex C must not add platform-specific watcher
dependencies or start real file-system event streams in this slice.

Required policy:

- file-system events are hints, not truth;
- polling metadata snapshots are fallback evidence, not parser truth;
- disagreement between event and polling snapshots must produce
  `manual_review_required` or `window_degraded`;
- watcher errors must be reported as non-blocking metadata unless they prevent
  even metadata collection;
- any future platform watcher must preserve a polling fallback and symbolic
  status vocabulary.

## Buffer And Backpressure Policy

A future monitor must use bounded update metadata.

Required fields or equivalent:

- `buffer_capacity`;
- `queued_update_count`;
- `dropped_update_count`;
- `coalesced_update_count`;
- `backpressure_status`;
- `oldest_update_status`;
- `newest_update_status`.

If capacity is exceeded, the helper must prefer degraded/review status over
pretending the window is complete.

Backpressure is operational metadata only. It is not parser truth, live
watcher correctness, drift health, fixture proof, or readiness evidence.

## Scan And Token-Size Limits

The monitor must define limits before any future line or range inspection is
authorized.

For this slice:

- content scanning is forbidden;
- token-size limits apply only to metadata objects and test data;
- oversized metadata should produce `metadata_limit_exceeded` or
  `manual_review_required`;
- a future content-inspection contract must define maximum byte ranges,
  truncation behavior, redaction, and private-artifact retention separately.

## Local Artifact And Output Root Policy

This contract does not authorize writing local offset state.

If a later contract authorizes local state, it must:

- live outside Git;
- use a local-only output root;
- avoid exact private path display in committed artifacts;
- keep exact offsets, sizes, timestamps, and raw source identifiers local-only;
- provide deletion/retention guidance;
- require secret/private-marker validation before any public summary is
  committed.

Codex C for this issue may write only source code, focused tests, and an
implementation handoff if implementation is separately requested.

## Relationship To #439 Offset-Window Process

Issue #439 defined an offset-capture process for private-evidence windows and
authorized only docs/template support. This #452 contract turns the same
privacy posture into a parser-recovery monitor boundary.

Shared rules:

- symbolic source/window labels only in committed artifacts;
- exact private offsets, sizes, timestamps, paths, hashes, and raw content stay
  local-only;
- approval is required before any private source metadata collection;
- offset metadata does not promote corpus rows or prove parser behavior.

Different scope:

- #439 was corpus private-evidence process scaffolding.
- #452 is parser-recovery window-monitor metadata scaffolding for future
  field recovery and harvest workflows.

## Relationship To #451 Field Recovery Matrix

The Field Recovery Matrix may consume future reduced window-monitor statuses
as review context, but not as parser fact evidence by itself.

Allowed relationship:

```text
offset-window status
  -> recovery review context
  -> field recovery matrix review-required path
```

Forbidden relationship:

```text
offset-window status
  -/-> direct recovery category
  -/-> parser output restoration
  -/-> high-confidence parser truth
```

## Relationship To #453-#456 Recovery Workflow

This contract preserves #453 through #456 as later workflow stages. It does
not solve them.

Expected later stages may define:

- recovery review packet consumption;
- recovery proof or issue-draft generation;
- approved fixture-promotion linkage;
- Codex F/G handoff support.

Those stages require their own issues/contracts before implementation.

## Invariants

- Public or committed artifacts must never contain raw private log content.
- Public or committed artifacts must never contain exact private paths,
  offsets, file sizes, timestamps, inode/file IDs, archive names, raw hashes,
  or byte ranges from real private sources.
- Private source metadata collection requires explicit issue/contract/user
  approval.
- Source labels must be symbolic and public-safe.
- `contents_read` must be false for monitor metadata in this slice.
- `parser_behavior_ready` remains false.
- `pipeline_activation_ready_for_issue_388` remains false.
- `private_harvest_authorized` remains false.
- `fixture_promotion_authorized` remains false.
- `corpus_status_change_authorized` remains false.
- Non-direct, degraded, blocked, stale, approximate, watcher, offset-window,
  or review-required signals must not become parser truth.
- Watcher success must not be claimed from synthetic or metadata-only tests.

## Error Behavior

If approval is missing for a non-synthetic source, stop before collecting
metadata and return `window_blocked_missing_approval`.

If the source label is not symbolic or contains path-like material, reject it
without echoing the supplied value.

If file metadata is unavailable, return `file_metadata_unavailable` and
`window_degraded` or `window_manual_review_required`.

If an end marker precedes a start marker, return `offset_range_reversed` and
do not summarize the range.

If a source generation changes during a window, return
`offset_range_crosses_generation` and require review.

If update buffering overflows, return `buffer_over_limit_degraded` or
`buffer_dropped_updates` and require review.

If a watcher event stream fails but polling metadata is available, report
`event_stream_unavailable_polling` and continue metadata-only review.

If both watcher events and polling metadata are unavailable, return
`metadata_unavailable` and fail closed.

## Side Effects

Allowed in this Codex B pass:

- create or update this contract only.

Allowed in a future Codex C implementation, if requested:

- add a pure metadata helper;
- add focused synthetic/temp-file tests;
- add an implementation handoff.

Forbidden in this Codex B pass and not authorized for Codex C by default:

- run private watcher/tailer checks;
- read private Player.log or UTC_Log content;
- collect real private offsets or file sizes;
- write local offset state;
- write recovery packets;
- edit corpus manifest or session ledger;
- create fixtures, expected outputs, or golden replay manifests;
- start parser runner or local app watcher;
- change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  behavior.

## Dependency Order

Recommended future implementation order:

1. Add vocabulary constants and metadata dataclasses or dictionaries.
2. Add source-label and privacy validation.
3. Add source-transition classification from synthetic metadata snapshots.
4. Add start/end window classification.
5. Add buffer/backpressure summary classification.
6. Add validators that reject private markers and readiness overclaims.
7. Add synthetic/temp-file tests only.
8. Add implementation handoff.

Do not integrate with parser runtime, local app watcher, diagnostics, drift,
harvest reports, review packets, fixtures, or corpus metadata in this issue.

## Compatibility

Existing `FileTailer` behavior must remain unchanged.

Existing local app live watcher status and process-control behavior must
remain unchanged.

Existing UTC_Log source adapter and local harvest candidate report behavior
must remain unchanged.

Existing #388 planning semantics and false readiness flags must remain
unchanged.

This contract adds no new environment variables, config keys, command-line
flags, public routes, schema migrations, workbook columns, webhook fields, or
Apps Script behavior.

## Tests Required

Future Codex C should run:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py
PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
python3 -m ruff check src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md \
  src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py \
  tests/test_local_watcher_offset_window_monitor.py \
  docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md \
  src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py \
  tests/test_local_watcher_offset_window_monitor.py \
  docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Codex C may run the full test suite if focused tests pass and time permits,
but must not run private/live/local watcher checks.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`.
- Contract defines source selection, symbolic source labels, start/end window
  metadata, generation statuses, rotation/truncation/recreate/archive
  behavior, stale-window behavior, read mode policy, event/polling policy,
  buffer/backpressure behavior, error behavior, scan limits, local artifact
  policy, validation expectations, and stop conditions.
- Contract authorizes only synthetic/temp-file metadata implementation.
- Contract does not authorize private log reads, active watcher runs, parser
  runtime integration, local app endpoint changes, fixture promotion, corpus
  status changes, or readiness claims.
- Contract includes a Codex C handoff and workflow handoff.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Codex C may implement only the synthetic/temp-file metadata helper and tests
authorized by this contract.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #452.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/452

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md

Base branch:
main

Goal:
Implement the synthetic/temp-file metadata helper and focused tests for the
local watcher offset-window monitor boundary. Stay inside the contract.

Allowed implementation surface:
- src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py
- tests/test_local_watcher_offset_window_monitor.py
- docs/implementation_handoffs/parser_recovery_local_watcher_offset_window_monitor_comparison.md

Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, or
private smoke sources. Do not start a watcher, start the parser runner, call
FileTailer open/poll methods from the new helper, create local offset state,
write recovery packets, create fixtures, edit corpus metadata, change parser
behavior, change local app behavior, promote rows, activate #388/#381, or
claim parser_behavior_ready or pipeline_activation_ready_for_issue_388.

Required validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_local_watcher_offset_window_monitor.py
- PYTHONPATH=src python3 -m pytest -q tests/test_tailer.py
- PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
- python3 -m ruff check src/mythic_edge_parser/app/local_watcher_offset_window_monitor.py tests/test_local_watcher_offset_window_monitor.py
- git diff --check
- python3 tools/check_agent_docs.py
- path-scoped secret/private-marker and protected-surface checks for changed files
```

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
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #452 problem representation"
  target_artifact: "docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md"
  verdict: "local_watcher_offset_window_monitor_contract_ready_for_synthetic_metadata_implementation"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_scope: "synthetic_temp_file_metadata_helper_and_tests_only"
  stop_conditions:
    - "Do not close #452, #388, or #434."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, or private smoke checks."
    - "Do not create committed fixtures, golden replay manifests, expected outputs, fixture-promotion packets, proof files, metadata diff files, recovery packets, issue/fixture drafts, local watcher outputs, offset state, local/generated artifacts, or corpus metadata edits."
    - "Do not promote blocked, report-only, private-evidence, external-boundary, approximate, fallback, watcher, offset-window, or review-required signals to parser truth."
    - "Do not change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics behavior, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, release readiness, production behavior, or final integration policy."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, field recovery readiness, private smoke success, watcher correctness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
