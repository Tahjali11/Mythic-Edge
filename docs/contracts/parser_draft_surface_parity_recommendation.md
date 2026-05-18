# Parser Draft Surface Parity Recommendation

## Metadata

- role: Codex B / Module Contract Writer / Contract Amendment Reviewer
- primary_issue: https://github.com/Tahjali11/Mythic-Edge/issues/122
- follow_up_issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/123
  - https://github.com/Tahjali11/Mythic-Edge/issues/124
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- branch: codex/parser-reliability-intelligence
- source_contract: docs/contracts/parser_draft_bot.md
- source_implementation_handoff: docs/implementation_handoffs/parser_draft_bot_comparison.md
- source_review_report: docs/contract_test_reports/parser_draft_bot.md
- status: docs-only recommendation
- risk_tier: High

Required agent docs:

- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

## Scope Reconciliation Addendum

This artifact resolves the Codex G blocker recorded on issue #122 and tracker
#47 on 2026-05-18.

Observed mismatch:

- The handoff expected a recommendation-only artifact at
  `docs/contracts/parser_draft_surface_parity_recommendation.md`.
- The integration branch instead already contains the reviewed DraftBot
  implementation package at commit
  `02df882538d607d32e43a5544422035ae8c25db1`.
- The recommendation artifact exists only as an untracked local file and is not
  part of the branch history.

Lifecycle decision:

1. Issue #122 should now be treated as the DraftBot implementation package, not
   as a recommendation-only artifact.
2. `docs/contracts/parser_draft_bot.md` is the authoritative contract for issue
   #122.
3. This recommendation should be submitted only as a docs-only scope
   reconciliation artifact. It does not supersede, amend, or replace the
   DraftBot contract or implementation package.
4. After this artifact is tracked, or after the same decision is posted as an
   issue comment and the untracked local file is intentionally discarded, issue
   #122 may route back to Codex G for closure under DraftBot-only scope.
5. Issues #123 and #124 remain the correct follow-up contract surfaces for
   DraftHuman and DraftComplete.
6. Draft golden replay, fixture, and corpus coverage remains a later follow-up
   and should not block #122 unless #122 claims full draft-surface parity.

## Decision

Do not amend `docs/contracts/parser_draft_bot.md` for issue #122.

Issue #122 should be reconciled as the DraftBot implementation package already
present on `codex/parser-reliability-intelligence`, with
`docs/contracts/parser_draft_bot.md` as its authoritative contract.

The existing DraftBot contract is correctly scoped to Quick Draft / bot draft
parser support. It explicitly keeps `DraftHuman` and `DraftComplete` out of
scope, defines focused false-positive requirements so DraftBot does not claim
human or complete markers, and treats golden/corpus fixture coverage as full
reliability evidence rather than a minimum blocker for the first DraftBot parser
pass.

Broader draft-surface parity should continue as follow-up contract work:

1. `docs/contracts/parser_draft_human.md` for issue #123.
2. `docs/contracts/parser_draft_complete.md` for issue #124.
3. A later fixture/corpus coverage contract after DraftBot, DraftHuman, and
   DraftComplete parser behavior is implemented and reviewed.

This recommendation should not block Codex G handling for issue #122 unless
the submitted #122 package claims full draft-surface parity, claims nonzero
golden/corpus draft coverage, or closes/deprioritizes #123/#124 without a
separate explicit decision.

Because this file is currently untracked, the immediate workflow step is Codex
F to submit this docs-only reconciliation artifact, unless the user explicitly
chooses to convert it into an issue comment and discard the local file instead.
After that cleanup, Codex G can resume #122 lifecycle handling.

## Current Evidence

Observed from the current branch and reviewed artifacts:

- `DraftBotEvent`, `DraftHumanEvent`, and `DraftCompleteEvent` already exist as
  stable event classes.
- `src/mythic_edge_parser/parsers/draft_bot.py` exists and handles only
  `BotDraftDraftStatus` and `BotDraftDraftPick`.
- Router dispatch includes `parsers.draft_bot` only; no `draft_human` or
  `draft_complete` parser module exists.
- `tests/test_draft_bot_parser.py` includes false-positive tests for
  `Draft.Notify`, `EventPlayerDraftMakePick`, `LogBusinessEvents`, `PickGrpId`,
  and `DraftCompleteDraft`.
- Schema payload snapshots include `DraftBot.bot_draft_status` and
  `DraftBot.bot_draft_pick`, but no `DraftHuman.*` or `DraftComplete.*`
  payload entries.
- Feature-equity corpus baseline still records zero counts for `DraftBot`,
  `DraftHuman`, and `DraftComplete`.
- Codex C and Codex E both record golden replay DraftBot fixture coverage and
  nonzero corpus DraftBot coverage as unverified residual risk, not completed
  parity.

## Coverage Matrix

| Surface | DraftBot / issue #122 | DraftHuman / issue #123 | DraftComplete / issue #124 | Recommendation |
| --- | --- | --- | --- | --- |
| Marker detection | Covered for `BotDraftDraftStatus` and `BotDraftDraftPick`. | Missing for `Draft.Notify`, `EventPlayerDraftMakePick`, and `LogBusinessEvents` with `PickGrpId`. | Missing for `DraftCompleteDraft`. | Keep #122 scoped. Contract #123 and #124 separately. |
| Stable event kind | Covered through existing `DraftBot` event kind. | Event class and `DraftHuman` kind exist, but no parser emits it. | Event class and `DraftComplete` kind exist, but no parser emits it. | Do not change event class names or kind values. |
| Stable payload type per family | Covered for `bot_draft_status` and `bot_draft_pick`. | Missing; #123 must define human draft payload types. | Missing; #124 must define completion payload types. | Define per-family payload type values in follow-up contracts. |
| Normalized card IDs as integers | Covered for DraftBot pack/pick card ids. | Missing; #123 must define pack cards and picked-card ID normalization. | Partial/not applicable; #124 may have completion metadata rather than pack card lists. | Reuse DraftBot numeric strictness unless evidence requires a narrower rule. |
| Pack/pick numbers | Covered for DraftBot. | Missing; #123 must define human draft pack/pick index rules. | Partial/not applicable; #124 should not invent pack/pick numbers unless completion evidence contains them. | Preserve observed values; do not convert zero/one-based indexes without evidence. |
| Draft/event identity when available | Covered for DraftBot alias set. | Missing; #123 must define human draft identity aliases. | Missing; #124 must define draft id, event id/name, queue/context fields. | Keep identity parser-owned and optional when absent. |
| Raw evidence preservation via `raw_*` | Covered as `raw_draft_bot`. | Missing; expected future field should likely be `raw_draft_human`. | Missing; expected future field should likely be `raw_draft_complete`. | Require full parsed top-level payload preservation in each follow-up. |
| False-positive separation | Covered in DraftBot tests for human and completion markers. | Missing; #123 must prove it does not claim bot or complete markers. | Missing; #124 must prove it does not claim bot or human markers. | Cross-family false-positive tests are mandatory. |
| Router/package expectations | Covered for `draft_bot` in Unity and UNKNOWN dispatch. | Missing for `draft_human`. | Missing for `draft_complete`. | Contract route order before implementation; avoid broad parser shadowing. |
| Schema snapshot updates | Covered for `DraftBot.*` payload keys. | Missing for `DraftHuman.*` payload keys. | Missing for `DraftComplete.*` payload keys. | Update only after focused tests define stable payload shapes. |
| Feature-equity corpus counts | Partial: baseline still has `DraftBot: 0`; this is documented. | Missing: baseline has `DraftHuman: 0`. | Missing: baseline has `DraftComplete: 0`. | Use a later fixture/corpus contract to add safe synthetic/sanitized draft fixtures. |
| Golden replay fixture evidence | Missing for all draft families. | Missing. | Missing. | Add only under explicit fixture/corpus contract; do not commit raw private logs. |
| Coaching/analytics boundary | Covered as out of scope. | Must be repeated. | Must be repeated. | Draft parser events are evidence, not advice. |

## Recommendation For Issue #122

Issue #122 should remain a DraftBot-only package.

Codex G may continue handling issue #122 if all of these are true:

- The submitted scope says DraftBot only.
- It does not claim full Manasight draft-surface parity.
- It does not claim DraftHuman or DraftComplete parser support.
- It does not claim nonzero golden/corpus draft coverage.
- It preserves the existing residual-risk language for live MTGA payload field
  names, DraftBot golden replay coverage, and nonzero DraftBot corpus evidence.
- It leaves issue #123 and issue #124 open for later contract work.

Recommended Codex G wording for #122 completion:

```text
Issue #122 completed the DraftBot parser slice only. DraftHuman (#123),
DraftComplete (#124), and draft golden/corpus fixture coverage remain open
follow-up scope. Feature-equity corpus draft counts remain zero until a safe
synthetic or sanitized draft fixture contract updates the baseline.
```

## Follow-Up Contracts Needed

### Issue #123: DraftHuman Parser

Recommended title:

```text
[parser-reliability] Contract DraftHuman parser support
```

Recommended contract artifact:

```text
docs/contracts/parser_draft_human.md
```

Scope:

- Recognize human draft markers:
  - `Draft.Notify`
  - `EventPlayerDraftMakePick`
  - `LogBusinessEvents` payloads with `PickGrpId`
- Emit existing `DraftHumanEvent` with stable payload types.
- Define normalized pack/pick card IDs as integers.
- Define pack/pick numbers and draft/event identity when available.
- Preserve raw parsed evidence, expected as `raw_draft_human`.
- Prove false positives against DraftBot and DraftComplete markers.
- Update parser payload schema snapshots only for `DraftHuman.*` keys.
- Keep workbook/webhook/App Script/state/final reconciliation out of scope.

### Issue #124: DraftComplete Parser

Recommended title:

```text
[parser-reliability] Contract DraftComplete parser support
```

Recommended contract artifact:

```text
docs/contracts/parser_draft_complete.md
```

Scope:

- Recognize draft completion marker:
  - `DraftCompleteDraft`
- Emit existing `DraftCompleteEvent` with stable payload types.
- Define normalized draft id, event id/name, completion source, and bot/human
  metadata when available.
- Preserve raw parsed evidence, expected as `raw_draft_complete`.
- Prove false positives against DraftBot and DraftHuman markers.
- Update parser payload schema snapshots only for `DraftComplete.*` keys.
- Keep workbook/webhook/App Script/state/final reconciliation out of scope.

### Later Fixture/Corpus Coverage

Recommended title:

```text
[parser-reliability] Add draft golden replay and feature-equity corpus coverage
```

Recommended timing:

- After DraftBot, DraftHuman, and DraftComplete parser implementations are
  reviewed, or after at least DraftBot is submitted if the user explicitly
  wants a DraftBot-only fixture pass first.

Recommended contract artifact:

```text
docs/contracts/parser_draft_fixture_corpus_coverage.md
```

Scope:

- Add small synthetic or sanitized draft fixture slices under the golden replay
  policy.
- Exercise draft parser events through the normal `LineBuffer` and `Router`
  path.
- Add expected golden replay manifest coverage for draft event families.
- Update count-only feature-equity corpus baseline with reviewed count changes.
- Preserve privacy, redaction, and no-raw-private-log guarantees.
- Avoid changing parser behavior, parser payload shapes, workbook schema,
  webhook payload shape, Apps Script behavior, runtime status files, failed
  posts, generated data, or production behavior.

## Validation Expectations

For this recommendation pass:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/parser_draft_surface_parity_recommendation.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
Select-String -Path docs\contracts\parser_draft_surface_parity_recommendation.md -Pattern '[ \t]+$'
```

For future DraftHuman / DraftComplete contract writer passes:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/parser_draft_human.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/parser_draft_complete.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

For future fixture/corpus coverage implementation:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_golden_replay_harness.py tests\test_feature_equity_corpus_ratchet.py
py -m mythic_edge_parser.app.golden_replay tests\fixtures\golden_replay
py -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests\fixtures\golden_replay --baseline tests\fixtures\feature_equity_corpus\feature_equity_corpus_baseline.v1.json
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/main
```

If a repo-approved secret/private-content scanner exists on the active branch,
run it against any new fixture, manifest, snapshot, baseline, and report
fixture paths.

## Protected Surfaces

This recommendation does not authorize changes to:

- parser behavior
- DraftHuman or DraftComplete implementation
- parser state final reconciliation
- parser event classes
- event kind values
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- runtime status files
- failed posts
- generated data
- workbook exports
- raw private logs
- secrets, credentials, tokens, webhook URLs, or environment variables
- CI gates
- production behavior
- draft coaching, card ratings, AI draft advice, or deck construction analytics

## Acceptance Criteria

This recommendation is complete when:

- The existing DraftBot contract is classified as sufficient for #122 only.
- Issue #122 is explicitly classified as the DraftBot implementation package,
  not as a recommendation-only artifact.
- `docs/contracts/parser_draft_bot.md` is identified as the authoritative
  contract for #122.
- The recommendation artifact is either submitted as a docs-only reconciliation
  artifact or intentionally converted into an issue comment and removed from the
  local worktree.
- Missing Manasight-exposed draft parser families are identified.
- Follow-up issue scopes for DraftHuman, DraftComplete, and draft
  fixture/corpus coverage are named.
- Codex G blocking guidance for #122 is explicit.
- Validation expectations and protected-surface boundaries are recorded.
- No code, parser behavior, snapshots, fixtures, corpus baselines, raw logs, or
  production surfaces are changed by this pass.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/122"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "F"
  next_role: "Codex F: Module Submitter for docs-only reconciliation artifact; then Codex G for issue #122 handling"
  source_artifact: "docs/contracts/parser_draft_bot.md; docs/implementation_handoffs/parser_draft_bot_comparison.md; docs/contract_test_reports/parser_draft_bot.md"
  target_artifact: "docs/contracts/parser_draft_surface_parity_recommendation.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  verdict: "issue #122 is the DraftBot package; parser_draft_bot.md remains authoritative; submit this file only as docs-only reconciliation; route broader draft parity to follow-up contracts"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/parser_draft_surface_parity_recommendation.md"
    - "trailing-whitespace scan for docs/contracts/parser_draft_surface_parity_recommendation.md"
  stop_conditions:
    - "Do not block #122 G handling after the recommendation artifact is tracked or intentionally converted to an issue comment."
    - "Do not add DraftHuman or DraftComplete behavior under #122."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, CI gates, or production behavior."
    - "Do not update fixtures, schema snapshots, or corpus baselines in this recommendation pass."
    - "Do not target main or mark #47/#11 complete."
```
