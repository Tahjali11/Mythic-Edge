# Player.log Evidence Ledger Schema Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/128

## Parent Issue

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Completed Support Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

## Role Performed

Codex C: Module Implementer.

## Source Artifact

`docs/contracts/player_log_evidence_ledger_schema.md`

## Worktree Note

The active integration checkout was stale and had unrelated untracked module
files. Codex C created a clean sibling worktree on a feature branch:

`codex/player-log-evidence-ledger-schema`

The branch starts from `origin/codex/parser-reliability-intelligence` at
`066b55f`, the #127 draft fixture coverage merge commit. The Codex B contract
artifact existed only as an untracked local file in the stale integration
checkout, so Codex C copied that contract into this clean worktree as the
source artifact for issue #128.

## Summary Of Implementation Comparison

The current branch had the supporting parser-reliability stack from tracker
#47, including diagnostics, golden replay, feature-equity corpus ratchet, drift
sensor, DraftBot, DraftHuman, DraftComplete, and synthetic draft fixture
coverage.

The contract mismatch was the intended issue #128 gap:

- no parser-local evidence ledger module;
- no stable machine-readable ledger schema object;
- no vocabulary constants or validators;
- no seed output-family registry;
- no complete Tier 1 `match_id` / `MTGA Match ID` sample;
- no focused tests for schema loading, validation, serialization,
  determinism, copy safety, and privacy boundaries.

Codex C implemented the smallest contract-approved slice: schema/vocabulary,
seven family registrations, one complete Tier 1 `match_id` seed entry, field
evidence validation helpers, and focused tests.

## Confirmed Matches

- Parser behavior was not changed.
- Parser state final reconciliation was not changed.
- Parser event classes were not changed.
- Match/game identity behavior was not changed.
- Diagnostics, golden replay, feature-equity corpus ratchet, state, models,
  sheet schema, router, parser modules, workbook, webhook, and Apps Script
  behavior were not changed.
- `docs/contracts/player_log_evidence_ledger.md` remains the broad #11
  contract.
- `docs/decisions/ADR-0003-player-log-drift-policy.md` remains accepted ADR
  authority for Player.log drift/privacy posture.
- Issue #128 stays scoped to `evidence_ledger.py` plus focused tests and
  handoff only.

## Contract Mismatches Found And Fixed

- Missing `src/mythic_edge_parser/app/evidence_ledger.py`.
  - Fixed with a pure, side-effect-free module.
- Missing required ledger constants and vocabulary constants.
  - Fixed with stable constants from the #128 contract.
- Missing deterministic ledger builder.
  - Fixed with `build_player_log_evidence_ledger()`.
- Missing copy-safe entry iterator.
  - Fixed with `iter_ledger_entries()`.
- Missing ledger and entry validators.
  - Fixed with `validate_player_log_evidence_ledger()` and
    `validate_ledger_entry()`.
- Missing field-evidence schema validation.
  - Added `FIELD_EVIDENCE_OBJECT`, `FIELD_EVIDENCE_SCHEMA_VERSION`, and
    `validate_field_evidence()` so future reports can validate the shape
    without attaching it to runtime rows.
- Missing seven-family seed registry.
  - Fixed with one `seeded_sample` Tier 1 family and six `registered_future`
    families.
- Missing complete `tier1.match_identity.match_id` entry.
  - Fixed with the required direct and fallback evidence signals, policies,
    invariants, degradation behavior, review modules, tests, and fixture refs.
- Missing focused tests.
  - Fixed with `tests/test_evidence_ledger.py`.

## Safeguards Added

- Builders are deterministic and include no timestamps.
- Builders do not read files, environment variables, Git state, logs, runtime
  status, external services, workbooks, webhooks, or Apps Script.
- Validators return stable error strings instead of raising for malformed
  caller payloads.
- Validators report missing required fields, duplicate IDs, unknown vocabulary
  labels, absolute paths, and raw-log-like or secret-like text.
- `iter_ledger_entries()` returns copy-safe data so caller mutation does not
  mutate the module registry.
- Ledger privacy metadata states raw private logs and raw payload values are
  not included.
- The seed entry uses path strings and symbolic surfaces only; it does not
  include raw `Player.log` values or examples.

## Finality Vocabulary Note For Reviewer

ADR-0003 lists `live`, `provisional`, and `reconciled` as required finality
labels. The broader #11 ledger contract and the issue #128 contract also use
`final`, and issue #128 explicitly requires `FINALITY_LABELS` to include
`final`.

Codex C implemented `("live", "provisional", "final", "reconciled")` because
the issue #128 contract uses `final` in the ledger-entry and field-evidence
schemas. Please have Codex E verify whether this is acceptable as an
issue-scoped decomposition of the broad #11 contract or whether Codex B should
clarify the ADR/contract vocabulary relationship.

## Files Changed

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md`

## Public Interface Added

Module:

- `src/mythic_edge_parser/app/evidence_ledger.py`

Constants:

- `LEDGER_OBJECT`
- `LEDGER_SCHEMA_VERSION`
- `LEDGER_VERSION`
- `FIELD_EVIDENCE_OBJECT`
- `FIELD_EVIDENCE_SCHEMA_VERSION`
- `VALUE_SOURCES`
- `CONFIDENCE_LEVELS`
- `FINALITY_LABELS`
- `INVARIANT_STATUSES`
- `DRIFT_FLAGS`

Functions:

- `build_player_log_evidence_ledger()`
- `iter_ledger_entries()`
- `validate_player_log_evidence_ledger(payload=None)`
- `validate_ledger_entry(entry)`
- `validate_field_evidence(payload)`

No CLI was added.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
# 15 passed

python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
# 14 passed

python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
# 20 passed

python3 -m pytest -q tests
# 874 passed

python3 -m ruff check src tests tools
# All checks passed.

git diff --check
# passed

git diff --no-index --check /dev/null docs/contracts/player_log_evidence_ledger_schema.md
# no whitespace output; exit 1 expected because /dev/null differs from the file

LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/player_log_evidence_ledger_schema.md
# no matches

printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Protected Surface Gate: passed; forbidden: 0; warnings: 0

rg <forbidden secret/private marker patterns> docs/contracts/player_log_evidence_ledger_schema.md src/mythic_edge_parser/app/evidence_ledger.py tests/test_evidence_ledger.py
# no matches
```

`tools/check_secret_patterns.py` is not present on this branch, so Codex C used
a focused `rg` private-marker scan over the changed files.

## Still-Unverified Layers

- GitHub CI was not run.
- Runtime field-evidence attachment was intentionally not implemented.
- Schema snapshots, drift reports, invariant execution, automatic issue
  creation, diagnostics report-shape changes, golden replay manifest-shape
  changes, and feature-equity ratchet behavior changes were intentionally not
  implemented.
- Full Tier 1-3 and Tier 4-7 ledger mapping remains future work under issue
  #11 or later child issues.
- Live private `Player.log` files and local diagnostics artifacts were not
  read, copied, summarized, or committed.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

## Pasteable Next-Thread Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #128:
  https://github.com/Tahjali11/Mythic-Edge/issues/128

  Parent issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/11

  Completed support tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/47

  Branch:
  codex/parser-reliability-intelligence

  Use:
    - docs/contracts/player_log_evidence_ledger_schema.md
    - docs/contracts/player_log_evidence_ledger.md
    - docs/decisions/ADR-0003-player-log-drift-policy.md
    - docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/parsers/match_state.py
    - src/mythic_edge_parser/parsers/gre/game_state.py
    - src/mythic_edge_parser/parsers/gre/game_result.py
    - tests/test_log_drift_sensor.py
    - tests/test_parser_diagnostics_mode.py
    - tests/test_golden_replay_harness.py
    - tests/test_feature_equity_corpus_ratchet.py

  Goal:
    Verify the issue #128 implementation against the Player.log evidence ledger
    schema contract.

  Confirm:
    - evidence_ledger.py is pure parser-provenance metadata and has no filesystem, network, environment, GitHub, workbook, webhook, Apps Script, runtime-status, local-log, or model-provider side effects.
    - Required constants and vocabulary are present.
    - build_player_log_evidence_ledger() returns deterministic JSON-serializable data with no generated timestamps or local/private values.
    - iter_ledger_entries() is copy-safe.
    - The ledger includes the seven required output-family registrations.
    - Only match_identity_and_lifecycle is seeded_sample in issue #128.
    - Exactly one complete entry exists: tier1.match_identity.match_id.
    - The seed entry includes required direct evidence signals and parser-context fallback signal.
    - Validators return stable errors without raising for malformed caller payloads.
    - Validators detect missing fields, unknown value-source labels, unknown confidence labels, unknown finality labels, unknown drift flags, duplicate entry IDs, duplicate signal IDs, absolute paths, and raw-log-like/private text.
    - Field-evidence validation remains schema-only and does not attach metadata to runtime rows.
    - No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, runtime status schema, failed posts, workbook exports, generated data, secrets, environment variable contracts, production behavior, or AI/analytics truth changed.

  Reviewer attention:
    - ADR-0003 lists finality labels live/provisional/reconciled, while the broad #11 contract and issue #128 contract also require final. Codex C implemented final because issue #128 explicitly requires it. Decide whether this is acceptable or requires Codex B clarification.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
    - python3 -m pytest -q tests
    - python3 -m ruff check src tests tools
    - git diff --check
    - git diff --no-index --check /dev/null docs/contracts/player_log_evidence_ledger_schema.md
    - LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/player_log_evidence_ledger_schema.md
    - printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

  Output:
    - Findings first, if any.
    - Contract-test verdict.
    - Validation results.
    - Remaining non-blocking gaps.
    - Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
    - workflow_handoff block.

  Do not target main directly.
  Do not close issue #11.
  Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.
  Do not implement schema snapshots, drift reports, invariant execution, runtime row field-evidence attachment, or automatic GitHub issue creation.
  Do not read, copy, summarize, or commit raw private Player.log excerpts or local diagnostics artifacts.
  Do not stage, commit, merge, or push unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_schema.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md"
  verdict: "ready_for_module_review"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-schema"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "git diff --no-index --check /dev/null docs/contracts/player_log_evidence_ledger_schema.md"
    - "LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/player_log_evidence_ledger_schema.md"
    - "printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not implement schema snapshots, drift reports, invariant execution, runtime row field-evidence attachment, or automatic GitHub issue creation."
    - "Do not read, copy, summarize, or commit raw private Player.log excerpts or local diagnostics artifacts."
```
