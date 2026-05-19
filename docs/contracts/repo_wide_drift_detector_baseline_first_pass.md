# Repo-Wide Drift Detector Baseline First Pass Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/96

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch target: `codex/repo-wide-hardening-run`

Related policy issue: https://github.com/Tahjali11/Mythic-Edge/issues/70

Related first golden fixture issue: https://github.com/Tahjali11/Mythic-Edge/issues/94

This is a contract-writing artifact only. It does not implement code, create
fixtures, generate or refresh drift baselines, change detector behavior, add
failing CI gates, target `main`, or mark tracker #82 complete.

## Module

Repo-wide drift detector baseline first pass.

Plain English: this issue should prove that Mythic Edge can commit one tiny,
normalized drift-report reference derived from an already committed sanitized
fixture. The committed reference is a reviewable expected output for a focused
test. It is not a local runtime baseline, not a live `Player.log` drift gate,
and not permission to refresh detector baselines automatically.

## Owning Layer

Owning layer: repo-wide hardening fixture and drift-report reference
governance.

Truth boundary:

- MTGA `Player.log` is local observable evidence, not absolute game truth.
- Parser and state interpretation remain the truth owners for parser-managed
  match and game facts.
- `src/mythic_edge_parser/app/log_drift_sensor.py` owns the current drift
  report construction behavior.
- A committed drift-report reference is a deterministic test oracle for one
  sanitized fixture slice. It does not own parser truth, detector truth, or
  workbook truth.
- Runtime drift reports and runtime drift baselines remain local artifacts.
- Workbook formulas, dashboards, webhook transport, Apps Script, live Google
  Sheets, deployed Apps Script, and AI/analytics consumers remain downstream.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`

Expected future Codex C implementation or comparison artifact:

- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`

Expected future Codex E review or contract-test report:

- `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`

Future implementation files authorized by this contract, if Codex C confirms
the current repo still matches issue #96:

- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- narrow extension to `tests/fixtures/golden_fixture_manifest.json`
- narrow test-only additions to `tests/test_log_drift_sensor.py`

Related files referenced but not owned by this contract:

- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `audit_player_log_drift.py`
- `tests/fixtures/flush_timing_corpus_slice.log`
- `tests/fixtures/golden_fixture_manifest.json`
- `tests/test_log_drift_sensor.py`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/repo_wide_golden_fixture_first_pass.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tools/select_validation.py`

This contract does not authorize production parser/runtime source changes,
detector behavior changes, schema snapshot refreshes, workbook exports, runtime
status files, failed posts, raw logs, generated data, or CI required/failing
gate changes.

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this Codex B pass:

- The branch is even with `origin/codex/repo-wide-hardening-run`.
- Tracker #82 is open.
- Issue #96 is open and asks for the first report-only drift detector baseline
  implementation pass.
- Issue #94 / PR #95 introduced
  `tests/fixtures/golden_fixture_manifest.json` and a first governed parser
  replay fixture entry.
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md` exists and
  defines drift baselines as report-oriented, report-only comparison artifacts.
- `docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md`
  found no blocking issues and preserved the current request-name status gap as
  a documented future concern.
- `docs/contracts/code_hardening_golden_fixture_policy.md` requires committed
  fixture references to be sanitized or synthetic, paired with explicit
  expected output, and governed by provenance metadata.
- `docs/contracts/repo_wide_golden_fixture_first_pass.md` chose
  `tests/fixtures/golden_fixture_manifest.json` as the first metadata
  mechanism.
- `docs/contracts/player_log_evidence_ledger.md` defines Tier 6 as runtime
  health and drift detection and requires parser drift to stay separate from
  transport, workbook, and deployment drift.
- `ADR-0003` says current observed log behavior can be used as a golden
  baseline for tests and drift detection, but not as a guarantee from Wizards.
- `ADR-0004` says snapshot and protected-surface drift require explicit issue,
  contract, review, and validation authority.

Observed `log_drift_sensor.py` behavior:

- `build_player_log_drift_report(source_path, baseline_payload=None)` reads a
  log file, routes entries through `Router`, counts headers, routed event kinds,
  unknown signatures, unmatched API names, unmatched request API names, and
  baseline deltas.
- The report currently includes:
  - `object`
  - `status`
  - `analyzed_at`
  - `source_path`
  - `entry_counts`
  - `headers`
  - `routed_event_kinds`
  - `top_unknown_signatures`
  - `top_unmatched_api_names`
  - `top_unmatched_request_api_names`
  - `baseline_delta`
- Runtime report and baseline defaults live under the runtime status root:
  - `DEFAULT_DRIFT_REPORT_PATH`
  - `DEFAULT_DRIFT_BASELINE_PATH`
- `write_player_log_drift_report()` writes the latest report and overwrites the
  baseline only when `refresh_baseline=True`.
- The CLI exits `0` for normal completion and prints a summary plus selected
  new drift families.
- Current `status == "review"` is triggered by unknown entries, new unknown
  signatures, or new unmatched response/signal API names. It is not currently
  triggered solely by `new_unmatched_request_api_names`.

Observed tests and fixtures:

- `tests/test_log_drift_sensor.py` reads
  `tests/fixtures/flush_timing_corpus_slice.log`, strips comment lines that
  start with `#`, writes the remaining text to a temporary `Player.log`, and
  calls the drift sensor against that temporary file.
- Current tests assert selected report values and selected baseline-delta
  values directly.
- Current tests do not compare a committed normalized report expected-output
  JSON.
- `tests/fixtures/flush_timing_corpus_slice.log` is already committed and is
  the only authorized input fixture for this first drift-report reference pass.
- No committed drift-report expected-output file currently exists for this
  fixture.
- No local runtime report, local runtime baseline, raw local `Player.log`, or
  generated drift output is committed by current tests.

Current gap:

- Mythic Edge has direct drift sensor assertions but no governed, normalized,
  committed drift-report reference derived from a sanitized fixture.
- The existing fixture manifest does not yet classify the flush timing drift
  fixture or link it to an expected drift-report output.
- The current drift detector baseline policy remains report-only, but there is
  no first small committed reference that demonstrates the safe workflow.

## Exact Smallest Drift-Report Reference Candidate

The exact first drift-report reference candidate is:

- `tests/fixtures/flush_timing_corpus_slice.log`

Required fixture ID:

- `player_log_drift_flush_timing_v1`

Required fixture classes:

- `sanitized_player_log_excerpt`
- `drift_report_expected_output`
- `report_only_reference`

Required input handling:

- Reuse the existing committed fixture.
- Do not add a new `.log` fixture.
- Do not modify `tests/fixtures/flush_timing_corpus_slice.log`.
- Build the test input the same way current `tests/test_log_drift_sensor.py`
  does: read the fixture, remove lines that start with `#`, write the result to
  a temporary `Player.log`, and call the detector against that temporary file.
- Record this as an `input_transform` of
  `strip_fixture_comment_lines_for_existing_test_compatibility`.
- Do not change `iter_log_entries()` or detector runtime behavior to ignore
  comments.

Required baseline/reference mode:

- Use `baseline_payload={}` or the detector's equivalent missing-baseline
  behavior.
- Do not read a committed baseline file.
- Do not write a baseline file.
- Do not call `write_player_log_drift_report()` with `refresh_baseline=True`.
- Do not commit anything under the runtime status root.

Reason for selection:

- It is already committed.
- It already drives focused drift sensor tests.
- It is small enough for review.
- It exercises unknown signatures, unmatched API names, unmatched request API
  names, and baseline-delta construction.
- It avoids importing new raw local logs.
- It proves the report-reference workflow without broadening into the future
  full drift baseline policy.

Rejected first-pass candidates:

- Local `Player.log` or `Player-prev.log`: forbidden raw local/private inputs.
- Runtime `player_log_drift_latest.json`: local runtime artifact, not a
  committed expected output.
- Runtime `player_log_drift_baseline.json`: local runtime baseline, not
  authorized for commit.
- New sanitized log fixture: broader than needed for the first pass.
- Parser regression match or Bo3 fixtures: useful parser replay inputs, but not
  the smallest drift detector report candidate.

## Expected Output Path

Required future expected output path:

- `tests/fixtures/player_log_drift_flush_timing_expected.json`

Required expected output kind:

- `normalized_drift_report_reference`

Required top-level expected output shape:

```json
{
  "object": "mythic_edge_player_log_drift_report_reference",
  "schema_version": 1,
  "fixture_id": "player_log_drift_flush_timing_v1",
  "input_path": "tests/fixtures/flush_timing_corpus_slice.log",
  "input_transform": "strip_fixture_comment_lines_for_existing_test_compatibility",
  "report_builder": "src.mythic_edge_parser.app.log_drift_sensor.build_player_log_drift_report",
  "baseline_mode": "empty_in_memory_baseline",
  "normalized_report": {}
}
```

Codex C may add stable metadata fields only if they remain deterministic,
reviewable, and free of local paths, timestamps, secrets, raw private evidence,
runtime artifact paths, workbook IDs, or deployment IDs.

## Normalized Report Fields

`normalized_report` must include only these detector-produced fields:

- `object`
- `status`
- `entry_counts`
- `headers`
- `routed_event_kinds`
- `top_unknown_signatures`
- `top_unmatched_api_names`
- `top_unmatched_request_api_names`
- `baseline_delta`

`normalized_report` must exclude:

- `analyzed_at`
- `source_path`
- `report_path`
- `baseline_path`
- local temporary file paths
- runtime status paths
- raw log lines
- raw JSON payload bodies
- raw request IDs
- raw account IDs
- local usernames or absolute paths
- webhook URLs
- workbook IDs
- Apps Script deployment IDs
- generated data dumps
- failed post payloads

Required field semantics:

- `object` preserves the current detector report object value, currently
  `player_log_drift_report`.
- `status` is included as observed behavior for this fixture. This locks the
  current status for this candidate only and does not resolve or authorize
  changes to request-name-only status semantics.
- `entry_counts` preserves the detector's current count keys and numeric
  values.
- `headers` preserves detector output as a sorted object.
- `routed_event_kinds` preserves detector output as a sorted object.
- `top_unknown_signatures` preserves detector-normalized signatures and counts
  only. It must not include raw entry bodies.
- `top_unmatched_api_names` preserves detector-normalized API names and counts.
- `top_unmatched_request_api_names` preserves detector-normalized request API
  names and counts.
- `baseline_delta` preserves all current delta keys:
  - `new_unknown_signatures`
  - `resolved_unknown_signatures`
  - `new_unmatched_api_names`
  - `resolved_unmatched_api_names`
  - `new_unmatched_request_api_names`
  - `resolved_unmatched_request_api_names`

Ordering requirements:

- Object keys in committed JSON should be stable and human-reviewable.
- Detector-produced dictionaries should match the detector's sorted output.
- Counter payload arrays should preserve the detector's current output order.
- Baseline-delta arrays should preserve the detector's current sorted output.

## Metadata And Provenance Mechanism

The first-pass metadata mechanism is the existing manifest:

- `tests/fixtures/golden_fixture_manifest.json`

Codex C may extend the manifest with one new fixture entry. It must not replace
or weaken the existing `parser_regression_match_bo1_v1` entry from issue #94.

Required manifest entry shape:

```json
{
  "fixture_id": "player_log_drift_flush_timing_v1",
  "fixture_classes": [
    "sanitized_player_log_excerpt",
    "drift_report_expected_output",
    "report_only_reference"
  ],
  "input_path": "tests/fixtures/flush_timing_corpus_slice.log",
  "expected_output_path": "tests/fixtures/player_log_drift_flush_timing_expected.json",
  "expected_output_kind": "normalized_drift_report_reference",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/96",
  "tracker_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/82",
  "source_contract": "docs/contracts/repo_wide_drift_detector_baseline_first_pass.md",
  "policy_contracts": [
    "docs/contracts/code_hardening_drift_detector_baseline_policy.md",
    "docs/contracts/code_hardening_golden_fixture_policy.md",
    "docs/contracts/repo_wide_golden_fixture_first_pass.md"
  ],
  "related_adrs": [
    "docs/decisions/ADR-0003-player-log-drift-policy.md",
    "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
  ],
  "source_type": "local_saved_log_slice",
  "source_privacy_class": "sanitized_committable",
  "redaction_status": "preexisting_sanitized_fixture",
  "redaction_method": "preexisting_committed_sanitized_fixture_no_new_sanitization_in_issue_96",
  "input_transform": "strip_fixture_comment_lines_for_existing_test_compatibility",
  "baseline_mode": "empty_in_memory_baseline",
  "update_approval_required": true,
  "not_applicable": {}
}
```

Codex C may add fields if they are stable, reviewable, and consistent with the
golden fixture policy. Codex C must not remove required fields without routing
back to Codex B.

## Required Provenance Fields

The manifest entry for `player_log_drift_flush_timing_v1` must include all of
these fields:

- `fixture_id`
- `fixture_classes`
- `input_path`
- `expected_output_path`
- `expected_output_kind`
- `source_issue`
- `tracker_issue`
- `source_contract`
- `policy_contracts`
- `related_adrs`
- `source_type`
- `source_privacy_class`
- `redaction_status`
- `redaction_method`
- `redaction_categories`
- `minimum_evidence_preserved`
- `parser_surfaces_under_test`
- `expected_output_fields`
- `evidence_ledger_tiers`
- `tier_scope_notes`
- `value_source_labels_expected`
- `confidence_labels_expected`
- `finality_labels_expected`
- `drift_flags_expected`
- `invariants_expected`
- `input_transform`
- `baseline_mode`
- `update_approval_required`
- `update_policy`
- `known_limitations`
- `not_applicable`

Required values or allowed value families:

- `fixture_id`: `player_log_drift_flush_timing_v1`
- `fixture_classes`: exactly includes `sanitized_player_log_excerpt`,
  `drift_report_expected_output`, and `report_only_reference`
- `input_path`: `tests/fixtures/flush_timing_corpus_slice.log`
- `expected_output_path`:
  `tests/fixtures/player_log_drift_flush_timing_expected.json`
- `expected_output_kind`: `normalized_drift_report_reference`
- `source_issue`: issue #96 URL
- `tracker_issue`: tracker #82 URL
- `source_contract`: this contract path
- `policy_contracts`: drift detector baseline policy, golden fixture policy,
  and repo-wide golden fixture first pass contract
- `related_adrs`: ADR-0003 and ADR-0004 at minimum
- `source_type`: `local_saved_log_slice`
- `source_privacy_class`: `sanitized_committable`
- `redaction_status`: `preexisting_sanitized_fixture`
- `redaction_method`:
  `preexisting_committed_sanitized_fixture_no_new_sanitization_in_issue_96`
- `redaction_categories`: must name the categories reviewed, such as account
  identity, display names, local paths, credentials, webhook URLs, workbook
  identifiers, runtime/local artifacts, and raw private log context
- `minimum_evidence_preserved`: must name the evidence families intentionally
  preserved, such as scene change, unmatched API response, unmatched API
  request, unknown signature, and routed event family evidence
- `parser_surfaces_under_test`: must include
  `log_drift_sensor.build_player_log_drift_report`, `LineBuffer`, `Router`,
  `_entry_signature`, `_api_name`, `_baseline_delta`, and the test fixture
  loader behavior
- `expected_output_fields`: must exactly match the normalized report field list
  in this contract
- `evidence_ledger_tiers`: must include `Tier 0: fixture metadata only` and
  `Tier 6: runtime health and drift detection`
- `tier_scope_notes`: must say this fixture does not prove Tier 1-5 parser
  facts, Tier 7 analytics, live workbook state, deployed Apps Script state, or
  full evidence-ledger behavior
- `value_source_labels_expected`, `confidence_labels_expected`,
  `finality_labels_expected`, and `drift_flags_expected`: must be
  `not_applicable` until the evidence ledger is implemented
- `invariants_expected`: must include stable normalized report shape, no
  volatile fields, no local paths, no raw log bodies, no baseline file write,
  and no fixture input changes
- `input_transform`:
  `strip_fixture_comment_lines_for_existing_test_compatibility`
- `baseline_mode`: `empty_in_memory_baseline`
- `update_approval_required`: `true`
- `update_policy`: must say updates require issue #96 or a follow-up issue,
  this contract or an amended contract, Codex C handoff, Codex E review, and
  PR drift-budget disclosure
- `known_limitations`: must say this first fixture does not prove broad drift
  coverage, live local Player.log drift, runtime baseline refresh policy,
  request-name-only status semantics, parser correctness, workbook state,
  deployed Apps Script state, evidence-ledger metadata, or sanitizer
  completeness

## Not-Applicable Provenance Fields

The manifest entry must include a `not_applicable` object for fields that the
golden fixture policy, evidence-ledger vocabulary, or runtime drift detector
anticipates but this first pass does not supply.

Required `not_applicable` keys:

- `raw_log_source_path`
- `source_log_session_id`
- `source_schema_snapshot_id`
- `sanitizer_tool_version`
- `evidence_ledger_fixture_id`
- `runtime_drift_report_path`
- `runtime_drift_baseline_path`
- `committed_drift_baseline_path`
- `refresh_baseline_command`
- `live_workbook_id`
- `deployed_apps_script_version`
- `webhook_url`
- `generated_card_data_version`
- `external_api_source`
- `runtime_status_artifact`
- `failed_post_artifact`
- `workbook_export_artifact`

Required reasons:

- Raw source path and source session ID are not recorded because raw local log
  provenance may expose private local source details.
- Sanitizer tool version is not applicable because issue #96 reuses an
  existing committed sanitized fixture and does not run or implement sanitizer
  tooling.
- Evidence-ledger fixture ID is not applicable because the evidence ledger is
  not implemented.
- Runtime drift report and runtime drift baseline paths are not applicable
  because this issue must not create, refresh, or commit local runtime
  artifacts.
- Committed drift baseline path is not applicable because this issue authorizes
  a normalized expected report reference, not a committed detector baseline.
- Refresh baseline command is not applicable because `--refresh-baseline` must
  not be used.
- Live workbook, deployed Apps Script, webhook URL, generated data, runtime
  status, failed post, and workbook export artifacts are not inputs to this
  fixture and must remain out of scope.

## Required Test Behavior For Codex C

Codex C may add focused tests to `tests/test_log_drift_sensor.py`.

Required test intent:

- Load `tests/fixtures/golden_fixture_manifest.json`.
- Find fixture ID `player_log_drift_flush_timing_v1`.
- Verify the manifest points to
  `tests/fixtures/flush_timing_corpus_slice.log` and
  `tests/fixtures/player_log_drift_flush_timing_expected.json`.
- Verify the manifest marks the fixture as `report_only_reference`.
- Build the temporary `Player.log` input using the existing comment-stripping
  fixture helper behavior.
- Call `build_player_log_drift_report()` with an empty in-memory baseline.
- Normalize the actual report by removing `analyzed_at` and `source_path`.
- Compare the normalized actual report to the expected output JSON.
- Verify the expected output does not include forbidden volatile or local
  fields.
- Verify the test does not call `write_player_log_drift_report()` in a way that
  writes a runtime report or refreshes a baseline.

The test should reuse existing helper behavior where practical. It must not
change detector behavior, fixture input content, runtime status paths, or
`--refresh-baseline` behavior.

## What The Reference Proves

This first pass proves:

- one existing committed sanitized drift fixture can be identified as a
  governed drift-report reference
- one fixture entry can carry provenance, redaction, class, scope, input
  transform, baseline mode, and update-policy metadata
- one normalized report expected output can be paired with that fixture
- volatile local fields can be excluded from committed expected output
- the report can be checked deterministically from a clean clone
- fixture/evidence drift can be named explicitly in validation and PR drift
  budgets
- secret/private-marker, protected-surface, authorization, and validation
  selector checks can be run against the fixture-related changes

This first pass does not prove:

- broad drift detector correctness
- live local `Player.log` drift safety
- runtime drift baseline refresh safety
- request-name-only status semantics
- parser behavior correctness
- evidence-ledger behavior
- workbook schema, webhook, or Apps Script parity
- live workbook state
- deployed Apps Script state
- production readiness
- sanitizer completeness
- that current MTGA log shape is a Wizards guarantee

## Report-Only No-Gate Guarantees

Required guarantees:

- The committed expected output is a deterministic fixture reference, not a
  runtime baseline.
- The committed expected output must not live under `data/`, runtime status
  paths, failed posts, generated data, or workbook export paths.
- The implementation must not create, refresh, or commit
  `player_log_drift_latest.json` or `player_log_drift_baseline.json`.
- The implementation must not call the CLI with `--refresh-baseline`.
- The implementation must not add a GitHub Actions workflow step that reads
  local `Player.log`, runtime status files, or live drift baselines.
- The implementation must not add a new required/failing CI gate for live drift
  detection.
- A focused test may compare the committed expected JSON against the committed
  sanitized fixture. If that test fails, the failure is a deterministic fixture
  review signal, not permission to auto-refresh a baseline.
- Any update to the expected JSON requires issue, contract, implementation
  handoff, Codex E review, and PR drift-budget disclosure.

## Fixture And Evidence Drift-Budget Interpretation

Expected drift budget for Codex C:

- `Fixtures/evidence`: `Authorized drift` for adding
  `tests/fixtures/player_log_drift_flush_timing_expected.json`.
- `Fixtures/evidence`: `Authorized drift` for extending
  `tests/fixtures/golden_fixture_manifest.json` with the
  `player_log_drift_flush_timing_v1` entry.
- `Fixtures/evidence`: `No drift` for
  `tests/fixtures/flush_timing_corpus_slice.log`; this issue does not
  authorize changing that file.
- `Fixtures/evidence`: `No drift` for existing parser regression expected
  outputs and schema snapshots.
- `Runtime drift reports`: `No drift`; no local runtime reports may be
  committed.
- `Runtime drift baselines`: `No drift`; no local runtime baselines may be
  committed or refreshed.
- `Detector behavior`: `No drift`.
- `Parser behavior`: `No drift`.
- `Parser event shape/classes`: `No drift`.
- `Workbook/webhook/App Script shape`: `No drift`.
- `Parser truth ownership`: `No drift`.
- `CI gate behavior`: `No drift`.
- `Protected-surface authorization`: `N/A` unless a touched path triggers a
  warning, in which case Codex C must run the authorization checker with issue,
  contract, and handoff evidence.

Forbidden drift:

- modifying the existing `.log` fixture input
- adding a new `.log` fixture
- committing raw local `Player.log` or `Player-prev.log`
- committing runtime drift reports
- committing runtime drift baselines
- calling `--refresh-baseline`
- changing detector status semantics
- changing detector output shape
- refreshing parser schema snapshots
- changing parser expected outputs outside the new drift reference
- changing workbook schema, webhook payload shape, or Apps Script behavior
- treating scanner warnings as proof of complete sanitization

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event kind values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- detector behavior
- detector `status` semantics
- detector report field names
- `--refresh-baseline` behavior
- CI required/failing gate behavior
- Pyright gate behavior
- production deployment behavior
- merge-to-main policy
- secrets, credentials, tokens, API keys, or webhook URLs
- environment variable contracts
- raw local logs
- generated card, deck, tier, or oracle data
- runtime status files
- failed posts
- workbook exports
- live workbook state
- deployed Apps Script state

Allowed future implementation surfaces under this exact contract:

- `tests/fixtures/player_log_drift_flush_timing_expected.json`
- one new entry in `tests/fixtures/golden_fixture_manifest.json`
- focused test-only additions to `tests/test_log_drift_sensor.py`
- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`
- `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`

Any required change outside those surfaces must route back to Codex B or Codex
A before implementation continues.

## Error Behavior

If the manifest is missing:

- the focused test should fail with a message naming the missing manifest and
  fixture ID
- Codex C may add the manifest entry only if it can preserve existing manifest
  entries and satisfy this contract

If the manifest points to a missing input or expected output:

- the test should fail
- do not create a new input `.log` fixture
- do not change the existing input fixture to hide the issue

If the normalized expected report differs from actual detector output:

- do not auto-update the expected output
- inspect whether the diff is detector behavior drift, expected-output
  staleness, test harness drift, fixture drift, or intentional scope change
- route back to Codex B or E if classification is ambiguous

If the expected output contains volatile or local fields:

- remove the fields from the expected output and normalization contract
- do not change runtime detector output solely to satisfy committed reference
  normalization

If secret/private-marker scanning reports forbidden findings:

- stop and remove, redact, or rework the fixture metadata/output
- do not submit the reference as a governed fixture

If secret/private-marker scanning reports warnings only:

- report them in the handoff and PR drift budget
- warnings do not prove full safety; Codex E must review the fixture metadata
  and expected output content

If protected-surface checks report warnings:

- run the authorization checker with issue, contract, and handoff/report
  sources
- do not treat warnings as automatic authorization

## Side Effects

Allowed side effect in this Codex B thread:

- create `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md`

Forbidden side effects in this Codex B thread:

- no fixture implementation
- no expected output creation
- no fixture input changes
- no fixture data copying
- no raw-log sanitization
- no detector behavior changes
- no baseline generation
- no baseline refresh
- no runtime report writes
- no tests
- no parser behavior changes
- no schema changes
- no webhook/App Script changes
- no CI gate changes
- no PR creation
- no tracker closure

Allowed side effects in future Codex C implementation, if this contract is the
active source artifact:

- add the normalized drift-report expected output
- extend the golden fixture manifest with one new fixture entry
- add focused test-only coverage
- write the implementation handoff

## Validation Requirements

Contract-writer validation for this Codex B pass:

```powershell
git diff --check
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
'@ | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
'@ | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
'@ | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
py tools\check_agent_docs.py
```

Focused Codex C validation:

```powershell
git status --short --branch
py -m pytest -q tests\test_log_drift_sensor.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

Codex C path-scoped validation should include the touched implementation paths:

```powershell
@'
tests/fixtures/golden_fixture_manifest.json
tests/fixtures/player_log_drift_flush_timing_expected.json
tests/test_log_drift_sensor.py
docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
tests/fixtures/golden_fixture_manifest.json
tests/fixtures/player_log_drift_flush_timing_expected.json
tests/test_log_drift_sensor.py
docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
tests/fixtures/golden_fixture_manifest.json
tests/fixtures/player_log_drift_flush_timing_expected.json
tests/test_log_drift_sensor.py
docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
'@ | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md
@'
tests/fixtures/golden_fixture_manifest.json
tests/fixtures/player_log_drift_flush_timing_expected.json
tests/test_log_drift_sensor.py
docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md
'@ | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
```

Before Codex F submits a PR that includes the new expected output or manifest
entry:

```powershell
py -m pytest -q tests
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

Runtime parser tests beyond `tests/test_log_drift_sensor.py` are not required
for the contract-writer pass, but Codex E may request broader validation if the
implementation diff touches broader parser/test surfaces.

## Acceptance Criteria

- `docs/contracts/repo_wide_drift_detector_baseline_first_pass.md` exists.
- The contract links issue #96, tracker #82, drift detector baseline policy
  issue #70, and first golden fixture issue #94.
- The contract names `tests/fixtures/flush_timing_corpus_slice.log` as the
  exact first drift-report reference candidate.
- The contract names
  `tests/fixtures/player_log_drift_flush_timing_expected.json` as the expected
  output path.
- The contract defines the expected output as a normalized drift-report
  reference, not a runtime baseline.
- The contract requires reusing the existing fixture comment-stripping helper
  behavior without changing detector runtime parsing.
- The contract defines normalized report fields and volatile/local exclusions.
- The contract names `tests/fixtures/golden_fixture_manifest.json` as the
  metadata mechanism and defines required provenance fields.
- The contract distinguishes report-only references from runtime drift
  baselines and live drift gates.
- Report-only no-gate guarantees are explicit.
- Fixture/evidence drift-budget interpretation is explicit.
- Protected surfaces and forbidden side effects are named.
- Validation commands are defined for Codex B, Codex C, path-scoped checks, and
  submitter escalation.
- Expected Codex C handoff and Codex E report artifacts are named.
- The contract includes a pasteable Codex C prompt.
- The contract includes a `workflow_handoff` block.
- No code, fixture, baseline, runtime report, parser behavior, schema,
  webhook/App Script, CI gate, secret, raw log, generated data, runtime status,
  failed post, workbook export, production behavior, or `main` targeting change
  is made by the contract writer pass.

## Unknowns

- Whether the normalized expected report should include any future stable
  metadata beyond the required top-level fields.
- Whether future drift-report references should live beside fixtures under
  `tests/fixtures/` or move to a dedicated `tests/fixtures/drift_reports/`
  folder once there is more than one reference.
- Whether current status behavior should eventually treat
  `new_unmatched_request_api_names` alone as `review`.
- Whether future committed drift baselines should ever exist, and if so whether
  they should be full reports, reduced semantic snapshots, or manifest-declared
  baseline payloads.
- Whether a future evidence-ledger implementation should own a richer Tier 6
  drift expected-output shape.
- Whether old UUID-shaped values in existing sanitized fixture slices should be
  normalized further before accepting additional drift references.
- Whether future detector tests should assert CLI output and
  `--refresh-baseline` behavior with temporary files.

## Suspected Gaps

- No committed normalized drift-report reference currently exists.
- `flush_timing_corpus_slice.log` is useful and already committed, but its
  provenance is legacy compared with the new manifest policy.
- Current tests assert selected report fields but do not verify that committed
  expected output excludes volatile/local fields.
- Current tests do not verify manifest metadata for the drift fixture.
- Current tests do not prove missing, malformed, or non-object baseline payload
  behavior in a committed expected-output reference.
- Current tests do not cover CLI output or `--refresh-baseline` temporary-file
  behavior.
- The request-name-only status gap remains documented but intentionally
  unimplemented by this first pass.
- The evidence ledger is not implemented, so Tier 6 drift reports do not yet
  map to affected parser-managed outputs.

## Stop Conditions

Stop and route back to Codex B or A if Codex C needs to:

- change `src/mythic_edge_parser/app/log_drift_sensor.py`
- change `audit_player_log_drift.py`
- change `--refresh-baseline` behavior
- change detector report field names
- change detector status semantics
- add a committed runtime baseline
- add a committed runtime report
- add or modify `.log` fixture input
- use raw local `Player.log`
- refresh parser schema snapshots
- change parser behavior
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- add a failing live drift CI gate
- touch secrets, raw logs, generated data, runtime status files, failed posts,
  workbook exports, live workbook state, deployed Apps Script state, Pyright
  gate behavior, or production behavior
- target `main`
- mark tracker #82 complete

## Expected Codex C Handoff

Codex C should produce:

- `docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md`

The handoff must include:

- role performed
- issue and tracker used
- contract used
- branch and git status
- files inspected
- what was implemented or intentionally left unchanged
- fixture candidate selected
- manifest fields added
- normalized expected output fields added
- exact test section changed
- validation run and result
- secret/private-marker scan result
- protected-surface result
- surface-authorization result
- validation-selector result
- fixture/evidence drift-budget interpretation
- report-only no-gate confirmation
- forbidden scopes touched or not touched
- remaining risks
- next recommended role
- pasteable Codex E prompt
- `workflow_handoff` block

## Expected Codex E Report

Codex E should produce:

- `docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md`

The report must lead with findings and verify:

- the selected input fixture is exactly
  `tests/fixtures/flush_timing_corpus_slice.log`
- no new `.log` fixture was added
- the existing input fixture content was not changed
- the expected output path is exactly
  `tests/fixtures/player_log_drift_flush_timing_expected.json`
- the expected output is a normalized report reference, not a runtime baseline
- the expected output excludes `analyzed_at`, `source_path`, report paths,
  baseline paths, local temp paths, raw log bodies, raw JSON bodies, secrets,
  webhook URLs, workbook IDs, deployment IDs, runtime artifacts, failed posts,
  generated data, and workbook exports
- the manifest contains required provenance fields
- not-applicable fields have explicit reasons
- focused tests fail on missing or mismatched expected output
- no runtime baseline or runtime report is generated or committed
- `--refresh-baseline` behavior is not changed or invoked
- no failing live drift CI gate is added
- secret/private-marker scan has no forbidden findings
- protected-surface checks are clean or explicitly authorized
- parser behavior, detector behavior, parser state final reconciliation,
  workbook schema, webhook payload shape, Apps Script behavior, parser event
  classes, event kind values, parser payload shapes, match/game identity,
  deduplication, CI gate behavior, Pyright gate behavior, secrets, raw logs,
  generated data, runtime status files, failed posts, workbook exports, live
  workbook state, deployed Apps Script state, and production behavior were not
  changed

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for repo-wide hardening issue #96: Drift detector baseline first pass.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/96

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_drift_detector_baseline_first_pass.md

Goal:
Compare the current drift sensor, fixture manifest, and focused tests against the contract. Implement only the smallest fixture-reference/test changes needed to establish one report-only normalized drift-report expected output.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_drift_detector_baseline_first_pass.md
- docs/contracts/code_hardening_drift_detector_baseline_policy.md
- docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md
- docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/repo_wide_golden_fixture_first_pass.md
- docs/contracts/player_log_evidence_ledger.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- src/mythic_edge_parser/app/log_drift_sensor.py
- audit_player_log_drift.py
- tests/test_log_drift_sensor.py
- tests/fixtures/flush_timing_corpus_slice.log
- tests/fixtures/golden_fixture_manifest.json
- tools/check_secret_patterns.py
- tests/test_check_secret_patterns.py
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- tools/check_surface_authorization.py
- tests/test_check_surface_authorization.py
- tools/select_validation.py
- tests/test_select_validation.py

Before editing:
- Confirm branch is codex/repo-wide-hardening-run.
- Inspect git status and exclude unrelated changes.
- State what the drift-report reference is supposed to do, what current drift tests already do, what gap remains, and the exact minimal implementation plan.

Do:
- Reuse tests/fixtures/flush_timing_corpus_slice.log as the only first-pass input fixture.
- Do not add or change any .log input fixture.
- Extend tests/fixtures/golden_fixture_manifest.json with one entry for fixture_id player_log_drift_flush_timing_v1.
- Add tests/fixtures/player_log_drift_flush_timing_expected.json as a normalized drift-report reference.
- Build the expected report from the existing test input behavior: strip comment lines from the fixture into a temporary Player.log, call build_player_log_drift_report with an empty in-memory baseline, and remove analyzed_at and source_path.
- Add focused test coverage in tests/test_log_drift_sensor.py that loads the manifest, verifies the fixture metadata, normalizes the actual report, and compares it to the expected JSON.
- Ensure the expected output excludes analyzed_at, source_path, report paths, baseline paths, local temp paths, raw log bodies, raw JSON bodies, secrets, webhook URLs, workbook IDs, deployment IDs, runtime status, failed posts, generated data, and workbook exports.
- Produce docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md.

Do not:
- Change src/mythic_edge_parser/app/log_drift_sensor.py.
- Change audit_player_log_drift.py.
- Change detector behavior, detector status semantics, detector report shape, or --refresh-baseline behavior.
- Generate, refresh, or commit drift baselines.
- Commit runtime drift reports.
- Add a failing live drift CI gate.
- Change parser behavior.
- Change parser state final reconciliation.
- Change workbook schema.
- Change webhook payload shape.
- Change Apps Script behavior.
- Change parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, sync field names, runtime family names, runtime event_type values, or runtime scope values.
- Add new .log fixture data.
- Modify tests/fixtures/flush_timing_corpus_slice.log.
- Refresh schema snapshots.
- Modify unrelated parser expected outputs.
- Implement sanitizer tooling.
- Implement the Player.log evidence ledger.
- Touch secrets, credentials, environment variables, raw local logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, Pyright gate behavior, production behavior, or main.
- Stage, commit, open a PR, close issues, or mark tracker #82 complete unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_log_drift_sensor.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-96.md --authorization-file contract=docs\contracts\repo_wide_drift_detector_baseline_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_drift_detector_baseline_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

Final handoff must include:
- role performed
- issue/tracker
- contract used
- files changed
- exact test/fixture sections changed
- validation run and result
- fixture/evidence drift-budget interpretation
- report-only no-gate confirmation
- protected-surface status
- surface-authorization status
- secret/private-marker status
- validation-selector status
- what remains unverified
- whether forbidden scope was touched
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/96"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/repo_wide_drift_detector_baseline_first_pass.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_drift_detector_baseline_first_pass_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_drift_detector_baseline_first_pass.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git diff --check"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\\contracts\\repo_wide_drift_detector_baseline_first_pass.md"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_agent_docs.py"
  stop_conditions:
    - "Do not implement code, fixtures, tests, or detector changes in Codex B."
    - "Do not generate, refresh, or commit drift baselines."
    - "Do not commit runtime drift reports."
    - "Do not change detector behavior, detector status semantics, detector report shape, or --refresh-baseline behavior."
    - "Do not add a failing live drift CI gate."
    - "Do not add new .log input fixtures."
    - "Do not modify tests/fixtures/flush_timing_corpus_slice.log."
    - "Do not refresh schema snapshots or unrelated expected outputs."
    - "Do not implement sanitizer tooling or the Player.log evidence ledger."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, Pyright gate behavior, CI gate behavior, production behavior, or merge-to-main policy."
    - "Do not target main."
    - "Do not mark tracker #82 complete."
```
