# Parser Evidence Corpus Metadata Diff Generator Contract

## Module

Planning-only contract for issue #386, the corpus metadata diff generator
boundary in the parser evidence-pipeline lane.

Plain English: this contract defines how Mythic Edge may later describe a
proposed corpus manifest and session ledger metadata change for a reviewed
fixture-promotion candidate without applying that change. The proposed diff
is a review artifact only. It must not edit corpus metadata, write diff files,
create fixtures, draft golden replay manifests, bless parser behavior,
authorize private evidence, or activate the parser evidence pipeline.

This Codex B pass does not implement code, write metadata diff files, edit
`corpus_manifest.v1.json`, edit `session_ledger.v1.json`, run or read private
logs, create fixtures, draft golden replay manifests, promote corpus rows,
activate #388 or #381, or claim parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/386
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/384
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/523
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Risk tier: High
- Previous merge commit: `d31ebb8fa773edbd784a873c57b07f7bbbc97478`

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` is at `d31ebb8fa773edbd784a873c57b07f7bbbc97478`.
- Issue #384 is closed.
- PR #523 is merged.
- Issue #386 is open.
- Tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #386 still contains older ordering language that says
  fixture/manifest draft generation should exist before metadata diffs are
  produced. The latest #386 reconciliation comment allows Codex B contract
  work now because the #388 planning umbrella intentionally defines metadata
  movement rules before any committable fixture-file drafting.

Current readiness and authorization facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #386 and its latest Codex A reconciliation comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #384 and PR #523
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/implementation_handoffs/parser_evidence_fixture_promotion_proof_comparison.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `tests/test_fixture_promotion_proof.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

## Observed Current Behavior

Issue #384 added a synthetic-only, in-memory fixture promotion proof builder.
Observed #384 behavior:

- `build_fixture_promotion_proof(...)` builds deterministic
  `mythic_edge_fixture_promotion_proof` dictionaries from supplied #383 review
  packets, public-safe coverage summaries, public-safe check references, and
  optional public-safe proof context.
- Proofs can reach `proof_ready_for_review` when an approved #383 review
  packet and passing public-safe check references are supplied.
- Proofs remain report-only and preserve:
  - `parser_behavior_ready=false`
  - `pipeline_activation_ready_for_issue_388=false`
  - `private_harvest_authorized=false`
  - `fixture_promotion_authorized=false`
  - `file_writing_authorized=false`
  - `corpus_status_change_authorized=false`
- #384 did not add file writing, private harvest, fixture creation, corpus
  metadata mutation, golden replay manifest drafting, #388 activation, or
  parser behavior changes.

Current corpus metadata behavior:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json` is the committed
  corpus manifest.
- `tests/fixtures/parser_corpus/session_ledger.v1.json` is the committed
  session ledger.
- `src/mythic_edge_parser/app/corpus_parity_report.py` validates both files
  and builds the current report.
- Current corpus report status remains `partial_coverage_map_ready`.
- Current report summary has 45 families, 0 missing rows, and
  `parser_behavior_ready=false`.

There is no dedicated corpus metadata diff generator module, schema
implementation, file writer, test, or committed diff artifact for issue #386.

## Problem

#384 proof objects can explain why a candidate might be worth future fixture
promotion review. The next planning question is what metadata movement would
be proposed if a later workflow approved that candidate. That question must be
answered carefully because corpus metadata is close to public evidence claims:

- coverage status;
- coverage basis;
- known gaps;
- review notes;
- manifest paths;
- session ledger summaries;
- golden replay fixture references;
- parser behavior readiness metrics.

Without a contract, a future implementation could accidentally turn a
proposed metadata diff into corpus-status authority, mutate the manifest, drop
known-gap language, add `parser_behavior_verified` too early, or promote
private/external/report-only rows without the required proof and review gates.

The first bad value is treating any of these as corpus-status authority,
fixture-promotion authorization, parser behavior readiness, private-evidence
approval, #388 activation, release readiness, production readiness, analytics
truth, AI truth, coaching truth, or tracker completion:

- a proposed metadata diff;
- a #384 proof object;
- a #383 review packet;
- a #382 candidate summary;
- a passing check reference;
- a Codex-readable diff summary;
- a golden replay result;
- a corpus parity comparison.

## Scope Decision

This contract approves a planning boundary only.

Codex C implementation is not authorized by this contract. File writing is not
authorized by this contract. Corpus status movement is not authorized by this
contract. The next workflow step should be Codex A or an equivalent lifecycle
decision about whether #386 should remain planning-only, receive a separate
synthetic/in-memory Codex C implementation pass, or wait for later #388
activation.

This contract defines:

- the logical corpus metadata diff object;
- accepted inputs from #384 proof objects, #383 review packets, #382 candidate
  summaries, the current corpus manifest, and the current session ledger;
- forbidden inputs and forbidden side effects;
- proposed status-transition vocabulary;
- anti-overclaim rules;
- manifest/session-ledger consistency checks without applying changes;
- before/after coverage status semantics;
- evidence-basis and known-gap preservation rules;
- privacy and protected-surface requirements;
- validation expectations for a later implementation pass, if separately
  authorized.

This contract does not authorize:

- code implementation;
- metadata diff file generation;
- Markdown or JSON diff artifact writing;
- corpus manifest edits;
- session ledger edits;
- fixture creation;
- golden replay manifest drafting;
- expected-output changes;
- proof file writing;
- private source reads;
- diagnostics, drift, live MTGA, network, firewall, packet, OS/router, or
  private smoke checks;
- private harvest execution;
- fixture-promotion packet creation;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

Corpus / Provenance owns metadata diff vocabulary, status-transition
vocabulary, manifest/session-ledger consistency rules, evidence-basis
preservation rules, and anti-overclaim checks.

Generated / Local Artifacts owns any future local-only diff preview files, if
a later contract explicitly authorizes writing them.

Quality / Governance owns privacy gates, stop conditions, review routing,
protected-surface checks, role handoffs, and non-claim enforcement.

Parser owns event interpretation, routing semantics, parser events, parser
state, match/game identity, deduplication, and final reconciliation.

Golden replay owns replay harness behavior over committed sanitized fixtures
and expected manifests. It does not authorize metadata mutation by itself.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Generated / Local Artifacts, for any future local-only metadata diff files.
- Quality / Governance, for privacy gates, review routing, validation, and
  protected-surface boundaries.
- Parser, as the truth owner for parser facts that metadata entries may
  reference after separate proof.

This contract is not a parser behavior contract, not a private-evidence
execution contract, not a fixture-promotion contract, not a golden replay
fixture contract, not a workbook/transport contract, not an analytics
contract, not an AI/coaching contract, not a CI gate, and not a
release/deploy/production readiness gate.

## Truth Owner

Truth owner for current corpus metadata:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for #384 proof object shape:

- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `tests/test_fixture_promotion_proof.py`

Truth owner for #383 harvest review packet shape:

- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`

Truth owner for this proposed-diff vocabulary:

- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- any later reviewed implementation handoff and contract-test report, if
  implementation is explicitly authorized.

Truth owner for actual corpus metadata mutation remains a future explicit
fixture-promotion issue, contract, implementation, review, submitter, and
deployer path. This contract does not provide that authority.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code.

Potential future allowed data flow, if separately authorized:

```text
#382 candidate summary
  -> #383 harvest review packet
  -> #384 fixture promotion proof object
  -> current corpus manifest and current session ledger snapshots
  -> #386 in-memory proposed metadata diff object
  -> human/Codex review decision
  -> later scoped fixture/manifest draft issue, if approved
```

Potential future local-only file flow, not authorized now:

```text
#386 in-memory metadata diff
  -> local-only corpus_metadata_diff.json / corpus_metadata_diff.md
  -> Codex E review
  -> later fixture-promotion package, if separately authorized
```

Forbidden reverse flow:

- diff objects must not rewrite parser facts;
- diff objects must not create fixtures;
- diff objects must not write golden replay manifests;
- diff objects must not edit expected outputs;
- diff objects must not mutate the corpus manifest;
- diff objects must not mutate the session ledger;
- diff objects must not approve private evidence reads;
- diff objects must not authorize fixture promotion;
- diff status must not activate #388 or #381;
- diff reports must not become parser truth, workbook truth, analytics truth,
  AI truth, coaching truth, merge readiness, deploy readiness, release
  readiness, production readiness, or tracker completion.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`

Expected future review artifact, if this contract is submitted for review:

- `docs/contract_test_reports/parser_evidence_corpus_metadata_diff_generator.md`

Potential future implementation artifacts, not authorized by this contract:

- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `tests/test_corpus_metadata_diff_generator.py`
- `docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md`

Potential future local-only diff artifacts, not authorized by this contract
and not allowed in Git:

- `corpus_metadata_diff.json`
- `corpus_metadata_diff.md`
- local review notes that contain raw/private evidence, exact paths, hashes,
  offsets, screenshots, workbook exports, runtime artifacts, or secrets

Files explicitly not owned by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- any `tests/fixtures/golden_replay/*.manifest.json`
- any expected-output fixture file
- any private/local/generated artifact

## Public Interface

No public runtime interface is authorized now.

Logical future interface, if a later issue authorizes implementation:

```python
build_corpus_metadata_diff(
    *,
    promotion_proof: Mapping[str, Any],
    corpus_manifest: Mapping[str, Any],
    session_ledger: Mapping[str, Any],
    proposed_manifest_entry: Mapping[str, Any] | None = None,
    proposed_session_entry: Mapping[str, Any] | None = None,
    diff_context: Mapping[str, Any] | None = None,
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

- #384 `mythic_edge_fixture_promotion_proof` dictionaries created from
  synthetic or public-safe proof inputs.
- #383 `mythic_edge_harvest_review_packet` identifiers and reduced metadata
  already embedded or referenced by a proof object.
- #382 `mythic_edge_harvest_candidate_summary` identifiers and reduced
  metadata already embedded or referenced by upstream objects.
- In-memory current corpus manifest dictionaries loaded from
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- In-memory current session ledger dictionaries loaded from
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Public-safe proposed manifest entry dictionaries.
- Public-safe proposed session ledger entry dictionaries.
- Public-safe contract, issue, PR, test, and report references.

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

The logical metadata diff object should use this shape if a future
implementation is authorized:

```yaml
object: "mythic_edge_corpus_metadata_diff"
schema_version: "parser_evidence_corpus_metadata_diff.v1"
diff_id: "<stable public-safe id>"
created_at_utc: "<ISO-8601 timestamp or omitted in deterministic tests>"
source:
  promotion_proof_schema_version: "parser_evidence_fixture_promotion_proof.v1"
  proof_id: "..."
  proof_status: "proof_ready_for_review"
  review_packet_id: "..."
  candidate_report_id: "..."
authorization:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
diff_status: "draft"
metadata_targets:
  corpus_manifest: "tests/fixtures/parser_corpus/corpus_manifest.v1.json"
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
proposed_changes:
  manifest_entries: []
  session_entries: []
coverage_transition:
  families: []
  transition_kind: "no_change"
consistency_checks:
  manifest_schema_valid: false
  session_ledger_schema_valid: false
  family_scope_limited: false
  known_gaps_preserved: false
  privacy_flags_preserved: false
  no_metadata_mutation_performed: true
anti_overclaim:
  blocked: false
  reasons: []
non_claims:
  - "not_corpus_status_authority"
  - "not_fixture_promotion_authority"
  - "not_parser_truth"
  - "not_readiness"
```

Required output defaults:

- `parser_behavior_ready=false`
- `pipeline_activation_ready_for_issue_388=false`
- `file_writing_authorized=false`
- `private_harvest_authorized=false`
- `fixture_promotion_authorized=false`
- `corpus_status_change_authorized=false`
- `no_metadata_mutation_performed=true`

## Diff Status Vocabulary

Allowed `diff_status` values:

- `draft`: diff object is syntactically formed but not reviewed.
- `blocked_privacy`: diff cannot proceed because privacy/redaction evidence
  is missing, failed, or ambiguous.
- `blocked_authorization`: diff cannot proceed because required workflow,
  proof, fixture-promotion, file-writing, private-evidence, or metadata
  authority is missing.
- `insufficient_proof`: the #384 proof object is missing, stale, malformed, or
  not strong enough to reason about metadata movement.
- `no_metadata_change`: inputs do not describe a metadata movement candidate.
- `diff_ready_for_review`: diff is ready for human/Codex review as a
  report-only routing artifact.
- `diff_rejected`: diff was reviewed or evaluated and should not be used for
  follow-up planning.
- `blocked_overclaim`: proposed metadata language would overclaim coverage,
  readiness, parser behavior, private evidence, analytics truth, AI truth, or
  coaching truth.
- `needs_contract_update`: the diff requires schema, vocabulary, surface, or
  protected-boundary changes outside this contract.

`diff_ready_for_review` is not corpus-status authority, fixture-promotion
authorization, or file-writing authorization.

## Proposed Change Vocabulary

Allowed proposed change types:

- `no_change`
- `add_manifest_entry`
- `add_session_entry`
- `update_existing_manifest_entry`
- `update_existing_session_entry`
- `status_promotion_candidate`
- `status_correction_candidate`
- `known_gap_update_candidate`
- `review_note_update_candidate`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `needs_contract_update`
- `unknown`

Allowed coverage transition kinds:

- `no_change`
- `report_only_to_synthetic_candidate`
- `report_only_to_committed_candidate`
- `partial_to_synthetic_candidate`
- `partial_to_committed_candidate`
- `missing_to_report_only_candidate`
- `missing_to_synthetic_candidate`
- `blocked_private_evidence_no_change`
- `blocked_external_boundary_no_change`
- `status_correction_candidate`
- `unknown`

The diff may describe a transition candidate only. It must not perform the
transition.

## Status Transition and Anti-Overclaim Rules

All transitions must be explicit, family-scoped, and evidence-scoped.

General rules:

- Only scenario families named by the #384 proof object may appear in proposed
  transition rows.
- Unrelated families must remain absent from the diff or explicitly
  `no_change`.
- Existing report-only rows must remain report-only unless the proposed entry
  has dedicated synthetic or sanitized committed evidence for the same family.
- Existing blocked-private rows must remain blocked unless a separate
  approved private-evidence contract and review path authorizes a public-safe
  summary. This contract does not do that.
- Existing blocked-external rows must remain blocked unless a separate
  evidence-generation or external-boundary contract authorizes movement. This
  contract does not do that.
- `parser_behavior_verified` must not be added unless the proposed evidence
  is a parser-behavior fixture path with explicit validation and a later
  contract authorizes that claim.
- `coverage_basis` values must be preserved or extended only with a
  contract-authorized reason.
- `known_gaps` must not be deleted silently.
- `review_notes` must preserve non-claims when a row moves or gains
  additional evidence.
- `source_privacy` flags must remain false for raw private logs, external
  logs, and local private artifacts unless a future contract explicitly
  changes the corpus privacy model.

`covered_synthetic` candidate rules:

- Requires a proposed synthetic committed fixture or equivalent
  contract-authorized synthetic parser evidence reference.
- Requires privacy-safe metadata only.
- Requires known gaps that state what the synthetic case does not prove.
- Does not imply private smoke success, live parser behavior, release
  readiness, production behavior, analytics truth, AI truth, or coaching truth.

`covered_committed` candidate rules:

- Requires a proposed sanitized committed fixture reference and golden replay
  manifest reference.
- Requires a public-safe proof and review path that is stronger than a
  report-only proof.
- Requires known gaps and review notes preserving scope limits.
- Does not imply full corpus parity, release readiness, production behavior,
  analytics truth, AI truth, or coaching truth.

`covered_report_only` candidate rules:

- May be used to document a boundary, non-claim, metadata-only reference, or
  count-only report.
- Must not include `parser_behavior_verified` unless a separate contract says
  the row is both report-only and behavior-verified for a specific reason.
- Must not be treated as parser behavior readiness.

Anti-overclaim checks must block diffs that:

- add or imply `parser_behavior_ready=true`;
- add or imply `pipeline_activation_ready_for_issue_388=true`;
- add or imply `fixture_promotion_authorized=true`;
- add or imply `corpus_status_change_authorized=true`;
- add `parser_behavior_verified` without approved parser-behavior evidence;
- remove private/external/report-only non-claims;
- remove known gaps without replacement rationale;
- promote unrelated families;
- promote blocked-private or blocked-external families without separate
  authority;
- claim release readiness, production behavior, analytics truth, AI truth, or
  coaching truth.

## Manifest Consistency Rules

A proposed manifest entry must be public-safe and internally consistent.

Required checks:

- manifest object is `mythic_edge_parser_corpus_manifest`;
- manifest schema is `parser_corpus_manifest.v1`;
- proposed `entry_id` is stable and not duplicated unless the change type is
  an explicit update candidate;
- `entry_type` is one of the manifest-supported entry types;
- `source_kind`, `commit_status`, `privacy_class`, `sanitization_status`,
  `coverage_status`, and `coverage_basis` use supported values;
- every `scenario_families` value exists in the corpus taxonomy;
- every proposed path is repo-relative and public-safe;
- no path points to a raw log, compressed external log, SQLite file, workbook
  export, runtime artifact, failed post, private report, or secret-bearing
  artifact;
- `linked_issue` and `authorized_by_contract` are present for non-trivial
  metadata movement;
- `known_gaps` and `review_notes` are present when a row would otherwise look
  broader than the evidence supports;
- `source_privacy` remains unchanged unless a later contract explicitly
  authorizes privacy model changes.

## Session Ledger Consistency Rules

A proposed session ledger entry must be public-safe and internally
consistent.

Required checks:

- session ledger object is `mythic_edge_parser_corpus_session_ledger`;
- session ledger schema is `parser_corpus_session_ledger.v1`;
- proposed `session_id` is stable and not duplicated unless the change type
  is an explicit update candidate;
- session `scenario_families` align with proposed manifest entry families;
- `source_kind`, `commit_status`, `privacy_class`, and
  `sanitization_status` do not exceed the proposed evidence;
- `parser_coverage` counts are reduced metadata only;
- `game_rows` values are reduced metadata only;
- `report_only_redactions` explicitly preserve false flags for raw log lines,
  private paths, raw payloads, local private artifacts, and generated private
  artifacts where applicable;
- `known_gaps` preserve non-claims.

## Privacy and Protected-Surface Requirements

The diff object must fail closed when it sees forbidden raw/private data,
exact local paths, raw hashes, raw payloads, secrets, runtime artifacts,
workbook exports, or generated private artifacts.

The diff object must not touch or authorize changes to:

- parser behavior;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- analytics behavior;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge/deploy/release policy;
- production behavior.

## Invariants

- Metadata diff objects are advisory and report-only.
- Metadata diff objects must preserve all false readiness and authorization
  flags listed in this contract.
- Metadata diff objects must be deterministic for equivalent public-safe
  inputs.
- Metadata diff objects must fail closed on missing, stale, malformed, or
  ambiguous #384 proof inputs.
- Metadata diff objects must not echo forbidden private input values.
- Metadata diff objects must not write files unless a later contract
  explicitly authorizes file writing.
- Metadata diff objects must not read source files, private logs, diagnostics
  outputs, drift reports, network state, OS/router state, workbook exports, or
  runtime artifacts.
- Metadata diff objects must not create fixtures or expected manifests.
- Metadata diff objects must not mutate corpus metadata.
- Metadata diff objects must not activate #388 or #381.
- Metadata diff objects must not alter parser, workbook, webhook, Apps
  Script, analytics, AI, coaching, CI, release, deploy, or production
  behavior.

## Error Behavior

Missing #384 proof object:

- return or record `diff_status=insufficient_proof`.

Malformed #384 proof object:

- return or record `diff_status=needs_contract_update` when the shape is
  unknown, or `diff_status=insufficient_proof` when required fields are
  absent.

Proof not `proof_ready_for_review`:

- return or record `diff_status=insufficient_proof`,
  `blocked_authorization`, or `diff_rejected` depending on proof status.

Forbidden raw/private fields:

- return or record `diff_status=blocked_privacy`;
- do not echo forbidden values in diagnostics or error text.

Missing manifest or session ledger:

- return or record `diff_status=needs_contract_update`.

Invalid manifest/session schema:

- return or record `diff_status=needs_contract_update`.

Proposed overclaim:

- return or record `diff_status=blocked_overclaim`.

Missing file-writing, fixture-promotion, or corpus-status authority:

- return or record `diff_status=blocked_authorization` if the proposed action
  requires actual mutation. A report-only candidate may still be `draft` or
  `diff_ready_for_review` when it makes no mutation and all evidence is
  public-safe.

Contract ambiguity:

- return or record `diff_status=needs_contract_update`.

## Side Effects

No side effects are authorized by this contract.

Forbidden side effects include:

- file writes;
- local artifact writes;
- metadata diff artifact writes;
- fixture writes;
- golden replay manifest writes;
- expected-output writes;
- corpus manifest writes;
- session ledger writes;
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

1. Confirm #386 has an explicit implementation authorization and a clean target
   branch.
2. Re-read this contract, the #384 proof contract, and the corpus parity
   report contract surface.
3. Implement only an in-memory proposed metadata diff object builder.
4. Add synthetic-only focused tests for proof consumption, false readiness
   flags, forbidden-input rejection, anti-overclaim rules, manifest/session
   consistency checks, and no-mutation behavior.
5. Write an implementation handoff comparing behavior to this contract.
6. Route to Codex E for contract-test review.
7. Defer any file writer, metadata diff artifact, fixture draft, golden replay
   manifest draft, fixture-promotion packet, corpus metadata update, or #388
   activation to a separate contract and explicit approval.

## Compatibility

The diff vocabulary must remain compatible with:

- #382 `mythic_edge_harvest_candidate_summary` objects;
- #383 `mythic_edge_harvest_review_packet` objects;
- #384 `mythic_edge_fixture_promotion_proof` objects;
- current corpus manifest schema `parser_corpus_manifest.v1`;
- current session ledger schema `parser_corpus_session_ledger.v1`;
- existing corpus parity status, coverage basis, privacy, and readiness
  vocabulary;
- existing golden replay harness report semantics;
- existing feature-equity report semantics;
- existing privacy and protected-surface checker semantics;
- existing Mythic Edge workflow handoff vocabulary.

Compatibility does not authorize stale start-condition wording from issue
#386. The latest #516/#518/#388 planning contracts and the #381 through #384
sequence control non-activation semantics.

## Tests Required

Documentation-only validation for this contract:

```bash
python3 tools/check_agent_docs.py
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
git diff --check
printf 'docs/contracts/parser_evidence_corpus_metadata_diff_generator.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_corpus_metadata_diff_generator.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_corpus_metadata_diff_generator.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If a later implementation is explicitly authorized, focused tests should
cover:

- missing proof to `insufficient_proof`;
- malformed proof to `needs_contract_update`;
- non-ready proof to `insufficient_proof` or `blocked_authorization`;
- ready proof plus public-safe proposed entries to `diff_ready_for_review`;
- no proposed metadata movement to `no_metadata_change`;
- forbidden private fields to `blocked_privacy`;
- blocked-private family promotion attempt to `blocked_authorization`;
- blocked-external family promotion attempt to `blocked_authorization`;
- unrelated family promotion attempt to `blocked_overclaim`;
- deletion of known gaps to `blocked_overclaim`;
- premature `parser_behavior_verified` to `blocked_overclaim`;
- proposed paths that are not repo-relative to `blocked_privacy`;
- every output preserves false readiness and authorization flags;
- inputs are not mutated;
- no files are written.

## Acceptance Criteria

- The contract clearly distinguishes proposed metadata diffs from corpus
  metadata mutation.
- The contract preserves:
  - `parser_behavior_ready=false`
  - `pipeline_activation_ready_for_issue_388=false`
  - `file_writing_authorized=false`
  - `private_harvest_authorized=false`
  - `fixture_promotion_authorized=false`
  - `corpus_status_change_authorized=false`
  - `implementation_authorized=false`
- The contract defines a logical metadata diff object shape.
- The contract defines diff status vocabulary.
- The contract defines proposed change and coverage transition vocabulary.
- The contract defines anti-overclaim rules.
- The contract defines manifest/session-ledger consistency checks without
  authorizing metadata writes.
- The contract rejects private/raw input classes and protected-surface changes.
- The contract routes next work away from Codex C unless a later lifecycle
  decision explicitly authorizes implementation.

## Next Workflow Action

Next role: Codex A: Thinker / Lifecycle Reconciliation.

Codex C is not authorized by this contract because implementation,
file writing, private harvest, fixture promotion, and corpus status changes
are all still false.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for issue #386 under parser evidence-pipeline tracker #388.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/386

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Completed contract:
docs/contracts/parser_evidence_corpus_metadata_diff_generator.md

Goal:
Decide whether #386 should remain planning-only, receive a separate explicitly authorized synthetic-only in-memory Codex C implementation pass, or wait for later #388 activation. Preserve parser_behavior_ready=false, pipeline_activation_ready_for_issue_388=false, file_writing_authorized=false, fixture_promotion_authorized=false, and corpus_status_change_authorized=false unless a later reviewed implementation and approval path proves otherwise.

Do not implement code. Do not activate #388 or #381. Do not authorize private harvest, fixture promotion, file writing, corpus metadata mutation, fixture creation, golden replay manifest drafting, metadata diff artifact writing, or expected-output changes unless a new scoped issue and contract explicitly approve it. Do not read private logs or run private/live checks.

Expected output:
- lifecycle decision for #386;
- whether Codex C is authorized, and if so the exact synthetic-only in-memory scope;
- updated workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/386"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/384"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/523"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #386 reconciliation comment"
  target_artifact: "docs/contracts/parser_evidence_corpus_metadata_diff_generator.md"
  verdict: "planning_contract_complete_implementation_not_authorized"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "d31ebb8fa773edbd784a873c57b07f7bbbc97478"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null"
    - "python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "git diff --check"
    - "printf 'docs/contracts/parser_evidence_corpus_metadata_diff_generator.md\\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf 'docs/contracts/parser_evidence_corpus_metadata_diff_generator.md\\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf 'docs/contracts/parser_evidence_corpus_metadata_diff_generator.md\\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not close tracker #388 without explicit lifecycle approval."
    - "Do not close or bypass parent private-evidence issue #434."
    - "Do not activate #388 or #381."
    - "Do not route directly to Codex C without a new lifecycle authorization."
    - "Do not implement code, write metadata diff files, create fixtures, draft golden replay manifests, mutate corpus metadata, change expected outputs, or promote corpus rows."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not claim parser behavior readiness, fixture promotion authorization, private harvest authorization, corpus status change authorization, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
