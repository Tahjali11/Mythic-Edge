# Canonical Repository-Registry Bootstrap Contract Review

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/769

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Contract

`docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`

Reviewed SHA-256:
`f64dc584f780b0454d0dab59224796928e85f07c2f1bfb7a0574f7e0e217ac77`

## Implementation Under Test

Contract-only review on branch
`codex/role-pool-canonical-repository-registry-bootstrap-769` at
`17a71d182a1a189973f02a8e8c51669344823eb3`.

No registry or implementation bytes were created or reviewed.

## Report Lifecycle

`report_lifecycle: initial_contract_test`

## Contract Summary

The contract defines one future canonical, Core-only, validation-only
repository registry and one navigational authority-index refresh. It reuses
the accepted parser, registry validator, and R0 checker. Acceptance creates
eligibility for a separate owner implementation decision only.

## Internal Project Area Reviewed

`Governance / Role Pool`

## Bridge-Code Status Reviewed

`shared_support`

## Checks Run

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
gh issue view 769 --repo Tahjali11/Mythic-Edge --json ...
gh api repos/Tahjali11/Mythic-Edge/issues/comments/5137411208
py -B -m unittest test_check_pool_plan.py
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

The protected-surface and secret scans were also run in path-fed mode against
the untracked contract. Independent in-memory checks strictly parsed the
registry vector, reproduced all canonical digests and byte counts, exercised
the existing validator, rejected 19 one-at-a-time known-answer mutations, and
projected the proposed registry through the actual R0 selector and packet
builder.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. The contract contains only public
  repository, issue, actor, artifact, and digest bindings.
- Vocabulary coherence: passed. Registry, collision, precondition, terminal,
  eligibility, and non-claim terms agree with the accepted owners.
- Authority semantics: passed. Contract acceptance and checker eligibility do
  not become registry, release-state, task, R0, Stage-4, or readiness
  authority.
- Fail-closed schemas: passed. Closed field order, scalar types, canonical
  bytes, self-digests, unknown fields, duplicate keys, final LF, and exact
  known-answer equality remain independently checkable.
- Protected-surface rollout: passed. This is a contract-only prerequisite
  review; no authority artifact or operational state was created.

## Results

Passed.

- Live `origin/main`, local `HEAD`, and the required base all equal
  `17a71d182a1a189973f02a8e8c51669344823eb3`.
- Issue #769 is open with zero top-level comments.
- Owner comment `5137411208` remains unchanged, owner-authored, and bound to
  immutable actor ID `229644849`.
- All declared public artifact hashes recomputed exactly.
- The registry has 9 root fields and one 18-field entry.
- Entry bindings reproduced as `955` preimage bytes, `1037` complete bytes,
  self-digest
  `30bd9fec65f1c4c08158c2f0777646fc2c53113a845604c8f16aad072628ec1e`,
  and artifact SHA-256
  `754fc5e6c2046c9d6bab9dc4f550048282f0738143f9d04c63fb1b19cb93e330`.
- Registry bindings reproduced as `1393` preimage bytes, `1478` complete
  bytes, self-digest
  `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7`,
  and artifact SHA-256
  `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb`.
- The unchanged parser and validator accepted the exact registry with no
  errors.
- The actual R0 selector and packet builder projected
  `eligible_for_independent_review`, evidence self-digest
  `142d768a20aeed30eaa1f3510926ec94ee6d544e4c7f23dfad3d5685dbad3033`,
  `2621` bytes, and artifact SHA-256
  `894973a726fc0837064eee8d1df630994e0a3006817464f4bd317adfdf045802`.
- Focused validation passed: `97` registry-owner tests and `76` R0 checker
  tests.
- Agent-doc validation checked 54 files with 0 errors and 0 warnings.
- Protected-surface and secret scans reported forbidden 0 and warnings 0.
- No task-generated process or repository residue remained.

## Finding Lifecycle Summary

No findings.

## Confirmed Contract Matches

- Exact canonical registry and owner-selected authority shape.
- Fixed final path, absent release path, collision refusal, and fail-closed
  precondition drift.
- Exactly two future implementation files.
- Existing parser, validator, digest helper, and checker reuse.
- Six-column, twelve-row navigational index preservation and refresh rules.
- All five projected effect counts remain zero.
- All 16 projected authority fields remain false.

## Contract Mismatches

None.

## Missing Tests

None for contract acceptance. Exact implementation bytes and fixed-path
creation behavior require fresh Codex E review after separately authorized
Codex C work.

## Drift Notes

No blocking repository, contract, issue, validator, or public-binding drift
was observed. The current authority index is intentionally stale and is one of
the two contracted future implementation targets.

One ambient Codex App Server process owned by the desktop application predated
this review; no task or App Server process was created by this lane.

## Recommendation

Approve the contract. A separate owner implementation decision may authorize
Codex C to create only the exact registry and refresh only the navigational
index.

## Next Workflow Action

Next role: owner implementation decision, then Codex C.

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex C: Canonical Repository-Registry Bootstrap Implementer.

Use issue #769 and accepted contract
docs/contracts/role_pool_canonical_repository_registry_bootstrap.md at
SHA-256 f64dc584f780b0454d0dab59224796928e85f07c2f1bfb7a0574f7e0e217ac77.

Begin only after a separate exact owner implementation decision. Revalidate
the zero-comment condition and every contract binding. Create only the exact
1,478-byte registry and refresh only
docs/role_pool_current_authority_index.md. Run the contract-required
validation and stop without adoption, replacement, or cleanup on collision or
drift. Do not create release state, execute a task, advance R0-R8 or Stage 4,
or claim readiness. Route the exact two-file result to independent Codex E.
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
    - "workflow authority and repository registry"
    - "issue and tracker lifecycle"
    - "installed Role Pool and release state"
    - "R0-R8 and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "The current review is read-only apart from this required report. Future implementation remains separately owner-gated."
  stop_conditions:
    - "public binding or immutable identity drift"
    - "any top-level comment on issue #769"
    - "registry or release-state destination collision"
    - "scope beyond the exact two-file future implementation"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "E"
  next_thread: "owner_then_C"
  source_artifact: "docs/contracts/role_pool_canonical_repository_registry_bootstrap.md"
  target_artifact: "docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_future_submission_authority"
  branch: "codex/role-pool-canonical-repository-registry-bootstrap-769"
  validation:
    - "97 registry-owner tests passed"
    - "76 R0 checker tests passed"
    - "canonical registry and projected packet bindings exact"
    - "agent docs, protected-surface, secret, process, and residue checks passed"
  stop_conditions:
    - "owner implementation decision absent"
    - "issue #769 receives a top-level comment"
    - "registry or release-state destination appears"
    - "future implementation requires more than two exact files"
```
