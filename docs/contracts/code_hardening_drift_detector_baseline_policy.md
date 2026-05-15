# Code Hardening Drift Detector Baseline Policy Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/70

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Related evidence-ledger source issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous hardening context:

- Issue #68 / PR #69 added the golden fixture policy linked to the evidence
  ledger and merged into `codex/code-hardening-suite` at
  `1432f08dc1ee5e137f9576890dc7aab8fcd3c094`.
- Tracker #33 remains open.
- This issue defines drift detector baseline policy only.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Accepted ADRs read:

- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Current hardening contracts read:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`

Current code, tests, and fixtures read:

- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_check_protected_surfaces.py`
- `tools/check_protected_surfaces.py`
- `tests/fixtures/`

Remote evidence-ledger artifacts inspected from `origin/main` because they are
not currently present on `codex/code-hardening-suite`:

- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

This is a contract-writing artifact only. It does not create or modify drift
baselines, detector behavior, CI gates, fixtures, snapshots, parser behavior,
workbook schema, webhook shape, Apps Script behavior, parser event classes,
match/game identity, deduplication, secrets, raw logs, generated data, runtime
status files, failed posts, workbook exports, or local-only artifacts.

## Module

Drift detector baseline policy.

Plain English: a drift detector baseline is a reference comparison point for
the Player.log drift sensor. It helps answer "is this current log surface
different from the surface we expected?" It is a review signal, not parser
truth, not a schema migration, and not a CI failure gate unless a future issue,
contract, review, validation package, and explicit user approval escalate it.

## Owning Layer

Owning layer: Code Hardening drift report and baseline governance.

Truth boundary:

- MTGA `Player.log` is the only local observable evidence source, but not
  absolute game truth.
- Parser and state interpretation own parser truth for event interpretation,
  normalized match facts, and normalized game facts.
- The drift detector owns report-oriented QA signals about routing coverage,
  unknown log signatures, unmatched API names, and baseline deltas.
- Drift baselines are comparison artifacts. They do not own parser truth,
  workbook truth, webhook truth, Apps Script truth, schema truth, match/game
  identity, deduplication, final reconciliation, or production readiness.
- Golden fixtures, schema snapshots, protected-surface gates, PR drift budgets,
  and the future evidence ledger are related guardrails. None of them alone
  authorizes a baseline refresh or a failing gate.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`

Expected future comparison or review artifacts:

- `docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_drift_detector_baseline_policy.md`

Related files referenced but not owned by this contract:

- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/test_log_drift_sensor.py`
- `tests/fixtures/flush_timing_corpus_slice.log`
- `tests/fixtures/`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

Future files that require a separate issue or explicit implementation scope:

- any committed drift baseline
- any committed drift-report expected-output fixture
- any baseline manifest or sidecar
- any new sanitizer tool
- any new failing CI gate or workflow step
- any change to `log_drift_sensor.py`

## Public Interface

This contract creates no runtime public interface and changes no existing
function signature or CLI behavior.

Observed existing public-ish surfaces in `log_drift_sensor.py`:

- `build_player_log_drift_report(source_path, baseline_payload=None)`
- `write_player_log_drift_report(source_path=..., report_path=..., baseline_path=..., refresh_baseline=False)`
- command-line usage:

```powershell
py -m mythic_edge_parser.app.log_drift_sensor <source_log> --out <report.json> --baseline <baseline.json>
py -m mythic_edge_parser.app.log_drift_sensor <source_log> --out <report.json> --baseline <baseline.json> --refresh-baseline
```

Policy interface defined by this contract:

- what a drift detector baseline is
- report-only baseline semantics
- when reports remain informational
- evidence required before a failing gate
- refresh review policy
- future committed baseline metadata
- relationship to golden fixtures, schema snapshots, protected-surface gates,
  PR drift budgets, and the future evidence ledger

## Definitions

### Drift Detector Baseline

A drift detector baseline is a structured reference payload used by the
Player.log drift sensor to compare a current log analysis against a prior,
expected, or reviewed set of observed routing gaps.

Current baseline comparison inputs are the lists inside `baseline_payload`:

- `top_unknown_signatures`
- `top_unmatched_api_names`
- `top_unmatched_request_api_names`

The current detector computes these delta fields:

- `new_unknown_signatures`
- `resolved_unknown_signatures`
- `new_unmatched_api_names`
- `resolved_unmatched_api_names`
- `new_unmatched_request_api_names`
- `resolved_unmatched_request_api_names`

Important distinction:

- A baseline records "what the detector had seen or accepted for comparison."
- It does not record "what Arena guarantees."
- It does not record "what the parser should treat as true."
- It does not authorize ignoring newly missing evidence.

### Local Runtime Baseline

A local runtime baseline is a baseline JSON file written under an ignored or
runtime path for local comparison.

Observed default:

- `STATUS_ROOT / "player_log_drift_baseline.json"`

Policy:

- Local runtime baselines are operator aids.
- They may be refreshed locally for investigation.
- They must not be committed as local runtime status artifacts.
- They must not fail CI or block parser runtime by default.

### Committed Baseline

A committed baseline is any baseline or baseline-like expected drift output
checked into the repository.

Policy:

- No committed baseline exists in the current branch.
- This contract does not authorize creating one.
- A future committed baseline must comply with the golden fixture policy and a
  dedicated issue/contract.
- A committed baseline must be sanitized or synthetic, deterministic,
  provenance-labeled, reviewable, and paired with clear assertions.

### Report-Only Baseline

A report-only baseline produces comparison information without failing tests,
failing CI, blocking runtime, changing parser behavior, updating fixtures, or
refreshing snapshots.

Report-only means:

- drift report status values such as `review` are informational
- baseline deltas are review signals
- command exit behavior remains non-gating unless a future contract changes it
- local runtime reports and baselines remain local artifacts
- Codex threads may use reports to propose focused issues
- no baseline delta automatically authorizes code, fixture, snapshot, workbook,
  webhook, Apps Script, deployment, or parser truth changes

### Failing Gate

A failing gate is any test, CI step, local repo-check command, or runtime guard
that returns a failing status because a drift baseline comparison changed.

Policy:

- No failing drift baseline gate is authorized by issue #70.
- Escalating from report-only to failing requires explicit user approval and a
  new or amended contract.

## Inputs

### Source Log

Type: file path.

Observed source:

- `LOG_PATH`, usually local `Player.log`
- explicit `source_log` argument
- temporary files in tests
- committed sanitized fixtures copied into temporary files

Required policy:

- Local private `Player.log` may inform local reports and review.
- Raw local logs must not be committed.
- Committed inputs must be sanitized or synthetic and governed by the golden
  fixture policy.

### Baseline Payload

Type: JSON object / Python `dict[str, Any]`.

Observed accepted shape:

```json
{
  "top_unknown_signatures": [{"signature": "QuestGetQuests", "count": 1}],
  "top_unmatched_api_names": [{"api_name": "QuestGetQuests", "count": 1}],
  "top_unmatched_request_api_names": []
}
```

Observed tolerant behavior:

- Missing baseline file loads as an empty payload.
- Invalid JSON or non-object JSON loads as an empty payload.
- Missing expected list keys behave like empty lists.

Required policy:

- Empty or malformed baselines must not be treated as proof of no drift.
- If a baseline is missing, the report may still run, but review should state
  that no meaningful prior baseline was available.
- A future failing gate must define missing or malformed baseline behavior
  explicitly before it can fail CI.

### Detector Output

Type: JSON object / Python `dict[str, Any]`.

Observed current fields:

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

Required policy:

- Local reports may include local `source_path` and volatile `analyzed_at`
  because they are runtime artifacts.
- Committed expected outputs must normalize or omit volatile and local-only
  fields.

## Outputs

### Local Drift Report

Destination:

- observed default `STATUS_ROOT / "player_log_drift_latest.json"`
- explicit `--out` path
- temporary test paths

Semantics:

- local QA/provenance report
- informational by default
- not parser truth
- not workbook truth
- not a committed artifact unless a future contract explicitly authorizes a
  sanitized expected-output fixture

### Local Drift Baseline

Destination:

- observed default `STATUS_ROOT / "player_log_drift_baseline.json"`
- explicit `--baseline` path
- temporary test paths

Semantics:

- local comparison reference
- refreshable locally with `--refresh-baseline`
- not a committed artifact
- not a CI authority

### Future Committed Baseline Or Expected Output

Destination:

- not defined by this contract

Required future behavior if authorized:

- store under an approved fixture path
- comply with golden fixture policy
- include provenance metadata
- normalize volatile fields
- exclude raw local paths and private content
- remain report-only unless a separate gate contract escalates it

## Observed Current Behavior

Observed on `codex/code-hardening-suite` during this contract pass:

- Current HEAD is
  `1432f08dc1ee5e137f9576890dc7aab8fcd3c094`, the PR #69 merge.
- `docs/contracts/code_hardening_golden_fixture_policy.md` exists locally.
- The Player.log evidence-ledger problem representation and contract are
  absent locally on this branch and were read from `origin/main`.
- `tools/check_secret_patterns.py` is absent on this branch.
- No committed drift baseline file exists in `tests/fixtures/` or
  `tests/fixtures/schema_snapshots/`.

Observed `log_drift_sensor.py` behavior:

- `DEFAULT_DRIFT_REPORT_PATH` is `STATUS_ROOT / "player_log_drift_latest.json"`.
- `DEFAULT_DRIFT_BASELINE_PATH` is
  `STATUS_ROOT / "player_log_drift_baseline.json"`.
- `iter_log_entries()` reads a log file through `LineBuffer`.
- `build_player_log_drift_report()` routes entries through `Router`, counts
  headers, routed event kinds, unknown signatures, unmatched API names, and
  unmatched request API names.
- `_entry_signature()` redacts UUID-shaped values, long numbers, and long
  token-like values when deriving fallback signatures.
- `_entry_signature()` prefers API names or prefix labels where available.
- `_baseline_delta()` compares current unknown/unmatched sets to baseline
  unknown/unmatched sets.
- `build_player_log_drift_report()` currently sets `status` to `review` when
  router unknown count is nonzero, when new unknown signatures exist, or when
  new unmatched API names exist.
- Observed status logic does not include
  `new_unmatched_request_api_names` in the `status == "review"` condition.
  That is observed behavior only, not a contract change in this thread.
- `write_player_log_drift_report()` writes the report and overwrites the
  baseline only when `refresh_baseline=True`.
- The CLI prints a summary, report path, optional baseline refresh path, and
  selected new unmatched or unknown values.
- The CLI returns `0` on normal completion. It is not a failing drift gate.

Observed tests:

- `tests/test_log_drift_sensor.py` copies
  `tests/fixtures/flush_timing_corpus_slice.log` into a temporary
  `Player.log`.
- The report test asserts `status == "review"`, unknown entries are present,
  and selected unmatched API names are surfaced.
- The baseline-delta test writes a temporary `baseline.json`, then asserts new
  unmatched API names and new unmatched request API names are reported.
- The privacy test asserts a prefix label is preferred over an identity-bearing
  raw line.

Observed fixture and gate relationships:

- `tests/fixtures/flush_timing_corpus_slice.log` is a committed sanitized
  slice used by the drift sensor tests.
- `tools/check_protected_surfaces.py` forbids `data/status/**`, raw
  `Player.log` names, `data/match_logs/**`, failed posts, runtime logs,
  generated data, workbook exports, secret filenames, and webhook credential
  filenames.
- The protected-surface gate allows documented fixtures under
  `tests/fixtures/` by path. That path allowance is not content sanitization.
- Schema snapshot tests have explicit update approval messaging and an
  opt-in update environment variable. Drift baselines do not currently have an
  equivalent committed-baseline update mechanism.

## Required Guarantees

### Report-Only First Rollout

Drift detector baselines must remain report-only unless a future contract
explicitly escalates them.

Required behavior:

- Local reports may be written.
- Local baselines may be read.
- Local baselines may be refreshed only through explicit operator action.
- Reports may identify new and resolved unknown signatures.
- Reports may identify new and resolved unmatched API names.
- Reports may identify new and resolved unmatched request API names.
- Reports may help create focused follow-up issues.
- Reports may guide parser audit prioritization.

Forbidden without future escalation:

- failing CI because of baseline deltas
- failing repo checks because of baseline deltas
- blocking parser runtime because of baseline deltas
- auto-refreshing committed fixtures or snapshots
- auto-refreshing local or committed baselines in CI
- authorizing parser behavior changes
- authorizing workbook schema changes
- authorizing webhook payload changes
- authorizing Apps Script changes
- authorizing deployment changes

### Informational Report Conditions

Drift reports must remain informational when any of these are true:

- the report is generated from local private `Player.log`
- the baseline is local-only
- the baseline is missing or malformed
- the baseline lacks provenance metadata
- the source evidence is not a committed sanitized fixture or synthetic input
- the report includes volatile local fields such as `source_path` or
  `analyzed_at`
- no issue and contract authorizes a failing gate
- the affected parser-managed outputs have not been mapped through the
  evidence-ledger vocabulary
- false-positive and false-negative behavior is undocumented
- thresholds for actionable drift are undefined
- secret/content scanning is unavailable or not run for committed evidence
- the drift could be parser routing improvement, fixture update, schema
  update, or Arena log drift and has not been classified

### Evidence Required Before A Failing Gate

A drift baseline may become a failing gate only after all of these exist:

- explicit GitHub issue for gate escalation
- explicit module contract or amended contract authorizing the failing gate
- explicit user approval for escalation from report-only to failing
- deterministic sanitized or synthetic input fixtures if the gate depends on
  log evidence
- baseline provenance metadata
- redaction notes and privacy review
- documented update command and update approval policy
- documented threshold policy for actionable drift
- documented false-positive and false-negative behavior
- focused tests for pass, fail, missing baseline, malformed baseline, and
  baseline refresh behavior
- CI/local invocation design that does not read private local logs
- protected-surface gate output
- secret/content scan when such a tool exists
- mapping from drift signal to affected parser-managed output families, or an
  explicit statement that the gate covers only routing coverage
- PR drift-budget disclosure for fixtures/evidence and protected-surface
  authorization
- Codex E review with no blocking findings

Passing `tests/test_log_drift_sensor.py` is necessary but not sufficient for a
failing baseline gate.

### Baseline Refresh Review Policy

Local refresh policy:

- `--refresh-baseline` may remain a local/operator action.
- Local refreshes may overwrite local runtime baseline files.
- Local refreshes must not be committed.
- Local refreshes must not be treated as parser validation by themselves.

Future committed refresh policy:

- A committed baseline refresh requires a dedicated issue and contract.
- The PR must show the baseline diff.
- The PR must cite the source evidence, fixture IDs, schema snapshots, parser
  commit, detector version or commit, related ADRs, and reason for refresh.
- The PR must explain whether changes are due to an Arena update, parser
  routing change, fixture update, schema snapshot update, sanitizer update, or
  expected-output change.
- The PR must summarize new and resolved unknown signatures.
- The PR must summarize new and resolved unmatched API names.
- The PR must summarize new and resolved unmatched request API names.
- The PR should summarize routed event kind changes when the detector or
  baseline format supports that.
- The PR must identify suspected affected parser-managed output families when
  possible.
- The PR must state whether parser code changed. If parser behavior changed,
  the baseline refresh must not hide that change.
- The PR must not mix unrelated parser behavior fixes with a baseline-only
  refresh unless the issue and contract explicitly authorize the combined
  scope.

Not enough for refresh approval:

- "The detector generated this file."
- "The old baseline was noisy."
- "CI is failing."
- "Arena probably changed."
- "The workbook still looks fine."
- "AI/codegen updated it."

### Future Committed Baseline Metadata

If a future issue authorizes a committed baseline or drift-report expected
output, it must include or reference metadata with these fields:

- `baseline_id`
- `baseline_schema_version`
- `baseline_class`
- `source_issue`
- `source_contract`
- `related_adrs`
- `source_fixture_ids`
- `source_type`
- `source_privacy_class`
- `redaction_status`
- `redaction_notes`
- `detector_owner`
- `detector_commit_or_version`
- `parser_commit_or_version`
- `generated_at_policy`
- `source_path_policy`
- `covered_report_fields`
- `excluded_report_fields`
- `threshold_policy`
- `allowed_delta_policy`
- `false_positive_policy`
- `false_negative_policy`
- `affected_output_families`
- `evidence_ledger_tiers`
- `drift_flags_expected`
- `refresh_command`
- `refresh_approval_required`
- `known_limitations`

Allowed `baseline_class` values:

- `local_runtime_baseline`
- `sanitized_fixture_baseline`
- `synthetic_fixture_baseline`
- `committed_expected_drift_report`
- `report_only_reference`
- `failing_gate_reference`

Allowed `source_privacy_class` values:

- `local_private_raw`
- `sanitized_committable`
- `synthetic_committable`
- `repo_static`

Committed baselines must not use `local_private_raw`.

## Relationship To Other Guardrails

### Golden Fixtures

Drift baselines become golden-fixture-adjacent when they are committed or used
as expected output.

Required relationship:

- committed baselines must follow the golden fixture policy
- committed baselines must be sanitized or synthetic
- committed baselines must not contain local `source_path` values
- committed baselines must not contain volatile timestamps as oracle values
- committed baselines must include provenance metadata
- committed baselines must not be refreshed without issue, contract, and review

This contract does not create any golden fixtures or drift expected-output
fixtures.

### Schema Snapshots

Schema snapshots protect parser event, payload, workbook-facing row, runtime
row, and repo-side Apps Script shape surfaces.

Required relationship:

- drift baselines do not authorize schema snapshot updates
- schema snapshot updates do not authorize baseline refreshes
- both require issue, contract, review, and explicit update policy
- if a drift report points to a schema or event-shape change, route to the
  schema snapshot contract or a new parser/schema issue

### Protected-Surface Gate

The protected-surface gate protects against forbidden paths and reports
protected source paths.

Required relationship:

- local runtime drift reports and baselines under `data/status/**` are
  forbidden committed artifacts by path
- raw local logs are forbidden committed artifacts by path
- fixture paths under `tests/fixtures/` are path-allowed but still require
  policy, redaction, and review before new evidence-derived data is safe
- protected-surface warnings are review signals, not authorization

### PR Drift Budget

Any PR that creates, removes, refreshes, commits, or reinterprets a drift
baseline must fill the PR drift budget.

Required interpretation:

- `Runtime/parser behavior`: `No drift` for policy/docs-only baseline work
  unless detector or parser behavior changed.
- `Parser event shape/classes`: `No drift` unless event classes, kinds, or
  payload shapes changed.
- `Workbook/webhook/App Script shape`: `No drift` unless those surfaces changed.
- `Parser truth ownership`: `No drift` unless the PR moves truth ownership.
- `Fixtures/evidence`: `Authorized drift` if baseline or evidence fixtures are
  changed under an issue and contract.
- `Protected-surface authorization`: cite issue and contract for any warned
  protected path.
- `Residual drift / accepted gaps`: name report-only status, unimplemented
  ledger mapping, missing content scan, or accepted false-positive risks.

### Future Player.log Evidence Ledger

The future evidence ledger should eventually connect drift reports to affected
parser-managed outputs.

Required relationship:

- baseline policy must preserve the evidence-ledger vocabulary
- drift reports should eventually distinguish missing expected event families,
  missing payload paths, changed signal types, unknown event families, parser
  exceptions, transport failures, workbook drift, deployment drift, fixture
  gaps, and sensitive evidence redaction
- the detector may suggest affected output families, but parser/state remains
  the interpretation owner
- before ledger implementation, baseline deltas are routing coverage signals,
  not field-level truth metadata

## Invariants

- Drift detector baselines are evidence comparison artifacts, not parser truth.
- Report-only baselines must not fail CI, fail tests, block runtime, or change
  parser behavior by default.
- Local private `Player.log` may inform local drift reports but must not become
  a committed artifact.
- Local runtime reports and baselines under runtime status paths must not be
  committed.
- Baseline refresh must be explicit and reviewed before anything committed is
  updated.
- A missing or malformed baseline must not be interpreted as "no drift."
- A drift report must distinguish parser evidence drift from webhook transport
  failure, workbook drift, deployed Apps Script drift, local artifact drift, and
  AI/analytics interpretation.
- A failing gate requires a separate escalation issue, contract, review,
  validation, and user approval.
- Passing tests are necessary but not sufficient to approve a baseline refresh.
- Parser/state truth ownership from ADR-0001 remains unchanged.

## Error Behavior

Observed current behavior:

- Missing baseline file loads as `{}`.
- Invalid JSON baseline loads as `{}`.
- Non-object JSON baseline loads as `{}`.
- Missing baseline keys behave like empty sets.
- Missing or unreadable source logs are not covered by current focused tests.
- The CLI is not a drift gate and returns `0` on normal completion.

Required policy:

- Missing or malformed baselines are informational-report conditions unless a
  future gate contract defines stricter behavior.
- Future failing gate behavior must define missing baseline, malformed
  baseline, unreadable source log, empty source log, redacted source content,
  and detector exception behavior.
- Future committed expected outputs must normalize or omit local and volatile
  fields.
- Future review must classify drift as likely Arena log drift, parser routing
  drift, fixture drift, schema snapshot drift, sanitizer drift, transport
  drift, workbook drift, deployment drift, or unknown.

## Side Effects

Allowed side effect in this Codex B thread:

- create `docs/contracts/code_hardening_drift_detector_baseline_policy.md`

Observed existing runtime side effects when the detector is run:

- writes a drift report JSON to the requested or default report path
- may overwrite the requested or default baseline path when
  `refresh_baseline=True`
- prints a terminal summary

Forbidden side effects in this Codex B thread:

- no drift baseline creation or modification
- no detector behavior changes
- no CI gate changes
- no fixture changes
- no snapshot changes
- no parser behavior changes
- no runtime status file changes
- no raw-log sanitization
- no raw local log commits
- no PR creation
- no tracker closure

## Dependency Order

Future baseline-policy work should proceed in this order:

1. Confirm target branch is `codex/code-hardening-suite`.
2. Confirm the issue and contract authorize the exact baseline work.
3. Inspect `git status` and exclude unrelated files.
4. Classify the baseline as local runtime, sanitized fixture, synthetic
   fixture, committed expected report, report-only reference, or failing gate
   reference.
5. If committed, verify golden fixture policy compliance.
6. If schema/event shape is involved, verify schema snapshot policy compliance.
7. If any protected path is touched, record protected-surface authorization.
8. If a gate is proposed, route to a separate escalation contract before
   implementation.
9. Run focused validation.
10. Produce implementation handoff.
11. Route to Codex E for contract-test review.

Stop and route back to Codex B or A if the work requires parser behavior
changes, workbook/webhook/App Script changes, raw local log commitment,
committed baseline refresh without metadata, or CI failure gates not covered by
the current contract.

## Compatibility

- Existing `log_drift_sensor.py` report generation remains unchanged.
- Existing `--refresh-baseline` behavior remains local/operator controlled.
- Existing tests using temporary files remain valid.
- Existing schema snapshot update policy remains unchanged.
- Existing golden fixture policy remains the governing policy for committed
  sanitized evidence and expected outputs.
- Existing protected-surface gate remains path-based and does not become a
  baseline content scanner.
- Existing branch policy remains `codex/code-hardening-suite`, not `main`.

## Unknowns

- Whether committed drift baselines should ever exist, or whether future tests
  should prefer focused expected assertions.
- Whether a future committed baseline should be full report JSON, reduced
  semantic JSON, or a manifest-backed expected-output fixture.
- Whether `--refresh-baseline` should remain purely local forever.
- Whether report-only drift status should ever affect local exit codes.
- What exact threshold should count as actionable drift.
- How to classify new unmatched request API names relative to report status.
- How to distinguish parser routing improvements from Arena log drift without
  the future evidence ledger.
- Whether future drift reports should include affected parser-managed output
  families before the evidence ledger is implemented.
- Whether a content secret scanner must exist before any committed drift
  baseline is allowed.
- Whether future baseline review should include an expiration or review cadence.

## Suspected Gaps

- No dedicated drift detector baseline policy existed before this contract.
- No committed drift baseline exists.
- No committed drift-report expected-output fixture exists.
- Current detector reports include volatile `analyzed_at` and local
  `source_path`, which are appropriate locally but unsuitable as committed
  oracle fields without normalization.
- Current baseline payload shape is implicit in `log_drift_sensor.py` and
  focused tests rather than a standalone schema.
- Current `status == "review"` logic does not appear to consider
  `new_unmatched_request_api_names`.
- Current tests cover selected baseline delta behavior but not missing
  baseline, malformed baseline, refresh overwrite behavior, CLI output, or
  future committed baseline metadata.
- The evidence ledger is not implemented, so drift reports do not yet map
  signals to affected parser-managed output families.
- `tools/check_secret_patterns.py` is absent on this branch, so content-level
  privacy review depends on manual review and focused tests.
- Protected-surface gate forbids runtime status paths, which is correct, but it
  does not inspect untracked local reports or baseline content by default.

## Validation Requirements

### Contract-Writer Validation

Because this Codex B thread creates only a new Markdown file:

```powershell
git diff --check
git diff --no-index --check -- NUL docs\contracts\code_hardening_drift_detector_baseline_policy.md
```

Recommended path-scoped protected-surface check:

```powershell
'docs/contracts/code_hardening_drift_detector_baseline_policy.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Runtime tests are not required for a docs-only contract writer pass.

### Future Codex C Comparison Validation

For a docs-only comparison:

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
rg -n "baseline|refresh|report-only|drift|Player.log|fixture|snapshot|protected" docs\contracts src\mythic_edge_parser\app\log_drift_sensor.py tests\test_log_drift_sensor.py tests\fixtures
```

If Codex C edits only Markdown docs, parser tests are optional and should be
reported as skipped because no runtime code changed.

### Future Detector Or Baseline Implementation Validation

If a future issue authorizes detector code, tests, fixture, or baseline changes:

```powershell
py -m pytest -q tests\test_log_drift_sensor.py
py -m pytest -q tests\test_parser_regressions.py tests\test_event_schema_snapshots.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check
```

If a future content secret scanner exists:

```powershell
py tools\check_secret_patterns.py --all
```

Before a future PR that changes baselines, fixtures, detector code, or gates:

```powershell
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check
```

Interpretation:

- Pyright remains advisory unless a future contract escalates it.
- Full-suite validation is recommended before submitter work if any committed
  baseline, detector behavior, fixture, or expected output changes.
- Any failing drift gate requires separate validation beyond this contract.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- CI failure gates
- detector behavior
- `--refresh-baseline` semantics
- committed fixtures
- schema snapshots
- expected parser outputs
- secrets, credentials, tokens, API keys, or webhook URLs
- environment variable contracts
- raw local logs
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## Out Of Scope

This issue does not authorize:

- creating or modifying drift baselines
- changing `log_drift_sensor.py`
- changing `--refresh-baseline` behavior
- adding failing CI gates
- refreshing schema snapshots
- refreshing parser expected outputs
- creating or modifying fixture files
- committing raw `Player.log` files
- adding sanitized fixture data
- implementing sanitizer tooling
- implementing the Player.log evidence ledger
- changing parser behavior
- changing parser truth ownership
- changing workbook behavior
- changing webhook behavior
- changing Apps Script behavior
- changing deployment behavior
- targeting `main`
- marking tracker #33 complete

## Acceptance Criteria

- `docs/contracts/code_hardening_drift_detector_baseline_policy.md` exists.
- The contract defines what a drift detector baseline is.
- The contract defines report-only baseline semantics.
- The contract defines when drift reports remain informational.
- The contract defines evidence required before a failing gate.
- The contract defines baseline refresh review policy.
- The contract defines future committed baseline metadata expectations.
- The contract explains relationship to golden fixtures, schema snapshots,
  protected-surface gates, PR drift budgets, and the future evidence ledger.
- The contract distinguishes observed current behavior, required guarantees,
  unknowns, and suspected gaps.
- The contract preserves parser truth ownership and protected-surface
  boundaries.
- The contract includes expected validation evidence for Codex C/E work.
- The contract includes a pasteable Codex C handoff prompt.
- The contract does not create or modify baselines, detector behavior, CI
  gates, fixtures, snapshots, parser behavior, workbook schema, webhook shape,
  Apps Script behavior, parser event classes, match/game identity,
  deduplication, secrets, raw logs, generated data, runtime status files,
  failed posts, workbook exports, or local-only artifacts.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue used: https://github.com/Tahjali11/Mythic-Edge/issues/70

Contract artifact produced:
`docs/contracts/code_hardening_drift_detector_baseline_policy.md`

Risk tier: Medium for policy-only hardening. Escalate to High if future work
creates or modifies committed baselines, changes detector behavior, changes
refresh semantics, adds failing gates, refreshes snapshots/expected outputs,
creates fixtures from `Player.log`, or touches protected runtime surfaces.

Owning truth layer: Code Hardening drift report and baseline governance;
parser/state remains truth owner for event interpretation and normalized
match/game facts.

Public interface:

- policy definition of drift detector baselines
- report-only baseline semantics
- baseline refresh review policy
- future committed baseline metadata
- validation and escalation requirements

Invariants:

- Baselines are comparison artifacts, not truth owners.
- Report-only remains the default.
- Failing gates require future issue, contract, validation, review, and user
  approval.
- Local private `Player.log` and runtime status artifacts must not be
  committed.
- Baseline refresh must not normalize drift before parser/evidence review.

Required tests and validation: listed above.

Acceptance criteria: listed above.

Unknowns and suspected gaps: listed above.

Next recommended role: Codex C: Module Implementer / comparison thread.

Pasteable Codex C prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for the Code Hardening child issue: Drift detector baseline policy.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/70

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/code_hardening_drift_detector_baseline_policy.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- src/mythic_edge_parser/app/log_drift_sensor.py
- tests/test_log_drift_sensor.py
- tests/test_event_schema_snapshots.py
- tests/test_check_protected_surfaces.py
- tests/fixtures/
- origin/main:docs/problem_representations/player_log_evidence_ledger.md
- origin/main:docs/contracts/player_log_evidence_ledger.md

Goal:
Compare current drift detector code, tests, fixtures, and hardening docs against docs/contracts/code_hardening_drift_detector_baseline_policy.md. Produce docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md. Keep the pass comparison/docs-focused unless explicitly authorized to implement more.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Inspect git status and exclude unrelated changes.
- State what drift detector baselines are supposed to do, what current log_drift_sensor.py behavior already does, what policy gaps remain, and the exact minimal comparison or implementation plan.

Do:
- Compare build/write/report/baseline behavior against the contract.
- Compare tests/test_log_drift_sensor.py against report-only and baseline-delta expectations.
- Compare fixture, schema snapshot, protected-surface, and PR drift-budget relationships.
- Identify contract matches, gaps, missing tests, and whether any implementation is actually required.
- Produce docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md with files inspected, observed behavior, contract matches, contract gaps, protected-surface status, validation, remaining risks, and next recommended role.

Do not:
- Create or modify drift baselines.
- Change log drift detector behavior.
- Change --refresh-baseline behavior.
- Add failing CI gates.
- Refresh schema snapshots or expected outputs.
- Create or modify fixture files.
- Commit raw Player.log files.
- Add sanitized fixture data.
- Implement sanitizer tooling.
- Implement the Player.log evidence ledger.
- Modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
'docs/contracts/code_hardening_drift_detector_baseline_policy.md','docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md' | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py -m pytest -q tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/70"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_drift_detector_baseline_policy.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_drift_detector_baseline_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "git diff --no-index --check -- NUL docs\\contracts\\code_hardening_drift_detector_baseline_policy.md"
  stop_conditions:
    - "Do not create or modify drift baselines."
    - "Do not change log drift detector behavior or --refresh-baseline semantics."
    - "Do not add failing CI gates."
    - "Do not refresh schema snapshots or parser expected outputs."
    - "Do not create or modify fixture files, commit raw Player.log files, or add sanitized fixture data."
    - "Do not implement sanitizer tooling or the Player.log evidence ledger."
    - "Do not modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
