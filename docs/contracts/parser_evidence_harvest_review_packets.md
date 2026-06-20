# Parser Evidence Harvest Review Packets Contract

## Module

Planning-only contract for issue #383, the harvest review packet boundary in
the parser evidence-pipeline lane.

Plain English: this contract defines a stable human- and Codex-readable packet
format for reviewing #382 local harvest candidate summaries without opening
large raw logs, copying private evidence, writing packet files, approving
fixture promotion, or changing parser behavior.

This Codex B pass does not implement code, write review packet files, run or
read private logs, create fixtures, promote corpus rows, authorize private
harvest, or claim parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/383
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/382
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/521
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Risk tier: High
- Previous merge commit: `85167fe2011a951a5773ce6db92ee65f55e4f372`

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` is up to date with `origin/main`.
- `HEAD` is `85167fe2011a951a5773ce6db92ee65f55e4f372`.
- Issue #382 is closed.
- PR #521 is merged.
- Issue #383 is open.
- Tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #383 still contains stale all-45 coverage start-condition wording.
  The latest #383 comment routes this issue to Codex B for planning-only
  contract work and explicitly preserves non-activation.

Current readiness and authorization facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
implementation_authorized: false
file_writing_authorized: false
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #383 and its latest Codex A comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #382 and PR #521
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `tests/test_local_harvest_candidate_reports.py`

## Observed Current Behavior

Issue #382 added a synthetic-only, in-memory local harvest candidate report
builder.

Observed #382 behavior:

- `build_harvest_candidate_report(...)` returns deterministic
  `mythic_edge_harvest_candidate_summary` dictionaries.
- `parser_evidence_from_utc_log_normalization(...)` converts #381
  synthetic UTC_Log normalization metadata into reduced parser evidence.
- Private source classes are blocked with
  `authorization_status=missing_required`.
- Forbidden raw/private summary fields are rejected without echoing supplied
  values.
- Reports preserve:
  - `parser_behavior_verified=false`
  - `corpus_status_change_authorized=false`
  - `fixture_promotion_authorized=false`
  - `private_harvest_authorized=false`
  - `pipeline_activation_ready_for_issue_388=false`
- No file discovery, source tailing, private log reads, output artifact writes,
  fixture creation, corpus metadata changes, parser behavior changes, runtime
  changes, workbook changes, webhook changes, Apps Script changes, analytics
  changes, AI changes, or coaching changes were added.

There is no dedicated harvest review packet module, schema, file writer, test,
or committed review packet artifact for issue #383.

## Problem

Candidate reports are machine-readable and useful, but reviewing candidate
windows still needs a stable packet vocabulary that a human and a Codex review
thread can inspect safely. The packet must summarize the candidate without
pulling raw evidence into the repo and without turning a reviewer decision into
parser truth or fixture-promotion authority.

The first bad value is treating any of these as parser truth, corpus status
truth, private-evidence approval, fixture-promotion authorization, readiness,
or production evidence:

- a #382 candidate report;
- a #383 review packet;
- a redacted context note;
- a parser fact preview;
- a privacy report;
- a reviewer decision;
- a Codex-readable summary.

## Scope Decision

This contract approves a planning boundary only.

Codex C implementation is not authorized by this contract. File writing is
also not authorized by this contract. The next workflow step should be a
lifecycle/activation decision after this contract is reviewed or accepted.

This contract defines:

- the logical review packet object;
- the relationship to #382 candidate summaries;
- candidate summary Markdown shape;
- redacted context shape;
- parser fact preview consumption boundary;
- privacy report vocabulary;
- reviewer decision vocabulary;
- validation expectations for a later implementation pass, if separately
  authorized.

This contract does not authorize:

- code implementation;
- file writing helpers;
- packet file generation;
- private source reads;
- diagnostics, drift, live MTGA, or private smoke checks;
- private harvest execution;
- fixture-promotion packet creation;
- fixture creation;
- corpus status changes;
- parser behavior changes;
- #388 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

Corpus / Provenance owns review-packet vocabulary, packet status vocabulary,
reviewer decision fields, and handoff semantics.

Generated / Local Artifacts owns any future local-only packet files or packet
previews, if a later contract authorizes writing them.

Quality / Governance owns privacy gates, stop conditions, review routing,
non-claim enforcement, and validation checks.

Parser owns event interpretation, routing semantics, parser events, parser
state, match/game identity, deduplication, and final reconciliation.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Generated / Local Artifacts, for any future local-only review packet files.
- Quality / Governance, for review routing, validation, and protected-surface
  boundaries.
- Parser, as the truth owner for parser fact previews consumed by packets.

This contract is not a parser behavior contract, not a private evidence
execution contract, not a fixture-promotion contract, not a golden replay
fixture contract, not a local app contract, not an analytics contract, not a
workbook/transport contract, not an AI/coaching contract, not a CI gate, and
not a release/deploy/production readiness gate.

## Truth Owner

Truth owner for parser facts remains the existing parser, router, event,
state, match/game identity, deduplication, and final reconciliation layers.

Truth owner for #382 candidate report shape:

- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `tests/test_local_harvest_candidate_reports.py`

Truth owner for this review packet vocabulary:

- `docs/contracts/parser_evidence_harvest_review_packets.md`
- any later reviewed implementation handoff and contract-test report, if
  implementation is explicitly authorized.

Truth owner for private-evidence execution boundaries:

- issue #434;
- explicit future private-evidence issues/contracts/user approvals;
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`;
- related private-evidence execution contracts.

Review packets must not own parser facts, private log content, fixture
expected output, corpus status promotion, merge readiness, release readiness,
production behavior, analytics truth, AI truth, coaching truth, or tracker
completion.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code.

Potential future allowed data flow:

```text
#382 in-memory candidate summary
  -> #383 in-memory review packet model
  -> human/Codex review decision
  -> later scoped follow-up issue, if approved
```

Potential future local-only file flow, not authorized now:

```text
#382 candidate summary
  -> local-only packet files in ignored storage
  -> reviewer decision file
  -> later fixture-promotion proof issue, if approved
```

Forbidden reverse flow:

- review packets must not rewrite parser facts;
- reviewer decisions must not change corpus status;
- privacy reports must not authorize private evidence reads;
- packet status must not authorize fixture promotion;
- Codex-readable summaries must not become parser truth, workbook truth,
  analytics truth, AI truth, coaching truth, merge readiness, deploy
  readiness, release readiness, or production behavior.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_harvest_review_packets.md`

Expected future review artifact, if this contract is submitted for review:

- `docs/contract_test_reports/parser_evidence_harvest_review_packets.md`

Potential future implementation artifacts, not authorized by this contract:

- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`
- `docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md`

Potential future local-only generated artifacts, not authorized or committed:

- `review_packet_manifest.json`
- `candidate_summary.md`
- `redacted_context.md`
- `parser_fact_preview.json`
- `privacy_report.json`
- `reviewer_decision.json`

## Public Interface Boundary

No public runtime interface is approved in this contract.

If later activated, the smallest safe implementation should be a pure in-memory
packet builder over a supplied #382 candidate summary. It must not discover
files, read local logs, write packet files, call diagnostics, call drift tools,
tail live sources, or mutate runtime artifacts by default.

Logical future interface:

```python
build_harvest_review_packet(
    *,
    candidate_summary: Mapping[str, Any],
    reviewer_context: Mapping[str, Any] | None = None,
    reviewer_decision: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]
```

Any future file-writing helper must require a separate contract and explicit
activation because this contract preserves `file_writing_authorized=false`.

## Review Packet Manifest Shape

If later implemented, the packet manifest must use this logical shape:

```yaml
object: "mythic_edge_harvest_review_packet"
schema_version: "parser_evidence_harvest_review_packet.v1"
packet_id: "symbolic-public-safe-id"
created_at_utc: "ISO-8601 timestamp"
source:
  candidate_report_object: "mythic_edge_harvest_candidate_summary"
  candidate_report_schema_version: "parser_evidence_harvest_candidate_summary.v1"
  candidate_report_id: "symbolic-public-safe-id"
  source_label: "symbolic-public-safe-label"
  privacy_class: "public_fixture|synthetic|private_local|local_only_redacted"
  raw_source_committed: false
  raw_path_included: false
  raw_hash_included: false
  raw_content_included: false
authorization:
  private_harvest_authorized: false
  file_writing_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
packet_status: "draft|review_required|blocked_privacy|blocked_authorization|reviewed_followup_candidate|reviewed_rejected|reviewed_deferred"
artifacts:
  candidate_summary_markdown: null
  redacted_context_markdown: null
  parser_fact_preview_json: null
  privacy_report_json: null
  reviewer_decision_json: null
non_claims:
  parser_behavior_verified: false
  parser_truth_decided: false
  fixture_promotion_authorized: false
  private_harvest_authorized: false
  pipeline_activation_ready_for_issue_388: false
```

In a future in-memory implementation, `artifacts` may contain embedded
subobjects instead of file references. Future file references require separate
file-writing authorization and must be local-only unless a later contract
explicitly authorizes committed sanitized examples.

## Candidate Summary Markdown Shape

`candidate_summary.md` is a human-readable rendering of a #382 candidate
summary. It may include:

- packet id and candidate report id;
- source label, source kind, and privacy class;
- candidate family table;
- candidate status;
- coverage value;
- confidence;
- duplication risk;
- privacy risk;
- evidence status;
- blocking conditions;
- non-claims;
- validation commands run for the packet, if any.

It must not include:

- raw log excerpts;
- raw JSON payloads;
- exact private paths;
- raw hashes;
- exact offsets or byte sizes;
- decklists, draft picks, sealed pools, card choices, or strategy notes;
- private operator notes;
- readiness or truth claims beyond the contracted vocabulary.

## Redacted Context Shape

`redacted_context.md` is optional and must be minimal.

Allowed context:

- symbolic source label;
- scenario family ids;
- event counts;
- event kind names;
- diagnostics status labels already present in a supplied candidate report;
- drift status labels already present in a supplied candidate report;
- truncation/data-loss counts;
- degradation/warning labels;
- notes that context is unavailable because private authorization is missing.

Forbidden context:

- raw log lines;
- raw payload bodies;
- copied snippets from private source files;
- exact local paths;
- raw hashes;
- exact offsets, byte ranges, file sizes, or timestamp windows from private
  evidence;
- account identifiers;
- decklists or card choices;
- generated private artifacts;
- operator-authored private notes unless a later private-evidence contract
  explicitly authorizes a redacted public summary.

For private or local-only sources, the safest default is:

```text
Redacted context unavailable: private source review requires a separate
approval under issue #434.
```

## Parser Fact Preview Consumption

Review packets may consume the #382 `parser_fact_preview` object only as a
reduced review input.

Allowed preview fields:

- preview status;
- event counts;
- event kind names;
- diagnostics status labels;
- drift status labels;
- truncation/data-loss counts;
- degradation labels;
- booleans proving raw log lines, raw payloads, and private paths are not
  included.

Forbidden preview use:

- deciding parser truth;
- deciding fixture expected output;
- inferring hidden information;
- reconstructing missing GameState data;
- replacing parser state final reconciliation;
- treating preview presence as behavior verification;
- treating preview absence as parser failure without a separate diagnostics or
  parser contract.

## Privacy Report Shape

If later implemented, `privacy_report.json` must use this logical shape:

```yaml
object: "mythic_edge_harvest_review_privacy_report"
schema_version: "parser_evidence_harvest_review_privacy_report.v1"
status: "pass|warn|block|unavailable"
checks:
  raw_log_lines_included: false
  raw_payloads_included: false
  private_paths_included: false
  raw_hashes_included: false
  exact_offsets_included: false
  exact_file_sizes_included: false
  generated_private_artifacts_included: false
  secrets_or_credentials_included: false
findings:
  - finding_id: "symbolic-public-safe-id"
    severity: "warn|block"
    field: "symbolic-field-name"
    reason: "public-safe-reason-code"
non_claims:
  privacy_assurance: false
  private_harvest_authorized: false
```

Status rules:

- `pass`: no contracted privacy check found forbidden content in supplied
  in-memory packet data.
- `warn`: packet is public-safe but has missing optional privacy evidence or
  incomplete reviewer context.
- `block`: forbidden content, private source class without authorization, or
  raw/private marker detected.
- `unavailable`: privacy evaluation was not run or not supplied.

`pass` does not mean privacy assurance. It means only that the modeled packet
data passed the contracted checks in the selected scope.

## Reviewer Decision Shape

If later implemented, `reviewer_decision.json` must use this logical shape:

```yaml
object: "mythic_edge_harvest_reviewer_decision"
schema_version: "parser_evidence_harvest_reviewer_decision.v1"
decision_id: "symbolic-public-safe-id"
reviewer_role: "human|codex_e|codex_a|codex_b"
decision_status: "approve_for_followup|reject|defer|needs_private_authorization|needs_contract_update|blocked_privacy"
candidate_report_id: "symbolic-public-safe-id"
packet_id: "symbolic-public-safe-id"
rationale:
  - "public-safe reason"
allowed_next_route: "codex_a_problem_representation|codex_b_contract|codex_e_review|none"
blocked_routes:
  - "fixture_promotion"
  - "private_harvest_execution"
  - "corpus_status_change"
non_claims:
  parser_truth_decided: false
  fixture_promotion_authorized: false
  private_harvest_authorized: false
  corpus_status_change_authorized: false
  parser_behavior_verified: false
  pipeline_activation_ready_for_issue_388: false
```

Allowed `decision_status` values:

- `approve_for_followup`
- `reject`
- `defer`
- `needs_private_authorization`
- `needs_contract_update`
- `blocked_privacy`

Reviewer decisions may route work. They do not authorize parser truth,
fixture promotion, private evidence reads, corpus metadata changes, #388
activation, release readiness, production readiness, analytics truth, AI
truth, or coaching truth.

## Packet Status Vocabulary

Allowed `packet_status` values:

- `draft`: packet is assembled but not reviewed.
- `review_required`: packet is ready for human/Codex review in the contracted
  scope.
- `blocked_privacy`: packet contains or may contain forbidden/private material.
- `blocked_authorization`: packet requires private, file-writing, or fixture
  authority not present in the current issue.
- `reviewed_followup_candidate`: reviewer says a follow-up issue or contract
  may be useful.
- `reviewed_rejected`: reviewer rejects the candidate for current workflow
  purposes.
- `reviewed_deferred`: reviewer defers the candidate without rejecting it.

No `packet_status` may mean fixture promotion, corpus status movement, parser
behavior readiness, private evidence approval, or #388 activation.

## Accepted Inputs

Approved for contract discussion:

- #382 `mythic_edge_harvest_candidate_summary` dictionaries;
- #382 `parser_fact_preview` dictionaries;
- synthetic in-memory candidate summaries from focused tests;
- public-safe symbolic reviewer context;
- public-safe reviewer decision metadata;
- committed contracts and implementation handoffs as context.

Potential future input classes requiring separate activation:

- local-only packet files;
- private/local source pointers;
- private evidence window metadata;
- local-only redacted context created under an approved private-evidence
  contract;
- reviewer decisions based on private operator notes.

The latter classes are not authorized by this contract.

## Forbidden Inputs

A #383 contract, implementation, test, report, or public artifact must not
read, include, summarize, hash, copy, or commit:

- raw private `Player.log` content;
- raw private `UTC_Log` content;
- raw log lines or raw JSON payload bodies;
- exact private paths;
- raw source hashes;
- exact private file offsets, file sizes, byte ranges, or timestamp windows;
- app-data contents;
- live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or
  private smoke data;
- runtime status files from a real run;
- failed posts;
- workbook exports;
- generated SQLite databases;
- decklists, sealed pools, draft picks, strategy notes, card choices, or
  private reports;
- secrets, credentials, tokens, API keys, webhook URLs, or screenshots.

## Error Behavior

A future packet builder must fail closed or degrade safely:

- missing candidate summary produces `blocked_authorization` or
  `reviewed_deferred`, not approval;
- unsupported candidate summary object or schema version produces
  `needs_contract_update`;
- private source class without authorization produces
  `blocked_authorization`;
- forbidden content detection produces `blocked_privacy`;
- malformed reviewer decision produces `needs_contract_update`;
- missing privacy report produces `review_required` or `warn`, not `pass`;
- ambiguous next route produces `defer`.

Errors must not echo forbidden supplied values.

## Side Effects

This contract authorizes no side effects beyond creating this contract file.

Future implementation, if separately authorized, should default to in-memory
packet construction only. Any file writes require a later explicit contract or
activation that preserves local-only artifact boundaries.

Forbidden side effects:

- reading local logs;
- writing packet files;
- writing runtime status;
- writing failed-post artifacts;
- writing workbook exports;
- creating fixtures;
- changing corpus manifest or session ledger;
- opening GitHub issues;
- updating trackers;
- posting webhooks;
- changing workbook, Apps Script, analytics, AI, coaching, CI, merge, deploy,
  release, or production behavior.

## Compatibility

This contract depends on #382 candidate reports remaining compatible with:

- `object: "mythic_edge_harvest_candidate_summary"`
- `schema_version: "parser_evidence_harvest_candidate_summary.v1"`

If #382 changes that shape, #383 must route back to Codex B before
implementation.

Review packets must preserve legacy safety flags and non-claims from #382:

- `parser_behavior_verified=false`
- `corpus_status_change_authorized=false`
- `fixture_promotion_authorized=false`
- `private_harvest_authorized=false`
- `pipeline_activation_ready_for_issue_388=false`

## Validation Obligations

This Codex B contract pass should validate documentation only:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf 'docs/contracts/parser_evidence_harvest_review_packets.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_harvest_review_packets.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_harvest_review_packets.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If a future implementation is explicitly authorized, minimum focused
validation should include synthetic-only tests:

```bash
python3 -m pytest -q tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf 'src/mythic_edge_parser/app/harvest_review_packets.py\ntests/test_harvest_review_packets.py\ndocs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/harvest_review_packets.py\ntests/test_harvest_review_packets.py\ndocs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/harvest_review_packets.py\ntests/test_harvest_review_packets.py\ndocs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Future implementation tests must prove:

- deterministic packet construction from #382 synthetic candidate summaries;
- no file writes occur by default;
- private source classes remain blocked;
- forbidden raw/private fields produce `blocked_privacy`;
- reviewer decisions cannot authorize fixture promotion or private harvest;
- privacy `pass` does not become privacy assurance;
- packet status cannot set parser readiness or #388 activation readiness;
- unsupported #382 schema versions route to `needs_contract_update`.

## Protected Surfaces

Do not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- diagnostics report shape;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- corpus manifest or session ledger status;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status schema;
- failed-post handling;
- workbook exports;
- analytics behavior;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- release readiness;
- production behavior;
- final integration policy.

Do not read, copy, hash, summarize, upload, or commit private logs, local-only
evidence, generated/private/runtime artifacts, secrets, credentials, tokens,
API keys, webhook URLs, screenshots, decklists, card choices, or private
reports.

## Acceptance Criteria

This contract is complete when:

- it defines the harvest review packet truth boundary;
- it preserves `implementation_authorized=false`;
- it preserves `file_writing_authorized=false`;
- it preserves `private_harvest_authorized=false`;
- it preserves `fixture_promotion_authorized=false`;
- it defines review packet, privacy report, redacted context, and reviewer
  decision logical shapes;
- it defines packet status vocabulary;
- it defines accepted and forbidden inputs;
- it explains why reviewer decisions are routing signals, not promotion or
  parser truth;
- documentation-only validation is run or explicitly recorded as unavailable;
- the next workflow route does not activate #383 implementation by default.

## Recommended Next Role

Recommended next role: Codex A, lifecycle/activation thinker.

Codex C is not recommended immediately because this contract is planning-only
and the latest #383 handoff says implementation, private harvest, fixture
promotion, and file writing are not authorized. Codex A should decide whether
#383 should remain deferred, split into a synthetic-only in-memory
implementation issue, or request explicit user approval for local-only packet
file writing under a later contract.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for issue #383 lifecycle activation after the Codex B
contract for harvest review packets.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/383

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_harvest_review_packets.md

Base branch:
main

Goal:
Decide whether #383 should remain planning-only, split into a synthetic-only
in-memory Codex C implementation issue, or require a separate user-approved
local-only file-writing/private-evidence path. Preserve
implementation_authorized=false, file_writing_authorized=false,
private_harvest_authorized=false, and fixture_promotion_authorized=false
unless you create an explicit scoped activation path.

Do not implement code.
Do not activate #388.
Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks.
Do not write packet files or generated artifacts.
Do not create fixtures or fixture-promotion packets.
Do not promote blocked, report-only, private-evidence, or external-boundary rows.
Do not claim parser_behavior_ready, pipeline activation readiness, fixture
promotion readiness, release readiness, production readiness, analytics truth,
AI truth, coaching truth, or full parser regression parity.

Expected output:
- lifecycle decision for #383
- whether a Codex C synthetic-only in-memory implementation prompt is
  appropriate
- required activation gates if implementation or file writing is recommended
- workflow_handoff block with repository and repository_url
```

workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/383"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/382"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/521"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #383 and #382 local harvest candidate report handoff"
  target_artifact: "docs/contracts/parser_evidence_harvest_review_packets.md"
  verdict: "planning_contract_complete_implementation_not_authorized"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "85167fe2011a951a5773ce6db92ee65f55e4f372"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  implementation_authorized: false
  file_writing_authorized: false
  stop_conditions:
    - "Do not implement code without a later explicit activation prompt."
    - "Do not write packet files or generated artifacts."
    - "Do not activate #388."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
