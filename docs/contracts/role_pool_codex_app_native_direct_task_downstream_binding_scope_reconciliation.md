# Direct App-Native Downstream Test-Binding Scope Reconciliation

## Module And Authority

This is one additive, test-only successor for Mythic Edge issue
[#813](https://github.com/Tahjali11/Mythic-Edge/issues/813), tracker
[#746](https://github.com/Tahjali11/Mythic-Edge/issues/746), draft PR
[#815](https://github.com/Tahjali11/Mythic-Edge/pull/815), and protected issue
[#769](https://github.com/Tahjali11/Mythic-Edge/issues/769).

It is bound to branch `codex/role-pool-app-native-direct-task-contract-813`,
reviewed head `921e645e239660defb411796fd0b14fa7875e074`, and source contract:

- `docs/contracts/role_pool_codex_app_native_direct_task_downstream_binding_transition.md`
- SHA-256
  `a4cf1c7eefbe723486c195ee444b0e503578b1e2c7253e79c4298471eba5b809`
- Immediate predecessor revision SHA-256
  `b1f0f0eaa5d1360983022d46db7a74ccc5febabfde841a72fb48eeaf9369c743`

Required governance sources are
[`docs/agent_constitution.md`](../agent_constitution.md),
[`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md),
and [`docs/templates/module_contract.md`](../templates/module_contract.md).
The current owner instruction authorizes only this Codex B contract. It
transfers no implementation, review, submission, or operational authority.

## Finding And Decision

Observed baseline:

- the exact four-file Codex C implementation is complete and its focused
  validation passes;
- the completed two-test fixture implementation passes `80` bootstrap tests,
  `74` launch-observer tests, and `154` combined tests;
- the restored-state aggregate gate reports `1 failed, 2884 passed, 4 skipped`;
- isolated execution of `tests/test_check_role_pool_r0_offline_observation.py`
  reports `186 passed, 1 failed`; and
- Codex D attempted the one contracted literal change, found one direct
  downstream digest consumer in the launch-observer test, stopped, reverted
  the attempted change, and restored the exact starting state with zero
  generated residue.

The first substitution changes the offline-observation test artifact from
`5a898d078ea6ee50c5090010866cbcd1b5f727503c08e2216d9d503ea99beb49`
to
`d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6`.
The launch-observer test directly names the former artifact as its current
successor owner-test digest, so one second same-length substitution is
mechanically required. Exact digest and path searches found no third
current-successor consumer.

Decision: preserve the completed implementation and authorize only the two
closed digest-literal substitutions defined below. No production, fixture,
schema, KAT, lifecycle, status, receipt, process, effect, authority, or
historical-evidence change is established or authorized.

## Truth Ownership

Internal project area: Quality / Governance.

Bridge-code status: `shared_support`.

The unchanged production owners retain truth:

- `tools/check_role_pool_r0_bootstrap.py` owns `FILE_BINDINGS`;
- `tools/run_role_pool_r0_trusted_launch_observer.py` owns
  `FROZEN_BINDINGS`; and
- completed fixture code owns only operation-free synthetic setup and
  assertions; and
- the two dependent tests named in this successor own only their exact
  current-successor comparison literals.

A fixture may admit a test to an unrelated branch. It cannot change
production truth, prove custody of historical bytes, or make current-successor
bytes valid under a historical owner.

## Exact Inputs

Completed Codex C starting bytes, which bind this successor:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | 56176 | `5b974517b6f56f7d9f35ca609ee936cf71846858a043e6bf5a31a7d2166856ea` |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py` | 214712 | `2ba40a598752dbb795e53e72d1c33e3b87d039c7ac8edfb08707018d80530df3` |
| `tests/test_check_role_pool_r0_offline_observation.py` | 65511 | `5a898d078ea6ee50c5090010866cbcd1b5f727503c08e2216d9d503ea99beb49` |
| `tests/test_run_role_pool_r0_direct_interpreter_preflight.py` | 76010 | `b92db370554244a6e67cb69551296a01992a6961582e979fe165258d6507c7f0` |

Production owners that must remain exact:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `tools/check_role_pool_r0_bootstrap.py` | 46642 | `954236dba7a39d3e6223fa114bc7190caf42ce853309870ed7c351ba12ae4289` |
| `tools/run_role_pool_r0_trusted_launch_observer.py` | 66397 | `ab46fdc687e2e1f1074cc202100869a8183bb95e8377eaac8c7f30061cdf098a` |

Completed two-test implementation starting bytes:

| Path | Predecessor SHA-256 | Current bytes | Current SHA-256 |
| --- | --- | ---: | --- |
| `tests/test_check_role_pool_r0_bootstrap.py` | `e79ef77bcd6248c8db7853313e63b50448f07f35177e40f49886a361546035c9` | 57389 | `880c4e5c7b4692bbb156e87225b0451eedcfe4702ec31f19b3618c4d7fe2498f` |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | `e504f417a9d47e24f095b7354facaf4ae6cad98fa129b01370bdee656bad4be1` | 41286 | `3a5521f9b9eee3982acaf32ca410ff84a6ee5931c2bd38c64f329ecfa6d34391` |

Exact two-literal successor:

| Path | Current bytes | Current SHA-256 | Prospective bytes | Prospective SHA-256 |
| --- | ---: | --- | ---: | --- |
| `tests/test_check_role_pool_r0_offline_observation.py` | 65511 | `5a898d078ea6ee50c5090010866cbcd1b5f727503c08e2216d9d503ea99beb49` | 65511 | `d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6` |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | 41286 | `3a5521f9b9eee3982acaf32ca410ff84a6ee5931c2bd38c64f329ecfa6d34391` | 41286 | `98e600ad2d5cb88f7a84b734486351120eac87a900d7ae3a18ac82edde41e1b4` |

Any drift stops implementation.

## Deterministic Consumer Closure

Exact digest searches and exact-path searches inspected the following direct
or potential deterministic consumers. Only rows marked `include` may change.

| Inspected consumer | Disposition | Reason |
| --- | --- | --- |
| `tests/test_check_role_pool_r0_offline_observation.py` | include | Its current-successor expectation directly names the changed bootstrap-test artifact. |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | include | Its `OWNER_TEST_SUCCESSOR_SHA256` directly names the offline-observation test artifact changed by the first substitution. |
| `tests/test_check_role_pool_r0_bootstrap.py` | exclude | Exact current input artifact; no byte in this successor changes. |
| `tools/check_role_pool_r0_bootstrap.py` | exclude | Production owner with frozen bindings; no changed current-successor literal is present. |
| `tools/check_role_pool_r0_offline_observation.py` | exclude | Lists its implementation paths but does not bind the changing test-artifact digest. |
| `tools/run_role_pool_r0_trusted_launch_observer.py` | exclude | Production owner remains bound to the historical owner-test artifact; that historical binding must not move. |
| `tools/run_role_pool_r0_direct_interpreter_preflight.py` | exclude | Deferred historical owner with a frozen harness-test binding; no current-successor literal is present. |
| `tools/check_role_pool_r0_prelaunch_gate_matrix.py` | exclude | Frozen historical matrix bindings remain evidence for their own accepted bytes, not the #813 successor. |
| `docs/contracts/role_pool_codex_app_native_direct_task_downstream_binding_transition.md` | exclude | Accepted source contract and immutable historical starting binding. |
| `docs/implementation_handoffs/role_pool_codex_app_native_direct_task_downstream_binding_fixer.md` | exclude | Historical implementation evidence, not an executable current-successor consumer. |
| Other matching accepted contracts and contract-test reports | exclude | Descriptive or immutable historical evidence; none contains either current-successor literal as a live expectation. |

The closed mechanical chain is:

```text
bootstrap test current SHA-256 880c4e5c...2498f
  -> one literal in the offline-observation test
  -> offline-observation test prospective SHA-256 d1952f5d...1df6
  -> one literal in the launch-observer test
  -> launch-observer test prospective SHA-256 98e600ad...e1b4
```

There is no schema identifier, fixture interface, KAT value, production
constant, or third artifact digest that changes as part of this chain.

## Closed Fixture Delta

Only these two pairs exist:

| Test owner | Dependency | Frozen predecessor SHA-256 | Current successor SHA-256 |
| --- | --- | --- | --- |
| bootstrap test | `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | `8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6` | `5b974517b6f56f7d9f35ca609ee936cf71846858a043e6bf5a31a7d2166856ea` |
| launch-observer test | `tests/test_check_role_pool_r0_offline_observation.py` | `79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784` | `5a898d078ea6ee50c5090010866cbcd1b5f727503c08e2216d9d503ea99beb49` |

The completed fixture implementation was constrained to one local helper,
context manager, or fake adapter in each named fixture test. It must continue
to:

1. operate only in memory or a test-owned temporary root;
2. accept only its named dependency and predecessor digest;
3. use any synthetic marker as a fixed test value distinct from real
   predecessor and successor bytes;
4. map only that marker to the predecessor digest and delegate all other
   payloads to real SHA-256;
5. never map or label real current-successor bytes as predecessor bytes;
6. never patch production constants, source, schemas, KATs, selectors, or
   status values;
7. restore all patched state and temporary objects on every exit; and
8. create no fixture file, helper module, snapshot, receipt, or digest family.

No wildcard, caller-selected mapping, generic hash substitution, third pair,
or further fixture edit is permitted by this successor.

## Preserved Completed Assertions

The completed bootstrap test must continue to:

- use its bounded fixture for existing synthetic branch tests;
- prove the frozen `stage3_validator` digest remains exact;
- prove the real current digest equals the bound successor and differs from
  the predecessor;
- require unpatched `_binding_status` to return `known_invalid`; and
- require unpatched `_evaluate_for_tests` to fail closed before owner loading.

The completed launch-observer test must continue to:

- use its bounded fixture for verified-owner execution tests;
- prove the production `FROZEN_BINDINGS` digest remains exact;
- prove the real current digest equals the bound successor and differs from
  the predecessor;
- require unpatched `_load_owner_api` to return
  `observation_binding_rejected`; and
- prove rejection occurs before any launch or operational adapter call.

No synthetic result may be represented as historical or current R0 evidence.

## Exact Dependent Assertion Corrections

The later implementation may perform exactly these two same-length,
one-occurrence substitutions, in this order:

| Ordinal | Path | Old literal | New literal |
| ---: | --- | --- | --- |
| 1 | `tests/test_check_role_pool_r0_offline_observation.py` | `e79ef77bcd6248c8db7853313e63b50448f07f35177e40f49886a361546035c9` | `880c4e5c7b4692bbb156e87225b0451eedcfe4702ec31f19b3618c4d7fe2498f` |
| 2 | `tests/test_run_role_pool_r0_trusted_launch_observer.py` | `5a898d078ea6ee50c5090010866cbcd1b5f727503c08e2216d9d503ea99beb49` | `d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6` |

Substitution 1 changes only the current-successor expectation for
`tests/test_check_role_pool_r0_bootstrap.py`. Substitution 2 changes only
`OWNER_TEST_SUCCESSOR_SHA256`, keeping it synchronized with the exact artifact
produced by substitution 1. Each old literal must occur exactly once and each
new literal zero times before editing. Each new literal must occur exactly once
and each old literal zero times afterward.

The frozen historical constants, including
`observation.R0_CHECKER_TEST_SHA256`, its predecessor expectation
`976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34`,
and the launch observer's predecessor owner-test digest
`79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784`,
remain unchanged. These are assertion updates, not owner rebinding or
historical-evidence reinterpretation.

## Exact Future Implementation Scope

After fresh Codex E acceptance and a separate exact owner implementation
decision, Codex C may modify exactly:

1. `tests/test_check_role_pool_r0_offline_observation.py`
2. `tests/test_run_role_pool_r0_trusted_launch_observer.py`

No production file, accepted source contract, report, handoff, helper,
configuration, fixture file, or third implementation path may change. The
completed fixture logic in both included tests must remain byte-for-byte
unchanged outside the two exact literal spans. Stop if any other byte or path
must change.

## Preserved Invariants And Nonclaims

The source contract remains controlling for every invariant outside the
completed fixture delta and two-literal correction. In particular, preserve
unchanged:

- both production owners and all frozen constants;
- the exact completed implementation except for the two authorized dependent
  assertion substitutions;
- Stage-3 snapshots and manifest algorithms;
- all schemas, field order, statuses, selectors, lifecycles, KATs, receipts,
  identities, and digest families;
- historical observation, preflight, sequence, consumption, and release
  meaning;
- no-echo, privacy, process, effect, cleanup, and fail-closed behavior;
- every false authority field; and
- issue #769.

Historical evidence is not successor evidence. Passing synthetic tests grants
no installation, synchronization, task, observation, receipt, release,
R0-R8, Stage-4, submission, merge, deployment, assurance, or readiness claim.

## Stop Behavior

Stop without widening scope if:

- a bound hash drifts;
- either failure has a different first cause;
- a production constant or current-successor rejection must change;
- a generic hash override or current-to-predecessor mapping is required;
- a durable fixture or third implementation path is required;
- either old literal has a count other than one before editing;
- either prospective file hash differs from its exact bound value;
- any byte outside the two exact literal spans must change; or
- any schema, KAT, lifecycle, status, authority, process, effect, or receipt
  change is required.

An unrelated aggregate failure remains a separate finding. It is not absorbed
into this successor.

## Bounded Repair Budget

The repair budget is inert until this successor is independently accepted and
the owner grants exact implementation authority. It then permits at most three
bounded correction cycles inside the two-file, two-literal behavior envelope.
A cycle is one concrete implementation, test, validation, or independent
review finding followed by one bounded repair and its required validation.

Every cycle must use the standard implementation or review handoff and record:

- `repair_cycle`;
- `failing_command_or_review_finding`;
- `first_failing_boundary`;
- `affected_paths`;
- `classification`;
- `repair_applied`;
- `validation_result`;
- `residue_status`;
- `remaining_risk`; and
- `next_routing_decision`.

The budget creates no lifecycle, evidence artifact, operational authority, or
permission to change additional files. It authorizes no production change,
weakened test, skipped safety gate, observation, receipt, or execution. Stop
when validation passes, when any mandatory stop condition occurs, or after the
third unsuccessful cycle. A required third path or semantic change returns to
Codex B; a framing or authority error returns to Codex A or the owner.

## Required Validation

The later implementation must run operation-free:

```text
py -B -m pytest tests/test_check_role_pool_r0_offline_observation.py -q -p no:cacheprovider
py -B -m pytest tests/test_check_role_pool_r0_bootstrap.py -q -p no:cacheprovider
py -B -m pytest tests/test_run_role_pool_r0_trusted_launch_observer.py -q -p no:cacheprovider
py -B -m pytest tests/test_check_role_pool_r0_bootstrap.py tests/test_check_role_pool_r0_offline_observation.py tests/test_run_role_pool_r0_trusted_launch_observer.py -q -p no:cacheprovider
py -B scripts/run_release_tests.py
py -B -m ruff check tests/test_check_role_pool_r0_offline_observation.py tests/test_run_role_pool_r0_trusted_launch_observer.py
py -B tools/check_agent_docs.py
git diff --check
```

Also verify exact changed paths, both pre-edit and post-edit occurrence counts,
all bound current and prospective hashes, same byte counts, unchanged fixture
logic, unchanged production and historical bindings, no real process or
external effect, and zero generated residue.

The expected delta is removal of only the `1` restored-state aggregate failure
without introducing a transient downstream failure.
The isolated offline-observation suite advances from `186 passed, 1 failed` to
`187 passed`; the bootstrap and launch-observer suites remain at `80` and `74`
passed respectively; and the unchanged aggregate test inventory is expected to
report `2885 passed, 4 skipped`. A different count or new regression must be
reported, not waived.

## Acceptance And Routing

Codex B changes only this contract. Contract acceptance makes only a separate
two-test-file, two-literal owner Codex C implementation decision eligible. An
in-scope concrete failure may route through Codex D using the remaining repair
budget, followed by fresh Codex E review. A passing implementation routes
directly to fresh Codex E review, then Codex F and Codex G through the normal
workflow.

Next role: Codex E, independent downstream test-binding scope reconciliation
contract reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent #813 Downstream Test-Binding Scope Reconciliation
Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/813
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Draft PR: https://github.com/Tahjali11/Mythic-Edge/pull/815
Branch: codex/role-pool-app-native-direct-task-contract-813
Reviewed head: 921e645e239660defb411796fd0b14fa7875e074

Review only
docs/contracts/role_pool_codex_app_native_direct_task_downstream_binding_scope_reconciliation.md
at the exact SHA-256 supplied by Codex B. Verify its source-contract binding,
predecessor revision SHA-256
b1f0f0eaa5d1360983022d46db7a74ccc5febabfde841a72fb48eeaf9369c743,
the exact restored starting files, both unchanged production owners, the
Codex D stop-and-revert handoff, and the focused `154 passed`, isolated `186
passed, 1 failed`, and restored aggregate `1 failed, 2884 passed, 4 skipped`
evidence.

Independently repeat the exact digest and path consumer search. Confirm the
closed implementation scope is exactly two same-length, one-occurrence literal
substitutions:

1. tests/test_check_role_pool_r0_offline_observation.py
   e79ef77bcd6248c8db7853313e63b50448f07f35177e40f49886a361546035c9
   -> 880c4e5c7b4692bbb156e87225b0451eedcfe4702ec31f19b3618c4d7fe2498f
   prospective SHA-256
   d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6

2. tests/test_run_role_pool_r0_trusted_launch_observer.py
   5a898d078ea6ee50c5090010866cbcd1b5f727503c08e2216d9d503ea99beb49
   -> d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6
   prospective SHA-256
   98e600ad2d5cb88f7a84b734486351120eac87a900d7ae3a18ac82edde41e1b4

Verify every inspected consumer has a justified include or exclude
disposition, no third mechanically affected current-successor consumer exists,
and no production, fixture logic, schema, KAT, lifecycle, status, receipt,
process, effect, historical meaning, or authority change is permitted. Verify
the three-cycle repair budget remains inert pending exact owner implementation
authority and cannot widen the accepted two-file behavior envelope.

Run contract-only docs, diff, protected-surface, private-marker, binding,
process, and residue checks. Do not implement, execute an observer, mutate
GitHub or issue #769, consume authority, submit, merge, install, synchronize,
advance R0-R8 or Stage 4, or claim readiness.

If accepted, make only a separate two-test-file, two-literal owner Codex C
implementation decision eligible. Return findings first and a compact
workflow_handoff.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read: ["ADR-0008"]
  protected_surfaces:
    - "historical R0 binding and evidence meaning"
    - "issue #769"
  authority_conflicts_found: false
  authority_conflict_notes: "Two direct current-successor assertions form one closed two-hop digest chain."
  stop_conditions:
    - "any path beyond the two named dependent tests is required"
    - "any byte beyond the two exact digest occurrences must change"
    - "any production constant or historical meaning must change"

workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  protected_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/769"
  pr: "https://github.com/Tahjali11/Mythic-Edge/pull/815"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_codex_app_native_direct_task_downstream_binding_scope_reconciliation.md"
  target_artifact: "docs/contract_test_reports/role_pool_codex_app_native_direct_task_downstream_binding_scope_reconciliation.md"
  risk_tier: "high"
  base_branch: "origin/main"
  branch: "codex/role-pool-app-native-direct-task-contract-813"
  reviewed_head: "921e645e239660defb411796fd0b14fa7875e074"
  predecessor_contract_sha256: "b1f0f0eaa5d1360983022d46db7a74ccc5febabfde841a72fb48eeaf9369c743"
  scope_delta: "two tests; two same-length digest substitutions; zero production paths"
  baseline: "focused 154 passed; isolated 186 passed and 1 failed; restored aggregate 1 failed, 2884 passed, 4 skipped"
  repair_cycle_limit: 3
  repair_budget_status: "inert_pending_contract_acceptance_and_exact_owner_implementation_authority"
  implementation_authorized: false
  observation_authorized: false
  receipt_publication_authorized: false
  release_mutation_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  submission_authorized: false
  merge_authorized: false
  live_ready: false
  stop_conditions:
    - "any third implementation path or production change is required"
    - "any change beyond the two exact digest occurrences is required"
  next_recommended_role: "Codex E: independent downstream test-binding scope reconciliation contract reviewer"
```
