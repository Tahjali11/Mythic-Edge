# Parser Corpus Firewall / Network-Drop Private Evidence Execution Contract

## Module

Collection, redaction, and status-transition contract for a future
firewall/network-drop private evidence execution packet.

Plain English: this contract defines how a later, explicitly approved local
private evidence packet may be scoped for `connection.firewall_or_network_drop`.
It does not run the packet, read private logs, collect network evidence,
manipulate network state, promote the corpus row, add synthetic fixtures,
change parser behavior, or claim parser support, network reliability,
readiness, production behavior, analytics truth, AI truth, coaching truth, or
full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/435
- Parent/private-evidence planning issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous parser-parity PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/433
- Previous parser-parity merge commit:
  `bf4cd02bf3ca13b59cd982801cd64b18138dead6`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch:
  `codex/parser-corpus-firewall-network-drop-private-evidence-execution`
- base_branch: `codex/parser-parity`
- observed_base_commit: `bf4cd02bf3ca13b59cd982801cd64b18138dead6`
- target_artifact:
  `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority inspected:

- issue #435 and tracker #158
- issue #434 and its GitHub handoff comment
- local-only parent draft:
  `../Mythic-Edge-issue-434/docs/contracts/parser_corpus_firewall_network_drop_private_evidence_plan.md`
- `docs/contracts/parser_corpus_firewall_network_drop_coverage.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_connection_error_payload_coverage.md`
- `docs/contracts/parser_corpus_reconnect_coverage.md`
- `docs/contracts/parser_corpus_connection_disconnect_coverage.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- parser-evidence workflow issues #381 through #388 as future
  infrastructure context only

## Observed Current Behavior

Observed on `origin/codex/parser-parity` at
`bf4cd02bf3ca13b59cd982801cd64b18138dead6`:

- Issue #435 is open.
- Parent issue #434 is open.
- Tracker #158 is open.
- The #434 contract file was observed in a local sibling issue worktree, but
  it is untracked there and not present on `codex/parser-parity`.
- The committed branch still contains the issue #404 boundary contract for
  `connection.firewall_or_network_drop`.
- The committed corpus manifest contains
  `firewall_network_drop_private_evidence_boundary_v1`.
- The committed session ledger has no firewall/network-drop private evidence
  session entry.
- The current corpus parity report remains
  `partial_coverage_map_ready`.
- `connection.firewall_or_network_drop` remains:

```text
scenario_family: connection.firewall_or_network_drop
coverage_status: blocked_private_evidence
coverage_basis: local_report_only
entry: firewall_network_drop_private_evidence_boundary_v1
```

Adjacent connection families remain separate:

- `connection.connection_error_payload`: `covered_synthetic`
- `connection.reconnect`: `covered_synthetic`
- `connection.disconnect`: `covered_synthetic`

Those adjacent rows prove only parser-owned connection payload, reconnect, and
disconnect metadata. They do not prove firewall behavior, Wi-Fi/drop behavior,
OS/router/ISP behavior, packet loss, network reliability, live reconnect
resilience, private smoke success, runtime health, release readiness, deploy
readiness, production behavior, analytics truth, AI truth, coaching truth, or
full corpus parity.

## Scope Decision

This contract authorizes only the shape of a future evidence packet.

It does not authorize Codex C to run the packet yet. A later execution thread
may proceed only after explicit user approval names all of the following:

1. the exact local source class, either one local `Player.log` file or one
   normalized `UTC_Log` source;
2. the exact candidate window or session marker to inspect;
3. whether optional operator-authored incident notes are allowed;
4. the local-only artifact class and retention expectation;
5. whether a redacted report-only summary candidate may be created for review.

Until that approval exists, `connection.firewall_or_network_drop` must remain
`blocked_private_evidence`.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns private evidence packet boundaries, redaction requirements,
and possible future status-transition gates for corpus parity metadata. It does
not own parser connection behavior, local network behavior, firewall behavior,
operating-system behavior, router behavior, diagnostics behavior, runtime
health, release readiness, deploy readiness, production behavior, analytics
truth, AI truth, coaching truth, or tracker completion.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting areas:

- Quality / Governance, for approval gates, redaction checks, non-claims, and
  validation evidence.
- Generated / Local Artifacts, for any future local-only private packet.
- Parser, only as a non-claim adjacent source for already-contracted
  connection metadata.

This is not a Parser behavior module, local app module, diagnostics module,
network reliability module, analytics module, AI module, coaching module,
release gate, deploy gate, production module, or CI policy module.

## Truth Owner

Current corpus truth remains owned by:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Parser-observed adjacent connection truth remains owned by:

- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- focused parser tests

Future private packet truth, if approved, is temporary and local-only. It may
support a human-reviewed corpus evidence decision, but it must not become
parser truth, network-cause truth, runtime health truth, release readiness,
deploy readiness, production readiness, analytics truth, AI truth, coaching
truth, or full parity truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract does not authorize bridge code.

Potential future source area:

- Generated / Local Artifacts, if the user explicitly approves a local
  evidence packet.

Potential future consuming area:

- Corpus / Provenance, for a redacted report-only summary candidate.

Forbidden reverse flow:

- Private evidence must not change parser behavior, parser event classes,
  router dispatch, diagnostics behavior, runtime status shape, corpus report
  semantics, workbook behavior, webhook behavior, Apps Script behavior, Google
  Sheets sync, output transport, analytics, AI, coaching, CI, merge, deploy,
  production, or tracker lifecycle.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`

Files this contract may reference but does not authorize Codex B to change:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- adjacent connection parser contracts, handoffs, and reports
- adjacent connection parser source and tests

Not owned by this contract:

- raw Player.log files;
- normalized UTC_Log source files;
- private app-data;
- private smoke outputs;
- firewall logs;
- Wi-Fi logs;
- OS/router diagnostics;
- packet captures;
- network traces;
- generated/runtime artifacts;
- runtime status files;
- failed posts;
- workbook exports;
- SQLite databases;
- secrets, credentials, tokens, API keys, or webhook URLs;
- parser source;
- parser event classes;
- workbook, webhook, Apps Script, Google Sheets, analytics, AI, coaching, CI,
  merge, deploy, production, or tracker lifecycle surfaces.

## Public Interface

This contract defines an evidence-packet interface for a later approval-gated
thread.

### Approval Record

A later execution thread must cite an approval record containing:

- `approved_by`: human/user approval in the active thread;
- `approved_issue`: issue #435 or a later child issue;
- `approved_source_class`: `player_log` or `normalized_utc_log`;
- `approved_source_identifier`: a user-provided local source label, not a
  committed exact filesystem path;
- `approved_window`: one coarse candidate window or session marker;
- `operator_notes_allowed`: boolean;
- `local_artifact_class`: one of the allowed local-only output classes below;
- `redacted_summary_candidate_allowed`: boolean.

The approval record may be quoted in committed docs only if it contains no raw
log text, local absolute paths, network identifiers, credentials, decklists,
private strategy notes, or private screenshots.

### Local Evidence Packet

A future local-only packet may contain:

- `packet_id`: local identifier;
- `scenario_family`: must be `connection.firewall_or_network_drop`;
- `source_class`: `player_log` or `normalized_utc_log`;
- `source_scope`: coarse user-approved label, never an exact committed path;
- `candidate_window`: coarse time/session marker supplied or approved by the
  user;
- `operator_notes`: optional user-authored incident summary with no raw log
  text or private strategy content;
- `connection_event_counts`: aggregate counts only;
- `adjacent_parser_markers_observed`: boolean or aggregate count summary;
- `redaction_status`: one of the labels below;
- `verdict`: one of the labels below;
- `non_claims`: required list of non-claims;
- `raw_artifact_retention`: local-only retention statement;
- `commit_eligibility`: `not_committable`, `redacted_summary_candidate`, or
  `rejected`.

This packet is local-only by default and must not be committed.

### Redacted Report-Only Summary Candidate

A future committed summary candidate, if explicitly approved and reviewed, may
contain only:

- issue and approval references;
- repo branch and commit used for the review;
- tool or command names used, without local paths;
- scenario family;
- source class;
- coarse approved window label;
- aggregate counts;
- verdict label;
- redaction checklist result;
- protected-surface checklist result;
- explicit non-claims;
- statement that raw/private artifacts stayed local and were not committed.

It must not contain raw log lines, exact local paths, raw payloads, network
identifiers, screenshots, private app-data, decklists, strategy notes,
credentials, tokens, keys, URLs, or generated/runtime artifacts.

## Inputs

### Allowed Inputs For This Contract Pass

- Issue #435.
- Parent issue #434 and its GitHub handoff.
- The local-only #434 draft contract, as context only.
- Tracker #158.
- Current committed corpus manifest and session ledger.
- Current corpus parity report generated from committed metadata.
- Existing firewall/network-drop and adjacent connection-family contracts.
- Existing corpus parity report code and focused tests.
- Parser-evidence workflow issues #381 through #388 as context only.

### Potential Future Local-Only Inputs After Explicit Approval

A later execution contract may authorize exactly one of:

- one user-selected local `Player.log` file;
- one user-selected normalized `UTC_Log` source.

A later execution contract may also authorize:

- one coarse candidate window or session marker;
- optional operator-authored incident notes;
- aggregate parser-observed connection event counts around the approved
  window;
- local-only redaction workbench notes.

### Forbidden Inputs

Forbidden for this contract and any future committed artifact:

- raw Player.log excerpts;
- raw normalized UTC_Log excerpts;
- private app-data contents;
- private smoke outputs;
- firewall logs;
- Wi-Fi logs;
- router diagnostics;
- OS network diagnostics;
- packet captures;
- IP addresses;
- MAC addresses;
- SSIDs;
- hostnames;
- ports;
- network traces;
- exact local filesystem paths;
- generated/private/runtime artifacts;
- runtime status files;
- failed posts;
- workbook exports;
- SQLite files;
- secrets, credentials, tokens, API keys, webhook URLs;
- decklists, card choices, private strategy notes;
- private screenshots unless a later contract explicitly allows local-only
  review and forbids commit;
- Manasight raw logs, compressed corpus files, raw session payloads, hash
  lists, byte-size lists, capture-date row lists, parser source, or external
  corpus contents.

## Outputs

Output of this contract pass:

- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`

Potential future local-only outputs, only after explicit approval:

- local raw evidence packet;
- local parser/diagnostic summary;
- local redaction workbench notes;
- local operator note attachment;
- local rejected-summary notes.

Potential future committed output, only after explicit approval, redaction, and
review:

- one redacted report-only summary candidate.

No output from this contract pass may promote corpus status, add session-ledger
evidence, add synthetic firewall/drop fixtures, or change parser/runtime
behavior.

## Redaction Vocabulary

Allowed redaction statuses:

- `not_started`
- `raw_local_only`
- `redaction_in_progress`
- `redaction_failed`
- `redacted_summary_ready_for_review`
- `redacted_summary_rejected`
- `redacted_summary_approved`

Allowed verdict labels:

- `not_run`
- `approval_required`
- `local_evidence_collected`
- `redaction_required`
- `redacted_summary_review_required`
- `insufficient_evidence`
- `contradictory_evidence`
- `report_only_summary_ready`
- `blocked_private_evidence_preserved`

These labels are review vocabulary only. They are not parser truth, network
truth, runtime health truth, readiness truth, analytics truth, AI truth, or
coaching truth.

## Status-Transition Gates

`connection.firewall_or_network_drop` must remain `blocked_private_evidence`
unless a later issue and contract authorize a transition.

The row may move to `covered_report_only` only after all of these happen:

1. explicit user approval names the exact local source/window/artifact class;
2. a local-only execution packet is produced outside the repo;
3. raw/private artifacts remain outside Git history;
4. a redacted summary candidate is created only if approved;
5. secret/private marker scanning passes for the candidate;
6. protected-surface checks pass for changed files;
7. human or Codex E review confirms that the summary is aggregate,
   privacy-safe, and non-authoritative;
8. focused corpus parity tests are updated only for the approved
   report-only boundary;
9. the committed summary says exactly what it proves and what it does not
   prove.

The row must remain `blocked_private_evidence` when:

- no explicit approval exists;
- no exact source/window/artifact class is named;
- evidence is ambiguous, contradictory, or insufficient;
- redaction fails or cannot be reviewed;
- the only evidence is adjacent parser metadata;
- the only evidence is public taxonomy metadata;
- the only evidence is synthetic text;
- the proposed summary contains any forbidden content;
- the proposed summary would imply parser support, network reliability,
  private smoke success, readiness, production behavior, analytics truth, AI
  truth, coaching truth, or full corpus parity.

The row must not move to `covered_synthetic` from private evidence.

The row must not move to `covered_committed` unless a future fixture-promotion
workflow creates a fully sanitized, Mythic Edge-owned, review-approved fixture
under a separate contract.

The row must never use `parser_behavior_verified` solely because a private
packet or redacted summary exists.

## Invariants

- This contract does not authorize private checks.
- This contract does not authorize Codex C to execute the local action.
- This contract does not authorize a corpus status change.
- `connection.firewall_or_network_drop` remains `blocked_private_evidence`.
- Adjacent connection rows remain non-claims for firewall/network-drop truth.
- Generic connection errors, reconnect markers, disconnect markers, socket
  closes, diagnostics status, public taxonomy metadata, and synthetic text do
  not prove firewall/network-drop behavior.
- Local private evidence is non-committable by default.
- A committed summary, if later approved, must be redacted, aggregate,
  report-only, and human-reviewed.
- Tracker #158 must remain open.
- Zero missing rows and zero partial rows must not be treated as full corpus
  parity while private or external rows remain blocked.
- No parser/runtime/workbook/webhook/App Script/Sheets/analytics/AI/coaching/
  CI/merge/deploy/production behavior is authorized to change.

## Error Behavior

If a future workflow lacks explicit user approval, it must stop before reading
or running private evidence.

If the approval does not name the exact local source/window/artifact class, the
workflow must stop and route back to Codex A or the user.

If private data is accidentally produced, it must remain local and must not be
committed.

If forbidden content appears in a candidate committed file, the candidate must
be rejected and the row must remain `blocked_private_evidence`.

If redaction cannot prove safety, the row must remain
`blocked_private_evidence`.

If evidence is ambiguous or contradictory, the row must remain
`blocked_private_evidence` and the local verdict should be
`insufficient_evidence` or `contradictory_evidence`.

If execution requires parser behavior changes, route to Codex A/B for a new
parser problem representation and contract.

If execution requires corpus status transition, route to Codex B for a
status-transition contract or contract amendment before implementation.

## Side Effects

Allowed in this contract pass:

- write this contract file;
- inspect committed repo files and GitHub issue metadata;
- inspect the local untracked #434 draft contract as context;
- run documentation and committed-corpus validation commands.

Forbidden in this contract pass:

- read, copy, hash, summarize, upload, or commit raw private log contents;
- run private Player.log, UTC_Log, app-data, firewall/drop, Wi-Fi, network,
  live MTGA, packet, OS/router, or private smoke checks;
- manipulate network state or instruct a live-match interruption;
- create local private evidence artifacts;
- create redacted summary candidates;
- change corpus manifest/session-ledger status;
- add synthetic firewall/drop fixtures;
- change parser/source/test behavior;
- open a PR;
- close issue #435, parent issue #434, or tracker #158.

## Dependency Order

Future private-evidence execution must proceed in this order:

1. User explicitly approves the exact local source/window/artifact class.
2. Codex A confirms or creates a scoped execution issue if the approval changes
   scope.
3. Codex B updates or confirms this contract if the approved action differs
   from it.
4. Codex C runs only the approved local action and keeps raw evidence outside
   the repo.
5. Codex C creates only local outputs unless a redacted summary candidate is
   explicitly approved.
6. Codex E or a human reviewer verifies redaction, non-claims, and forbidden
   content exclusions.
7. Codex C/D may make only reviewed docs/report metadata changes, if
   authorized.
8. Codex E reviews the final diff and validation evidence.
9. Codex F may submit only reviewed files.
10. Codex G may merge/close/update only after explicit deployer approval and
    normal gates.

## Compatibility

This contract preserves:

- existing corpus report vocabulary;
- existing `blocked_private_evidence` status;
- existing `local_report_only` basis;
- existing `firewall_network_drop_private_evidence_boundary_v1` row;
- existing adjacent connection row statuses;
- existing parser connection behavior;
- existing private-log drift row separation;
- parser-evidence workflow issues #381 through #388 as future infrastructure
  context, not implementation authority.

## Tests Required

Minimum validation for this contract pass:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped safety checks for this contract file:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin

printf '%s\n' \
  docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
```

Future execution validation, only after explicit approval, must add:

- local artifact boundary verification;
- redaction checklist validation;
- forbidden-content scan of any committed summary candidate;
- focused corpus parity test updates only if status transition is separately
  authorized;
- proof that raw/private artifacts were not staged or committed.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`.
- Contract records that the #434 draft contract is local-only/untracked and
  not current branch authority.
- Contract preserves `connection.firewall_or_network_drop` as
  `blocked_private_evidence`.
- Contract defines exact approval requirements before local execution.
- Contract defines allowed local-only inputs and outputs.
- Contract defines forbidden inputs and forbidden committed content.
- Contract defines redaction vocabulary and verdict vocabulary.
- Contract defines status-transition gates and cases where the row must remain
  blocked.
- Contract routes execution away from Codex C until later explicit approval
  names the source file/window and artifact class.

## Next Workflow Action

Next role: Codex E for contract review, or Codex A/user approval if the user
wants to proceed toward private evidence execution.

Codex C must not run the local evidence action yet.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #435.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/435

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Contract:
docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md

Base branch:
codex/parser-parity

Goal:
Review the firewall/network-drop private evidence execution contract for
accuracy, privacy safety, protected-surface boundaries, status-transition
gates, and workflow routing. Confirm that it does not authorize private checks,
raw log access, network manipulation, corpus promotion, parser behavior
changes, readiness claims, analytics truth, AI truth, coaching truth, or full
corpus parity.

Do not implement code.
Do not run private/firewall/network/live checks.
Do not target main.
Do not close tracker #158.
Do not claim parser support, network reliability, private smoke success,
readiness, production behavior, analytics truth, AI truth, coaching truth, or
full corpus parity.
```

Future Codex C prompt, only after later explicit user approval:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #435 only after explicit user
approval names the exact local source/window and local-only artifact class.

Contract:
docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md

Goal:
Run only the approved local-only evidence action and produce only the approved
local-only or redacted-summary-candidate artifacts. Raw/private evidence must
remain outside the repo. Do not promote connection.firewall_or_network_drop
unless a separate status-transition contract and review authorize it.

Stop if the approval does not name the exact source/window/artifact class.
Stop if any raw/private content would be committed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/435"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/433"
  previous_merge_commit: "bf4cd02bf3ca13b59cd982801cd64b18138dead6"
  completed_thread: "B"
  next_thread: "E"
  verdict: "contract_ready_for_review_private_execution_not_authorized"
  risk_tier: "High"
  branch: "codex/parser-corpus-firewall-network-drop-private-evidence-execution"
  base_branch: "codex/parser-parity"
  selected_family: "connection.firewall_or_network_drop"
  source_artifact: "GitHub issue #435, parent issue #434 handoff, and local-only #434 draft contract context"
  target_artifact: "docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md"
  internal_project_area: "Corpus / Provenance"
  truth_owner: "corpus parity metadata; future private evidence remains local-only until separately approved and reviewed"
  bridge_code_status: "deferred_future_boundary"
  validation:
    - "Contract writer verified issue #435 open, parent issue #434 open, tracker #158 open, and origin/codex/parser-parity at bf4cd02bf3ca13b59cd982801cd64b18138dead6."
    - "Contract writer verified the #434 draft contract exists only as an untracked local artifact in the sibling issue #434 worktree and is not present on codex/parser-parity."
    - "Documentation-only contract pass; no private/firewall/network/live checks run and no status promotion authorized."
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not run private/firewall/network/live checks until later explicit approval names the exact source file/window and local-only artifact class."
    - "Do not read, copy, hash, summarize, upload, or commit raw private log contents."
    - "Do not manipulate network state or instruct a live-match interruption."
    - "Do not add synthetic firewall/drop fixtures."
    - "Do not promote connection.firewall_or_network_drop beyond blocked_private_evidence without a later approved status-transition contract and review."
    - "Do not claim parser support, network reliability, private smoke success, readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
