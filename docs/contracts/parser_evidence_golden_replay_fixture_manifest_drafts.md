# Parser Evidence Golden Replay Fixture And Manifest Drafts Contract

## Module

Planning-only contract for issue #385, the golden replay fixture and manifest
draft boundary in the parser evidence-pipeline lane.

Plain English: this contract defines how Mythic Edge may later describe a
minimal sanitized golden replay fixture draft and matching golden replay
manifest draft for a reviewed evidence candidate. Drafts are review artifacts
only. They must not write fixture files, write manifest files, edit expected
outputs, mutate corpus metadata, authorize private harvest, promote corpus
rows, activate the parser evidence pipeline, or decide parser truth.

This Codex B pass does not implement code, write fixture drafts, write golden
replay manifests, write expected-output files, edit corpus metadata, run or
read private logs, create fixture-promotion packets, promote corpus rows,
activate #388 or #381, or claim parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/385
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/386
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/530
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Risk tier: High
- Previous merge commit: `b11351e99b025486be442c0c49a67b13288ac3d9`

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` and `origin/main` are at
  `b11351e99b025486be442c0c49a67b13288ac3d9`.
- Issue #386 is closed.
- PR #530 is merged.
- Issue #385 is open.
- Tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #385 still contains stale all-45 coverage start-condition wording.
  The latest #385 reconciliation comment routes this issue to Codex B for
  planning-only contract work and explicitly preserves non-activation.

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
- Issue #385 and its latest Codex A reconciliation comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #386 and PR #530
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/implementation_handoffs/parser_evidence_fixture_promotion_proof_comparison.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `tests/test_corpus_metadata_diff_generator.py`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `tests/test_fixture_promotion_proof.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- Existing committed golden replay manifests as public reference only
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

## Observed Current Behavior

Issue #384 added a synthetic-only, in-memory fixture promotion proof builder.
Observed #384 behavior:

- `build_fixture_promotion_proof(...)` builds deterministic
  `mythic_edge_fixture_promotion_proof` dictionaries from supplied #383 review
  packets, public-safe coverage summaries, public-safe check references, and
  optional public-safe proof context.
- Proofs can reach `proof_ready_for_review` when an approved #383 review
  packet and passing public-safe check references are supplied.
- Proofs remain report-only and preserve false readiness and authorization
  flags.
- #384 did not add file writing, private harvest, fixture creation, corpus
  metadata mutation, golden replay manifest drafting, #388 activation, or
  parser behavior changes.

Issue #386 added a synthetic-only, in-memory corpus metadata diff builder.
Observed #386 behavior:

- `build_corpus_metadata_diff(...)` builds deterministic
  `mythic_edge_corpus_metadata_diff` dictionaries from supplied in-memory #384
  proof objects, current corpus manifest dictionaries, current session ledger
  dictionaries, optional public-safe proposed manifest/session entries, and
  optional public-safe diff context.
- Diff objects can reach `diff_ready_for_review` or `no_metadata_change`, but
  they do not mutate metadata.
- Diff objects reject raw/private values, blocked private/external status
  movement, premature `parser_behavior_verified`, unrelated family promotion,
  known-gap deletion, and truth/readiness overclaims.
- #386 did not write metadata diff files, proof files, fixtures, golden replay
  manifests, expected outputs, corpus manifest edits, or session ledger edits.

Current golden replay behavior:

- `src/mythic_edge_parser/app/golden_replay.py` owns committed golden replay
  report behavior for explicit manifest paths.
- Existing committed manifests use object
  `mythic_edge_golden_replay_manifest` and schema
  `parser_golden_replay_manifest.v1`.
- Existing expected manifest sections include:
  - `router_stats`
  - `event_family_counts`
  - `event_kind_sequence`
  - `diagnostics_summary`
  - `truncation_and_data_loss`
  - `unknowns_and_degradation`
  - `parser_state`
  - `final_reconciliation`
  - `parser_owned_rows`
- Golden replay compares parser-owned outputs from committed sanitized or
  synthetic fixtures. It does not infer missing facts or authorize fixture
  creation.

There is no dedicated fixture/manifest draft object contract, draft generator
module, file writer, focused test file, committed draft artifact, or local
generated draft artifact for issue #385.

## Problem

#384 proof objects can explain whether a candidate might be worth later
fixture-promotion review. #386 metadata diff objects can describe proposed
corpus metadata movement if a candidate were approved. #385 sits between
those objects and actual committed golden replay evidence: it needs a stable
draft vocabulary for proposed fixture content and proposed manifest expected
sections.

That boundary is useful, but high risk. A future draft generator is close to
raw local evidence, sanitized fixture creation, expected-output truth, corpus
status changes, parser behavior claims, and readiness claims. Without a
contract, a future implementation could accidentally write private evidence,
turn draft expected output into parser truth, over-broaden a fixture window,
edit corpus metadata, or treat a draft as fixture-promotion authority.

The first bad value is treating any of these as parser truth, corpus status
truth, fixture-promotion authority, file-writing authority, private-evidence
approval, golden replay readiness, #388 activation, release readiness,
production readiness, analytics truth, AI truth, coaching truth, or tracker
completion:

- a #382 candidate summary;
- a #383 harvest review packet;
- a #384 proof object;
- a #386 metadata diff object;
- a proposed fixture draft;
- a proposed golden replay manifest draft;
- a public-safe parser-owned expected fact preview;
- a passing golden replay check reference;
- a Codex-readable draft summary.

## Scope Decision

This contract approves a planning boundary only.

Codex C implementation is not authorized by this contract. File writing is not
authorized by this contract. Fixture promotion is not authorized by this
contract. The next workflow step should be Codex A or an equivalent lifecycle
decision about whether #385 should remain planning-only, receive a separate
synthetic/in-memory Codex C implementation pass, or wait for later #388
activation.

This contract defines:

- the logical golden replay fixture-draft object;
- the logical golden replay manifest-draft object;
- optional packet vocabulary that groups a fixture draft and manifest draft;
- accepted inputs from #383 review packets, #384 proof objects, #386 metadata
  diff objects, current corpus manifest, current session ledger, and
  public-safe parser-owned expected fact previews;
- forbidden inputs and forbidden side effects;
- draft status vocabulary and anti-overclaim rules;
- fixture minimization rules and refusal rules;
- parser-owned expected section boundaries;
- provenance and review-gate requirements;
- privacy and protected-surface requirements;
- validation expectations for a later implementation pass, if separately
  authorized.

This contract does not authorize:

- code implementation;
- fixture file writing;
- golden replay manifest file writing;
- expected-output file writing;
- proof file writing;
- metadata diff file writing;
- fixture-promotion packet writing;
- local generated draft artifact writing;
- corpus manifest edits;
- session ledger edits;
- private source reads;
- diagnostics, drift, live MTGA, network, firewall, packet, OS/router, or
  private smoke checks;
- private harvest execution;
- fixture promotion;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Quality / Governance support.

Corpus / Provenance owns draft vocabulary, provenance links, draft status
vocabulary, manifest/session-ledger compatibility expectations, known-gap
preservation, and non-claim language.

Generated / Local Artifacts owns any future local-only draft files, if a
later contract explicitly authorizes writing them.

Parser owns event interpretation, routing semantics, parser events, parser
state, match/game identity, deduplication, and final reconciliation.

Golden replay owns replay behavior over committed sanitized fixtures and
explicit manifests. It does not authorize draft truth, fixture creation, or
corpus metadata mutation by itself.

Quality / Governance owns privacy gates, stop conditions, role routing,
protected-surface checks, and non-claim enforcement.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Generated / Local Artifacts, for any future local-only draft files.
- Quality / Governance, for privacy gates, review routing, validation, and
  protected-surface boundaries.
- Parser, as the truth owner for parser fact previews referenced by drafts.

This contract is not a parser behavior contract, not a private-evidence
execution contract, not a fixture-promotion contract, not a metadata mutation
contract, not a workbook/transport contract, not an analytics contract, not
an AI/coaching contract, not a CI gate, and not a release/deploy/production
readiness gate.

## Truth Owner

Truth owner for parser facts remains the existing parser, router, event,
state, match/game identity, deduplication, and final reconciliation layers.

Truth owner for #383 harvest review packet shape:

- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`

Truth owner for #384 proof object shape:

- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `tests/test_fixture_promotion_proof.py`

Truth owner for #386 metadata diff object shape:

- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `tests/test_corpus_metadata_diff_generator.py`

Truth owner for committed golden replay manifest/report behavior:

- `docs/contracts/parser_golden_replay_harness.md`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`

Truth owner for current corpus metadata:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for this draft vocabulary:

- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- any later reviewed implementation handoff and contract-test report, if
  implementation is explicitly authorized.

Draft objects must not own parser facts, private log content, fixture
promotion, golden replay expected truth, corpus status movement, merge
readiness, release readiness, production behavior, analytics truth, AI truth,
or coaching truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code.

Potential future allowed data flow, if separately authorized:

```text
#383 harvest review packet
  -> #384 fixture promotion proof
  -> #386 corpus metadata diff
  -> #385 fixture/manifest draft packet
  -> later reviewed fixture-promotion workflow
  -> later committed sanitized fixture and golden replay manifest
```

Forbidden reverse flow:

```text
draft packet
  -> parser truth
  -> corpus metadata mutation
  -> fixture promotion
  -> private harvest approval
  -> readiness claims
```

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`

Expected future review artifact, if this contract is reviewed:

- `docs/contract_test_reports/parser_evidence_golden_replay_fixture_manifest_drafts.md`

Potential future implementation artifacts, only if separately authorized:

- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
- `tests/test_golden_replay_fixture_manifest_drafts.py`
- `docs/implementation_handoffs/parser_evidence_golden_replay_fixture_manifest_drafts_comparison.md`

Files referenced but not owned or authorized for modification by this
contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- existing files under `tests/fixtures/golden_replay/`
- existing fixture slices under `tests/fixtures/`
- `src/mythic_edge_parser/app/golden_replay.py`
- parser, router, diagnostics, drift, evidence-ledger, workbook, analytics,
  AI, and runtime surfaces.

## Public API Boundary

No public API is authorized by this Codex B pass.

If a later lifecycle decision explicitly authorizes a synthetic/in-memory
implementation, the public behavior should preserve this logical shape. Exact
Python names may vary, but the semantics must not:

```python
def build_golden_replay_fixture_manifest_draft_packet(
    *,
    harvest_review_packet: Mapping[str, Any],
    promotion_proof: Mapping[str, Any],
    metadata_diff: Mapping[str, Any] | None,
    corpus_manifest: Mapping[str, Any],
    session_ledger: Mapping[str, Any],
    parser_expected_fact_preview: Mapping[str, Any] | None = None,
    draft_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...
```

Required future API properties, if separately authorized:

- pure in-memory operation;
- deterministic output for deterministic inputs;
- no file reads beyond supplied in-memory dictionaries;
- no file writes;
- no mutation of input dictionaries;
- no private path, raw line, raw hash, local artifact, token, credential, or
  hostile payload echo in returned values;
- all readiness and authorization flags preserved as false.

## Logical Draft Packet Shape

A future in-memory implementation may return a packet object to group the
fixture draft and manifest draft:

```yaml
object: "mythic_edge_golden_replay_fixture_manifest_draft_packet"
schema_version: "parser_evidence_golden_replay_fixture_manifest_drafts.v1"
packet_id: "public-safe-deterministic-id"
draft_status: "draft_ready_for_review"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/385"
authorized_by_contract: "docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md"
source_artifacts:
  harvest_review_packet_id: "..."
  promotion_proof_id: "..."
  metadata_diff_id: "..."
readiness_flags:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
authorization_flags:
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
fixture_draft: {}
manifest_draft: {}
review_gates: []
privacy: {}
non_claims: []
```

The packet is optional. If future implementation returns separate fixture and
manifest draft objects instead, each object must still carry equivalent
status, provenance, privacy, authorization, and non-claim fields.

## Logical Fixture-Draft Object

Required object identity:

```yaml
object: "mythic_edge_golden_replay_fixture_draft"
schema_version: "parser_evidence_golden_replay_fixture_draft.v1"
```

Required fields:

- `fixture_draft_id`: stable public-safe identifier.
- `draft_status`: one of the status values defined in this contract.
- `scenario_families`: non-empty list scoped to the reviewed candidate.
- `parser_event_families`: list of parser event families expected in the
  candidate, if public-safe and parser-owned.
- `source_kind`: proposed source class.
- `source_privacy_class`: proposed privacy class.
- `sanitization_status`: proposed sanitization status.
- `raw_private_log_committed`: must be false.
- `file_writing_authorized`: must be false unless a later contract explicitly
  changes this value.
- `proposed_fixture_path`: optional repo-relative proposal only; must not be
  written by this contract.
- `fixture_window_summary`: count-only and symbolic window description.
- `minimization`: scope and refusal evidence.
- `redaction_summary`: public-safe redaction categories and booleans only.
- `parser_fact_preview_refs`: references to public-safe parser-owned expected
  fact preview sections, if supplied.
- `source_artifacts`: #383/#384/#386 public-safe identifiers.
- `review_gates`: gates required before any future file writing.
- `known_gaps`: preserved known gaps.
- `non_claims`: required non-claims.

Allowed `source_kind` values:

- `synthetic_player_log_slice_draft`
- `sanitized_player_log_slice_draft`
- `metadata_only_fixture_draft`

Allowed `source_privacy_class` values:

- `synthetic_committable_candidate`
- `sanitized_committable_candidate`
- `committed_count_only`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `requires_review`

Allowed `sanitization_status` values:

- `synthetic`
- `sanitized_draft`
- `not_applicable_count_only`
- `requires_review`
- `blocked_privacy`

Fixture drafts must not include raw line text, raw JSON payloads, local
absolute paths, raw hashes, byte offsets from private files, source file sizes,
timestamps that identify a private play session, decklists, private strategy
notes, screenshots, workbook exports, failed posts, runtime artifacts,
credentials, tokens, API keys, webhook URLs, or exact private evidence
locations.

## Logical Manifest-Draft Object

Required object identity:

```yaml
object: "mythic_edge_golden_replay_manifest_draft"
schema_version: "parser_evidence_golden_replay_manifest_draft.v1"
```

Required fields:

- `manifest_draft_id`: stable public-safe identifier.
- `draft_status`: one of the status values defined in this contract.
- `proposed_manifest_path`: optional repo-relative proposal only; must not be
  written by this contract.
- `proposed_fixture_path`: optional repo-relative proposal only; must match
  the fixture draft if supplied.
- `manifest_object`: should be `mythic_edge_golden_replay_manifest` for a
  future committed manifest.
- `manifest_schema_version`: should be `parser_golden_replay_manifest.v1`
  unless a later golden replay contract changes the schema.
- `source`: public-safe proposed source metadata.
- `coverage`: scenario families, parser event families, known gaps, expected
  degradation, truncation/data-loss expectations, and non-claims.
- `expected_draft`: public-safe parser-owned expected sections.
- `parser_owned_expected_sections`: explicit list of expected sections
  included in the draft.
- `forbidden_expected_sections`: explicit list of excluded downstream or
  unsafe sections.
- `source_artifacts`: #383/#384/#386 public-safe identifiers.
- `review_gates`: gates required before any future committed manifest.
- `authorization_flags`: all false by default.

Manifest drafts must be visibly different from committed manifests. They must
carry `draft_status`, `file_writing_authorized=false`, and explicit non-claim
language. A draft must not be stored under `tests/fixtures/golden_replay/` by
default. A future file-writing contract must decide whether local-only draft
paths are allowed and where they live.

## Accepted Inputs

Future implementation, if separately authorized, may accept only supplied
in-memory, public-safe objects from these sources:

- #383 harvest review packets:
  - object: `mythic_edge_harvest_review_packet`
  - schema version: `parser_evidence_harvest_review_packet.v1`
  - accepted statuses: reviewer-approved or review-ready statuses defined by
    the #383 contract and implementation.
- #384 fixture promotion proof objects:
  - object: `mythic_edge_fixture_promotion_proof`
  - schema version: `parser_evidence_fixture_promotion_proof.v1`
  - expected ready status: `proof_ready_for_review`.
- #386 corpus metadata diff objects:
  - object: `mythic_edge_corpus_metadata_diff`
  - schema version: `parser_evidence_corpus_metadata_diff.v1`
  - accepted statuses: `diff_ready_for_review` or `no_metadata_change`.
- Current corpus manifest dictionaries:
  - object: `mythic_edge_parser_corpus_manifest`
  - schema version: `parser_corpus_manifest.v1`.
- Current session ledger dictionaries:
  - object: `mythic_edge_parser_corpus_session_ledger`
  - schema version: `parser_corpus_session_ledger.v1`.
- Public-safe parser-owned expected fact previews supplied as dictionaries.

Accepted parser-owned expected fact previews may include:

- router statistics;
- event family counts;
- event kind sequence;
- diagnostics summary fields that are already report-safe;
- truncation and data-loss counts or symbolic events;
- unknown-entry and degradation counts or symbolic signatures;
- parser state fields already allowed in golden replay manifests;
- final reconciliation fields produced by parser state, not re-inferred by
  the draft generator;
- parser-owned row previews already allowed by the golden replay harness;
- explicit known gaps and expected degradation notes.

Each parser fact preview must include a source reference tying it to an
accepted #383/#384/#386 object or current public committed fixture. Preview
sections without source references must be treated as `insufficient_review`.

## Forbidden Inputs

Future implementation must reject or refuse:

- raw private `Player.log` contents;
- raw private `UTC_Log` contents;
- raw line text;
- raw JSON payload values from local evidence;
- private app-data contents;
- exact private local file paths;
- raw hashes or hash lists from private files;
- private file offsets or file sizes;
- screenshots;
- workbook exports;
- runtime status files;
- failed posts;
- SQLite files;
- generated/private artifacts;
- secrets, credentials, tokens, API keys, webhook URLs, or Apps Script URLs;
- decklists, deck names, deck IDs, private strategy notes, card choices, or
  private sideboarding notes;
- live MTGA, diagnostics, drift, network, firewall/drop, packet, OS/router, or
  private smoke check outputs;
- Manasight raw logs, compressed corpus files, parser source, or external
  corpus contents;
- downstream analytics, AI, coaching, workbook, dashboard, or Apps Script
  interpretations as expected parser facts.

Forbidden inputs must produce `blocked_privacy`, `blocked_authorization`, or
`blocked_overclaim` without echoing the supplied forbidden value.

## Draft Status Vocabulary

Allowed draft statuses:

- `draft`: object is well-formed but not ready for review.
- `draft_ready_for_review`: object is public-safe, minimal, sourced, and ready
  for a review thread; it is still not file-writing or promotion authority.
- `blocked_privacy`: input or proposed output contains forbidden private or
  sensitive material.
- `blocked_authorization`: requested source class, row status, or side effect
  requires authority this contract does not provide.
- `insufficient_review`: upstream review packet or reviewer decision is
  missing, malformed, or not approved enough for draft construction.
- `insufficient_proof`: #384 proof is missing, malformed, rejected, or not
  `proof_ready_for_review`.
- `insufficient_metadata_diff`: #386 metadata diff is missing, malformed, or
  not in an accepted status when metadata movement is part of the draft.
- `insufficient_parser_preview`: parser-owned expected fact preview is absent,
  unsourced, malformed, or outside the golden replay expected-section
  boundary.
- `refused_oversized_window`: proposed fixture window is too large to be a
  minimal golden replay candidate.
- `refused_ambiguous_window`: proposed fixture window cannot be tied to a
  stable scenario family, event family, or parser-owned expected fact preview.
- `refused_multi_family_window`: proposed fixture window spans unrelated
  scenario families that require separate contracts or separate drafts.
- `blocked_overclaim`: draft attempts to claim parser truth, fixture
  promotion, corpus status movement, private smoke success, readiness, or
  downstream truth.
- `draft_rejected`: reviewer or deterministic check rejects the draft.
- `needs_contract_update`: input schema or requested output is outside this
  contract.

Status precedence for a future implementation:

```text
blocked_privacy
blocked_authorization
blocked_overclaim
needs_contract_update
insufficient_review
insufficient_proof
insufficient_metadata_diff
insufficient_parser_preview
refused_oversized_window
refused_ambiguous_window
refused_multi_family_window
draft_rejected
draft
draft_ready_for_review
```

## Fixture Minimization Rules

Fixture drafts must describe the smallest plausible replay slice that could
support the reviewed parser-owned behavior.

Required minimization rules:

- A fixture draft should cover one primary scenario family unless a contract
  explicitly allows a combined family.
- A fixture draft should list the intended parser event families and exclude
  unrelated families.
- A fixture draft should state why each proposed line class or symbolic
  section is needed.
- A fixture draft should prefer synthetic or already sanitized evidence.
- A fixture draft must preserve ordering only to the extent parser behavior
  requires.
- A fixture draft must keep timestamps synthetic, redacted, or symbolic unless
  timestamp behavior is the contracted subject.
- A fixture draft must use relationship-preserving placeholders for IDs when
  identity relationships are parser-relevant.
- A fixture draft must refuse broad windows, whole sessions, full matches with
  unrelated actions, private deck data, hidden-card evidence, and strategy
  notes unless a later contract explicitly narrows and authorizes them.

Refusal requirements:

- Overbroad or whole-session windows must return `refused_oversized_window`.
- Ambiguous windows without enough parser-owned expected fact preview must
  return `refused_ambiguous_window`.
- Windows spanning unrelated scenario families must return
  `refused_multi_family_window`.
- Private or raw input must return `blocked_privacy`.
- Blocked private/external corpus families must return
  `blocked_authorization` unless a later private-evidence or external-boundary
  contract explicitly authorizes the source class.

## Parser-Owned Expected Section Boundary

Manifest drafts may include only expected sections that the golden replay
harness already treats as parser-owned or that a later golden replay contract
adds explicitly.

Allowed expected sections for v1 drafts:

- `router_stats`
- `event_family_counts`
- `event_kind_sequence`
- `diagnostics_summary`
- `truncation_and_data_loss`
- `unknowns_and_degradation`
- `parser_state`
- `final_reconciliation`
- `parser_owned_rows`

Expected section rules:

- `router_stats` may include routed, unknown, timestamp-missing, and
  timestamp-parse-failure counts.
- `event_family_counts` and `event_kind_sequence` may include parser event
  families and event kinds, not raw payloads.
- `diagnostics_summary` may include public-safe pass/review/fail/degraded
  summaries, not raw diagnostics artifacts.
- `truncation_and_data_loss` may include counts and symbolic event classes,
  not reconstructed missing GameState data.
- `unknowns_and_degradation` may include counts and symbolic signatures, not
  raw unknown lines or hostile marker contents.
- `parser_state` may include parser-owned state fields that are already
  allowed in committed golden replay manifests.
- `final_reconciliation` may include parser-produced match/game result fields
  only when supplied by parser-owned preview evidence; the draft generator
  must not reconcile or infer winners itself.
- `parser_owned_rows` may include row previews already allowed by the golden
  replay harness. They are parser-owned output previews, not workbook truth.

Forbidden expected sections:

- workbook formulas or workbook schema truth;
- dashboard logic;
- Apps Script behavior;
- webhook delivery truth;
- Google Sheets sync truth;
- analytics aggregates or statistical claims;
- AI/model-provider output;
- coaching advice;
- gameplay advice;
- player-mistake labels;
- hidden-card inference;
- archetype classification;
- complete decklists;
- sealed pools, draft pools, private decklists, deck names, or sideboard
  strategy notes;
- release, deploy, production, merge, or tracker-completion claims.

## Provenance And Review Gates

Each draft object must carry provenance sufficient for review without exposing
private evidence:

- source repository and repository URL;
- issue #385;
- tracker #388;
- parent private-evidence issue #434;
- upstream #383 review packet identifier;
- upstream #384 proof identifier;
- upstream #386 metadata diff identifier, if used;
- current corpus manifest schema version;
- current session ledger schema version;
- proposed scenario families;
- proposed parser event families;
- public-safe check references, if supplied;
- explicit non-claims.

Required review gates before any future file writing:

- #383 review packet accepted by its own contract.
- #384 proof object reaches `proof_ready_for_review`.
- #386 metadata diff is `diff_ready_for_review` or explicitly
  `no_metadata_change`.
- Privacy checks pass without raw/private value echo.
- Protected-surface checks pass.
- The draft remains minimal and public-safe.
- Parser-owned expected fact preview is source-labeled and does not include
  downstream truth.
- A later contract explicitly authorizes file writing and names the target
  artifact locations.
- A later reviewer/submitter/deployer path approves any corpus metadata
  change.

## Privacy Requirements

Draft objects must preserve:

```yaml
raw_private_log_committed: false
private_paths_included: false
raw_payloads_included: false
local_private_artifacts_committed: false
external_logs_committed: false
```

Drafts may contain only:

- repo-relative proposed paths;
- public issue and PR URLs;
- public contract paths;
- synthetic IDs;
- redaction category names;
- symbolic parser event family names;
- count-only summaries;
- public-safe known-gap statements;
- public-safe validation command names.

Drafts must not contain:

- local absolute paths;
- private source filenames;
- private source offsets;
- private source file sizes;
- raw hashes of private source material;
- raw lines;
- raw payloads;
- exact timestamps from a private play session;
- account IDs, display names, opponent identifiers, machine names, local user
  names, or source paths;
- credentials, tokens, keys, or URLs that identify private infrastructure.

## Anti-Overclaim Rules

Drafts must include explicit non-claims:

- not parser truth;
- not golden replay pass evidence;
- not fixture-promotion authority;
- not file-writing authority;
- not corpus metadata mutation authority;
- not corpus status movement;
- not private-evidence approval;
- not #388 or #381 activation;
- not `parser_behavior_ready=true`;
- not release readiness;
- not deploy readiness;
- not production readiness;
- not analytics truth;
- not AI truth;
- not coaching truth;
- not full parser regression parity.

A future implementation must return `blocked_overclaim` if an input or draft
attempts to:

- set `parser_behavior_ready=true`;
- set `pipeline_activation_ready_for_issue_388=true`;
- set `file_writing_authorized=true` without a later contract;
- set `fixture_promotion_authorized=true`;
- set `corpus_status_change_authorized=true`;
- set `private_harvest_authorized=true`;
- remove known gaps without explicit proof;
- promote a blocked, private-evidence, external-boundary, or report-only row
  without a later contract;
- replace parser-owned expected facts with workbook, analytics, AI, coaching,
  or human interpretation.

## Error And Malformed Input Behavior

Future implementation must fail closed:

- Missing or malformed #383 review packet returns `insufficient_review` or
  `needs_contract_update`.
- Missing, malformed, rejected, or non-ready #384 proof returns
  `insufficient_proof` or the corresponding blocked status.
- Missing, malformed, rejected, or non-ready #386 metadata diff returns
  `insufficient_metadata_diff` when metadata movement is requested.
- Missing or unsourced parser-owned expected preview returns
  `insufficient_parser_preview`.
- Forbidden raw/private values return `blocked_privacy` without value echo.
- Blocked private/external source classes return `blocked_authorization`.
- Unsupported schema versions return `needs_contract_update`.
- Overclaim attempts return `blocked_overclaim`.
- Overbroad fixture windows return the appropriate refusal status.

Malformed input handling must preserve deterministic output shape, false
readiness flags, false authorization flags, and sanitized diagnostic messages.

## Side Effects

This contract authorizes no side effects beyond writing this contract file.

Future implementation, if separately authorized for in-memory draft objects,
must still have no side effects:

- no fixture files;
- no golden replay manifest files;
- no expected-output files;
- no proof files;
- no metadata diff files;
- no fixture-promotion packets;
- no local-only draft files;
- no corpus manifest edits;
- no session ledger edits;
- no private source reads;
- no diagnostics, drift, live MTGA, network, firewall/drop, packet, OS/router,
  or private smoke checks;
- no parser behavior changes;
- no runtime status changes.

File writing remains deferred by default. Any future file-writing path must
receive a separate contract that names allowed artifact locations, retention
rules, validation, privacy scans, and review gates.

## Compatibility Expectations

Future draft objects must remain compatible with:

- #383 harvest review packet vocabulary;
- #384 fixture promotion proof vocabulary;
- #386 corpus metadata diff vocabulary;
- current golden replay manifest expected sections;
- current corpus manifest and session ledger schema versions;
- current corpus parity report readiness semantics;
- current #388 planning-only umbrella semantics.

Compatibility rules:

- Existing committed fixtures and manifests must not be edited by #385.
- Existing corpus metadata must not be edited by #385.
- Existing golden replay report behavior must not be changed by #385.
- Draft object schemas must be versioned.
- New fields must be additive unless a later contract explicitly revises the
  schema.
- Draft objects must be safe to render in Markdown without leaking private
  data.

## Validation Expectations For Future Implementation

If a later lifecycle decision explicitly authorizes a synthetic/in-memory
Codex C implementation, focused tests must cover:

- ready public-safe #383/#384/#386 inputs produce
  `draft_ready_for_review`;
- missing #383 review packet produces `insufficient_review`;
- missing or non-ready #384 proof produces `insufficient_proof`;
- missing or non-ready #386 metadata diff produces
  `insufficient_metadata_diff` when needed;
- missing or unsourced parser expected preview produces
  `insufficient_parser_preview`;
- raw/private values anywhere in accepted inputs produce `blocked_privacy`
  without echo;
- blocked private/external source classes produce `blocked_authorization`;
- overclaim attempts produce `blocked_overclaim`;
- oversized, ambiguous, and multi-family windows produce their refusal
  statuses;
- fixture draft and manifest draft preserve false readiness and authorization
  flags;
- generated draft objects are deterministic and do not mutate inputs;
- parser-owned expected section allowlist is enforced;
- forbidden downstream expected sections are rejected;
- known gaps are preserved unless explicitly supported by upstream proof;
- no file writes occur.

Suggested validation commands for a future implementation:

```bash
python3 -m pytest -q tests/test_golden_replay_fixture_manifest_drafts.py
python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

If future implementation changes code, it must also run path-scoped secret,
protected-surface, and validation-selector checks for changed paths.

## Acceptance Criteria

This Codex B contract is complete when:

- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
  exists.
- The contract defines logical fixture-draft and manifest-draft objects.
- The contract defines accepted inputs, forbidden inputs, draft statuses,
  minimization/refusal rules, parser-owned expected section boundaries,
  provenance requirements, privacy requirements, and validation expectations.
- The contract preserves #388 inactive status and all false readiness and
  authorization flags.
- The contract explicitly states that file writing remains deferred by
  default.
- The contract routes the next role without authorizing implementation by
  itself.

## Recommended Next Role

Recommended next role: Codex A: Thinker / Lifecycle Reconciliation.

Reason: issue #385 is now contract-defined, but implementation remains
unauthorized by the latest issue reconciliation and by this contract. Codex A
should decide whether to keep #385 planning-only, create an explicit
implementation authorization comment for a synthetic/in-memory Codex C pass,
or defer implementation until later #388 activation work.

Codex C should run only after a separate lifecycle decision explicitly
authorizes implementation and preserves the no-file-writing boundary.

## Validation Performed During Codex B

The following validation was run after creating this contract:

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Observed corpus parity output remained:

```text
partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

No code, fixture, manifest, expected-output, proof, metadata, local generated,
or private-evidence artifacts were created.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker / Lifecycle Reconciliation for issue #385.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/385

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/386

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/530

Latest merge commit:
b11351e99b025486be442c0c49a67b13288ac3d9

Source contract:
docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md

Goal:
Reconcile the completed #385 planning-only contract and decide the next
lifecycle route.

Decide whether #385 should:
- remain planning-only;
- route to Codex E for contract review;
- receive a separate explicit authorization for a synthetic/in-memory Codex C
  implementation; or
- defer implementation until later #388 activation work.

Preserve:
- parser_behavior_ready=false
- pipeline_activation_ready_for_issue_388=false
- file_writing_authorized=false
- private_harvest_authorized=false
- fixture_promotion_authorized=false
- corpus_status_change_authorized=false

Do not implement code.
Do not create fixture files, golden replay manifest files, expected-output
files, proof files, metadata diff files, fixture-promotion packets, corpus
metadata edits, or local/generated artifacts.
Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks.
Do not promote blocked, report-only, private-evidence, or external-boundary rows.
Do not claim parser behavior readiness, pipeline activation readiness, fixture
promotion readiness, release readiness, production readiness, analytics truth,
AI truth, coaching truth, or full parser regression parity.

Expected output:
- Lifecycle decision
- Recommended next role
- Any issue/tracker comment text, if appropriate
- workflow_handoff block with repository and repository_url
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/385"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/386"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/530"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #385 reconciliation comment"
  target_artifact: "docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md"
  verdict: "golden_replay_fixture_manifest_draft_contract_complete_planning_only"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "b11351e99b025486be442c0c49a67b13288ac3d9"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  stop_conditions:
    - "Do not implement code without a separate lifecycle authorization."
    - "Do not create fixture files, golden replay manifest files, expected-output files, proof files, metadata diff files, fixture-promotion packets, corpus metadata edits, or local/generated artifacts."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not proceed to private harvest execution."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
