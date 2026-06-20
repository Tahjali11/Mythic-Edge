# Parser Evidence Fixture Promotion Proof Contract

## Module

Planning-only contract for issue #384, the fixture promotion proof boundary in
the parser evidence-pipeline lane.

Plain English: this contract defines how a future report-only proof object may
explain whether an approved harvest review packet would make parser evidence
stronger. The proof is a review and routing artifact only. It must not create
fixtures, mutate corpus metadata, promote coverage rows, bless parser behavior,
authorize private evidence, or activate the parser evidence pipeline.

This Codex B pass does not implement code, write proof files, run or read
private logs, create fixtures, draft golden replay manifests, promote corpus
rows, activate #388 or #381, or claim parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/384
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/383
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/522
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Risk tier: High
- Previous merge commit: `334c999324c9ac36d6697adc9eab92342f228416`

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` is at `334c999324c9ac36d6697adc9eab92342f228416`.
- Issue #383 is closed.
- PR #522 is merged.
- Issue #384 is open.
- Tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #384 still contains stale all-45 coverage start-condition wording.
  The latest #384 comment routes this issue to Codex B for planning-only
  contract work and explicitly preserves non-activation.

Current readiness and authorization facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
file_writing_authorized: false
implementation_authorized: false
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #384 and its latest Codex A comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #383 and PR #522
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/implementation_handoffs/parser_evidence_harvest_review_packets_comparison.md`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`

## Observed Current Behavior

Issue #381 added a planning boundary for a synthetic-only UTC_Log source
adapter.

Issue #382 added a synthetic-only, in-memory local harvest candidate report
builder.

Issue #383 added a synthetic-only, in-memory harvest review packet builder.
Observed #383 behavior:

- `build_harvest_review_packet(...)` consumes #382 candidate summaries and
  produces deterministic `mythic_edge_harvest_review_packet` dictionaries.
- Review packets summarize candidate coverage value, privacy risk, parser fact
  previews, and reviewer routing vocabulary.
- Review packets preserve:
  - `parser_behavior_verified=false`
  - `corpus_status_change_authorized=false`
  - `fixture_promotion_authorized=false`
  - `private_harvest_authorized=false`
  - `pipeline_activation_ready_for_issue_388=false`
- Review packets do not write files, read private logs, generate fixtures,
  draft golden replay manifests, mutate corpus metadata, activate #388, change
  parser behavior, or claim readiness.

There is no dedicated fixture promotion proof module, schema implementation,
file writer, test, or committed proof artifact for issue #384.

Existing golden replay, corpus parity, feature-equity, privacy, and
protected-surface checks can supply review evidence for a later proof object.
They are not promotion authority by themselves.

## Problem

Harvest review packets can say that a candidate deserves review, but they do
not answer the next planning question: if a later workflow approved this
candidate, what evidence would need to be true before it could become a
fixture-promotion packet?

That question is useful, but dangerous. A proof object sits near fixture
creation, corpus status movement, expected-output truth, privacy review, and
parser behavior claims. Without a contract, a later implementation could
accidentally turn a report-only proof into fixture-promotion authorization or
readiness evidence.

The first bad value is treating any of these as parser truth, corpus status
truth, private-evidence approval, fixture-promotion authorization, #388
activation, merge readiness, deploy readiness, release readiness, production
readiness, analytics truth, AI truth, coaching truth, or tracker completion:

- a #382 candidate summary;
- a #383 harvest review packet;
- a reviewer decision;
- a future #384 proof object;
- a golden replay pass;
- a corpus parity diff;
- a feature-equity comparison;
- a privacy check;
- a protected-surface check;
- a Codex-readable proof report.

## Scope Decision

This contract approves a planning boundary only.

Codex C implementation is not authorized by this contract. File writing is not
authorized by this contract. Fixture promotion is not authorized by this
contract. The next workflow step should be Codex A or an equivalent lifecycle
decision about whether #384 should remain planning-only, receive a separate
implementation issue, or wait for later #388 activation.

This contract defines:

- the logical fixture promotion proof object;
- accepted proof inputs from #382 and #383 artifacts;
- reviewer-decision consumption rules;
- before/after coverage comparison vocabulary;
- parser-owned fact preview boundaries;
- golden replay, corpus parity, feature-equity, privacy, and
  protected-surface check references as evidence requirements;
- proof status vocabulary;
- report-only proof versus fixture-promotion authorization boundaries;
- validation expectations for a later implementation pass, if separately
  authorized.

This contract does not authorize:

- code implementation;
- proof file generation;
- Markdown or JSON proof artifact writing;
- private source reads;
- diagnostics, drift, live MTGA, network, firewall, packet, OS/router, or
  private smoke checks;
- local app-data discovery;
- private harvest execution;
- fixture-promotion packet creation;
- fixture creation;
- golden replay manifest drafting;
- expected-output changes;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

Corpus / Provenance owns proof vocabulary, coverage-comparison vocabulary,
proof status vocabulary, fixture-promotion prerequisite descriptions, and
report-only proof semantics.

Generated / Local Artifacts owns any future local-only proof files, if a later
contract explicitly authorizes writing them.

Parser owns event interpretation, routing semantics, parser events, parser
state, match/game identity, deduplication, and final reconciliation.

Golden replay owns replay harness behavior over committed sanitized fixtures
and expected manifests. It does not authorize fixture creation or expected
manifest truth.

Quality / Governance owns privacy gates, stop conditions, review routing,
protected-surface checks, role handoffs, and non-claim enforcement.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Generated / Local Artifacts, for any future local-only proof files.
- Quality / Governance, for privacy gates, review routing, and validation.
- Parser, as the truth owner for parser fact previews referenced by proof
  objects.

This contract is not a parser behavior contract, not a private-evidence
execution contract, not a fixture-promotion contract, not a golden replay
fixture contract, not a workbook/transport contract, not an analytics
contract, not an AI/coaching contract, not a CI gate, and not a
release/deploy/production readiness gate.

## Truth Owner

Truth owner for parser facts remains the existing parser, router, event,
state, match/game identity, deduplication, and final reconciliation layers.

Truth owner for #382 candidate report shape:

- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `tests/test_local_harvest_candidate_reports.py`

Truth owner for #383 harvest review packet shape:

- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`

Truth owner for this proof vocabulary:

- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- any later reviewed implementation handoff and contract-test report, if
  implementation is explicitly authorized.

Truth owner for corpus status remains the corpus manifest, session ledger,
corpus parity report code, and their reviewed contracts. A proof object may
describe proposed status effects; it must not mutate or own them.

Truth owner for fixture promotion remains a future explicit fixture-promotion
issue, contract, implementation, review, and approval path. This contract does
not provide that authority.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code.

Potential future allowed data flow, if separately authorized:

```text
#382 in-memory candidate summary
  -> #383 in-memory harvest review packet
  -> #384 in-memory fixture promotion proof object
  -> human/Codex review decision
  -> later scoped fixture-promotion issue, if approved
```

Potential future local-only file flow, not authorized now:

```text
#383 review packet
  -> local-only promotion_proof.json / promotion_proof.md
  -> reviewer decision
  -> later fixture-promotion packet draft, if separately authorized
```

Forbidden reverse flow:

- proof objects must not rewrite parser facts;
- proof objects must not create fixtures;
- proof objects must not write expected manifests;
- proof objects must not mutate corpus status;
- proof objects must not approve private evidence reads;
- proof objects must not authorize fixture promotion;
- proof status must not activate #388 or #381;
- proof reports must not become parser truth, workbook truth, analytics truth,
  AI truth, coaching truth, merge readiness, deploy readiness, release
  readiness, production readiness, or tracker completion.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_fixture_promotion_proof.md`

Expected future review artifact, if this contract is submitted for review:

- `docs/contract_test_reports/parser_evidence_fixture_promotion_proof.md`

Potential future implementation artifacts, not authorized by this contract:

- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `tests/test_fixture_promotion_proof.py`
- `docs/implementation_handoffs/parser_evidence_fixture_promotion_proof_comparison.md`

Potential future local-only proof artifacts, not authorized by this contract
and not allowed in Git:

- `promotion_proof.json`
- `promotion_proof.md`
- local review notes that contain raw/private evidence, exact paths, hashes,
  offsets, screenshots, workbook exports, runtime artifacts, or secrets

## Public Interface

No public runtime interface is authorized now.

Logical future interface, if a later issue authorizes implementation:

```python
build_fixture_promotion_proof(
    *,
    review_packet: Mapping[str, Any],
    coverage_before: Mapping[str, Any],
    proposed_coverage_after: Mapping[str, Any] | None = None,
    check_refs: Mapping[str, Any] | None = None,
    proof_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]
```

The future interface must be pure and deterministic:

- no private file reads;
- no source discovery;
- no diagnostics execution;
- no golden replay execution;
- no network access;
- no GitHub mutation;
- no file writes;
- no corpus metadata writes;
- no fixture writes;
- no parser behavior changes.

## Inputs

Allowed inputs:

- #383 `mythic_edge_harvest_review_packet` dictionaries created from
  synthetic or public-safe candidate summaries.
- #382 `mythic_edge_harvest_candidate_summary` identifiers and reduced
  metadata already embedded or referenced by a review packet.
- Public-safe coverage status summaries from the corpus manifest, session
  ledger, and corpus parity report.
- Public-safe check references for golden replay, corpus parity,
  feature-equity, privacy, and protected-surface evidence.
- Public-safe contract references and issue/PR references.
- Explicit reviewer decision vocabulary from #383, consumed only as routing
  evidence.

Forbidden inputs:

- raw `Player.log` or `UTC_Log` lines;
- raw `Player.log` or `UTC_Log` snippets;
- private local app-data contents;
- exact private file paths;
- raw file hashes;
- exact private byte offsets, sizes, or timestamps that identify local files;
- screenshots;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- failed posts;
- secrets, credentials, tokens, API keys, webhook URLs, or environment
  variable values;
- Manasight raw logs, compressed corpus files, parser source, hash lists,
  byte-size lists, capture-date row lists, or external corpus contents;
- live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift,
  or private smoke outputs;
- raw decklists, card choices, private strategy notes, analytics outputs, AI
  outputs, or coaching outputs.

## Outputs

The logical proof object should use this shape if a future implementation is
authorized:

```yaml
object: "mythic_edge_fixture_promotion_proof"
schema_version: "parser_evidence_fixture_promotion_proof.v1"
proof_id: "<stable public-safe id>"
created_at_utc: "<ISO-8601 timestamp or omitted in deterministic tests>"
source:
  review_packet_schema_version: "..."
  review_packet_id: "..."
  candidate_report_id: "..."
  reviewer_decision_id: "..."
authorization:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  file_writing_authorized: false
  corpus_status_change_authorized: false
proof_status: "draft"
coverage_comparison:
  family: "<scenario family>"
  before_status: "<current status>"
  proposed_after_status: "<candidate status or null>"
  status_change_kind: "no_change"
  metadata_mutation_authorized: false
parser_fact_scope:
  parser_behavior_verified: false
  facts_proposed: []
  fact_preview_ref: "<public-safe summary ref or null>"
evidence_checks:
  golden_replay: {status: "not_run", refs: []}
  corpus_parity: {status: "not_run", refs: []}
  feature_equity: {status: "not_run", refs: []}
  privacy: {status: "not_run", refs: []}
  protected_surface: {status: "not_run", refs: []}
non_claims:
  - "not_fixture_promotion_authority"
  - "not_parser_truth"
  - "not_private_evidence_authorization"
  - "not_readiness"
```

Required output defaults:

- `parser_behavior_ready=false`
- `pipeline_activation_ready_for_issue_388=false`
- `private_harvest_authorized=false`
- `fixture_promotion_authorized=false`
- `file_writing_authorized=false`
- `corpus_status_change_authorized=false`
- `parser_behavior_verified=false`
- `metadata_mutation_authorized=false`

## Proof Status Vocabulary

Allowed `proof_status` values:

- `draft`: proof object is syntactically formed but not reviewed.
- `blocked_privacy`: proof cannot proceed because privacy/redaction evidence
  is missing, failed, or ambiguous.
- `blocked_authorization`: proof cannot proceed because the required workflow
  approval, issue activation, or role authorization is missing.
- `insufficient_review`: the #383 review packet or reviewer decision is
  missing, incomplete, stale, or not strong enough to reason about fixture
  promotion prerequisites.
- `proof_ready_for_review`: proof is ready for human/Codex review as a
  report-only routing artifact.
- `proof_rejected`: proof was reviewed and should not be used for follow-up
  fixture-promotion planning.
- `needs_contract_update`: the proof requires schema, vocabulary, surface, or
  protected-boundary changes outside this contract.

`proof_ready_for_review` is not fixture-promotion authorization.

## Reviewer Decision Consumption Rules

The proof may consume reviewer decision data from a #383 review packet only as
routing evidence.

Allowed reviewer-decision handling:

- `approve_for_followup` may permit a proof object to reach
  `proof_ready_for_review` when all other required public-safe evidence is
  present.
- `needs_contract_update` must map to `needs_contract_update`.
- `blocked_privacy` or any privacy failure must map to `blocked_privacy`.
- `needs_private_authorization` must map to `blocked_authorization`.
- `defer`, `reject`, missing decision, stale decision, ambiguous decision, or
  mismatched candidate identity must map to `insufficient_review` or
  `proof_rejected`.

Forbidden reviewer-decision handling:

- no reviewer decision may authorize private source reads;
- no reviewer decision may authorize fixture creation;
- no reviewer decision may authorize expected-output changes;
- no reviewer decision may authorize corpus status mutation;
- no reviewer decision may authorize #388 or #381 activation;
- no reviewer decision may claim parser behavior readiness.

## Coverage Comparison Vocabulary

Coverage comparison is descriptive and report-only.

Allowed `status_change_kind` values:

- `no_change`: the proof describes no proposed coverage-status movement.
- `stronger_evidence_candidate`: the proof identifies evidence that may
  support a future stronger claim, but no status movement is authorized.
- `status_promotion_candidate`: the proof describes a possible future status
  transition that would still require a separate fixture-promotion contract,
  implementation, review, and approval.
- `blocked_private_evidence`: the proposed path requires private evidence that
  is not authorized.
- `blocked_external_boundary`: the proposed path depends on external evidence
  or behavior outside Mythic Edge ownership.
- `needs_contract_update`: the proposed path requires new schema, vocabulary,
  fixture, or protected-surface authority.
- `unknown`: comparison could not be evaluated from public-safe inputs.

The proof may reference `before_status` and `proposed_after_status`, but must
not edit the corpus manifest, session ledger, generated reports, fixtures,
expected manifests, feature-equity baselines, or any source of corpus status.

## Evidence Check Vocabulary

Allowed evidence check status values:

- `not_run`
- `pass`
- `warn`
- `review`
- `diff`
- `fail`
- `blocked`
- `unavailable`

Check references may name public-safe command labels, contract-test report
paths, implementation handoff paths, issue links, PR links, or reduced
artifact identifiers.

Evidence check non-claims:

- a golden replay `pass` does not authorize fixture promotion;
- a corpus parity `pass` does not mutate corpus status;
- a feature-equity `pass` does not prove feature parity;
- a privacy `pass` does not prove privacy assurance;
- a protected-surface `pass` does not authorize protected-surface changes;
- any `diff`, `fail`, `blocked`, or `unavailable` status must prevent
  `proof_ready_for_review` unless a later contract explicitly defines a
  review-only exception.

## Parser Fact Preview Boundary

The proof may summarize parser-owned fact previews from #383 only when those
previews are already reduced, public-safe, and non-private.

Allowed fact-preview content:

- parser event family names;
- reduced counts;
- scenario-family labels;
- public-safe parser fact field names;
- public-safe validation references;
- degraded/unknown/review-needed vocabulary.

Forbidden fact-preview content:

- raw log lines;
- exact private source locations;
- exact raw event payloads;
- raw card lists, decklists, strategy notes, or screenshots;
- hidden-card inference;
- archetype classification;
- gameplay advice;
- player-mistake labels;
- AI/model-provider output;
- workbook/export/private runtime content.

Fact previews are not parser truth. They are planning summaries that point to
the parser-owned surfaces that would need tests if fixture promotion were ever
separately authorized.

## Invariants

- Proof objects are advisory and report-only.
- Proof objects must preserve all false readiness and authorization flags
  listed in this contract.
- Proof objects must be deterministic for equivalent public-safe inputs.
- Proof objects must fail closed on missing, stale, malformed, or ambiguous
  review packet inputs.
- Proof objects must not echo forbidden private input values.
- Proof objects must not write files unless a later contract explicitly
  authorizes file writing.
- Proof objects must not read source files, private logs, diagnostics outputs,
  drift reports, network state, OS/router state, workbook exports, or runtime
  artifacts.
- Proof objects must not create fixtures or expected manifests.
- Proof objects must not mutate corpus metadata.
- Proof objects must not activate #388 or #381.
- Proof objects must not alter parser, workbook, webhook, Apps Script,
  analytics, AI, coaching, CI, release, deploy, or production behavior.

## Error Behavior

Missing #383 review packet:

- return or record `proof_status=insufficient_review`.

Malformed #383 review packet:

- return or record `proof_status=needs_contract_update` when the shape is
  unknown, or `proof_status=insufficient_review` when required fields are
  absent.

Review packet identity mismatch:

- return or record `proof_status=insufficient_review`.

Forbidden raw/private fields:

- return or record `proof_status=blocked_privacy`;
- do not echo forbidden values in diagnostics or error text.

Missing reviewer decision:

- return or record `proof_status=insufficient_review`.

Reviewer decision requiring private authorization:

- return or record `proof_status=blocked_authorization`.

Evidence check failure, diff, or unavailable state:

- return or record `proof_status=proof_rejected`, `blocked_privacy`,
  `blocked_authorization`, or `insufficient_review` depending on the failed
  check;
- do not promote to `proof_ready_for_review`.

Contract ambiguity:

- return or record `proof_status=needs_contract_update`.

## Side Effects

No side effects are authorized by this contract.

Forbidden side effects include:

- file writes;
- local artifact writes;
- fixture writes;
- golden replay manifest writes;
- expected-output writes;
- corpus manifest or session ledger writes;
- generated report writes;
- GitHub issue edits;
- PR creation;
- tracker updates;
- CI changes;
- private source reads;
- diagnostics or drift execution;
- workbook, webhook, Apps Script, Google Sheets, output transport, analytics,
  AI, coaching, release, deploy, or production changes.

## Dependency Order

If a later workflow authorizes implementation, the safe order is:

1. Confirm #384 has an explicit implementation authorization and a clean target
   branch.
2. Re-read this contract and the #383 review packet contract.
3. Implement only the in-memory proof object builder.
4. Add synthetic-only focused tests for proof status mapping, false readiness
   flags, forbidden-input rejection, and coverage-comparison vocabulary.
5. Write an implementation handoff comparing behavior to this contract.
6. Route to Codex E for contract-test review.
7. Defer any file writer, local-only proof artifact, fixture-promotion packet,
   fixture creation, expected-output update, corpus metadata update, or #388
   activation to a separate contract and explicit approval.

## Compatibility

The proof vocabulary must remain compatible with:

- #382 `mythic_edge_harvest_candidate_summary` objects;
- #383 `mythic_edge_harvest_review_packet` objects;
- existing corpus parity statuses and session-ledger metadata;
- existing golden replay harness report semantics;
- existing feature-equity report semantics;
- existing privacy and protected-surface checker semantics;
- existing Mythic Edge workflow handoff vocabulary.

Compatibility does not authorize old stale start-condition wording from issue
#384. The latest #516/#518/#388 planning contracts and #381/#382/#383 sequence
control non-activation semantics.

## Tests Required

Documentation-only validation for this contract:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf 'docs/contracts/parser_evidence_fixture_promotion_proof.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_fixture_promotion_proof.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_fixture_promotion_proof.md\n' | python3 tools/select_validation.py --paths-from-stdin
```

If a later implementation is explicitly authorized, focused tests should cover:

- valid #383 review packet to `draft`;
- approved review packet with all public-safe check refs to
  `proof_ready_for_review`;
- missing or stale review packet to `insufficient_review`;
- privacy-blocked input to `blocked_privacy`;
- missing workflow authorization to `blocked_authorization`;
- schema mismatch to `needs_contract_update`;
- rejected reviewer decision to `proof_rejected`;
- every output preserves false readiness and authorization flags;
- forbidden private fields are rejected without echoing values;
- coverage-comparison vocabulary never mutates corpus metadata;
- proof objects are deterministic and side-effect free.

## Acceptance Criteria

- The contract clearly distinguishes report-only proof from fixture-promotion
  authorization.
- The contract preserves:
  - `parser_behavior_ready=false`
  - `pipeline_activation_ready_for_issue_388=false`
  - `private_harvest_authorized=false`
  - `fixture_promotion_authorized=false`
  - `file_writing_authorized=false`
  - `implementation_authorized=false`
- The contract defines a logical proof object shape.
- The contract defines proof status vocabulary.
- The contract defines reviewer-decision consumption rules.
- The contract defines coverage-comparison vocabulary without authorizing
  metadata mutation.
- The contract defines evidence check references as prerequisites, not
  authority.
- The contract rejects private/raw input classes and protected-surface changes.
- The contract routes next work away from Codex C unless a later lifecycle
  decision explicitly authorizes implementation.

## Next Workflow Action

Next role: Codex A: Thinker / Lifecycle Reconciliation.

Codex C is not authorized by this contract because implementation, file
writing, private harvest, and fixture promotion are all still false.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for issue #384 under parser evidence-pipeline tracker #388.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/384

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Completed contract:
docs/contracts/parser_evidence_fixture_promotion_proof.md

Goal:
Decide whether #384 should remain planning-only, receive a separate explicitly authorized synthetic-only Codex C implementation pass, or wait for later #388 activation. Preserve parser_behavior_ready=false and pipeline_activation_ready_for_issue_388=false unless a later reviewed implementation proves otherwise.

Do not implement code. Do not activate #388 or #381. Do not authorize private harvest, fixture promotion, file writing, corpus metadata mutation, fixture creation, golden replay manifest drafting, or expected-output changes unless a new scoped issue and contract explicitly approve it. Do not read private logs or run private/live checks.

Expected output:
- lifecycle decision for #384;
- whether Codex C is authorized, and if so the exact synthetic-only scope;
- updated workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/384"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/383"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/522"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #384 and Codex A planning comment"
  target_artifact: "docs/contracts/parser_evidence_fixture_promotion_proof.md"
  verdict: "planning_contract_complete_implementation_not_authorized"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "334c999324c9ac36d6697adc9eab92342f228416"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  file_writing_authorized: false
  implementation_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "printf 'docs/contracts/parser_evidence_fixture_promotion_proof.md\\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf 'docs/contracts/parser_evidence_fixture_promotion_proof.md\\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf 'docs/contracts/parser_evidence_fixture_promotion_proof.md\\n' | python3 tools/select_validation.py --paths-from-stdin"
  stop_conditions:
    - "Do not close tracker #388 without explicit lifecycle approval."
    - "Do not close or bypass parent private-evidence issue #434."
    - "Do not activate #388 or #381."
    - "Do not route directly to Codex C without a new lifecycle authorization."
    - "Do not implement code, write proof files, create fixtures, draft golden replay manifests, mutate corpus metadata, change expected outputs, or promote corpus rows."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not claim parser behavior readiness, fixture promotion authorization, private harvest authorization, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
