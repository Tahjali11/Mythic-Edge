# Direct App-Native R0 Adapter-Hash Rebinding Fixer Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/813>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/746>

## Contract

- `docs/contracts/trusted_owner_native_role_pool_profile.md`
- `docs/contracts/role_pool_codex_app_native_direct_task_adapter.md`

## Source Finding

The owner supplied a fresh Codex E workflow handoff with verdict
`accepted_exact_direct_app_native_fix`. It confirmed
`ME-RP-813-E-003` and `ME-RP-813-E-004` fixed, then reported the R0 bootstrap
result as `55 passed; 23 failed from one frozen adapter-hash binding` and
classified it as
`mechanical_successor_drift_not_reviewed_fix_regression`.

The previously persisted contract review is:
`docs/contract_test_reports/role_pool_codex_app_native_direct_task_adapter.md`.
The current owner-supplied E handoff is the direct source for this later
mechanical finding.

## Internal Project Area

Quality / Governance

## Truth Owner

The accepted issue #813 contracts and independently reviewed direct-adapter
bytes own the exact frozen binding. The read-only R0 checker only validates and
reports that binding.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer for the exact frozen direct-adapter SHA-256 mismatch.

## Intended Behavior

The R0 checker must accept the exact independently reviewed direct app-native
adapter bytes while continuing to fail closed on any later adapter drift.

## Actual Behavior

The checker and focused assertion still froze predecessor candidate digest
`104c02469ad800d9f0a4972e58da41b9381d9f7f12863f8a2e9c111bff3969de`.
The reviewed adapter bytes hash to
`fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98`.

The exact bootstrap suite reproduced `55 passed, 23 failed`. Every failure
reached the same first bad gate in `_evaluate_roots`: the
`direct_fake_transport` value in `FILE_BINDINGS` did not equal the observed
adapter digest, so the checker raised `PacketUnavailableError` before loading
the owner modules.

## Exact Fix

Rebound only the `direct_fake_transport` SHA-256 literal in the checker and
the matching focused expected value. No function, branch, schema, selector,
status, release rule, source/install rule, effect field, or authority field
changed.

## Files Changed

- `tools/check_role_pool_r0_bootstrap.py`
- `tests/test_check_role_pool_r0_bootstrap.py`
- `docs/implementation_handoffs/role_pool_codex_app_native_direct_task_adapter_hash_rebinding_fixer.md`

## Code Changed

Yes. One frozen SHA-256 literal changed in `FILE_BINDINGS` for
`direct_fake_transport`. The checker remains read-only and operation-free.

## Tests Added Or Updated

The existing exact-binding assertion was updated first to the reviewed digest.
It failed against the still-stale checker, proving the regression test was
sensitive to the mismatch. After the checker edit, that assertion and the
complete R0 bootstrap suite passed.

## Interface Changes

None. No public schema, function signature, CLI argument, status vocabulary,
receipt, release record, environment variable, file path, task operation, or
authority interface changed.

## Contracted Area Status

The fix stayed inside the companion contract's frozen checker/test rebinding
boundary. The reviewed adapter, planner integration, profile, companion
contract, report, registry, release state, canonical installed skill, and all
other product or workflow surfaces were untouched by this D repair.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: preserved.
- Vocabulary and example coherence: unchanged.
- Authority/readiness semantics: unchanged; validation creates no task,
  observation, installation, release, submission, merge, or readiness
  authority.
- Fail-closed schema or validator checks: preserved; only the exact accepted
  adapter digest changed.
- Protected-surface rollout phase: remains R0 operation-free validation only.

## Validation Run

```text
Pre-fix reproduction:
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py -p no:cacheprovider
55 passed, 23 failed

Regression-first proof after test edit and before checker edit:
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py::test_successor_contract_and_profile_bindings_are_exact -p no:cacheprovider
1 failed on checker digest 104c... versus expected fae7...

Post-fix exact-binding assertion:
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py::test_successor_contract_and_profile_bindings_are_exact -p no:cacheprovider
1 passed

Post-fix R0 bootstrap suite:
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py -p no:cacheprovider
78 passed

Reviewed direct-adapter and planner suites:
py -B -m pytest -q docs\codex_skills\mythic-edge-role-pool\scripts\test_trusted_native_app_direct_task_adapter.py docs\codex_skills\mythic-edge-role-pool\scripts\test_check_pool_plan.py -p no:cacheprovider
129 passed

git diff --check
passed

py -B tools\check_agent_docs.py
55 files; 0 errors; 0 warnings

Path-fed protected-surface gate
3 paths; forbidden 0; warnings 0

Path-fed secret/private-marker gate
3 paths; forbidden 0; warnings 0

Path-fed validation selector
5 required, 1 recommended, 1 advisory; warnings 0

Read-only production R0 checker
contract_binding_status=exact
validator_bundle_status=exact
offline_validation_status=passed
terminal_status=blocked_manifest_invalid
all observed effect counts=0
all authority flags=false

py -B -m ruff check --no-cache tools\check_role_pool_r0_bootstrap.py tests\test_check_role_pool_r0_bootstrap.py
not run: the only installed Python 3.13 environment has no Ruff module

Generated-residue audit
one ignored .ruff_cache directory; zero .pyc files; preserved without cleanup
```

## Still Unverified

- Fresh independent Codex E review of this exact two-literal D delta remains
  required.
- No real Codex task operation, observation, registry write, release append,
  installation, synchronization, GitHub write, R0-R8 advancement, Stage 4
  action, submission, merge, or deployment was run or authorized.
- Installed-tree safety, manifest-transition integration, release rebaseline,
  and later R2 capability evidence remain separate gates.
- Ruff remains unverified because the current environment lacks the module;
  this is missing tool setup, not a test or checker regression.

## Reviewer Focus

Verify that the adapter bytes independently hash to
`fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98`,
that exactly the checker and focused assertion use that value, and that no
other behavior changed. Reconfirm `ME-RP-813-E-003` and
`ME-RP-813-E-004` remain fixed in the reviewed six-path candidate and treat
manifest, installed-tree, release, and R2 gates as separate.

## Next Workflow Action

Next role: Codex E, fresh independent direct app-native fix reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Direct App-Native R0 Hash-Rebinding Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/813
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Branch: codex/role-pool-app-native-direct-task-contract-813
Base: origin/main@c24f1edf0a09a98439bdbd92ccf4e13155a3dd87
Contracts:
- docs/contracts/trusted_owner_native_role_pool_profile.md
- docs/contracts/role_pool_codex_app_native_direct_task_adapter.md
Source review:
- docs/contract_test_reports/role_pool_codex_app_native_direct_task_adapter.md
Fixer handoff:
- docs/implementation_handoffs/role_pool_codex_app_native_direct_task_adapter_hash_rebinding_fixer.md

Review the complete existing issue #813 candidate, but treat the new Codex D
delta as exactly one frozen direct-adapter digest replacement in
tools/check_role_pool_r0_bootstrap.py and the matching expected value in
tests/test_check_role_pool_r0_bootstrap.py. Independently hash
docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_direct_task_adapter.py
and require
fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98.

Reconfirm ME-RP-813-E-003 and ME-RP-813-E-004 remain fixed, the 129-test
direct/planner suite passes, the R0 bootstrap suite now passes all 78 tests,
and checker schemas, selectors, release semantics, source/install behavior,
effects, and authority flags are unchanged. Treat manifest transition,
installed-tree safety, release rebaseline, and R2 capability evidence as
separate gates.

Do not implement, invoke a real task operation, mutate registry/release/
installed/GitHub state, advance R0-R8 or Stage 4, submit, merge, deploy, or
claim readiness. Findings lead; route a concrete regression to D and an
ambiguity to B.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "D"
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
    - "docs/decisions/ADR-0012-long-horizon-context-and-delegation-discipline.md"
  protected_surfaces:
    - "Role Pool R0 validator binding"
    - "native task launch authority"
    - "registry and release capacity"
    - "installed Role Pool skill"
  authority_conflicts_found: false
  authority_conflict_notes: "The current owner instruction supplies exact Codex D authorization for the mechanical checker/test hash rebinding only."
  stop_conditions:
    - "need to change any value beyond the one checker/test digest pair"
    - "need to invoke a real task operation"
    - "need to mutate registry, release, installation, GitHub, or rung state"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "owner-supplied Codex E handoff reporting one frozen adapter-hash binding regression"
  target_artifact: "fresh independent review of the exact R0 hash rebinding"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "origin/main"
  branch: "codex/role-pool-app-native-direct-task-contract-813"
  internal_project_area: "Quality / Governance"
  truth_owner: "accepted issue #813 contracts and reviewed direct-adapter bytes"
  bridge_code_status: "shared_support"
  validation:
    - "regression-first exact-binding assertion failed before checker edit"
    - "post-fix exact-binding assertion: 1 passed"
    - "post-fix R0 bootstrap suite: 78 passed"
    - "direct-adapter and planner suites: 129 passed"
    - "git diff --check: passed"
    - "agent docs: 55 files, 0 errors, 0 warnings"
    - "path-fed protected and secret gates: 3 paths, forbidden 0, warnings 0"
    - "read-only R0 checker: exact bindings, offline validation passed, blocked_manifest_invalid, zero effects and authority"
    - "Ruff: unverified because the current Python environment lacks the module"
  stop_conditions:
    - "no real task operation or observation"
    - "no registry, release, installation, GitHub, rung, submission, merge, or deployment mutation"
    - "no readiness or assurance claim"
```
