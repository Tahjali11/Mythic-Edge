# Parser Evidence Harvest Review Packets Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/383

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

## Contract

`docs/contracts/parser_evidence_harvest_review_packets.md`

## Internal Project Area

Parser evidence pipeline / Corpus and Provenance, with Quality / Governance
support.

## Truth Owner

Parser-owned truth remains with the existing parser, router, state, match/game
identity, deduplication, and final reconciliation layers. Harvest review
packets are advisory review/routing artifacts only.

## Bridge-Code Status

`shared_support`

The implementation consumes #382 in-memory candidate summaries and emits a
reduced in-memory review packet. It does not connect to runtime, diagnostics,
drift, golden replay, corpus metadata, fixture promotion, workbook, webhook,
Apps Script, analytics, AI, or coaching surfaces.

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

The Codex B contract is planning-only and records
`implementation_authorized=false`. The current user prompt explicitly
activated only the smallest synthetic/in-memory implementation described by
the contract. This pass preserves the contract's private-harvest,
file-writing, fixture-promotion, corpus-status, and #388 activation
boundaries.

Confirmed matches:

- Builds `mythic_edge_harvest_review_packet` dictionaries with schema version
  `parser_evidence_harvest_review_packet.v1`.
- Consumes supplied #382 `mythic_edge_harvest_candidate_summary` mappings.
- Validates the #382 object and schema version.
- Embeds reduced candidate summary markdown, redacted context markdown, parser
  fact preview JSON, privacy report JSON, and optional reviewer decision JSON
  in memory only.
- Blocks private source classes without authorization.
- Blocks forbidden raw/private fields without echoing supplied values.
- Treats reviewer decisions as routing metadata only.
- Keeps all parser behavior, fixture-promotion, private-harvest, corpus-status,
  #388 activation, release, analytics, AI, coaching, and parity flags false.

Still deferred:

- Packet file writing.
- Private Player.log or UTC_Log reads.
- Local source discovery, log tailing, diagnostics/drift/private smoke checks,
  fixture creation, fixture promotion, corpus manifest/session-ledger changes,
  and #388 activation.

## Files Changed

- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`
- `docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md`

Source artifact present and unchanged by this Codex C pass:

- `docs/contracts/parser_evidence_harvest_review_packets.md`

## Code Changed

Added `src/mythic_edge_parser/app/harvest_review_packets.py`.

New public helper:

- `build_harvest_review_packet(...)`

Behavior surface:

- Pure deterministic in-memory packet construction from supplied mappings.
- No filesystem reads.
- No filesystem writes.
- No parser behavior changes.
- No corpus metadata changes.
- No runtime, workbook, webhook, Apps Script, analytics, AI, or coaching
  changes.

## Tests Added Or Updated

Added `tests/test_harvest_review_packets.py`.

Focused coverage includes:

- deterministic packet construction from #382 synthetic candidate summaries;
- public-safe reviewer context and reviewer decision metadata;
- private source class authorization blocking;
- raw/private field privacy blocking without value echo;
- upstream privacy findings staying blocked;
- unsupported candidate summary schema routing to contract update;
- malformed reviewer decision routing to contract update;
- forbidden reviewer context blocking without value echo;
- non-mapping candidate summaries failing closed without value echo.

## Interface Changes

New local Python module interface only. No CLI, environment variable,
configuration file, runtime status field, corpus metadata field, workbook
column, webhook payload field, Apps Script surface, public runtime endpoint, or
packet file writer was added.

## Contracted Area Status

Stayed inside the user-activated synthetic-only in-memory packet-builder scope.
The implementation did not create local harvest artifacts, parser fixtures,
fixture-promotion packets, corpus manifest/session-ledger changes, or #388
activation outputs.

## Validation Run

```bash
python3 -m pytest -q tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
# 16 passed

python3 -m pytest -q tests
# 1806 passed

python3 -m ruff check src tests tools
# passed

python3 tools/check_agent_docs.py
# passed: errors 0, warnings 0

git diff --check
# passed; note this worktree currently has only untracked changed files

for target in docs/contracts/parser_evidence_harvest_review_packets.md src/mythic_edge_parser/app/harvest_review_packets.py tests/test_harvest_review_packets.py docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md; do git diff --no-index --check /dev/null "$target" >/dev/null; rc=$?; if [ "$rc" -ne 1 ]; then exit "$rc"; fi; done
# passed for new files

printf '%s\n' docs/contracts/parser_evidence_harvest_review_packets.md src/mythic_edge_parser/app/harvest_review_packets.py tests/test_harvest_review_packets.py docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' docs/contracts/parser_evidence_harvest_review_packets.md src/mythic_edge_parser/app/harvest_review_packets.py tests/test_harvest_review_packets.py docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' docs/contracts/parser_evidence_harvest_review_packets.md src/mythic_edge_parser/app/harvest_review_packets.py tests/test_harvest_review_packets.py docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
# selection_status: ok; recommended full pytest and Pyright advisory

python3 tools/run_pyright_advisory_report.py
# advisory_findings, non-blocking: 390 existing type findings; tooling_config_blockers 0
```

## Still Unverified

- Private/local harvest execution.
- Private Player.log or UTC_Log evidence windows.
- Packet file-writing behavior.
- Fixture promotion readiness.
- Parser behavior readiness.
- #388 pipeline activation readiness.
- Release, deploy, production, analytics, AI, coaching, or full parser
  regression parity.

## Reviewer Focus

Codex E should verify:

- no source file discovery, log tailing, default Player.log path use, or packet
  file write behavior exists;
- packets cannot include raw log lines, raw payloads, private paths, raw hashes,
  exact offsets, exact file sizes, generated artifacts, or private content;
- private source classes remain blocked without separate authorization;
- reviewer decisions cannot authorize fixture promotion, private harvest,
  corpus status changes, or #388 activation;
- unsupported #382 schema versions route to contract update rather than
  approval;
- tests cover the contracted safety boundaries.

## Codex D Fixer Addendum

Source finding: `HREV-E-001`
(`blocking_privacy_sanitizer_gap_route_to_codex_d`).

Fault category: implementation privacy sanitizer gap.

The sanitizer previously detected POSIX local paths only at the start of a
string or after whitespace. A public-safe-looking reviewer context value such
as an assignment-prefixed local path could pass validation and be echoed in the
in-memory `reviewer_context` payload.

Fix produced:

- tightened local-path text detection so punctuation/assignment-prefixed
  POSIX local paths are treated as forbidden content while public URL text
  remains allowed;
- added focused regression coverage proving an assignment-prefixed private
  path blocks the packet and is not echoed.
- added the remaining sanitizer coverage for labeled, URI-shaped, and
  URL-encoded private path values so `file:///...`, `source_path:/...`,
  `windows_path:C:\...`, and encoded local-path strings block without echoing
  supplied values;
- closed the remaining colon/URI local-path gap for `file://localhost/...`,
  nested `uri:file://localhost/...`, `vscode://file/...`, and encoded
  localhost file URI shapes;
- kept normal public `https://github.com/...` reviewer-context URLs allowed.

Validation run during Codex D:

```bash
python3 -m pytest -q tests/test_harvest_review_packets.py tests/test_local_harvest_candidate_reports.py
# 27 passed

python3 -m ruff check src/mythic_edge_parser/app/harvest_review_packets.py tests/test_harvest_review_packets.py
# All checks passed!
```

## Next Workflow Action

Next role: Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #383.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/383

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/382

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/521

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_harvest_review_packets.md

Implementation handoff:
docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md

Review scope:
- src/mythic_edge_parser/app/harvest_review_packets.py
- tests/test_harvest_review_packets.py
- docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md
- docs/contracts/parser_evidence_harvest_review_packets.md

Goal:
Review the #383 synthetic-only in-memory harvest review packet builder against
the issue, contract, implementation handoff, and diff. Verify that the current
user activation stayed limited to in-memory packet construction and did not
read private sources, discover files, write packet files, create fixtures,
promote corpus rows, change parser behavior, or claim readiness.

Focus:
- #382 candidate summary object/schema validation.
- No raw/private value echo in privacy blocks or errors.
- Private source classes remain blocked without separate authorization.
- Reviewer decisions are routing metadata only.
- All parser behavior, fixture promotion, private harvest, corpus status, #388
  activation, release, analytics, AI, coaching, and parity flags remain false.
- No protected parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  surfaces changed.

Do not:
- Fix code unless explicitly re-routed to Codex D.
- Read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift,
  network, or private smoke data.
- Write packet files or generated artifacts.
- Create fixtures or fixture-promotion packets.
- Activate #388 or #381.
- Close #383, #388, or #434.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
- python3 -m ruff check src tests tools
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private marker scan for changed files
- path-scoped protected-surface gate for changed files
- path-scoped validation selector for changed files
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/383"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/382"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/521"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_evidence_harvest_review_packets.md"
  target_artifact: "docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  file_writing_authorized: false
  validation:
    - "python3 -m pytest -q tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "git diff --no-index --check for new files"
    - "path-scoped secret/private marker scan passed"
    - "path-scoped protected-surface gate passed"
    - "path-scoped validation selector passed"
    - "python3 tools/run_pyright_advisory_report.py advisory findings only"
  stop_conditions:
    - "Do not write packet files or generated artifacts."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, diagnostics, drift, or private smoke checks."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
