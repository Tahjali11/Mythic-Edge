# Player.log Evidence Ledger Tier 5 Opponent-Card-Observation Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/166

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Status

- Branch: `codex/parser-reliability-intelligence`
- Starting status: branch matched `origin/codex/parser-reliability-intelligence`; the issue #166 contract existed as an untracked source artifact.
- Ending status: modified implementation/test/handoff files plus the untracked issue #166 contract source artifact.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `docs/contract_test_reports/player_log_evidence_ledger_tier5_gameplay_action.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_evidence_ledger.py`
- GitHub issue #166

## Current Behavior Compared To Contract

Before this pass, Tier 5 `card_identity_and_gameplay_actions` already had status `seeded_sample`, owner modules for gameplay actions and opponent observations, and seed fields `["grp_id", "gameplay_action"]`. It still listed `opponent_card_observation` under `future_fields`.

Existing Tier 5 ledger entries were:

- `tier5.card_identity.grp_id`
- `tier5.gameplay_action.gameplay_action`

No entry existed for `tier5.opponent_card_observation.*`. Existing tests also preserved the old future-field expectation and did not directly assert the exact one-entry set for `tier5.gameplay_action.*`, matching the non-blocking #165 P3 review note.

The parser behavior side already existed in `opponent_card_observations.py` and focused tests. It returns observations only for supported opponent-visible action entries and suppresses hidden draw observations. This pass did not change that behavior.

## Implementation Option Chosen

Implemented the smallest metadata/test-only change authorized by the contract:

- Move `opponent_card_observation` from Tier 5 future field to current seed field.
- Add exactly one broad opponent-card-observation ledger entry.
- Harden Tier 5 tests around exact `tier5.gameplay_action.*` and `tier5.opponent_card_observation.*` entry IDs.
- Keep parser/runtime/workbook/webhook/App Script behavior untouched.

## Files Changed

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md`

Source artifact present but not edited by this thread:

- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`

## Exact Sections Changed

### `src/mythic_edge_parser/app/evidence_ledger.py`

- Updated Tier 5 `card_identity_and_gameplay_actions` family:
  - `seed_fields` is now exactly `["grp_id", "gameplay_action", "opponent_card_observation"]`.
  - `future_fields` is now exactly `[]`.
  - Family notes now cite issues #163, #165, and #166 as the current Tier 5 seed mappings.
- Updated `grp_id` and `gameplay_action` notes/invariants from deferred opponent-observation language to issue #166 mapped-boundary language.
- Added `_OPPONENT_CARD_OBSERVATION_ENTRY` with:
  - direct evidence for visible action, visibility, actor-seat, card-identity, and status context;
  - fallback evidence for reveal annotations, public-zone presence, derived zone transitions, gameplay-action dependency, `grp_id` dependency, name/display enrichment, and degraded/conflicting status;
  - value-source, confidence, finality, invariant, degradation, drift, privacy, and downstream boundary metadata;
  - path-only privacy posture and no raw payload values.
- Added the new entry to `_LEDGER_ENTRIES`.

### `tests/test_evidence_ledger.py`

- Updated contracted Tier 5 fields and entries for issue #166.
- Updated Tier 5 future-field expectations to empty.
- Removed `opponent_card_observation` from prior forbidden seed-field sets where it is now contract-authorized.
- Added an opponent-observation facet forbidden set to prevent accidental separate seed fields for observation facets, hidden cards, decklists, sideboard deltas, archetypes, advice, Line Tracer, AI, or model-provider truth.
- Added exact-entry assertions for:
  - `tier5.gameplay_action.* == {"tier5.gameplay_action.gameplay_action"}`
  - `tier5.opponent_card_observation.* == {"tier5.opponent_card_observation.opponent_card_observation"}`
- Added focused tests for opponent-card-observation evidence sources, fallback/degradation paths, value-source/confidence/finality boundaries, drift flags, and protected non-truth boundaries.

## Code Changed

Runtime parser behavior did not change. The only source code change is static evidence-ledger metadata in `src/mythic_edge_parser/app/evidence_ledger.py`.

## Tests Changed

Focused ledger tests changed in `tests/test_evidence_ledger.py`.

No opponent-card-observation parser tests were edited.

## Interface Changes

No parser interface, runtime payload, workbook schema, webhook payload, Apps Script behavior, parser event class, match identity, game identity, deduplication, fixture, snapshot, drift baseline, or production interface changed.

The evidence-ledger metadata interface now includes:

- Tier 5 seed field: `opponent_card_observation`
- Entry ID: `tier5.opponent_card_observation.opponent_card_observation`

## Validation Run

- `py -m pytest -q tests\test_evidence_ledger.py` -> `83 passed`
- `py -m pytest -q tests\test_opponent_card_observations.py` -> `10 passed`
- `py -m ruff check src tests tools` -> `All checks passed!`
- `git diff --check` -> passed with no output
- Path-scoped protected-surface check for the touched file set -> `forbidden: 0`, `warnings: 0`, `result: passed`

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/App Script/production surfaces were intentionally touched. The diff is limited to evidence-ledger metadata, focused ledger tests, and this handoff.

## What Remains Unverified

- GitHub Actions were not run.
- Live workbook state was not checked.
- Deployed Apps Script state was not checked.
- Production behavior was not checked.
- Runtime action artifact generation was not checked.
- Future analytics consumption of opponent observations remains out of scope.

## Reviewer Focus

Codex E should verify:

- Tier 5 seed/future fields exactly match the #166 contract.
- The new opponent-observation entry documents required direct, fallback, dependency, enrichment, finality, drift, degradation, and privacy boundaries.
- Tests directly enforce exact `tier5.gameplay_action.*` and `tier5.opponent_card_observation.*` entry sets.
- The change does not alter opponent-card-observation parser behavior or promote analytics/AI/model-provider output into truth.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #166.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/166

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md

Implementation handoff:
docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md

Changed files expected:
- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md

Task:
Review the implementation against the #166 contract. Lead with findings ordered by severity. Verify that Codex C seeded `opponent_card_observation` as exactly one Tier 5 evidence-ledger field, added the required metadata/tests, and did not change parser behavior.

Check especially:
- Tier 5 seed_fields is exactly `["grp_id", "gameplay_action", "opponent_card_observation"]`.
- Tier 5 future_fields is exactly `[]`.
- The only `tier5.opponent_card_observation.*` entry is `tier5.opponent_card_observation.opponent_card_observation`.
- The only `tier5.gameplay_action.*` entry remains `tier5.gameplay_action.gameplay_action`.
- The new entry documents visible action, visibility, actor-seat, card identity, status, dependencies, enrichment, value-source, confidence, finality, invariants, degradation, drift, and path-only privacy boundaries.
- No separate seed fields were added for observation facets, hidden cards, complete decklists, sideboard deltas, archetypes, gameplay advice, Line Tracer, AI, or model-provider truth.
- No parser behavior, gameplay-action behavior, opponent-card-observation behavior, workbook schema, webhook payload shape, Apps Script behavior, runtime artifact shape, fixtures, snapshots, drift baselines, secrets, raw logs, generated data, production behavior, analytics truth, AI truth, or model-provider behavior changed.

Suggested validation:
py -m pytest -q tests\test_evidence_ledger.py
py -m pytest -q tests\test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin

Do not edit code in the review thread. Do not stage, commit, push, open a PR, merge, target main, close issue #166, or close tracker #11 unless explicitly asked.

Final output must include:
- role performed
- issue/tracker
- contract and handoff reviewed
- findings first
- contract matches
- contract mismatches
- missing tests or safeguards
- validation run and result
- protected-surface status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/166"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/parser-reliability-intelligence"
  files_changed:
    - "src/mythic_edge_parser/app/evidence_ledger.py"
    - "tests/test_evidence_ledger.py"
    - "docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md"
  source_artifact_present:
    - "docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md"
  validation:
    - "py -m pytest -q tests\\test_evidence_ledger.py -> 83 passed"
    - "py -m pytest -q tests\\test_opponent_card_observations.py -> 10 passed"
    - "py -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0, result passed"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not change gameplay-action behavior."
    - "Do not change opponent-card-observation behavior or payload shape."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, production behavior, analytics truth, AI truth, model-provider behavior, secrets, raw logs, generated data, runtime artifacts, fixtures, snapshots, or drift baselines."
    - "Do not target main."
    - "Do not close tracker #11."
```
