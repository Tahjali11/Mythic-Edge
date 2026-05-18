# Parser Opponent Card Observations Implementation Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/50

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/48

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/111

Previous merge commit: `76b63622494b0bbc6150e6bd19973b4ac8e0be0c`

Branch: `codex/parser-reliability-intelligence`

Source artifact: `docs/contracts/parser_opponent_card_observations.md`

Role performed: Codex C: Module Implementer

Risk tier: High

## Summary

Implemented a pure, deterministic opponent-card observation helper for
parser-supported opponent-visible gameplay action facts. The helper consumes
action-entry dictionaries, emits JSON-serializable observation payloads, and
keeps archetype, decklist, hidden-information, workbook, webhook, Apps Script,
AI, and analytics inference out of parser truth.

No parser state final reconciliation, workbook schema, webhook payload shape,
Apps Script behavior, output transport, parser event classes, match/game
identity, deduplication, secrets, environment variables, raw logs, generated
data, runtime status files, failed posts, or workbook exports were changed.

## Confirmed Matches

- `gameplay_actions.py` already records deterministic action-entry material
  from `GameState` events: match/game context, turn, action type, instance and
  GRP IDs, actor relation, zones, raw action types, annotation types, and
  catalog-enriched display fields.
- `grp_id_catalog.py` remains enrichment only; the new helper does not import
  or write generated catalog artifacts.
- `card_performance.py` already filters action entries to blank/local actor
  relation before aggregation, and the new focused test now freezes that
  opponent-exclusion behavior.
- `golden_replay.py` and diagnostics mode remain unchanged.
- Existing golden replay manifests remain compatible because no required
  opponent-observation manifest section was added.

## Contract Mismatches Fixed

- Added the missing dedicated module:
  `src/mythic_edge_parser/app/opponent_card_observations.py`.
- Added the missing focused tests:
  `tests/test_opponent_card_observations.py`.
- Added focused card-performance coverage proving opponent action entries do
  not enter local card-performance aggregation.

## Implementation Details

The new helper exposes the contracted v1 public behavior:

- `OPPONENT_CARD_OBSERVATION_OBJECT`
- `OPPONENT_CARD_OBSERVATIONS_OBJECT`
- `SCHEMA_VERSION`
- `build_opponent_card_observation(action_entry)`
- `build_opponent_card_observations_payload(action_entries, *, match_id="")`

The helper:

- returns `None` for non-opponent entries, unsupported action types, hidden
  draws, and non-mapping inputs;
- emits only `actor_relation="opponent"` observations;
- preserves `grp_id`, `observed_grp_id`, `overlay_grp_id`,
  `object_source_grp_id`, `parent_id`, and `identity_hint_source`;
- preserves card-name/display-name enrichment separately from observed IDs;
- maps catalog-specific statuses such as `exact_numeric_match` into normalized
  observation statuses while preserving source context through
  `name_resolution_source`;
- reports missing seat mapping as degraded/review-required instead of guessing
  local or actor seat IDs;
- reports missing card identity, contradictory seat evidence, contradicted
  name resolution, candidate/ambiguous/name-only resolution, and data-loss
  evidence through `degradation_flags`;
- uses evidence-ledger vocabulary for `evidence_status`, `value_source`, and
  `confidence`;
- performs no filesystem writes and imports no workbook, webhook, Apps Script,
  OpenAI, model-provider, diagnostics, golden replay, or output transport
  surfaces.

## Tests Added Or Updated

Added `tests/test_opponent_card_observations.py` coverage for:

- full clean opponent-visible spell observation payload shape;
- input immutability;
- actor seat derivation from `raw_action_types`;
- preservation of canonical and observed ID fields when they differ;
- non-opponent and non-mapping neutral behavior;
- missing seat mapping degraded/review behavior;
- hidden draw from library to hand producing no clean observation;
- missing card identity degraded/review behavior without guessing;
- candidate and contradicted names staying lower-confidence enrichment;
- contradictory actor/action seat evidence producing conflict;
- unresolved known ID preserving ID with placeholder display text;
- collection payload counts, degraded counts, and review status.

Updated `tests/test_card_performance.py` to include an opponent action entry
and assert it remains excluded from card-performance aggregation.

## Interface Changes

New local parser-intelligence helper interface only:

- `src/mythic_edge_parser/app/opponent_card_observations.py`

No workbook columns, webhook fields, Apps Script behavior, runtime status
schema, parser event classes, environment variables, CLI entrypoints, or
production output transport were added or changed.

No `gameplay_actions.py` runtime action JSON/Markdown shape was changed. The
helper can consume action-entry dictionaries that preserve seat fields, and it
degrades rather than guesses when those fields are absent.

## Golden Replay Decision

No golden replay fixture or manifest was added in this pass. Focused unit tests
cover the v1 helper boundaries, and adding a golden replay fixture would have
required broader fixture construction without changing the helper behavior.
Existing golden replay validation was run to confirm compatibility.

## Validation Evidence

Commands run:

```bash
python3 -m pytest -q tests/test_opponent_card_observations.py
```

Result: `10 passed`.

```bash
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py
```

Result: `24 passed`.

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py
```

Result: `12 passed`.

```bash
python3 -m ruff check src tests tools
```

Result: passed.

```bash
git diff --check
```

Result: passed.

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

Result: passed with 4 warnings on pre-existing branch changes relative to
`origin/main`: `src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`.

Focused protected-surface check for this issue's files:

```bash
printf '%s\n' src/mythic_edge_parser/app/opponent_card_observations.py tests/test_opponent_card_observations.py tests/test_card_performance.py docs/contracts/parser_opponent_card_observations.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result: passed with 0 warnings.

Additional broader check run:

```bash
python3 -m pytest -q
```

Result: `717 passed`.

## Still-Unverified Layers

- Live MTGA logs were not read.
- Workbook schema, webhook delivery, Apps Script, runtime status files,
  failed-post artifacts, generated catalog data, and workbook exports were not
  queried or mutated.
- `tools/check_secret_patterns.py` is not present on this branch, so no
  branch-native content scanner was run.
- No golden replay opponent-observation fixture was added; future fixture
  coverage can be added under a follow-up if reviewer or user wants parser-path
  replay coverage.

## Open Risks

- The helper consumes action-entry dictionaries. Current gameplay action
  runtime artifacts do not always preserve local/actor seat IDs, so the helper
  marks missing seat mapping as degraded/review-required instead of guessing.
- Candidate, ambiguous, contradicted, and name-only resolution are conservative
  review surfaces. A later analytics contract can decide how to consume them.
- Opponent observations are not exported to workbook/webhook/runtime status
  surfaces in v1.

## Unrelated Local Files Observed

Unrelated untracked files remain outside this module:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

The source contract `docs/contracts/parser_opponent_card_observations.md` is
untracked in this checkout and is in scope for issue #50.

## Reviewer Focus

Codex E should pay special attention to:

- whether missing seat mapping should remain a degraded observation or be
  dropped entirely;
- whether candidate/unresolved name resolution is appropriately conservative;
- whether no `gameplay_actions.py` runtime artifact integration is acceptable
  for v1;
- whether card-performance opponent exclusion remains fully protected;
- whether no golden replay fixture is acceptable for this implementation pass.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

If Codex E finds no blocking issues, proceed to Codex F: Module Submitter. If
Codex E finds concrete implementation defects, route to Codex D: Module Fixer.
If Codex E finds contract ambiguity or a required runtime artifact integration,
route to Codex B: Module Contract Writer.

## Pasteable Next-Thread Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #50 and docs/contracts/parser_opponent_card_observations.md.

  Goal:
    Verify the Codex C opponent-card observation helper implementation against the contract. Confirm the module records parser-supported opponent-visible card/action observations while keeping archetype, decklist, hidden-information inference, workbook/webhook/App Script output, AI/model-provider output, and analytics inference out of parser truth.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/50
    - Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/48
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/111
    - Previous merge commit: 76b63622494b0bbc6150e6bd19973b4ac8e0be0c
    - Branch/base: codex/parser-reliability-intelligence

  Use:
    - AGENTS.md
    - docs/agent_constitution.md
    - docs/agent_rules.yml
    - docs/codex_module_workflow.md
    - docs/agent_threads/contract_test.md
    - docs/contracts/parser_opponent_card_observations.md
    - docs/implementation_handoffs/parser_opponent_card_observations_comparison.md
    - docs/contracts/player_log_evidence_ledger.md
    - docs/contracts/parser_golden_replay_harness.md
    - docs/contracts/parser_diagnostics_mode.md
    - docs/contracts/parser_gre_game_state.md
    - docs/contracts/parser_gre_turn_info.md
    - docs/contracts/parser_extractors.md
    - src/mythic_edge_parser/app/opponent_card_observations.py
    - src/mythic_edge_parser/app/gameplay_actions.py
    - src/mythic_edge_parser/app/grp_id_catalog.py
    - src/mythic_edge_parser/app/card_performance.py
    - src/mythic_edge_parser/app/golden_replay.py
    - src/mythic_edge_parser/app/parser_diagnostics.py
    - tests/test_opponent_card_observations.py
    - tests/test_gameplay_actions.py
    - tests/test_card_performance.py
    - tests/test_grp_id_catalog.py
    - tests/test_golden_replay_harness.py

  Confirm:
    - Public constants and helper functions match the contract shape.
    - The helper returns None for non-opponent entries, unsupported action types, hidden draws, and non-mapping inputs.
    - Emitted observations always use actor_relation="opponent".
    - Clean observations preserve known local seat, actor seat, visible evidence, IDs, identity hint source, action type, visibility, evidence status, value source, confidence, and degradation flags.
    - Missing seat mapping is degraded/review-required and does not guess seat IDs.
    - Missing card identity is degraded/review-required and does not guess card names.
    - Candidate, ambiguous, contradicted, name-only, and unresolved name resolution remain enrichment and do not replace observed IDs.
    - Hidden opponent cards, complete opponent decklists, archetypes, and likely-copy inference are not emitted.
    - The helper has no filesystem writes and does not import workbook, webhook, Apps Script, OpenAI/model-provider, diagnostics, golden replay, output transport, or generated-data surfaces.
    - Card-performance aggregation still excludes opponent action entries.
    - Existing gameplay action, catalog, golden replay, and diagnostics behavior remain compatible.
    - No workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

  Validation:
    - python3 -m pytest -q tests/test_opponent_card_observations.py
    - python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py
    - python3 -m ruff check src tests tools
    - git diff --check
    - python3 tools/check_protected_surfaces.py --base origin/main
    - printf '%s\n' src/mythic_edge_parser/app/opponent_card_observations.py tests/test_opponent_card_observations.py tests/test_card_performance.py docs/contracts/parser_opponent_card_observations.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
    - python3 -m pytest -q

  Output:
    - Findings first, if any.
    - Contract-test verdict.
    - Validation results.
    - Remaining non-blocking gaps.
    - Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
    - workflow_handoff block.

  Do not:
    - Target main directly.
    - Close tracker #47 or related issue #11.
    - Change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
    - Infer hidden opponent cards, complete opponent decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces.
    - Make card performance aggregate opponent cards.
    - Copy Manasight source code or commit raw private Player.log excerpts.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/50"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/111"
  previous_merge_commit: "76b63622494b0bbc6150e6bd19973b4ac8e0be0c"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_opponent_card_observations.md"
  target_artifact: "docs/implementation_handoffs/parser_opponent_card_observations_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_opponent_card_observations.py"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "focused stdin protected-surface check for issue #50 files"
    - "python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not infer hidden opponent cards, complete opponent decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces."
    - "Do not make card performance aggregate opponent cards."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/50"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/111"
  previous_merge_commit: "76b63622494b0bbc6150e6bd19973b4ac8e0be0c"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_opponent_card_observations.md"
  target_artifact: "docs/implementation_handoffs/parser_opponent_card_observations_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_opponent_card_observations.py -> 10 passed"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py -> 24 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed with 4 pre-existing branch warnings"
    - "focused stdin protected-surface check for issue #50 files -> passed with 0 warnings"
    - "python3 -m pytest -q -> 717 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not infer hidden opponent cards, complete opponent decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces."
    - "Do not make card performance aggregate opponent cards."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
```
