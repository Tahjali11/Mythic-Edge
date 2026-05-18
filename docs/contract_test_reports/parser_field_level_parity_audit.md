# Parser Field-Level Parity Audit Contract-Test Report

## Findings

No blocking findings.

### Non-blocking: submitter routing must avoid an accidental PR to `main`

The reviewed issue #121 package is currently on
`codex/parser-reliability-intelligence`, which the issue identifies as the
current integration branch. No open pull request exists for the branch at
review time. Codex F should stage, commit, and push only the reviewed issue
#121 docs. It must not open a PR to `main`; if a draft PR is required, Codex F
should stop and ask for the approved non-main base branch.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/121

## Trackers

- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/parser_field_level_parity_audit.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Reviewed artifacts:

- `docs/contracts/parser_field_level_parity_audit.md`
- `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`

No parser source, tests, fixtures, snapshots, corpus baselines, workbook,
webhook, Apps Script, runtime, secret, or production files were changed by the
issue #121 package under review.

## Contract Summary

Issue #121 is a docs-only field-level parity audit. The contract asks Codex C to
compare existing parser surfaces against the field-level parity standard, label
parser-owned normalized fields versus raw-evidence fields, record test/schema/
golden/corpus evidence, preserve unknowns and suspected gaps, and recommend
follow-up issues without changing behavior.

## Checks Run

```powershell
git fetch --prune origin
gh issue view 121 --json number,title,state,url,body,labels
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence
git diff --check
@'
docs/contracts/parser_field_level_parity_audit.md
docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_gre_connect_resp_parser.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_small_modules.py
py -m pytest -q tests\test_client_actions_parser.py tests\test_match_state_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py
py -m pytest -q tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py
py -m pytest -q
py -m ruff check src tests tools
py tools\check_protected_surfaces.py --base origin/main
gh pr list --head codex/parser-reliability-intelligence --json number,title,state,isDraft,baseRefName,headRefName,url
```

## Results

- Issue #121 is open.
- Branch is `codex/parser-reliability-intelligence`.
- Branch is even with `origin/codex/parser-reliability-intelligence`: `0 0`.
- Working tree before this report contained only two untracked issue #121 docs:
  - `docs/contracts/parser_field_level_parity_audit.md`
  - `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`
- `git diff --check`: passed.
- Path-scoped protected-surface gate for the issue #121 contract and handoff:
  `changed_paths: 2`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Schema snapshot tests: `6 passed in 0.59s`.
- ConnectResp / connection / collection / small parser slice:
  `66 passed in 0.59s`.
- ClientAction / MatchState / GameState / GameResult slice:
  `96 passed in 0.60s`.
- Feature-equity corpus ratchet / golden replay slice:
  `19 passed in 0.97s`.
- Full local suite: `743 passed in 4.92s`.
- Ruff: `All checks passed!`.
- Branch-wide protected-surface gate against `origin/main`: passed with
  `forbidden: 0` and 9 warnings from earlier parser reliability branch work
  outside issue #121.
- No open PR exists with head `codex/parser-reliability-intelligence`.

## Confirmed Contract Matches

- The comparison is docs-only, as required by the contract.
- The comparison covers every required family:
  ConnectResp, EventLifecycle, Session, Rank, Collection, DeckCollection,
  Inventory, MatchConnectionState, TcpConnectionClose, WebSocketClosed,
  ConnectionError, MatchState, ClientAction, limited GameState overlap, and
  limited GameResult overlap.
- The matrix uses only contract-approved status labels:
  `verified`, `documented_partial`, and `raw_preserved_only`.
- Parser-owned normalized fields and raw-evidence fields are separated per
  family.
- The connection payload gaps are not hidden: the handoff names missing
  explicit `type` and `raw_*` wrappers for relevant connection families as
  future-contract work.
- The comparison correctly treats zero feature-equity corpus coverage as a
  coverage gap, not as a parser behavior bug.
- The comparison preserves parser truth ownership: workbook, webhook, Apps
  Script, dashboards, diagnostics, corpus reports, and AI are not promoted to
  parser truth.
- The comparison routes broader GameState normalization to future backlog work
  and records that
  `docs/problem_representations/game_state_normalization_backlog.md` is absent
  on this branch.
- Recommended follow-ups are framed as future issues/contracts, not as
  authorization for Codex C to change parser behavior.
- No tests, fixtures, schema snapshots, corpus baselines, parser payloads, event
  classes, workbook/webhook/App Script surfaces, runtime artifacts, secrets, or
  production behavior were changed.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing tests for this docs-only comparison.

Residual follow-up items are already named in the handoff and should remain
future scoped work:

- add committed golden/corpus coverage for audited zero-count families;
- decide the connection payload `type` / `raw_*` policy;
- decide whether `Session.raw_session` mixed string/dict evidence is accepted;
- decide whether EventLifecycle should stay marker-level only;
- restore, create, or explicitly defer the GameState normalization backlog;
- consider a machine-readable parity matrix after the markdown V1 is accepted.

## Drift Notes

- Repo drift: expected new issue #121 docs only.
- Branch drift: branch-wide protected-surface warnings exist from earlier parser
  reliability work outside issue #121; path-scoped issue #121 gate is clean.
- Workbook drift: not inspected and not in scope.
- Deployment drift: not inspected and not in scope.
- Local-data drift: no raw logs, generated data, runtime status files,
  failed-post files, workbook exports, secrets, or local-only artifacts were
  touched.
- PR lifecycle drift: no PR exists yet for the current head branch.

## Protected-Surface Status

Issue #121 protected-surface status is clean. The reviewed package only adds
contract/comparison docs and this contract-test report. No protected parser,
runtime, workbook, webhook, Apps Script, secret, generated-data, or production
surface was changed.

## Recommendation

Approve for Codex F: Module Submitter, with the routing caveat that Codex F
must not open a PR to `main` and should stop for clarification if a non-main PR
base is not explicit.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for parser reliability issue #121.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/121

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Reviewed artifacts:
- docs/contracts/parser_field_level_parity_audit.md
- docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
- docs/contract_test_reports/parser_field_level_parity_audit.md

Codex E verdict:
No blocking findings. The docs-only issue #121 package is ready to submit.

Expected scope:
- Stage only the three reviewed issue #121 docs listed above.
- Do not stage parser source, tests, fixtures, snapshots, corpus baselines, raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, or unrelated files.
- Commit the reviewed issue #121 package.
- Push codex/parser-reliability-intelligence.
- Do not open a PR to main. If the workflow requires a draft PR, stop and ask for the approved non-main base branch before opening one.
- Link issue #121 and trackers #47/#11 in the commit or PR text where appropriate.

Validation evidence from Codex E:
- git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence -> 0 0
- git diff --check -> passed
- path-scoped protected-surface gate for issue #121 docs -> passed with 0 warnings
- py -m pytest -q tests\test_event_schema_snapshots.py -> 6 passed
- py -m pytest -q tests\test_gre_connect_resp_parser.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_small_modules.py -> 66 passed
- py -m pytest -q tests\test_client_actions_parser.py tests\test_match_state_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py -> 96 passed
- py -m pytest -q tests\test_feature_equity_corpus_ratchet.py tests\test_golden_replay_harness.py -> 19 passed
- py -m pytest -q -> 743 passed
- py -m ruff check src tests tools -> passed

Residual risks to mention:
- Remote CI has not run yet.
- No PR exists yet for head codex/parser-reliability-intelligence.
- Branch-wide protected-surface gate has warnings from earlier parser reliability work outside issue #121; the path-scoped issue #121 gate is clean.
- Live workbook, deployed Apps Script, webhook transport, production parser behavior, private local Player.log evidence, and future corpus coverage were not inspected.

Stop conditions:
- Do not change parser behavior, parser state final reconciliation, parser event classes, parser payload shapes, event kind values, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, runtime status files, failed posts, generated data, workbook exports, secrets, credentials, environment variables, production behavior, tests, fixtures, schema snapshots, or corpus baselines.
- Do not target main.
- Do not mark issue #121, tracker #47, or related tracker #11 complete.
- Do not stage unrelated files.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/121"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/parser_field_level_parity_audit.md"
  implementation_handoff: "docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md"
  review_artifact: "docs/contract_test_reports/parser_field_level_parity_audit.md"
  risk_tier: "Medium"
  branch: "codex/parser-reliability-intelligence"
  verdict: "ready for Codex F"
  findings:
    blocking: []
    non_blocking:
      - "Codex F must avoid opening a PR to main; if a draft PR is required, ask for the approved non-main base branch."
  validation:
    - "git status --short --branch -> issue #121 docs only before E report"
    - "git rev-list --left-right --count HEAD...origin/codex/parser-reliability-intelligence -> 0 0"
    - "git diff --check -> passed"
    - "path-scoped protected-surface gate for issue #121 docs -> passed with 0 warnings"
    - "py -m pytest -q tests\\test_event_schema_snapshots.py -> 6 passed in 0.59s"
    - "py -m pytest -q tests\\test_gre_connect_resp_parser.py tests\\test_connection_parsers.py tests\\test_collection_parser.py tests\\test_parser_small_modules.py -> 66 passed in 0.59s"
    - "py -m pytest -q tests\\test_client_actions_parser.py tests\\test_match_state_parser.py tests\\test_gre_game_state_parser.py tests\\test_gre_game_result_parser.py -> 96 passed in 0.60s"
    - "py -m pytest -q tests\\test_feature_equity_corpus_ratchet.py tests\\test_golden_replay_harness.py -> 19 passed in 0.97s"
    - "py -m pytest -q -> 743 passed in 4.92s"
    - "py -m ruff check src tests tools -> passed"
    - "branch-wide protected-surface gate -> passed with 9 warnings outside issue #121"
    - "gh pr list --head codex/parser-reliability-intelligence -> []"
  forbidden_scope_touched: false
  remaining_unverified:
    - "Remote CI"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Webhook transport behavior"
    - "Production parser behavior"
    - "Private local Player.log evidence"
    - "Future corpus coverage for currently zero-count audited families"
    - "Future evidence-ledger field-level provenance/confidence/finality"
  stop_conditions:
    - "Do not stage unrelated files outside the three issue #121 docs."
    - "Do not change parser behavior or protected runtime/workbook/webhook/App Script surfaces."
    - "Do not update tests, fixtures, schema snapshots, or corpus baselines."
    - "Do not target main."
    - "Do not mark issue #121, tracker #47, or related tracker #11 complete."
```
