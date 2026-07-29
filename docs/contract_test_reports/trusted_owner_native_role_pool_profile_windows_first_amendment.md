# Contract Test Report: Windows-First Trusted-Owner Native Role Pool Amendment

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/744

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Contract

`docs/contracts/trusted_owner_native_role_pool_profile.md`

Reviewed SHA-256:
`2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322`

Reviewed byte count: `94440`

Accepted predecessor SHA-256:
`eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc`

## Implementation Evidence Preserved

- Accepted Codex C handoff SHA-256:
  `c0bcbb87bdd21b897293fd6dfcd3ab0cc52445bd4edf1f73ddac69ae9dacf649`
- Terminal Codex E implementation report SHA-256:
  `7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8`
- Accepted managed-tree manifest SHA-256:
  `f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7`
- Branch:
  `codex/trusted-owner-native-profile-contract-744`

The accepted implementation evidence remains byte-identical. This report is a
separate artifact so the predecessor review receipt is not modified.

## Report Lifecycle

`report_lifecycle: contract_clarification_review`

## Contract Summary

The amendment narrows the initial native dispatch host to trusted Windows
runtime observations. Native macOS dispatch is deferred and nonblocking. A Mac
remotely controlling a process executing on Windows is Windows-hosted. An
unsupported or unobservable host, or a missing or incompatible exact
`codex:native-task-create/v1` primitive, selects the existing priority-1
`blocked_request_or_packet_invalid` outcome before any claim or persistent
effect. No weaker launcher, broker, shell, subprocess, repository executable,
receipt, or silent fallback is permitted.

Read-only or in-memory offline validation remains platform-neutral but cannot
supply installation, dispatch, canary, rung, Stage-4, or readiness authority.
The existing schemas, digest families, scheduling rules, 20 terminal outcomes,
external-isolation boundary, and graduated release ladder are preserved.

## Internal Project Area Reviewed

`Quality / Governance`

The amendment changes workflow enforcement requirements only. It does not move
parser, transport, stored-fact, analytics, AI, deployment, or credential truth
ownership.

## Bridge-Code Status Reviewed

The accepted repository-owned candidate remains inert bridge code. The
installed Role Pool remains intentionally different, so installation and
dispatch remain blocked pending later owner decisions and evidence.

## Checks Run

```powershell
py -3.13 -B -m unittest discover -s docs\codex_skills\mythic-edge-role-pool\scripts -p test_check_pool_plan.py -v
py -3.13 -B -m pytest -q -p no:cacheprovider tests\test_install_codex_skills.py
py -3.13 -B -m pytest -q -p no:cacheprovider
py -3.13 -B -m ruff check src tests tools
py -3.13 -B -m ruff check docs\codex_skills\mythic-edge-role-pool\scripts\check_pool_plan.py docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py --select F,I
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B "%USERPROFILE%\.codex\skills\.system\skill-creator\scripts\quick_validate.py" docs\codex_skills\mythic-edge-role-pool
py -3.13 -B scripts\run_release_tests.py
py -3.13 -B tools\install_codex_skills.py --check --skill mythic-edge-role-pool
git diff --check
```

The installed offline gate was run from
`%USERPROFILE%\.codex\skills\mythic-edge-role-pool`. Protected-surface
and private-marker scans were limited to the reviewed amendment path.

## Results

`accepted`

- Contract hash and byte count: exact and stable.
- Closed YAML objects: `3`, parsed with duplicate-key rejection.
- Terminal outcomes: `20`, with unique priorities `1` through `20`.
- Schema vocabulary: unchanged; no platform selector was added to caller data.
- Candidate focused contract tests: `87 passed`.
- Installer tests: `14 passed, 3 skipped` for unavailable directory symlinks.
- Full repository tests: `2086 passed, 4 skipped`; skips are the known
  unavailable Windows symlink cases.
- Installed offline Role Pool gate: `350 passed` plus structural validation.
- Ruff, agent-doc, skill-structure, diff, protected-surface, and private-marker
  checks: passed.
- Matching task process count: `0`.
- Generated residue count: `0`.
- Installer check: expected `target_differs` / `drift`; no installation or
  synchronization occurred.

## Finding Lifecycle Summary

No blocking or nonblocking implementation finding was opened.

## Confirmed Contract Matches

- Windows is the sole initial execution host for installation mutation, live
  validation, canaries, and R0-R8 advancement.
- Runtime-owned `os.name == "nt"` and `sys.platform == "win32"` observations
  determine host support; callers cannot supply platform identity.
- Remote control from macOS does not change the Windows execution host.
- Unsupported-host and missing-primitive failures occur before claim,
  worktree, task, command, installer staging, or another persistent effect.
- The exact native task adapter remains `codex:native-task-create/v1`.
- Platform failure cannot activate broker, `codex exec`, shell, subprocess,
  repository execution, weaker receipts, or another fallback.
- Project-wide claim ordering still covers independent registered Windows
  coordinators and distinct request IDs.
- Safe and Automatic transitions, F draft-PR-only behavior, unknown
  reconciliation without retry, external-isolation escalation, retained V5
  ownership, and the two-observation rung gate are preserved.
- Native Mac enablement requires a separate issue, accepted contract,
  independent review, owner decision, and its own evidence.
- ADR-0010 and ADR-0011 remain nonprecedential while Proposed.
- Security issues #116, #117, #118, #139, #140, and #141 remain separate.

## Prospective Codex C Scope

The owner's separate current instruction authorizes implementation only after
this successful independent review. That implementation is limited to:

1. `docs/codex_skills/mythic-edge-role-pool/SKILL.md`
2. `docs/codex_skills/mythic-edge-role-pool/references/pool-state-schema.md`
3. `docs/codex_skills/mythic-edge-role-pool/references/role-readiness-and-safety.md`
4. `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py`
5. `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py`
6. `docs/codex_skills/mythic-edge-role-pool/scripts/test_skill_contract.py`
7. `tools/install_codex_skills.py`
8. `tests/test_install_codex_skills.py`

Codex C must stop and route to Codex B if another path, schema, digest family,
terminal outcome, launcher, or operational capability is required.

## Remaining Inputs

Registry population, the scheduling surface, Windows native-task capability
evidence, installation targets, installation authority, dispatch authority,
canary authority, and rung advancement remain separate future decisions. They
do not block this inert implementation.

## Recommendation

Approve the exact Windows-first contract amendment and route the separately
authorized eight-path inert implementation to Codex C. Keep installation,
registry population, claim creation, task/worktree creation, dispatch,
canaries, rung advancement, Stage 4, submission, merge, deployment, and live
authority false.

## Next Workflow Action

Next role: Codex C, Windows-first trusted-owner native Role Pool amendment
implementer.

```yaml
workflow_handoff:
  role_performed: "Codex E: Independent Windows-First Trusted-Owner Native Role Pool Contract Amendment Reviewer"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/744"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  branch: "codex/trusted-owner-native-profile-contract-744"
  reviewed_artifact: "docs/contracts/trusted_owner_native_role_pool_profile.md"
  reviewed_sha256: "2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322"
  predecessor_sha256: "eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc"
  accepted_c_handoff_sha256: "c0bcbb87bdd21b897293fd6dfcd3ab0cc52445bd4edf1f73ddac69ae9dacf649"
  terminal_e_report_sha256: "7e90c7a308aad844f278b9f5609295f0fcc936bbf4592d0b3844c342c41c97a8"
  canonical_manifest_sha256: "f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7"
  finding_status: "no_findings"
  contract_verdict: "accepted_exact_windows_first_trusted_owner_native_role_pool_amendment"
  initial_dispatch_host: "windows"
  native_mac_dispatch: "deferred_nonblocking"
  unsupported_host_outcome: "blocked_request_or_packet_invalid_before_side_effects"
  terminal_outcome_count: 20
  schema_or_digest_family_added: false
  implementation_scope_path_count: 8
  owner_implementation_authorized: true
  implementation_authorized: true
  test_modification_authorized: true
  installation_authorized: false
  registry_population_authorized: false
  claim_creation_authorized: false
  task_or_worktree_creation_authorized: false
  dispatch_authorized: false
  canary_authorized: false
  rung_advancement_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  live_ready: false
  validation: "87 focused; 14 installer with 3 skipped; 2086 repository with 4 skipped; installed 350 plus structural validation; safety checks passed"
  generated_residue_count: 0
  next_recommended_role: "Codex C: exact eight-path Windows-first inert implementation"
```
