# Player.log Evidence Ledger Schema Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/128

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

Completed support tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

## Contract

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`

## Implementation Under Test

Implementation branch:
`codex/player-log-evidence-ledger-schema`

Integration target:
`codex/parser-reliability-intelligence`

Local worktree:
`/Users/tahjblow/Documents/New project/Mythic-Edge-issue-128`

Implementation handoff:
`docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md`

Changed and untracked files under review:

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/implementation_handoffs/player_log_evidence_ledger_schema_comparison.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`

## Findings

No blocking findings.

### Resolved Prior Finding

The prior finality-vocabulary blocker is resolved by Codex B's contract
clarification.

Evidence:

- `docs/contracts/player_log_evidence_ledger_schema.md:76` now limits
  ADR-0003 precedence to value-source labels, confidence labels, drift flags,
  invariant-status labels, and privacy posture.
- `docs/contracts/player_log_evidence_ledger_schema.md:80` explicitly carves
  out finality vocabulary as an issue #128 clarification.
- `docs/contracts/player_log_evidence_ledger_schema.md:114` records the
  resolution: preserve ADR-0003 labels and intentionally add `final` as a
  schema-level label.
- `docs/contracts/player_log_evidence_ledger_schema.md:122` requires
  `FINALITY_LABELS` to be exactly
  `("live", "provisional", "final", "reconciled")`.
- `src/mythic_edge_parser/app/evidence_ledger.py:31` implements that tuple.
- `tests/test_evidence_ledger.py:21` asserts that exact tuple.

## Contract-Test Verdict

Pass. The clarified contract intentionally includes `final` in
`FINALITY_LABELS` as a schema-level label while preserving the ADR-0003 labels.
The existing implementation and tests satisfy the clarified contract. Issue
#128 is ready for Codex F: Module Submitter.

## Confirmed Contract Matches

- `src/mythic_edge_parser/app/evidence_ledger.py` exists and is a pure
  parser-provenance metadata module.
- The module imports no project runtime surfaces and performs no filesystem,
  network, environment, GitHub, workbook, webhook, Apps Script, runtime-status,
  local-log, or model-provider side effects on import.
- Required constants and vocabulary constants are present.
- `build_player_log_evidence_ledger()` returns deterministic,
  JSON-serializable dictionaries with no generated timestamp.
- `iter_ledger_entries()` is copy-safe.
- The ledger contains the seven required output-family registrations.
- Only `match_identity_and_lifecycle` has `seeded_sample` status.
- Exactly one complete ledger entry exists:
  `tier1.match_identity.match_id`.
- The seed entry includes the three required direct evidence signals:
  `match_state.match_id`, `game_state.identity.match_id`, and
  `game_result.identity.match_id`.
- The seed entry includes the required parser-context fallback signal:
  `parser_context.current_match_id`.
- Validators return stable error codes without raising for malformed caller
  payloads.
- Validators detect missing fields, unknown value-source labels, unknown
  confidence labels, unknown finality labels, unknown drift flags, duplicate
  entry IDs, duplicate signal IDs, absolute paths, and raw-log-like/private
  text.
- Field-evidence validation remains schema-only and does not attach metadata to
  runtime rows.
- The issue #128 diff does not change parser behavior, parser state final
  reconciliation, parser event classes, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, runtime status
  schema, failed posts, workbook exports, generated data, secrets, environment
  variable contracts, production behavior, or AI/analytics truth.

## Contract Mismatches

None.

## Missing Tests

No blocking implementation test gap was found.

The existing vocabulary test asserts the clarified issue #128 contract,
including all ADR-0003 finality labels plus the schema-level `final` label.

## Drift Notes

- Contract drift: the previous finality-vocabulary ambiguity has been clarified
  in the issue #128 contract. ADR-0003 still has narrower wording, but the
  clarified contract explicitly preserves ADR-0003 labels and scopes `final` as
  an issue #128 schema-level label. A future ADR cleanup may align wording, but
  it is not blocking this package.
- Branch/worktree drift: the implementation branch is checked out locally and
  tracks `origin/codex/parser-reliability-intelligence`; files are still
  untracked because this is a pre-submit local implementation package.
- Branch-scope protected-surface warnings appear when checking the whole branch
  against `origin/main`. Those warnings come from prior parser-reliability
  modules already on the integration branch, not the issue #128 changed-file
  set.
- No workbook, deployment, local-data, PR lifecycle, or tracker lifecycle drift
  was observed in the issue #128 changed-file set.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
# 15 passed in 0.03s

python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py
# 14 passed in 0.04s

python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
# 20 passed in 0.16s

python3 -m pytest -q tests
# 874 passed in 1.10s

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed

git diff --no-index --check /dev/null docs/contracts/player_log_evidence_ledger_schema.md
# passed as whitespace check; diff exit code 1 normalized because /dev/null differs from the file

LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/player_log_evidence_ledger_schema.md
# no matches

printf '<issue #128 changed paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Protected Surface Gate: passed; forbidden: 0; warnings: 0

python3 tools/check_protected_surfaces.py --base origin/main
# Protected Surface Gate: passed; forbidden: 0; warnings: 12 branch-scope inherited parser-reliability warnings

# Codex E re-review after Codex B clarification:
python3 -m pytest -q tests/test_evidence_ledger.py
# 15 passed in 0.03s

python3 -m ruff check src/mythic_edge_parser/app/evidence_ledger.py tests/test_evidence_ledger.py
# All checks passed!

git diff --check
# passed

printf '<clarification re-review paths>' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Protected Surface Gate: passed; forbidden: 0; warnings: 0
```

`tools/check_secret_patterns.py` is not present on this branch. A focused `rg`
scan over the issue #128 changed paths found only intentional forbidden-marker
test needles in `tests/test_evidence_ledger.py`; no live secret, webhook,
workbook, local-path, runtime-status, failed-post, generated-data, or private
Player.log content was found in the ledger payload.

## Protected-Surface Review

The issue #128 changed-file set is limited to a contract, implementation
handoff, a new parser-provenance metadata module, focused tests, and this
contract-test report. No parser/runtime/workbook/webhook/App Script behavior
files changed.

## Remaining Non-Blocking Gaps

- Runtime field-evidence attachment was intentionally not implemented.
- Schema snapshots, drift reports, invariant execution, automatic issue
  creation, diagnostics report-shape changes, golden replay manifest-shape
  changes, and feature-equity ratchet behavior changes remain future work.
- Full Tier 1-3 and Tier 4-7 ledger mapping remains future work under issue
  #11 or later child issues.
- GitHub CI was not run by this reviewer.

## Recommendation

Approve for the next workflow role.

Next role: Codex F: Module Submitter.

Codex F should stage only the issue #128 reviewed files and target
`codex/parser-reliability-intelligence`, not `main`.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_schema.md"
  target_artifact: "Codex F Module Submitter package for issue #128"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-schema"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 15 passed"
    - "python3 -m pytest -q tests/test_log_drift_sensor.py tests/test_parser_diagnostics_mode.py -> 14 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py -> 20 passed"
    - "python3 -m pytest -q tests -> 874 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "git diff --no-index --check /dev/null docs/contracts/player_log_evidence_ledger_schema.md -> whitespace clean"
    - "LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/player_log_evidence_ledger_schema.md -> no matches"
    - "path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
    - "Codex E re-review: python3 -m pytest -q tests/test_evidence_ledger.py -> 15 passed"
    - "Codex E re-review: python3 -m ruff check src/mythic_edge_parser/app/evidence_ledger.py tests/test_evidence_ledger.py -> passed"
    - "Codex E re-review: git diff --check -> passed"
    - "Codex E re-review: path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not implement schema snapshots, drift reports, invariant execution, runtime row field-evidence attachment, or automatic GitHub issue creation."
    - "Do not read, copy, summarize, or commit raw private Player.log excerpts or local diagnostics artifacts."
```
