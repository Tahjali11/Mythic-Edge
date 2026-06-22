# Parser Evidence Bounded Local Dry Run Contract

## Module

Planning contract for issue #559, the first bounded local dry-run lane under
the parser evidence pipeline tracker.

Plain English: this contract defines what a later Codex C dry run may do,
where it may stop, and what it must not claim. The intended dry run is a
single, fixture-safe pass through the existing #388 helper surfaces so the
team can prove the handoff shape before any private harvest, fixture
promotion, corpus metadata update, or recurring automation is allowed.

The contract does not run the dry run. It does not read private logs, create
fixtures, update corpus metadata, change parser behavior, or activate #388.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/559
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Dependency issue: https://github.com/Tahjali11/Mythic-Edge/issues/557
- Dependency PR: https://github.com/Tahjali11/Mythic-Edge/pull/562
- Dependency merge commit: `2bf909d55ea05587dc151adda71b0b7d6e84487f`
- Base branch: `main`
- Target branch: `main`
- Working branch: `codex/parser-evidence-bounded-local-dry-run-559`
- Latest verified base commit: `2bf909d55ea05587dc151adda71b0b7d6e84487f`
- Risk tier: High

Observed during this Codex B pass:

- Issue #559 is open.
- Tracker #388 is open.
- Parent private-evidence issue #434 is open.
- Issue #557 is closed and PR #562 is merged.
- The operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- A clean issue worktree was used because the primary checkout contained
  unrelated local governance and workflow changes.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #559
- Tracker #388
- Parent private-evidence issue #434
- Issue #557 and PR #562
- `docs/contracts/parser_evidence_pipeline_activation_contract.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- `docs/contracts/parser_evidence_reviewed_fixture_promotion_pr_assist.md`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/app/utc_log_source_adapter.py`
- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `src/mythic_edge_parser/app/harvest_review_packets.py`
- `src/mythic_edge_parser/app/fixture_promotion_proof.py`
- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- Focused #381 through #387 tests as reference only

No private Player.log, UTC_Log, app-data, live MTGA, firewall/drop, network,
packet, OS/router, diagnostics, drift, private smoke, workbook export, SQLite,
or generated local artifact was run, tailed, hashed, copied, summarized, or
read.

## Observed Current Behavior

Issue #557 established that #388 has enough reviewed planning to frame a
bounded local dry-run issue. It did not authorize the dry run itself.

The #388 helper chain now has reviewed contracts and source modules for:

1. UTC_Log source-adapter boundaries.
2. Local harvest candidate reports.
3. Harvest review packets.
4. Fixture-promotion proof objects.
5. Golden replay fixture and manifest draft packets.
6. Corpus metadata diff drafts.
7. Reviewed fixture-promotion PR-assist packets.

Those modules are synthetic-only, in-memory, review-only, or draft-only by
contract. They do not authorize private source reads, fixture promotion,
corpus metadata edits, parser behavior changes, GitHub actions, merge actions,
or production-facing behavior.

Current preserved readiness and authorization flags remain:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

## Problem

The first bad value is treating "the dry-run issue exists" as "the dry run may
now execute over local/private evidence."

The second bad value is treating "the helper modules compose in concept" as
"fixtures may be promoted" or "the parser evidence pipeline is active."

Without a specific #559 contract, a future role could accidentally:

- run private Player.log or UTC_Log data;
- store local evidence artifacts in a public path;
- create fixture or manifest files directly;
- update corpus metadata from a generated diff;
- treat a review packet as parser truth;
- treat a proof object as fixture-promotion approval;
- treat a successful dry-run shape as parser behavior readiness;
- route #388 into recurring automation.

## Scope Decision

This contract authorizes only the contract boundary for a future bounded dry
run. Codex B does not run the dry run.

The narrowest safe future path is:

1. Review this contract.
2. Submit and merge the contract-only artifact through normal Codex E/F/G
   routing.
3. Require explicit user approval before any Codex C dry-run execution.
4. Allow Codex C to run only a fixture-safe, synthetic, no-private-source dry
   run unless a later contract and approval record authorize a stricter
   private-window path.

Default selected path:

```yaml
selected_path: fixture_safe_synthetic_in_memory
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

This contract does not authorize a reusable orchestrator module by default.
The first Codex C pass should prefer existing helper modules and focused tests.
If Codex C proves that a tiny helper is required to compose the dry run safely,
it must stop and route that implementation need through a new or amended
contract before writing source code.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

Quality / Governance owns:

- dry-run approval semantics;
- role routing;
- stop conditions;
- non-claims;
- validation evidence requirements;
- protected-surface boundaries.

Corpus / Provenance owns:

- candidate-report vocabulary;
- review-packet vocabulary;
- fixture-promotion proof vocabulary;
- fixture/manifest draft vocabulary;
- corpus metadata diff vocabulary.

Parser remains the truth owner for parser interpretation, parser events,
router behavior, parser state, match/game identity, deduplication, and final
reconciliation.

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance.

This contract is not a parser behavior module, private evidence execution
packet, fixture-promotion package, corpus status update, CI gate, merge gate,
deploy gate, workbook module, analytics module, AI module, coaching module, or
production module.

## Truth Owner

This contract owns dry-run workflow semantics only.

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

Dry-run artifacts may show that public-safe helper outputs can be composed for
review. They must not become parser truth, fixture truth, merge readiness,
deploy readiness, gameplay advice, analytics truth, AI truth, or coaching
truth.

## Bridge-Code Status

`deferred_future_boundary`

No source bridge code is authorized by this contract. A future Codex C dry run
may invoke existing helper modules in a one-shot fixture-safe process after
review and explicit approval. It may not add bridge code, source adapters,
file writers, watchers, schedulers, or promotion helpers unless a later
contract authorizes that implementation.

## Files Owned By This Contract

- `docs/contracts/parser_evidence_bounded_local_dry_run.md`

Expected later public-safe review artifacts, if separately authorized:

- `docs/implementation_handoffs/parser_evidence_bounded_local_dry_run_comparison.md`
- `docs/contract_test_reports/parser_evidence_bounded_local_dry_run.md`

This contract does not authorize edits to:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- golden replay fixture files;
- golden replay expected-output files;
- local app-data roots;
- runtime logs;
- SQLite databases;
- workbook exports;
- private evidence packets;
- GitHub issue or PR bodies.

## Public Interface

The future dry-run packet should use this public-safe schema label:

```yaml
schema_version: "parser_evidence_bounded_local_dry_run.v1"
object: "parser_evidence_bounded_local_dry_run_report"
```

Required dry-run report sections:

- `identity`
- `source_context`
- `approval_context`
- `run_mode`
- `input_refs`
- `pipeline_steps`
- `output_refs`
- `validation`
- `redaction_and_forbidden_content`
- `protected_surface_summary`
- `authorization_flags`
- `non_claims`
- `verdict`
- `next_recommended_role`

The report is a workflow evidence artifact. It is not parser output and must
not be consumed by runtime parser code, workbook sync code, analytics code, AI
code, or production tooling.

## Allowed Run Modes

This contract recognizes these run-mode labels:

- `contract_only_no_run`: docs-only boundary work. This is the only mode
  performed by Codex B.
- `fixture_safe_synthetic_in_memory`: a later Codex C may run existing helper
  functions in memory using committed synthetic fixtures or inline synthetic
  values, with no private inputs and no generated files other than an approved
  public-safe comparison report.
- `fixture_safe_committed_synthetic_files`: a later Codex C may read already
  committed synthetic fixtures if they are named by the approved prompt and do
  not contain private or external raw logs.
- `approved_sanitized_metadata_only`: blocked for #559 by default; may be
  allowed only by a later explicit approval record and amended contract.
- `approved_private_window`: blocked for #559 by default; may be allowed only
  by a later private-evidence execution contract, parent #434 routing, and
  explicit user approval that names the exact local evidence scope.
- `blocked_broad_automation`: recurring, scheduled, watcher, live MTGA, or
  broad harvest automation is not allowed.

#559 Codex B performs only:

```yaml
run_mode: contract_only_no_run
```

The recommended first Codex C dry-run mode is:

```yaml
run_mode: fixture_safe_synthetic_in_memory
```

## Allowed Inputs

Allowed for Codex B:

- public GitHub issue and PR metadata for #559, #557, #388, and #434;
- committed governance docs;
- committed contracts;
- committed source modules and tests as reference only;
- committed local-artifact manifest metadata;
- committed validation tooling.

Allowed for a future Codex C fixture-safe dry run:

- committed synthetic fixtures already present in the repo;
- inline synthetic strings that contain no real MTGA private payload;
- existing in-memory helper outputs from #381 through #387 modules;
- repo-relative file references;
- public-safe validation command output summaries;
- public-safe issue and contract references.

Allowed only after a later explicit private-evidence approval path:

- one user-selected local metadata-only source window;
- one symbolic offset-window summary that does not include raw private lines,
  exact private paths, raw hashes, usernames, decklists, strategy notes, or
  secret-adjacent values.

## Forbidden Inputs

Forbidden for Codex B and for the default #559 dry run:

- raw private Player.log;
- raw private UTC_Log;
- app-data contents;
- live MTGA data;
- private diagnostics;
- private drift output;
- network, firewall/drop, packet, OS/router, or watcher evidence;
- private smoke output;
- raw log excerpts;
- exact private local paths;
- raw file hashes;
- screenshots;
- workbook exports;
- SQLite databases;
- credentials, tokens, API keys, webhook URLs, or secrets;
- decklists, card choices, private strategy notes, or player notes;
- external raw corpora;
- Manasight raw logs, compressed logs, parser source, hash lists, byte-size
  lists, capture-date rows, or raw session payloads.

## Output Location Classes

Allowed by this Codex B contract:

- `public_contract_only`: this contract file.

Allowed for a later reviewed Codex C fixture-safe pass:

- `public_safe_implementation_handoff`: a docs-only comparison report under
  `docs/implementation_handoffs/`.
- `public_safe_contract_test_report`: a docs-only review report under
  `docs/contract_test_reports/`, if Codex E needs it.
- `stdout_summary_public_safe`: terminal output summarized in the final answer
  or comparison report without raw payloads or local absolute paths.

Blocked unless a later contract and explicit approval authorize them:

- `gitignored_local_dry_run_dir`;
- `local_app_data_root`;
- `private_evidence_packet_dir`;
- `private_offset_window_state`;
- `fixture_output_path`;
- `golden_replay_manifest_path`;
- `corpus_metadata_path`;
- `github_issue_or_pr_body`;
- `recurring_automation_state`.

Any future local-only artifact location must be recorded symbolically, not as
an exact local absolute path, in public artifacts.

## No-Write Rules

Codex B may write only this contract.

The first Codex C pass may write only a public-safe comparison/report artifact
if the contract is reviewed and the user explicitly approves the fixture-safe
dry run.

The first Codex C pass must not write:

- fixture files;
- expected-output files;
- golden replay manifest files;
- corpus manifest or session ledger changes;
- private evidence packets;
- local generated evidence artifacts;
- issue drafts;
- PR branches;
- commits;
- GitHub comments;
- GitHub issues;
- GitHub pull requests.

## Dry-Run Pipeline Shape

A later fixture-safe dry run should prove only that the public-safe handoff
shape composes. It should not prove parser behavior correctness.

Recommended step order:

1. Preflight the repo, issue, tracker, parent gate, branch, and approval
   metadata.
2. Select one fixture-safe synthetic input case.
3. Exercise the UTC_Log source adapter only if the selected case is UTC_Log
   shaped; otherwise record `not_applicable_for_selected_case`.
4. Build a local harvest candidate summary in memory.
5. Build a harvest review packet in memory.
6. Build a fixture-promotion proof object in memory.
7. Build a golden replay fixture/manifest draft packet in memory.
8. Build a corpus metadata diff draft in memory.
9. Optionally inspect PR-assist vocabulary as `not_run_review_only`; do not
   create a PR-assist artifact unless separately authorized.
10. Run focused validation and forbidden-content scans.
11. Write one public-safe comparison report if approved.

Each step must record:

- `step_id`;
- `input_ref`;
- `output_ref`;
- `status`;
- `blocked_reason`, when blocked;
- `authorization_flags`;
- `non_claims`;
- `public_safe_summary`.

## Dry-Run Report Shape

The later dry-run report should use this shape:

```yaml
schema_version: "parser_evidence_bounded_local_dry_run.v1"
object: "parser_evidence_bounded_local_dry_run_report"
identity:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/559"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  dry_run_id: "<public-safe id>"
approval_context:
  approved_by_user: "<required before Codex C execution>"
  approved_run_mode: "fixture_safe_synthetic_in_memory"
  private_inputs_authorized: false
run_mode: "fixture_safe_synthetic_in_memory"
input_refs:
  - ref_id: "<repo-relative synthetic ref or inline synthetic id>"
    source_class: "committed_synthetic_fixture | inline_synthetic"
pipeline_steps:
  - step_id: "source_adapter"
    status: "completed | not_applicable_for_selected_case | blocked"
  - step_id: "candidate_report"
    status: "completed | blocked"
  - step_id: "harvest_review_packet"
    status: "completed | blocked"
  - step_id: "fixture_promotion_proof"
    status: "completed | blocked"
  - step_id: "golden_replay_fixture_manifest_draft"
    status: "completed | blocked"
  - step_id: "corpus_metadata_diff"
    status: "completed | blocked"
output_refs:
  - ref_id: "<public-safe report or in-memory summary id>"
    output_class: "public_safe_implementation_handoff | stdout_summary_public_safe"
authorization_flags:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
non_claims:
  parser_truth: false
  fixture_promotion_readiness: false
  private_smoke_success: false
  release_readiness: false
  production_readiness: false
  analytics_truth: false
  ai_truth: false
  coaching_truth: false
verdict: "dry_run_completed_public_safe | blocked | review_required"
```

## Status Vocabulary

Allowed dry-run statuses:

- `contract_only_no_run`
- `ready_for_fixture_safe_codex_c_after_review_and_approval`
- `dry_run_completed_public_safe`
- `review_required`
- `blocked_missing_user_approval`
- `blocked_private_input`
- `blocked_unapproved_output_location`
- `blocked_forbidden_content`
- `blocked_fixture_promotion`
- `blocked_corpus_metadata_change`
- `blocked_parser_behavior_change`
- `blocked_missing_validation`
- `blocked_broad_automation`

The status `dry_run_completed_public_safe` may mean only that the approved
fixture-safe dry-run shape completed. It must not mean parser behavior ready,
fixture promotion ready, private harvest ready, or #388 fully active.

## Required Preflight Checks

A later Codex C dry-run prompt must confirm:

- repository is `Tahjali11/Mythic-Edge`;
- remote URL matches `https://github.com/Tahjali11/Mythic-Edge`;
- worktree is clean or only contains approved scoped changes;
- issue #559 is the active dry-run issue;
- tracker #388 remains open;
- parent private-evidence issue #434 remains open;
- dependency #557 / PR #562 is merged;
- run mode is explicitly approved;
- selected input is synthetic or committed fixture-safe;
- private inputs remain unauthorized;
- output location class is approved;
- no fixture-promotion path is enabled;
- no corpus metadata edit path is enabled;
- no parser behavior change path is enabled;
- no GitHub issue or PR action path is enabled;
- no scheduled or recurring automation path is enabled.

Any missing, stale, ambiguous, or contradictory value is a stop condition.

## Redaction And Forbidden-Content Scans

All public or proposed-public outputs from a future dry run must be scanned for:

- local absolute paths;
- usernames;
- raw Player.log or UTC_Log excerpts;
- private JSON or JSONL payloads;
- exact private file names that reveal local structure;
- raw hashes;
- IP/network traces;
- screenshots;
- workbook export contents;
- SQLite file names or contents;
- credentials, tokens, API keys, webhook URLs, or secrets;
- decklists, card choices, private strategy notes, and player notes.

A scan failure must produce `blocked_forbidden_content` and must not be
"fixed" by moving the same content into another committed artifact.

## Error Behavior

The dry-run process must fail closed.

Required fail-closed behavior:

- Missing approval means `blocked_missing_user_approval`.
- Any private input means `blocked_private_input`.
- Any unapproved output location means `blocked_unapproved_output_location`.
- Any forbidden-content scan hit means `blocked_forbidden_content`.
- Any attempt to write fixtures means `blocked_fixture_promotion`.
- Any attempt to edit corpus metadata means `blocked_corpus_metadata_change`.
- Any parser behavior change means `blocked_parser_behavior_change`.
- Any missing required validation means `blocked_missing_validation`.
- Any recurring or broad automation request means `blocked_broad_automation`.

If a helper output is malformed, the report must identify the failed step and
route to Codex A or B for reframing, or Codex D only if a reviewed Codex C
implementation already exists and a concrete defect is found.

## Side Effects

Codex B side effects allowed by this contract:

- create or update `docs/contracts/parser_evidence_bounded_local_dry_run.md`.

Future Codex C side effects allowed only after review and explicit approval:

- run focused validation commands over committed source and synthetic data;
- print public-safe stdout summaries;
- create a public-safe implementation handoff/report if authorized.

Side effects not allowed:

- private source reads;
- private source writes;
- fixture creation;
- fixture promotion;
- corpus metadata edits;
- parser behavior changes;
- issue creation;
- PR creation;
- branch creation for execution artifacts;
- commits;
- pushes;
- scheduled automation;
- production-facing changes.

## Compatibility

The dry run must preserve the existing #381 through #387 helper contracts and
schema labels:

- `parser_evidence_harvest_candidate_summary.v1`
- `parser_evidence_harvest_review_packet.v1`
- `parser_evidence_fixture_promotion_proof.v1`
- `parser_evidence_golden_replay_fixture_manifest_drafts.v1`
- `parser_evidence_corpus_metadata_diff.v1`

The dry run may compose those artifacts for review. It must not reinterpret
their false authorization flags, promote their outputs, or widen their input
classes.

## Non-Claims

This contract and any future #559 dry-run report must not claim:

- parser behavior readiness;
- strict `pipeline_activation_ready_for_issue_388`;
- private harvest authorization;
- private smoke success;
- fixture-promotion readiness;
- corpus status change readiness;
- coverage confirmation;
- full parser regression parity;
- merge readiness;
- release readiness;
- production readiness;
- workbook truth;
- analytics truth;
- AI truth;
- coaching truth;
- gameplay advice;
- hidden-card inference;
- player-mistake labels.

## Validation Requirements

Codex B validation for this contract:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_bounded_local_dry_run.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_bounded_local_dry_run.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_bounded_local_dry_run.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Later Codex C validation, if explicitly approved:

```bash
python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py tests/test_fixture_promotion_proof.py tests/test_golden_replay_fixture_manifest_drafts.py tests/test_corpus_metadata_diff_generator.py
git diff --check
printf '%s\n' docs/implementation_handoffs/parser_evidence_bounded_local_dry_run_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/implementation_handoffs/parser_evidence_bounded_local_dry_run_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

If Codex C adds any source file despite this contract's default no-source-code
boundary, that is a contract mismatch unless a later amended contract
explicitly authorizes it.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_evidence_bounded_local_dry_run.md`.
- The default dry-run path is fixture-safe and synthetic.
- Private Player.log and UTC_Log reads remain blocked.
- Local/private artifact locations remain blocked by default.
- Fixture creation and promotion remain blocked.
- Corpus metadata edits remain blocked.
- Parser behavior changes remain blocked.
- The future dry-run report shape includes commands, input refs, output refs,
  validation, redaction, non-claims, and verdict.
- The next role is review before any execution-oriented Codex C pass.

## Next Workflow Action

Next role: Codex E for contract review.

Codex C dry-run execution may be considered only after this contract is
reviewed, submitted, merged, and the user explicitly approves the
fixture-safe run mode. A private-window run remains blocked pending a separate
private-evidence contract and approval path.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #559.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/559

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract artifact:
docs/contracts/parser_evidence_bounded_local_dry_run.md

Review goal:
Review the bounded local dry-run contract for #559. Confirm that it permits
only a future fixture-safe dry-run boundary after review and explicit user
approval, and that it does not authorize private log reads, fixture promotion,
corpus metadata edits, parser behavior changes, broad #388 activation,
readiness claims, issue/PR creation, commits, pushes, or automation.

Focus:
- allowed run modes and default selected path;
- private-input and local-artifact boundaries;
- dry-run report schema and status vocabulary;
- validation and forbidden-content scan requirements;
- preserved false flags;
- whether Codex C should remain blocked until explicit user approval.

Protected boundaries:
- Do not run the dry run.
- Do not read private Player.log, UTC_Log, app-data, live MTGA, diagnostics,
  drift, network/firewall, packet, OS/router, or private smoke evidence.
- Do not create fixtures, fixture-promotion packets, corpus metadata diffs,
  issue drafts, PR branches, commits, pushes, or local/generated artifacts.
- Do not claim parser_behavior_ready, pipeline_activation_ready_for_issue_388,
  fixture-promotion readiness, private smoke success, release readiness,
  production readiness, analytics truth, AI truth, coaching truth, or full
  parser regression parity.

Expected output:
- Findings first, if any.
- Contract verdict.
- Validation reviewed or run.
- Recommended next role.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/559"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  dependency_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/557"
  dependency_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/562"
  completed_thread: "B"
  next_thread: "E"
  verdict: "bounded_local_dry_run_contract_ready_for_review_no_execution_authorized"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-evidence-bounded-local-dry-run-559"
  dependency_merge_commit: "2bf909d55ea05587dc151adda71b0b7d6e84487f"
  target_artifact: "docs/contracts/parser_evidence_bounded_local_dry_run.md"
  selected_path: "fixture_safe_synthetic_in_memory_after_review_and_explicit_user_approval"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "printf '%s\\n' docs/contracts/parser_evidence_bounded_local_dry_run.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_evidence_bounded_local_dry_run.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_evidence_bounded_local_dry_run.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not run the dry run before contract review and explicit user approval."
    - "Do not read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift, network/firewall, packet, OS/router, or private smoke evidence."
    - "Do not create fixtures, promote fixtures, update corpus metadata, change parser behavior, or claim readiness."
    - "Do not activate broad #388 execution, private harvest, scheduled automation, issue/PR creation, commits, pushes, merge, deploy, analytics truth, AI truth, or coaching truth from this contract."
```
