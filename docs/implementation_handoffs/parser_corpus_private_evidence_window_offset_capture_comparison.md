# Private Evidence Window Offset Capture Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/439

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Parent/private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Related completed packet:
  https://github.com/Tahjali11/Mythic-Edge/issues/438
- Related PR: https://github.com/Tahjali11/Mythic-Edge/pull/440

## Contract

- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`

## Internal Project Area

Corpus / Provenance, with Quality / Governance support for redaction,
validation, and protected-surface review.

Generated / Local Artifacts is a future local-only storage concern only. This
implementation did not create local offset state.

## Truth Owner

The contract owns only process vocabulary and documentation for future private
evidence windows. Current corpus status truth remains owned by:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

No parser, network, runtime health, drift health, workbook, analytics, AI,
coaching, readiness, production, or full-corpus-parity truth changed.

## Bridge-Code Status

`deferred_future_boundary`

This docs-only pass adds no bridge code. Any executable helper that records
offsets, reads local file metadata, or inspects appended bytes requires a later
issue/contract and explicit user approval.

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

Current repo state matched the contract:

- issue #439 is open;
- tracker #158 is open;
- parent issue #434 is open;
- issue #438 is closed after PR #440;
- PR #440 is merged into `main`;
- branch head is `a51760af738761c390dd4818fb9e86a839a1b241`;
- corpus parity still reports
  `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`;
- no template or implementation handoff existed for the offset-window process.

The contract authorized only a docs/template scaffold and an implementation
handoff. The implementation stayed inside that boundary.

## What Changed

- Added `docs/templates/private_evidence_window_offset_capture.md`.
- Added this implementation handoff.

The template is metadata-only. It separates:

- approval record fields;
- local-only start marker fields;
- local-only end marker fields;
- local-only derived window summary fields;
- optional sanitized public lifecycle summary candidate fields;
- forbidden public fields;
- redaction checklist;
- non-claims.

## Files Changed

- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
  - Source contract artifact from Codex B, present in this worktree.
- `docs/templates/private_evidence_window_offset_capture.md`
- `docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md`

## Code Changed

No runtime code changed.

No executable offset-capture tooling was added. No parser, router, diagnostics,
drift, golden replay, feature-equity, evidence-ledger, workbook, webhook, Apps
Script, Google Sheets, analytics, AI, coaching, CI, merge, deploy, production,
or tracker lifecycle surface changed.

## Tests Added Or Updated

No Python tests were added or updated because the contract authorized only a
docs/template scaffold.

## Interface Changes

The new template documents process fields for future approved private-evidence
windows. It does not create a runtime interface, CLI, environment-variable
contract, corpus status vocabulary, parser payload shape, workbook schema,
webhook payload shape, or local artifact schema.

## Contracted Area Status

The implementation stayed within the authorized Corpus / Provenance and
Quality / Governance documentation boundary.

Protected-surface authorization: Authorized - workflow_authority_docs -
`docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
contract authorizes `docs/templates/private_evidence_window_offset_capture.md`
as the docs-only offset-window checklist template.

No private logs were read. No private, firewall, network, live MTGA, app-data,
packet, OS/router, or private smoke checks were run. No local offset state,
local private packet, redacted lifecycle summary from real private data, raw
private artifact, exact private path, exact offset, exact file size, exact
private timestamp, raw hash, or local-only artifact was created or committed.

Blocked rows remain blocked by default, including:

- `connection.firewall_or_network_drop`
- `mythic_edge.private_log_report_only_drift`

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
git diff --no-index --check /dev/null docs/contracts/parser_corpus_private_evidence_window_offset_capture.md
git diff --no-index --check /dev/null docs/templates/private_evidence_window_offset_capture.md
git diff --no-index --check /dev/null docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md
printf '%s\n' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  docs/templates/private_evidence_window_offset_capture.md \
  docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  docs/templates/private_evidence_window_offset_capture.md \
  docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  docs/templates/private_evidence_window_offset_capture.md \
  docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md \
  | python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_corpus_private_evidence_window_offset_capture.md --authorization-file handoff=docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md
LC_ALL=C rg -n '[^[:ascii:]]' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  docs/templates/private_evidence_window_offset_capture.md \
  docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md
LC_ALL=C rg -n '[[:blank:]]$' \
  docs/contracts/parser_corpus_private_evidence_window_offset_capture.md \
  docs/templates/private_evidence_window_offset_capture.md \
  docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md
find . -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm'
```

Results:

- corpus parity CLI: `partial_coverage_map_ready (45 families, 6 committed, 0 missing)`.
- agent docs check: passed.
- Ruff: passed.
- tracked diff whitespace check: passed.
- explicit untracked-doc whitespace checks: passed, no findings.
- path-scoped secret/private-marker scan: passed.
- path-scoped protected-surface gate: passed with one expected
  `workflow_authority_docs` warning for
  `docs/templates/private_evidence_window_offset_capture.md`; the contract
  explicitly authorizes this template file.
- protected-surface authorization checker: `authorization_status: ok`.
- ASCII scan: passed.
- trailing-whitespace scan: passed.
- generated SQLite artifact scan: clean.

## Still Unverified

- No real offset capture was attempted.
- No appended byte range was inspected.
- No private drift evidence was collected.
- No redacted lifecycle summary from real private data was produced.
- No corpus status transition was attempted.

Those items require later explicit issue, contract, approval, and review.

## Reviewer Focus

Codex E should verify:

- the template is metadata-only and not executable tooling;
- no private values, exact offsets, exact file sizes, exact private timestamps,
  exact private paths, raw hashes, or local-only artifacts are present;
- the template keeps future start/end/derived metadata local-only by default;
- public lifecycle summary fields are symbolic and aggregate-only;
- blocked rows remain blocked by default;
- no parser/runtime/downstream behavior changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #439.

Review the docs-only offset-window scaffold against:
- docs/contracts/parser_corpus_private_evidence_window_offset_capture.md
- docs/templates/private_evidence_window_offset_capture.md
- docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md

Focus on whether the implementation stayed docs-only, preserved private
evidence boundaries, avoided executable tooling, avoided private values, and
kept blocked corpus rows blocked by default.

Do not read private logs, run private/firewall/network/live checks, promote
blocked rows, or change parser/runtime/downstream behavior.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/439"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/438"
  related_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/440"
  completed_thread: "C"
  next_thread: "E"
  verdict: "offset_capture_docs_only_scaffold_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-private-evidence-window-offset-capture"
  base_branch: "main"
  verified_main_merge_commit: "a51760af738761c390dd4818fb9e86a839a1b241"
  source_artifact: "docs/contracts/parser_corpus_private_evidence_window_offset_capture.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_private_evidence_window_offset_capture_comparison.md"
  template_artifact: "docs/templates/private_evidence_window_offset_capture.md"
  staged_follow_up: "mythic_edge.private_log_report_only_drift"
  tracker_status: "open"
  stop_conditions:
    - "Do not read private logs."
    - "Do not run private/firewall/network/live checks without explicit approval."
    - "Do not create executable offset-capture tooling in this slice."
    - "Do not commit raw private evidence, exact private paths, exact offsets, exact file sizes, exact private timestamps, raw hashes, or local-only artifacts."
    - "Do not promote blocked corpus rows by default."
```
