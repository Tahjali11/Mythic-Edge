# Parser Corpus Sealed Entry Lifecycle Coverage Contract

## Module

Sealed entry lifecycle corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge move exactly
`core_gameplay.sealed_entry` from missing coverage to safe synthetic metadata
coverage. It proves only that Mythic Edge has repo-owned corpus evidence tying
sealed event context to an event-entry lifecycle marker. It does not prove
sealed deckbuilding, sealed matches, sealed pool contents, deck contents, or
sealed gameplay support.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/357
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/355
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/356
- Previous merge commit: `e9802ae9f015ef36e5a44efd06dfd0f246e2912e`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-sealed-entry-lifecycle-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `e9802ae9f015ef36e5a44efd06dfd0f246e2912e`
- target_artifact:
  `docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md`
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
- `docs/implementation_handoffs/parser_corpus_sealed_lifecycle_coverage_comparison.md`
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/app/models.py`

External reference status:

- Public Manasight metadata may be used only through already merged taxonomy
  and sealed lifecycle audits or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, or external
  corpus contents.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the sealed entry scenario
family. Parser modules own parser behavior. The corpus parity report owns
coverage status claims. External taxonomy explains why a scenario matters, but
it does not prove Mythic Edge coverage.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and prior corpus audits, but it is
not a Parser behavior module and is not an analytics, AI, workbook, local app,
or production module.

## Truth Owner

Truth owner for sealed entry coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for sealed parser behavior:

- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/models.py`

Truth boundary:

- `event_identity.classify_event_identity(...)` owns sealed event identity
  classification.
- `event_lifecycle.try_parse(...)` owns generic `EventJoin` lifecycle marker
  parsing and raw body preservation.
- `match_state.try_parse(...)` owns match-state event ID extraction.
- Corpus parity artifacts own the claim that Mythic Edge has safe corpus
  evidence for `core_gameplay.sealed_entry`.
- The sealed entry corpus claim is review metadata. It is not parser truth,
  match truth, game truth, deck-state truth, workbook truth, analytics truth,
  AI truth, coaching truth, merge readiness, deploy readiness, public-release
  readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing sealed event identity and generic EventJoin parser behavior
  -> synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for core_gameplay.sealed_entry
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change event identity classification.
- Corpus metadata must not change event lifecycle parser output.
- Corpus metadata must not change match state parsing, parser state final
  reconciliation, parser event classes, router semantics, workbook output,
  analytics, AI, coaching, or production behavior.

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

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md`

Files Codex C may inspect but must not change unless the focused tests expose a
contract mismatch that is routed back for clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/app/models.py`
- focused parser tests for event identity, event lifecycle, match state, app
  models, and corpus parity

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- parser event class changes
- golden replay fixtures
- feature-equity baselines
- committed raw log fixtures
- sealed deckbuild fixture work
- sealed match fixture work
- submitted-deck card-content fixture work
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, and production surfaces

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
`scenario_family` is `core_gameplay.sealed_entry`.

No new public Python API is required.

No new CLI flag is required.

No new environment variable is authorized.

## Observed Current Behavior

Observed from `codex/parser-parity` at
`e9802ae9f015ef36e5a44efd06dfd0f246e2912e`:

- Issue #357 is open.
- Tracker #158 is open.
- Issue #355 is closed and PR #356 is merged.
- The Mythic Edge corpus parity report is
  `partial_coverage_map_ready`.
- Report summary:
  - total scenario families: 45
  - covered committed: 6
  - covered synthetic: 2
  - covered report-only: 0
  - partial: 3
  - missing: 28
  - deferred: 0
  - blocked private evidence: 0
  - blocked external boundary: 6
  - not applicable: 0
- `core_gameplay.sealed_entry`, `core_gameplay.sealed_deckbuild`, and
  `core_gameplay.sealed_matches` are all currently `missing` with
  `coverage_basis == ["external_reference_only"]` and no Mythic Edge entries.
- The sealed lifecycle V1 report recommended splitting sealed entry from sealed
  deckbuilding and sealed matches before any corpus status promotion.

Observed parser behavior relevant to this slice:

- `event_identity.classify_event_identity(...)` recognizes event IDs
  containing sealed as limited sealed identity. Focused tests assert sealed
  family and sealed subtype behavior for a sealed event ID.
- `event_lifecycle.try_parse(...)` recognizes generic `EventJoin`,
  `EventEnterPairing`, and `EventClaimPrize` markers and preserves the raw
  lifecycle body. It does not extract sealed-specific fields from lifecycle
  bodies.
- `match_state.try_parse(...)` extracts `event_id` from match room config or
  player entries and emits match state payloads.
- Current corpus parity data does not yet tie sealed event context and
  `EventJoin` marker evidence together in an owned entry.

## Required Guarantees

Codex C may implement the narrow V1 synthetic metadata path.

The only authorized status promotion is:

| Scenario family | From | To |
| --- | --- | --- |
| `core_gameplay.sealed_entry` | `missing` | `covered_synthetic` |

Codex C must keep these scenario families `missing`:

- `core_gameplay.sealed_deckbuild`
- `core_gameplay.sealed_matches`

The V1 coverage claim must mean only:

- Mythic Edge has a committed synthetic metadata/session-ledger entry for
  sealed entry lifecycle coverage.
- The entry ties sealed event context to generic event-entry lifecycle marker
  handling through existing parser-owned behavior and tests.
- The coverage is synthetic review metadata, not committed raw gameplay
  evidence.

The V1 coverage claim must not mean:

- sealed matches are covered;
- sealed deckbuilding is covered;
- sealed pool contents are covered;
- submitted-deck card contents are covered;
- deck names, deck IDs, card choices, sideboarding quality, archetypes,
  matchup plans, gameplay advice, player mistakes, or AI/coaching truth are
  covered;
- Mythic Edge has full corpus parity with Manasight;
- parser behavior changed.

## Inputs

### Corpus Manifest Entry

Type: JSON object inside `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.

Required V1 entry id:

```text
sealed_entry_lifecycle_synthetic_v1
```

Required fields:

```yaml
entry_id: "sealed_entry_lifecycle_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/357"
authorized_by_contract: "docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md"
scenario_families:
  - "core_gameplay.sealed_entry"
parser_event_families:
  - "MatchState"
  - "EventLifecycle"
parser_claim_families:
  - "sealed_event_identity"
  - "event_lifecycle"
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
  event_lifecycle_test: "tests/test_parser_small_modules.py"
  match_state_test: "tests/test_parsers.py"
```

The entry must include review notes or known gaps that say sealed entry
coverage does not prove sealed deckbuilding, sealed matches, sealed pool
contents, submitted-deck contents, or full sealed lifecycle support.

### Session Ledger Entry

Type: JSON object inside `tests/fixtures/parser_corpus/session_ledger.v1.json`.

Required V1 session id:

```text
sealed_entry_lifecycle_synthetic_v1
```

Required fields:

```yaml
session_id: "sealed_entry_lifecycle_synthetic_v1"
title: "Synthetic sealed entry lifecycle evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/357"
authorized_by_contract: "docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md"
scenario_families:
  - "core_gameplay.sealed_entry"
format_family: "limited_sealed"
match_shape: "sealed_entry_only"
record_summary: "synthetic_metadata_summary_only"
parser_coverage:
  event_families:
    MatchState: 1
    EventLifecycle: 1
  unknown_entries: 0
  truncation_count: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  external_logs_included: false
  decklists_included: false
```

The session ledger entry must include known gaps stating that this is synthetic
sealed entry metadata only.

### Allowed Evidence Classes

- Repo-owned parser source and focused tests.
- Repo-owned corpus manifest and session ledger metadata.
- Synthetic metadata examples that contain no raw log lines.
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

After Codex C implementation, the `core_gameplay.sealed_entry` row should be:

```yaml
scenario_family: "core_gameplay.sealed_entry"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
mythic_edge_entries:
  - "sealed_entry_lifecycle_synthetic_v1"
external_reference_status: "reference_category_not_checked"
```

Notes must include an explicit non-claim similar to:

```text
Synthetic sealed entry coverage proves sealed context plus event-entry lifecycle metadata only; sealed deckbuild and sealed matches remain missing.
```

The exact note wording may vary, but the non-claim must be present in either
the row notes or the entry review notes and covered by tests.

### Corpus Parity Summary

With the current 45-family taxonomy, adding this entry should update the
summary as follows:

```yaml
covered_committed: 6
covered_synthetic: 3
covered_report_only: 0
partial: 3
missing: 27
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

- `docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md`

The comparison/handoff must summarize:

- observed pre-change corpus status;
- files changed;
- exact coverage status change;
- validation run;
- non-claims for sealed deckbuilding and sealed matches;
- residual risks;
- next recommended role.

## Unknowns

- Whether a later sealed deckbuild child should use synthetic metadata only,
  sanitized owned fixture snippets, or local/private report-only summaries.
- Whether sealed matches require a synthetic committed replay fixture or a
  narrower event identity and match-state metadata entry first.
- Whether future Manasight taxonomy changes will split sealed entry into more
  granular categories.

These unknowns do not block the sealed entry V1 synthetic metadata path.

## Suspected Gaps

- Current corpus parity fixtures do not exercise sealed event context plus
  event-entry lifecycle as a committed parser replay.
- Event lifecycle parsing is generic. It preserves raw lifecycle body but does
  not produce sealed-specific event lifecycle fields.
- The sealed entry coverage claim will remain metadata-level until a future
  contract authorizes committed sanitized or synthetic log/replay fixtures.

## Invariants

- Only `core_gameplay.sealed_entry` may move to `covered_synthetic`.
- `core_gameplay.sealed_deckbuild` must remain `missing`.
- `core_gameplay.sealed_matches` must remain `missing`.
- Public Manasight metadata remains reference taxonomy only.
- Corpus coverage does not decide parser truth.
- Corpus coverage does not decide match/game truth.
- Corpus coverage does not decide merge readiness, deploy readiness, tracker
  completion, public-release readiness, analytics truth, AI truth, or gameplay
  advice.
- Synthetic sealed entry metadata must contain no raw log lines, private paths,
  external corpus contents, decklists, sealed pool contents, or strategy notes.
- Event identity classification alone is not sealed entry coverage.
- Generic `EventJoin` parsing alone is not sealed entry coverage.
- Sealed entry coverage requires the synthetic metadata entry to connect sealed
  context and event-entry lifecycle evidence.

## Error Behavior

Codex C must stop and route back to Codex B if:

- `core_gameplay.sealed_entry` is missing from the taxonomy;
- current corpus validation fails before implementation;
- current sealed entry status is already not `missing` and no intervening
  merged contract explains why;
- the manifest/session-ledger schemas reject the required synthetic entry
  shape;
- implementation requires parser behavior changes;
- implementation requires raw external or private log evidence;
- implementation would change sealed deckbuild or sealed match status;
- implementation would touch protected downstream surfaces.

If a focused test reveals that existing parser behavior does not support the
claimed sealed context or event-entry marker evidence, Codex C must not patch
parser behavior in this slice. It must record the blocker and route to Codex A
or Codex B for a smaller prerequisite.

## Side Effects

Allowed Codex C side effects:

- append one manifest entry to `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- append one session ledger entry to `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- update focused corpus parity tests for the new synthetic row and summary;
- write the required implementation handoff and contract test report.

Forbidden Codex C side effects:

- modifying parser source;
- modifying parser event classes;
- modifying router behavior;
- changing sealed deckbuild or sealed match corpus statuses;
- adding committed raw log fixtures;
- adding golden replay fixtures;
- adding feature-equity baseline changes;
- writing runtime status artifacts;
- updating workbook, webhook, Apps Script, Google Sheets, analytics, AI,
  coaching, local app, production, CI, merge, or deploy surfaces;
- closing tracker #158.

## Dependency Order

Codex C should work in this order:

1. Verify branch state includes PR #356 merge commit
   `e9802ae9f015ef36e5a44efd06dfd0f246e2912e`.
2. Regenerate the corpus parity report from repo-owned inputs.
3. Confirm sealed entry, sealed deckbuild, and sealed matches are currently
   `missing`.
4. Add the single synthetic manifest entry.
5. Add the matching single synthetic session ledger entry.
6. Update focused corpus parity tests for the sealed entry row, summary counts,
   and sealed deckbuild/match non-claims.
7. Run validation and write the handoff/report artifacts.

## Compatibility

This slice must preserve:

- `SCENARIO_FAMILIES` ordering and values;
- `COVERAGE_STATUSES` vocabulary;
- corpus manifest schema version;
- session ledger schema version;
- corpus parity report schema version;
- current parser event classes;
- current event identity classifier behavior;
- current event lifecycle parser behavior;
- current match state parser behavior;
- current workbook/webhook/App Script/output/local app behavior.

## Tests Required

Codex C should run:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_parsers.py
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

If Codex C changes additional files, it must include them in the path-scoped
privacy/protected-surface/selector checks.

Codex E should verify:

- only `core_gameplay.sealed_entry` changed coverage status;
- sealed deckbuild and sealed matches remain `missing`;
- the new entry is synthetic, committed, and privacy-safe;
- no external/raw/private log artifacts or deck contents were committed;
- parser behavior was not changed;
- corpus report notes preserve the non-claims.

Codex F should stage only reviewed files.

Codex G must not close tracker #158 unless explicitly instructed by the user.

## Acceptance Criteria

- `docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md` exists.
- The contract names `core_gameplay.sealed_entry` as the only authorized status
  promotion.
- The contract keeps `core_gameplay.sealed_deckbuild` and
  `core_gameplay.sealed_matches` missing.
- The contract defines the exact synthetic manifest and session ledger entry
  IDs.
- The contract defines allowed and forbidden evidence classes.
- The contract requires no parser behavior changes.
- The contract forbids external/raw/private logs and deck-content artifacts.
- The contract defines validation expectations and a Codex C handoff.

## Open Questions And Contract Risks

- The coverage is synthetic metadata coverage, not replayed sealed entry log
  coverage.
- Future sealed match and sealed deckbuild work will need separate contracts
  and may need stronger fixture/privacy policy.
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

  Act as Codex C: Module Implementer for issue #357 under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/357

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Previous issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/355

  Previous PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/356

  Previous merge commit:
  e9802ae9f015ef36e5a44efd06dfd0f246e2912e

  Branch:
  codex/parser-corpus-sealed-entry-lifecycle-coverage

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md

  Goal:
  Implement the narrow synthetic metadata/session-ledger slice for
  core_gameplay.sealed_entry. Move only sealed entry from missing to
  covered_synthetic by adding repo-owned synthetic corpus metadata that ties
  sealed event context to event-entry lifecycle evidence. Keep sealed deckbuild
  and sealed matches missing.

  Do:
    - Verify PR #356 is present in the local branch at or after merge commit
      e9802ae9f015ef36e5a44efd06dfd0f246e2912e.
    - Regenerate the current corpus parity report from repo-owned inputs.
    - Confirm core_gameplay.sealed_entry, core_gameplay.sealed_deckbuild, and
      core_gameplay.sealed_matches are currently missing before editing.
    - Add exactly one synthetic manifest entry:
      sealed_entry_lifecycle_synthetic_v1.
    - Add exactly one synthetic session ledger entry:
      sealed_entry_lifecycle_synthetic_v1.
    - Update focused corpus parity tests so sealed entry is covered_synthetic,
      sealed deckbuild remains missing, sealed matches remain missing, and the
      summary counts reflect the one-family change.
    - Preserve explicit non-claims in notes/tests.
    - Create docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md.
    - Create docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md.

  Do not:
    - Implement parser behavior changes.
    - Change event identity, event lifecycle, match state, parser state, router,
      parser event classes, match/game identity, or deduplication behavior.
    - Change sealed deckbuild or sealed match corpus status.
    - Add committed raw log fixtures, golden replay fixtures, or feature-equity
      baseline changes.
    - Open a PR.
    - Close tracker #158 or issue #357.
    - Import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw
      session payloads, compressed corpus files, hash lists, byte-size lists,
      capture-date row lists, parser source, or external corpus contents.
    - Commit private Player.log excerpts, private local logs, generated data,
      SQLite files, runtime artifacts, workbook exports, credentials, tokens,
      API keys, webhook URLs, sealed pool data, decklists, deck names, card
      choices, or private strategy notes.
    - Claim full Mythic Edge corpus parity, sealed match support, or sealed
      deckbuild support.
    - Change workbook schema, webhook payload shape, Apps Script behavior,
      Google Sheets sync, output transport, analytics truth, AI truth, coaching
      behavior, OpenAI/model-provider behavior, CI gates, merge readiness,
      deploy readiness, or production behavior.

  Validation:
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_parsers.py
    - python3 tools/check_agent_docs.py
    - git diff --check
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
    - printf '%s\n' tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/357"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/355"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/356"
  previous_merge_commit: "e9802ae9f015ef36e5a44efd06dfd0f246e2912e"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_sealed_entry_lifecycle_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_sealed_entry_lifecycle_coverage.md"
  verdict: "contract_ready_for_synthetic_sealed_entry_lifecycle_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-sealed-entry-lifecycle-coverage"
  base_branch: "codex/parser-parity"
  base_commit: "e9802ae9f015ef36e5a44efd06dfd0f246e2912e"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_event_identity.py tests/test_parser_small_modules.py tests/test_parsers.py"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan against origin/codex/parser-parity"
    - "path-scoped protected-surface gate against origin/codex/parser-parity"
    - "validation selector against origin/codex/parser-parity"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not change event identity, event lifecycle, match state, parser state, router, parser event classes, match/game identity, or deduplication behavior."
    - "Do not change sealed deckbuild or sealed match corpus status."
    - "Do not add committed raw log fixtures, golden replay fixtures, or feature-equity baseline changes."
    - "Do not open a PR."
    - "Do not close tracker #158 or issue #357."
    - "Do not import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw session payloads, compressed corpus files, hash lists, byte-size lists, capture-date row lists, parser source, or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, sealed pool data, decklists, deck names, card choices, or private strategy notes."
    - "Do not claim full Mythic Edge corpus parity, sealed match support, or sealed deckbuild support."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge readiness, deploy readiness, or production behavior."
```
