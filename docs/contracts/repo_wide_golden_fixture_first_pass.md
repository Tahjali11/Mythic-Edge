# Repo-Wide Golden Fixture First Pass Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/94

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch target: `codex/repo-wide-hardening-run`

Related policy issue: https://github.com/Tahjali11/Mythic-Edge/issues/68

Related future backlog: https://github.com/Tahjali11/Mythic-Edge/issues/48

Previous repo-wide hardening context:

- Issue #92 / PR #93 workbook/webhook schema snapshot tests merged into
  `codex/repo-wide-hardening-run` at
  `52ca6e6748370a07cb6b8afeba595c955ce492d5`.
- Tracker #82 remains open.
- This issue defines the first tiny governed golden-fixture acceptance path.
- The full golden replay harness from issue #48 remains future work.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Policy, ADR, and hardening artifacts read:

- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_golden_fixture_policy.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Fixture, test, and tool surfaces read:

- `tests/test_parser_regressions.py`
- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_slice.log`
- `tests/fixtures/parser_regression_bo3_expected.json`
- `tests/test_sanitize.py`
- `src/mythic_edge_parser/sanitize.py`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tests/test_check_surface_authorization.py`
- `tools/select_validation.py`
- `tests/test_select_validation.py`

This is a contract-writing artifact only. It does not implement fixture
metadata, add or copy fixture data, sanitize raw logs, add tests, change parser
behavior, change schema, change webhook or Apps Script behavior, change CI
gates, target `main`, or mark tracker #82 complete.

## Module

Repo-wide first sanitized golden fixture implementation pass.

Plain English: this issue should prove that Mythic Edge can accept one existing
sanitized parser replay fixture as a governed golden fixture, with explicit
provenance metadata and one small parser-owned expected output. It should prove
the workflow, not broad parser correctness.

## Owning Layer

Owning layer: repo-wide hardening fixture governance and test infrastructure.

Truth boundary:

- MTGA `Player.log` is local observable evidence, not absolute game truth.
- Parser and state interpretation remain the truth owners for parser-managed
  match and game facts.
- The existing committed fixture is evidence for deterministic tests.
- The new reduced expected output is a test oracle for one accepted behavior
  slice. It is not parser truth and must not redefine parser behavior by
  itself.
- Golden-fixture metadata records provenance, redaction status, scope, and
  update policy. It is not a second parser, not an evidence ledger
  implementation, and not a workbook workaround.
- Workbook formulas, dashboards, webhook transport, Apps Script, live Google
  Sheets, deployed Apps Script, and AI/analytics consumers remain downstream.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_golden_fixture_first_pass.md`

Expected future Codex C implementation or comparison artifact:

- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`

Expected future Codex E review or contract-test report:

- `docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md`

Future implementation files authorized by this contract, if Codex C confirms
the current repo still matches issue #94:

- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/parser_regression_match_golden_expected.json`
- narrow additions to `tests/test_parser_regressions.py`

Related files referenced but not owned by this contract:

- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_slice.log`
- `tests/fixtures/parser_regression_bo3_expected.json`
- `tests/test_sanitize.py`
- `src/mythic_edge_parser/sanitize.py`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tools/check_surface_authorization.py`
- `tools/select_validation.py`

This contract does not authorize changes to production parser/runtime source
files, schema snapshots, workbook exports, runtime status files, failed posts,
raw logs, generated data, or CI required/failing behavior.

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this contract pass:

- The branch is even with `origin/codex/repo-wide-hardening-run`.
- Tracker #82 is open and names the golden fixture implementation pass as the
  next queue item after #92.
- Issue #94 is open and asks for the first tiny governed golden-fixture
  acceptance path.
- `docs/contracts/code_hardening_golden_fixture_policy.md` exists and defines
  fixture classes, provenance metadata, redaction requirements, expected-output
  pairing, update policy, validation, and protected surfaces.
- `docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md`
  classifies existing parser replay fixtures as useful legacy/unclassified
  fixtures.
- `docs/contract_test_reports/code_hardening_golden_fixture_policy.md`
  found no blocking issues and recorded a residual risk around legacy
  unclassified fixture content.
- `docs/decisions/ADR-0003-player-log-drift-policy.md` says committed
  fixtures must be sanitized and current observed log behavior is a baseline,
  not a Wizards guarantee.
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
  requires issue, contract, review, and validation for protected surface and
  snapshot drift.
- `tests/test_parser_regressions.py` currently replays two parser regression
  fixture pairs through `LineBuffer`, `Router`, parser transforms, and parser
  state.
- `tests/test_parser_regressions.py` compares a full replay snapshot against
  paired `*_expected.json` files.
- The full snapshot contains router stats, event traces, parser context,
  match summary debug output, match rows, match-log row output, and game-log
  row output.
- `tests/fixtures/parser_regression_match_slice.log` is small, already
  committed, labeled sanitized, and exercises a Bo1 match lifecycle with rank,
  match start, submit deck, game state, and game result evidence.
- `tests/fixtures/parser_regression_match_expected.json` is the existing full
  parser regression expected output for that input.
- `tools/check_secret_patterns.py` now exists on this repo-wide hardening
  branch and treats raw Player.log-style markers inside sanitized fixture
  context as warnings rather than failures.
- `tools/check_protected_surfaces.py` allows documented fixture paths under
  `tests/fixtures/` by path, but that allowance is not content sanitization.
- `tools/select_validation.py` maps `tests/fixtures/parser_regression_*` to
  `tests/test_parser_regressions.py` and maps schema snapshot fixtures to
  `tests/test_event_schema_snapshots.py`.

Current gap:

- No v1 manifest, sidecar, or test-owned declaration records provenance and
  redaction metadata for a golden parser replay fixture.
- No reduced parser-owned expected-output fixture demonstrates the
  golden-fixture policy without promoting the broader legacy regression
  snapshot to a fully governed golden oracle.

## Exact First Fixture Candidate

The exact first golden fixture candidate is:

- `tests/fixtures/parser_regression_match_slice.log`

Fixture ID for v1 metadata:

- `parser_regression_match_bo1_v1`

Fixture classes:

- `sanitized_player_log_excerpt`
- `parser_replay_fixture`

Reason for selection:

- It is already committed.
- It is small enough for human review.
- It is labeled sanitized.
- It avoids importing new raw local logs.
- It exercises parser-owned match and game row outputs.
- It covers a simple Bo1 lifecycle, which is the smallest useful acceptance
  path before Bo3, sideboarding, drift baselines, or future ledger fixtures.

Rejected first-pass candidates:

- `tests/fixtures/parser_regression_bo3_slice.log`: useful but broader than
  needed for the first acceptance path.
- `tests/fixtures/flush_timing_corpus_slice.log`: useful for drift sensor
  tests but carries known legacy/unclassified redaction risk and is not the
  smallest parser-owned row-output candidate.
- `tests/fixtures/router_smoke_slice.log`: useful for routing smoke tests but
  does not prove match/game row expected-output pairing.
- New `.log` fixture data: not authorized for this issue.

## Expected Output Decision

This contract chooses the preferred issue #94 path:

- Add one reduced parser-owned expected output fixture.
- Do not classify `tests/fixtures/parser_regression_match_expected.json` as the
  first v1 golden expected output.

Required future expected output path:

- `tests/fixtures/parser_regression_match_golden_expected.json`

Required expected output kind:

- `reduced_parser_owned_output`

Required expected output scope:

- `match_log_row`
- `game_log_rows`

Forbidden expected output content for this first pass:

- full `event_traces`
- router stats
- parser context snapshots
- `match_summary_debug`
- `match_summary_row`
- raw JSON payloads
- raw log lines
- raw bytes or hashes
- local paths
- live workbook IDs
- webhook URLs
- deployed Apps Script identifiers
- runtime status payloads
- failed post payloads
- generated card, deck, tier, or oracle data dumps

The existing `tests/fixtures/parser_regression_match_expected.json` remains the
legacy full parser regression oracle. It may be read by Codex C for comparison,
but this contract does not authorize modifying it in issue #94.

Rationale:

- A reduced output proves the governed golden fixture path without duplicating
  every current full regression snapshot field.
- The first v1 golden expected output should focus on parser-owned business
  outputs rather than parser internals.
- Keeping the full snapshot as legacy regression coverage prevents the first
  golden pass from pretending that all current replay internals have
  provenance metadata.

## Metadata And Provenance Mechanism

The first-pass metadata mechanism must be JSON, not YAML.

Required future manifest path:

- `tests/fixtures/golden_fixture_manifest.json`

Required manifest shape:

```json
{
  "object": "mythic_edge_golden_fixture_manifest",
  "schema_version": 1,
  "fixtures": []
}
```

Required fixture entry shape:

```json
{
  "fixture_id": "parser_regression_match_bo1_v1",
  "fixture_classes": [
    "sanitized_player_log_excerpt",
    "parser_replay_fixture"
  ],
  "input_path": "tests/fixtures/parser_regression_match_slice.log",
  "expected_output_path": "tests/fixtures/parser_regression_match_golden_expected.json",
  "expected_output_kind": "reduced_parser_owned_output",
  "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/94",
  "tracker_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/82",
  "source_contract": "docs/contracts/repo_wide_golden_fixture_first_pass.md",
  "policy_contract": "docs/contracts/code_hardening_golden_fixture_policy.md",
  "related_adrs": [
    "docs/decisions/ADR-0003-player-log-drift-policy.md",
    "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
  ],
  "source_type": "local_saved_log_slice",
  "source_privacy_class": "sanitized_committable",
  "redaction_status": "sanitized",
  "redaction_method": "preexisting_committed_sanitized_fixture",
  "redaction_categories": [],
  "minimum_evidence_preserved": [],
  "parser_surfaces_under_test": [],
  "evidence_ledger_tiers": [],
  "value_source_labels_expected": "not_applicable",
  "confidence_labels_expected": "not_applicable",
  "finality_labels_expected": "not_applicable",
  "drift_flags_expected": "not_applicable",
  "invariants_expected": [],
  "update_approval_required": true,
  "update_policy": "",
  "known_limitations": [],
  "not_applicable": {}
}
```

Codex C may add fields if they are stable, reviewable, and consistent with the
golden fixture policy. Codex C must not remove required fields without routing
back to Codex B.

## Required Provenance Fields

The manifest entry for `parser_regression_match_bo1_v1` must include all of
these fields:

- `fixture_id`
- `fixture_classes`
- `input_path`
- `expected_output_path`
- `expected_output_kind`
- `source_issue`
- `tracker_issue`
- `source_contract`
- `policy_contract`
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
- `update_approval_required`
- `update_policy`
- `known_limitations`
- `not_applicable`

Required values or allowed value families:

- `fixture_id`: `parser_regression_match_bo1_v1`
- `fixture_classes`: exactly includes `sanitized_player_log_excerpt` and
  `parser_replay_fixture`
- `input_path`: `tests/fixtures/parser_regression_match_slice.log`
- `expected_output_path`:
  `tests/fixtures/parser_regression_match_golden_expected.json`
- `expected_output_kind`: `reduced_parser_owned_output`
- `source_issue`: issue #94 URL
- `tracker_issue`: tracker #82 URL
- `source_contract`: this contract path
- `policy_contract`: `docs/contracts/code_hardening_golden_fixture_policy.md`
- `related_adrs`: ADR-0003 and ADR-0004 at minimum
- `source_type`: `local_saved_log_slice`
- `source_privacy_class`: `sanitized_committable`
- `redaction_status`: `sanitized`
- `redaction_method`:
  `preexisting_committed_sanitized_fixture_no_new_sanitization_in_issue_94`
- `redaction_categories`: must name the categories reviewed, such as account
  identity, display names, local paths, credentials, webhook URLs, workbook
  identifiers, and runtime/local artifacts
- `minimum_evidence_preserved`: must name the minimum evidence families the
  fixture intentionally preserves, such as rank response, match room state,
  submit deck response, game state, and game result
- `parser_surfaces_under_test`: must name the test harness surfaces used by
  the replay, such as `LineBuffer`, `Router`, parser transforms, parser state
  update, `state.build_match_log_row`, and
  `state.build_game_summary_rows`
- `expected_output_fields`: exactly includes `match_log_row` and
  `game_log_rows`
- `evidence_ledger_tiers`: may include Tier 0, Tier 1, Tier 2, Tier 3, and a
  narrowly scoped Tier 4 note for submit-deck-seen evidence only
- `tier_scope_notes`: must state that this fixture is not Tier 5 card action
  coverage, Tier 6 drift baseline coverage, or Tier 7 analytics coverage
- `value_source_labels_expected`, `confidence_labels_expected`,
  `finality_labels_expected`, and `drift_flags_expected`: must be
  `not_applicable` until the evidence ledger is implemented
- `invariants_expected`: must be focused on current parser-owned output
  assertions, such as stable match ID, exactly one Bo1 game row, final match
  row present, and no raw JSON in the reduced expected output
- `update_approval_required`: `true`
- `update_policy`: must say updates require issue #94 or a follow-up issue,
  this contract or an amended contract, Codex C handoff, Codex E review, and
  PR drift-budget disclosure
- `known_limitations`: must say this first fixture does not prove broad parser
  correctness, Bo3 behavior, sideboarding deltas, drift baseline policy,
  evidence-ledger metadata, live workbook state, deployed Apps Script state, or
  sanitizer completeness

## Not-Applicable Provenance Fields

The manifest entry must include a `not_applicable` object for fields that the
golden fixture policy or evidence-ledger vocabulary anticipates but this first
pass does not supply.

Required `not_applicable` keys:

- `raw_log_source_path`
- `source_log_session_id`
- `source_schema_snapshot_id`
- `sanitizer_tool_version`
- `evidence_ledger_fixture_id`
- `drift_baseline_id`
- `drift_report_expected_output_path`
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
  provenance must not expose private local source details.
- Sanitizer tool version is not applicable because issue #94 reuses an
  existing committed sanitized fixture and does not run or implement sanitizer
  tooling.
- Evidence-ledger fixture ID is not applicable because the evidence ledger is
  not implemented.
- Drift baseline and drift report expected output are not applicable because
  this issue does not implement drift baseline policy.
- Live workbook, deployed Apps Script, webhook URL, generated data, runtime
  status, failed post, and workbook export artifacts are not inputs to this
  fixture and must remain out of scope.

## Required Test Behavior For Codex C

Codex C may add a focused test to `tests/test_parser_regressions.py`.

Required test intent:

- Load `tests/fixtures/golden_fixture_manifest.json`.
- Find fixture ID `parser_regression_match_bo1_v1`.
- Verify the manifest points to
  `tests/fixtures/parser_regression_match_slice.log` and
  `tests/fixtures/parser_regression_match_golden_expected.json`.
- Replay the input fixture through the same parser-owned path used by current
  parser regression tests.
- Reduce the actual replay result to only `match_log_row` and `game_log_rows`.
- Compare that reduced actual result to the reduced expected output JSON.
- Verify the reduced expected output does not include forbidden internal
  sections such as `event_traces`, `router_stats`, `context`,
  `match_summary_debug`, `match_summary_row`, or `raw_json`.

The test should reuse existing helper behavior where practical. It must not
change parser behavior, parser state behavior, fixture input content, or the
existing full regression expected output.

## What The Fixture Proves

This first pass proves:

- one existing committed sanitized parser replay input can be identified as a
  governed golden fixture
- one fixture entry can carry v1 provenance, redaction, class, scope, and
  update-policy metadata
- one reduced parser-owned expected output can be paired with that input
- the reduced output can be checked deterministically from a clean clone
- fixture drift can be named explicitly in validation and PR drift budgets
- secret/private-marker and protected-surface checks can be run against
  fixture-related changes

This first pass does not prove:

- broad parser correctness
- all Bo1 parser behavior
- Bo3 behavior
- sideboarding or exact deck-delta behavior
- card-action or card-resolution behavior
- drift detector baseline behavior
- Player.log evidence-ledger behavior
- sanitizer completeness
- live workbook state
- deployed Apps Script state
- webhook transport behavior
- generated card or tier data correctness
- Arena's real game truth

## Parser Truth And Test-Oracle Boundaries

Required guarantees:

- Parser/state remains the truth owner for match and game interpretation.
- `parser_regression_match_golden_expected.json` is a reviewable test oracle
  for one selected fixture, not a truth source.
- If the reduced expected output fails, Codex must classify the failure before
  changing anything.
- Possible failure classes include parser behavior drift, test harness drift,
  fixture drift, expected-output staleness, schema drift, sanitizer/redaction
  drift, and accidental private-data introduction.
- A failing golden test must not be fixed by blindly regenerating expected
  output.
- Workbook formulas, dashboards, webhook transport, Apps Script, and AI output
  must not override the parser-owned actual replay result.

## Fixture Drift-Budget Interpretation

For issue #94 and its PR:

- `Fixtures/evidence`: `Authorized drift` for adding
  `tests/fixtures/golden_fixture_manifest.json` and
  `tests/fixtures/parser_regression_match_golden_expected.json`, if and only
  if they match this contract.
- `Fixtures/evidence`: `No drift` for the existing input
  `tests/fixtures/parser_regression_match_slice.log`; this issue does not
  authorize changing that file.
- `Fixtures/evidence`: `No drift` for the existing full expected output
  `tests/fixtures/parser_regression_match_expected.json`; this issue does not
  authorize changing that file.
- `Fixtures/evidence`: `Residual drift` if metadata remains incomplete, if the
  reduced expected output cannot be added cleanly, or if the legacy full
  regression output remains the only oracle.
- `Runtime/parser behavior`: `No drift`.
- `Parser event shape/classes`: `No drift`.
- `Workbook/webhook/App Script shape`: `No drift`.
- `Parser truth ownership`: `No drift`.
- `Protected-surface authorization`: `N/A` unless Codex C touches a path that
  the protected-surface gate warns on.

Forbidden fixture drift:

- modifying existing `.log` fixture input content
- adding a new `.log` fixture
- modifying existing full parser regression expected JSON
- refreshing schema snapshots
- adding drift baselines
- adding raw local logs or runtime/local artifacts
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
- CI required/failing gates
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

- `tests/fixtures/golden_fixture_manifest.json`
- `tests/fixtures/parser_regression_match_golden_expected.json`
- focused test-only additions to `tests/test_parser_regressions.py`
- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`
- `docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md`

Any required change outside those surfaces must route back to Codex B or Codex
A before implementation continues.

## Error Behavior

If the manifest is missing:

- the focused golden fixture test should fail with a message naming the
  missing manifest and fixture ID
- Codex C should add the manifest only if it can satisfy this contract

If the manifest points to a missing input or expected output:

- the test should fail
- do not create a new input `.log` fixture
- do not modify the existing full regression expected output to hide the issue

If the reduced expected output differs from actual parser-owned output:

- do not auto-update the expected output
- inspect whether the diff is parser behavior drift, expected-output
  staleness, test harness drift, schema drift, or fixture drift
- route back to Codex B or E if classification is ambiguous

If secret/private-marker scanning reports forbidden findings:

- stop and remove, redact, or rework the fixture metadata/output
- do not submit the fixture as golden

If secret/private-marker scanning reports warnings only:

- report them in the handoff and PR drift budget
- warnings do not prove full safety; Codex E must review the fixture metadata
  and output content

If protected-surface checks report warnings:

- run the authorization checker with issue, contract, and handoff/report
  sources
- do not treat warnings as automatic authorization

## Side Effects

Allowed side effect in this Codex B thread:

- create `docs/contracts/repo_wide_golden_fixture_first_pass.md`

Forbidden side effects in this Codex B thread:

- no fixture metadata implementation
- no expected output creation
- no fixture input changes
- no fixture data copying
- no raw-log sanitization
- no sanitizer tooling implementation
- no tests
- no parser behavior changes
- no schema changes
- no webhook/App Script changes
- no CI gate changes
- no PR creation
- no tracker closure

Allowed side effects in future Codex C implementation, if this contract is the
active source artifact:

- add the manifest
- add the reduced expected output
- add focused test-only coverage
- write the implementation handoff

## Validation Requirements

Contract-writer validation for this Codex B pass:

```powershell
git diff --check
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_golden_fixture_first_pass.md
'@ | py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_golden_fixture_first_pass.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
@'
docs/contracts/repo_wide_golden_fixture_first_pass.md
'@ | py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\contracts\repo_wide_golden_fixture_first_pass.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
@'
docs/contracts/repo_wide_golden_fixture_first_pass.md
'@ | py tools\select_validation.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin
py tools\check_agent_docs.py
```

Focused Codex C validation:

```powershell
git status --short --branch
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-94.md --authorization-file contract=docs\contracts\repo_wide_golden_fixture_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_golden_fixture_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

If Codex C touches any Python test file:

```powershell
py -m ruff check src tests tools
py -m pyright
```

Before Codex F submits a PR that includes fixture metadata or expected output:

```powershell
py -m pytest -q tests
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check
```

Runtime parser tests beyond `tests/test_parser_regressions.py` are not required
for the contract-writer pass, but Codex E may request them if the implementation
diff touches broader parser/test surfaces.

## Acceptance Criteria

- `docs/contracts/repo_wide_golden_fixture_first_pass.md` exists.
- The contract links issue #94, tracker #82, policy issue #68, and future
  backlog issue #48.
- The contract names
  `tests/fixtures/parser_regression_match_slice.log` as the exact first
  fixture candidate.
- The contract chooses a new reduced parser-owned expected output rather than
  promoting `parser_regression_match_expected.json` to the first v1 golden
  expected output.
- The contract names
  `tests/fixtures/parser_regression_match_golden_expected.json` as the reduced
  expected output path.
- The contract names
  `tests/fixtures/golden_fixture_manifest.json` as the first metadata
  mechanism.
- Required and not-applicable provenance fields are defined.
- The contract defines what the fixture proves and does not prove.
- Parser truth ownership and fixture/test-oracle boundaries are preserved.
- Fixture drift-budget interpretation is explicit.
- Protected surfaces and forbidden side effects are named.
- Validation commands are defined for Codex B, Codex C, Codex E/F escalation,
  and fixture-related changes.
- Expected Codex C handoff and Codex E report artifacts are named.
- The contract includes a pasteable Codex C prompt.
- The contract includes a `workflow_handoff` block.
- No fixture, code, parser behavior, schema, webhook/App Script, CI gate,
  secret, raw log, generated data, runtime status, failed post, workbook
  export, production behavior, or `main` targeting change is made by the
  contract writer pass.

## Unknowns

- Whether the reduced expected output should be generated directly from the
  replay helper or mechanically reduced from the current full expected JSON
  during Codex C implementation.
- Whether future fixture metadata should remain in one central manifest or move
  to sidecars when the fixture corpus grows.
- Whether future evidence-ledger fixture IDs should reuse this fixture ID or
  wrap it in a separate ledger fixture declaration.
- Whether the sanitizer module should eventually produce manifest metadata.
- Whether UUID-shaped or long opaque identifiers in older fixture slices should
  be normalized before those fixtures are accepted as v1 golden fixtures.
- Whether future fixture policy should require all parser regression fixtures
  to have metadata before new fixtures may be added.

## Suspected Gaps

- Existing parser replay fixtures remain legacy/unclassified until this first
  manifest is implemented.
- Existing sanitizer tests cover the sanitizer function but do not prove that
  existing committed fixtures were produced by that sanitizer.
- The secret/private-marker scanner can report sanitized fixture markers, but
  it is not a sanitizer and does not prove fixture provenance.
- The protected-surface gate allows `tests/fixtures/` paths by path, so
  content and provenance review remain necessary.
- No test currently verifies that a manifest entry points to a paired
  parser-owned expected output.
- No reduced parser-owned expected output fixture currently exists.
- No evidence-ledger value-source, confidence, finality, drift flag, or
  invariant metadata exists for this fixture.

## Expected Codex C Handoff

Codex C should produce:

- `docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md`

The handoff must include:

- role performed
- issue and tracker used
- contract used
- branch and git status
- files inspected
- what was implemented or intentionally left unchanged
- fixture candidate selected
- manifest fields added
- reduced expected output fields added
- exact test section changed
- validation run and result
- secret/private-marker scan result
- protected-surface result
- fixture drift-budget interpretation
- forbidden scopes touched or not touched
- remaining risks
- next recommended role
- pasteable Codex E prompt
- `workflow_handoff` block

## Expected Codex E Report

Codex E should produce:

- `docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md`

The report must lead with findings and verify:

- the selected fixture is exactly `parser_regression_match_slice.log`
- no new `.log` fixture was added
- existing input fixture content was not changed
- existing full expected output was not changed
- the manifest contains required provenance fields
- not-applicable fields have explicit reasons
- reduced expected output contains only allowed parser-owned output fields
- focused tests fail on missing or mismatched golden metadata/output
- secret/private-marker scan has no forbidden findings
- protected-surface checks are clean or explicitly authorized
- parser behavior, schema, webhook/App Script behavior, CI gates, secrets, raw
  logs, generated data, runtime status files, failed posts, workbook exports,
  live workbook state, deployed Apps Script state, and production behavior were
  not changed

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for repo-wide hardening issue #94: First sanitized golden fixture implementation pass.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/94

Branch:
codex/repo-wide-hardening-run

Contract:
docs/contracts/repo_wide_golden_fixture_first_pass.md

Goal:
Compare the current parser regression fixture/test surfaces against the contract. Implement only the smallest test/fixture-metadata changes needed to establish the first governed golden fixture acceptance path.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/repo_wide_golden_fixture_first_pass.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md
- docs/contract_test_reports/code_hardening_golden_fixture_policy.md
- docs/contracts/player_log_evidence_ledger.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- tests/test_parser_regressions.py
- tests/fixtures/parser_regression_match_slice.log
- tests/fixtures/parser_regression_match_expected.json
- tests/test_sanitize.py
- src/mythic_edge_parser/sanitize.py
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
- State what the first golden fixture pass is supposed to do, what current fixtures/tests already do, what gap remains, and the exact minimal implementation plan.

Do:
- Reuse tests/fixtures/parser_regression_match_slice.log as the only first-pass input fixture.
- Do not add or change any .log input fixture.
- Add tests/fixtures/golden_fixture_manifest.json with one entry for fixture_id parser_regression_match_bo1_v1.
- Add tests/fixtures/parser_regression_match_golden_expected.json containing only the reduced parser-owned expected output for match_log_row and game_log_rows.
- Add focused test coverage, likely in tests/test_parser_regressions.py, that loads the manifest, replays the fixture, reduces actual output to match_log_row and game_log_rows, and compares it to the reduced expected output.
- Ensure the reduced expected output does not include event traces, router stats, parser context, debug output, raw_json, raw log lines, local paths, webhook URLs, runtime status, failed posts, workbook exports, generated data, or live workbook/deployment identifiers.
- Produce docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md.

Do not:
- Change parser behavior.
- Change parser state final reconciliation.
- Change workbook schema.
- Change webhook payload shape.
- Change Apps Script behavior.
- Change parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, sync field names, runtime family names, runtime event_type values, or runtime scope values.
- Add new .log fixture data.
- Modify tests/fixtures/parser_regression_match_slice.log.
- Modify tests/fixtures/parser_regression_match_expected.json.
- Refresh schema snapshots.
- Add drift baselines.
- Implement sanitizer tooling.
- Implement the Player.log evidence ledger.
- Touch secrets, credentials, environment variables, raw local logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, CI gates, production behavior, or main.
- Stage, commit, open a PR, close issues, or mark tracker #82 complete unless explicitly asked.

Validation:
git status --short --branch
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py tests\test_check_surface_authorization.py tests\test_select_validation.py
py -m ruff check src tests tools
py -m pyright
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-94.md --authorization-file contract=docs\contracts\repo_wide_golden_fixture_first_pass.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_golden_fixture_first_pass_comparison.md
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
git diff --check

Final handoff must include:
- role performed
- issue/tracker
- contract used
- files changed
- exact test/fixture sections changed
- validation run and result
- fixture drift-budget interpretation
- protected-surface status
- secret/private-marker status
- what remains unverified
- whether forbidden scope was touched
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/94"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/repo_wide_golden_fixture_first_pass.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_golden_fixture_first_pass_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/repo_wide_golden_fixture_first_pass.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "git diff --check"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --paths-from-stdin --authorization-file contract=docs\\contracts\\repo_wide_golden_fixture_first_pass.md"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run"
  stop_conditions:
    - "Do not implement fixture metadata, expected output, tests, or code in Codex B."
    - "Do not add, copy, sanitize, or commit fixture data in Codex B."
    - "Do not add new .log input fixtures."
    - "Do not modify tests/fixtures/parser_regression_match_slice.log."
    - "Do not modify tests/fixtures/parser_regression_match_expected.json."
    - "Do not refresh schema snapshots or add drift baselines."
    - "Do not implement sanitizer tooling or the Player.log evidence ledger."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, live workbook state, deployed Apps Script state, CI gates, production behavior, or merge-to-main policy."
    - "Do not target main."
    - "Do not mark tracker #82 complete."
```
