# Parser Evidence Pipeline Activation Contract

## Module

Bounded activation contract for issue #388, the parser evidence pipeline
tracker.

Plain English: this contract defines when Mythic Edge may move the #388 lane
from planning and tooling into a single bounded local dry-run workflow. The
dry-run workflow may be planned only through a later scoped issue and contract.
This contract does not run private logs, promote fixtures, update corpus
metadata, change parser behavior, or claim readiness.

Activation in this contract means "the repo has enough reviewed planning to
frame the first local dry-run issue." It does not mean parser behavior is
ready, the pipeline is broadly active, private evidence may be read, fixtures
may be promoted, or production work may begin.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/557
- Active tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Working branch: `codex/parser-evidence-pipeline-activation-contract-557`
- Latest verified base commit: `11dfdc5e2c060c9e6c7ee2dfb19b3d015220506d`
- Risk tier: High

Observed during this Codex B pass:

- Issue #557 is open.
- Tracker #388 is open.
- Parent private-evidence issue #434 is open.
- Predecessor issues #381 through #387 are closed.
- Predecessor PRs #520, #521, #522, #523, #530, #536, and #537 are merged.
- The operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- A clean issue worktree was used to avoid unrelated local work in the primary
  checkout.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #557
- Tracker #388
- Parent private-evidence issue #434
- Issues #381, #382, #383, #384, #385, #386, and #387
- PRs #520, #521, #522, #523, #530, #536, and #537
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`
- `docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/app/utc_log_source_adapter.py`
- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
- `tests/test_utc_log_source_adapter.py`
- `tests/test_local_harvest_candidate_reports.py`
- `tests/test_harvest_review_packets.py`
- `tests/test_fixture_promotion_proof.py`
- `tests/test_corpus_metadata_diff_generator.py`
- `tests/test_golden_replay_fixture_manifest_drafts.py`

No private Player.log, UTC_Log, app-data, live MTGA, firewall/drop, network,
packet, OS/router, diagnostics, drift, private smoke, workbook export, SQLite,
or local generated artifact was run, tailed, hashed, copied, summarized, or
read.

## Observed Current Behavior

The #388 lane now has reviewed planning and public-safe helper contracts for:

1. UTC_Log source-adapter boundaries.
2. Local harvest candidate reports.
3. Harvest review packets.
4. Fixture-promotion proof objects.
5. Corpus metadata diff drafts.
6. Golden replay fixture and manifest drafts.
7. Reviewed fixture-promotion PR-assist packets.

The implemented helper modules are synthetic-only, in-memory, review-only, or
draft-only by contract. They do not authorize private evidence reads, fixture
promotion, corpus metadata edits, parser behavior changes, GitHub issue or PR
actions, merge actions, or production-facing behavior.

Current preserved readiness and authorization flags remain:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

The local artifacts manifest classifies private logs, historical JSONL inputs,
runtime outputs, status snapshots, transport failures, bad events, decklists,
workbook exports, SQLite databases, app-data state, local logs, local
diagnostics, and secret-like configuration as local/private or secret-adjacent
surfaces. Those surfaces may not become committed activation evidence.

## Problem

The first bad value is treating "planning/tooling exists" as "private evidence
may now be run" or "the parser evidence pipeline is ready."

The predecessor issues created useful review-only building blocks, but #388 is
still high risk because it sits near raw local logs, local-only offset windows,
fixture drafting, corpus metadata diffs, issue/PR assist flows, and parser
truth boundaries. A safe activation contract must make the next step narrow:
one explicitly approved, local dry-run issue with named inputs, named outputs,
and stop conditions.

Without this contract, a future thread could accidentally:

- read private logs because the adapter exists;
- write local evidence artifacts into Git;
- promote a fixture draft without review;
- update corpus metadata from a generated diff;
- treat review packets as parser truth;
- treat #388 as active for broad automation;
- claim readiness because predecessor tooling merged.

## Scope Decision

This contract approves only a governance decision:

- #388 has enough reviewed planning for Codex A to frame the first bounded
  local dry-run issue, or for Codex B to write the dry-run contract if such an
  issue already exists and explicitly routes to B.

This contract does not authorize:

- private Player.log or UTC_Log execution;
- private source reads;
- private source hashing;
- private source summarization;
- local artifact creation;
- fixture creation or promotion;
- expected-output file creation;
- corpus metadata edits;
- parser behavior changes;
- issue creation by Codex B;
- PR creation by Codex B;
- scheduled or recurring automation;
- broad #388 activation;
- readiness claims.

The next implementation-adjacent step must be a separate dry-run issue and
contract. That contract must name the exact local run mode, preflight checks,
artifact locations, redaction rules, validation commands, and stop conditions
before any Codex C work begins.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

Quality / Governance owns:

- #388 activation semantics;
- A-G role routing;
- predecessor gate checks;
- human approval metadata;
- stop conditions;
- false-readiness preservation.

Corpus / Provenance owns:

- harvest candidate vocabulary;
- review packet vocabulary;
- fixture-promotion proof vocabulary;
- corpus metadata diff vocabulary;
- fixture and manifest draft vocabulary.

Parser remains the truth owner for parser interpretation, parser events,
router behavior, parser state, match/game identity, deduplication, and final
reconciliation.

This contract is not a parser behavior module, fixture-promotion package,
corpus status update, private evidence execution packet, CI gate, merge gate,
deploy gate, analytics module, AI module, coaching module, workbook module, or
production module.

## Truth Boundary

This contract owns workflow activation semantics only.

It does not own truth for:

- raw Player.log or UTC_Log content;
- Arena game state;
- parser facts;
- fixture expected output;
- corpus status;
- workbook rows;
- analytics labels;
- AI or coaching output;
- release readiness;
- production readiness.

Evidence-pipeline artifacts may summarize, classify, or prepare evidence for
human review. They must not become parser truth, fixture truth, merge
readiness, deploy readiness, gameplay advice, analytics truth, AI truth, or
coaching truth.

## Bridge-Code Status

`deferred_future_boundary`

No bridge code is authorized by this contract. Future child issues may define
bridge behavior from local/private evidence to local-only review artifacts,
but only after their own contracts name source classes, artifacts, validation,
privacy rules, and stop conditions.

## Predecessor Gate State

The following predecessor gates are satisfied for planning-to-dry-run issue
framing:

| Gate | Required State | Observed State |
| --- | --- | --- |
| #381 UTC_Log source adapter contract | Closed and merged | Closed, PR #520 merged |
| #382 local harvest candidate reports contract | Closed and merged | Closed, PR #521 merged |
| #383 harvest review packets contract | Closed and merged | Closed, PR #522 merged |
| #384 fixture-promotion proof contract | Closed and merged | Closed, PR #523 merged |
| #386 corpus metadata diff generator contract | Closed and merged | Closed, PR #530 merged |
| #385 fixture/manifest draft contract | Closed and merged | Closed, PR #536 merged |
| #387 reviewed fixture-promotion PR-assist contract | Closed and merged | Closed, PR #537 merged |
| #388 pipeline tracker | Open | Open |
| #434 private-evidence parent | Open | Open |

The following gates are not satisfied and must remain false:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
production_readiness_authorized: false
```

## Activation Vocabulary

Allowed activation statuses:

- `inactive_planning_only`: #388 has contracts/tooling but no local execution
  issue is active.
- `activation_contract_ready_for_review`: this contract exists and is ready
  for Codex E review.
- `activation_contract_merged`: this contract has passed Codex E/F/G and is
  merged.
- `dry_run_issue_required`: a new scoped dry-run issue must be created or
  selected before Codex B writes an execution contract.
- `dry_run_contract_required`: the dry-run issue exists, but Codex B must
  define exact run boundaries before Codex C.
- `bounded_dry_run_authorized`: a later dry-run contract and explicit user
  approval authorize exactly one local dry run.
- `private_execution_blocked`: approval, contract, source scope, artifact
  root, or privacy checks are missing.
- `fixture_promotion_blocked`: any fixture creation, expected-output update,
  or fixture-promotion packet is out of scope.
- `corpus_metadata_update_blocked`: any manifest or session-ledger edit is out
  of scope.
- `halted_stop_condition`: a stop condition was encountered and the workflow
  must route back to A, B, E, or the user.

Forbidden activation statuses:

- `parser_behavior_ready`
- `pipeline_activation_ready_for_issue_388`
- `fixture_promotion_ready`
- `private_smoke_success`
- `release_ready`
- `production_ready`
- `full_corpus_parity`

Those labels remain unavailable unless a later contract, implementation,
review, submitter, deployer, and explicit user approval prove them.

## Allowed Run Modes

This contract recognizes these run-mode labels for future contracts:

- `no_run_contract_only`: docs-only contract work. This is the only run mode
  authorized by #557.
- `synthetic_in_memory_preflight`: a future contract may authorize tests or
  helpers that use synthetic committed fixtures and write no artifacts.
- `approved_local_dry_run_metadata_only`: a future contract may authorize a
  local-only dry run over approved metadata that does not read raw private log
  payloads.
- `approved_local_dry_run_private_window`: a future contract may authorize one
  user-approved local evidence window with strict offset/window, redaction,
  retention, and local-only artifact rules.
- `blocked_private_execution`: no private execution may proceed.
- `not_allowed_broad_automation`: recurring, scheduled, or broad automation is
  out of scope.

#557 authorizes only:

```yaml
run_mode: no_run_contract_only
```

## Activation Checklist

A later dry-run issue may proceed to Codex B only if its handoff includes a
checklist equivalent to:

```yaml
activation_checklist:
  schema_version: parser_evidence_pipeline_activation.v1
  repository: Tahjali11/Mythic-Edge
  repository_url: https://github.com/Tahjali11/Mythic-Edge
  tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
  parent_private_evidence_issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
  predecessor_issues_381_through_387_closed: true
  predecessor_prs_520_521_522_523_530_536_537_merged: true
  dry_run_issue: "<required before execution>"
  dry_run_contract: "<required before execution>"
  requested_run_mode: "<one allowed run mode>"
  explicit_user_approval_for_private_inputs: "<required before private execution>"
  approved_source_class: "<synthetic | metadata_only | private_window>"
  approved_output_location_class: "<committed_docs | gitignored_local_only>"
  raw_log_reading_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```

Any missing, ambiguous, stale, or contradictory checklist value is a stop
condition.

## Human Approval Metadata

Private or local dry-run approval must be explicit and fresh. A future approval
record must include:

- approving user or issue comment;
- approval date;
- repository;
- tracker;
- dry-run issue;
- requested run mode;
- allowed source class;
- allowed local source window class, if any;
- allowed local output location class;
- forbidden source classes;
- allowed retention period;
- expiration condition;
- required redaction checks;
- exact non-claims;
- route after completion.

Approval to write this #557 contract is not approval to run private evidence.

## Allowed Inputs

Allowed for this contract:

- public GitHub issue and PR metadata for #557, #388, #434, and #381 through
  #387;
- committed governance docs;
- committed contracts;
- committed implementation modules and tests;
- committed local-artifact manifest metadata;
- committed validation tooling help output.

Allowed for a later dry-run contract only if explicitly named:

- synthetic committed fixtures;
- public-safe reduced evidence summaries;
- in-memory review packet data;
- local-only symbolic offset-window metadata;
- user-approved private evidence window metadata that does not enter Git.

## Forbidden Inputs

Forbidden for this contract and for any future dry-run unless a later contract
and explicit user approval say otherwise:

- raw Player.log payloads;
- raw UTC_Log payloads;
- private app-data contents;
- live MTGA reads;
- network, firewall/drop, packet, OS/router, or live diagnostics checks;
- workbook exports;
- SQLite databases and sidecar files;
- runtime logs;
- transport failure payloads;
- raw local file paths;
- raw hashes of private files;
- decklists, card choices, strategy notes, screenshots, or private reports;
- credentials, tokens, API keys, secrets, or webhook URLs;
- external corpus contents;
- Manasight logs or parser source.

## Artifact Boundaries

Committed artifacts allowed by this contract:

- this contract;
- future contract-test reports for this contract;
- future implementation handoffs that contain only public-safe workflow
  metadata.

Committed artifacts forbidden by this contract:

- raw private logs;
- raw private lines;
- raw private paths;
- private file hashes;
- local source windows;
- local evidence packets;
- private reports;
- runtime outputs;
- SQLite files;
- workbook exports;
- fixture files;
- expected-output files;
- corpus manifest edits;
- session-ledger edits.

Local-only artifacts may be authorized only by a later dry-run contract. That
future contract must name a gitignored local output location class, redaction
rules, retention rules, and deletion or archival expectations. Local-only
artifacts must not be staged, committed, pasted into issues, or summarized in
public with raw details.

## Allowed Commands

Allowed in this #557 pass:

```bash
git status --short --branch
gh issue view 557 --repo Tahjali11/Mythic-Edge
gh issue view 388 --repo Tahjali11/Mythic-Edge
gh issue view 434 --repo Tahjali11/Mythic-Edge
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_contract.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_contract.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_contract.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Allowed for a future dry-run contract only after Codex B defines scope:

- synthetic fixture tests;
- in-memory helper tests;
- local-only metadata preflight commands;
- path-scoped secret and protected-surface checks;
- repo status checks;
- public-safe report validation.

Forbidden commands until a later contract and explicit user approval:

- any command that reads private Player.log or UTC_Log payloads;
- any command that tails live MTGA logs;
- any command that inspects app-data contents;
- any command that toggles firewall, network, OS/router, or packet state;
- any command that creates fixtures, expected outputs, corpus metadata edits,
  issue comments, PRs, branches, commits, pushes, or scheduled jobs.

## Preflight Requirements For A Later Dry Run

A later dry-run contract must require all of these before Codex C:

1. Verify the operating repository and remote.
2. Verify branch and base commit.
3. Verify no unrelated local changes will be touched.
4. Verify #388 and #434 are open, unless a newer contract supersedes them.
5. Verify #381 through #387 remain closed and merged.
6. Verify the dry-run issue explicitly authorizes the selected run mode.
7. Verify private input approval exists if the run mode needs private input.
8. Verify the approved artifact location is local-only or committed-docs only.
9. Verify forbidden artifact classes are not staged.
10. Verify no raw private paths or payloads will be printed.
11. Verify scanner commands and path-scoped validation are available.
12. Verify the dry-run will route to Codex E review before any submission or
    deployment step.

Failure at any preflight step must stop the workflow.

## Status And Refusal Vocabulary

Allowed dry-run routing statuses:

- `ready_for_codex_a_dry_run_issue`
- `ready_for_codex_b_dry_run_contract`
- `ready_for_codex_c_synthetic_preflight_only`
- `ready_for_codex_c_approved_local_metadata_dry_run`
- `ready_for_codex_e_review`
- `blocked_missing_approval`
- `blocked_missing_contract`
- `blocked_private_input_scope`
- `blocked_artifact_location`
- `blocked_raw_payload_risk`
- `blocked_fixture_promotion_request`
- `blocked_corpus_metadata_request`
- `blocked_parser_behavior_request`
- `blocked_broad_automation_request`

Forbidden statuses:

- `ready_for_private_harvest`
- `ready_for_fixture_promotion`
- `ready_for_corpus_status_update`
- `ready_for_pipeline_activation`
- `ready_for_release`
- `ready_for_production`

## Stop Conditions

Stop immediately if any future thread is asked to:

- read, copy, hash, summarize, or upload raw private logs;
- inspect private app-data contents;
- print raw local paths or private offsets into public docs;
- commit local-only artifacts;
- commit SQLite files or sidecars;
- commit runtime logs, transport failure outputs, workbook exports, decklists, screenshots,
  credentials, tokens, API keys, webhook URLs, or private reports;
- create fixtures or expected-output files without a fixture-specific
  contract;
- edit `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- edit `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- claim parser readiness, pipeline activation readiness, fixture-promotion
  readiness, private smoke success, release readiness, production readiness,
  analytics truth, AI truth, coaching truth, or full corpus parity;
- change parser behavior, parser state final reconciliation, parser event
  classes, router semantics, diagnostics shape, drift behavior, golden replay
  behavior, evidence-ledger behavior, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, CI gates, merge
  policy, deploy policy, or production behavior.

## Mythic-Edge-Corpus And External Automation Gates

This contract does not authorize mutation of any sibling repository or
external corpus automation.

If a future dry-run or fixture-promotion path references a separate
Mythic-Edge-Corpus repository, automation gate, external corpus runner, or
scheduled job, that reference must be treated as a stop condition until a
repo-scoped handoff identifies:

- repository and repository URL;
- operating checkout;
- allowed read/write scope;
- artifact authority;
- source of truth;
- validation commands;
- forbidden content rules;
- issue and PR routing.

No external automation may promote fixtures, update corpus metadata, create
source-repo issues, or claim readiness from this contract.

## A-G Workflow Routing

Recommended sequence after this contract:

1. Codex E reviews this contract against issue #557 and the #388/#434 gates.
2. Codex F submits the contract-only package if E finds no blockers.
3. Codex G merges only with explicit approval and confirms #388/#434 remain
   open unless separately authorized.
4. Codex A creates or reconciles the first bounded local dry-run issue.
5. Codex B writes the dry-run contract for that issue.
6. Codex C may act only if the dry-run contract explicitly authorizes it.
7. Codex E reviews dry-run evidence before any Codex F/G step.

Codex B for #557 must not skip directly to Codex C implementation.

## Compatibility Expectations

This contract is compatible with:

- `parser_evidence_pipeline_activation_criteria.md`;
- `parser_evidence_pipeline_planning_umbrella.md`;
- the #381 through #387 predecessor contracts;
- the #456 human-approved parser/corpus update workflow.

It narrows the next step from "pipeline activation" to "first bounded dry-run
issue framing." It does not change existing readiness metrics, parser
behavior, fixture policy, corpus metadata, private-evidence handling, or
GitHub lifecycle policy.

## Validation Requirements

Codex B validation for this contract:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_contract.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_contract.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_contract.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Codex C validation for a later dry-run implementation must be defined by that
future contract. At minimum, it should include:

- focused tests for any helper touched;
- path-scoped secret and protected-surface checks;
- `git diff --check`;
- public-safe artifact scan;
- explicit no-private-payload evidence;
- explicit false-readiness assertions.

Codex E review focus:

- ensure activation status is not overclaimed;
- ensure #388 and #434 boundaries remain open and respected;
- ensure no private evidence was read or summarized;
- ensure no fixture or corpus metadata change is hidden in the diff;
- ensure next-role routing goes to dry-run issue framing, not broad execution.

## Acceptance Criteria

This contract satisfies issue #557 only if:

- the #388 activation checklist is explicit;
- predecessor gates #381 through #387 are listed;
- #434 remains a private-evidence parent gate;
- allowed run modes are named;
- output locations are split into committed public-safe artifacts and
  local-only artifacts;
- stop conditions cover raw logs, secrets, local paths, app-data, workbook
  exports, SQLite files, private strategy data, fixture promotion, corpus
  metadata, and readiness claims;
- the next step routes to a first bounded dry-run issue, not broad recurring
  automation.

## Recommended Next Role

Codex E should review this contract before any Codex F/G submission.

After merge, the next substantive role should be Codex A to create or
reconcile the first bounded local dry-run issue under #388. If such an issue
already exists and explicitly routes to B, Codex B may write that dry-run
contract next.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #557.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/557

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract artifact:
docs/contracts/parser_evidence_pipeline_activation_contract.md

Review goal:
Review the #388 bounded activation contract. Confirm it routes only to a first
bounded local dry-run issue and does not authorize private Player.log or
UTC_Log reads, fixture promotion, corpus metadata updates, parser behavior
changes, broad automation, or readiness claims.

Focus:
- predecessor gates #381 through #387;
- #434 private-evidence parent boundary;
- allowed run modes and local/private artifact boundaries;
- stop conditions for raw logs, secrets, local paths, app-data, workbook
  exports, SQLite files, private strategy data, fixture promotion, corpus
  metadata, and readiness claims;
- next-role routing to Codex E/F/G for this contract, then Codex A/B for a
  separate dry-run issue/contract.

Protected boundaries:
- Do not run private Player.log or UTC_Log files.
- Do not promote fixtures or update corpus metadata.
- Do not claim parser_behavior_ready, pipeline activation readiness,
  production readiness, analytics truth, AI truth, coaching truth, or full
  corpus parity.
- Do not implement code, open a PR, merge, or close #388/#434/#557.

Expected output:
- Findings first, if any.
- Contract approval or required fixes.
- Validation evidence reviewed.
- Recommended next role.
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/557"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "E"
  verdict: "bounded_parser_evidence_pipeline_activation_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-evidence-pipeline-activation-contract-557"
  latest_verified_base_commit: "11dfdc5e2c060c9e6c7ee2dfb19b3d015220506d"
  target_artifact: "docs/contracts/parser_evidence_pipeline_activation_contract.md"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  recommended_after_review: "Codex F/G for contract-only submission, then Codex A to create or reconcile the first bounded local dry-run issue under #388."
  stop_conditions:
    - "Do not run private Player.log or UTC_Log files."
    - "Do not promote fixtures or update corpus metadata."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, production readiness, analytics truth, AI truth, coaching truth, or full corpus parity."
    - "Do not activate broad #388 execution, scheduled automation, private harvest, fixture promotion, corpus metadata edits, parser changes, issue creation, PR creation, merge, or deploy from this contract alone."
```
