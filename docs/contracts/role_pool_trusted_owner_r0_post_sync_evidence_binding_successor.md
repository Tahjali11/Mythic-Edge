# Role Pool R0 Post-Sync Evidence Binding Successor Contract

Status: `review_pending`

Risk tier: `high`

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/766

Completed predecessor: https://github.com/Tahjali11/Mythic-Edge/issues/761

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746

Base: `origin/main@1e36cb728dd84389569f1c9093f0909bfed7381a`

Parent R0 contract:
`docs/contracts/role_pool_trusted_owner_r0_offline_bootstrap_validation.md`

Parent R0 contract SHA-256:
`9793951fa1a5a2e6ca7d1bb6325e89e9c2ca185aa4609b19481891405ef32a03`

Amended profile:
`docs/contracts/trusted_owner_native_role_pool_profile.md`

Amended profile SHA-256:
`944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f`

## Finding And Scope

`ME-RP-766-B-001` is fixed at contract level by this successor. The accepted
#761 checker pins predecessor profile and installer hashes. Changing the
profile and later installer without updating those pins makes
`contract_binding_status=known_invalid`; production also rejects an unexpected
installer before it can emit a packet.

This contract supersedes only the parent contract's current binding custody,
two-file implementation envelope, and pre/post-sync expected observations.
Every unmentioned parent clause remains controlling and unchanged.

The following are preserved exactly:

- schema `trusted_owner_r0_offline_bootstrap_evidence.v1`;
- operation `evaluate_r0_bootstrap_eligibility_read_only`;
- all 37 packet fields, field order, types, canonical bytes, and self-digest;
- every component vocabulary and the nine terminal statuses in their existing
  first-failure order;
- fixed issue #761 packet lineage and base-commit semantics;
- absent-registry and `absent_bootstrap_candidate` release-state semantics;
- no-echo, root derivation, owner-validator, and unknown-outcome rules;
- all five zero effect counts and all 16 false authority fields; and
- no R0 acceptance, installation, dispatch, canary, Stage 4, or readiness
  claim.

No public schema, result path, receipt, status, digest family, lifecycle, or
authority field is added.

## Exact Predecessor Bindings

| Binding | Exact predecessor value |
| --- | --- |
| Profile | `4a0ba9efe5c987735c09df66f94f42924a92a40ca68fd15a84ffb2c41842c94d` |
| Installer | `7954d1c6b4cd816b4fb9d09be68a42ea89df9f6ffff20e13b76bab97e965dbda` |
| Installer test | `04bf917eef2b6a63a53a2ec600c9ceb7cc6f610e715d4a78045bc1dc353ab7e9` |
| Checker | `57e7a4b22903d7e9e72ed5dd83b7542db212ef231f1fe2e0be8a050e0bccfde0` |
| Checker test | `fd1f93d76c124944733559f125d9ee5cfdc3f8529b008904ea950967331bcdb4` |
| Source tree | 41 nodes; 36 files; 6,495 canonical bytes; `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Installed tree | 39 nodes; 34 files; 6,159 canonical bytes; `ab56582b39474db9e2cb50f83e7e05a341376efa7c9a10f0b1ec306c94d2009e` |
| Current evidence | `ba7b47f6e9d2984ff726c379dde66a31a45c61e55f01b4c444883cbdc625cd2a` |
| Current terminal | `blocked_skill_source_drift` |

The current evidence also records `registry_status=absent`,
`release_state_status=absent_bootstrap_candidate`, zero effects, and zero true
authority fields.

## Successor Binding Rule

After this contract and the amended profile receive one independent Codex E
acceptance, a separately authorized Codex C implementation must finalize files
in this order:

1. implement and test only the profile-defined `--offline-r0-sync` mode;
2. freeze and hash the resulting installer;
3. update the checker to bind exactly:
   - amended profile SHA-256
     `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f`;
   - this exact successor artifact SHA-256 from the accepted B/E handoff; and
   - the frozen installer SHA-256 from step 2;
4. preserve every other `FILE_BINDINGS` row and packet constant;
5. update focused tests only for the successor bindings and required
   pre-sync/post-sync projections; and
6. freeze and report all four implementation hashes and the derived validator
   bundle digest for independent E reproduction.

The checker must use the successor artifact digest as
`R0_CONTRACT_SHA256`. `PROFILE_CONTRACT_SHA256` and the profile
`FILE_BINDINGS` row must use the amended profile digest. The installer
`FILE_BINDINGS` row must use the final reviewed installer digest. No caller,
environment value, runtime packet, or mutable file may supply these constants.

The exact final installer, checker, checker-test, and validator-bundle hashes
are intentionally unknown until C freezes the bytes. They become current only
after independent E review; they cannot be inferred or self-accepted.

During B/E contract review, the unchanged predecessor checker deterministically
reports an invalid profile binding because the amended profile bytes are
already present. That transitional rejection is expected and grants no
authority. Only the accepted four-file C/E result may establish the successor
bindings.

## Closed Four-File Implementation Scope

Codex C may modify exactly:

1. `tools/install_codex_skills.py`;
2. `tests/test_install_codex_skills.py`;
3. `tools/check_role_pool_r0_bootstrap.py`; and
4. `tests/test_check_role_pool_r0_bootstrap.py`.

The installer delta is limited to the profile-defined offline existing-target
operation. The checker delta is limited to the three binding updates above.
Checker-test changes may bind the successor and prove the two required
projections; they may not alter schema, precedence, owner behavior, no-echo,
effect, authority, or release semantics.

No Role Pool source, manifest, registry, release state, accepted contract,
App Server adapter, installed copy, workflow input, or other implementation
path may change. If another path is required, C stops and routes to B.

## Required Observations

Before installed mutation, the successor checker must produce:

- `contract_binding_status=exact`;
- `manifest_status=exact`;
- `source_install_status=installed_drift`;
- `registry_status=absent`;
- `release_state_status=absent_bootstrap_candidate`;
- `validator_bundle_status=exact`;
- `offline_validation_status=passed`;
- `terminal_status=blocked_skill_source_drift`;
- zero effects; and
- all 16 authority fields false.

Synthetic post-sync fixtures must replace the installed observation with the
exact source observation and then produce:

- installed tree: 41 nodes, 36 files, 6,495 canonical bytes, SHA-256
  `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`;
- `source_install_status=identical`;
- `registry_status=absent`;
- `release_state_status=absent_bootstrap_candidate`;
- `terminal_status=blocked_registry_missing_or_invalid`;
- `eligible_for_independent_review=false`;
- zero effects; and
- all 16 authority fields false.

The production post-sync projection is not run during C implementation. It
requires later integration, one fresh owner mutation authority, exact
predecessor-tree revalidation, one completed sync, and fresh independent
review. A synthetic result cannot stand in for that observation.

## Validation And Routing

Codex C and Codex E must run:

```powershell
py -B -m pytest -q tests\test_install_codex_skills.py tests\test_check_role_pool_r0_bootstrap.py
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
git diff --check
```

Tests must cover exact and wrong binding values, missing/alternate target,
unsafe trees, concurrent drift, staging/replacement/rollback/cleanup failure,
no capability query, deterministic synthetic sync, both required checker
projections, all existing terminal-selector cases, canonical bytes, no-echo,
zero effects, and false authority.

Codex E must independently verify the exact four-file diff and hashes,
successor constants, validator bundle, unchanged source tree, focused tests,
current production pre-sync packet, and all protected boundaries. Acceptance
of these two contracts permits only a fresh owner implementation decision.
After C implementation and a second independent E acceptance, routing to Codex
F may be considered. Neither acceptance grants installation, sync, registry,
release, process, task, dispatch, canary, R0-R8, Stage 4, submission, merge,
deployment, readiness, or assurance authority.

## Current Authority

Current and terminal authority counts are `0`. Future implementation authority
is `0` pending independent E acceptance and a separate owner decision.
Installed-copy mutation always requires another later exact owner decision.
