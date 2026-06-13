# Parser Corpus Manasight Taxonomy Audit

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/352
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- dependency_completed: https://github.com/Tahjali11/Mythic-Edge/issues/351
- dependency_pr: https://github.com/Tahjali11/Mythic-Edge/pull/353
- contract: docs/contracts/parser_corpus_manasight_taxonomy_audit.md
- branch: codex/manasight-corpus-taxonomy-audit
- base_commit: f91e38e7de421e52e44f2e6d9e693c40bbe7218b
- report_lifecycle: final_approval
- internal_project_area: Corpus / Provenance
- bridge_code_status: bridge_code
- generated_by_role: Codex C / Module Implementer
- reviewed_by_role: Codex E / Module Reviewer

## Source Snapshot

### Mythic Edge

The Mythic Edge corpus parity report was generated from repo-owned inputs:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

Current report status:

- status: partial_coverage_map_ready
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

The #351 dependency is present in this branch. The
`drift_debug.gsm_truncation` row is `covered_synthetic` with entries
`feature_equity_corpus_baseline_v1` and
`gsm_truncation_marker_synthetic_v1`.

### Public Manasight Metadata

Observed public reference:

- repository: https://github.com/manasight/manasight-corpus
- default_branch: main
- main commit observed: ea4d1a86c3711717b5ef9a354c7f9279598c43c3
- pushed_at: 2026-05-28T21:22:52Z
- description: sanitized MTG Arena game log files for parser smoke testing
- corpus_tag: manasight-corpus-v1
- public manifest metadata entries counted: 44
- public session heading count observed: 149

Public metadata sources used:

- README.md
- sessions.md
- smoke-corpus-manifest.toml
- repository tree path names as category hints only

No external corpus files, compressed log files, external raw session rows,
hash lists, byte-size lists, capture-date rows, parser source, or private local
artifacts were copied into this report.

## Non-Claims

- This report does not claim full Mythic Edge corpus parity with Manasight.
- This report does not claim parser support from Manasight category presence.
- This report does not change parser behavior, corpus schema, workbook schema,
  webhook shape, Apps Script behavior, analytics truth, AI truth, coaching
  behavior, CI gates, merge readiness, deploy readiness, public-release
  readiness, issue closure, or tracker completion.
- External metadata remains reference taxonomy only.

## Taxonomy Mapping

All rows use `privacy_boundary:
external_metadata_only_no_log_import`. Public examples are bounded category
labels only, not external corpus rows.

| manasight_category_id | manasight_category_label | metadata_sources | public_category_hints | mythic_edge_scenario_family | mythic_edge_current_coverage_status | mythic_edge_coverage_basis | comparison_status | dependency_notes | recommended_follow_up_issue_type | recommended_priority | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| corpus.manifest_metadata | Corpus manifest metadata | README.md; smoke-corpus-manifest.toml | corpus tag; manifest count | manifest.metadata | partial | count_ratchet_only | mapped_partial | Mythic Edge has count-ratchet metadata, but not a complete corpus manifest parity story. | codex_a_child_issue | Medium | Keep external manifest metadata bounded; do not mirror external rows. |
| corpus.session_ledger_metadata | Session ledger metadata | README.md; sessions.md | public session headings | session.ledger_metadata | covered_committed | fixture_metadata_only | mapped_covered | Mythic Edge has a committed session ledger scaffold. | none | Low | Covered as Mythic Edge metadata, not external session truth. |
| gameplay.standard_bo1 | Standard best-of-one | sessions.md; smoke-corpus-manifest.toml | Standard; Bo1 | core_gameplay.standard_bo1 | covered_committed | fixture_metadata_only; parser_behavior_verified | mapped_covered | Existing committed fixture covers this family narrowly. | none | Low | Coverage does not imply parity across all Standard variants. |
| gameplay.standard_bo3 | Standard best-of-three | sessions.md; smoke-corpus-manifest.toml | Standard; Bo3 | core_gameplay.standard_bo3 | covered_committed | fixture_metadata_only; parser_behavior_verified | mapped_covered | Existing committed fixture covers this family narrowly. | none | Low | Coverage does not imply all sideboard or reconnect variants. |
| gameplay.traditional_bo3 | Traditional best-of-three | sessions.md; smoke-corpus-manifest.toml | Traditional; Bo3 | core_gameplay.traditional_bo3 | covered_committed | fixture_metadata_only; parser_behavior_verified | mapped_covered | Shares current Mythic Edge Bo3 committed evidence. | none | Low | Keep distinct from future traditional-event edge cases. |
| gameplay.draft_only | Draft-only parser flow | sessions.md; smoke-corpus-manifest.toml | draft-only | core_gameplay.draft_only | covered_synthetic | fixture_metadata_only; parser_behavior_verified | mapped_covered | Current coverage is synthetic, not a real draft session corpus. | codex_a_child_issue | Medium | Future work should add broader limited-session evidence. |
| gameplay.draft_with_games | Draft session with games | sessions.md; smoke-corpus-manifest.toml | draft with game | core_gameplay.draft_with_games | missing | external_reference_only | mapped_missing | Needs Mythic Edge-owned sanitized or synthetic limited gameplay evidence. | codex_a_child_issue | High | Do not infer match support from draft-only fixture coverage. |
| gameplay.sealed_entry | Sealed entry | sessions.md; smoke-corpus-manifest.toml | sealed entry | core_gameplay.sealed_entry | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Requires Mythic Edge parser/fixture support review before coverage claim. | codex_a_child_issue | High | Candidate child issue for sealed lifecycle problem representation. |
| gameplay.sealed_deckbuild | Sealed deckbuilding | sessions.md; smoke-corpus-manifest.toml | sealed deckbuild | core_gameplay.sealed_deckbuild | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Requires Mythic Edge parser/fixture support review before coverage claim. | codex_a_child_issue | High | Keep deck contents out of committed audit artifacts. |
| gameplay.sealed_matches | Sealed matches | sessions.md; smoke-corpus-manifest.toml | sealed matches | core_gameplay.sealed_matches | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Requires Mythic Edge-owned match fixture evidence. | codex_a_child_issue | High | Do not import external sealed captures. |
| runtime.detailed_logs_disabled | Detailed logs disabled | sessions.md; smoke-corpus-manifest.toml | detailed logs disabled | log_runtime.detailed_logs_disabled | missing | external_reference_only | mapped_missing | Needs Mythic Edge local/synthetic diagnostic evidence. | codex_a_child_issue | High | Likely report-only or synthetic first; avoid private local logs. |
| runtime.log_rotation | Log rotation | sessions.md; smoke-corpus-manifest.toml | log rotation | log_runtime.rotation | blocked_external_boundary | external_reference_only | mapped_blocked_external_boundary | Current Mythic Edge row is external-reference-only. | codex_a_child_issue | High | Needs Mythic Edge-owned rotation fixture or report-only summary. |
| runtime.malformed_headerless | Malformed or headerless entries | sessions.md; README.md | malformed/headerless class | log_runtime.malformed_or_headerless | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs parser/buffer behavior review before corpus coverage. | codex_a_child_issue | Medium | Keep this separate from unknown-entry drift. |
| runtime.timestamp_anomaly | Timestamp anomalies | sessions.md | timestamp anomaly class | log_runtime.timestamp_anomaly | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs explicit parser/runtime evidence before coverage. | codex_a_child_issue | Medium | Do not fabricate timestamp edge cases from external metadata. |
| runtime.unknown_entry | Unknown entries | sessions.md | parser drift/debug headings | log_runtime.unknown_entry | missing | external_reference_only | mapped_missing | Needs Mythic Edge unknown-entry fixture/report coverage. | codex_a_child_issue | High | Good candidate for local report-only drift coverage. |
| connection.reconnect | Reconnect and connection health | sessions.md; smoke-corpus-manifest.toml | connection; reconnect | connection.reconnect | blocked_external_boundary | external_reference_only | mapped_blocked_external_boundary | Current Mythic Edge row is external-reference-only. | codex_a_child_issue | High | Needs Mythic Edge-owned reconnect evidence. |
| connection.disconnect | Disconnect | sessions.md; smoke-corpus-manifest.toml | disconnect/network class | connection.disconnect | missing | external_reference_only | mapped_missing | Needs Mythic Edge-owned disconnect evidence. | codex_a_child_issue | High | Keep network capture details out of committed report. |
| connection.firewall_network_drop | Firewall, Wi-Fi, or directional drop | sessions.md; smoke-corpus-manifest.toml | firewall; Wi-Fi; pfctl | connection.firewall_or_network_drop | missing | external_reference_only | mapped_missing | Needs local synthetic/report-only coverage plan. | codex_a_child_issue | High | May require approval-gated local-machine evidence later. |
| connection.error_payload | Connection error payloads | sessions.md | connection error class | connection.connection_error_payload | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs parser/diagnostics behavior review before coverage claim. | codex_a_child_issue | Medium | Do not infer payload shape from external summaries. |
| timer.active_player_timer | Active player timer | sessions.md | timer | timer.active_player_timer | missing | external_reference_only | mapped_missing | Needs Mythic Edge-owned timer evidence. | codex_a_child_issue | Medium | Keep separate from inactivity timeout. |
| timer.inactivity_timeout | Inactivity timeout | sessions.md; smoke-corpus-manifest.toml | inactivity | timer.inactivity_timeout | blocked_external_boundary | external_reference_only | mapped_blocked_external_boundary | Current Mythic Edge row is external-reference-only. | codex_a_child_issue | High | Needs owned fixture/report-only evidence before coverage claim. |
| timer.pre_match_idle | Pre-match idle/timer state | sessions.md | pre-match timer class | timer.pre_match_idle | missing | external_reference_only | mapped_missing | Needs Mythic Edge-owned timer-state evidence. | codex_a_child_issue | Medium | Could pair with timer normalization roadmap. |
| deck_api.start_hook_deck_snapshot | StartHook deck snapshot | README.md; sessions.md | deck snapshot class | deck_api.start_hook_deck_snapshot | missing | external_reference_only | mapped_missing | Needs Mythic Edge-owned deck API evidence. | codex_a_child_issue | Medium | Must not move deck truth into downstream reports. |
| deck_api.deck_summary | Deck summaries | sessions.md; smoke-corpus-manifest.toml | deck summaries | deck_api.deck_summary | missing | external_reference_only | mapped_missing | Needs owned deck summary fixture/report coverage. | codex_a_child_issue | Medium | Keep deck contents/private lists out of committed report. |
| deck_api.deck_upsert_event_set | Deck upsert and event-set deck | sessions.md | deck upsert; event set deck | deck_api.event_set_deck | covered_committed | fixture_metadata_only; parser_behavior_verified | mapped_covered | Event-set deck has narrow committed evidence; deck upsert remains separate missing family. | codex_a_child_issue | Medium | Follow-up should split `deck_api.deck_upsert` rather than overread event-set coverage. |
| deck_api.store_pack_inbox_crafting | Store, pack, inbox, or crafting surfaces | sessions.md; smoke-corpus-manifest.toml | store; pack; inbox; crafting | deck_api.store_pack_inbox_or_crafting | missing | external_reference_only | mapped_missing | Needs owned blind-spot coverage or explicit deferral. | codex_a_child_issue | Low | May be lower product priority than parser match reliability. |
| gameplay.mulligan_stress | Mulligan stress | sessions.md | mulligan | gameplay_stress.mulligan | covered_committed | fixture_metadata_only; parser_behavior_verified | mapped_covered | Current Bo3 fixture covers mulligan family narrowly. | none | Low | Does not prove all mulligan edge cases. |
| gameplay.opponent_auto_concede | Opponent auto-concede or no-action games | sessions.md | auto-concede | gameplay_stress.opponent_auto_concede | missing | external_reference_only | mapped_missing | Needs Mythic Edge-owned game-end edge fixture. | codex_a_child_issue | Medium | Useful parser final-reconciliation stress case. |
| gameplay.conjure | Conjure | sessions.md; smoke-corpus-manifest.toml | Conjure | gameplay_stress.conjure | blocked_external_boundary | external_reference_only | mapped_blocked_external_boundary | Current Mythic Edge row is external-reference-only. | codex_a_child_issue | Medium | Requires owned fixture; do not infer hidden or generated-card truth. |
| gameplay.spellbook | Spellbook | sessions.md; smoke-corpus-manifest.toml | Spellbook | gameplay_stress.spellbook | blocked_external_boundary | external_reference_only | mapped_blocked_external_boundary | Current Mythic Edge row is external-reference-only. | codex_a_child_issue | Medium | Requires owned fixture; do not infer hidden choices. |
| gameplay.companion_large_deck | Companion or large-deck shape | sessions.md | companion/large deck class | gameplay_stress.companion_or_large_deck | missing | external_reference_only | mapped_missing | Needs owned fixture/report coverage if product priority remains. | codex_a_child_issue | Low | Keep decklist identity out of parser corpus truth. |
| gameplay.action_attribution_event_ordering | Action attribution and event ordering | sessions.md | edge cases; debug | gameplay_stress.action_attribution | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs parser behavior and reduced expected facts before corpus claim. | codex_a_child_issue | High | Also map to `gameplay_stress.event_ordering`, currently missing. |
| drift.gsm_truncation | GSM truncation markers | sessions.md; smoke-corpus-manifest.toml | truncation | drift_debug.gsm_truncation | covered_synthetic | count_ratchet_only; diagnostics_only; fixture_metadata_only; parser_behavior_verified | mapped_covered | #351 added synthetic data-loss coverage. | none | Low | Truncation is data-loss evidence, not recovered game-state truth. |
| drift.recycle_rollback_limbo | Recycle, rollback, or limbo drift | sessions.md; smoke-corpus-manifest.toml | recycle; rollback; limbo | drift_debug.recycle_or_rollback | blocked_external_boundary | external_reference_only | mapped_blocked_external_boundary | Current Mythic Edge row is external-reference-only. | codex_a_child_issue | High | Needs owned parser-drift reproduction or report-only evidence. |
| drift.missing_message_type | Missing message type or parser type-field failures | sessions.md; smoke-corpus-manifest.toml | parser type field | drift_debug.missing_message_type | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs parser behavior/test clarification before coverage claim. | codex_a_child_issue | High | Keep separate from GSM truncation marker coverage. |
| drift.rename_recycle_collision | Rename/recycle collision | sessions.md; smoke-corpus-manifest.toml | rename collision | drift_debug.rename_or_rotation_collision | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs owned drift reproduction or synthetic reduced fixture. | codex_a_child_issue | High | Do not copy external collision cases. |
| drift.phantom_deck_origin | Phantom or deck-origin drift | sessions.md; smoke-corpus-manifest.toml | phantom; deck origin | drift_debug.phantom_or_deck_origin | missing | external_reference_only | needs_parser_behavior_before_corpus_claim | Needs owned parser behavior evidence before coverage claim. | codex_a_child_issue | High | Candidate for drift-focused problem representation. |

## Recommended Future #158 Child Issues

Suggested next child issues, in priority order:

1. Sealed lifecycle corpus coverage:
   - Covers `core_gameplay.sealed_entry`,
     `core_gameplay.sealed_deckbuild`, and `core_gameplay.sealed_matches`.
   - Start with Codex A because parser behavior support may need inspection
     before corpus metadata can be honest.

2. Connection and runtime interruption corpus coverage:
   - Covers `connection.reconnect`, `connection.disconnect`,
     `connection.firewall_or_network_drop`, `log_runtime.rotation`, and
     `timer.inactivity_timeout`.
   - Start with report-only or synthetic owned evidence; do not commit private
     machine captures.

3. Runtime parser resilience coverage:
   - Covers `log_runtime.detailed_logs_disabled`,
     `log_runtime.malformed_or_headerless`, `log_runtime.timestamp_anomaly`,
     and `log_runtime.unknown_entry`.
   - Start with Codex A/B to decide parser behavior versus corpus-only scope.

4. Drift regression corpus coverage:
   - Covers `drift_debug.recycle_or_rollback`,
     `drift_debug.missing_message_type`,
     `drift_debug.rename_or_rotation_collision`, and
     `drift_debug.phantom_or_deck_origin`.
   - Keep each child narrow enough to avoid reconstructing missing data.

5. Gameplay mechanics stress coverage:
   - Covers `gameplay_stress.conjure`, `gameplay_stress.spellbook`,
     `gameplay_stress.companion_or_large_deck`,
     `gameplay_stress.action_attribution`, and
     `gameplay_stress.event_ordering`.
   - Explicitly forbid hidden-card, generated-card, decklist, archetype, or
     coaching truth.

6. Deck API and economy blind-spot coverage:
   - Covers `deck_api.start_hook_deck_snapshot`,
     `deck_api.deck_summary`, `deck_api.deck_upsert`, and
     `deck_api.store_pack_inbox_or_crafting`.
   - Keep deck contents and private collection data out of committed artifacts.

7. Draft-with-games corpus coverage:
   - Covers `core_gameplay.draft_with_games`.
   - Build on current synthetic draft-only coverage without overclaiming
     limited-match coverage.

## Privacy And Protected-Surface Assertions

- No parser behavior changes were made.
- No parser event classes, router semantics, final reconciliation, match/game
  identity, deduplication, workbook schema, webhook payload shape, Apps Script
  behavior, Google Sheets sync, output transport, runtime status artifacts,
  failed delivery artifacts, workbook exports, SQLite/local app behavior,
  analytics truth, AI truth, coaching behavior, OpenAI/model-provider
  behavior, or production behavior were changed.
- No external corpus files, compressed log files, raw session rows, hash lists,
  byte-size lists, capture-date row lists, private logs, generated artifacts,
  credentials, tokens, keys, or webhook URLs were committed.
- Mapping rows are category-level planning evidence only.

## Residual Risks

- Manasight public metadata can change after this snapshot. Future reviewers
  should refresh the source snapshot if using this report for new issue
  planning.
- Some `missing` rows may reveal true parser behavior gaps. This report routes
  those to future Codex A/B work instead of implementing behavior.
- `mapped_covered` rows are narrow Mythic Edge coverage claims. They do not
  imply semantic parity with all public Manasight sessions in the same category.
- External-reference-only rows remain blocked until Mythic Edge creates owned,
  safe evidence.

## Codex E Contract-Test Addendum

### Findings

No blocking findings.

### Contract-Test Verdict

The metadata-only taxonomy audit satisfies
`docs/contracts/parser_corpus_manasight_taxonomy_audit.md` and is ready for
Codex F: Module Submitter.

### Validation Reviewed

- Live issue check: issue #352 is open, tracker #158 is open, and dependency
  PR #353 is merged into `main`.
- Live public metadata check: `manasight/manasight-corpus` still exposes
  `README.md`, `sessions.md`, `smoke-corpus-manifest.toml`, and `corpus/`;
  default branch is `main`; pushed timestamp is `2026-05-28T21:22:52Z`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  -> `partial_coverage_map_ready`.
- Row inspection confirms `drift_debug.gsm_truncation` is
  `covered_synthetic`, not provisional, with `mapped_covered` taxonomy audit
  status.
- `python3 -m pytest -q tests/test_corpus_parity_report.py` -> `7 passed`.
- `python3 -m pytest -q tests` -> `1765 passed`.
- `python3 -m ruff check src tests tools` -> passed.
- `python3 tools/check_agent_docs.py` -> passed.
- `git diff --check` -> passed.
- Untracked docs whitespace scan with `git diff --no-index --check` printed no
  whitespace errors.
- Explicit path-scoped secret/private-marker scan over the contract, audit, and
  handoff -> passed, `forbidden: 0`, `warnings: 0`.
- Explicit path-scoped protected-surface gate over the contract, audit, and
  handoff -> passed, `forbidden: 0`, `warnings: 0`.
- Explicit path-scoped validation selector -> `selection_status: ok`.

### Confirmed Contract Matches

- The audit is Markdown/report-only and does not add code, tests, fixtures,
  parser behavior, or runtime behavior.
- The audit maps public Manasight metadata to Mythic Edge corpus families as
  category-level planning evidence only.
- The report does not copy Manasight raw logs, compressed corpus files, raw
  session rows, hash lists, byte-size row lists, capture-date row lists, parser
  source, private logs, generated artifacts, credentials, tokens, keys, or
  webhook URLs.
- The audit does not claim full parity, parser support from category mapping,
  merge readiness, deploy readiness, public-release readiness, issue closure,
  or tracker completion.
- #351 is treated as merged and non-provisional; GSM truncation remains
  parser-owned data-loss evidence, not recovered GameState truth.
- Future behavior or fixture work is routed to future #158 Codex A/B child
  issues.

### Contract Mismatches

None.

### Missing Tests

None blocking. The contract allows Markdown-only V1; focused corpus parity
tests and full pytest passed. No optional Python helper or JSON validator was
added, so no new focused test file was required.

### Drift Classification

- Issue lifecycle: #352 and tracker #158 remain open as expected.
- Dependency lifecycle: #351 / PR #353 is merged as expected.
- External metadata: Manasight metadata may drift in the future; refresh before
  using this audit as the basis for new child issues.
- Protected surfaces: no parser, runtime, workbook, webhook, Apps Script,
  analytics, AI, local app, or production surfaces changed.

## Next Role

Codex F / Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/352"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  dependency_completed: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
  dependency_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/353"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md"
  target_artifact: "draft PR for metadata-only Manasight taxonomy audit"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/manasight-corpus-taxonomy-audit"
  base_commit: "f91e38e7de421e52e44f2e6d9e693c40bbe7218b"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json -> partial_coverage_map_ready"
    - "row inspection -> drift_debug.gsm_truncation covered_synthetic and mapped_covered"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py -> 7 passed"
    - "python3 -m pytest -q tests -> 1765 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "python3 tools/check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> passed"
    - "path-scoped protected-surface gate -> passed"
    - "path-scoped validation selector -> selection_status ok"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158 or issue #352."
    - "Do not import, copy, mirror, or commit Manasight raw logs, compressed corpus files, raw session payloads, hash lists, byte-size row lists, capture-date row lists, parser source, or external corpus contents."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status files, failed delivery artifacts, workbook exports, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, or production behavior."
    - "Do not claim full Mythic Edge corpus parity or tracker completion from this taxonomy audit."
```
