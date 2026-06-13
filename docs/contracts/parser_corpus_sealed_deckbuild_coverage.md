# Parser Corpus Sealed Deckbuild Coverage Contract

## Module

Sealed deckbuild corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge move exactly
`core_gameplay.sealed_deckbuild` from missing coverage to safe synthetic
metadata coverage. It proves only that Mythic Edge has repo-owned corpus
evidence tying sealed event context to a bounded submit-deck/deckbuild signal.
It does not prove sealed pool contents, submitted-deck card-content truth,
decklist identity, deck names, card choices, sideboarding quality, archetypes,
gameplay advice, analytics truth, AI truth, or coaching truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/361
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/359
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/360
- Previous merge commit: `369e2d5396f0fc9b42565f102a88e6ad498bedf7`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-sealed-deckbuild-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `369e2d5396f0fc9b42565f102a88e6ad498bedf7`
- target_artifact: `docs/contracts/parser_corpus_sealed_deckbuild_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md`
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
- `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md`
- `docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md`
- `docs/contracts/parser_corpus_sealed_match_coverage.md`
- `docs/contract_test_reports/parser_corpus_sealed_match_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `docs/contracts/parser_client_actions.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/event_identity.py`

External reference status:

- Public Manasight metadata may be used only through already merged taxonomy,
  sealed lifecycle, sealed entry, and sealed match audits or as category-level
  reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the sealed deckbuild scenario
family. Parser modules and parser state own the underlying client-action and
match summary behavior. Evidence-ledger contracts own submitted-deck signal and
card-content provenance boundaries. The corpus parity report owns only the
coverage status claim that Mythic Edge has safe repo-owned evidence for a
sealed deckbuild coverage family.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence, evidence-ledger privacy
boundaries, and prior corpus audits, but it is not a Parser behavior module
and is not an analytics, AI, workbook, local app, deck-state, or production
module.

## Truth Owner

Truth owner for sealed deckbuild coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for parser behavior referenced by sealed deckbuild coverage:

- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`

Truth owner for submitted-deck provenance boundaries:

- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`

Truth boundary:

- `event_identity.classify_event_identity(...)` owns sealed event identity
  classification.
- `client_actions.try_parse(...)` owns `ClientMessageType_SubmitDeckResp`
  parsing, request context preservation, and normalized `deck_cards` /
  `sideboard_cards` payload fields.
- `state.py` owns applying submit-deck client actions to
  `MatchSummary.submit_deck_seen`.
- `models.py` owns model serialization for `submit_deck_seen` and existing
  row display values.
- Evidence-ledger contracts own the distinction between submit-deck signal
  evidence and submitted-deck card-content evidence.
- Corpus parity artifacts own the claim that Mythic Edge has safe corpus
  evidence for `core_gameplay.sealed_deckbuild`.
- The sealed deckbuild corpus claim is review metadata. It is not parser
  truth, decklist truth, sealed pool truth, card-choice truth, workbook truth,
  analytics truth, AI truth, coaching truth, merge readiness, deploy
  readiness, public-release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing sealed event identity and submit-deck client-action behavior
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for core_gameplay.sealed_deckbuild
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change event identity classification.
- Corpus metadata must not change submit-deck parsing, card-list normalization,
  parser state updates, model row shape, parser event classes, router
  semantics, workbook output, analytics, AI, coaching, or production behavior.
- Corpus metadata must not turn submitted-deck cards into sealed pool truth,
  decklist identity, card-choice quality, archetype classification, gameplay
  advice, or AI/coaching truth.

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
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_sealed_deckbuild_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_state.py`
- `tests/test_client_actions_parser.py`
- `docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md`

Files Codex C may inspect but must not change unless a focused test exposes a
contract mismatch that is routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- focused parser tests for client actions, event identity, app models, parser
  state, and corpus parity

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- parser event class changes
- router changes
- parser state final reconciliation changes
- submitted-deck runtime artifact changes
- GRP candidate scoring or card-name resolution changes
- golden replay fixtures
- feature-equity baselines
- committed raw log fixtures
- sealed pool fixture work
- decklist/deck-name/deck-ID fixture work
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public interface remains the existing corpus parity report API:

```python
def build_corpus_parity_report(
    manifest_path: Path,
    *,
    session_ledger_path: Path | None = None,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]:
    ...

def validate_session_ledger(payload: Mapping[str, Any]) -> list[str]:
    ...
```

The contracted report row is the existing `coverage_matrix` entry whose
`scenario_family` is `core_gameplay.sealed_deckbuild`.

No new public Python API is required.

No new CLI flag is required.

No new environment variable is authorized.

No workbook, webhook, Apps Script, runtime status, analytics, AI, or local app
surface is authorized.

## Observed Current Behavior

Observed from `codex/parser-parity` at
`369e2d5396f0fc9b42565f102a88e6ad498bedf7`:

- Issue #361 is open.
- Tracker #158 is open.
- Issue #359 is closed and PR #360 is merged into `codex/parser-parity`.
- The Mythic Edge corpus parity report is
  `partial_coverage_map_ready`.
- Report summary:
  - total scenario families: 45
  - covered committed: 6
  - covered synthetic: 4
  - covered report-only: 0
  - partial: 3
  - missing: 26
  - deferred: 0
  - blocked private evidence: 0
  - blocked external boundary: 6
  - not applicable: 0
- `core_gameplay.sealed_entry` is currently `covered_synthetic` through
  `sealed_entry_lifecycle_synthetic_v1`.
- `core_gameplay.sealed_matches` is currently `covered_synthetic` through
  `sealed_match_synthetic_v1`.
- `core_gameplay.sealed_deckbuild` is currently `missing` with
  `coverage_basis == ["external_reference_only"]`.

Observed parser behavior relevant to this slice:

- `event_identity.classify_event_identity(...)` recognizes event IDs
  containing sealed as limited sealed identity.
- `client_actions.try_parse(...)` recognizes
  `ClientMessageType_SubmitDeckResp` as specialized payload type
  `submit_deck_resp`.
- Specialized submit-deck payloads include `deck_cards`, `sideboard_cards`,
  `game_state_id`, `resp_id`, `request_id`, and `raw_client_action`.
- Submit-deck card-list normalization is parser-owned behavior, but this
  corpus slice must not store card-list values in the corpus manifest, session
  ledger, reports, or handoffs.
- `state.py` sets `MatchSummary.submit_deck_seen = True` when a specialized
  `submit_deck_resp` or generic `ClientMessageType_SubmitDeckResp` is observed
  for the current match.
- `models.py` exposes `submit_deck_seen` in debug, sheet, history, and match
  log surfaces.
- Existing evidence-ledger contracts distinguish `submit_deck_seen` from
  `submitted_deck_cards`. Empty or malformed submitted card lists can still
  support `submit_deck_seen`, but cannot support card-content truth.

## Required Guarantees

Codex C may implement the narrow V1 synthetic metadata and focused-test path.

The only authorized status promotion is:

| Scenario family | From | To |
| --- | --- | --- |
| `core_gameplay.sealed_deckbuild` | `missing` | `covered_synthetic` |

Codex C must preserve:

| Scenario family | Required status |
| --- | --- |
| `core_gameplay.sealed_entry` | `covered_synthetic` |
| `core_gameplay.sealed_matches` | `covered_synthetic` |

The V1 coverage claim must mean only:

- Mythic Edge has a committed synthetic metadata/session-ledger entry for
  sealed deckbuild coverage.
- The entry ties sealed event context to an existing parser-owned submit-deck
  signal and bounded submit-deck shape evidence.
- Focused tests verify the existing parser/state path for sealed context plus
  submit-deck signal behavior without changing parser behavior.
- The coverage is synthetic review metadata, not committed raw gameplay
  evidence.
- Corpus metadata and reports contain no submitted card-list values, deck
  names, sealed pool contents, card choices, or strategy notes.

The V1 coverage claim must not mean:

- sealed pool contents are known;
- submitted-deck card-content truth is committed in the corpus;
- a complete decklist, deck name, deck ID, or decklist identity is known;
- card choices, deckbuilding quality, sideboard quality, matchup plans,
  archetypes, gameplay advice, player mistakes, analytics truth, AI truth, or
  coaching truth are covered;
- Mythic Edge has full corpus parity with Manasight;
- parser behavior changed.

## Coverage Preconditions

`core_gameplay.sealed_deckbuild` may become `covered_synthetic` only when the
synthetic metadata and tests prove all of these ingredients:

1. Sealed context:
   - event ID or event identity evidence classifies the match as sealed.
2. Submit-deck/deckbuild signal:
   - `ClientMessageType_SubmitDeckResp` can be parsed as `submit_deck_resp`
     and/or consumed as a generic submit-deck client-action compatibility path.
3. Parser state signal:
   - parser state can set `MatchSummary.submit_deck_seen` for the current
     sealed-context match.
4. Privacy boundary:
   - corpus artifacts contain no raw submitted card lists, sealed pool
     contents, deck names, deck IDs, card choices, private strategy notes, raw
     log lines, or external corpus contents.
5. Non-claim boundary:
   - corpus notes explicitly state that sealed deckbuild coverage is bounded
     signal/shape metadata only.

Evidence that is not enough by itself:

- public Manasight sealed category labels;
- #357 sealed entry coverage;
- #359 sealed match coverage;
- sealed event ID classification alone;
- `ClientMessageType_SubmitDeckResp` parsing alone;
- raw submitted-deck card-list values;
- manual prose claiming sealed deckbuilding was observed.

## Inputs

### Corpus Manifest Entry

Type: JSON object inside `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.

Required V1 entry id:

```text
sealed_deckbuild_synthetic_v1
```

Required fields:

```yaml
entry_id: "sealed_deckbuild_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/361"
authorized_by_contract: "docs/contracts/parser_corpus_sealed_deckbuild_coverage.md"
scenario_families:
  - "core_gameplay.sealed_deckbuild"
parser_event_families:
  - "MatchState"
  - "ClientAction"
parser_claim_families:
  - "sealed_event_identity"
  - "sealed_submit_deck_signal"
  - "bounded_submit_deck_shape"
  - "deckbuild_privacy_boundary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

Allowed `paths` fields may reference only repo-owned metadata, tests, or docs.
Recommended paths:

```yaml
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  event_identity_test: "tests/test_event_identity.py"
  client_actions_test: "tests/test_client_actions_parser.py"
  state_summary_test: "tests/test_state.py"
  evidence_boundary_contract: "docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md"
```

The entry must include review notes or known gaps that say sealed deckbuild
coverage is bounded synthetic signal/shape evidence only and does not prove
sealed pool contents, submitted-deck card-content truth, decklists, deck names,
card choices, archetypes, gameplay advice, analytics truth, AI truth, or
coaching truth.

The manifest entry must not include:

- `deck_cards` values;
- `sideboard_cards` values;
- card names;
- GRP IDs;
- deck names;
- deck IDs;
- submitted-deck signatures derived from real or synthetic card values;
- sealed pool contents;
- raw payload snippets.

### Session Ledger Entry

Type: JSON object inside `tests/fixtures/parser_corpus/session_ledger.v1.json`.

Required V1 session id:

```text
sealed_deckbuild_synthetic_v1
```

Required fields:

```yaml
session_id: "sealed_deckbuild_synthetic_v1"
title: "Synthetic sealed deckbuild submit-deck signal evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/361"
authorized_by_contract: "docs/contracts/parser_corpus_sealed_deckbuild_coverage.md"
scenario_families:
  - "core_gameplay.sealed_deckbuild"
format_family: "limited_sealed"
match_shape: "sealed_deckbuild_submit_deck_signal_only"
record_summary: "synthetic_metadata_summary_only"
parser_coverage:
  event_families:
    MatchState: 1
    ClientAction: 1
  unknown_entries: 0
  truncation_count: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
```

The session ledger entry must include known gaps stating that this is synthetic
sealed deckbuild signal metadata only.

The session ledger entry must not include card-list, decklist, sealed pool,
deck-name, card-choice, or strategy-note values.

### Allowed Evidence Classes

- Repo-owned parser source and focused tests.
- Repo-owned corpus manifest and session ledger metadata.
- Synthetic metadata examples that contain no raw log lines and no card-list
  values.
- Focused synthetic test payloads in tests when they use fake IDs, fake teams,
  and no card names, deck names, sealed pool data, or strategy notes.
- Public Manasight taxonomy only as category-level reference context through
  prior audits.

### Forbidden Evidence Classes

- Manasight raw logs.
- `.log.gz` files.
- raw session payloads.
- compressed corpus files.
- hash lists, byte-size row lists, capture-date row lists, or mirrored
  external manifest rows.
- copied external parser source.
- private `Player.log` excerpts.
- private local logs.
- raw sealed pool data.
- raw submitted decklists.
- deck names, deck IDs, card choices, or private strategy notes.
- generated data.
- SQLite files.
- runtime artifacts.
- failed delivery artifacts.
- workbook exports.
- credentials, tokens, API keys, or webhook URLs.

## Outputs

### Corpus Parity Report Row

After Codex C implementation, the `core_gameplay.sealed_deckbuild` row should
be:

```yaml
scenario_family: "core_gameplay.sealed_deckbuild"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
mythic_edge_entries:
  - "sealed_deckbuild_synthetic_v1"
external_reference_status: "reference_category_not_checked"
```

Notes must include an explicit non-claim similar to:

```text
Synthetic sealed deckbuild coverage proves sealed context plus bounded submit-deck signal metadata only; it does not include submitted card lists, sealed pool contents, deck names, card choices, analytics truth, AI truth, or coaching truth.
```

The exact note wording may vary, but the non-claim must be present in either
the row notes or the entry review notes and covered by tests.

### Corpus Parity Summary

With the current 45-family taxonomy, adding this entry should update the
summary as follows:

```yaml
covered_committed: 6
covered_synthetic: 5
covered_report_only: 0
partial: 3
missing: 25
deferred: 0
blocked_private_evidence: 0
blocked_external_boundary: 6
not_applicable: 0
```

If the taxonomy changes before Codex C runs, Codex C must update only the
assertions that depend on total family counts and explain the change in the
handoff.

### Required Handoff Artifacts

Codex C must create:

- `docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md`

The comparison/handoff must summarize:

- observed pre-change corpus status;
- files changed;
- exact coverage status change;
- validation run;
- privacy non-claims for card/deck/pool data;
- residual risks;
- next recommended role.

## Unknowns

- Whether a future sealed deckbuild replay fixture should be sanitized
  log-based, fully synthetic log-based, local/private report-only, or remain
  metadata-only.
- Whether a future sealed pool evidence family should exist at all, given
  private strategic sensitivity.
- Whether submitted-deck signatures should ever be allowed in corpus parity
  metadata rather than evidence-ledger or local-private reports.

These unknowns do not block the sealed deckbuild V1 synthetic metadata path.

## Suspected Gaps

- Current corpus parity fixtures do not replay a sealed deckbuild log.
- This V1 entry will be metadata-level coverage, not a golden replay fixture.
- Existing parser tests cover submit-deck parsing and sealed match context
  separately; Codex C should add a focused parser/state test tying sealed
  context to `submit_deck_seen` while asserting card/deck values are not stored
  in corpus metadata.

## Invariants

- Only `core_gameplay.sealed_deckbuild` may move to `covered_synthetic`.
- `core_gameplay.sealed_entry` must remain `covered_synthetic`.
- `core_gameplay.sealed_matches` must remain `covered_synthetic`.
- Public Manasight metadata remains reference taxonomy only.
- Corpus coverage does not decide parser truth.
- Corpus coverage does not decide decklist truth.
- Corpus coverage does not decide sealed pool truth.
- Corpus coverage does not decide merge readiness, deploy readiness, tracker
  completion, public-release readiness, analytics truth, AI truth, or gameplay
  advice.
- Synthetic sealed deckbuild metadata must contain no raw log lines, private
  paths, external corpus contents, decklists, sealed pool contents, card
  choices, card IDs, card names, deck names, deck IDs, submitted-deck
  signatures, or strategy notes.
- Sealed event identity alone is not sealed deckbuild coverage.
- #357 sealed entry coverage alone is not sealed deckbuild coverage.
- #359 sealed match coverage alone is not sealed deckbuild coverage.
- SubmitDeckResp parsing alone is not sealed deckbuild coverage.
- Sealed deckbuild coverage requires the synthetic metadata entry to connect
  sealed context and a bounded submit-deck/deckbuild signal while preserving
  privacy non-claims.

## Error Behavior

Codex C must stop and route back to Codex B if:

- `core_gameplay.sealed_deckbuild` is missing from the taxonomy;
- current corpus validation fails before implementation;
- current sealed deckbuild status is already not `missing` and no intervening
  merged contract explains why;
- current sealed entry or sealed match status is not `covered_synthetic`;
- the manifest/session-ledger schemas reject the required synthetic entry
  shape;
- implementation requires parser behavior changes;
- implementation requires raw external or private log evidence;
- implementation requires card-list values in corpus metadata;
- implementation would touch protected downstream surfaces.

If a focused test reveals that existing parser behavior does not support the
claimed sealed-context submit-deck signal path, Codex C must not patch parser
behavior in this slice. It must record the blocker and route to Codex A or
Codex B for a smaller prerequisite.

## Side Effects

Allowed Codex C side effects:

- append one manifest entry to `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- append one session ledger entry to `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- update focused corpus parity tests for the new synthetic row and summary;
- add focused parser/state tests that prove existing sealed-context
  submit-deck signal behavior without changing parser code;
- write the required implementation handoff and contract test report.

Forbidden Codex C side effects:

- modifying parser source;
- modifying parser event classes;
- modifying router behavior;
- modifying parser state final reconciliation behavior;
- adding card-list values to corpus metadata;
- adding committed raw log fixtures;
- adding golden replay fixtures;
- adding feature-equity baseline changes;
- writing runtime status artifacts;
- updating workbook, webhook, Apps Script, Google Sheets, analytics, AI,
  coaching, local app, production, CI, merge, deploy, or final integration
  surfaces;
- closing tracker #158.

## Dependency Order

Codex C should work in this order:

1. Verify branch state includes PR #360 merge commit
   `369e2d5396f0fc9b42565f102a88e6ad498bedf7`.
2. Regenerate the corpus parity report from repo-owned inputs.
3. Confirm sealed entry and sealed matches are `covered_synthetic`, while
   sealed deckbuild is currently `missing`.
4. Add or update the focused parser/state test proving sealed context plus
   submit-deck signal behavior without parser code changes.
5. Add the single synthetic manifest entry.
6. Add the matching single synthetic session ledger entry.
7. Update focused corpus parity tests for the sealed deckbuild row, summary
   counts, and privacy non-claims.
8. Run validation and write the handoff/report artifacts.

## Compatibility

This slice must preserve:

- `SCENARIO_FAMILIES` ordering and values;
- `COVERAGE_STATUSES` vocabulary;
- corpus manifest schema version;
- session ledger schema version;
- corpus parity report schema version;
- current parser event classes;
- current event identity classifier behavior;
- current client-action parser behavior;
- current submit-deck payload shape;
- current parser state final reconciliation behavior;
- current `MatchSummary.submit_deck_seen` behavior;
- current workbook/webhook/App Script/output/local app behavior.

## Tests Required

Codex C should run:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

If Codex C changes additional files, it must include them in the path-scoped
privacy/protected-surface/selector checks.

Codex E should verify:

- only `core_gameplay.sealed_deckbuild` changed coverage status;
- sealed entry remains `covered_synthetic`;
- sealed matches remains `covered_synthetic`;
- the new entry is synthetic, committed, and privacy-safe;
- no external/raw/private log artifacts or deck contents were committed;
- no card-list, deck-name, sealed-pool, card-choice, or strategy-note values
  appear in corpus metadata or docs;
- parser behavior was not changed;
- focused tests prove existing sealed-context submit-deck signal behavior;
- corpus report notes preserve the privacy non-claims.

Codex F should stage only reviewed files.

Codex G must not close tracker #158 unless explicitly instructed by the user.

## Acceptance Criteria

- `docs/contracts/parser_corpus_sealed_deckbuild_coverage.md` exists.
- The contract names `core_gameplay.sealed_deckbuild` as the only authorized
  status promotion.
- The contract keeps `core_gameplay.sealed_entry` as `covered_synthetic`.
- The contract keeps `core_gameplay.sealed_matches` as `covered_synthetic`.
- The contract defines the exact synthetic manifest and session ledger entry
  IDs.
- The contract defines coverage preconditions involving sealed context plus
  bounded submit-deck/deckbuild signal evidence.
- The contract defines allowed and forbidden evidence classes.
- The contract requires no parser behavior changes.
- The contract forbids external/raw/private logs and card/deck/pool artifacts.
- The contract defines validation expectations and a Codex C handoff.

## Open Questions And Contract Risks

- The coverage is synthetic metadata coverage, not replayed sealed deckbuild
  log coverage.
- Future sealed pool or submitted-deck card-content corpus work would need a
  separate privacy-specific contract.
- Synthetic test payloads may use fake integer IDs to verify parser behavior,
  but corpus metadata must not preserve those values.
- The corpus parity report currently derives status from manifest/session
  entries, so non-claims must be visible in notes/tests rather than inferred
  by the report engine.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #361 under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/361

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Previous issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/359

  Previous PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/360

  Previous merge commit:
  369e2d5396f0fc9b42565f102a88e6ad498bedf7

  Branch:
  codex/parser-corpus-sealed-deckbuild-coverage

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_sealed_deckbuild_coverage.md

  Goal:
  Implement the narrow synthetic metadata/session-ledger slice for
  core_gameplay.sealed_deckbuild. Move only sealed deckbuild from missing to
  covered_synthetic by adding repo-owned synthetic corpus metadata and focused
  tests that tie sealed event context to existing parser-owned submit-deck
  signal behavior. Keep sealed entry and sealed matches covered_synthetic.

  Do:
    - Verify PR #360 is present in the local branch at or after merge commit
      369e2d5396f0fc9b42565f102a88e6ad498bedf7.
    - Regenerate the current corpus parity report from repo-owned inputs.
    - Confirm core_gameplay.sealed_entry and core_gameplay.sealed_matches are
      covered_synthetic and core_gameplay.sealed_deckbuild is currently
      missing before editing.
    - Add or update a focused parser/state test proving existing sealed-context
      submit-deck signal behavior without parser source changes.
    - Add exactly one synthetic manifest entry:
      sealed_deckbuild_synthetic_v1.
    - Add exactly one synthetic session ledger entry:
      sealed_deckbuild_synthetic_v1.
    - Update focused corpus parity tests so sealed deckbuild is
      covered_synthetic, sealed entry remains covered_synthetic, sealed matches
      remains covered_synthetic, and the summary counts reflect the one-family
      change.
    - Preserve explicit privacy non-claims in notes/tests.
    - Create docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md.
    - Create docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md.

  Do not:
    - Implement parser behavior changes.
    - Change event identity, client-action parsing, submit-deck parsing,
      card-list normalization, parser state, router, parser event classes,
      match/game identity, or deduplication behavior.
    - Add card-list values, deck names, deck IDs, sealed pool contents, card
      choices, submitted-deck signatures, or strategy notes to corpus metadata
      or docs.
    - Add committed raw log fixtures, golden replay fixtures, or feature-equity
      baseline changes.
    - Open a PR.
    - Close tracker #158 or issue #361.
    - Target main directly.
    - Import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw
      session payloads, compressed corpus files, hash lists, byte-size lists,
      capture-date row lists, parser source, or external corpus contents.
    - Commit private Player.log excerpts, private local logs, generated data,
      SQLite files, runtime artifacts, workbook exports, credentials, tokens,
      API keys, webhook URLs, sealed pool data, decklists, deck names, card
      choices, or private strategy notes.
    - Claim full Mythic Edge corpus parity, sealed pool support, decklist
      support, archetype classification, gameplay advice, AI truth, analytics
      truth, or coaching truth.
    - Change workbook schema, webhook payload shape, Apps Script behavior,
      Google Sheets sync, output transport, runtime status fields, analytics
      truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI
      gates, merge readiness, deploy readiness, production behavior, or final
      integration policy.

  Validation:
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py
    - python3 -m ruff check src tests tools
    - python3 tools/check_agent_docs.py
    - git diff --check
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_state.py docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/361"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/359"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/360"
  previous_merge_commit: "369e2d5396f0fc9b42565f102a88e6ad498bedf7"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_sealed_deckbuild_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_sealed_deckbuild_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_sealed_deckbuild_coverage.md"
  verdict: "contract_ready_for_synthetic_sealed_deckbuild_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-deckbuild-coverage"
  base_branch: "codex/parser-parity"
  base_commit: "369e2d5396f0fc9b42565f102a88e6ad498bedf7"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan against origin/codex/parser-parity"
    - "path-scoped protected-surface gate against origin/codex/parser-parity"
    - "validation selector against origin/codex/parser-parity"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not change event identity, client-action parsing, submit-deck parsing, card-list normalization, parser state, router, parser event classes, match/game identity, or deduplication behavior."
    - "Do not add card-list values, deck names, deck IDs, sealed pool contents, card choices, submitted-deck signatures, or strategy notes to corpus metadata or docs."
    - "Do not add committed raw log fixtures, golden replay fixtures, or feature-equity baseline changes."
    - "Do not open a PR."
    - "Do not close tracker #158 or issue #361."
    - "Do not target main directly."
    - "Do not import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, sealed pool data, decklists, deck names, card choices, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, sealed pool support, decklist support, archetype classification, gameplay advice, AI truth, analytics truth, or coaching truth."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status fields, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
```
