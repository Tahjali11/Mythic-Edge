# Code Hardening Golden Fixture Policy Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/68

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Related evidence-ledger source issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Hardening contracts and current surfaces read:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `tests/test_parser_regressions.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_check_protected_surfaces.py`
- `tools/check_protected_surfaces.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/fixtures/`

Remote evidence-ledger artifacts inspected from `origin/main` because they are
not currently present on `codex/code-hardening-suite`:

- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

This contract defines how Mythic Edge may turn local `Player.log` evidence,
parser replay slices, expected parser outputs, schema snapshots, and future
drift-report baselines into committed golden fixtures safely. It is a contract
artifact only. It does not create fixture files, add sanitized fixture data,
sanitize raw logs, implement sanitizer tooling, implement the evidence ledger,
refresh drift detector baselines, open a PR, target `main`, or mark tracker
#33 complete.

## Module

Golden fixture policy linked to the Player.log evidence ledger.

Plain English: golden fixtures are committed examples that tests treat as
trusted reference cases. They are useful only if they are sanitized,
representative, paired with explicit expected output, and reviewed when they
change. They must not become a private-log dump, a second parser, or an
unreviewed way to bless schema drift.

## Owning Layer

Owning layer: Code Hardening test and fixture governance.

Truth boundary:

- MTGA `Player.log` is the project's ultimate local observable evidence
  source, but not absolute game truth.
- Parser and state interpretation own parser truth for match/game facts.
- `models.py`, `state.py`, `extractors.py`, parser modules, and schema/export
  modules remain the owning code for parser behavior and output shape.
- Golden fixtures are evidence and test oracles. They prove that current code
  still handles selected evidence the same way; they do not define new parser
  semantics by themselves.
- The future Player.log evidence ledger may explain provenance, labels,
  confidence, finality, drift, invariants, and degradation. It must remain a
  QA/provenance layer, not a second parser.
- Workbook formulas, helper tabs, dashboards, Apps Script, webhook transport,
  and AI/analytics consumers must not use fixture content to override
  parser-owned truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/code_hardening_golden_fixture_policy.md`

Future policy implementation or comparison artifacts, if authorized:

- `docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md`
- `docs/contract_test_reports/code_hardening_golden_fixture_policy.md`
- optional fixture manifest or documentation artifact if a future issue
  explicitly authorizes it

Related files referenced but not owned by this contract:

- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_slice.log`
- `tests/fixtures/parser_regression_bo3_expected.json`
- `tests/fixtures/flush_timing_corpus_slice.log`
- `tests/fixtures/router_smoke_slice.log`
- `tests/fixtures/schema_snapshots/*.json`
- `tests/test_parser_regressions.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_drift_sensor.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`, if added by a future hardening issue
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

## Public Interface

This contract creates no runtime public interface.

The policy interface for future fixture work is:

- fixture class vocabulary
- provenance metadata requirements
- redaction requirements
- input-to-expected-output pairing requirements
- update and review workflow
- validation expectations
- protected-surface and out-of-scope boundaries

Future implementations may choose a machine-readable representation such as:

- a central `tests/fixtures/fixture_manifest.json`
- one sidecar metadata file per fixture
- a Markdown fixture index plus focused tests
- Python dataclasses or constants that can render a manifest

V1 policy preference: a future machine-readable manifest or sidecar system is
preferred for new golden fixtures, but this contract does not authorize adding
that artifact in the contract writer pass. Existing fixtures are legacy
fixtures until a future implementation issue explicitly retrofits metadata.

## Observed Current Behavior

Observed on `codex/code-hardening-suite` during this contract pass:

- Current branch is `codex/code-hardening-suite`.
- The branch is aligned with `origin/codex/code-hardening-suite`.
- Current HEAD is
  `0d84dc7` / PR #67 merge, after the accepted seed ADRs.
- `docs/decisions/ADR-0001-parser-owns-truth.md`,
  `docs/decisions/ADR-0003-player-log-drift-policy.md`, and
  `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
  exist and are accepted.
- `docs/problem_representations/player_log_evidence_ledger.md` and
  `docs/contracts/player_log_evidence_ledger.md` are absent locally on this
  hardening branch, but present on `origin/main`.
- `tools/check_secret_patterns.py` is absent on the current branch.
- `src/mythic_edge_parser/app/log_drift_sensor.py` exists and writes local
  drift reports by default under runtime status paths.

Observed committed fixture and snapshot surfaces:

- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_slice.log`
- `tests/fixtures/parser_regression_bo3_expected.json`
- `tests/fixtures/flush_timing_corpus_slice.log`
- `tests/fixtures/router_smoke_slice.log`
- `tests/fixtures/schema_snapshots/apps_script_repo_parity.json`
- `tests/fixtures/schema_snapshots/parser_event_classes.json`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/schema_snapshots/runtime_export_row_keys.json`
- `tests/fixtures/schema_snapshots/sheet_schema_surfaces.json`
- `tests/fixtures/schema_snapshots/workbook_row_keys.json`

Observed test behavior:

- `tests/test_parser_regressions.py` replays selected `.log` fixture slices
  through `LineBuffer`, `Router`, parser transforms, and parser state, then
  compares full snapshots against paired `*_expected.json` files.
- Parser regression expected outputs include event traces, router stats,
  context, match summary debug dictionaries, match rows, match-log rows, and
  game-log rows.
- `tests/test_event_schema_snapshots.py` snapshots parser event classes,
  payload keys, workbook row keys, sheet schema surfaces, runtime export row
  keys, and repo-side Apps Script parity.
- Schema snapshot tests use
  `MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS=1` as an explicit opt-in update mode
  and include a failure message that says not to auto-update snapshots without
  explicit issue, contract, and review approval.
- Schema snapshot tests reject selected forbidden value snippets such as
  webhook URLs, local user paths, local runtime data paths, failed posts, and
  deployment labels.
- `tests/test_log_drift_sensor.py` uses
  `tests/fixtures/flush_timing_corpus_slice.log` as committed input, copies it
  to a temporary `Player.log`, builds a drift report, and asserts unknown or
  unmatched API names and baseline deltas.
- `tests/test_log_drift_sensor.py` asserts that `_entry_signature()` prefers a
  prefix label for privacy instead of preserving a full identity-bearing line.
- `tests/test_check_protected_surfaces.py` verifies that raw `Player.log`
  filenames and local data paths are forbidden, while documented fixtures
  under `tests/fixtures/` are allowed by path.

Observed `log_drift_sensor.py` behavior:

- `build_player_log_drift_report(source_path, baseline_payload=None)` reads a
  log file, routes entries, counts routed and unknown entries, summarizes
  unknown signatures, unmatched API names, unmatched request API names, and
  baseline deltas.
- `write_player_log_drift_report()` writes a local report and can refresh a
  baseline when `refresh_baseline=True`.
- Default report and baseline paths live under the runtime status root.
- The report currently includes `source_path` as a string, `analyzed_at` as the
  current UTC timestamp, entry counts, routed event kinds, unknown signatures,
  unmatched API names, unmatched request API names, and baseline deltas.
- Current drift reports are local runtime artifacts. They are not committed
  golden fixtures under this contract.

## Observed Evidence Ledger Context

The `origin/main` evidence-ledger contract defines:

- `Player.log` as evidence, not absolute game truth.
- parser/state as the interpretation layer.
- value-source labels: `observed`, `derived`, `inferred`, `unknown`,
  `conflict`, `legacy_enriched`
- confidence labels: `high`, `medium`, `low`, `unknown`
- finality labels: `live`, `provisional`, `final`, `reconciled`
- drift flags such as `missing_expected_event_family`,
  `missing_expected_payload_path`, `changed_signal_type`,
  `new_unknown_event_family`, `new_unknown_payload_path`, `fallback_used`,
  `weak_fallback_used`, `conflicting_evidence`, `invariant_failed`,
  `schema_snapshot_missing`, `fixture_gap`, `parser_exception`,
  `transport_failure`, `workbook_drift`, `deployment_drift`, and
  `sensitive_evidence_redacted`
- invariant statuses: `passed`, `failed`, `not_applicable`, `not_checked`,
  `degraded`
- Tier 0 evidence and quality metadata
- Tier 1 match identity and lifecycle
- Tier 2 queue, format, rank, and event context
- Tier 3 game-level facts
- Tier 4 sideboarding and deck state
- Tier 5 card identity and gameplay actions
- Tier 6 runtime health and drift detection
- Tier 7 derived analytics outputs
- golden fixture requirements for committed redacted fixtures or synthetic
  structured fixtures

This contract narrows that ledger context into a hardening policy for committed
fixtures. It does not implement the ledger itself.

## Fixture Classes

### `sanitized_player_log_excerpt`

Definition:

- A committed `.log` excerpt derived from `Player.log` or a saved log slice
  after redaction and review.

Allowed uses:

- parser replay
- drift sensor tests
- evidence-ledger validation
- focused parser regression tests

Required traits:

- minimal lines needed for the covered behavior
- sanitized identity, local paths, tokens, IDs, URLs, and private content
- stable timestamps only when timing behavior is under test
- stable placeholder IDs that preserve relationships without exposing private
  identifiers
- comment header that describes the covered behavior without private source
  details

Forbidden traits:

- raw local `Player.log`
- full session dumps
- webhook URLs
- account IDs, display names, screen names, or opponent identities from a real
  user unless replaced with placeholders
- live workbook IDs, deployment IDs, local absolute paths, or credentials

Current examples:

- `tests/fixtures/parser_regression_match_slice.log`
- `tests/fixtures/parser_regression_bo3_slice.log`
- `tests/fixtures/flush_timing_corpus_slice.log`
- `tests/fixtures/router_smoke_slice.log`

### `parser_replay_fixture`

Definition:

- A replayable committed input fixture that exercises parser routing,
  transforms, state updates, and output construction.

Allowed uses:

- regression tests that replay a log slice through the parser
- evidence-ledger tests that map parser-managed outputs to raw evidence

Required traits:

- deterministic replay from a clean clone
- no network, live workbook, live Apps Script, local runtime file, or private
  log dependency
- documented parser surfaces exercised by the fixture
- expected-output pairing unless the test only asserts parser health or a
  local drift-report summary

Current examples:

- `parser_regression_match_slice.log`
- `parser_regression_bo3_slice.log`

### `parser_expected_output_snapshot`

Definition:

- A committed expected-output file paired with a replay fixture and used as a
  test oracle for parser-owned outputs.

Allowed uses:

- match/game row regression snapshots
- event trace snapshots
- parser context snapshots
- future evidence-ledger expected field-evidence snapshots

Required traits:

- paired with a specific input fixture
- generated by an explicit, reviewed command or helper
- stable JSON encoding
- no raw local log payloads beyond the sanitized fixture evidence already
  approved
- no local absolute paths, current timestamps, credentials, runtime status
  paths, failed posts, workbook exports, or generated card data

Current examples:

- `tests/fixtures/parser_regression_match_expected.json`
- `tests/fixtures/parser_regression_bo3_expected.json`

### `schema_snapshot_fixture`

Definition:

- A committed snapshot of stable schema surfaces, event classes, payload key
  sets, workbook-facing row keys, runtime row keys, or repo-side Apps Script
  parity.

Allowed uses:

- accidental schema drift detection
- code review evidence for protected schema surfaces

Required traits:

- schema shape, key order, class names, event kind values, or parity metadata
  only
- no raw private values
- explicit opt-in update flow
- update failure message that names issue/contract/review approval

Current examples:

- `tests/fixtures/schema_snapshots/*.json`

### `drift_report_expected_output`

Definition:

- A future committed expected-output file for a drift-report test, derived from
  sanitized evidence or synthetic inputs.

Allowed uses:

- proving unknown event families, missing payload paths, changed types, or
  baseline deltas are reported deterministically
- proving parser evidence drift remains separate from transport, workbook,
  deployment, or analytics drift

Required traits:

- no local source paths in the committed expected output
- no volatile `analyzed_at` values unless normalized
- no raw private unknown-entry text
- baseline refresh must be explicit and reviewed

Current status:

- Not implemented as a committed golden class. Current drift sensor tests use
  temporary local paths and direct assertions rather than committed full
  expected-report JSON.

### `evidence_ledger_fixture`

Definition:

- A future fixture pairing sanitized evidence with expected evidence-ledger
  metadata for parser-managed outputs.

Allowed uses:

- validating value-source labels
- validating confidence labels
- validating finality labels
- validating drift flags, invariant statuses, degradation behavior, and
  review-required flags

Required traits:

- linked to evidence-ledger contract version
- references Tier 0 through Tier 7 output families as appropriate
- distinguishes direct evidence, fallback evidence, missing evidence, and
  conflicts
- no workbook schema or webhook payload shape changes unless separately
  authorized

Current status:

- Not implemented.

### `workbook_or_apps_script_parity_snapshot`

Definition:

- A committed repo-side snapshot that compares Python schema/export surfaces
  with repository Apps Script source or workbook-facing row keys.

Allowed uses:

- static parity checks from committed repo code
- protected schema review evidence

Required traits:

- repo-side only unless a future issue explicitly authorizes live workbook or
  deployed Apps Script checks
- no live spreadsheet IDs, deployment URLs, webhook URLs, or workbook exports
- clear statement that passing repo-side parity does not prove the live
  workbook or deployed Apps Script is current

Current examples:

- `tests/fixtures/schema_snapshots/apps_script_repo_parity.json`
- `tests/fixtures/schema_snapshots/workbook_row_keys.json`

## Required Guarantees

### General Fixture Guarantees

Committed golden fixtures must be:

- sanitized or synthetic
- minimal but representative
- deterministic from a clean clone
- explicitly paired with their expected parser-owned output or assertion target
- reviewable in a PR diff
- tied to an issue and contract
- free of secrets, credentials, webhook URLs, local-only paths, raw private
  logs, runtime status files, failed posts, generated card data, and workbook
  exports
- clear about whether they are parser replay input, expected parser output,
  schema snapshot, drift-report expected output, evidence-ledger expected
  output, or parity snapshot

Committed golden fixtures must not:

- silently redefine parser behavior
- silently bless schema drift
- expose raw local `Player.log` data
- include unreviewed local artifacts
- depend on live workbook state or deployed Apps Script state
- use AI-generated output as parser truth
- imply that current `Player.log` shape is guaranteed by Wizards

### Evidence-Ledger Linkage

When a fixture asserts business-critical parser-managed outputs, future
metadata should identify which evidence-ledger tier(s) it covers:

- Tier 0: evidence and quality metadata
- Tier 1: match identity and lifecycle
- Tier 2: queue, format, rank, and event context
- Tier 3: game-level facts
- Tier 4: sideboarding and deck state
- Tier 5: card identity and gameplay actions
- Tier 6: runtime health and drift detection
- Tier 7: derived analytics outputs

V1 hardening does not require every existing fixture to cover every tier.
Coverage must be explicit so a small Bo1 fixture does not masquerade as full
ledger validation.

### Provenance Metadata

Any new or substantially updated golden fixture after this policy is adopted
must have provenance metadata, either in a future manifest, sidecar, fixture
header, or test-owned declaration.

Required provenance fields:

- `fixture_id`
- `fixture_class`
- `fixture_paths`
- `source_issue`
- `source_contract`
- `related_adrs`
- `source_type`
- `source_privacy_class`
- `redaction_status`
- `redaction_method`
- `redaction_categories`
- `minimum_evidence_preserved`
- `parser_surfaces_under_test`
- `expected_output_paths`
- `evidence_ledger_tiers`
- `value_source_labels_expected`
- `confidence_labels_expected`
- `finality_labels_expected`
- `drift_flags_expected`
- `invariants_expected`
- `update_command`
- `update_approval_required`
- `known_limitations`

Allowed `source_type` values:

- `local_player_log`
- `local_saved_log_slice`
- `synthetic_log_slice`
- `parser_replay_output`
- `schema_snapshot`
- `drift_report`
- `evidence_ledger_output`
- `repo_static_parity`

Allowed `source_privacy_class` values:

- `local_private_raw`
- `sanitized_committable`
- `synthetic_committable`
- `repo_static`

Allowed `redaction_status` values:

- `not_applicable`
- `sanitized`
- `synthetic`
- `legacy_unclassified`
- `requires_review`

Existing fixtures may be marked `legacy_unclassified` by a future manifest
retrofit. That status is a known gap, not proof that the fixture is unsafe.

### Redaction Requirements

Before any local `Player.log` evidence becomes a committed fixture, the
redaction process must remove, replace, or normalize:

- real account IDs
- real display names and screen names
- opponent identities
- access tokens, refresh tokens, API keys, bearer tokens, auth headers, and
  credential material
- webhook URLs
- Apps Script deployment URLs
- spreadsheet IDs
- local absolute paths and user profile names
- machine names or local host details
- deck IDs or user IDs that identify a private account
- private request IDs when they are not needed for parser behavior
- long opaque identifiers unless relationship-preserving placeholders are
  required
- raw chat or free-text content if it ever appears in a log source
- full runtime status, failed-post payloads, bad-event captures, or workbook
  exports

Redaction should preserve:

- event family markers needed by `LineBuffer` and `Router`
- payload paths needed by parser modules
- relationship structure, using stable placeholders when needed
- game, match, team, seat, object, and card IDs only to the degree needed for
  parser behavior
- timestamps only when timing behavior, ordering, or duration is under test
- evidence required for expected parser outputs

Redaction must not:

- alter the behavior being tested
- remove evidence needed to reproduce the parser output
- replace private data with real-looking personal data
- introduce fields that did not exist in the source evidence unless the
  fixture is clearly marked synthetic
- convert an inferred behavior into an observed behavior

### Expected-Output Pairing

Each replay fixture that asserts parser behavior must be paired with one of:

- an expected-output snapshot
- focused assertions with a documented target
- a future evidence-ledger expected-output fixture

Expected outputs must state or make obvious:

- which input fixture they pair with
- which parser surfaces they cover
- which outputs are final, provisional, or live when finality matters
- which outputs are parser-owned truth and which are downstream enrichment
- which metadata labels are expected when evidence-ledger metadata exists

Expected outputs must not include:

- raw private payloads
- unnormalized local paths
- volatile timestamps unrelated to parser behavior
- source paths from local temporary directories
- current drift-report timestamps unless normalized
- generated card data dumps
- workbook exports
- failed post payloads
- secrets or credential-like values

If expected outputs are changed because parser behavior intentionally changed,
the PR must cite the behavior-change issue and contract. Updating expected
outputs alone is not sufficient proof that the new behavior is correct.

### Schema Snapshot Guarantees

Schema snapshots must remain:

- stable
- deterministic
- reviewable
- free of private raw values
- explicit about update approval

Schema snapshots may include:

- event class names
- event `kind` values
- performance class values
- top-level payload key sets
- workbook-facing row keys
- sync field names
- runtime family names
- runtime event types
- runtime scopes
- repo-side Apps Script dispatch/header/key parity

Schema snapshots must not include:

- raw local logs
- raw bytes or raw hashes
- real timestamps, except stable test constants
- local runtime paths
- webhook URLs
- spreadsheet IDs
- deployment IDs
- workbook export contents
- failed posts
- generated card/tier data dumps

### Drift Baseline Guarantees

Future committed drift baselines or expected drift-report outputs must:

- be built only from sanitized or synthetic evidence
- normalize volatile fields such as `analyzed_at`
- avoid committing local `source_path` values
- avoid raw unknown-entry text that contains private data
- show parser evidence drift separately from transport, workbook, deployment,
  local artifact, and AI/analytics drift
- require explicit approval before refresh

This contract does not authorize refreshing
`player_log_drift_baseline.json` or committing runtime drift reports.

### Existing Fixture Compatibility

Existing committed fixtures are not retroactively rejected by this contract.

Compatibility rule:

- Existing fixtures may continue to be used while a future issue decides
  whether to add metadata, rename fixtures, split fixtures, or create a central
  manifest.

Review rule:

- Any substantial update to an existing fixture after this contract must follow
  this policy's redaction, provenance, pairing, update, and validation rules.

## Update And Review Workflow

### Creating A New Golden Fixture

Required workflow:

1. Create or cite a GitHub issue that names the behavior, schema surface, drift
   case, or evidence-ledger tier the fixture will cover.
2. Cite the relevant module contract or create one before fixture work begins.
3. Select the smallest representative raw evidence slice, synthetic slice, or
   repo-static source.
4. Redact or synthesize the fixture.
5. Preserve the minimum evidence needed for the parser behavior under test.
6. Pair the fixture with expected output or focused assertions.
7. Add provenance metadata by the approved future metadata mechanism.
8. Run focused validation.
9. Run protected-surface and secret/local-artifact checks when those tools
   exist.
10. Route to Codex E for review before submitter work.

### Updating A Golden Fixture

Allowed reasons:

- parser behavior changed under an explicit issue and contract
- schema surface changed under an explicit issue and contract
- a fixture contained unnecessary private or volatile material and is being
  redacted without changing behavior
- a fixture was too broad and is being reduced while preserving the behavior
  under test
- evidence-ledger metadata was added under an explicit fixture/ledger issue
- a baseline was refreshed under an explicit drift-report baseline issue

Not allowed:

- updating snapshots just because a test failed
- updating expected output without explaining the semantic change
- treating the update command as approval
- hiding a parser regression by accepting new output
- broadening fixture evidence beyond the issue scope
- adding raw local logs because they are convenient

### Approval Rule

Any update to these fixture classes requires explicit issue, contract, and
review approval:

- `sanitized_player_log_excerpt`
- `parser_expected_output_snapshot`
- `schema_snapshot_fixture`
- `drift_report_expected_output`
- `evidence_ledger_fixture`
- `workbook_or_apps_script_parity_snapshot`

For parser replay fixtures and expected outputs, approval must name whether the
change is:

- behavior-preserving redaction
- behavior-preserving minimization
- authorized parser behavior drift
- authorized schema drift
- authorized evidence-ledger metadata expansion
- authorized drift baseline refresh

### PR Drift Budget

PRs that add, remove, regenerate, or reinterpret fixtures must disclose fixture
drift in the PR drift budget.

Required drift-budget interpretation:

- `No drift`: fixture files are not touched and no expected outputs change.
- `Authorized drift`: fixture or expected output changes are explicitly
  authorized by issue and contract.
- `Residual drift`: fixture coverage, redaction confidence, metadata, or
  validation remains incomplete and is accepted or routed to a follow-up.
- `N/A`: no fixture/evidence surface applies.

## Validation Requirements

### Contract-Writer Validation

Because this Codex B thread creates only a new Markdown file:

```powershell
git diff --check
git diff --no-index --check -- NUL docs\contracts\code_hardening_golden_fixture_policy.md
```

### Future Fixture-Policy Comparison Validation

For a docs-only comparison or metadata-policy implementation:

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "fixture|golden|Player.log|redact|snapshot|drift|ledger" docs\contracts tests\fixtures tests
```

If `tools/check_secret_patterns.py` exists in a future branch:

```powershell
py tools\check_secret_patterns.py --all
```

### Future Fixture Or Snapshot Validation

When parser replay fixtures or expected outputs are touched:

```powershell
py -m pytest -q tests\test_parser_regressions.py
py -m pytest -q tests\test_log_drift_sensor.py
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

When schema snapshots are touched:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_check_protected_surfaces.py
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

When fixture changes could affect parser-owned rows, runtime exports, or
schema surfaces:

```powershell
py -m pytest -q tests\test_parser_regressions.py tests\test_event_schema_snapshots.py tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py
py -m ruff check src tests tools
git diff --check
```

Before Codex F submits a PR that touches fixture data or expected output:

```powershell
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check
```

Interpretation:

- Pyright remains advisory unless a future contract escalates it.
- Full-suite validation is recommended before submitter work when committed
  fixture data or expected output changes because those changes can mask broad
  parser drift.
- If only this contract file changes, runtime parser tests are not required.

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
- secrets, credentials, tokens, API keys, or webhook URLs
- environment variable contracts
- raw local logs
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

Allowed future fixture-policy surfaces, only when separately authorized:

- fixture metadata or manifest docs
- committed sanitized fixtures under `tests/fixtures/`
- committed expected parser-output snapshots under `tests/fixtures/`
- committed schema snapshots under `tests/fixtures/schema_snapshots/`
- focused tests that validate fixture policy, redaction expectations, pairing,
  or deterministic output
- implementation handoff and review artifacts

## Out Of Scope

This issue does not authorize:

- creating fixture files
- adding sanitized fixture data
- sanitizing raw logs
- implementing sanitizer tooling
- implementing the evidence ledger
- implementing drift detector baseline refresh policy
- refreshing or committing drift baselines
- committing local runtime drift reports
- changing parser behavior
- changing parser state final reconciliation
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- changing parser event classes
- changing event `kind` values
- changing parser payload shapes
- changing match identity
- changing game identity
- changing deduplication
- changing secrets or environment variables
- committing raw logs
- changing generated data
- changing runtime status files
- changing failed posts
- changing workbook exports
- opening a PR from the contract writer pass
- targeting `main`
- marking tracker #33 complete

## Error Behavior

If a future fixture contains forbidden private or local material:

- the protected-surface gate should fail if the path is forbidden
- a future secret scanner should fail if content patterns are detected
- Codex E/F/G must stop and route to removal, redaction, or a new contract
- the fixture must not be accepted as a golden reference

If a fixture lacks expected-output pairing:

- tests may still use it for smoke or drift-count assertions, but the fixture
  metadata must name the assertion target
- it must not be described as full parser-output coverage

If a snapshot or expected-output mismatch appears:

- do not auto-update
- inspect whether the diff is parser behavior drift, schema drift, redaction
  drift, test harness drift, or fixture staleness
- require issue/contract/review approval before updating the committed oracle

If a sanitized fixture cannot preserve behavior without private content:

- leave the evidence local and ignored
- use a synthetic structured fixture if possible
- record the fixture gap
- do not commit the raw source

If a future drift report includes local source paths or volatile timestamps:

- normalize or omit those fields before committing expected output
- route back if normalization would change runtime report behavior beyond test
  serialization

## Side Effects

Allowed side effect in this Codex B thread:

- create `docs/contracts/code_hardening_golden_fixture_policy.md`

Forbidden side effects in this Codex B thread:

- no fixture creation
- no raw-log sanitization
- no expected-output updates
- no schema snapshot updates
- no drift baseline refresh
- no parser/runtime/workbook/App Script behavior changes
- no PR creation
- no tracker closure

Future fixture-policy implementation side effects require a separate scoped
issue and contract or an explicit Codex C instruction against this contract.

## Dependency Order

Future fixture work should proceed in this order:

1. Confirm the target branch is `codex/code-hardening-suite`.
2. Confirm source issue and contract authorize fixture work.
3. Inspect `git status` and exclude unrelated files.
4. Classify the fixture by this contract's fixture classes.
5. Identify the parser/evidence-ledger tier(s) and protected surfaces involved.
6. Redact or synthesize evidence before committing anything.
7. Pair replay inputs with expected output or focused assertions.
8. Add provenance metadata by the approved future mechanism.
9. Run focused replay, snapshot, drift, and protected-surface validation.
10. Produce implementation handoff.
11. Route to Codex E for contract-test review.

Stop and route back to Codex B or A if satisfying the fixture goal requires
parser behavior changes, workbook/webhook/App Script changes, raw local log
commitment, live workbook access, deployed Apps Script checks, or baseline
refresh policy not covered by the current issue.

## Compatibility

- Existing committed fixtures remain usable.
- Existing schema snapshot update mode remains opt-in through
  `MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS=1`.
- Existing parser regression expected-output files remain current oracles until
  an explicit issue and review approve changes.
- Existing protected-surface gate behavior remains path-based and allows
  documented fixtures under `tests/fixtures/`.
- The absence of `tools/check_secret_patterns.py` on this branch is an
  observed current-state gap, not a requirement to implement it here.
- `origin/main` evidence-ledger docs may be cited from this branch without
  copying those docs into `codex/code-hardening-suite`.
- `MGTA Start Time` and other existing workbook-facing names remain unchanged.

## Unknowns

- Whether fixture provenance should be stored in one central manifest, sidecar
  files, Markdown tables, Python declarations, or a hybrid.
- Whether existing fixtures should be retrofitted immediately or left as
  legacy fixtures until they are next touched.
- What exact sanitizer tooling should exist, if any.
- Which local logs should become the first approved golden corpus.
- Whether drift-report expected outputs should live under `tests/fixtures/` or
  a dedicated drift-baseline fixture folder.
- Whether committed drift baselines should be full JSON reports, reduced
  semantic snapshots, or focused expected assertions.
- Whether evidence-ledger fixtures should be authored before or after the
  machine-readable ledger implementation exists.
- How much timestamp normalization is acceptable for replay fixtures where
  ordering and durations matter.
- Whether a future content scanner should become required CI before new
  evidence-derived fixtures are allowed.

## Suspected Gaps

- No unified fixture provenance manifest or sidecar metadata currently exists.
- Existing parser regression fixtures are labeled sanitized in comments, but
  there is no machine-readable redaction metadata.
- Existing expected parser-output snapshots do not include evidence-ledger
  value-source, confidence, finality, drift, or invariant metadata because the
  ledger is not implemented.
- Existing schema snapshots have a strong update policy but are not connected
  to a general fixture policy document until this contract.
- Existing drift sensor tests assert selected behavior, but no full committed
  drift-report expected-output fixture exists.
- `log_drift_sensor.py` writes local reports and baselines under runtime status
  paths; this is appropriate for runtime but not yet governed by a committed
  baseline refresh policy.
- `tools/check_secret_patterns.py` is absent on the current branch, so fixture
  privacy currently depends on path gates, focused test guards, review, and
  manual inspection rather than a content scanner.
- The protected-surface gate intentionally allows `tests/fixtures/*.log` by
  path, so fixture redaction must be handled by policy, review, future content
  checks, and fixture-specific tests.
- No evidence-ledger fixture class currently validates Tier 0-7 metadata.

## Acceptance Criteria

- `docs/contracts/code_hardening_golden_fixture_policy.md` exists.
- The contract links issue #68, tracker #33, and evidence-ledger context.
- The contract names Code Hardening fixture governance as the owning layer.
- The contract preserves parser/state truth ownership.
- The contract distinguishes observed current behavior from required
  guarantees.
- The contract defines fixture classes.
- The contract defines provenance metadata requirements.
- The contract defines redaction requirements.
- The contract defines expected-output pairing requirements.
- The contract defines schema snapshot and drift baseline boundaries.
- The contract defines update and review workflow.
- The contract defines validation expectations.
- The contract names protected surfaces and out-of-scope behavior.
- The contract records unknowns and suspected gaps.
- The contract does not create fixtures, add fixture data, sanitize logs,
  implement tooling, implement the evidence ledger, refresh baselines, change
  parser behavior, or target `main`.
- The contract routes next work to Codex C: Module Implementer / comparison
  thread.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/68

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Related ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Contract produced:
`docs/contracts/code_hardening_golden_fixture_policy.md`

Risk tier: Medium for documentation and fixture governance. Escalate to High if
implementation creates fixture data from local logs, changes parser behavior,
changes schema, refreshes committed baselines, or touches protected runtime
surfaces.

Owning truth layer: Code Hardening fixture governance; parser/state remains
truth owner for interpretation and normalized match/game facts.

Public interface:

- fixture class vocabulary
- provenance metadata requirements
- redaction requirements
- expected-output pairing rules
- update/review workflow
- validation expectations

Invariants:

- Committed fixtures must be sanitized or synthetic.
- Fixture updates require explicit issue, contract, and review approval.
- Replay inputs must pair with expected parser output or focused assertions.
- Schema snapshots and expected outputs must not be auto-updated after a test
  failure.
- Local private `Player.log` may inform local review, but raw logs must not be
  committed.
- Parser truth remains parser/state owned.
- Drift reports must distinguish parser evidence drift from transport,
  workbook, deployment, local artifact, and AI/analytics drift.

Required tests and validation: listed above.

Acceptance criteria: listed above.

Open questions or contract risks:

- Manifest vs sidecar vs Markdown metadata storage remains undecided.
- Existing fixtures are legacy and not yet machine-classified.
- Content secret scanning is absent on this branch.
- Drift-report baseline refresh policy is explicitly out of scope.
- Evidence-ledger implementation is absent; fixture metadata should be ready
  for it without pretending it already exists.

Next recommended thread role: Codex C: Module Implementer / comparison thread.

Pasteable next-thread prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for the Code Hardening child issue: Golden fixture policy linked to the evidence ledger.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/68

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- origin/main:docs/problem_representations/player_log_evidence_ledger.md
- origin/main:docs/contracts/player_log_evidence_ledger.md
- tests/test_parser_regressions.py
- tests/test_event_schema_snapshots.py
- tests/test_log_drift_sensor.py
- tests/test_check_protected_surfaces.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- tools/check_protected_surfaces.py
- tests/fixtures/

Goal:
Compare the current fixture, snapshot, drift sensor, and protected-surface behavior against docs/contracts/code_hardening_golden_fixture_policy.md. Produce docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md. Keep the pass comparison/docs-focused unless the user explicitly authorizes a concrete implementation.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Inspect git status and exclude unrelated changes.
- State what golden fixtures are supposed to do, what current fixtures/snapshots already do, what policy gaps remain, and the exact minimal comparison or implementation plan.

Do:
- Compare existing parser replay fixtures, expected outputs, schema snapshots, drift sensor tests, and protected-surface gate behavior against the contract.
- Identify which fixture classes already exist, which are missing, and which are legacy/unclassified.
- Identify current redaction, provenance, expected-output pairing, update-policy, validation, and protected-surface coverage.
- Produce docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md with contract matches, gaps, files inspected, validation, protected-surface status, remaining risks, and next recommended role.
- If the user explicitly authorizes implementation in this thread, keep it docs/test-policy narrow and do not create fixture data unless separately approved.

Do not:
- Create fixture files.
- Add sanitized fixture data.
- Sanitize raw logs.
- Implement sanitizer tooling.
- Implement the evidence ledger.
- Implement drift detector baseline refresh policy.
- Refresh or commit drift baselines.
- Modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
py -m pytest -q tests\test_parser_regressions.py tests\test_event_schema_snapshots.py tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/68"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_golden_fixture_policy.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "git diff --no-index --check -- NUL docs\\contracts\\code_hardening_golden_fixture_policy.md"
  stop_conditions:
    - "Do not create fixture files or add sanitized fixture data."
    - "Do not sanitize raw logs or implement sanitizer tooling."
    - "Do not implement the evidence ledger."
    - "Do not implement drift detector baseline refresh policy."
    - "Do not refresh or commit drift baselines."
    - "Do not modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
