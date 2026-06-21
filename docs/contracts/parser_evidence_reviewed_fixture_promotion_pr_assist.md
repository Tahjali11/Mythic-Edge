# Parser Evidence Reviewed Fixture Promotion PR-Assist Contract

## Module

Planning-only contract for issue #387, the PR-assist workflow boundary for
reviewed fixture-promotion packages in the parser evidence-pipeline lane.

Plain English: this contract defines how Mythic Edge may later assemble a
review-only PR-assist packet for a reviewed fixture-promotion candidate. The
packet may summarize intended files, validation evidence, protected-surface
checks, privacy checks, issue links, and draft PR text. It must not stage
files, create commits, push branches, open or edit PRs, merge, close issues,
update trackers as completed, write fixture files, mutate corpus metadata,
promote fixtures, authorize private harvest, or decide parser truth.

This Codex B pass does not implement code, open a PR, create a PR branch,
stage files, commit, push, write PR-assist output files, write fixtures, write
golden replay manifests, write expected outputs, edit corpus metadata, run or
read private logs, promote corpus rows, activate #388 or #381, or claim parser
behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/387
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/385
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/536
- Previous merge commit: `421fc14783fa8582ecb34595dfd4692273ff77ef`
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` and `origin/main` are at
  `421fc14783fa8582ecb34595dfd4692273ff77ef`.
- Issue #385 is closed and PR #536 is merged.
- Issue #387 is open.
- Tracker #388 remains open and inactive.
- Parent private-evidence issue #434 remains open.
- Issue #387's original all-45 synthetic-or-stronger start wording is stale
  for planning-only work. The latest #387 reconciliation comment, current
  #388 body, #516 activation criteria update, and #518 planning umbrella
  contract authorize Codex B planning work only.

Current readiness and authorization facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
pr_creation_authorized: false
staging_authorized: false
commit_authorized: false
push_authorized: false
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #387 and its Codex A reconciliation comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #385 and PR #536
- `.github/pull_request_template.md`
- `docs/templates/workflow_handoff.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/implementation_handoffs/parser_evidence_golden_replay_fixture_manifest_drafts_comparison.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/implementation_handoffs/parser_evidence_fixture_promotion_proof_comparison.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`

## Observed Current Behavior

Issue #383 supplies synthetic-only in-memory harvest review packet objects.
Issue #384 supplies synthetic-only in-memory fixture-promotion proof objects.
Issue #386 supplies synthetic-only in-memory corpus metadata diff objects.
Issue #385 supplies synthetic-only in-memory golden replay fixture and
manifest draft packet objects.

The deployed #385 package preserves these boundaries:

- no fixture files are written;
- no golden replay manifest files are written;
- no expected-output files are written;
- no proof files or metadata diff files are written;
- no fixture-promotion packets are written;
- no corpus metadata edits are performed;
- no private harvest is authorized or executed;
- no corpus status movement is authorized;
- #388 remains open and inactive;
- `parser_behavior_ready=false`;
- `pipeline_activation_ready_for_issue_388=false`;
- `file_writing_authorized=false`;
- `private_harvest_authorized=false`;
- `fixture_promotion_authorized=false`;
- `corpus_status_change_authorized=false`.

There is no dedicated #387 PR-assist contract, module, test, output object, or
committed PR-assist artifact before this contract.

The pull request template already requires issue, tracker, contract,
implementation handoff, review evidence, risk tier, layer ownership, drift
budget, protected-surface checkboxes, validation, PR lifecycle fields, and
workflow handoff. It also says to use `Closes #...` only when a PR fully
satisfies the issue, and `Refs #...` for partial, planning-only,
contract-only, tracker, or follow-up work.

## Problem

#387 is the final staged child in the initial #388 evidence-pipeline tooling
sequence. Previous children can produce review packets, proof objects,
metadata diffs, and fixture/manifest draft packets in memory. The remaining
planning question is how a future workflow may help Codex F submit a reviewed
fixture-promotion package without crossing into Codex F or Codex G authority.

That boundary is high risk because PR-assist output sits near:

- reviewed-file lists;
- staged-file expectations;
- draft PR body text;
- issue close keywords;
- target branch selection;
- validation summaries;
- protected-surface summaries;
- fixture and corpus metadata mutation;
- private-evidence and local artifact boundaries;
- Codex F submitter actions;
- Codex G deployer actions.

The first bad value is treating any PR-assist packet, reviewed-file list,
draft PR text, check summary, or Codex-readable recommendation as authority
to stage files, create commits, push branches, open or edit PRs, merge, close
issues or trackers, promote fixtures, mutate corpus metadata, claim parser
behavior readiness, or claim pipeline activation readiness.

## Scope Decision

This contract approves a planning boundary only.

Codex C implementation is not authorized by this contract. File writing is not
authorized by this contract. PR creation is not authorized by this contract.
Staging, commits, pushes, merges, issue closure, tracker updates as completed,
fixture promotion, corpus status changes, private harvest, and #388/#381
activation are not authorized by this contract.

This contract defines:

- logical PR-assist package vocabulary;
- accepted upstream input objects from #383, #384, #386, and #385;
- draft PR body requirements;
- reviewed-file-list and intended-staging safeguards;
- `Refs` versus `Closes` guidance;
- target-branch and source-branch safety boundaries;
- validation summary and protected-surface summary requirements;
- privacy and local-artifact rejection rules;
- Codex F submitter boundary preservation;
- Codex G deployer boundary preservation;
- refusal/status vocabulary for unsafe packages;
- validation expectations for a later implementation, if separately
  authorized.

This contract does not authorize:

- code implementation;
- PR-assist output file writing;
- PR branch creation;
- `git add`, staging, commits, pushes, or draft PR creation;
- PR body edits;
- merge readiness decisions;
- issue closure or tracker completion;
- fixture file writing;
- golden replay manifest file writing;
- expected-output file writing;
- proof file writing;
- metadata diff file writing;
- corpus manifest edits;
- session ledger edits;
- private source reads;
- diagnostics, drift, live MTGA, network, firewall/drop, packet, OS/router,
  or private smoke checks;
- private harvest execution;
- fixture promotion;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

Quality / Governance owns PR-assist workflow boundaries, role routing,
submitter/deployer separation, lifecycle wording, branch safety, issue-link
policy, staging safeguards, protected-surface check summaries, and
non-claim preservation.

Corpus / Provenance owns fixture-promotion evidence vocabulary, upstream
review/proof/diff/draft references, proposed file classifications, corpus
metadata non-claims, and fixture-promotion non-claims.

Generated / Local Artifacts owns any future local-only preview files if a
later contract explicitly authorizes writing them.

Parser remains the truth owner for parser interpretation, parser events,
router behavior, parser state, match/game identity, deduplication, and final
reconciliation.

Codex F owns submitter actions: staging reviewed files, committing, pushing,
and opening or updating draft PRs after review allows it.

Codex G owns deployer actions: merge readiness, marking PRs ready, merging,
issue closure, tracker updates, and lifecycle evidence after explicit user
approval.

## Internal Project Area

Primary: Quality / Governance.

Supporting:

- Corpus / Provenance, for fixture-promotion evidence and corpus metadata
  review vocabulary.
- Generated / Local Artifacts, for any future local-only preview artifacts.
- Parser, as the truth owner for parser facts referenced by upstream packets.

This contract is not a parser behavior contract, not a fixture-promotion
authorization contract, not a private-evidence execution contract, not a
workbook/transport contract, not an analytics contract, not an AI/coaching
contract, not a CI gate, not a merge gate, and not a release/deploy/production
readiness gate.

## Truth Owner

Truth owner for PR lifecycle policy:

- `docs/codex_module_workflow.md`
- `.github/pull_request_template.md`
- `docs/templates/workflow_handoff.md`
- this contract, for #387-specific PR-assist vocabulary.

Truth owner for upstream #383 review packet shape:

- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `tests/test_harvest_review_packets.py`

Truth owner for upstream #384 proof shape:

- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `tests/test_fixture_promotion_proof.py`

Truth owner for upstream #386 metadata diff shape:

- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `tests/test_corpus_metadata_diff_generator.py`

Truth owner for upstream #385 fixture/manifest draft packet shape:

- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
- `tests/test_golden_replay_fixture_manifest_drafts.py`

Truth owner for current corpus metadata remains:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

A PR-assist packet may summarize proposed actions. It does not own truth for
parser facts, fixture promotion, corpus status, PR mergeability, deploy
readiness, release readiness, production behavior, analytics truth, AI truth,
or coaching truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code.

Potential future data flow, if separately authorized:

```text
#383 review packet
  + #384 proof object
  + #386 metadata diff object
  + #385 fixture/manifest draft packet
  + public-safe validation evidence
  -> in-memory PR-assist packet
  -> Codex E review
  -> Codex F submitter judgment
```

Forbidden reverse flow:

- PR-assist output must not mutate upstream review packets, proof objects,
  metadata diff objects, fixture/manifest draft packets, corpus manifest,
  session ledger, fixtures, expected outputs, parser behavior, runtime
  behavior, workbook/webhook/App Script surfaces, analytics, AI, coaching, CI,
  merge policy, deploy policy, production behavior, or final integration
  policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`

Expected future review artifact, if this contract receives Codex E review:

- `docs/contract_test_reports/parser_evidence_reviewed_fixture_promotion_pr_assist.md`

Potential future implementation files, only if separately authorized:

- `src/mythic_edge_parser/app/reviewed_fixture_promotion_pr_assist.py`
- `tests/test_reviewed_fixture_promotion_pr_assist.py`
- `docs/implementation_handoffs/parser_evidence_reviewed_fixture_promotion_pr_assist_comparison.md`

Files explicitly not owned by this contract:

- `.github/pull_request_template.md`
- `docs/codex_module_workflow.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- any file under `tests/fixtures/golden_replay/`
- any expected-output fixture file
- any proof file
- any metadata diff file
- any PR-assist output file
- any local/private/generated/runtime artifact
- any GitHub issue, PR body, branch, commit, or tracker state

## Public Interface

No public runtime interface is authorized now.

Logical future interface, if a later issue explicitly authorizes a
synthetic-only in-memory implementation:

```python
def build_reviewed_fixture_promotion_pr_assist(
    *,
    harvest_review_packet: Mapping[str, Any],
    promotion_proof: Mapping[str, Any],
    metadata_diff: Mapping[str, Any] | None,
    fixture_manifest_draft_packet: Mapping[str, Any],
    validation_evidence: Mapping[str, Any] | None = None,
    pr_context: Mapping[str, Any] | None = None,
    proposed_files: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    ...
```

Required future API properties, if separately authorized:

- pure in-memory operation;
- deterministic output for deterministic inputs;
- no file reads beyond supplied in-memory dictionaries;
- no source discovery;
- no Git commands;
- no GitHub writes;
- no file writes;
- no staging, committing, pushing, PR creation, PR editing, merge, issue
  closure, or tracker updates;
- no mutation of input dictionaries;
- no private path, raw line, raw hash, raw payload, local artifact, token,
  credential, or hostile payload echo in returned values;
- all readiness and authorization flags preserved as false.

## Logical PR-Assist Packet Shape

A future in-memory implementation may return this logical object:

```yaml
object: "mythic_edge_reviewed_fixture_promotion_pr_assist"
schema_version: "parser_evidence_reviewed_fixture_promotion_pr_assist.v1"
assist_id: "public-safe-deterministic-id"
created_at_utc: "ISO-8601 timestamp or deterministic test value"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/387"
pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
authorized_by_contract: "docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md"
assist_status: "draft"
source_artifacts:
  harvest_review_packet_id: "..."
  promotion_proof_id: "..."
  metadata_diff_id: "..."
  fixture_manifest_draft_packet_id: "..."
readiness_flags:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
authorization_flags:
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  pr_creation_authorized: false
  staging_authorized: false
  commit_authorized: false
  push_authorized: false
  merge_authorized: false
  issue_closure_authorized: false
  tracker_completion_authorized: false
targeting:
  base_branch: "main"
  target_branch: "main"
  source_branch: "symbolic-branch-name-or-null"
  target_branch_approved_by_issue: false
reviewed_file_list: []
draft_pr_body: {}
validation_summary: {}
protected_surface_summary: {}
privacy_summary: {}
codex_f_boundary: {}
codex_g_boundary: {}
refusal_reasons: []
non_claims: []
```

The packet is a review and routing artifact only. It is not a PR, not a
staging plan that can be executed automatically, not a commit plan, not a
merge plan, not fixture-promotion authority, and not corpus-status authority.

## Accepted Inputs

Future implementation, if separately authorized, may accept only supplied
in-memory, public-safe objects from these sources:

- #383 harvest review packets:
  - object: `mythic_edge_harvest_review_packet`
  - schema version: `parser_evidence_harvest_review_packet.v1`
  - accepted status: `reviewed_followup_candidate` or a later
    contract-authorized equivalent.
- #384 fixture promotion proof objects:
  - object: `mythic_edge_fixture_promotion_proof`
  - schema version: `parser_evidence_fixture_promotion_proof.v1`
  - accepted status: `proof_ready_for_review`.
- #386 corpus metadata diff objects:
  - object: `mythic_edge_corpus_metadata_diff`
  - schema version: `parser_evidence_corpus_metadata_diff.v1`
  - accepted status: `diff_ready_for_review` or `no_metadata_change`.
- #385 golden replay fixture/manifest draft packets:
  - object: `mythic_edge_golden_replay_fixture_manifest_draft_packet`
  - schema version:
    `parser_evidence_golden_replay_fixture_manifest_drafts.v1`
  - accepted status: `draft_ready_for_review`.
- Public-safe validation evidence:
  - command labels;
  - pass/review/fail/diff/blocked/unavailable statuses;
  - repo-relative report paths;
  - issue or PR links;
  - CI check names and statuses;
  - no raw logs, private paths, secrets, or generated private artifacts.
- Public-safe PR context:
  - issue URL;
  - tracker URL;
  - contract path;
  - implementation handoff path;
  - review or contract-test report path;
  - approved base and target branch values;
  - draft PR title text;
  - public-safe summary bullets;
  - explicit non-claims.
- Public-safe proposed file descriptors:
  - repo-relative path;
  - artifact role;
  - source object reference;
  - review status;
  - intended PR section;
  - whether the file is allowed in a future Codex F reviewed scope.

All accepted inputs must be public-safe. Public-safe means they contain no raw
private log content, no exact private paths, no raw payload values, no private
hashes or offsets, no local-only artifacts, no credentials, and no readiness
or truth overclaims.

## Forbidden Inputs

Future implementation must reject or refuse:

- raw private `Player.log` contents;
- raw private `UTC_Log` contents;
- raw line text;
- raw JSON payload values;
- private app-data contents;
- exact private local file paths;
- raw hashes or hash lists from private files;
- private file offsets, byte ranges, or file sizes;
- private timestamp windows that identify a local play session;
- screenshots;
- workbook exports;
- runtime status files;
- failed posts;
- SQLite files;
- generated/private artifacts;
- secrets, credentials, tokens, API keys, webhook URLs, Apps Script URLs, or
  environment variable values;
- decklists, deck names, deck IDs, private strategy notes, card choices, or
  private sideboarding notes;
- live MTGA, diagnostics, drift, network, firewall/drop, packet, OS/router, or
  private smoke check outputs;
- Manasight raw logs, compressed corpus files, parser source, or external
  corpus contents;
- downstream analytics, AI, coaching, workbook, dashboard, or Apps Script
  interpretations as parser expected facts;
- local absolute paths in draft PR body text, reviewed file lists, validation
  summaries, or workflow handoff blocks;
- unsafe PR lifecycle keywords such as `Closes #388` or tracker-completion
  language unless a future Codex G deployer contract explicitly authorizes
  tracker closure.

Forbidden inputs must produce `blocked_privacy`, `blocked_authorization`, or
`blocked_overclaim` without echoing the supplied forbidden value.

## Reviewed File List Shape

Each reviewed file descriptor must use this logical shape:

```yaml
path: "repo/relative/path"
artifact_role: "contract|implementation_handoff|source|test|fixture|golden_replay_manifest|expected_output|corpus_manifest|session_ledger|contract_test_report|other"
source_evidence_ref: "public-safe-source-id"
review_status: "reviewed_allowed|review_required|blocked_privacy|blocked_authorization|blocked_overclaim|unrelated|unknown"
stage_allowed_by_assist: false
requires_codex_f_judgment: true
requires_codex_g_deployer: false
privacy_class: "public_safe|synthetic|sanitized_committable|local_private_not_committed|generated_private|unknown"
protected_surface_class: "none|parser|corpus_metadata|fixture|runtime|workbook_webhook_apps_script|analytics_ai_coaching|workflow_lifecycle|unknown"
notes: []
```

Rules:

- `path` must be repo-relative.
- `stage_allowed_by_assist` must always be false. PR-assist may recommend
  review status, but Codex F must decide staging after independent inspection.
- `requires_codex_f_judgment` must be true for any proposed file.
- `requires_codex_g_deployer` must be true only when the file implies merge,
  issue closure, tracker updates, or deployer follow-up.
- Fixture, manifest, expected-output, corpus manifest, or session ledger
  files must be listed only as proposed reviewed scope. Their presence in a
  list does not authorize writing, staging, or mutation.
- Any descriptor pointing at raw/private/local/generated/runtime artifacts
  must be `blocked_privacy` or `blocked_authorization`.
- Unrelated paths must be `unrelated` and must not be included in draft PR
  body sections except as a blocker.

## Draft PR Body Requirements

PR-assist may produce draft PR body sections only as text suggestions. The
suggested text must follow `.github/pull_request_template.md` and preserve
all non-claims.

Required sections:

- Summary.
- Linked Issue, Tracker, And Contract.
- Related ADRs, or `N/A` when none are relevant.
- Implementation handoff.
- Review or contract-test report.
- Risk Tier.
- Layer Ownership.
- Drift Budget.
- Changes.
- Protected Surfaces.
- Tests.
- Contract Verification.
- PR Lifecycle.
- Still Unverified.
- Workflow Handoff.

Required #387-specific content:

- Link issue #387.
- Link tracker #388.
- Link parent private-evidence issue #434.
- Link source contracts and implementation handoffs for #383, #384, #386,
  and #385 when they are part of the proposed package.
- State `parser_behavior_ready=false`.
- State `pipeline_activation_ready_for_issue_388=false`.
- State `file_writing_authorized=false` unless a later issue explicitly
  changes it.
- State `private_harvest_authorized=false`.
- State `fixture_promotion_authorized=false`.
- State `corpus_status_change_authorized=false`.
- State that Codex F owns staging/commit/push/PR submission.
- State that Codex G owns merge, issue closure, tracker updates, and deployer
  lifecycle evidence.
- State that the PR-assist packet is not parser truth, fixture-promotion
  authority, corpus status authority, readiness authority, merge authority, or
  deploy authority.

Forbidden draft PR body content:

- raw/private values;
- local absolute paths;
- unsafe close keywords for #388, #434, or other trackers;
- claims that a fixture is promoted before a reviewed PR is merged;
- claims that corpus status changed before metadata has actually changed in a
  reviewed, merged PR;
- claims that parser behavior is ready;
- claims that #388 or #381 is active;
- release, production, analytics, AI, coaching, privacy-assurance, or
  security-assurance claims.

## `Refs` Versus `Closes` Guidance

PR-assist must preserve the repository PR template policy:

- Use `Refs #...` for planning-only, contract-only, partial, tracker,
  follow-up, or review-only work.
- Use `Closes #...` only when the PR fully satisfies the specific issue named.
- Never suggest `Closes #388` from a #387 or fixture-promotion PR unless a
  future Codex G deployer pass explicitly authorizes tracker closure.
- Never suggest `Closes #434` from PR-assist or fixture-promotion work unless
  a separate private-evidence lifecycle issue explicitly authorizes closing
  the parent private-evidence issue.
- A future PR-assist implementation for #387 itself should suggest
  `Refs #387` unless that future PR fully implements the #387 contract and
  the issue has no remaining work.
- A future fixture-promotion PR may suggest `Closes #<fixture-promotion-child>`
  only for the dedicated issue whose reviewed package it fully satisfies.
- Tracker and parent issue links should normally be `Refs`.

Unsafe close keywords must produce `unsafe_pr_lifecycle` or
`blocked_authorization`.

## Target Branch And Source Branch Safety

PR-assist may report branch metadata. It must not switch branches, create
branches, push branches, or open PRs.

Target branch rules:

- `target_branch` must come from the current issue, handoff, or explicit user
  instruction.
- Because this handoff names `target_branch: main`, draft text may name
  `main` as the approved future target for this planning lane.
- PR-assist must still state that targeting `main` does not bypass Codex F
  and Codex G gates.
- Missing, mismatched, or stale target branch authority must produce
  `unsafe_target_branch` or `blocked_authorization`.

Source branch rules:

- A source branch may be suggested only as a symbolic future branch name.
- PR-assist must not create or switch to the branch.
- Source branch must not be `main` for implementation work unless the future
  issue explicitly authorizes direct work on `main`.
- Dirty worktree, unrelated changes, or untracked private/generated artifacts
  in a future submitter context must be surfaced as blockers, not silently
  included.

## Assist Status Vocabulary

Allowed `assist_status` values:

- `draft`: packet is syntactically formed but not ready for review.
- `assist_ready_for_review`: packet is public-safe, minimal, sourced, and
  ready for Codex E or human review; it is still not submitter authority.
- `blocked_privacy`: input or proposed output contains forbidden private or
  sensitive material.
- `blocked_authorization`: requested source class, target branch, file set,
  lifecycle action, or side effect requires authority this contract does not
  provide.
- `blocked_overclaim`: packet or draft text attempts to claim parser truth,
  fixture promotion, corpus status movement, private smoke success,
  readiness, merge authority, deploy authority, or downstream truth.
- `insufficient_review`: #383 review packet is missing, malformed, stale, or
  not an accepted reviewed follow-up candidate.
- `insufficient_proof`: #384 proof is missing, malformed, rejected, or not
  `proof_ready_for_review`.
- `insufficient_metadata_diff`: #386 metadata diff is missing, malformed, or
  not accepted when metadata movement is part of the proposed package.
- `insufficient_draft_packet`: #385 fixture/manifest draft packet is missing,
  malformed, rejected, or not `draft_ready_for_review`.
- `insufficient_validation`: validation evidence is missing, stale, failed,
  unavailable, or insufficient for the proposed file set.
- `unsafe_file_set`: proposed file list includes unrelated files, raw/private
  artifacts, forbidden generated artifacts, or unreviewed protected surfaces.
- `unsafe_pr_lifecycle`: proposed draft PR text has unsafe close keywords,
  tracker completion language, merge/deploy claims, or branch/lifecycle drift.
- `needs_contract_update`: input schema or requested output is outside this
  contract.
- `assist_rejected`: reviewer or deterministic check rejects the packet.

Status precedence for a future implementation:

```text
blocked_privacy
blocked_authorization
blocked_overclaim
unsafe_pr_lifecycle
unsafe_file_set
needs_contract_update
insufficient_review
insufficient_proof
insufficient_metadata_diff
insufficient_draft_packet
insufficient_validation
assist_rejected
draft
assist_ready_for_review
```

## Validation Summary Requirements

PR-assist may summarize validation evidence only when it is supplied as
public-safe metadata. It must not run validation unless a future issue
separately authorizes implementation behavior.

Allowed validation evidence fields:

```yaml
command_label: "python3 -m pytest -q tests/test_example.py"
status: "pass|review|warn|diff|fail|blocked|unavailable|not_run"
source_ref: "public-safe-report-or-ci-ref"
scope: "contract|focused_tests|full_tests|ruff|agent_docs|diff_check|secret_scan|protected_surface|selector|pyright_advisory|ci"
notes: []
```

Validation summary rules:

- A `pass` status means only that the supplied public-safe evidence says the
  check passed in the named scope.
- `diff`, `fail`, `blocked`, or `unavailable` must prevent
  `assist_ready_for_review` unless a later review-only exception is
  contract-authorized.
- Pyright remains advisory unless a later contract makes it required.
- CI evidence may be summarized by check name and status; logs must not be
  copied if they include private or hostile values.
- Validation summaries must not claim merge readiness or deploy readiness.

Required future Codex C tests, if implementation is separately authorized:

- valid #383/#384/#386/#385 inputs plus public-safe validation evidence to
  `assist_ready_for_review`;
- missing review packet to `insufficient_review`;
- non-ready proof to `insufficient_proof`;
- missing required metadata diff to `insufficient_metadata_diff`;
- non-ready draft packet to `insufficient_draft_packet`;
- failing or missing validation evidence to `insufficient_validation`;
- raw/private input to `blocked_privacy` without value echo;
- overclaiming draft PR text to `blocked_overclaim`;
- unsafe `Closes #388` or tracker completion text to `unsafe_pr_lifecycle`;
- proposed raw/local/generated artifact path to `unsafe_file_set`;
- all readiness and authorization flags remain false;
- input dictionaries are not mutated;
- deterministic output for equivalent inputs.

## Protected-Surface Summary Requirements

PR-assist may summarize protected-surface evidence only as public-safe
metadata.

Required protected-surface categories:

- parser behavior;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- match/game identity;
- deduplication;
- corpus metadata;
- fixtures and expected outputs;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status files;
- failed posts;
- workbook exports;
- analytics behavior;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge policy;
- deploy policy;
- production behavior.

The summary must distinguish:

- unchanged;
- touched and contract-authorized;
- touched and blocked;
- unknown/review required.

Unknown, blocked, or unauthorized protected-surface touches must prevent
`assist_ready_for_review`.

## Privacy And Local-Artifact Rules

PR-assist must fail closed on raw/private/local/generated material.

Public outputs may include:

- repo-relative public paths;
- symbolic source IDs;
- issue and PR URLs;
- contract and report paths;
- command labels;
- pass/review/fail status labels;
- reduced counts;
- boolean privacy flags;
- public-safe non-claims.

Public outputs must not include:

- raw log lines;
- raw payloads;
- private local paths;
- raw hashes;
- exact private offsets, byte ranges, sizes, or timestamp windows;
- private app-data contents;
- private source filenames;
- screenshots;
- runtime status files;
- failed posts;
- workbook exports;
- SQLite files;
- generated/private artifacts;
- exact local report paths;
- decklists, deck names, deck IDs, strategy notes, card choices, or private
  sideboarding notes;
- secrets, credentials, tokens, API keys, webhook URLs, or Apps Script URLs.

If a future implementation sees a forbidden value, it must return
`blocked_privacy` and identify only a symbolic reason code.

## Codex F Submitter Boundary

PR-assist may help Codex F by preparing review material. It must not become
Codex F.

PR-assist may suggest:

- intended file list;
- file classifications;
- draft PR title;
- draft PR body text;
- validation summary;
- protected-surface summary;
- issue link policy;
- remaining risks;
- non-claims;
- workflow handoff draft.

PR-assist must not:

- stage files;
- decide the final staged set;
- run `git add`;
- create commits;
- push branches;
- open or edit PRs;
- mark PRs ready;
- close issues;
- update trackers as completed;
- bypass Codex E review;
- bypass Codex F's independent status and diff inspection.

Codex F must still inspect `git status`, review diffs, stage only reviewed
files, verify target branch, prepare the final PR body, and preserve issue and
tracker lifecycle language.

## Codex G Deployer Boundary

PR-assist may include a handoff section for Codex G. It must not become Codex
G.

PR-assist may name deployer gates:

- PR is not draft when ready for merge consideration;
- target branch is approved;
- CI/checks pass or named failures are explicitly waived;
- review has no blocking findings;
- diff remains within reviewed scope;
- no forbidden files or private artifacts are included;
- issue close behavior is correct;
- tracker update behavior is correct;
- explicit user deployer approval is present.

PR-assist must not:

- merge PRs;
- mark PRs ready;
- decide merge readiness;
- decide deploy readiness;
- close issues;
- close trackers;
- update tracker lifecycle as completed;
- claim production readiness or release readiness.

## Invariants

- PR-assist packets are advisory and review-only.
- PR-assist packets must preserve all false readiness and authorization flags
  listed in this contract.
- PR-assist packets must be deterministic for equivalent public-safe inputs.
- PR-assist packets must fail closed on missing, stale, malformed, or
  ambiguous upstream #383/#384/#386/#385 inputs.
- PR-assist packets must not echo forbidden private input values.
- PR-assist packets must not read source files, private logs, diagnostics
  outputs, drift reports, network state, OS/router state, workbook exports, or
  runtime artifacts.
- PR-assist packets must not write files unless a later contract explicitly
  authorizes file writing.
- PR-assist packets must not stage, commit, push, open PRs, edit PRs, merge,
  close issues, or update trackers.
- PR-assist packets must not create fixtures, expected manifests, expected
  outputs, proof files, metadata diff files, or corpus metadata edits.
- PR-assist packets must not activate #388 or #381.
- PR-assist packets must not alter parser, workbook, webhook, Apps Script,
  analytics, AI, coaching, CI, release, deploy, or production behavior.

## Error Behavior

Missing #383 review packet:

- return or record `assist_status=insufficient_review`.

Malformed #383 review packet:

- return or record `assist_status=needs_contract_update` when the shape is
  unknown, or `assist_status=insufficient_review` when required fields are
  absent.

Review packet not reviewed for follow-up:

- return or record `assist_status=insufficient_review` or
  `assist_rejected`.

Missing or non-ready #384 proof:

- return or record `assist_status=insufficient_proof`.

Missing or non-ready #386 metadata diff when metadata movement is proposed:

- return or record `assist_status=insufficient_metadata_diff`.

Missing or non-ready #385 draft packet:

- return or record `assist_status=insufficient_draft_packet`.

Forbidden raw/private fields:

- return or record `assist_status=blocked_privacy`;
- do not echo forbidden values in diagnostics or error text.

Unrelated or forbidden file set:

- return or record `assist_status=unsafe_file_set`.

Unsafe close keywords, tracker completion language, branch drift, or lifecycle
overclaim:

- return or record `assist_status=unsafe_pr_lifecycle`.

Missing workflow, staging, PR creation, fixture-promotion, corpus-status, or
deployer authority:

- return or record `assist_status=blocked_authorization` if the proposed
  action requires actual mutation.

Truth/readiness overclaim:

- return or record `assist_status=blocked_overclaim`.

Contract ambiguity:

- return or record `assist_status=needs_contract_update`.

## Side Effects

This contract authorizes one side effect: creation of this contract file.

No side effects are authorized for future implementation unless separately
approved. Forbidden side effects include:

- file reads beyond supplied public-safe in-memory inputs;
- file writes;
- local artifact writes;
- PR-assist output file writes;
- fixture writes;
- golden replay manifest writes;
- expected-output writes;
- proof writes;
- metadata diff writes;
- corpus manifest or session ledger writes;
- generated report writes;
- branch creation;
- branch switching;
- staging;
- committing;
- pushing;
- PR creation or editing;
- merge;
- issue closure;
- tracker updates as completed;
- CI changes;
- private source reads;
- diagnostics or drift execution;
- workbook, webhook, Apps Script, Google Sheets, output transport, analytics,
  AI, coaching, release, deploy, or production changes.

## Dependency Order

If a later workflow authorizes implementation, the safe order is:

1. Confirm issue #387 has an explicit implementation authorization and a clean
   target branch.
2. Re-read this contract, #388, #434, the #518 umbrella, and upstream #383,
   #384, #386, and #385 contracts and implementation handoffs.
3. Implement only a pure in-memory PR-assist packet builder.
4. Add synthetic-only focused tests for status mapping, false readiness flags,
   privacy blocking, overclaim blocking, file-set checks, lifecycle keyword
   checks, and deterministic output.
5. Write an implementation handoff comparing behavior to this contract.
6. Route to Codex E for contract-test review.
7. Defer all staging, commits, pushes, PR creation, fixture writing, manifest
   writing, metadata mutation, fixture promotion, private harvest, #388
   activation, and deployment to separate role gates and explicit approval.

## Compatibility

PR-assist vocabulary must remain compatible with:

- #383 `mythic_edge_harvest_review_packet` objects;
- #384 `mythic_edge_fixture_promotion_proof` objects;
- #386 `mythic_edge_corpus_metadata_diff` objects;
- #385 `mythic_edge_golden_replay_fixture_manifest_draft_packet` objects;
- existing PR template sections;
- existing workflow handoff vocabulary;
- existing corpus parity statuses and readiness flags;
- existing secret/private marker and protected-surface checker semantics;
- existing Codex F submitter and Codex G deployer boundaries.

Compatibility does not authorize old stale start-condition wording from issue
#387. The latest #516/#518/#388 planning contracts and #381-#386 sequence
control non-activation semantics.

## Tests Required

Documentation-only validation for this contract:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf 'docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If a later implementation is explicitly authorized, focused tests should
cover:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_reviewed_fixture_promotion_pr_assist.py
PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py tests/test_reviewed_fixture_promotion_pr_assist.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf 'src/mythic_edge_parser/app/reviewed_fixture_promotion_pr_assist.py\ntests/test_reviewed_fixture_promotion_pr_assist.py\ndocs/implementation_handoffs/parser_evidence_reviewed_fixture_promotion_pr_assist_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/reviewed_fixture_promotion_pr_assist.py\ntests/test_reviewed_fixture_promotion_pr_assist.py\ndocs/implementation_handoffs/parser_evidence_reviewed_fixture_promotion_pr_assist_comparison.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/reviewed_fixture_promotion_pr_assist.py\ntests/test_reviewed_fixture_promotion_pr_assist.py\ndocs/implementation_handoffs/parser_evidence_reviewed_fixture_promotion_pr_assist_comparison.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Future implementation tests must prove:

- valid upstream objects can produce `assist_ready_for_review`;
- blocked, missing, stale, malformed, or mismatched upstream objects fail
  closed with the right status;
- forbidden private content returns `blocked_privacy` without value echo;
- unsafe close keywords return `unsafe_pr_lifecycle`;
- forbidden file descriptors return `unsafe_file_set`;
- overclaims return `blocked_overclaim`;
- all readiness and authorization flags remain false;
- no side effects occur.

## Acceptance Criteria

- The contract clearly defines PR-assist as review-only support, not submitter
  or deployer authority.
- The contract defines accepted upstream inputs from #383, #384, #386, and
  #385.
- The contract defines forbidden inputs and privacy/local-artifact blockers.
- The contract defines a logical PR-assist packet shape.
- The contract defines reviewed-file-list safeguards.
- The contract defines draft PR body requirements and `Refs` versus `Closes`
  guidance.
- The contract defines target/source branch safety.
- The contract preserves Codex F and Codex G boundaries.
- The contract preserves all false readiness and authorization flags.
- The contract does not authorize implementation, PR creation, staging,
  fixture writing, corpus metadata mutation, private harvest, fixture
  promotion, or #388/#381 activation.
- Documentation validation for the contract passes or failures are recorded.

## Next Workflow Action

Next role: Codex E, Module Reviewer / Contract Tester.

Codex C implementation is not authorized by this contract. A later Codex A,
Codex G, or user lifecycle decision may authorize a separate synthetic-only
in-memory Codex C implementation pass. Until that happens, review the contract
only.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #387.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/387

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/385

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/536

Previous merge commit:
421fc14783fa8582ecb34595dfd4692273ff77ef

Source contract:
docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md

Goal:
Review the planning-only PR-assist contract for reviewed fixture-promotion
packages. Confirm it preserves Codex F submitter and Codex G deployer
boundaries and does not authorize code implementation, staging, commits,
pushes, PR creation, fixture writing, corpus metadata mutation, private
harvest, fixture promotion, #388/#381 activation, parser behavior readiness,
release readiness, analytics truth, AI truth, or coaching truth.

Review focus:
- PR-assist packet is advisory and review-only.
- Accepted inputs from #383/#384/#386/#385 are correctly scoped.
- Forbidden raw/private/local/generated artifacts fail closed.
- Reviewed-file-list safeguards keep staging under Codex F.
- Draft PR body requirements preserve the repo PR template and non-claims.
- `Refs` versus `Closes` guidance cannot close #388 or #434.
- Target/source branch rules do not bypass submitter/deployer gates.
- Status vocabulary and validation expectations are testable.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not close #387, #388, or #434.
- Do not activate #388 or #381.
- Do not stage files, commit, push, open PRs, edit PRs, merge PRs, or close issues/trackers.
- Do not create fixture files, manifest files, expected-output files, proof files, metadata diff files, PR-assist output files, or corpus metadata edits.
- Do not run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift, network, firewall/drop, packet, OS/router, or private smoke checks.
- Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity.

Expected output:
- Contract-test findings, if any.
- Validation summary.
- Recommended next role.
- workflow_handoff block with repository and repository_url.
```

Pasteable Codex A prompt if the user later wants to decide whether Codex C
implementation should be authorized:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for a possible implementation authorization decision
for issue #387.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/387

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Source contract:
docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md

Goal:
Decide whether a later synthetic-only in-memory Codex C implementation is
appropriate for the reviewed fixture-promotion PR-assist packet, or whether
the lane should remain contract/review-only.

Preserve:
- parser_behavior_ready=false
- pipeline_activation_ready_for_issue_388=false
- file_writing_authorized=false
- private_harvest_authorized=false
- fixture_promotion_authorized=false
- corpus_status_change_authorized=false
- pr_creation_authorized=false
- staging_authorized=false
- commit_authorized=false
- push_authorized=false

Do not implement code. Do not open a PR. Do not create PR branches, stage
files, commit, push, open PRs, edit PRs, merge PRs, create fixture files,
write PR-assist output files, mutate corpus metadata, run/read private logs,
activate #388/#381, or claim readiness/truth.

Expected output:
- implementation authorization decision;
- if authorized, a narrow Codex C prompt limited to pure in-memory
  synthetic/public-safe PR-assist packet building;
- if not authorized, the next review/governance route;
- workflow_handoff block with repository and repository_url.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/387"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/385"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/536"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #387 reconciliation comment"
  target_artifact: "docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md"
  verdict: "reviewed_fixture_promotion_pr_assist_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "421fc14783fa8582ecb34595dfd4692273ff77ef"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  pr_creation_authorized: false
  staging_authorized: false
  commit_authorized: false
  push_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private marker scan"
    - "path-scoped protected-surface check"
    - "path-scoped validation selector"
  stop_conditions:
    - "Do not implement code without a later explicit lifecycle authorization."
    - "Do not create PR branches, stage files, commit, push, open PRs, edit PRs, merge PRs, or close issues/trackers."
    - "Do not create fixture files, golden replay manifest files, expected-output files, proof files, metadata diff files, PR-assist output files, corpus metadata edits, or local/generated artifacts."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not proceed to private harvest execution."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
