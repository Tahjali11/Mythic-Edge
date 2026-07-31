# R0 Terminal-Receipt Recovery Contract Review

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/771

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Coordination Surface

https://github.com/Tahjali11/Mythic-Edge/issues/769

## Contract

`docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md`

Reviewed SHA-256:
`a90d1f9478c48209a53cceba9607cbc3e0ee762420991ba6cd4d4871e283ed0f`

Accepted parent contract SHA-256:
`a96936c4237652ea1c74b3d63164fa6918bd9c90f509fd3d9f2fce24bb9bb61d`

Accepted parent review SHA-256:
`c3f07e5ba5dd51cc3bcfcbe3dbe9f2ba301da16c5988636e42d3d680bfb27ffd`

## Implementation Under Test

Contract-only terminal disposition and fresh-attempt recovery definition on
branch `codex/role-pool-r0-terminal-receipt-recovery-771` from
`origin/main@0e1c58496725b9df5cdde561a5aac0a3c4cb8edd`.

Before this report was created, the reviewed contract was the only changed
path. No GitHub comment, release state, implementation handoff, authority
index, registry, installed skill, or operational state was changed.

## Report Lifecycle

`report_lifecycle: final_approval`

## Contract Summary

The contract records the prior R0 bootstrap attempt as terminal after GitHub
stored a noncanonical consumption-comment body. The historical owner decision
is permanently nonreusable, the malformed comment remains immutable evidence,
and no canonical consumption receipt or release state is inferred.

A later distinct attempt must first integrate this contract and review, publish
fresh eligibility, and receive a distinct owner decision. Its sole comment POST
must carry canonical receipt bytes inside a one-key canonical API wrapper over
binary stdin to a direct non-shell `gh api` child process. Acceptance depends
on exact GitHub body-byte equality after one read-only reconciliation.

## Internal Project Area Reviewed

`Governance / Role Pool`

## Bridge-Code Status Reviewed

`shared_support`

## Governance Sources

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`

## Checks Run

```powershell
git status --short --branch
git diff --check
gh issue view 769 --repo Tahjali11/Mythic-Edge --json ...
gh api repos/Tahjali11/Mythic-Edge/issues/771/comments --paginate
gh api repos/Tahjali11/Mythic-Edge/issues/comments/5139550089
gh api repos/Tahjali11/Mythic-Edge/issues/comments/5139572911
gh api repos/Tahjali11/Mythic-Edge/issues/comments/5139603966
py -B tools\check_agent_docs.py
py -B tools\check_role_pool_r0_bootstrap.py
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py -k release_state -p no:cacheprovider
py -B -m unittest test_check_pool_plan.TrustedOwnerNativeProfileTests.test_external_isolation_classification_and_release_ladder
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

The unittest ran from
`docs/codex_skills/mythic-edge-role-pool/scripts`. The protected-surface and
secret scans were also run with the exact untracked contract path supplied by
`--paths-from-stdin`.

Independent in-memory checks used strict duplicate-key JSON parsing, rebuilt
both receipt vectors and the API wrapper, exercised the required reconciliation
distinctions, derived the historical record ID, and enumerated the complete
recovery selector.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. Public artifacts contain only approved
  issue references, digests, bounded statuses, and non-claim fields. The future
  transport forbids echoing command output, credentials, executable paths, or
  raw transport diagnostics.
- Vocabulary coherence: passed. `CP-03`,
  `r0_bootstrap_consumption_ambiguous`, `consumed_nonreusable`,
  `present_malformed_immutable_nonreceipt`, and
  `canonical_consumption_receipt_created=false` describe one coherent terminal
  state.
- Authority semantics: passed. Contract acceptance permits only submission and
  integration routing. It creates no fresh eligibility, owner decision,
  comment, release, R0, process, network, dispatch, Stage-4, merge, deployment,
  or readiness authority.
- Fail-closed schemas: passed. Exact body equality owns acceptance. Quote loss,
  line-ending changes, prefix or suffix bytes, duplicate exact bodies, related
  malformed bodies, wrong issue, wrong author, edit history, response
  contradiction, and unreadable comments all select ambiguity.
- Protected-surface rollout: passed. The contract remains in the existing
  issue #771 lane and changes no runtime or repository authority owner.

## Results

Passed with no blocking findings.

- The reviewed contract is an ordinary non-reparse file of 24,920 bytes with
  exact SHA-256
  `a90d1f9478c48209a53cceba9607cbc3e0ee762420991ba6cd4d4871e283ed0f`.
- Local HEAD, `origin/main`, and live GitHub `main` were exact at
  `0e1c58496725b9df5cdde561a5aac0a3c4cb8edd`.
- The parent contract and accepted review remained exact at
  `a96936c4237652ea1c74b3d63164fa6918bd9c90f509fd3d9f2fce24bb9bb61d`
  and
  `c3f07e5ba5dd51cc3bcfcbe3dbe9f2ba301da16c5988636e42d3d680bfb27ffd`.

### Historical Terminal Evidence

- Eligibility comment `5139550089` is owner-authored and unedited at
  `2026-07-31T05:19:13Z`, contains 2,764 bytes without a final LF, and has
  SHA-256
  `831b687f5df120f32e1b05143dab3bf52ec7f5c794c2cb395c185dac6a2e12c5`.
- Owner decision `5139572911` is owner-authored and unedited at
  `2026-07-31T05:23:18Z`, contains 3,174 bytes without a final LF, and has
  SHA-256
  `2ae7a827033c21fa0ac25e12f872f7fbba44340c7b036599047d3ea51499c331`.
- Comment `5139603966` is owner-authored and unedited at
  `2026-07-31T05:28:17Z`, contains 861 bytes with exactly one final LF, and has
  SHA-256
  `482e14a2acb0e69b7bdf97b2d45c4287cd3e0a0f8cf6dad6a9cbb6e2169f91b5`.
- Strict JSON parsing rejects comment `5139603966`; its keys and strings lack
  the required quotation marks.
- It is the only comment containing owner-decision reference `5139572911` and
  the only comment containing the consumption schema marker.
- Parent lifecycle selection is therefore `CP-03` with terminal result
  `r0_bootstrap_consumption_ambiguous`.
- Owner decision `5139572911` is permanently `consumed_nonreusable`. The
  malformed comment cannot be edited, deleted, reposted, or reinterpreted as a
  canonical receipt.
- No canonical consumption receipt, release-state record, index update, or
  implementation handoff was created.

### Canonical Receipt Comparison

- The historical record ID independently derives as
  `r0.bootstrap.e2c7cb44b7d3eb144c4b87d819c09128`.
- The intended historical candidate has 12 ordered fields.
- Its self-digest preimage is 819 bytes with SHA-256
  `bf74dc0e0ae70d6aca26b3a7831b3a1b5bf951c86772954990c05bd78c5f9371`.
- Its complete canonical candidate is 907 bytes with artifact SHA-256
  `850f51628bd6aec24b69698d7bbac7d7c707821141622442d9e69b864d5a823c`.
- The malformed body declares that intended self-digest, but its stored bytes
  are different. The canonical candidate remains prospective comparison
  evidence and was not treated as historical success.

### Binary Transport KAT

- The unchanged parent KAT has 12 fields, an 818-byte preimage, and a 906-byte
  complete canonical receipt.
- Its self-digest is
  `c1a27275f03f166ca52df60dc573c3e48fb40a92d63a9cefa545003a03247479`.
- Its complete artifact SHA-256 is
  `ad36c3ccf378d370a1ab5027857d852845ecdee9896b9da7df7f0f3330beb509`.
- Wrapping that body as canonical `{"body": ...}` JSON without a wrapper final
  LF produces exactly 964 bytes and SHA-256
  `f1a817216a8379fe1906540b24fbc7c4537f7a7463ac75ffd5318521766d6f1e`.
- Strict wrapper decoding returns one string whose UTF-8 bytes are exactly the
  original 906-byte receipt, including its final LF.

The direct non-shell, binary-stdin transport is constructible without placing
receipt bytes in a command line or requiring a repository helper, alternate
endpoint, fallback, edit, delete, or retry.

### Reconciliation Matrix

The following all selected `CP-03 publication_ambiguous`:

- quote loss;
- missing final LF;
- CRLF replacement;
- body prefix or suffix;
- duplicate exact bodies;
- a related malformed body;
- wrong issue;
- wrong author;
- edited comment;
- response URL contradiction; and
- unreadable comments.

A reported success with one exact body and an unknown call result with one
exact body selected `CP-01`. A known failure with no exact or related match
selected `CP-02`.

### Recovery Selector Audit

- Preflight vectors: `512`
- Parent consumption tuples: `12`
- Total tuples: `524`
- Recovery rows: `10`
- Reused parent rows: `3`
- Total rows: `13`
- Overlap count: `0`
- Uncovered count: `0`
- Unreachable-row count: `0`

Independent row counts were `[256,128,64,32,16,8,4,2,1,1]` for
`TRP-01` through `TRP-10`, followed by `CP-01=2`, `CP-02=1`, and
`CP-03=9`.

### Current-State And Validation Results

- Issue #769 remained open with zero top-level comments.
- Release state remained absent.
- The implementation-handoff destination remained absent.
- The current-authority index remained exact at
  `4fd141f4abcd725ec18779e14b3d82bfb0a651f834b90bbe637235c411ace274`
  and continued to report `absent_unactivated_release_state`.
- The stopped Codex C worktree was clean at the exact base.
- The R0 checker emitted the exact 2,621-byte packet with artifact SHA-256
  `894973a726fc0837064eee8d1df630994e0a3006817464f4bd317adfdf045802`
  and evidence self-digest
  `142d768a20aeed30eaa1f3510926ec94ee6d544e4c7f23dfad3d5685dbad3033`.
- Checker results were `source_install_status=identical`,
  `registry_status=valid_exact`,
  `release_state_status=absent_bootstrap_candidate`, and
  `terminal_status=eligible_for_independent_review`.
- All five checker effect counts were zero and all 16 checker authority fields
  were false.
- Focused release-state tests: `9 passed`, `67 deselected`.
- Release-ladder unittest: passed.
- Agent-doc validation: `54` files, `0` errors, `0` warnings.
- Base and explicit-path protected-surface scans: forbidden `0`, warnings `0`.
- Base and explicit-path secret/private-marker scans: forbidden `0`, warnings
  `0`.
- Diff and whitespace checks: passed.
- Matching task process count: `0`.
- Generated residue count: `0`.
- Open PRs #374 and #391 did not touch the recovery contract, parent contract,
  current-authority index, or release-state path.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-RP-771-C-002` | high | `fixed_state_followup` | `terminal_disposition_and_fresh_recovery_contract_confirmed` | not_blocking_for_contract_submission | GitHub stored noncanonical 861-byte comment `5139603966` after the single authorized POST. | Exact API readback confirms the malformed immutable body; the contract permanently spends decision `5139572911`, forbids historical repair, and defines a distinct future binary-safe transport and exact-body reconciliation route. | F |

## Confirmed Contract Matches

- Historical GitHub body bytes remain the sole owner of receipt truth.
- The malformed comment is immutable nonreceipt evidence.
- The historical owner decision is permanently nonreusable.
- Canonical comparison bytes are not reconstructed as historical success.
- Exact binary-stdin transport preserves the complete receipt body.
- Exact-body reconciliation rejects every required ambiguity class.
- Fresh eligibility and a distinct owner decision are mandatory after
  integration.
- The parent schema, release writer, index process, three-file implementation
  envelope, and R0 offline-only ceiling remain unchanged.
- Contract acceptance leaves every current authority and readiness field false.

## Contract Mismatches

None.

## Missing Tests

None for contract acceptance. The real transport remains intentionally
unexecuted. A separately authorized future Codex C attempt must dynamically
rebuild its fresh receipt and wrapper, enforce the direct-process bounds, make
at most one POST, and perform the one permitted exact API reconciliation.

## Drift Notes

No blocking repository, GitHub, index, registry, installed-tree, validator,
release-path, process, or residue drift was observed. The malformed comment is
historical external-state evidence, not repository drift and not repairable
state.

## Recommendation

Approve the terminal-receipt recovery contract for contract-only submission
and integration routing.

This acceptance does not authorize Codex F, merge, fresh eligibility, a fresh
owner decision, Codex C, comment publication, release creation, index refresh,
R0 acceptance, dispatch, R1-R8, Stage 4, deployment, or readiness. Fresh
eligibility and a distinct owner decision remain ineligible until this
contract and report are integrated.

## Next Workflow Action

Next role: separately approved Codex F for contract-only submission.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex F: R0 Terminal-Receipt Recovery Contract Submitter.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/771
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Branch: codex/role-pool-r0-terminal-receipt-recovery-771

Stage only:
- docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md
- docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md

Require contract SHA-256
a90d1f9478c48209a53cceba9607cbc3e0ee762420991ba6cd4d4871e283ed0f
and the exact report SHA-256 from the Codex E handoff.

Before submission, refetch issue #771 comments 5139550089, 5139572911, and
5139603966 and require their exact accepted bytes and unedited timestamps.
Require issue #769 to remain open with zero comments, release state and the
implementation handoff to remain absent, and the current-authority index to
remain exact.

Commit, push, and open or update only a draft PR linked to #771 and tracker
#746. Do not edit or delete comments, reuse the spent owner decision, create
fresh eligibility or authority, create release state, modify the index,
implement, merge, dispatch, advance R0-R8 or Stage 4, or claim readiness.
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
    - "GitHub consumption evidence"
    - "release-state authority"
    - "current-authority index"
    - "R0-R8 and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "This is the same active #771 lane returning from one terminal fail-closed attempt. PRs #374 and #391 are unrelated."
  stop_conditions:
    - "historical public comment or repository binding drift"
    - "issue #769 receives a top-level comment"
    - "release-state or implementation-handoff destination appears"
    - "scope expands beyond the contract and review report"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/771"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_submission_authority"
  branch: "codex/role-pool-r0-terminal-receipt-recovery-771"
  finding_status:
    ME-RP-771-C-002: "terminal_disposition_and_fresh_recovery_contract_confirmed"
  historical_lifecycle_result: "r0_bootstrap_consumption_ambiguous"
  historical_owner_decision_status: "consumed_nonreusable"
  canonical_consumption_receipt_created: false
  release_state_created: false
  fresh_eligibility_eligible: false
  fresh_owner_decision_eligible: false
  submission_authorized: false
  merge_authorized: false
  r0_accepted: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  validation:
    - "three historical comments exact and unedited"
    - "819/907-byte historical candidate comparison exact"
    - "906-to-964-byte binary transport KAT exact"
    - "524 tuples; 13 rows; audit 0/0/0"
    - "R0 checker and focused release validation passed"
    - "agent-doc and path-scoped safety checks passed"
  stop_conditions:
    - "historical comment or binding drift"
    - "release-state or index mutation"
    - "scope beyond the contract and report"
  next_recommended_role: "Separately approved Codex F: contract-only submitter"
```
