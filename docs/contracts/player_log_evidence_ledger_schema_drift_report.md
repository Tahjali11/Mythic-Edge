# Player.log Evidence Ledger Schema Drift Report Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/177
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/175
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/176
- previous_merge_commit: 19c95a134029de4eb278a5f4d51a2e816c2e1ff2
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-schema-drift-report
- target_artifact: docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related authority:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #177 defines the next residual Player.log evidence-ledger layer: a
report-only schema drift evaluator for the evidence-ledger schema snapshot.

Issue #175 already added a deterministic snapshot builder and a comparison
object that can say whether the current evidence-ledger schema surface matches
the approved committed snapshot. This contract defines a narrow report layer
that consumes that comparison and answers:

> What stable evidence-ledger schema surfaces changed compared with the
> approved snapshot, and what should a reviewer inspect?

It must not answer:

- whether parser behavior is semantically correct
- whether a PR is ready to merge
- whether a deployment is ready
- whether a snapshot update is approved
- whether Arena did or did not drift
- whether runtime, workbook, webhook, Apps Script, analytics, AI, or model
  provider behavior changed

Plain English: the snapshot comparison is the smoke alarm. The drift report is
the note taped beside it that says which rooms to inspect. It is not the fire
chief, the building code, or permission to repaint the house.

## Relationship To Prior Work

`docs/contracts/player_log_evidence_ledger.md` sketched future schema snapshot
and drift-report layers. Issue #177 implements only a schema drift report for
the evidence-ledger snapshot surface, not the broader live Player.log drift
system.

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
the evidence-ledger object, vocabulary, validators, and privacy posture.

`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md` remains
authoritative for the snapshot builder, expected snapshot fixture, update
policy, and snapshot comparison object. The schema drift report must consume
that comparison instead of reimplementing snapshot comparison.

`src/mythic_edge_parser/app/log_drift_sensor.py` and
`src/mythic_edge_parser/app/parser_diagnostics.py` remain live-log and
diagnostics reporting surfaces. Issue #177 must not wire schema drift reports
into those runtime reports.

ADR-0004 remains authoritative for protected-surface and snapshot-change
policy: a diff is review evidence, not automatic authorization.

## Owning Layer

Owning layer: parser resilience / evidence-ledger schema review metadata.

Truth boundary:

- `src/mythic_edge_parser/app/evidence_ledger.py` owns current
  evidence-ledger metadata and vocabulary.
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py` owns deterministic
  projection and comparison of the evidence-ledger schema surface.
- The new schema drift report layer owns review-oriented summarization of that
  comparison.
- Parser modules and parser state remain truth producers for event
  interpretation, match facts, game facts, identity, final reconciliation, and
  parser-owned classification.
- The report is local review evidence only. It is not parser truth, runtime
  truth, workbook truth, CI truth, merge readiness, deploy readiness, tracker
  completion, baseline approval, analytics truth, AI truth, or model-provider
  truth.

The schema drift report must not become:

- a parser
- a ledger authoring surface
- a snapshot updater
- an invariant executor
- a fixture replayer
- a live-log scanner
- a diagnostics or runtime status writer
- a workbook/App Script validator
- a CI, merge, or deploy gate
- an automatic GitHub issue creator
- an AI or analytics truth source

## Observed Current Behavior

Observed from `origin/codex/parser-reliability-intelligence` at
`19c95a134029de4eb278a5f4d51a2e816c2e1ff2`:

- Issue #11 is open as the Player.log evidence-ledger and parser-resilience
  tracker.
- Issue #177 is open.
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py` exists and exposes:
  - `build_evidence_schema_snapshot()`
  - `compare_evidence_schema_snapshot()`
  - `load_expected_evidence_schema_snapshot()`
  - `write_evidence_schema_snapshot()`
  - `main()`
- `tools/build_evidence_schema_snapshot.py --check` emits a
  `mythic_edge_player_log_evidence_schema_snapshot_comparison` JSON object.
- The current committed expected snapshot matches the generated current
  snapshot with comparison status `pass`.
- The current snapshot summary contains 7 output families, 71 entries, 448
  evidence signals, and the intentionally deferred field
  `tier3.game_level_facts.deck_state`.
- Snapshot comparison statuses are `pass`, `diff`, and `fail`.
- Snapshot comparison already reports added, removed, and changed output
  families, entries, evidence signals, vocabulary, and policies, while
  suppressing raw values.
- No evidence-ledger schema drift report module exists.
- No schema drift report CLI wrapper exists.
- No focused schema drift report tests exist.
- No report artifact is currently committed or generated by default.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_schema_drift_report.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_schema_drift_report.py
- tools/build_evidence_schema_drift_report.py
- tests/test_evidence_schema_drift_report.py
- docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_schema_drift_report.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- tools/build_evidence_schema_snapshot.py
- tests/test_evidence_schema_snapshot.py
- tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py

## Public Interface

Recommended module:

```python
src/mythic_edge_parser/app/evidence_schema_drift_report.py
```

Required constants:

```python
EVIDENCE_SCHEMA_DRIFT_REPORT_OBJECT = "mythic_edge_player_log_evidence_schema_drift_report"
EVIDENCE_SCHEMA_DRIFT_REPORT_VERSION = "player_log_evidence_schema_drift_report.v1"
EVIDENCE_SCHEMA_DRIFT_REPORT_STATUSES = ("pass", "review", "fail")
```

Required public functions:

```python
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


def build_evidence_schema_drift_report(
    comparison: Mapping[str, Any],
    *,
    current_snapshot: Mapping[str, Any] | None = None,
    expected_snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...


def build_current_evidence_schema_drift_report(
    *,
    expected_snapshot_path: Path | None = None,
) -> dict[str, Any]:
    ...


def write_evidence_schema_drift_report(
    path: Path,
    report: Mapping[str, Any],
) -> None:
    ...


def main(argv: Sequence[str] | None = None) -> int:
    ...
```

Allowed implementation form:

- pure functions returning JSON-serializable dictionaries
- standard-library-only CLI wrapper
- optional internal helpers for affected-entry and recommendation extraction

Required behavior regardless of implementation form:

- Importing the module must have no filesystem, network, environment, GitHub,
  workbook, webhook, Apps Script, runtime-status, local-log, OpenAI, or model
  provider side effects.
- `build_evidence_schema_drift_report()` must consume the existing snapshot
  comparison shape. It must not reimplement snapshot diffing.
- Builders must be deterministic and must not include volatile timestamps, git
  commit SHAs, branch names, working-tree status, hostnames, local usernames,
  current absolute paths, or environment variable values.
- Builders must not include raw snapshot record values beyond stable IDs,
  repo-relative module paths, test paths, vocabulary names, policy names, and
  diff key lists already allowed by the snapshot comparison contract.
- Malformed caller-provided payloads must produce report status `fail` rather
  than uncaught exceptions.

Recommended CLI/tool wrapper:

```text
tools/build_evidence_schema_drift_report.py
```

Recommended CLI modes:

- `--check`: build the current evidence-ledger snapshot, compare it with the
  committed expected snapshot, and print the schema drift report as JSON.
- `--expected PATH`: compare against an explicit expected snapshot path.
- `--comparison PATH`: build a report from an existing snapshot comparison
  JSON file, without rebuilding snapshots.
- `--out PATH`: write the JSON report to an explicit local path.
- `--markdown-out PATH`: optionally write a sanitized Markdown summary to an
  explicit local path.

Required CLI exit behavior:

- Return `0` for report status `pass`.
- Return `0` for report status `review`, because this tool is review evidence
  and must not become a CI, merge, or deploy gate by default.
- Return nonzero for report status `fail`.
- Never update the committed expected snapshot.
- Never set or require `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT`.

## Inputs

Allowed inputs:

- The in-memory result of
  `evidence_schema_snapshot.compare_evidence_schema_snapshot()`.
- The in-memory current and expected schema snapshots, solely to enrich
  affected entry, output family, recommended review module, and test lists.
- Optional explicit expected snapshot JSON path under
  `tests/fixtures/evidence_schema_snapshots/`.
- Optional explicit comparison JSON path produced by the snapshot builder.
- Optional explicit local report output paths.

Forbidden inputs:

- raw private Player.log files
- sanitized or synthetic fixture log contents
- live local MTGA logs
- runtime status files
- failed posts
- workbook exports
- generated card/tier/cache data
- local runtime artifacts
- live workbook state
- deployed Apps Script state
- webhook URLs
- environment variable values
- secrets, credentials, tokens, API keys
- OpenAI/model-provider output
- AI summaries
- external metagame data

V1 must not read golden replay manifests, feature-equity reports, parser
diagnostics reports, log drift reports, runtime status files, or workbook
exports directly. It may name those modules or tests only when the evidence
ledger snapshot already lists them as stable review references.

## Output Shape

Required report object:

```yaml
object: "mythic_edge_player_log_evidence_schema_drift_report"
schema_version: "player_log_evidence_schema_drift_report.v1"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/177"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
status: "pass"
review_required: false
status_reasons: []
comparison:
  object: "mythic_edge_player_log_evidence_schema_snapshot_comparison"
  schema_version: "player_log_evidence_schema_snapshot_comparison.v1"
  status: "pass"
  expected_snapshot_id: "sha256:..."
  current_snapshot_id: "sha256:..."
summary:
  output_family_changes: 0
  entry_changes: 0
  evidence_signal_changes: 0
  vocabulary_changes: 0
  policy_changes: 0
  privacy_findings: 0
  forbidden_content_findings: 0
  limitation_count: 0
  affected_output_family_count: 0
  affected_entry_count: 0
  affected_evidence_signal_count: 0
  recommended_review_module_count: 0
  recommended_test_count: 0
drift:
  added_output_families: []
  removed_output_families: []
  changed_output_families: []
  added_entries: []
  removed_entries: []
  changed_entries: []
  added_evidence_signals: []
  removed_evidence_signals: []
  changed_evidence_signals: []
  changed_vocabulary: []
  changed_policies: []
affected:
  output_families: []
  entries: []
  evidence_signals: []
review_guidance:
  recommended_review_modules: []
  recommended_tests: []
  review_notes: []
drift_flags: []
privacy:
  forbidden_content_findings: []
  local_absolute_paths_found: []
  raw_private_logs_included: false
  raw_payload_values_included: false
  local_absolute_paths_included: false
  runtime_artifacts_included: false
  generated_data_included: false
protected_surface_assertions:
  parser_behavior_changed: false
  parser_state_final_reconciliation_changed: false
  parser_event_classes_changed: false
  runtime_status_schema_changed: false
  diagnostics_report_shape_changed: false
  golden_replay_behavior_changed: false
  feature_equity_behavior_changed: false
  workbook_schema_changed: false
  webhook_payload_shape_changed: false
  apps_script_behavior_changed: false
  output_transport_changed: false
  analytics_or_ai_truth_changed: false
limitations: []
```

Required status values:

- `pass`: snapshot comparison status is `pass`, no diff, no privacy findings,
  and no report input/tool limitations exist.
- `review`: snapshot comparison status is `diff`, the diff is usable, and a
  human reviewer should inspect affected schema surfaces. This is not failure
  by itself.
- `fail`: snapshot comparison status is `fail`, comparison input is malformed,
  privacy/forbidden content is detected, expected snapshot cannot be read,
  current snapshot cannot be built, or the report cannot be produced
  trustworthily.

Required status mapping:

```text
snapshot comparison pass -> drift report pass
snapshot comparison diff -> drift report review
snapshot comparison fail -> drift report fail
unknown or malformed comparison status -> drift report fail
privacy findings in any report input -> drift report fail
```

## Drift Categorization And Review Guidance

The report must preserve the snapshot comparison's diff categories:

- `added_output_families`
- `removed_output_families`
- `changed_output_families`
- `added_entries`
- `removed_entries`
- `changed_entries`
- `added_evidence_signals`
- `removed_evidence_signals`
- `changed_evidence_signals`
- `changed_vocabulary`
- `changed_policies`

The report must derive affected surfaces by stable IDs only:

- `affected.output_families` is the sorted union of changed family IDs plus
  output families associated with affected entries or evidence signals when
  current/expected snapshots are provided.
- `affected.entries` is the sorted union of affected entry IDs plus entry IDs
  parsed from affected evidence signal keys and policy keys.
- `affected.evidence_signals` contains snapshot comparison evidence-signal
  keys in the existing `entry_id:evidence_kind:signal_id` form.

Review guidance must be deterministic:

- Prefer `recommended_review_modules` and `tests` listed on affected current
  or expected snapshot entries.
- If affected entries cannot be resolved, fall back to:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
  - `tests/test_evidence_ledger.py`
  - `tests/test_evidence_schema_snapshot.py`
- If vocabulary changes, include `docs/contracts/player_log_evidence_ledger_schema.md`.
- If output family changes, include `docs/contracts/player_log_evidence_ledger.md`.
- If privacy findings exist, include
  `src/mythic_edge_parser/app/evidence_schema_snapshot.py` and
  `tests/test_evidence_schema_snapshot.py`.

The report may reuse existing evidence-ledger drift flags, but it must not
invent new drift flags in issue #177. Recommended mapping:

- any diff: `changed_signal_type`
- malformed or missing expected/current snapshot: `schema_snapshot_missing`
- privacy or forbidden content findings: `sensitive_evidence_redacted`
- removed expected entries or signals: `missing_expected_payload_path`
- added entries or signals: `new_unknown_payload_path`

Detailed drift category lists remain the primary review evidence. Drift flags
are compact labels only and must not collapse the detailed report.

## Privacy And Sanitization

Required privacy posture:

- The report must never include raw private Player.log excerpts.
- The report must never include raw payload values.
- The report must never include webhook URLs, API keys, tokens, credentials,
  secrets, local absolute paths, runtime status contents, failed post contents,
  workbook exports, generated card data, OpenAI/model-provider output, or AI
  summaries.
- Privacy findings may identify paths such as
  `expected.entries[0].parser_owner` but must not reproduce the offending
  value.
- Markdown output, if implemented, must follow the same redaction and path-only
  rules as JSON output.
- Writing a report to an explicit local path must scan the report for
  forbidden/private snippets before writing.

Required forbidden snippets and patterns should stay aligned with the snapshot
builder, including:

- `[UnityCrossThreadLogger]`
- `[Client GRE]`
- `DETAILED LOGS:`
- `script.google.com/macros/`
- webhook URLs
- bearer tokens
- `api_key`
- `secret`
- `token`
- `/Users/`
- `C:\Users\`
- `data/runtime_logs/`
- `data/failed_posts/`
- `data/status/`
- `data/generated/`

## Error Behavior

Malformed comparison payload:

- Report status must be `fail`.
- `status_reasons` should include `malformed_comparison`.
- The report must not raise uncaught exceptions for caller-provided mappings.

Unknown comparison status:

- Report status must be `fail`.
- `status_reasons` should include `unknown_comparison_status`.

Missing or malformed expected snapshot when using the current-report builder:

- Report status must be `fail`.
- `drift_flags` should include `schema_snapshot_missing`.
- The report must not create or update any baseline.

Snapshot diff:

- Report status must be `review`.
- `review_required` must be `true`.
- The report must name affected stable IDs and review targets.
- The report must not imply that updating the snapshot is approved.

Privacy or forbidden content:

- Report status must be `fail`.
- The report may include finding paths and counts only.
- The report must not echo the private value.

Contract ambiguity:

- If Codex C cannot determine whether a review note belongs in the report, it
  should keep the report minimal, document the omission in the implementation
  handoff, and route back to Codex B if the omission blocks useful review.

## Side Effects

Allowed for Codex C:

- Add `src/mythic_edge_parser/app/evidence_schema_drift_report.py`.
- Add `tools/build_evidence_schema_drift_report.py`.
- Add `tests/test_evidence_schema_drift_report.py`.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md`.
- Optionally produce a local uncommitted report by explicit `--out` or
  `--markdown-out` path while validating manually.

Forbidden for Codex C:

- Changing evidence-ledger entries, vocabulary, or the committed expected
  snapshot unless a separate contract/review loop explicitly authorizes it.
- Updating `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`.
- Changing parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics report shape, runtime status schema,
  log drift report behavior, invariant execution, golden replay behavior,
  feature-equity behavior, card-performance calculations, workbook schema,
  webhook payload shape, Apps Script behavior, output transport, ActionLogRow
  shape, match/game identity, deduplication, Match Journal behavior, overlay
  behavior, SQLite behavior, Google Sheets sync behavior, production behavior,
  analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge
  policy, deploy policy, secrets, environment variables, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or local runtime
  artifacts.
- Adding runtime field-evidence attachment.
- Adding invariant execution.
- Wiring schema drift reports into diagnostics, golden replay, feature-equity,
  log drift sensor, runtime status, workbook export, webhook delivery, or CI.
- Adding automatic GitHub issue or tracker updates.
- Reading, copying, summarizing, or committing raw private logs or local
  artifacts.

## Dependency Order

Implementation should proceed in this order:

1. Add a pure report builder that consumes a supplied snapshot comparison.
2. Add affected-surface and review-guidance extraction from optional current
   and expected snapshots.
3. Add privacy scanning for report inputs and output.
4. Add a CLI wrapper that builds current comparison through the existing
   snapshot builder or reads an explicit comparison JSON.
5. Add focused tests for pass, review, fail, privacy, malformed input, CLI
   exit behavior, and no snapshot update behavior.
6. Produce the implementation handoff.

Do not edit the snapshot builder unless a focused implementation issue proves
that a tiny compatibility helper is required. If such a helper changes the
snapshot comparison shape, route back to Codex B first.

## Compatibility

The report must remain compatible with the #175 snapshot comparison shape:

- `object`
- `schema_version`
- `status`
- `expected_snapshot_id`
- `current_snapshot_id`
- `summary`
- `diff`
- `privacy`
- `drift_flags`
- `review_required`
- `limitations`

The report must not rename snapshot comparison statuses. It may map them to
report statuses as specified above.

The report must not require every future evidence-ledger field to have an
entry-level recommendation. Missing recommendations should fall back to generic
review modules/tests rather than fail the report.

The report must not require a committed report fixture. Focused tests should
use synthetic in-memory comparison payloads and temporary output paths.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_schema_drift_report.py` should prove:

- A `pass` snapshot comparison produces a `pass` drift report with
  `review_required: false`.
- A `diff` snapshot comparison produces a `review` drift report with
  `review_required: true`.
- A `fail` snapshot comparison produces a `fail` drift report.
- Malformed comparison input produces a `fail` report without uncaught
  exceptions.
- Unknown comparison status produces a `fail` report.
- The report preserves all snapshot comparison diff category lists.
- The report derives affected entries from changed entries, changed evidence
  signal keys, and changed policy keys.
- The report derives affected output families from changed families and
  affected entries when snapshots are supplied.
- Recommended review modules and tests come from affected snapshot entries when
  available and fall back to generic evidence-ledger/snapshot targets when not.
- Privacy findings are path-only and never echo private values.
- Writing a report rejects forbidden/private/volatile snippets.
- CLI `--check` returns `0` for `pass` and `review`, nonzero for `fail`.
- CLI `--out` writes only to an explicit path.
- CLI does not update the expected snapshot and does not require or set
  `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT`.

Focused existing tests should continue to pass:

```bash
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
```

Recommended validation for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_schema_drift_report.py
python3 tools/build_evidence_schema_drift_report.py --check
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
python3 -m ruff check src tests tools
git diff --check
```

Protected-surface validation when available:

```bash
printf '%s\n' \
  docs/contracts/player_log_evidence_ledger_schema_drift_report.md \
  src/mythic_edge_parser/app/evidence_schema_drift_report.py \
  tools/build_evidence_schema_drift_report.py \
  tests/test_evidence_schema_drift_report.py \
  docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Documentation-only validation for this Codex B pass:

```bash
git diff --check
printf '%s\n' \
  docs/contracts/player_log_evidence_ledger_schema_drift_report.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_schema_drift_report.md` exists.
- The contract defines a local report-only schema drift evaluator that consumes
  the #175 snapshot comparison object.
- The contract defines report status mapping from snapshot comparison
  `pass/diff/fail` to report `pass/review/fail`.
- The contract defines report shape, privacy rules, protected surfaces,
  validation expectations, and Codex C handoff.
- The contract authorizes only report-builder code, optional CLI wrapper,
  focused tests, and implementation handoff docs.
- The contract forbids committed report artifacts by default.
- The contract forbids snapshot baseline updates.
- The contract keeps schema drift reports as review evidence only, not parser
  truth, CI truth, merge readiness, deploy readiness, tracker completion, or
  automatic drift approval.
- The contract preserves the intentionally deferred Tier 3 `deck_state`
  boundary.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- A future issue may decide whether schema drift reports should be attached to
  diagnostics, golden replay, feature-equity, or runtime status reports. Issue
  #177 does not authorize that integration.
- A future issue may define a broader live Player.log drift report that combines
  log drift sensor output, diagnostics, truncation, feature equity, and schema
  drift. Issue #177 is schema-snapshot-only.
- A future issue may decide whether Markdown reports are worth standardizing.
  JSON is the required durable shape for issue #177.
- A future issue may add CI usage. Issue #177 deliberately keeps default CLI
  `review` status non-failing so the report remains advisory.

## Suspected Gaps

- No `src/mythic_edge_parser/app/evidence_schema_drift_report.py` module
  exists.
- No `tools/build_evidence_schema_drift_report.py` wrapper exists.
- No `tests/test_evidence_schema_drift_report.py` exists.
- The existing snapshot comparison is intentionally compact and does not yet
  expand changed schema IDs into reviewer-facing modules and tests.
- The current snapshot comparison `diff` status fails the snapshot check, which
  is correct for baseline protection, but there is no separate local report
  that explains the diff without becoming a gate.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #177, the Player.log evidence-ledger schema drift report under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/177
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/175
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/176
- Previous merge commit: 19c95a134029de4eb278a5f4d51a2e816c2e1ff2
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_schema_drift_report.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md

Goal:
Compare the current evidence-ledger snapshot implementation and focused tests against the schema drift report contract. Implement only the smallest coherent local report builder, optional CLI wrapper, focused tests, and implementation handoff needed to satisfy the contract.

Do:
- Verify the branch is based on codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Add a pure schema drift report builder, preferably at src/mythic_edge_parser/app/evidence_schema_drift_report.py.
- Consume the existing evidence_schema_snapshot.compare_evidence_schema_snapshot() result instead of reimplementing snapshot comparison.
- Map snapshot comparison pass/diff/fail to drift report pass/review/fail.
- Add deterministic affected-entry, affected-family, recommended-review-module, and recommended-test summaries based on stable snapshot IDs and entry metadata only.
- Add a local tool wrapper, preferably tools/build_evidence_schema_drift_report.py.
- Add focused tests, preferably tests/test_evidence_schema_drift_report.py.
- Keep CLI review status advisory: --check should return 0 for pass and review, and nonzero only for fail.
- Preserve privacy: report finding paths and counts only, never raw private values, raw payload values, logs, local absolute paths, secrets, webhook URLs, runtime artifacts, workbook exports, generated data, or AI/model-provider output.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not implement parser behavior changes.
- Do not change parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, log drift report behavior, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Do not update tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json.
- Do not change evidence-ledger entries or vocabulary unless a separate contract/review loop explicitly authorizes it.
- Do not wire schema drift reports into diagnostics, golden replay, feature-equity, log drift sensor, runtime status, workbook export, webhook delivery, or CI.
- Do not add invariant execution, runtime field-evidence attachment, merge/deploy gates, automatic tracker updates, or automatic GitHub issue creation.
- Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth.
- Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_schema_drift_report.py
- python3 tools/build_evidence_schema_drift_report.py --check
- python3 -m pytest -q tests/test_evidence_schema_snapshot.py
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
- python3 -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, drift report module, tool wrapper, focused tests, and implementation handoff if the tool is available.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/177"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/175"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/176"
  previous_merge_commit: "19c95a134029de4eb278a5f4d51a2e816c2e1ff2"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_schema_drift_report.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_schema_drift_report_comparison.md"
  verdict: "schema_drift_report_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-schema-drift-report"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_schema_drift_report.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not implement parser behavior changes."
    - "Do not change parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, log drift report behavior, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not update tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json."
    - "Do not change evidence-ledger entries or vocabulary unless a separate contract/review loop explicitly authorizes it."
    - "Do not wire schema drift reports into diagnostics, golden replay, feature-equity, log drift sensor, runtime status, workbook export, webhook delivery, or CI."
    - "Do not add invariant execution, runtime field-evidence attachment, merge/deploy gates, automatic tracker updates, or automatic GitHub issue creation."
    - "Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
```
