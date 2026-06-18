# Parser Corpus Companion / Large-Deck Coverage Contract

## Module

Companion / large-deck corpus evidence boundary for the parser corpus parity
report.

Plain English: this slice lets Mythic Edge account for exactly
`gameplay_stress.companion_or_large_deck` as report-only boundary metadata. It
does not add parser support, committed gameplay fixtures, synthetic gameplay
fixtures, companion legality detection, large-deck size detection, decklist
completion, hidden-card inference, sideboard truth, deck identity truth,
archetype classification, gameplay advice, analytics truth, AI truth, coaching
truth, release readiness, production behavior, or full Mythic Edge corpus
parity.

This contract explicitly prevents Mythic Edge from treating generic deck
snapshots, submitted-deck card-content evidence, card identity provenance,
StartHook deck summaries, public taxonomy metadata, or large-looking private
deck material as companion / large-deck parser support.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/406
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/407
- Previous merge commit:
  `bece21b5d5e01ccaff110b7caaf6a1bfbe320bea`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-companion-large-deck-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `bece21b5d5e01ccaff110b7caaf6a1bfbe320bea`
- target_artifact:
  `docs/contracts/parser_corpus_companion_large_deck_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_corpus_opponent_auto_concede_coverage.md`
- `docs/contract_test_reports/parser_corpus_opponent_auto_concede_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier3_deck_state.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `tests/test_collection_parser.py`
- `tests/test_client_actions_parser.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_evidence_ledger.py`
- `tests/test_grp_id_candidates.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, decklists,
  companion candidates, sideboard choices, deck names, deck IDs, card choices,
  strategy notes, gameplay advice, private smoke reports, generated data,
  SQLite files, runtime artifacts, workbook exports, credentials, tokens, API
  keys, or webhook URLs.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic companion / large-deck coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, or blocked-private-evidence status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage.

Reasoning:

- The current corpus taxonomy audit maps public companion / large-deck metadata
  to Mythic Edge scenario family
  `gameplay_stress.companion_or_large_deck`, but marks it `missing`.
- Mythic Edge has adjacent deck-related evidence surfaces, including StartHook
  deck snapshots, StartHook-bound deck summaries, submitted-deck card-content
  evidence, runtime submitted-deck artifacts, GRP ID candidate review, and card
  identity provenance.
- Those surfaces can describe bounded parser-observed card IDs, submitted
  mainboard/sideboard lists, summary/deck correlations, or card-identity
  lookup provenance. They do not prove companion presence, companion legality,
  companion castability, sideboard companion state, large-deck size, full
  decklist contents, deck identity, deck ownership, archetype classification,
  matchup plans, strategy, or gameplay correctness.
- A synthetic coverage fixture would need a future contract that defines an
  owned and privacy-safe observable evidence model for a companion or
  large-deck scenario. This issue does not have that evidence yet.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic or sanitized metadata.
- Leaving the row plain `missing` hides a useful inspected boundary: adjacent
  deck and card-identity evidence is intentionally not enough for a companion /
  large-deck support claim.

This decision records `gameplay_stress.companion_or_large_deck` as report-only
boundary metadata. It changes corpus parity metadata and tests only; it does
not change parser behavior or create a dedicated companion / large-deck
fixture.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`gameplay_stress.companion_or_large_deck` scenario family. Parser modules own
deck snapshot parsing, submitted-deck parsing, card identity surfaces, parser
events, router behavior, match/game identity, and final reconciliation. The
corpus parity package owns only the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance evidence
for context, but it is not a Parser behavior module, deck-state module,
submitted-deck module, card-identity module, diagnostics module, golden replay
module, analytics module, AI module, coaching module, release-readiness module,
or production module.

## Truth Owner

Truth owner for `gameplay_stress.companion_or_large_deck` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for parser behavior referenced only as non-claim context:

- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`

Truth boundary:

- StartHook collection parsing may describe bounded `PlayerCards`,
  `DeckSummaries`, and `Decks` evidence.
- Submitted-deck parsing may describe observed normalized submitted mainboard
  and sideboard `grpId` lists from submit-deck payloads.
- Card identity provenance may describe how `grpId` / `cardId` identifiers can
  be observed or enriched.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for `gameplay_stress.companion_or_large_deck`.
- Corpus parity must not infer companion presence, companion legality,
  companion castability, large-deck size, complete decklists, exact deck
  identity, deck ownership, sideboard state, hidden cards, archetypes, matchup
  plans, gameplay advice, player mistakes, analytics truth, AI truth, coaching
  truth, release readiness, production behavior, or full corpus parity from
  adjacent deck/card evidence.

Coverage status is review metadata. It is not parser truth, deck-state truth,
submitted-deck truth, card-identity truth, match/game truth, analytics truth,
AI truth, coaching truth, merge readiness, deploy readiness, public/private
release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing deck/card parser evidence and evidence-ledger boundary docs
  -> explicit companion / large-deck non-claim boundary metadata
  -> corpus parity row for gameplay_stress.companion_or_large_deck
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change StartHook parsing, submit-deck parsing,
  card-list normalization, runtime submitted-deck artifacts, GRP candidate
  scoring, evidence-ledger entries, parser events, router dispatch,
  match/game identity, parser state final reconciliation, workbook output,
  analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn generic deck snapshots, submitted-deck
  card-content evidence, card identity provenance, StartHook summaries, public
  taxonomy labels, local private deck material, or large-looking card lists
  into a companion / large-deck parser support claim.

Protected surfaces explicitly not touched:

- parser behavior
- StartHook parser behavior
- client-action parser behavior
- submitted-deck parsing behavior
- card-list normalization behavior
- parser event classes
- router semantics
- parser state final reconciliation
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- runtime status artifacts or schema
- runtime submitted-deck artifacts
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- failed delivery artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_companion_large_deck_coverage.md`

Future implementation files owned by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md`

Referenced but not silently owned:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `tests/test_collection_parser.py`
- `tests/test_client_actions_parser.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_evidence_ledger.py`
- `tests/test_grp_id_candidates.py`

Codex C may edit `src/mythic_edge_parser/app/corpus_parity_report.py` only if
the existing report code cannot represent the contracted manifest/session
ledger metadata. Codex C must not edit parser modules or runtime modules unless
it returns to Codex B with a contract loopback.

## Public Interface

This contract covers corpus parity metadata only.

Authorized scenario family:

| Scenario family | Authorized status | Meaning |
| --- | --- | --- |
| `gameplay_stress.companion_or_large_deck` | `covered_report_only` | The corpus report records that companion / large-deck coverage has an inspected non-claim boundary. |

Authorized manifest entry:

| Field | Required value |
| --- | --- |
| `entry_id` | `companion_large_deck_boundary_report_v1` |
| `entry_type` | `session_ledger_entry` |
| `source_kind` | `committed_count_only_report` |
| `commit_status` | `committed` |
| `privacy_class` | `committed_count_only` |
| `sanitization_status` | `not_applicable_count_only` |
| `scenario_families` | `["gameplay_stress.companion_or_large_deck"]` |
| `parser_event_families` | `[]` |
| `coverage_status` | `covered_report_only` |
| `coverage_basis` | `["fixture_metadata_only"]` |

Required `parser_claim_families`:

- `companion_large_deck_boundary_report`
- `generic_deck_snapshot_not_companion_or_large_deck`
- `submitted_deck_cards_not_decklist_truth`
- `card_identity_not_deck_shape_truth`
- `companion_legality_not_claimed`
- `decklist_completion_non_claim`

Required manifest notes or review text must state that the entry is report-only
boundary metadata and does not claim:

- companion presence
- companion legality
- companion castability
- large-deck size
- complete decklist contents
- deck identity
- deck ownership
- submitted-deck truth beyond existing submitted-card evidence
- sideboard truth beyond existing observed lists
- hidden-card truth
- archetype classification
- matchup plans
- gameplay advice
- analytics truth
- AI truth
- coaching truth
- release readiness
- production behavior
- full Mythic Edge corpus parity

Authorized session ledger entry:

| Field | Required value |
| --- | --- |
| `session_id` | `companion_large_deck_boundary_report_v1` |
| `authorized_by_contract` | `docs/contracts/parser_corpus_companion_large_deck_coverage.md` |
| `scenario_families` | `["gameplay_stress.companion_or_large_deck"]` |
| `format_family` | `gameplay_stress` |
| `match_shape` | `companion_large_deck_boundary_report_only` |
| `record_summary` | `committed_companion_large_deck_boundary_metadata_only` |

Required session-ledger `parser_coverage` facts:

- `event_families` must be `{}`.
- `unknown_entries` must be `0`.
- `truncation_count` must be `0`.
- `deck_snapshot_reference_entries` must be `1`.
- `submitted_deck_reference_entries` must be `1`.
- `card_identity_reference_entries` must be `1`.
- `dedicated_companion_fixtures` must be `0`.
- `dedicated_large_deck_fixtures` must be `0`.
- `companion_legality_claims` must be `0`.
- `decklist_completion_claims` must be `0`.

Required session-ledger game row summary:

- `game_rows.count` must be `0`.
- `game_rows.result_shape` must be `not_applicable`.

Required redaction and privacy facts:

- no raw/private Player.log excerpts
- no external corpus payloads
- no private decklists
- no raw submitted-deck payloads
- no deck names
- no deck IDs
- no sideboard choices
- no companion candidates
- no card choices
- no strategy notes
- no local smoke outputs
- no generated/private/runtime artifacts
- no credentials, tokens, API keys, or webhook URLs

Forbidden public-interface changes:

- no new parser events
- no parser route changes
- no corpus parity report CLI behavior changes unless required by existing
  metadata rendering
- no diagnostics, golden replay, feature-equity, evidence-ledger, runtime
  status, analytics, workbook, webhook, Apps Script, Google Sheets, AI, or
  coaching interface changes

## Inputs

Allowed inputs:

- Existing committed corpus parity manifest and session ledger.
- Existing committed contracts and contract-test reports for corpus parity,
  StartHook deck snapshot, deck summary, submitted-deck card-content
  provenance, card identity provenance, and deck-state deferral.
- Existing focused parser tests for adjacent deck/card evidence, used only as
  non-claim context.
- Public Manasight metadata only as category-level reference context through
  the already merged taxonomy audit or public metadata pages.

Forbidden inputs:

- Manasight raw logs, `.log.gz` files, compressed corpus files, raw session
  payloads, external corpus contents, hash lists, byte-size row lists, or
  capture-date row lists.
- Private Player.log excerpts, private local logs, raw submitted-deck payloads,
  raw decklists, sealed pools, deck names, deck IDs, companion choices,
  sideboard choices, card choices, strategy notes, private smoke reports, local
  runtime artifacts, generated data, SQLite files, workbook exports, secrets,
  credentials, tokens, API keys, or webhook URLs.
- Model-provider output or AI interpretation.

## Outputs

Authorized outputs for Codex C:

- One corpus manifest entry for
  `gameplay_stress.companion_or_large_deck`.
- One session-ledger entry with count-only, report-only boundary metadata.
- Focused tests proving the corpus report renders the row as
  `covered_report_only` and preserves all companion / large-deck non-claims.
- An implementation handoff and contract test report.

Forbidden outputs:

- committed raw or synthetic gameplay log slices
- committed decklists
- committed deck names or deck IDs
- committed companion candidates
- committed card choices or sideboard choices
- new parser event classes
- new parser route behavior
- new runtime files
- new workbook/export/webhook/App Script fields
- new analytics tables/views
- AI/model-provider outputs
- release-readiness or deploy-readiness verdicts

## Invariants

- `gameplay_stress.companion_or_large_deck` may become only
  `covered_report_only` in this slice.
- `coverage_basis` must remain exactly `["fixture_metadata_only"]` unless a
  future contract authorizes a real fixture path.
- `parser_event_families` must remain empty for the authorized entry.
- Generic deck snapshots are not companion / large-deck evidence.
- StartHook `DeckSummaries` are not dedicated companion / large-deck evidence.
- Submitted-deck card lists are not complete decklist truth, deck identity
  truth, or companion legality truth.
- Card identity provenance is not deck shape truth.
- Public taxonomy metadata is not parser support evidence.
- Local private or large-looking deck material must not be committed.
- Corpus parity status must not become parser truth, deck-state truth,
  analytics truth, AI truth, coaching truth, merge readiness, deploy readiness,
  release readiness, production behavior, or tracker-completion authority.

## Error Behavior

Malformed manifest or session-ledger data must fail existing corpus parity
validation tests. Codex C must not add permissive parsing that silently accepts
ambiguous coverage claims.

If implementation discovers that the existing corpus report cannot represent
the contracted report-only boundary without changing report code, Codex C may
make the smallest corpus-report-only code change and document it in the
implementation handoff. That change must not affect parser behavior.

If implementation discovers a genuine parser behavior gap or a tempting
fixture opportunity, Codex C must stop and route back to Codex B. This contract
does not authorize parser behavior changes or synthetic fixture promotion.

If private evidence would be needed to make a stronger claim, the row must
remain report-only and the private evidence must stay out of the repo and out
of GitHub issue comments.

## Side Effects

Allowed future Codex C side effects:

- Edit committed corpus parity metadata.
- Edit focused corpus parity tests.
- Write implementation handoff and contract test report docs.

Forbidden side effects:

- opening or closing issues
- opening a PR unless separately asked
- staging or committing unless separately asked
- changing parser behavior
- creating runtime/generated/private artifacts
- committing local logs or raw private evidence
- changing CI gates, merge policy, deploy policy, or production behavior

## Dependency Order

Codex C should make changes in this order:

1. Confirm branch and base state against `origin/codex/parser-parity`.
2. Compare current manifest/session-ledger/report behavior against this
   contract.
3. Add the manifest entry.
4. Add the session-ledger entry.
5. Add focused corpus parity tests for status, claim families, non-claims, and
   summary counts.
6. Run focused validation.
7. Write the implementation handoff and contract test report.
8. Run docs/protected-surface/secret checks on the changed files.

## Compatibility

Compatibility expectations:

- Existing covered families and summary counts must remain stable except for
  the one status move authorized here.
- Current report semantics for `covered_committed`, `covered_synthetic`,
  `covered_report_only`, `partial`, `missing`, `blocked_private_evidence`, and
  `blocked_external_boundary` must remain compatible.
- Existing entries for StartHook deck snapshot, deck summary, submitted-deck
  card-content provenance, card identity provenance, and deck-state deferral
  must not be reinterpreted.
- No report consumer may treat this row as companion / large-deck parser
  support.

Expected summary-count delta after Codex C:

- `covered_report_only` increases by `1`.
- `missing` decreases by `1`.
- Other status counts remain unchanged unless the current base branch already
  contains unrelated merged changes.

## Tests Required

Codex C must run or justify not running:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also inspect, but should not need to run unless it edits
adjacent code:

- `tests/test_collection_parser.py`
- `tests/test_client_actions_parser.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_evidence_ledger.py`
- `tests/test_grp_id_candidates.py`

## Acceptance Criteria

- `docs/contracts/parser_corpus_companion_large_deck_coverage.md` exists and
  records the report-only boundary.
- Codex C can implement the contract with corpus metadata/tests/docs only.
- `gameplay_stress.companion_or_large_deck` is represented as
  `covered_report_only`, not `covered_synthetic`.
- The manifest and session ledger preserve explicit non-claims for companion
  presence, companion legality, large-deck size, decklist completion, deck
  identity, hidden-card inference, archetype classification, gameplay advice,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, and full corpus parity.
- No parser behavior or protected surface changes are authorized.
- No raw/private/external corpus contents or decklists are committed.

## Unknowns

- No committed Mythic Edge-owned fixture currently proves a companion-specific
  scenario.
- No committed Mythic Edge-owned fixture currently proves a large-deck-specific
  scenario.
- Current parser behavior may preserve card-list evidence, but this contract
  does not determine whether the parser can or should classify companion or
  large-deck state.
- The exact future evidence model for safe synthetic companion / large-deck
  coverage remains undefined.

## Suspected Gaps

- Corpus parity can currently express that the family has been inspected, but
  not that Mythic Edge has dedicated companion / large-deck parser support.
- Adjacent deck evidence surfaces are easy to overread as deck-state truth.
- A future companion / large-deck fixture contract will need sharper rules for
  allowed synthetic card IDs, deck-size counts, sideboard/companion fields, and
  whether any card-list values can safely be committed.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #408, companion / large-deck corpus coverage, under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/408

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_companion_large_deck_coverage.md

Goal:
Implement the smallest corpus metadata/test/docs package needed to satisfy the contract. This is report-only boundary coverage for `gameplay_stress.companion_or_large_deck`, not parser support and not synthetic gameplay coverage.

Expected files:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md
- docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md

Required behavior:
- Add exactly one report-only manifest entry for `gameplay_stress.companion_or_large_deck`.
- Add exactly one count-only session-ledger entry.
- Keep `coverage_status` as `covered_report_only`.
- Keep `coverage_basis` as `["fixture_metadata_only"]`.
- Keep `parser_event_families` empty.
- Preserve explicit non-claims for companion presence, companion legality, companion castability, large-deck size, complete decklists, deck identity, deck ownership, sideboard truth, hidden-card truth, archetype classification, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, production behavior, and full corpus parity.
- Do not change parser behavior or protected surfaces.

Do not:
- Target main directly.
- Close tracker #158.
- Claim full Mythic Edge corpus parity.
- Promote this family to covered_synthetic without contract loopback.
- Import, copy, mirror, or commit Manasight raw logs, external corpus contents, private Player.log excerpts, private local logs, raw submitted-deck payloads, decklists, deck names, deck IDs, companion choices, sideboard choices, card choices, strategy notes, private smoke reports, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs.
- Change parser behavior, StartHook parser behavior, client-action parser behavior, submitted-deck parsing behavior, card-list normalization behavior, parser event classes, router semantics, parser state final reconciliation, match/game identity, deduplication, diagnostics, golden replay, feature-equity, evidence ledger, runtime status, workbook, webhook, Apps Script, Google Sheets sync, output transport, analytics, AI/OpenAI, coaching, CI gates, merge policy, deploy policy, or production behavior.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
- python3 -m ruff check src tests tools
- git diff --check

End with:
- implementation summary
- files changed
- validation results
- remaining risks
- recommended next role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/406"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/407"
  previous_merge_commit: "bece21b5d5e01ccaff110b7caaf6a1bfbe320bea"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_companion_large_deck_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-companion-large-deck-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret/protected-surface checks"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not promote gameplay_stress.companion_or_large_deck to covered_synthetic without contract loopback."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, raw submitted-deck payloads, decklists, deck names, deck IDs, companion choices, sideboard choices, card choices, strategy notes, private smoke reports, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces."
```
