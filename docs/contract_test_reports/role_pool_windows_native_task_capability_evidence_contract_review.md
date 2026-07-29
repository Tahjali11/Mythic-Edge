# Contract Test Report: Windows Native-Task Capability Evidence Contract

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/757

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Contract

`docs/contracts/role_pool_windows_native_task_capability_evidence.md`

Reviewed contract SHA-256:
`d165838cf77ff1e9d9f765ece0f68dd86d89b6370a4515f1d6b55b0ccae9ebef`.

Review authority:

- [Agent constitution](../agent_constitution.md)
- [Contract-test role](../agent_threads/contract_test.md)
- [Contract-test report template](../templates/contract_test_report.md)

## Implementation Under Test

Contract-only package on branch
`codex/role-pool-native-task-capability-evidence-757`.

- `HEAD`: `9dbc34e74d067c094bb2995480e47852eb3ab671`
- Base: `origin/main@9dbc34e74d067c094bb2995480e47852eb3ab671`
- Reviewed path:
  `docs/contracts/role_pool_windows_native_task_capability_evidence.md`
- No implementation, host metadata, task, installation, registry, release
  state, dispatch, canary, R0, or Stage-4 operation was reviewed or executed.

## Report Lifecycle

`report_lifecycle: final_approval`

## Contract Summary

The contract defines a read-only, metadata-first evidence boundary for deciding
whether a trusted Windows Codex runtime exposes the exact
`codex:native-task-create/v1` capability and all nine required guarantees. It
must derive exactly one of three closed verdicts without using generic
subagent behavior, repository tests, or a task-creating probe as production
evidence. Contract acceptance must preserve all operational authority as
false.

## Internal Project Area Reviewed

`Quality / Governance`

This matches issue #757 and the contract.

## Bridge-Code Status Reviewed

`shared_support`

The contract defines evidence and routing semantics only. The first-party
runtime remains the capability truth owner, and the accepted profile remains
the requirements owner.

## Checks Run

```powershell
git fetch --prune origin
git status --short --branch
git remote get-url origin
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main

gh issue view 746 --repo Tahjali11/Mythic-Edge
gh issue view 757 --repo Tahjali11/Mythic-Edge
gh issue view 755 --repo Tahjali11/Mythic-Edge
gh issue view 744 --repo Tahjali11/Mythic-Edge
gh pr list --repo Tahjali11/Mythic-Edge --state open
gh pr view 374 --repo Tahjali11/Mythic-Edge
gh pr view 391 --repo Tahjali11/Mythic-Edge
gh pr view 756 --repo Tahjali11/Mythic-Edge

git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

Additional deterministic review:

- recomputed the contract and accepted profile SHA-256 values;
- regenerated the existing canonical Role Pool managed manifest;
- verified the two future registry and release-state paths remain absent;
- read the production installer observer and the canonical synthetic adapter
  boundary without invoking either;
- parsed the nine-fact table and three-verdict vocabulary;
- enumerated all 19,683 combinations of the three evidence states over nine
  facts; and
- ran path-fed protected-surface and secret/private-marker scans over the
  untracked contract and this report.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. The future report excludes raw
  descriptors, task content, task identifiers, private paths, installed paths,
  environment values, credentials, raw host output, and exception details.
- Vocabulary coherence: passed. Exactly three verdicts and three fact-level
  evidence states are defined. The nine fact IDs are ordered and closed.
- Authority semantics: passed. Even exact capability support permits only
  routing to frame the next prerequisite; it does not authorize a task,
  installation, registry, release state, dispatch, canary, R0, Stage 4,
  submission, merge, deployment, or readiness.
- Fail-closed behavior: passed. Missing, stale, indirect, untrusted,
  conflicting, private, or task-dependent evidence selects
  `insufficient_evidence`. A directly authoritative negative selects
  `capability_unavailable`.
- Protected-surface rollout: passed. Contract review is separate from
  metadata inspection, and metadata inspection is separate from any future
  single-use synthetic characterization.
- ADR-0008: passed for this review. PRs #374 and #391 remain open. The current
  user invocation supplies a fresh task-scoped `explicit_user_override` for
  this E review only; it expires with this report and does not transfer to the
  metadata inspector.

## Results

`approve`

No blocking or nonblocking contract finding was identified.

Contract verdict:

`accepted_exact_windows_native_task_capability_evidence_contract`

This is contract acceptance only. Capability support remains unobserved and
unaccepted.

## Finding Lifecycle Summary

No findings.

## Confirmed Contract Matches

- Repository, branch, issue, tracker, open-PR, and ADR-0008 bindings are
  current.
- Issue #757 is open and is a native child of tracker #746.
- Issues #744 and #755 are closed; PR #756 is merged at the current Core base.
- PRs #374 and #391 are the only open Core pull requests.
- The supplied stale profile digest is rejected. The repository and issue both
  bind the refreshed profile SHA-256
  `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322`.
- The canonical Role Pool source recomputes to 34 files and 2,001,219 bytes.
- The canonical manifest recomputes to 4,921 bytes and SHA-256
  `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175`.
- The production installer capability observer is explicitly fail-closed and
  returns false because no exact production evidence is bound.
- The repository task adapter is explicitly `synthetic_only`, one-use, and
  cannot establish production capability truth.
- The facts are exactly:
  `windows_host_identity`,
  `exact_launcher_available_and_compatible`, `request_binding`,
  `one_task_cardinality`, `receipt_binding`, `timeout_enforcement`,
  `unknown_outcome_fail_closed`, `automatic_retry_forbidden`, and
  `fallback_forbidden`.
- The verdicts are exactly `exact_capability_supported`,
  `capability_unavailable`, and `insufficient_evidence`.
- The deterministic selector covers all `3^9 = 19,683` combinations:
  `capability_unavailable=19,171`, `insufficient_evidence=511`, and
  `exact_capability_supported=1`, with overlap `0` and uncovered `0`.
- Generic subagent behavior, thread tools, tests, mocks, shell/process
  discovery, and user-entered claims cannot satisfy a production fact.
- Metadata inspection must precede task creation and must leave task creation,
  retry, fallback, and persistent workflow mutation counts at zero.
- The current authority index is correctly treated as stale navigation after
  the #756 merge and #755 closure.
- All current, review, metadata-inspection, and terminal operational authority
  remains false.

## Contract Mismatches

None.

## Missing Tests

None for contract acceptance. The deterministic verdict domain was enumerated
independently. No capability test or task characterization was authorized or
needed for this contract-only review.

## Drift Notes

- Core, issue, tracker, profile, source, and manifest drift: none.
- PR lifecycle drift: none. #374 and #391 remain open; #756 is merged.
- Authority-index drift: expected and explicitly handled. Its snapshot predates
  current Core and must not be used for this decision.
- Installed-copy drift: not re-probed in this contract-only pass. The current
  issue records the fresh read-only `target_differs / drift` observation.
- Host capability state: unknown by design. No metadata source was inspected.

## Recommendation

`approve`

After a separate owner decision, route to one metadata-only evidence
inspection. That pass may inspect only already exposed authoritative
first-party capability metadata, create only the contract-defined public-safe
evidence report, and must create zero tasks and zero persistent workflow
mutations.

## Next Workflow Action

Next role: separately authorized metadata-only capability evidence inspector.

Pasteable next-thread prompt after a fresh owner decision:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex C: Metadata-Only Windows Native-Task Capability Evidence
Inspector for https://github.com/Tahjali11/Mythic-Edge/issues/757.

Work on branch codex/role-pool-native-task-capability-evidence-757. Read the
accepted contract and independent contract-review report. Recompute their
digests and refresh origin/main, issue #757, tracker #746, ADR-0008, open PRs,
the accepted profile, canonical 34-file manifest, registry/release-state
absence, and current installed-copy observation before inspecting capability
metadata.

Inspect only authoritative first-party capability metadata already exposed
read-only to the current Codex runtime. Do not create a task to discover
whether task creation is authorized. Do not use generic subagent behavior,
thread tools, repository tests, mocks, shell output, process discovery,
executable discovery, environment variables, memory, or user-entered claims
as capability evidence.

Create only
docs/contract_test_reports/role_pool_windows_native_task_capability_evidence.md.
Project the nine facts in contract order, derive exactly one closed verdict,
and keep task_creation_count, automatic_retry_count, fallback_attempt_count,
and persistent_workflow_mutation_count at zero. Emit no raw descriptor, task
content, task ID, private path, installed path, environment value, credential,
exception text, or unrelated host detail.

Stop with insufficient_evidence if authoritative metadata is absent,
incomplete, conflicting, stale, private, or would require any task or other
forbidden operation. Do not install or synchronize the skill, create registry
or release state, dispatch, run canaries, advance R0-R8 or Stage 4, submit,
merge, deploy, or claim readiness. Route the durable result to fresh
independent Codex E review.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/757"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  role_performed: "Codex E: Independent Windows Native-Task Capability Evidence Contract Reviewer"
  completed_thread: "E"
  next_thread: "owner_decision_then_metadata_inspector"
  source_artifact: "docs/contracts/role_pool_windows_native_task_capability_evidence.md"
  target_artifact: "docs/contract_test_reports/role_pool_windows_native_task_capability_evidence_contract_review.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-native-task-capability-evidence-757"
  reviewed_contract_sha256: "d165838cf77ff1e9d9f765ece0f68dd86d89b6370a4515f1d6b55b0ccae9ebef"
  contract_verdict: "accepted_exact_windows_native_task_capability_evidence_contract"
  capability_evidence_inspected: false
  capability_verdict_created: false
  task_creation_count: 0
  persistent_workflow_mutation_count: 0
  installation_or_sync_performed: false
  registry_or_release_state_mutated: false
  dispatch_or_canary_performed: false
  r0_entry_or_advancement_performed: false
  stage4_authorized: false
  submission_or_merge_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Fresh owner metadata-inspection decision, then bounded metadata-only inspector"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md"
  protected_surfaces:
    - "first-party Codex task capability and launcher identity"
    - "task creation, receipt, timeout, unknown-outcome, retry, and fallback boundaries"
    - "Role Pool installation, registry, release state, dispatch, canary, R0, and Stage-4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "The stale supplied profile digest is explicitly rejected; current repository and issue bindings agree. The E-only explicit_user_override expires with this report."
  stop_conditions:
    - "binding or lifecycle drift"
    - "need to inspect host metadata during contract review"
    - "need to create a task or another persistent workflow object"
    - "scope expansion beyond the contract and review report"
```
