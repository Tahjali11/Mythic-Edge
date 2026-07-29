# Contract Test Report: Trusted-Owner Native Role Pool Profile

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/744

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/746

## Contract

`docs/contracts/trusted_owner_native_role_pool_profile.md`

Reviewed SHA-256:
`eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc`

## Implementation Under Test

- Branch: `codex/trusted-owner-native-profile-contract-744`
- Starting commit: `0e58eacfe5f0530880c36adfc529c64f08525e79`
- Implementation handoff:
  `docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md`
- Canonical managed-tree manifest SHA-256:
  `f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7`

## Report Lifecycle

`report_lifecycle: final_implementation_confirmation`

## Contract Summary

The candidate must provide an inert, repository-owned trusted-owner native
Role Pool profile with closed packet schemas, exact repository and predecessor
identity, bounded path scopes, fail-closed result and release validation,
single-use scheduling semantics, a graduated release ladder, and a reviewed
installer synchronization path with staging, rollback, and final validation.
No installation, registry population, dispatch, canary, Stage 4, merge,
deployment, or live authority is created by this implementation.

## Internal Project Area Reviewed

`Quality / Governance`, matching `docs/internal_project_map.md`. The candidate
does not move parser truth, runtime truth, workbook truth, or deployment
authority.

## Bridge-Code Status Reviewed

The canonical skill tree and installer changes are inert bridge code between
the historical installed Role Pool and a future repository-owned source. The
installed skill remains unchanged and drifting, so native dispatch remains
blocked.

## Checks Run

```powershell
py -3.13 -B -m unittest discover -s docs\codex_skills\mythic-edge-role-pool\scripts -p test_check_pool_plan.py -v
py -3.13 -B -m pytest -q -p no:cacheprovider tests\test_install_codex_skills.py
py -3.13 -B -m pytest -q -p no:cacheprovider
py -3.13 -B -m ruff check src tests tools
py -3.13 -B -m ruff check docs\codex_skills\mythic-edge-role-pool\scripts\check_pool_plan.py docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py --select F,I
py -3.13 -B tools\check_agent_docs.py
py -3.13 -B "$env:CODEX_HOME\skills\.system\skill-creator\scripts\quick_validate.py" docs\codex_skills\mythic-edge-role-pool
py -3.13 -B scripts\run_release_tests.py
py -3.13 -B tools\install_codex_skills.py --check --skill mythic-edge-role-pool
py -3.13 -B tools\check_protected_surfaces.py --base 0e58eacfe5f0530880c36adfc529c64f08525e79 --paths-from-stdin
py -3.13 -B tools\check_secret_patterns.py --base 0e58eacfe5f0530880c36adfc529c64f08525e79 --paths-from-stdin
git diff --check
```

Additional bounded in-memory negative probes exercised the five findings below
and the direct predecessor cross-bindings added by Codex D. They did not edit
implementation or execute a live Role Pool operation.

## Governance Checks Reviewed

- Public-safe/no-echo behavior: passed for the candidate and review evidence.
- Vocabulary coherence: passed for the reviewed contract-bound vocabulary.
- Authority semantics: passed; all live, installation, dispatch, canary,
  Stage-4, merge, and deployment authority remains false.
- Fail-closed schemas: path, repository identity, result authority, wildcard,
  rollback, and exact Automatic predecessor ownership conditions pass.
- Protected-surface rollout: preserved as an inert implementation candidate.

## Results

`accepted`

The candidate inventory, hashes, canonical managed tree, ordinary validation,
installed offline gate, structural checks, and safety scans pass. All five
review findings are fixed-confirmed. The exact inert implementation candidate
is accepted; this creates no installation, dispatch, canary, Stage-4,
submission, merge, deployment, or live authority.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ME-RP-744-E-007 | P1 | fixed_state_followup | fixed_confirmed | not_blocking | A completed result with `validation.status=failed` and a file outside an empty lane mutation scope remained valid terminal release evidence. | Failed validation now returns `result.validation:completed_requires_passed_validation`; unauthorized output returns both scope errors; released evidence without the owning request fails closed. | none |
| ME-RP-744-E-008 | P1 | fixed_state_followup | fixed_confirmed | not_blocking | Lane issue repository identity was not compared with the registry entry canonical repository. | The original cross-repository issue case now returns `request:repository_identity_mismatch`. | none |
| ME-RP-744-E-009 | P1 | fixed_state_followup | fixed_confirmed | not_blocking | Automatic predecessor digests were checked only for shape, not against owning predecessor bytes. | The exact valid chain returns `[]`; all five canonically re-digested forgeries now fail closed with `predecessor_result_invalid`, `predecessor_claim_mismatch`, or `predecessor_release_mismatch`. Missing and duplicate claim evidence is also rejected. | none |
| ME-RP-744-E-010 | P1 | fixed_state_followup | fixed_confirmed | not_blocking | `relative_path` accepted bracket wildcard syntax. | `*`, `?`, `[ab]`, and `[!a]` forms all return false from the scalar validator. | none |
| ME-RP-744-E-011 | P1 | fixed_state_followup | fixed_confirmed | not_blocking | Synchronization proceeded when the original rollback snapshot was unavailable. | The focused test proves a null first snapshot returns false before `os.replace`, preserves the target bytes, and leaves no staging or backup residue. | none |

## Final Verification After Codex D

### Observed

- `validate_trusted_native_request` requires the predecessor request, claim
  events, claim observations, results, and release events for every
  non-bootstrap Automatic request.
- `_native_validate_automatic_predecessor` validates each result against the
  exact owning request and its exact confirmed-running claim observation.
- It cross-binds the release event to that observation, request, wave, complete
  lane set, result, handoff, worktree observation, and task receipt.
- The exact valid predecessor chain returns no errors.
- Canonically re-digested forgeries in result `request_sha256`, result
  `wave_id`, result `claim_observation_sha256`, result validation command plan,
  and release-event `wave_id` all return deterministic ownership errors.
- Missing claim events, missing claim observations, duplicate claim events,
  and duplicate claim observations all fail closed.

### Derived

`ME-RP-744-E-009` is fixed-confirmed. Self-consistent redigestion can no longer
substitute for ownership by the exact predecessor request and claim chain.
The correction uses the existing schemas and evidence route and does not widen
registry, dispatch, platform, installer, release-ladder, or live scope.

## Confirmed Contract Matches

- The contract SHA-256 is exact and stable.
- The implementation scope contains only the two tracked installer paths, the
  34-file canonical skill tree, the contract, and the implementation handoff.
- The canonical tree has 34 files, 1,976,865 bytes, a 4,921-byte manifest, and
  SHA-256
  `f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7`.
- The six authorized class-B files changed; the other 28 managed files remain
  exact, including all 25 class-S/class-X paths.
- The candidate remains inert. No registry, release state, install, sync,
  dispatch, claim, task, canary, Stage-4, merge, or deployment action occurred.
- The installed historical Role Pool gate passed 350 tests plus structural
  validation and retained `NOT LIVE-READY`.

## Original Contract Mismatches

The sections below preserve the initial review evidence. The Finding Lifecycle
Summary and follow-up section above are the current dispositions.

### ME-RP-744-E-007: Invalid effects can become accepted release evidence

`validate_trusted_native_result` verifies file-change shape and validation
command ordering, but does not require changed paths to remain within the
lane's `mutation_scope` or require every planned validation to pass when
`result=completed`. `validate_trusted_native_terminal_evidence` then accepts
that completed packet for a `released` event.

Expected: `accepted_wave_complete` requires all validation passed and all
effects within authority. Out-of-scope changes or failed validation must
select a failure outcome, never valid release evidence.

### ME-RP-744-E-008: Issue repository identity is not cross-bound

`validate_trusted_native_request` validates the issue URL shape but does not
bind its owner/repository components to the registry entry's
`canonical_name`.

Expected: an issue from another repository selects
`blocked_repository_identity_mismatch`.

### ME-RP-744-E-009: Predecessor ownership is not validated

The request validator accepts any well-formed
`predecessor_request_sha256` and `predecessor_packet_sha256`. It receives no
owning predecessor request, accepted result, or released handoff evidence from
which to prove immediate lineage.

Expected: an Automatic successor must bind the immediately preceding released
request and accepted result in the same series; arbitrary, missing, stale, or
extra predecessor context selects `blocked_predecessor_packet_invalid`.

### ME-RP-744-E-010: Bracket wildcards pass `relative_path`

`_native_is_relative_path` rejects only `*` and `?`. Bracket expressions such
as `src/[ab].py` remain valid in registry read/mutation scopes, lane scopes,
working directories, artifacts, changes, and handoff paths.

Expected: every wildcard form is rejected before scope comparison.

### ME-RP-744-E-011: Sync lacks a proven rollback precondition

`_synchronize_existing_skill` captures `original_snapshot` but does not stop
when it is `None`. It can replace the installed target and delete the backup
without ever proving a readable rollback snapshot.

Expected: inability to capture the exact original tree blocks synchronization
before staging or target mutation.

## Regression Coverage

- Completed results require every planned validation to pass.
- Result paths must remain inside lane mutation scope and expected outputs.
- Lane issue repository identity must match the registry canonical name.
- Automatic successors reject unowned, stale, missing, duplicate, extra, and
  cross-series predecessor evidence.
- All supported wildcard forms are rejected from every `relative_path`
  surface.
- Synchronization refuses mutation when the original rollback snapshot is
  unavailable.

## Drift Notes

No repository, issue, tracker, or deployment drift caused these findings. The
installed tree's expected drift remains a deliberate non-dispatch state. One
secret scanner lexical hit exists only in a byte-preserved historical
class-X contract vocabulary; the other 38 reviewed paths passed with zero
forbidden markers and zero warnings.

An exploratory whole-canonical-scripts Ruff `F,I` scan, broader than the
contracted changed-file scope, reports 20 pre-existing findings in untouched
migration files. Core Ruff and the exact changed
`check_pool_plan.py`/`test_check_pool_plan.py` `F,I` scope pass. The broader
baseline findings are not introduced by this fix and are nonblocking here.

The Codex D handoff records the read-only installer drift exit as `1`. The
independent command returns the implementation's contracted
`target_differs`/`drift` exit `3`. This is a nonblocking handoff transcription
error; no synchronization occurred.

## Recommendation

Accept the exact inert trusted-owner native Role Pool implementation candidate.
Per the owner's current Windows-first directive on issue #744, route one
bounded Codex B amendment before any live activation decision. The amendment
must define Windows as the initial supported dispatch host while preserving the
accepted adapter, scheduler, isolation, receipt, and release guarantees.

## Next Workflow Action

Next role: Codex B, bounded Windows-first trusted-owner native profile contract
amendment writer. No authority transfers from this review.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/744"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "E"
  next_thread: "B"
  source_artifact: "docs/implementation_handoffs/trusted_owner_native_role_pool_profile_comparison.md"
  target_artifact: "docs/contract_test_reports/trusted_owner_native_role_pool_profile.md"
  risk_tier: "high"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/trusted-owner-native-profile-contract-744"
  contract_sha256: "eb3742f433f345dfc8508847825b24e84d9c27bd3be0b88057d34e932e3255fc"
  canonical_manifest_sha256: "f56f590bfa2a5b90087ca51636fc26cff8325681fc580cc71fce7208d47cd5f7"
  implementation_verdict: "accepted_exact_inert_trusted_owner_native_profile_candidate"
  validation:
    - "direct predecessor probes: valid chain accepted; five redigested forgeries rejected"
    - "canonical focused Role Pool: 87 passed"
    - "installer: 14 passed; 3 skipped"
    - "full repository: 2086 passed; 4 skipped"
    - "installed offline gate: 350 passed; structural validation passed"
    - "Ruff, agent docs, structural, protected-surface, process, residue, and diff checks passed"
  finding_status:
    ME-RP-744-E-007: "fixed_confirmed"
    ME-RP-744-E-008: "fixed_confirmed"
    ME-RP-744-E-009: "fixed_confirmed"
    ME-RP-744-E-010: "fixed_confirmed"
    ME-RP-744-E-011: "fixed_confirmed"
  owner_windows_first_amendment_required: true
  installation_or_sync_performed: false
  dispatch_performed: false
  canary_performed: false
  submission_authorized: false
  stage4_authorized: false
  live_ready: false
  generated_residue_count: 0
  stop_conditions:
    - "No live activation before the owner-directed Windows-first amendment is independently accepted."
    - "No install, sync, dispatch, canary, Stage 4, merge, deployment, or live authority."
```
