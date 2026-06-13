# Parser Corpus Sealed Lifecycle Coverage Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/355
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/352
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/354
- previous_merge_commit: `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- contract: `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`
- branch: `codex/parser-corpus-sealed-lifecycle-coverage`
- base_commit: `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- report_lifecycle: final_approval
- risk_tier: High
- reviewed_by_role: Codex E / Module Reviewer

## Source Snapshot

PR #354 is present in the local branch:

- local HEAD: `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`
- `dfaf7c54f0146b28fe746e24fbba3a53a5e49611` is an ancestor of `HEAD`
- #352 taxonomy audit report is present at
  `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`

The corpus parity report was regenerated from repo-owned inputs only:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Observed result:

- status: `partial_coverage_map_ready`
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 2
- covered_report_only: 0
- partial: 3
- missing: 28
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6
- not_applicable: 0

No Manasight logs, compressed corpus files, raw session payloads, external
manifest row details, private local logs, runtime artifacts, generated data, or
deck contents were imported or copied.

## Sealed Corpus Snapshot

The three in-scope sealed lifecycle rows remain missing:

| scenario_family | coverage_status | coverage_basis | mythic_edge_entries | external_reference_status |
| --- | --- | --- | --- | --- |
| `core_gameplay.sealed_entry` | `missing` | `external_reference_only` | none | `reference_category_not_checked` |
| `core_gameplay.sealed_deckbuild` | `missing` | `external_reference_only` | none | `reference_category_not_checked` |
| `core_gameplay.sealed_matches` | `missing` | `external_reference_only` | none | `reference_category_not_checked` |

The #352 taxonomy audit maps public sealed category labels to these rows, but
marks them `needs_parser_behavior_before_corpus_claim`. That mapping remains
reference taxonomy only and is not a Mythic Edge parser-support claim.

## Parser Behavior Inspection

Inspected repo-owned parser and model surfaces:

- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/decklists.py`
- focused tests for event identity, event lifecycle, client actions, parser
  package wiring, models, transforms, and corpus parity

Observed parser ingredients:

- `classify_event_identity(...)` classifies event IDs containing `sealed` as
  limited sealed identity. Focused tests assert `event_family == "sealed"`,
  `queue_subtype == "sealed"`, and `is_sealed_match is True` for a sealed
  event ID.
- `event_lifecycle.try_parse(...)` recognizes generic `EventJoin`,
  `EventEnterPairing`, and `EventClaimPrize` markers and preserves the raw
  lifecycle body. It does not extract sealed event context from lifecycle
  bodies.
- `match_state.try_parse(...)` extracts `event_id` from game-room config first
  and player entries as fallback. It emits match state payloads, but a generic
  match-state payload does not prove sealed entry, sealed deckbuilding, or
  sealed match coverage by itself.
- GRE GameState parsing preserves `gameInfo`, including `superFormat` and
  `matchWinCondition` when present, and parser state can ingest those fields
  into `MatchSummary`.
- `client_actions.try_parse(...)` recognizes
  `ClientMessageType_SubmitDeckResp` and normalizes `deck_cards` and
  `sideboard_cards`.
- Parser state records `submit_deck_seen` from specialized submit-deck events
  and generic `ClientMessageType_SubmitDeckResp` events.
- Submitted deck card lists are privacy-sensitive evidence. Current
  submit-deck support can support submit-deck observation, but it does not
  prove sealed deckbuilding, sealed pool contents, deck construction quality,
  or sealed lifecycle completion.

## Sealed Entry Assessment

Current ingredients:

- Sealed event identity can be classified from parser-produced event context.
- Generic event lifecycle markers are parsed.

Current gap:

- No Mythic Edge-owned committed fixture, session ledger entry, or local
  report summary ties sealed event context to entry lifecycle markers.

V1 decision:

- Keep `core_gameplay.sealed_entry` as `missing`.

Future acceptable path:

- A synthetic sealed entry lifecycle fixture or report-only local/private
  summary that proves sealed event context plus entry lifecycle marker handling
  through the normal parser route, without raw logs or deck contents.

Evidence not enough by itself:

- public Manasight sealed category labels;
- generic `EventJoin` without sealed context;
- sealed event identity classification without lifecycle markers;
- prose that says sealed entry happened.

## Sealed Deckbuild Assessment

Current ingredients:

- Submit-deck response parsing exists.
- State records submit-deck seen.
- Evidence-ledger contracts already treat submit-deck signal and submitted-card
  content as bounded, privacy-sensitive provenance.

Current gap:

- No Mythic Edge-owned evidence proves a sealed-context deckbuild lifecycle.
- No committed fixture or report summary safely ties sealed event context to
  submit-deck evidence.

V1 decision:

- Keep `core_gameplay.sealed_deckbuild` as `missing`.

Future acceptable path:

- A privacy-reviewed report-only sealed deckbuild summary that records
  sealed-context submit-deck signal metadata without raw card lists, or a
  synthetic fixture using fake integer IDs and explicit sealed context.

Evidence not enough by itself:

- `submit_deck_seen`;
- `ClientMessageType_SubmitDeckResp` card lists without sealed context;
- raw submitted deck contents;
- deck names, deck IDs, sealed pool contents, card ratings, or card choices;
- public Manasight sealed deckbuild labels.

## Sealed Matches Assessment

Current ingredients:

- Match state and GameState parsing can carry event ID, format, and
  match-win-condition context.
- `MatchSummary.event_identity()` can expose sealed identity when sealed
  context exists.
- Existing committed match fixtures prove narrow Standard match paths, not
  sealed match paths.

Current gap:

- No Mythic Edge-owned sealed match fixture, session ledger entry, or
  report-only summary exercises match state, GameState, game result, and final
  match summary in a sealed event context.

V1 decision:

- Keep `core_gameplay.sealed_matches` as `missing`.

Future acceptable path:

- A synthetic sealed match fixture that exercises the normal parser route with
  reduced expected facts and no private deck/card contents, or an approved
  local/private report-only sealed match summary with redacted source evidence.

Evidence not enough by itself:

- sealed event ID classification alone;
- generic match-state parsing without sealed context;
- public sealed category labels;
- generic limited or draft fixtures.

## Privacy And Protected-Surface Assertions

- No parser behavior changed.
- No parser state final reconciliation, parser event classes, router
  semantics, match/game identity, deduplication, workbook schema, webhook
  payload shape, Apps Script behavior, Google Sheets sync, output transport,
  runtime status artifacts, workbook exports, SQLite/local app behavior,
  analytics truth, AI truth, coaching behavior, OpenAI/model-provider
  behavior, CI gate, merge policy, deploy policy, or production behavior
  changed.
- No corpus manifest status or session ledger status changed.
- No committed log fixture was added.
- No external corpus file, compressed log file, raw session payload, private
  log, raw sealed pool, raw submitted decklist, generated data, credential,
  token, key, or webhook URL was committed.

## Explicit Non-Claims

- This report does not claim sealed lifecycle support.
- This report does not claim full Mythic Edge corpus parity.
- This report does not claim parser support from public taxonomy mapping.
- This report does not decide merge readiness, deploy readiness,
  public-release readiness, issue closure, tracker completion, analytics
  truth, AI truth, or gameplay advice.
- This report does not infer hidden cards, complete decklists, archetypes,
  gameplay advice, player mistakes, sealed pool contents, or card-choice
  quality.

## Recommended Next Child Path

Recommended next workflow route: Codex A or Codex B should split sealed
lifecycle into separate implementation-safe children before any corpus status
promotion.

Suggested order:

1. Sealed entry lifecycle fixture/report contract:
   - scope: sealed context plus event entry lifecycle markers;
   - likely artifact: synthetic committed fixture or report-only local/private
     summary;
   - status target after implementation: `core_gameplay.sealed_entry`.

2. Sealed match fixture contract:
   - scope: sealed context through match state, GameState, game result, and
     summary identity;
   - likely artifact: synthetic committed fixture with reduced expected facts;
   - status target after implementation: `core_gameplay.sealed_matches`.

3. Sealed deckbuild privacy contract:
   - scope: sealed-context submit-deck signal and bounded count/signature
     metadata;
   - likely artifact: report-only summary first, synthetic fixture only if
     fake IDs and privacy policy are explicit;
   - status target after implementation: `core_gameplay.sealed_deckbuild`.

Do not promote any of the three sealed rows until a future contract authorizes
owned evidence and status updates.

## Validation

Validation was run after creating this report and the implementation handoff.
See the companion handoff for command-by-command results:

- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

### Contract-Test Verdict

The report-only sealed lifecycle inspection satisfies
`docs/contracts/parser_corpus_sealed_lifecycle_coverage.md` and is ready for
Codex F: Module Submitter.

### Validation Reviewed

- Live issue check: issue #355 is open, tracker #158 is open, issue #352 is
  closed, and PR #354 is merged into `main`.
- Dependency check: local HEAD is
  `dfaf7c54f0146b28fe746e24fbba3a53a5e49611`, and the required merge commit is
  an ancestor of HEAD.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  -> `partial_coverage_map_ready`.
- Row inspection confirms `core_gameplay.sealed_entry`,
  `core_gameplay.sealed_deckbuild`, and `core_gameplay.sealed_matches` all
  remain `missing` with `coverage_basis == ["external_reference_only"]` and no
  Mythic Edge entries.
- `python3 -m pytest -q tests/test_corpus_parity_report.py` -> `7 passed`.
- `python3 -m pytest -q tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_client_actions_parser.py tests/test_parsers.py tests/test_app_models.py tests/test_transforms.py`
  -> `161 passed`.
- `python3 -m pytest -q tests` -> `1765 passed`.
- `python3 -m ruff check src tests tools` -> passed.
- `python3 tools/check_agent_docs.py` -> passed.
- `git diff --check` -> passed.
- Untracked docs whitespace scan with `git diff --no-index --check` printed no
  whitespace errors.
- Explicit path-scoped secret/private-marker scan over the contract, report,
  and handoff -> passed, `forbidden: 0`, `warnings: 0`.
- Explicit path-scoped protected-surface gate over the contract, report, and
  handoff -> passed, `forbidden: 0`, `warnings: 0`.
- Explicit path-scoped validation selector -> `selection_status: ok`.

### Confirmed Contract Matches

- V1 remains report-only and does not change corpus manifest/session ledger
  coverage statuses.
- The three sealed lifecycle rows stay `missing` and are not promoted to
  `covered_synthetic`, `covered_committed`, `covered_report_only`, or
  `partial`.
- Parser behavior is inspected as evidence context only; no parser behavior,
  parser tests, event classes, state reconciliation, router semantics, match or
  game identity, or deduplication behavior changed.
- The report explicitly avoids sealed support claims from public taxonomy
  mapping, event identity classification alone, generic lifecycle markers, or
  submit-deck signals without sealed context.
- The report keeps sealed deckbuild privacy boundaries explicit and rejects raw
  sealed pool data, raw submitted decklists, deck names, deck IDs, card
  ratings, and private card choices as V1 evidence.
- No external/raw/private log artifacts, Manasight corpus files, generated
  artifacts, SQLite files, workbook exports, credentials, tokens, keys, or
  webhook URLs were added.
- Future coverage promotion is routed to separate Codex A/B child issues.

### Contract Mismatches

None.

### Missing Tests

None blocking. The contract intentionally chose report-only V1 and authorized
no new fixtures, parser tests, manifest entries, or session ledger entries.
Focused corpus and parser-adjacent tests plus full pytest passed.

### Drift Classification

- Issue lifecycle: #355 and tracker #158 remain open as expected.
- Dependency lifecycle: #352 is closed and PR #354 is merged as expected.
- Local artifact drift: existing committed test fixture `.log` files are
  present in `tests/fixtures/`; no new sealed, external, private, generated, or
  runtime artifacts were added by this package.
- Protected surfaces: no parser, runtime, workbook, webhook, Apps Script,
  analytics, AI, local app, or production surfaces changed.

## Next Role

Codex F / Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/355"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/352"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/354"
  previous_merge_commit: "dfaf7c54f0146b28fe746e24fbba3a53a5e49611"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_sealed_lifecycle_coverage.md"
  target_artifact: "draft PR for report-only sealed lifecycle coverage inspection"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-lifecycle-coverage"
  base_commit: "dfaf7c54f0146b28fe746e24fbba3a53a5e49611"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json -> partial_coverage_map_ready"
    - "row inspection -> sealed_entry, sealed_deckbuild, and sealed_matches remain missing with external_reference_only"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py -> 7 passed"
    - "python3 -m pytest -q tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_client_actions_parser.py tests/test_parsers.py tests/test_app_models.py tests/test_transforms.py -> 161 passed"
    - "python3 -m pytest -q tests -> 1765 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "python3 tools/check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> passed"
    - "path-scoped protected-surface gate -> passed"
    - "path-scoped validation selector -> selection_status ok"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158 or issue #355."
    - "Do not implement parser behavior changes."
    - "Do not change corpus manifest or session ledger coverage statuses in V1."
    - "Do not add committed log fixtures in V1."
    - "Do not import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, raw sealed pool data, raw submitted decklists, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs."
    - "Do not claim full Mythic Edge corpus parity or sealed support from taxonomy mapping alone."
    - "Do not infer sealed deck contents, hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or AI/coaching truth."
```
