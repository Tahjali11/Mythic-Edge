# Core Secret/Private Marker Scanner Fresh ARS/Refactor Evidence Preflight

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/681>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS evidence gate: <https://github.com/Tahjali11/Mythic-Edge/issues/664>

Source decision packet issue: <https://github.com/Tahjali11/Mythic-Edge/issues/669>

Source decision packet PR: <https://github.com/Tahjali11/Mythic-Edge/pull/670>

Source decision packet merge commit:
`9a3b3af3e0022145cc9cd6f562e0e7c3d5695a22`

Source decision packet artifact:
`docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`

Target candidate: `tools/check_secret_patterns.py`

Candidate id: `secret_private_marker_scan`

Candidate class: `local_advisory_check_surface`

## Module

`core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight`

This contract defines the preflight gate that must be satisfied before any
future Codex C implementation may decompose the secret/private marker scanner.

Plain English: issue #669 decided that the scanner may only be decomposed
inside the same repository, behind the same public command, and only after
either fresh scoped ARS/refactor evidence exists or the owner explicitly
accepts proceeding without that fresh evidence. This issue defines what those
two routes must contain. It does not collect the evidence or approve the
implementation.

This contract is planning-only. It does not implement code, move files, open a
PR, run ARS, run Refactor Scout, inspect private evidence, inspect source
beyond public repo artifacts needed for contract writing, change scanner
behavior, change command-line arguments, change scan modes, change output or
exit-code semantics, change safe-excerpt behavior, change public-safe/no-echo
boundaries, change checked-file selection, change CI, or claim readiness,
security assurance, privacy assurance, or parser truth.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: https://github.com/Tahjali11/Mythic-Edge
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/681
- Project roadmap / tracker: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Broad decomposition tracker: https://github.com/Tahjali11/Mythic-Edge/issues/463
- Related ARS evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/664
- Source decision packet issue: https://github.com/Tahjali11/Mythic-Edge/issues/669
- Source decision packet PR: https://github.com/Tahjali11/Mythic-Edge/pull/670
- Target artifact:
  `docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md`

## Source Artifacts Inspected

- GitHub issue #681
- GitHub issue #568
- GitHub issue #463
- GitHub issue #664
- GitHub issue #669
- GitHub PR #670
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`

No private logs, private evidence, local app-data, runtime artifacts, failed
posts, workbook exports, generated data dumps, credentials, tokens, secret
values, live endpoint values, ARS run artifacts, Refactor Scout artifacts,
private scan outputs, source-repo mutation surfaces, raw diffs, or private
source snippets were read, created, imported, or modified.

## Owning Layer

Primary layer: repository coordination and agent workflow / Quality and
Governance local advisory check surface.

This contract governs only the evidence-preflight authority needed before a
future behavior-preserving decomposition of `tools/check_secret_patterns.py`.
It does not own scanner behavior, parser truth, EventBus behavior, API payload
shape, frontend behavior, live-capture behavior, workbook/webhook behavior,
Apps Script behavior, CI enforcement, security assurance, or privacy
assurance.

## Internal Project Area

Quality and Governance local advisory checks.

The candidate remains a repo-local advisory scanner. It supports workflow
validation by flagging secret-looking values and private-marker patterns in
repo files selected by the scanner. Its output is review evidence only.

## Truth Owner

- `tools/check_secret_patterns.py` owns the current scanner command surface,
  scan modes, finding categories, severity/result semantics, report rendering,
  safe-excerpt handling, and exit-code behavior.
- `tests/test_check_secret_patterns.py` owns the current behavior-preservation
  test expectations for the scanner.
- The #669 decision packet owns the decomposition decision and same-repo-first
  boundary.
- This #681 contract owns only the evidence-preflight and owner-acceptance
  vocabulary before any later implementation.
- Repo governance docs, current issues, current contracts, accepted ADRs, and
  human owner decisions remain the authority for workflow routing.

## Bridge-Code Status

`not_bridge_code`

This contract does not bridge parser facts, EventBus delivery, API payloads,
frontend state, live capture, workbook data, webhook data, or Apps Script. It
is a governance preflight for a local advisory helper.

## Files Owned By This Contract

- `docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md`

Files referenced but not owned:

- `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_repo_inspection_authorized: false
source_mutation_authorized: false
private_evidence_inspection_authorized: false
private_evidence_storage_authorized: false
scanner_behavior_change_authorized: false
cli_contract_change_authorized: false
scan_mode_change_authorized: false
exit_code_change_authorized: false
finding_category_change_authorized: false
severity_semantics_change_authorized: false
safe_excerpt_change_authorized: false
no_echo_boundary_change_authorized: false
checked_file_set_change_authorized: false
ci_change_authorized: false
parser_behavior_change_authorized: false
eventbus_behavior_change_authorized: false
api_payload_change_authorized: false
frontend_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
workbook_webhook_change_authorized: false
apps_script_change_authorized: false
readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

Any future handoff, evidence packet, review, or implementation plan that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Observed Current Behavior

Issue #669 / PR #670 merged the Phase 5 decomposition decision packet for
`tools/check_secret_patterns.py`.

The source packet records:

- candidate id: `secret_private_marker_scan`;
- candidate class: `local_advisory_check_surface`;
- current path: `tools/check_secret_patterns.py`;
- final decision: `request_fresh_ars_refactor_evidence`;
- same-repo decomposition may be considered later only behind the same public
  command path;
- cross-repo extraction is rejected;
- scanner behavior, command arguments, scan modes, output, exit codes, finding
  categories, severity semantics, safe excerpts, public-safe/no-echo behavior,
  checked-file selection, and CI behavior must not change without a separate
  contract;
- future implementation needs either fresh scoped ARS/refactor evidence or
  explicit owner acceptance scoped to the candidate and target commit or
  branch.

The current scanner remains a local advisory helper. It is security/privacy
adjacent because it reports secret-looking values, private-marker categories,
and safe redacted excerpts. That status makes false authority risky: a later
thread must not confuse scanner decomposition with proof of security, proof of
privacy, proof that no private data exists, or approval to weaken scanner
coverage.

## Problem Statement And First Bad Values

The intended workflow is:

1. use #669 as the source decomposition decision;
2. satisfy this #681 preflight by either recording fresh scoped evidence or
   recording explicit owner acceptance to proceed without fresh evidence;
3. route to Codex C only after explicit user routing and only for a
   behavior-preserving same-repo implementation.

The first bad value is treating #669 as direct Codex C implementation
authority.

The second bad value is treating absent, stale, broad, mismatched, ambiguous,
or private-only ARS/refactor material as fresh scoped clearance.

The third bad value is treating owner acceptance as a blanket waiver. Owner
acceptance must name this issue, candidate, current path, target commit or
branch, allowed next role, and preserved boundaries.

The fourth bad value is echoing private evidence, private paths, raw scan
payloads, source snippets, raw diffs, secret-looking values, credentials,
tokens, endpoint values, failed-post payloads, runtime artifacts, workbook
exports, generated data, or local-only evidence into a public contract or
handoff.

The fifth bad value is claiming readiness, security assurance, privacy
assurance, no-secret status, no-private-data status, release readiness, deploy
readiness, production readiness, or parser truth from either an evidence
preflight or a scanner pass.

## Public Interface

This contract does not change the public scanner interface. For later
implementation planning, the preserved public interface remains:

- command path: `tools/check_secret_patterns.py`;
- CLI options: `--base`, `--repo-root`, `--paths-from-stdin`, and `--all`;
- scan modes: `changed-files`, `paths-from-stdin`, and
  `all-repo-advisory`;
- result values: `passed`, `warning`, `failed`, and `error`;
- severity values: `allowed`, `warning`, and `forbidden`;
- exit-code behavior from #669;
- report heading: `Secret / Private Marker Scan`;
- finding category ids and reason behavior covered by
  `tests/test_check_secret_patterns.py`;
- safe-excerpt and no-echo behavior;
- stdout/stderr routing;
- deterministic finding ordering.

Any proposed change to those items is outside this preflight and must route
back to Codex B.

## Evidence Route Vocabulary

A future handoff may use exactly one evidence route:

- `fresh_scoped_ars_evidence`: a current, public-safe ARS evidence summary
  exists for this exact candidate and target.
- `fresh_scoped_refactor_scout_evidence`: a current, public-safe Refactor
  Scout evidence summary exists for this exact candidate and target.
- `combined_fresh_scoped_evidence`: both ARS and Refactor Scout summaries
  exist and agree on the scoped route.
- `explicit_owner_acceptance_without_fresh_evidence`: the human owner has
  explicitly accepted proceeding without fresh scoped evidence for this
  candidate and target.
- `insufficient_or_stale_evidence`: evidence exists but is missing required
  fields, stale, superseded, too broad, private-only, or mismatched.
- `no_evidence_recorded`: no evidence or owner acceptance is recorded.
- `unsupported_evidence_route`: the proposed evidence route is not one of the
  allowed values above.

Only the first four route values may satisfy this preflight. The last three
must fail closed.

## Evidence Status Vocabulary

Each evidence route must also resolve to one status:

- `precondition_satisfied`: the evidence or owner acceptance satisfies this
  contract, and a later Codex C implementation may be considered only after
  explicit user routing.
- `fresh_but_blocking_findings`: evidence is fresh and scoped, but it reports
  blocker findings that must be resolved or accepted before implementation.
- `fresh_but_review_required`: evidence is fresh and scoped, but the summary
  raises ambiguity that requires Codex E or owner review.
- `stale_target_commit`: reviewed commit does not match the target commit and
  no current branch-scoped freshness rule applies.
- `stale_tool_bundle`: ARS or Refactor Scout version, contract, policy bundle,
  or route is not current for this question.
- `mismatched_candidate`: evidence does not name `secret_private_marker_scan`
  and `tools/check_secret_patterns.py`.
- `mismatched_repository`: evidence does not name `Tahjali11/Mythic-Edge`.
- `mismatched_boundary`: evidence assumes behavior, command, output,
  safe-excerpt, no-echo, checked-file-set, CI, or source-inspection changes.
- `too_broad`: evidence is project-wide or repo-wide without a candidate row
  for this scanner.
- `private_only`: evidence cannot be summarized publicly without unsafe
  private values or no-echo violations.
- `revoked`: owner or review explicitly revoked the evidence.
- `superseded`: a newer issue, contract, PR, or merge changed the target.
- `expired`: evidence age or stated expiry makes it no longer current.
- `unsupported`: evidence uses unsupported vocabulary or unknown authority.

Only `precondition_satisfied` may route toward Codex C, and even then only
after explicit user routing.

## Fresh Scoped ARS/Refactor Evidence Requirements

Fresh scoped evidence must be a public-safe summary from a separately
authorized ARS or Refactor Scout action. This #681 contract does not authorize
that action.

The evidence summary must include all required fields:

| Field | Requirement |
| --- | --- |
| `evidence_route` | One allowed value from this contract. |
| `evidence_status` | One allowed status from this contract. |
| `repository` | `Tahjali11/Mythic-Edge`. |
| `repository_url` | `https://github.com/Tahjali11/Mythic-Edge`. |
| `issue` | `https://github.com/Tahjali11/Mythic-Edge/issues/681` or the later implementation issue that explicitly consumes this preflight. |
| `source_decision_packet_issue` | `https://github.com/Tahjali11/Mythic-Edge/issues/669`. |
| `source_decision_packet_pr` | `https://github.com/Tahjali11/Mythic-Edge/pull/670`. |
| `source_decision_packet_merge_commit` | `9a3b3af3e0022145cc9cd6f562e0e7c3d5695a22` or a newer reviewed source packet commit if #669 is superseded. |
| `candidate_id` | `secret_private_marker_scan`. |
| `candidate_path` | `tools/check_secret_patterns.py`. |
| `candidate_class` | `local_advisory_check_surface`. |
| `reviewed_scope` | Must name this exact candidate path and not only the whole repo. |
| `reviewed_commit` | Exact commit reviewed, or branch plus base commit when branch-scoped evidence is explicitly allowed. |
| `target_commit_or_branch` | Exact future implementation target. |
| `evidence_tool` | `ARS`, `Refactor Scout`, or `ARS and Refactor Scout`. |
| `evidence_tool_version_or_contract` | Public-safe version, contract, policy bundle, or run descriptor. |
| `evidence_created_at` | Date or timestamp in UTC. |
| `evidence_authority_source` | Issue, PR, handoff, or owner instruction authorizing the evidence action. |
| `implementation_boundary_reviewed` | Must state same-repo behavior-preserving decomposition only. |
| `public_interface_change_detected` | Must be `false` to satisfy this preflight. |
| `safe_excerpt_no_echo_change_detected` | Must be `false` to satisfy this preflight. |
| `ci_or_enforcement_change_detected` | Must be `false` to satisfy this preflight. |
| `source_mutation_detected` | Must be `false` to satisfy this preflight. |
| `private_evidence_used` | Must be `false` for public evidence summaries unless a separate private-evidence lane exists and only symbolic public output is emitted. |
| `public_safe_summary` | Symbolic summary using only allowed public-safe categories. |
| `blocker_categories` | Public-safe symbolic categories, or empty list. |
| `advisory_categories` | Public-safe symbolic categories, or empty list. |
| `non_claims` | Must preserve the non-claims in this contract and #669. |
| `next_route` | One allowed routing label from this contract. |

Fresh evidence must fail closed if any required field is missing, unknown,
ambiguous, private-only, internally inconsistent, or contradicted by current
repo state.

## Explicit Owner Acceptance Alternative

Owner acceptance may substitute for fresh scoped evidence only when it is
explicit, current, and scoped.

Accepted owner-acceptance forms:

- a current user instruction in the active workflow thread that names issue
  #681, candidate id `secret_private_marker_scan`, path
  `tools/check_secret_patterns.py`, target commit or branch, and allowed next
  role;
- a GitHub issue comment by the owner on #681 or the later implementation
  issue that names the same fields;
- a reviewed handoff from Codex A/B/E/G that quotes or links the owner
  acceptance and preserves the false-authority flags;
- an explicit owner acceptance recorded in a future contract or PR description
  that is scoped to this candidate and reviewed before Codex C starts.

Required owner-acceptance fields:

| Field | Requirement |
| --- | --- |
| `acceptance_route` | `explicit_owner_acceptance_without_fresh_evidence`. |
| `owner_acceptance_source` | Current thread instruction, issue comment, handoff, contract, or PR text. |
| `accepted_issue` | Issue #681 or the later implementation issue. |
| `accepted_repository` | `Tahjali11/Mythic-Edge`. |
| `accepted_candidate_id` | `secret_private_marker_scan`. |
| `accepted_candidate_path` | `tools/check_secret_patterns.py`. |
| `accepted_target_commit_or_branch` | Exact commit or branch. |
| `accepted_next_role` | Codex C may be considered only after explicit routing. |
| `accepted_scope` | Same-repo behavior-preserving decomposition only. |
| `accepted_protected_boundaries` | Must preserve scanner behavior, command surface, output, exit codes, safe excerpts, no-echo boundary, checked-file set, and CI behavior. |
| `accepted_non_claims` | Must state no readiness, security assurance, privacy assurance, no-secret proof, no-private-data proof, release/deploy/production readiness, or parser truth. |
| `expiration_condition` | Must expire on target commit/branch change, scanner behavior change, interface change, new blocker finding, revoked acceptance, or superseding contract. |

Forbidden owner-acceptance forms:

- broad phrases such as `approval granted` without issue, candidate, and
  target scope;
- acceptance tied only to #669 without naming #681 or the implementation
  target;
- acceptance copied from an older closed issue without current owner renewal;
- acceptance supplied only by Codex without owner source;
- acceptance that authorizes source mutation, CI changes, private evidence
  reads, scanner behavior changes, or readiness/security/privacy claims;
- acceptance that cannot be made public-safe.

## Public-Safe Evidence Summary Rules

Allowed public-safe evidence summary content:

- repository name;
- candidate id and repo-relative path;
- reviewed commit, target commit, branch name, or PR number;
- evidence route and status labels from this contract;
- public-safe tool version, contract, or bundle labels;
- symbolic blocker/advisory categories;
- count-like summary fields when they do not expose private values;
- links to public issues, PRs, contracts, or handoffs;
- route recommendation and non-claim labels.

Forbidden public evidence summary content:

- secret-looking values;
- credentials, tokens, live endpoint values, or local environment values;
- private local paths;
- raw private logs or raw log fragments;
- failed-post payloads, runtime status payloads, generated-data dumps, or
  workbook exports;
- raw diffs, source snippets, or patches from private or source-repo
  inspection;
- exact private scan output;
- vulnerability proof payloads or exploit details;
- screenshots, workbook exports, local app-data, private decklists, or live
  MTGA data;
- any text that claims readiness, security assurance, privacy assurance,
  parser truth, no-secret status, or no-private-data status.

If evidence cannot be summarized without forbidden content, the public status
must be `private_only` and the route must fail closed.

## Routing Labels

Allowed route labels:

- `route_to_codex_c_after_explicit_user_routing`: precondition satisfied;
  implementation may be considered only after the user explicitly routes
  Codex C.
- `route_to_codex_e_review`: contract or evidence summary needs independent
  review.
- `route_to_codex_b_clarification`: contract or evidence vocabulary is
  ambiguous or incomplete.
- `route_to_codex_a_reframe`: scope, target, or authority changed enough to
  require new problem representation.
- `route_to_owner_decision`: owner must decide whether to accept proceeding
  without fresh evidence or request evidence gathering.
- `blocked_no_current_evidence_or_acceptance`: neither valid evidence nor
  valid owner acceptance exists.
- `blocked_private_or_unsafe_evidence`: evidence cannot be summarized safely.
- `blocked_behavior_change_requested`: proposed work changes scanner behavior
  or protected surfaces.
- `blocked_unsupported_authority`: authority source is stale, ambiguous,
  arbitrary, invented, or unsupported.

No route label authorizes implementation by itself.

## Codex C Preconditions

A later Codex C implementation may start only when all of these are true:

- #669 remains the current source decision packet or a newer reviewed packet
  explicitly supersedes it.
- This #681 preflight is reviewed or explicitly accepted by the owner.
- The route is one of:
  - `fresh_scoped_ars_evidence` with `precondition_satisfied`;
  - `fresh_scoped_refactor_scout_evidence` with `precondition_satisfied`;
  - `combined_fresh_scoped_evidence` with `precondition_satisfied`;
  - `explicit_owner_acceptance_without_fresh_evidence` with
    `precondition_satisfied`.
- The evidence or acceptance names `secret_private_marker_scan`,
  `tools/check_secret_patterns.py`, `Tahjali11/Mythic-Edge`, and the target
  commit or branch.
- The implementation scope remains same-repo behavior-preserving
  decomposition behind the existing public command path.
- The implementation does not change scanner behavior, command arguments,
  scan modes, output shape, exit-code semantics, finding categories, severity
  semantics, safe excerpts, no-echo behavior, checked-file selection, or CI.
- The user explicitly routes Codex C after the precondition is recorded.

If any condition is false, route to the appropriate fail-closed label above.

## Validation Expectations

Validation for this Codex B contract:

```bash
git diff --check
python3 tools/check_agent_docs.py
printf "%s\n" docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf "%s\n" docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf "%s\n" docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Recommended file hygiene scans for this new public contract:

```bash
LC_ALL=C grep -n '[^ -~]' docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md
tail -c 1 docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md | od -An -t x1
rg -n '[ \t]$' docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md
```

Validation for a later evidence-gathering issue must be defined by that issue.
This contract does not authorize ARS, Refactor Scout, source inspection,
private evidence inspection, run-artifact creation, or candidate dossier
creation.

Validation for a later Codex C implementation must include the #669
behavior-preservation checks and at minimum:

```bash
python3 tools/check_secret_patterns.py --base origin/main
printf "%s\n" tools/check_secret_patterns.py tests/test_check_secret_patterns.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 -m pytest -q tests/test_check_secret_patterns.py
python3 -m py_compile tools/check_secret_patterns.py
python3 -m ruff check tools/check_secret_patterns.py tests/test_check_secret_patterns.py
git diff --check
printf "%s\n" <changed-paths> | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf "%s\n" <changed-paths> | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf "%s\n" <changed-paths> | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

If helper modules are introduced in a later implementation, they must be added
to focused tests and path-scoped scans. If validation exposes a scanner
behavior mismatch, route to Codex D only when the mismatch is concrete and
within the approved implementation scope; otherwise route back to Codex B.

## Side Effects

This contract writes one documentation artifact only:

- `docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md`

No code, scanner behavior, tests, CI, runtime state, private evidence, ARS
artifacts, Refactor Scout artifacts, candidate dossiers, issues, PRs, comments,
labels, branches, commits, status checks, parser behavior, EventBus behavior,
API behavior, frontend behavior, live-capture behavior, workbook/webhook
behavior, or Apps Script behavior are created or changed by this contract.

## Dependency Order

The required workflow order is:

1. #669 decision packet remains current.
2. #681 preflight contract is reviewed.
3. Owner chooses either fresh scoped evidence gathering or explicit scoped
   owner acceptance.
4. Evidence or acceptance is recorded in public-safe form.
5. Codex E or owner confirms the precondition status.
6. User explicitly routes Codex C.
7. Codex C may compare implementation options against #669 and #681 without
   changing behavior beyond the approved same-repo decomposition boundary.

## Compatibility

This contract preserves all current scanner compatibility from #669. It does
not rename the tool, change command-line syntax, change scan modes, change
finding categories, change severity/result labels, change report output,
change exit-code behavior, change safe-excerpt tokens, change no-echo
requirements, change checked-file selection, or change tests.

## Acceptance Criteria

- The contract exists at the target path.
- The contract cites #681, #669, PR #670, #568, #463, and #664.
- The contract preserves #669's final decision:
  `request_fresh_ars_refactor_evidence`.
- The contract defines fresh scoped ARS/refactor evidence requirements.
- The contract defines explicit owner acceptance as a scoped alternative.
- The contract defines public-safe/no-echo evidence-summary rules.
- The contract defines fail-closed statuses and routing labels.
- The contract states that no evidence gathering, implementation, file move,
  source mutation, CI change, scanner behavior change, readiness claim,
  security assurance, privacy assurance, or parser truth claim is authorized by
  this contract.
- The contract defines Codex C preconditions for later implementation.
- The contract defines validation expectations for this contract and later
  implementation.

## Non-Claims

This contract does not claim:

- implementation readiness;
- decomposition implementation readiness;
- merge readiness;
- scanner behavior correctness beyond current tests and contract references;
- no-secret status;
- no-private-data status;
- security assurance;
- privacy assurance;
- parser truth;
- analytics truth;
- AI truth;
- coaching truth;
- reliability readiness;
- release readiness;
- deploy readiness;
- production readiness;
- ARS clearance;
- Refactor Scout clearance.

## Recommended Next Role

Next role: Codex E - Module Reviewer.

Codex E should review this preflight contract against issue #681, issue #669,
PR #670, issue #664, #568 Phase 5, and the current scanner contract. If the
contract is sound, Codex E should mark it ready for Codex F submission. Codex E
must not route to Codex C unless valid evidence or owner acceptance is already
recorded and the user explicitly routes implementation.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #681.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/681

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Related ARS evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/664

Source decision packet:
docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md

Target artifact:
docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md

Review goal:
Review the contract-only fresh scoped ARS/refactor evidence preflight for
tools/check_secret_patterns.py. Verify that it preserves #669's
request_fresh_ars_refactor_evidence decision, defines fresh scoped evidence
and explicit owner acceptance, keeps public-safe/no-echo evidence summaries,
fails closed on stale/mismatched/private-only evidence, and does not authorize
implementation, ARS, Refactor Scout, source inspection, private evidence reads,
scanner behavior changes, CI changes, readiness claims, security assurance,
privacy assurance, or parser truth claims.

Protected boundaries:
Do not implement code, move files, open a PR, run ARS, run Refactor Scout,
inspect private evidence, change scanner behavior, change CLI/output/exit-code
semantics, change safe-excerpt/no-echo behavior, change CI, change
parser/EventBus/API/frontend/live-capture/workbook/webhook behavior, or claim
readiness/security/privacy/parser truth.

Expected output:
Findings first. State whether the contract is ready for Codex F submission,
needs Codex B clarification, or is blocked. Include validation reviewed,
remaining risk, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/681"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/669"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/670"
  previous_merge_commit: "9a3b3af3e0022145cc9cd6f562e0e7c3d5695a22"
  completed_thread: "B"
  next_thread: "E"
  verdict: "fresh_scoped_ars_refactor_evidence_preflight_contract_ready_for_review"
  target_artifact: "docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md"
  source_artifact: "docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md"
  candidate_surface: "tools/check_secret_patterns.py"
  candidate_id: "secret_private_marker_scan"
  candidate_surface_class: "local_advisory_check_surface"
  final_decision_preserved: "request_fresh_ars_refactor_evidence"
  implementation_authorized: false
  file_move_authorized: false
  same_repo_decomposition_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  source_repo_inspection_authorized: false
  source_mutation_authorized: false
  private_evidence_inspection_authorized: false
  scanner_behavior_change_authorized: false
  cli_contract_change_authorized: false
  scan_mode_change_authorized: false
  exit_code_change_authorized: false
  finding_category_change_authorized: false
  severity_semantics_change_authorized: false
  safe_excerpt_change_authorized: false
  no_echo_boundary_change_authorized: false
  checked_file_set_change_authorized: false
  ci_change_authorized: false
  parser_behavior_change_authorized: false
  eventbus_behavior_change_authorized: false
  api_payload_change_authorized: false
  frontend_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
