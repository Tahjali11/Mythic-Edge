# Player.log Evidence Ledger Schema Snapshot Builder Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/175
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/173
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/174
- previous_merge_commit: cc729500a6efeb832578096cc1acc06a03221ad0
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-schema-snapshot-builder
- target_artifact: docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier3_deck_state.md
- docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md
- docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #175 defines the next narrow residual Player.log evidence-ledger layer:
a deterministic evidence-ledger schema snapshot builder.

The static evidence-ledger mapping is now seeded through Tier 7, except for
the intentionally deferred Tier 3 `deck_state` boundary. The next useful
resilience step is a reviewable snapshot artifact that records the approved
ledger schema surface so future drift reports and invariant checks can compare
against it.

Plain English: the snapshot builder should answer "did the evidence-ledger
surface change?" It should not answer "is the parser semantically correct?",
"is this safe to merge?", "is this safe to deploy?", "did Arena never drift?",
or "should this baseline be auto-updated?"

This contract documents future snapshot behavior only. It must not change
parser behavior, parser state final reconciliation, parser event classes,
router semantics, diagnostics report shape, runtime status schema, drift report
implementation, invariant execution, golden replay behavior, feature-equity
behavior, card-performance calculations, workbook schema, webhook payload
shape, Apps Script behavior, output transport, runtime artifacts, Match
Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync
behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates,
merge policy, or deploy policy.

## Relationship To Prior Work

`docs/contracts/player_log_evidence_ledger.md` sketched future schema snapshot,
drift report, and invariant layers. Issue #175 implements only the contract for
the schema snapshot builder. It does not implement drift reports, invariant
execution, runtime field-evidence attachment, or runtime/status reporting.

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
the machine-readable evidence-ledger object shape, vocabulary constants,
validators, and privacy posture. The snapshot builder observes that validated
ledger shape; it does not replace or reinterpret it.

`docs/contracts/player_log_evidence_ledger_tier3_deck_state.md` remains
authoritative for the intentionally deferred `deck_state` boundary. A snapshot
must preserve the presence of deferred fields and boundary notes without
turning `deck_state` into a seeded truth field.

`docs/contracts/player_log_evidence_ledger_tier6_runtime_health_drift.md` and
`docs/contracts/player_log_evidence_ledger_tier7_derived_analytics.md` remain
authoritative for runtime-health, drift, and derived-analytics provenance
boundaries. A snapshot may record their stable entry IDs and schema paths, but
it must not treat those report outputs as CI, merge, deploy, workbook,
analytics, or AI truth.

`docs/contracts/code_hardening_parser_event_schema_snapshots.md` and
ADR-0004 provide the durable snapshot policy precedent: snapshots are
deterministic review artifacts; update mode must be opt-in; snapshot diffs
require issue, contract, and review approval; volatile/private content is
forbidden.

## Owning Layer

Owning layer: parser resilience / evidence-ledger schema snapshot metadata.

Truth boundary:

- `src/mythic_edge_parser/app/evidence_ledger.py` owns current ledger metadata,
  vocabulary, output families, entries, evidence signals, validators, privacy
  policy, and copy-safe ledger serialization.
- The future snapshot builder owns deterministic projection of that ledger
  schema surface into a sanitized committed snapshot and an optional local
  comparison report.
- Parser modules and parser state remain truth producers for event
  interpretation, match facts, game facts, identity, final reconciliation, and
  parser-owned classification.
- Golden replay, feature-equity corpus ratchet, parser diagnostics, and log
  drift sensor may consume snapshot results later, but issue #175 must not wire
  those consumers.
- Workbook, webhook, Apps Script, Match Journal, overlay, SQLite, Google
  Sheets, analytics, AI/model-provider output, CI, merge/deploy policy, and
  production behavior remain downstream or out of scope.

The snapshot builder must not become:

- a parser
- a ledger authoring surface
- a drift-report evaluator
- an invariant executor
- a fixture replayer
- a live-log scanner
- a runtime status reporter
- a workbook/App Script validator
- a CI, merge, or deploy authority
- a baseline auto-updater
- an AI or analytics truth source

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- tools/build_evidence_schema_snapshot.py
- tests/test_evidence_schema_snapshot.py
- tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json
- docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- tests/test_event_schema_snapshots.py
- tests/fixtures/schema_snapshots/
- tools/check_protected_surfaces.py

## Public Interface

Future implementation should create an evidence-ledger-specific module:

```python
src/mythic_edge_parser/app/evidence_schema_snapshot.py
```

Required constants:

```python
EVIDENCE_SCHEMA_SNAPSHOT_OBJECT = "mythic_edge_player_log_evidence_schema_snapshot"
EVIDENCE_SCHEMA_SNAPSHOT_VERSION = "player_log_evidence_schema_snapshot.v1"
EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_OBJECT = "mythic_edge_player_log_evidence_schema_snapshot_comparison"
EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_VERSION = "player_log_evidence_schema_snapshot_comparison.v1"
EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH = Path(
    "tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json"
)
UPDATE_ENV_VAR = "MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT"
```

Required public functions:

```python
def build_evidence_schema_snapshot(
    ledger: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def compare_evidence_schema_snapshot(
    current: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> dict[str, Any]:
    ...

def load_expected_evidence_schema_snapshot(
    path: Path = EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH,
) -> dict[str, Any]:
    ...

def write_evidence_schema_snapshot(
    path: Path,
    snapshot: Mapping[str, Any],
) -> None:
    ...

def main(argv: Sequence[str] | None = None) -> int:
    ...
```

Recommended CLI/tool wrapper:

```text
tools/build_evidence_schema_snapshot.py
```

Recommended CLI modes:

- `--check`: build the current snapshot, compare with the expected committed
  snapshot, and return nonzero on `diff` or `fail`.
- `--write PATH`: write the current snapshot to an explicit local path.
- `--update`: update the expected committed snapshot only when
  `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1` is set.
- No default mode may update committed snapshots.

The CLI is local tooling. A failing check is evidence for review; it is not by
itself semantic parser truth, CI policy, merge readiness, or deploy readiness.

## Inputs

Allowed inputs:

- The in-memory result of `evidence_ledger.build_player_log_evidence_ledger()`.
- Optional explicit expected snapshot JSON path under
  `tests/fixtures/evidence_schema_snapshots/`.
- Optional explicit local output path for a generated review artifact.

Allowed imported code:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- Python standard-library modules for deterministic JSON serialization,
  hashing, paths, mappings, and CLI argument parsing.

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

V1 should not read golden replay manifests, feature-equity baselines, parser
diagnostics reports, or drift reports directly. It may capture ledger-declared
`fixture_refs`, tests, recommended review modules, and source paths as stable
schema strings. A later contract may add report/corpus snapshot sections.

## Snapshot Output Shape

Required snapshot object:

```yaml
object: "mythic_edge_player_log_evidence_schema_snapshot"
schema_version: "player_log_evidence_schema_snapshot.v1"
snapshot_version: 1
snapshot_id: "sha256:<canonical-content-hash>"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/175"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
ledger:
  object: "mythic_edge_player_log_evidence_ledger"
  schema_version: "player_log_evidence_ledger_schema.v1"
  ledger_version: "player_log_evidence_ledger.v1"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  branch_target: "codex/parser-reliability-intelligence"
  related_adrs: []
privacy:
  raw_private_logs_included: false
  raw_payload_values_included: false
  local_absolute_paths_included: false
  runtime_artifacts_included: false
  generated_data_included: false
  source_paths_are_repo_relative_or_symbolic: true
summary:
  output_family_count: 7
  entry_count: 0
  evidence_signal_count: 0
  direct_evidence_signal_count: 0
  fallback_evidence_signal_count: 0
  deferred_output_fields: []
vocabulary:
  value_sources: []
  confidence_levels: []
  finality_labels: []
  drift_flags: []
  invariant_statuses: []
output_families:
  - tier: 1
    output_family: "match_identity_and_lifecycle"
    status: "seeded_sample"
    seed_fields: []
    future_fields: []
    owner_modules: []
entries:
  - entry_id: "tier1.match_identity.match_id"
    tier: 1
    output_family: "match_identity_and_lifecycle"
    output_field: "match_id"
    display_name: "MTGA Match ID"
    parser_owner: "src/mythic_edge_parser/app/state.py"
    model_surface: "MatchSummary.to_match_log_row"
    downstream_surfaces: []
    parser_managed_truth: true
    coverage_status: "seeded_sample"
    direct_signal_ids: []
    fallback_signal_ids: []
    value_source_policy: {}
    confidence_policy: {}
    finality_policy: {}
    invariant_checks: []
    drift_flags: []
    recommended_review_modules: []
    tests: []
    fixture_refs: []
evidence_signals:
  - entry_id: "tier1.match_identity.match_id"
    evidence_kind: "direct"
    signal_id: "match_state.match_id"
    parser_event_kind: "MatchState"
    parser_event_type: "match_started"
    raw_event_family: "matchGameRoomStateChangedEvent"
    raw_message_type: ""
    normalized_payload_path: "payload.match_id"
    raw_payload_path: "matchGameRoomStateChangedEvent.gameRoomInfo.matchId"
    required_for_final: true
    value_source_when_used: "observed"
    confidence_when_used: "high"
    finality_when_used: "live"
    allowed_types: []
    privacy_class: "path_only_no_values"
snapshot_policy:
  deterministic: true
  update_mode_default: "disabled"
  update_env_var: "MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT"
  auto_update_allowed: false
  comparison_authority: "review_signal_only"
limitations: []
```

### Snapshot ID Policy

`snapshot_id` should be a SHA-256 hash over the canonical snapshot payload with
`snapshot_id` temporarily omitted or set to an empty string. The hash must not
include timestamps, local paths, current user names, machine names, git commit
SHAs, runtime values, or environment values.

The snapshot must not include `generated_at`, `updated_at`, current date/time,
current git branch, current git commit, current user, current machine, or local
working-tree status. Those values belong in local run logs or implementation
handoffs, not in committed deterministic snapshots.

## Included Stable Fields

The snapshot must include only stable schema strings, booleans, integers, and
ordered lists derived from the evidence ledger:

- ledger object, schema version, ledger version, source issue, parent issue,
  branch target, and related ADR paths
- vocabulary values:
  - value sources
  - confidence levels
  - finality labels
  - drift flags
  - invariant statuses
- output family records:
  - tier
  - output family
  - status
  - seed fields
  - future fields
  - owner modules
- entry records:
  - entry ID
  - tier
  - output family
  - output field
  - display name
  - parser owner
  - model surface
  - downstream surfaces
  - parser-managed-truth flag
  - coverage status
  - direct signal IDs
  - fallback signal IDs
  - value-source policy
  - confidence policy
  - finality policy
  - invariant checks
  - drift flags
  - recommended review modules
  - tests
  - fixture references
- evidence signal records:
  - entry ID
  - evidence kind: `direct` or `fallback`
  - signal ID
  - parser event kind
  - parser event type
  - raw event family
  - raw message type
  - normalized payload path
  - raw payload path
  - required-for-final boolean
  - value source when used
  - confidence when used
  - finality when used
  - allowed type labels
  - privacy class

The snapshot should include `missing_behavior` only if Codex C can keep the
content stable and free of private values. If included, it must be treated as
schema/boundary text and tested for forbidden content. If omitted in v1, the
contract tests must still verify missing behavior through
`tests/test_evidence_ledger.py`.

The snapshot should not include long prose notes or degradation behavior by
default. Those remain validated in focused evidence-ledger tests. This keeps
the committed snapshot from becoming a noisy Markdown-prose diff surface.

## Excluded Or Forbidden Fields

The snapshot must not include:

- raw Player.log lines
- raw nested Player.log payload values
- private sanitized fixture contents
- `EventMetadata.raw_bytes`
- `raw_bytes_hash` values
- timestamps or generated dates
- git commit SHA or current branch values
- local absolute paths
- current user or machine names
- environment variable values
- runtime status file contents
- failed-post contents
- webhook URLs
- API keys, tokens, credentials, secrets
- workbook exports
- raw workbook IDs, spreadsheet IDs, deployment tags, live workbook state
- generated card data, generated tier data, or local cache contents
- card-performance generated artifacts
- feature-equity generated reports
- diagnostics generated reports
- drift generated reports
- golden replay generated reports
- Apps Script deployment output
- OpenAI/model-provider output
- AI summaries
- analytics recommendations
- gameplay advice
- player-mistake labels
- hidden-card inference
- archetype classification

Forbidden or volatile snippets must be rejected by tests. The forbidden text
policy should at least cover:

- `"[UnityCrossThreadLogger]"`
- `"[Client GRE]"`
- `"DETAILED LOGS:"`
- `"script.google.com/macros/"`
- webhook-looking URLs
- `"Bearer "`
- `"api_key"`
- `"secret"`
- `"token"`
- `"/Users/"`
- `"C:\\Users\\"`
- `"data/runtime_logs/"`
- `"data/failed_posts/"`
- `"data/status/"`
- `"data/generated/"`

## Determinism And Sorting

Required JSON formatting:

- UTF-8 text
- two-space indentation
- deterministic key order
- trailing newline
- no generated timestamp
- no platform-specific path separator

Required ordering:

- Preserve evidence-ledger output family order by tier.
- Preserve seed-field and future-field order from the ledger, because that
  order is contract-visible.
- Preserve value-source, confidence, finality, drift, and invariant vocabulary
  order from the ledger constants.
- Preserve each entry's direct-evidence and fallback-evidence signal order.
- Sort only order-insensitive aggregate indexes, if Codex C adds any.

The snapshot builder must not mutate the ledger returned by
`build_player_log_evidence_ledger()`.

## Comparison Report Shape

Required comparison object:

```yaml
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
diff:
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
privacy:
  forbidden_content_findings: []
  local_absolute_paths_found: []
drift_flags: []
review_required: false
limitations: []
```

Allowed status values:

- `pass`: current and expected snapshots match and no privacy findings exist.
- `diff`: snapshots differ in stable schema content.
- `fail`: expected snapshot is missing or malformed, current ledger is invalid,
  forbidden/private content is detected, or comparison cannot complete.

No `ok` status is required for this builder. Use `pass` to mirror snapshot-test
language and keep it distinct from feature-equity `ok`.

Comparison status is a review signal only. It is not parser semantic
correctness, CI truth, merge readiness, deploy readiness, tracker completion,
or automatic baseline approval.

## Snapshot Storage And Update Policy

Required committed expected snapshot path:

```text
tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json
```

Required focused test path:

```text
tests/test_evidence_schema_snapshot.py
```

Required update behavior:

- Missing expected snapshot must fail focused tests with a clear policy message
  unless update mode is explicitly enabled.
- Snapshot mismatch must fail focused tests with a clear policy message.
- Update mode must be opt-in only.
- The required update environment variable is:
  `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1`.
- Update mode must never be the default.
- Update mode must not read raw logs, runtime files, failed posts, workbook
  exports, generated data, secrets, live workbook state, OpenAI/model-provider
  output, or local analytics artifacts.
- The update failure message must tell future agents not to auto-update the
  snapshot without issue, contract, and review approval.

Recommended failure message content:

```text
Evidence schema snapshot mismatch. Do not auto-update evidence schema snapshots.
Snapshot changes require explicit issue, contract, and review approval.
After approval only, set MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1 and rerun
tests/test_evidence_schema_snapshot.py.
```

Snapshot updates require explicit approval.

A snapshot diff may be approved only when all are true:

- A GitHub issue or contract authorizes the ledger schema drift.
- The PR drift budget names the drift as authorized or accepted residual drift.
- Codex E review or contract-test report confirms the snapshot diff is
  intentional.
- Protected-surface gate output is recorded and any warnings are explicitly
  cited.
- The update does not include forbidden volatile content.

Not enough for approval:

- tests pass
- snapshot changed after refactor
- AI/codegen updated it
- update command produced the diff
- workbook accepted the payload
- comparison status is `diff`

## Error Behavior

Malformed current ledger:

- `build_evidence_schema_snapshot()` should validate the ledger first.
- If validation fails, the builder must not silently create a clean snapshot.
- The CLI/check path should return `fail` or nonzero and report validation
  errors without dumping private data.

Missing expected snapshot:

- Comparison status should be `fail`.
- Focused tests should fail with the snapshot policy message.
- Missing expected snapshot must not auto-create a new baseline without the
  update environment variable and approval.

Snapshot diff:

- Comparison status should be `diff`.
- Diff output should name added, removed, or changed output families, entries,
  evidence signals, vocabulary, and policies.
- Diff output should not include raw payload values.
- Diff output must not authorize updating the baseline.

Forbidden content:

- Any forbidden/private/volatile content in the generated snapshot or expected
  snapshot is `fail`.
- Forbidden findings should identify the section/key or high-level category,
  not reproduce the private value.

Contract ambiguity:

- If Codex C cannot decide whether a stable field belongs in the snapshot, it
  should keep the field out, document the reason in the handoff, and route to
  Codex B for contract clarification if the omission affects comparison value.

## Side Effects

Allowed for Codex C:

- Add `src/mythic_edge_parser/app/evidence_schema_snapshot.py`.
- Add `tools/build_evidence_schema_snapshot.py`.
- Add `tests/test_evidence_schema_snapshot.py`.
- Add the committed expected snapshot JSON under
  `tests/fixtures/evidence_schema_snapshots/`.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md`.

Forbidden for Codex C:

- Changing evidence-ledger entries or vocabulary except where required by an
  explicit review finding in the implementation thread. The expected
  implementation should be snapshot-only.
- Changing parser behavior, diagnostics, drift, golden replay, feature-equity,
  card-performance, workbook, webhook, Apps Script, runtime, Match Journal,
  overlay, SQLite, Google Sheets sync, analytics, AI, or model-provider
  behavior.
- Adding runtime field-evidence attachment.
- Adding invariant execution.
- Adding drift report evaluation.
- Adding CI gates, merge gates, deploy gates, or automatic issue generation.
- Reading, copying, summarizing, or committing raw private logs or local
  artifacts.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_schema_snapshot.py` should prove:

- `build_evidence_schema_snapshot()` returns the contracted top-level object,
  schema version, snapshot version, privacy block, summary block, vocabulary
  block, output family records, entry records, evidence signal records, and
  snapshot policy block.
- The snapshot validates the current evidence ledger before projecting it.
- Snapshot generation is deterministic across repeated calls.
- `snapshot_id` is stable and computed from canonical content excluding the
  `snapshot_id` field.
- The committed expected snapshot matches the generated current snapshot.
- Missing expected snapshot fails with a policy message unless update mode is
  enabled.
- Snapshot mismatch fails with a policy message unless update mode is enabled.
- Update mode is disabled unless
  `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1`.
- The snapshot excludes timestamps, git commit, current branch, local paths,
  runtime artifact contents, raw logs, raw payload values, failed posts,
  workbook exports, generated data, secrets, webhook URLs, and AI/model
  provider output.
- Comparison reports added, removed, and changed output families, entries,
  evidence signals, vocabulary, and policies without raw values.
- The snapshot preserves Tier 3 `deck_state` as deferred and does not seed
  fake deck-state truth.
- The snapshot preserves Tier 6 and Tier 7 report/analytics boundaries without
  promoting them to CI, merge, deploy, workbook, analytics, or AI truth.

Focused tests in `tests/test_evidence_ledger.py` should continue to pass.

Recommended validation for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
python3 -m ruff check src tests tools
git diff --check
```

Protected-surface validation when available:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
src/mythic_edge_parser/app/evidence_schema_snapshot.py
tools/build_evidence_schema_snapshot.py
tests/test_evidence_schema_snapshot.py
tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json
docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md
EOF
```

Documentation-only validation for this Codex B pass:

```bash
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
EOF
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
  exists.
- The contract defines a deterministic evidence-ledger-specific snapshot
  builder, expected snapshot path, comparison report shape, update policy,
  privacy rules, protected surfaces, validation expectations, and Codex C
  handoff.
- The contract authorizes only snapshot-builder code, tests, one committed
  expected snapshot fixture, an optional CLI wrapper, and implementation
  handoff docs.
- The contract forbids raw/private/volatile content in snapshots.
- The contract forbids automatic baseline updates.
- The contract keeps snapshot comparison as review evidence only, not parser
  truth, CI truth, merge readiness, deploy readiness, tracker completion, or
  automatic drift approval.
- The contract does not reopen completed Tier 1 through Tier 7 mapping slices.
- The contract preserves the intentionally deferred Tier 3 `deck_state`
  boundary.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- A future schema v2 may want to snapshot `missing_behavior` and
  `degradation_behavior` prose. V1 should avoid long prose snapshots unless
  Codex C can prove they remain stable and useful.
- A future drift-report contract must decide how to consume snapshot comparison
  output and how to map changed schema surfaces to affected ledger entries.
- A future invariant contract must decide which invariant names become
  executable checks.
- A future runtime/status contract may expose snapshot IDs or comparison
  summaries locally. Issue #175 does not authorize that exposure.
- A future contract may add golden replay, feature-equity, diagnostics, or
  drift-report snapshot sections. V1 should not read those generated reports.

## Suspected Gaps

- No `src/mythic_edge_parser/app/evidence_schema_snapshot.py` module exists.
- No `tools/build_evidence_schema_snapshot.py` wrapper exists.
- No `tests/test_evidence_schema_snapshot.py` exists.
- No committed evidence-ledger schema snapshot fixture exists.
- Existing parser event schema snapshots cover event/payload/workbook/runtime
  row surfaces, not evidence-ledger provenance surfaces.
- Existing evidence-ledger tests validate current ledger content, but they do
  not provide a committed JSON baseline for future diff comparison.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #175, the Player.log evidence-ledger schema snapshot builder under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/175
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/173
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/174
- Previous merge commit: cc729500a6efeb832578096cc1acc06a03221ad0
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the schema snapshot builder contract. Implement only the smallest coherent snapshot-builder code, test, expected fixture, optional tool wrapper, and handoff needed to satisfy the contract.

Do:
- Verify the branch is based on codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Add a deterministic evidence-ledger-specific snapshot builder, preferably at src/mythic_edge_parser/app/evidence_schema_snapshot.py.
- Add a local tool wrapper, preferably tools/build_evidence_schema_snapshot.py.
- Add focused tests, preferably tests/test_evidence_schema_snapshot.py.
- Add one committed expected snapshot fixture at tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json.
- Snapshot only stable evidence-ledger schema surfaces: vocabulary, output families, seed/future fields, entry IDs, output fields, evidence signal IDs, normalized/raw payload paths, policy maps, drift flags, invariant names, recommended review modules, tests, and fixture refs.
- Exclude raw/private/volatile content, timestamps, local paths, runtime artifacts, generated data, workbook exports, secrets, webhook URLs, AI/model-provider output, and live external state.
- Keep update mode opt-in only through MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Do not implement drift report evaluation, invariant execution, runtime field-evidence attachment, diagnostics/golden replay/feature-equity integration, runtime status exposure, CI gates, merge/deploy gates, or automatic issue generation.
- Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth.
- Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths.
- Do not auto-update snapshots without explicit issue, contract, and review approval.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_schema_snapshot.py
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_event_schema_snapshots.py
- python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
- python3 -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, snapshot module, tool wrapper, focused tests, expected snapshot fixture, and implementation handoff if the tool is available.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/175"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/173"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/174"
  previous_merge_commit: "cc729500a6efeb832578096cc1acc06a03221ad0"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md"
  verdict: "schema_snapshot_builder_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-schema-snapshot-builder"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not implement drift report evaluation, invariant execution, runtime field-evidence attachment, diagnostics/golden replay/feature-equity integration, runtime status exposure, CI gates, merge/deploy gates, or automatic issue generation."
    - "Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth."
    - "Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
    - "Do not auto-update snapshots without explicit issue, contract, and review approval."
```
