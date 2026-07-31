# R0 Offline Observation Contract and Implementation Review

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/776

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Protected Coordination Surface

https://github.com/Tahjali11/Mythic-Edge/issues/769

## Contract

`docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md`

Reviewed SHA-256:
`df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8`

Reviewed metadata predecessor SHA-256:
`f05451e0b76c4d879748ab989c4d7eb374958c4e7adb96b069643e1feb16484e`

Original consumption-closure predecessor SHA-256:
`0a80cdcc1c3b0e5fe255c3f0fd25fd9183101e750619659af1af2b9256b2eeda`

## Implementation Under Test

Branch `codex/role-pool-r0-observation-contract-776` at
`origin/main@6a7ee5948dfd8a854d9a1d3f50981fc06a1f5216`:

- `tools/check_role_pool_r0_offline_observation.py`, SHA-256
  `7c049ab3e33e0ecb849155a2c31c0bb20974f334d635a86408dac69362ca6f3c`;
- `tests/test_check_role_pool_r0_offline_observation.py`, SHA-256
  `a44706410d8dd83acc90521a6d88f658a63f23c970e22cbe6ff8a30da7b8a746`.

No observation, consumption, receipt publication, release mutation, or rung
advancement was performed.

## Report Lifecycle

`report_lifecycle: final_approval`

## Contract Summary

The contract defines two predeclared Windows-hosted R0 offline observations.
Each identity must cross one irreversible, public-safe prelaunch consumption
boundary before its sole launch. Exact consumption readback is the only
nonterminal consumption outcome. All failed, absent, conflicting, unreadable,
or ambiguous outcomes are permanently nonreusable and require a separately
accepted successor rather than retry.

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
git diff --check
py -B -m pytest tests\test_check_role_pool_r0_offline_observation.py -q
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
py -B -m pytest tests\test_check_role_pool_r0_bootstrap.py -q
py -B -m pytest docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py -q -k release
py -B -m ruff check tools\check_role_pool_r0_offline_observation.py tests\test_check_role_pool_r0_offline_observation.py
py -B -m pytest -q
py -B tools\check_role_pool_r0_bootstrap.py
```

The protected-surface and secret scans were additionally run with the exact
untracked contract path supplied through `--paths-from-stdin`. Independent
in-memory checks strictly parsed all four canonical JSON blocks, recomputed
all self- and artifact digests, checked the 36-field consumption schema, and
enumerated the complete 15-tuple consumption selector. A direct, side-effect-
free handler probe supplied the documented `os.startfile` and `os.startfile/2`
audit event names to `AuditBoundary`.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed. Consumption and receipt bodies contain
  only contracted public references, digests, enums, counts, and false
  authority values.
- Vocabulary coherence: passed for the consumption and observation lifecycle.
- Authority semantics: passed. Contract review creates no implementation,
  observation, publication, release, R1, Stage-4, or readiness authority.
- Fail-closed schemas: passed for all four canonical JSON objects and the
  consumption selector.
- Handoff conformance: passed. The current `workflow_handoff` contains every
  repository-required high-risk field. Removing only the six corrected fields
  reproduces the previously reviewed contract exactly.
- Protected-surface rollout: passed. Both Windows-native `startfile` audit
  events are rejected and counted through the existing process boundary.

## Contract Review Results (Preserved)

The contract remains accepted. The implementation review below does not reopen
the fixed contract findings.

- Contract bytes: 54,180, UTF-8 without BOM, LF-only, one final LF.
- Contract SHA-256 is exact and stable at
  `df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8`.
- An independent inverse projection removed only `repository_url`,
  `target_artifact`, `base_branch`, `target_branch`, `validation`, and
  `stop_conditions`; the resulting 53,511 bytes reproduced predecessor
  SHA-256
  `f05451e0b76c4d879748ab989c4d7eb374958c4e7adb96b069643e1feb16484e`.
- Strict YAML parsing found no missing required `workflow_handoff` or
  `instruction_context` fields.
- The observation profile and two receipt vectors remained byte-exact.
- The 36-field consumption vector has a 2,526-byte preimage, 2,614-byte
  complete object, self-digest
  `6d0e6a9aeb895c75a43cc013cf895016570574e836fdca67a0ea2071bc441ab1`,
  and artifact SHA-256
  `5fdd20f34258315199dc15ab416e9243eb68190171f514ad2c037f1afde0b4f2`.
- The 15 consumption tuples produced counts `[2,1,5,4,3]` with overlap,
  uncovered, and unreachable counts `0/0/0`.
- Exact consumption readback is the sole route to launch. Every absent or
  ambiguous post-attempt state remains nonreusable, including for a fresh
  task.
- Issue #769 remained open with zero comments. Issues #776 and #746 remained
  open.
- The current R0 checker retained exact bindings, source/install equality,
  zero effects, all-false authority, and terminal
  `blocked_release_state_conflict`.
- R0 tests: 76 passed.
- Release-focused tests: 6 passed, 91 deselected.
- Agent-doc check: 54 files, 0 errors, 0 warnings.
- Exact-path protected and private-marker scans: forbidden 0, warnings 0.
- Task-specific extra generated residue count: 0.

## Implementation Review Results

Accepted. No blocking implementation finding remains.

- Exact implementation hashes match the Codex C handoff.
- Focused implementation tests: 73 passed.
- R0 checker tests: 76 passed.
- Release-focused tests: 6 passed, 91 deselected.
- Full repository tests: 2,264 passed, 4 platform skips, 1 dependency
  deprecation warning.
- Ruff, agent-doc, diff, exact-path protected-surface, and exact-path secret
  checks passed.
- The read-only production checker returned its expected
  `blocked_release_state_conflict` terminal with source/install equality, zero
  effects, and all authority false.
- Issue #769 is open with zero comments; #776 and tracker #746 remain open.
- Direct audit probes rejected `os.startfile` and `os.startfile/2`; each
  produced only `observation_safety_boundary_failed`, incremented process and
  total forbidden-attempt counts to one, and exposed no supplied argument.
- Matching harness process count and generated residue count are zero.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- |
| `ME-RP-776-E-001` | high | `fixed_state_followup` | `fixed_confirmed_preserved` | not_blocking | Canonical prelaunch consumption, irreversible POST boundary, exact readback, 15-tuple selector, terminal nonreuse, and fresh-task reconciliation remain byte-exact. | Owner decision |
| `ME-RP-776-E-002` | medium | `fixed_state_followup` | `fixed_confirmed` | not_blocking | The six previously missing handoff fields are present and valid; inverse projection reproduces the reviewed predecessor exactly, proving no semantic expansion. | none |
| `ME-RP-776-E-003` | high | `fixed_state_followup` | `fixed_confirmed` | not_blocking | Original evidence: both Windows audit events were absent and passed through with zero accounting. Current bytes include both in `_PROCESS_EVENTS`; independent probes and focused tests confirm symbolic rejection, one process-attempt count, and no argument echo. | F |

## Confirmed Contract Matches

- Durable prelaunch consumption is now defined before either harness launch.
- Exact readback alone permits the initiating task to launch once.
- Known failure, collision, ambiguous commit, invalid readback, timeout, and
  unavailable prior state never recreate authority.
- Observation 2 remains gated by exact observation-1 consumption and accepted
  receipt evidence.
- The existing two-file implementation scope, process boundary, canonical
  receipt identities, natural digest order, fixed bindings, and #769
  protection remain unchanged.
- The implementation exactly reproduces all four canonical contract objects,
  15 consumption tuples with counts `[2,1,5,4,3]`, natural receipt ordering,
  fixed owner bindings, and all-false receipt authority.
- Strict receipt and consumption parsing, sequence predecessor enforcement,
  fake transport reconciliation, lifecycle precedence, no-echo output, stable
  file reads, R0 projection, and zero-effect checks are covered and passing.
- All operational and readiness authority remains false.

## Contract Mismatches

None remain. `ME-RP-776-E-003` originally established that the process audit
boundary omitted the Windows-native `os.startfile` and `os.startfile/2` events
documented by
[Python](https://docs.python.org/3/library/os.html#os.startfile). The exact
reviewed implementation now includes both event names in `_PROCESS_EVENTS` and
preserves the existing single symbolic failure route.

## Missing Tests

None block submission. The focused process-boundary parametrization now covers
both `startfile` events and independently proves rejection, process-attempt
accounting, and no argument echo.

## Drift Notes

No binding, source/install, registry, release, authority-index, issue,
protected-issue, repository, or installed-state drift was observed. The
confirmed fix is limited to the two reviewed implementation paths. All four
intended artifacts remain untracked in this branch, so exact-path scans covered
their actual bytes in addition to the standard base-diff gates.

## Recommendation

Approve the exact reviewed contract, implementation, tests, and review report
for Codex F submission after an explicit owner submission and target-branch
decision. This approval grants no observation, consumption, publication,
release-state, R1, R0-R8, Stage-4, merge, deployment, or readiness authority.

## Next Workflow Action

Next role: Codex F after explicit owner submission authorization and target
selection.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex F: R0 Offline Observation Harness Submitter.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/776
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Protected coordination surface: https://github.com/Tahjali11/Mythic-Edge/issues/769
Branch: codex/role-pool-r0-observation-contract-776

Accepted contract:
docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md

Required SHA-256:
df6cce588e6d64ba5ba24b5d8d7f267c9c9a7e769c9a254527a9e7fd3d68e2b8

Exact reviewed implementation hashes:
- tools/check_role_pool_r0_offline_observation.py
  7c049ab3e33e0ecb849155a2c31c0bb20974f334d635a86408dac69362ca6f3c
- tests/test_check_role_pool_r0_offline_observation.py
  a44706410d8dd83acc90521a6d88f658a63f23c970e22cbe6ff8a30da7b8a746

Require the exact final Codex E report SHA-256 from the immediately preceding
handoff before proceeding. Stage only:
- docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md
- docs/contract_test_reports/role_pool_trusted_owner_r0_offline_observation_sequence.md
- tools/check_role_pool_r0_offline_observation.py
- tests/test_check_role_pool_r0_offline_observation.py

Do not use `git add -A`. Recompute all four artifact hashes, confirm no unrelated
change, rerun the focused tests and submission gates, then commit and push only
after the owner supplies an explicit submission decision and PR target. Open or
update a draft PR linked to #776 and tracker #746 only under that authority.

Do not invoke either observation, consume or publish authority or receipts,
comment on #769, mutate release state, install, dispatch, authorize R1, merge,
deploy, advance R0-R8 or Stage 4, or claim readiness. Route the draft PR to
Codex G for integration-readiness review; merge remains separately authorized.
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
    - "R0 release and observation authority"
    - "single-use prelaunch consumption and terminal nonreuse"
    - "canonical and installed Role Pool bytes"
    - "issue #769 zero-comment coordination boundary"
  authority_conflicts_found: false
  authority_conflict_notes: "Current instruction authorized independent E-003 confirmation and this report update only; submission and target selection remain separate."
  stop_conditions:
    - "binding or reviewed-contract drift"
    - "scope beyond the contract-permitted review report"
    - "need to edit implementation, execute an observation, publish, or mutate release state"
    - "any proposed comment on issue #769"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/role_pool_trusted_owner_r0_offline_observation_sequence.md"
  target_artifact: "docs/contract_test_reports/role_pool_trusted_owner_r0_offline_observation_sequence.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_owner_submission_decision"
  branch: "codex/role-pool-r0-observation-contract-776"
  finding_status:
    ME-RP-776-E-001: "fixed_confirmed_preserved"
    ME-RP-776-E-002: "fixed_confirmed"
    ME-RP-776-E-003: "fixed_confirmed"
  contract_verdict: "accepted_exact_r0_offline_observation_sequence_contract"
  implementation_verdict: "accepted_exact_two_file_r0_offline_observation_harness"
  owner_implementation_decision_eligible: true
  implementation_authorized: false
  submission_authorized: false
  merge_authorized: false
  observation_authorized: false
  consumption_authorized: false
  receipt_publication_authorized: false
  release_state_mutation_authorized: false
  r1_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  validation:
    - "implementation hashes exact; four canonical JSON vectors exact"
    - "15 consumption tuples; counts [2,1,5,4,3]; audit 0/0/0"
    - "73 focused, 76 R0, 6 release-focused, and 2264 repository tests passed"
    - "Ruff, agent-doc, diff, and exact-path safety scans passed"
    - "os.startfile and os.startfile/2 rejected, counted once, symbolic no-echo"
  stop_conditions:
    - "owner submission or target-branch decision is absent"
    - "staged scope exceeds the exact four reviewed artifacts"
    - "observation or operational authority is requested"
    - "issue #769 comment or release-state mutation"
  next_recommended_role: "Codex F after explicit owner submission and target-branch decision"
```
