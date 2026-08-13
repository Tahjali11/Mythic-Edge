# Mythic Edge Issue Wave Skill Contract Test Report

## Findings

No blocking findings remain on the exact current checkpoint/two-wave package.

### ME-IW-855-E-008 - P1 - fixed confirmed on current bytes

- `finding_lifecycle`: `fixed_state_followup`
- `finding_status`: `fixed_confirmed_current_bytes`
- `blocking_status`: `not_blocking`
- `next_route`: `none`

The prior report proved that ordinary checkpoint and terminal release could
clear an expired reservation without the required recovery proof. Codex D
placed the correction in `release_run` after the shared monotonic-time check
and before event construction or persistence.

Fresh Codex E verification independently confirmed both release forms:

- at lease expiry plus one second, release raises
  `recovery_proof_required` and `run.json` plus `events.jsonl` remain
  byte-identical;
- at the exact expiry timestamp, the same otherwise-valid release succeeds;
- the expiry refusal occurs before `_coordination_event` and `_persist_event`,
  so it cannot append an event or replace the projection.

The exact regression slice passed `2 passed, 158 deselected`, and the complete
focused suite passed `160 passed` on the same helper bytes.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | current verification evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- |
| `ME-IW-855-E-001` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | E binds only the pre-commit package; F-only commit, package, branch, draft-PR, and check fields remain transition-scoped and immutable. | none |
| `ME-IW-855-E-002` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | Equality and both nesting directions across state, checkout, and worktree paths fail closed with loser state unchanged. | none |
| `ME-IW-855-E-003` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | One bounded admission lock covers scan through atomic publication; concurrent same-lane admission admits at most one wave and persistent locks fail closed. | none |
| `ME-IW-855-E-004` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | Public text rejects drive, POSIX, and both UNC absolute-path forms without echo while retaining safe relative, symbolic, and HTTPS text. | none |
| `ME-IW-855-E-005` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | Transition, renewal, release, segment authorization, and recovery reject backward event time without durable mutation. | none |
| `ME-IW-855-E-006` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | Resume requires the complete ordered lane/head/artifact proof and binds its canonical digest into the event and immutable segment history. | none |
| `ME-IW-855-E-007` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | Inspect emits continuation output only for a released, aligned checkpoint with one exact next role. | none |
| `ME-IW-855-E-008` | P1 | `fixed_state_followup` | `fixed_confirmed_current_bytes` | not_blocking | Checkpoint and terminal expiry-plus-one releases fail before persistence with byte-identical state; exact-expiry release succeeds. | none |

## Issue And Authority

- Issue: [#855](https://github.com/Tahjali11/Mythic-Edge/issues/855)
- Draft PR: [#856](https://github.com/Tahjali11/Mythic-Edge/pull/856)
- Contract: `docs/contracts/mythic_edge_issue_wave_skill.md`
- Contract SHA-256:
  `aa29efa936e08068358860c10f7f9e78040ea6e44312cc5a537080ca76bc2e2b`
- Implementation handoff:
  `docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md`
- Constitution: `docs/agent_constitution.md`
- Reviewer rules: `docs/agent_threads/review.md` and
  `docs/agent_threads/contract_test.md`
- Template: `docs/templates/contract_test_report.md`
- Accepted ADRs: ADR-0008 and ADR-0012
- `report_lifecycle`: `final_approval`

Live review evidence showed issue #855 open with its explicit WIP-1 exception.
PR #856 remained open, draft, and mergeable at pushed head
`e36b6f7e31ba4c7d3ebfff1fcadbf307faec64a1`, targeting
`main@702ed7c498049888c7cfc0a9cf6bf9a901d4f6f8`. Its six visible checks passed
for that older pushed head; they are not evidence for the current uncommitted
checkpoint/two-wave revision.

## Implementation Under Test

The current checkout remained at
`e36b6f7e31ba4c7d3ebfff1fcadbf307faec64a1` with an empty index. The complete
working package contains exactly these 11 paths:

1. `docs/codex_skills.md`
2. `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
3. `docs/codex_skills/mythic-edge-issue-wave/agents/openai.yaml`
4. `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
5. `docs/codex_skills/mythic-edge-issue-wave/references/state-schema.md`
6. `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
7. `docs/contract_test_reports/mythic_edge_issue_wave_skill.md`
8. `docs/contracts/mythic_edge_issue_wave_skill.md`
9. `docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md`
10. `tests/test_install_codex_skills.py`
11. `tests/test_mythic_edge_issue_wave_skill.py`

Every path is `modified` relative to the review base and uses regular blob
mode `100644`. No staged, unmerged, symlink, gitlink, intent-to-add, ignored,
or additional non-ignored path is part of the package.

The exact canonical `mythic_edge_issue_wave_reviewed_package.v1` binding is
computed after this report receives its final bytes and is carried in the
Codex E handoff to F. It is not self-embedded here because this report is one
of the manifest entries: embedding the package digest would change the report
bytes and invalidate that digest. Codex F must independently reconstruct the
same 11-entry manifest from the unchanged worktree before staging and require
an exact binding match.

## Confirmed Contract Matches

- Grammar supports bare autonomous Dispatch, the five new A-start checkpoint
  ranges, and aligned exact-next-role saved segments while rejecting malformed,
  backward, skipped, D-inclusive, permission-incompatible, and post-F forms.
- Explicit segments stop at their endpoint without launching the next role;
  unaffected lanes may complete while stopped lanes are not replaced.
- Two genuinely simultaneous disjoint waves can pass serialized admission;
  shared repositories, a third active wave, cross-run scope/path overlap, and
  persistent locks fail closed before repository effects.
- Active reservations use five-minute leases with a 60-second maximum renewal
  interval. Checkpoint and terminal release preserve work and history. Expiry
  neither releases nor authorizes work and requires the recovery route.
- Recovery requires task/agent termination proof, stable preserved state, and
  no active operation. In-flight uncertainty becomes
  `unknown_agent_outcome` and is never automatically retried or resumed.
- Manual advancement is detected as drift and is never imported, inferred, or
  retrospectively certified.
- Invocation, run, event, event-request, and Inspect projections are V2;
  candidate and reviewed-package manifests remain V1.
- The reviewed-package E/F handshake keeps E pre-commit and F as the sole
  owner of staging, commit, push, and draft-PR evidence.
- Public outputs reject local paths and sensitive markers without echo.
  Inspect omits private locations and produces continuation text only at a
  safe released checkpoint.
- Checkpoints surface governance packets without creating H; terminal routing
  aggregates material packets once and leaves task creation with root Codex.
- The helper imports only deterministic standard-library modules and has no
  Git, GitHub, network, native-agent, task-creation, installation, merge, or
  deployment capability.
- The explicit-only UI metadata remains aligned with the skill and cannot
  implicitly replace the legacy Role Pool.
- The legacy Role Pool tracked tree remains exactly
  `950768b80b760a0e0dfe3040df023de20eadaf81` with 38 files and zero changed
  paths.

## Checks Run

```text
E-008 checkpoint/terminal expiry boundary: 2 passed, 158 deselected
full focused issue-wave suite: 160 passed
installer suite: 45 passed, 3 filesystem-capability skips
installer list: passed; four repo-owned skills listed
Ruff on helper and focused/installer tests: passed
agent docs: 55 checked, 0 errors, 0 warnings
protected-surface scan: 11 changed paths, 0 forbidden, 0 warnings
secret/private-marker scan: 11 changed paths, 0 forbidden, 0 warnings
Python compilation: passed
git diff --check: passed
legacy Role Pool: exact tree, 38 files, zero changed paths
```

The focused and installer suites used separate isolated writable temporary
roots and disabled repository pytest caches. The three installer skips are
only unavailable directory-symlink capability on this filesystem.

The official skill-creator validator could not start because its available
interpreter lacks PyYAML; no dependency was installed. The full focused suite
includes the source-equivalent frontmatter, metadata, explicit-invocation,
reference, and skill-discovery checks, and the installer suite passed.

## Governance Checks Reviewed

- Public-safe/no-echo: passed on all changed paths and representative helper
  inputs.
- Vocabulary coherence: invocation, state, stop, check, lease, recovery, and
  route terms match the contract's closed vocabulary.
- Authority semantics: parsing, validation, E approval, F completion, passing
  checks, and `g_consideration_ready` are evidence states only and grant no
  merge, deployment, installation, production, or later-Dispatch authority.
- Fail-closed schemas: duplicate/unknown fields, malformed identities,
  invalid transitions, stale revisions, broken chains, path conflicts,
  expired leases, proof drift, and uncertain outcomes are covered.
- Protected rollout: the package changes only workflow coordination source,
  tests, and durable A-G artifacts. No product-runtime or legacy R0 surface
  changed.

## Contract Mismatches And Missing Tests

None found on current bytes.

## Drift And Residual Risk

- PR lifecycle drift remains until Codex F creates the new commit, pushes it,
  updates PR #856, and obtains checks for the new head.
- Official skill-creator validation remains unavailable in the current local
  environment because PyYAML is absent; source-equivalent and installer
  validation passed.
- No real write-enabled Dispatch, installation, deployment, parser, workbook,
  webhook, credential, production, or cross-machine behavior was exercised;
  those surfaces remain outside this package and its authority.
- The owner's conditional merge-and-close approval is reserved for Codex G
  after successful F and fresh live integration gates. Codex E does not
  consume or broaden that authority.

## Recommendation

`approve`

Verdict: `eligible_for_codex_f_draft_pr_update`

Codex F may stage only the exact E-bound 11-path package, create one new commit
without amending the existing commit, prove the new commit has the review base
as its sole parent and contains the exact package binding, push the existing
branch, update draft PR #856, and wait for its current-head checks. F must make
no implementation edit and must stop on any byte, path, mode, status, index,
parent, package, branch, PR, or check drift.

F does not merge, install, perform a real Dispatch, deploy, clean preserved
state, close issue #855, or consume the owner's conditional G authority.

## Pasteable Codex F Handoff

```text
Act as Mythic Edge Codex F for issue #855 on branch
agent/mythic-edge-issue-wave-855. Invoke $mythic-edge-workflow and refresh
current repo authority, live issue #855 and draft PR #856, accepted ADR-0008
and ADR-0012, contract SHA-256
aa29efa936e08068358860c10f7f9e78040ea6e44312cc5a537080ca76bc2e2b,
the implementation handoff, and this final Codex E report. Confirm HEAD is
e36b6f7e31ba4c7d3ebfff1fcadbf307faec64a1, the index is empty, and the exact
11-path current package reconstructs to the reviewed-package binding supplied
in the E handoff. Stage only those paths, rebind the index, create one new
commit without amending, prove its sole parent is the review base and its
package binding is identical, then push the existing branch and update draft
PR #856 with current evidence. Wait for and report checks on the new exact
head. Stop on any drift. Make no implementation edit. Do not merge, install,
perform a real Dispatch, deploy, clean preserved state, or close #855. The
owner's conditional merge-and-close approval belongs to a later Codex G pass
only after successful F and fresh live integration gates.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: fresh final checkpoint/two-wave contract reviewer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/855"
  pr: "https://github.com/Tahjali11/Mythic-Edge/pull/856"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md"
  target_artifact: "draft PR #856 update"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main"
  branch: "agent/mythic-edge-issue-wave-855"
  review_base_commit: "e36b6f7e31ba4c7d3ebfff1fcadbf307faec64a1"
  reviewed_path_count: 11
  verdict: "eligible_for_codex_f_draft_pr_update"
  finding_status:
    ME-IW-855-E-001: "fixed_confirmed_current_bytes"
    ME-IW-855-E-002: "fixed_confirmed_current_bytes"
    ME-IW-855-E-003: "fixed_confirmed_current_bytes"
    ME-IW-855-E-004: "fixed_confirmed_current_bytes"
    ME-IW-855-E-005: "fixed_confirmed_current_bytes"
    ME-IW-855-E-006: "fixed_confirmed_current_bytes"
    ME-IW-855-E-007: "fixed_confirmed_current_bytes"
    ME-IW-855-E-008: "fixed_confirmed_current_bytes"
  validation:
    - "160 focused issue-wave tests passed"
    - "45 installer tests passed; 3 filesystem-capability skips"
    - "Ruff, docs, protected-surface, secret, compile, diff, and legacy identity checks passed"
    - "E-008 checkpoint and terminal expiry boundaries independently confirmed"
  stop_conditions:
    - "any package, base, index, parent, branch, PR, or check drift"
    - "any implementation edit"
    - "installation, real Dispatch, merge, deployment, cleanup, or issue closure"
  next_recommended_role: "Codex F"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high workflow risk"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
    - "ADR-0012"
  protected_surfaces:
    - "workflow coordination, reservations, leases, and recovery"
    - "Git branches, worktrees, commits, pushes, draft PRs, and integration lifecycle"
    - "legacy Role Pool and R0-bound bytes, explicitly forbidden"
  authority_conflicts_found: false
  authority_conflict_notes: "The current issue, exact contract, accepted ADRs, and owner instruction align. Conditional G approval remains unconsumed."
  stop_conditions:
    - "blocking contract finding"
    - "legacy Role Pool or R0-bound byte change"
    - "staging, commit, push, PR update, installation, real Dispatch, G, merge, deployment, cleanup, or issue closure during E"
```
