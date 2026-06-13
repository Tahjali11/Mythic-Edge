# Parser Corpus Sealed Lifecycle Coverage Contract

## Module

Sealed lifecycle corpus coverage under the Mythic Edge parser corpus parity
roadmap.

Plain English: this contract defines the safe first slice for deciding how
Mythic Edge should eventually cover sealed event entry, sealed deckbuilding,
and sealed matches in its own corpus. It must not copy Manasight sealed logs,
commit private sealed deck contents, or claim sealed support from public
taxonomy mapping alone.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/355

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/352
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/354
- previous_merge_commit: `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- branch: `codex/parser-corpus-sealed-lifecycle-coverage`
- base_branch: `main`
- observed_base_commit: `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- target_artifact: `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`
- expected_report_artifact:
  `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related Mythic Edge authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/decklists.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`

External reference status:

- Public Manasight metadata may be used only through the already merged #352
  taxonomy audit or by category-level reference checks.
- This contract does not authorize importing, copying, mirroring, or
  committing Manasight logs, compressed corpus files, raw session payloads,
  hash lists, byte-size row lists, capture-date row lists, parser source, or
  external corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage policy, safe evidence classes, coverage
status preconditions, and Codex C report requirements for the sealed lifecycle
slice.

It does not own parser behavior, parser event interpretation, deck-state truth,
submitted-deck content truth, workbook output, analytics truth, AI truth,
merge readiness, deploy readiness, public-release readiness, or tracker
completion.

## Internal Project Area

Corpus / Provenance.

This work consumes Parser evidence and Evidence Ledger vocabulary, but the V1
artifact is a corpus coverage inspection and planning report.

## Truth Owner

Truth owner for current corpus coverage statuses:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Truth owner for sealed parser behavior:

- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`

Truth owner for submitted-deck signal and card-content provenance:

- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`

Truth boundary:

- Public Manasight metadata can explain why these scenario families matter.
- Mythic Edge-owned committed fixtures, synthetic fixtures, or local/private
  report summaries are required before Mythic Edge can claim coverage.
- Parser behavior claims must come from Mythic Edge code and tests, not from
  external category labels.
- `SubmitDeckResp` evidence may support submit-deck observation or card-list
  observation. It is not broad sealed deckbuilding truth without sealed event
  context and an authorized fixture/report path.
- `EventJoin`, `EventEnterPairing`, and `EventClaimPrize` evidence may support
  generic event lifecycle observation. They are not sealed-entry truth without
  sealed event identity context.

## Bridge-Code Status

`bridge_code`

Source project area: External / Collaboration Surface.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
public Manasight sealed category labels from #352
  -> Mythic Edge sealed scenario family questions
  -> Mythic Edge parser behavior inspection
  -> report-only coverage plan and future child issue recommendations
```

Forbidden reverse flow:

- The sealed coverage contract must not import Manasight sealed logs.
- The contract must not copy Manasight parser source or raw session details.
- The contract must not make external metadata into Mythic Edge coverage truth.
- The contract must not change parser behavior to satisfy a corpus row.
- The contract must not move sealed lifecycle truth into workbook formulas,
  dashboard logic, webhook transport, Apps Script, analytics, AI, or coaching
  surfaces.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status artifacts
- failed delivery artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- production behavior

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`

Future Codex C artifacts authorized by this contract:

- `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`

Files Codex C may inspect but must not change in V1 unless a later contract
explicitly authorizes a fixture/status implementation:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/decklists.py`
- `src/mythic_edge_parser/app/event_identity.py`
- focused tests for event identity, event lifecycle, client actions, match
  state, state summaries, transforms, saved event replay, and corpus parity

V1 does not authorize changing:

- parser modules;
- parser tests, except through a later explicit implementation route;
- corpus manifest or session ledger statuses;
- golden replay fixtures;
- feature-equity baselines;
- runtime artifacts;
- workbook, webhook, Apps Script, Google Sheets, analytics, AI, or local app
  surfaces.

## Public Interface

V1 public interface is a documentation/report artifact:

```text
docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md
```

The report must be readable by humans and structured enough for Codex threads
to decide the next child issue. No public Python API, CLI flag, environment
variable, workbook column, webhook field, parser event, runtime route, or
schema migration is required.

## In-Scope Scenario Families

The only corpus scenario families in scope are:

| Scenario family | Current status | V1 decision |
| --- | --- | --- |
| `core_gameplay.sealed_entry` | `missing` | Keep missing until Mythic Edge-owned sealed entry evidence exists. |
| `core_gameplay.sealed_deckbuild` | `missing` | Keep missing until sealed deckbuilding evidence is defined without leaking deck contents. |
| `core_gameplay.sealed_matches` | `missing` | Keep missing until owned sealed match fixture or report evidence proves the parser path. |

Out-of-scope scenario families:

- `core_gameplay.draft_only`
- `core_gameplay.draft_with_games`
- deck API blind spots
- collection or store surfaces
- gameplay stress mechanics
- connection/reconnect and runtime interruption categories
- evidence ledger field coverage
- analytics, Match Journal, local app, overlay, or workbook-visible coverage

## Observed Current Behavior

Observed from branch `codex/parser-corpus-sealed-lifecycle-coverage` at
`dfaf7c54f0146b28fe746e24fbba3a53a5e49611`:

- Issue #355 is open.
- Tracker #158 is open.
- Issue #352 is closed and PR #354 is merged.
- The Mythic Edge corpus parity report is
  `partial_coverage_map_ready`.
- Report summary:
  - total scenario families: 45
  - covered committed: 6
  - covered synthetic: 2
  - covered report-only: 0
  - partial: 3
  - missing: 28
  - blocked external boundary: 6
- The three sealed lifecycle rows are all currently `missing` with
  `coverage_basis == ["external_reference_only"]` and no Mythic Edge entries.
- The #352 taxonomy audit maps public Manasight sealed entry, sealed
  deckbuilding, and sealed matches to the three Mythic Edge sealed families
  and marks them `needs_parser_behavior_before_corpus_claim`.

Observed parser behavior relevant to sealed coverage:

- `event_identity.classify_event_identity(...)` recognizes event IDs
  containing sealed as limited sealed event identity. Focused tests assert
  `event_family == "sealed"`, `queue_subtype == "sealed"`, and
  `is_sealed_match is True` for a sealed event ID.
- `event_lifecycle.try_parse(...)` recognizes generic `EventJoin`,
  `EventEnterPairing`, and `EventClaimPrize` markers and preserves the raw
  lifecycle body. It does not extract JSON fields from lifecycle bodies.
- `match_state.try_parse(...)` extracts `event_id` from match room config or
  player entries and emits match state payloads. It does not by itself prove
  sealed entry, deckbuild, or match lifecycle coverage.
- GRE GameState parsing and state summary ingestion can carry `superFormat`
  and `matchWinCondition` into match summaries when present.
- `client_actions.try_parse(...)` recognizes specialized
  `ClientMessageType_SubmitDeckResp` payloads and normalizes `deck_cards` and
  `sideboard_cards`.
- `state.py` treats `submit_deck_resp` and generic
  `ClientMessageType_SubmitDeckResp` as submit-deck seen signals for the
  current match.
- Submit-deck card lists are sensitive card-content evidence and are covered
  by evidence-ledger boundaries. They do not prove sealed deckbuilding by
  themselves.

## Scope Decision

V1 implementation should be report-only parser behavior inspection and sealed
coverage planning.

Codex C should not change any corpus coverage status in V1. Specifically, it
must keep these rows `missing` unless a later contract explicitly authorizes
fixture/status work:

- `core_gameplay.sealed_entry`
- `core_gameplay.sealed_deckbuild`
- `core_gameplay.sealed_matches`

Rationale:

- The merged #352 audit identifies sealed lifecycle as the highest-priority
  next child, but also records that parser behavior must be inspected before
  coverage can be claimed.
- Current parser surfaces can identify sealed match context and generic event
  lifecycle signals, but no owned committed corpus entry ties those signals
  together as sealed lifecycle evidence.
- Current submit-deck support proves submit-deck observation and card-list
  normalization. It does not prove sealed deckbuilding, sealed pool contents,
  sideboard correctness, deck construction quality, or sealed lifecycle
  completion.
- Committing sealed deckbuilding evidence is privacy-sensitive because it can
  expose deck contents or card-pool details.

Codex C's V1 report should answer whether the next implementation child should
be:

- a synthetic sealed match fixture,
- a synthetic sealed entry lifecycle fixture,
- a report-only sealed deckbuild summary,
- a sealed event identity/parser test slice,
- or a smaller prerequisite parser contract.

## Inputs

Allowed inputs:

- repo-owned contracts, reports, manifests, session ledgers, tests, and parser
  source;
- the current Mythic Edge corpus parity report generated from repo-owned
  inputs;
- the #352 taxonomy audit report;
- public Manasight category labels as reference taxonomy only;
- synthetic examples written by Codex C in its report prose, if they do not
  include raw log excerpts, external rows, or private card lists.

Forbidden inputs:

- Manasight raw logs;
- `.log.gz` files;
- raw session payloads;
- compressed corpus files;
- hash lists, byte-size row lists, capture-date row lists, or mirrored
  manifest rows from external corpus files;
- copied external parser source;
- private `Player.log` excerpts;
- private local logs;
- raw sealed pool data;
- raw submitted decklists;
- generated data;
- SQLite files;
- runtime artifacts;
- failed delivery artifacts;
- workbook exports;
- credentials, tokens, API keys, or webhook URLs.

## Outputs

Required V1 output:

- `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`

Required report sections:

- source snapshot;
- current Mythic Edge corpus parity snapshot for the three sealed rows;
- observed parser behavior inspection;
- sealed entry evidence path assessment;
- sealed deckbuild evidence path assessment;
- sealed matches evidence path assessment;
- privacy and protected-surface assertions;
- explicit non-claims;
- recommended next child issue or implementation path.

Required Codex C handoff:

- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`

The report may recommend future changes, but V1 must not write:

- corpus manifest entries;
- session ledger entries;
- golden replay fixtures;
- parser code;
- parser tests;
- workbook/webhook/App Script fields;
- local runtime artifacts.

## Coverage Claim Preconditions

### `core_gameplay.sealed_entry`

A future status promotion requires Mythic Edge-owned evidence that connects a
sealed event identity or sealed event context to event entry lifecycle
markers.

Evidence that is not enough by itself:

- public Manasight sealed category labels;
- generic `EventJoin` without sealed context;
- event ID classification without lifecycle markers;
- manual prose claiming that sealed entry was observed.

Possible future acceptable evidence:

- synthetic committed fixture metadata that demonstrates sealed event identity
  plus entry lifecycle marker handling through the normal parser route;
- sanitized Mythic Edge-owned fixture snippet approved by a future contract;
- local/private report-only summary that records redacted sealed entry
  lifecycle evidence without exposing raw logs or deck contents.

### `core_gameplay.sealed_deckbuild`

A future status promotion requires an explicitly scoped sealed deckbuilding
evidence shape that preserves privacy.

Evidence that is not enough by itself:

- `submit_deck_seen`;
- `SubmitDeckResp` card lists without sealed context;
- raw or full submitted deck contents;
- decklist name, deck ID, sealed pool contents, card ratings, or card choices;
- public Manasight sealed deckbuild category labels.

Possible future acceptable evidence:

- report-only metadata that a sealed-context submit-deck signal was observed,
  with counts/signature only and no raw card list;
- synthetic submit-deck evidence that uses fake integer IDs and explicit
  sealed event context;
- a separate privacy-reviewed contract for sanitized sealed deckbuilding
  fixture snippets.

### `core_gameplay.sealed_matches`

A future status promotion requires Mythic Edge-owned evidence that a sealed
event context flows through match/game parser behavior.

Evidence that is not enough by itself:

- sealed event ID classification alone;
- generic match-state parsing without sealed event context;
- a sealed public category label in external metadata;
- a generic limited or draft match fixture.

Possible future acceptable evidence:

- synthetic sealed match fixture that exercises match state, GameState, game
  result, and match summary identity without private card/deck content;
- sanitized Mythic Edge-owned sealed match snippet approved by a future
  contract;
- report-only local/private sealed match summary with redacted source
  evidence.

## Invariants

- The three sealed lifecycle rows remain `missing` in V1.
- Public Manasight metadata remains reference taxonomy only.
- Corpus reports do not decide parser truth.
- Corpus reports do not decide merge readiness, deploy readiness,
  public-release readiness, tracker completion, analytics truth, AI truth, or
  gameplay advice.
- Event identity classification may support sealed match context, but it is
  not a sealed lifecycle coverage claim by itself.
- Event lifecycle markers may support lifecycle observation, but they are not
  sealed entry coverage by themselves.
- Submit-deck signals may support submit-deck observation, but they are not
  sealed deckbuilding truth by themselves.
- Deck contents, sealed pool contents, hidden cards, archetype labels,
  matchup plans, card ratings, and player choices must not become corpus
  truth in this slice.

## Error Behavior

Codex C must stop and report a blocker if:

- #352 / PR #354 is not present in the local branch;
- the sealed rows are not present in the current corpus taxonomy;
- the current report does not show the three sealed rows as `missing`;
- a proposed implementation requires raw external logs or private logs;
- a proposed fixture would include raw sealed deck contents or private card
  pool data;
- parser behavior changes appear necessary before the report can make honest
  claims.

If Codex C finds current behavior contradicts this contract, it must route
back to Codex B for clarification or Codex A for a smaller problem
representation.

## Side Effects

Allowed Codex C side effects:

- write `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`;
- write `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`.

Forbidden Codex C side effects in V1:

- modify parser code;
- modify parser tests;
- modify corpus manifest or session ledger statuses;
- add committed log fixtures;
- add raw/private/external artifacts;
- write runtime status artifacts;
- update workbook, webhook, Apps Script, Google Sheets, analytics, AI,
  production, or local app surfaces;
- close #158 or #355;
- open a PR unless separately asked.

## Dependency Order

Codex C should work in this order:

1. Verify branch state includes PR #354 merge commit
   `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`.
2. Regenerate the corpus parity report from repo-owned inputs.
3. Confirm the three sealed rows are still `missing`.
4. Inspect focused parser surfaces and tests listed in this contract.
5. Produce the report-only sealed lifecycle coverage assessment.
6. Produce the implementation handoff with the next recommended child route.
7. Run docs, privacy, protected-surface, and focused corpus validation.

## Compatibility

V1 must preserve:

- `SCENARIO_FAMILIES` ordering and values;
- `COVERAGE_STATUSES` vocabulary;
- corpus manifest schema version;
- session ledger schema version;
- corpus parity report schema version;
- current parser event classes;
- current event identity classifier behavior;
- current event lifecycle parser behavior;
- current client-action parser behavior;
- current submit-deck evidence-ledger boundaries;
- current workbook/webhook/App Script/output/local app behavior.

## Tests Required

Codex C should run:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_client_actions_parser.py tests/test_parsers.py tests/test_app_models.py tests/test_transforms.py
python3 tools/check_agent_docs.py
git diff --check
git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If Codex C adds any test, fixture, or manifest change despite this V1 report
route, it must stop and obtain a contract clarification first.

Codex E should verify:

- the V1 report does not change sealed corpus statuses;
- no external/raw/private log artifacts are committed;
- no raw sealed deck contents or submitted decklists are committed;
- parser behavior is inspected but not changed;
- sealed entry, deckbuild, and match non-claims are explicit;
- future coverage paths require Mythic Edge-owned evidence.

Codex F should stage only reviewed docs/report/handoff files.

Codex G must not close tracker #158 unless explicitly instructed by the user.

## Acceptance Criteria

- `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md` exists.
- The contract names the three in-scope sealed scenario families.
- The contract records the current rows as `missing`.
- The contract decides V1 is report-only parser behavior inspection and
  planning.
- The contract forbids status promotion in V1.
- The contract defines coverage preconditions for sealed entry, sealed
  deckbuild, and sealed matches.
- The contract preserves Manasight metadata as reference taxonomy only.
- The contract forbids external/raw/private logs and raw sealed deck contents.
- The contract defines validation expectations and a Codex C handoff.

## Open Questions And Contract Risks

- Sealed lifecycle may require a later parser contract if current event
  lifecycle payloads do not preserve enough sealed event context.
- Sealed deckbuilding may need a privacy-specific fixture policy before any
  committed evidence is safe.
- A synthetic fixture may be enough for sealed matches, but that should be a
  separate implementation child after the V1 report confirms the parser path.
- Event identity can classify sealed matches today, but corpus parity needs
  fixture/report evidence, not just classifier capability.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #355 under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/355

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Branch:
  codex/parser-corpus-sealed-lifecycle-coverage

  Contract:
  docs/contracts/parser_corpus_sealed_lifecycle_coverage.md

  Goal:
  Implement the V1 report-only sealed lifecycle corpus coverage inspection.
  Produce a local repo-owned report that inspects current parser behavior and
  defines the next safe coverage path for core_gameplay.sealed_entry,
  core_gameplay.sealed_deckbuild, and core_gameplay.sealed_matches without
  changing parser behavior or corpus coverage statuses.

  Do:
    - Verify PR #354 is present in the local branch at or after merge commit
      dfaf7c54f0146b28fe746e24fbba3a53a5e49611.
    - Regenerate the current corpus parity report from repo-owned inputs.
    - Confirm the three sealed rows remain missing.
    - Inspect focused parser surfaces for sealed event identity, generic event
      lifecycle markers, submit-deck signals, match state, GameState game_info,
      state summaries, and submitted-deck evidence boundaries.
    - Create docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md.
    - Create docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md.
    - Recommend the next child path: synthetic sealed match fixture, synthetic
      sealed entry lifecycle fixture, report-only sealed deckbuild summary,
      sealed parser behavior prerequisite, or another smaller slice.

  Do not:
    - Implement parser behavior changes.
    - Change corpus manifest or session ledger coverage statuses.
    - Add committed log fixtures.
    - Open a PR.
    - Close #158 or #355.
    - Import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw
      session payloads, compressed corpus files, hash lists, byte-size lists,
      capture-date row lists, or external corpus contents.
    - Commit private Player.log excerpts, private local logs, raw sealed pool
      data, raw submitted decklists, generated data, SQLite files, runtime
      artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs.
    - Claim full Mythic Edge corpus parity.
    - Claim sealed support from taxonomy mapping alone.
    - Infer sealed deck contents, hidden cards, complete decklists, archetypes,
      gameplay advice, player mistakes, or AI/coaching truth.
    - Change parser state final reconciliation, parser event classes, router
      semantics, match/game identity, deduplication, workbook schema, webhook
      payload shape, Apps Script behavior, Google Sheets sync, output transport,
      analytics truth, AI truth, coaching behavior, OpenAI/model-provider
      behavior, CI gates, merge readiness, deploy readiness, or production behavior.

  Validation:
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m pytest -q tests/test_corpus_parity_report.py
    - python3 -m pytest -q tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_client_actions_parser.py tests/test_parsers.py tests/test_app_models.py tests/test_transforms.py
    - python3 tools/check_agent_docs.py
    - git diff --check
    - git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/355"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/352"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/354"
  previous_merge_commit: "dfaf7c54f0146b28fe746e24fbba3a53a5e49611"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_sealed_lifecycle_coverage.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md"
  expected_handoff: "docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md"
  verdict: "contract_ready_for_report_only_sealed_lifecycle_inspection"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-lifecycle-coverage"
  base_commit: "dfaf7c54f0146b28fe746e24fbba3a53a5e49611"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 -m pytest -q tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_client_actions_parser.py tests/test_parsers.py tests/test_app_models.py tests/test_transforms.py"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not change corpus manifest or session ledger coverage statuses in V1."
    - "Do not add committed log fixtures in V1."
    - "Do not open a PR."
    - "Do not close #158 or #355."
    - "Do not import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, raw sealed pool data, raw submitted decklists, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs."
    - "Do not claim full Mythic Edge corpus parity or sealed support from taxonomy mapping alone."
    - "Do not infer sealed deck contents, hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or AI/coaching truth."
    - "Do not change parser state final reconciliation, parser event classes, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, or production behavior."
```
