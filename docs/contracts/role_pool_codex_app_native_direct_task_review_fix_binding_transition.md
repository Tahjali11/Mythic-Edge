# Direct App-Native Review-Fix Successor Binding Transition

## Module And Authority

This is one additive, operation-free successor contract for Mythic Edge issue
[#813](https://github.com/Tahjali11/Mythic-Edge/issues/813), tracker
[#746](https://github.com/Tahjali11/Mythic-Edge/issues/746), pull request
[#815](https://github.com/Tahjali11/Mythic-Edge/pull/815), and protected issue
[#769](https://github.com/Tahjali11/Mythic-Edge/issues/769).

It is bound to branch `codex/role-pool-app-native-direct-task-contract-813`,
reviewed predecessor `7c71461a3f515c1b74904391afff693aea328abd`, and
`origin/main@c24f1edf0a09a98439bdbd92ccf4e13155a3dd87`.

Required governance sources are
[`docs/agent_constitution.md`](../agent_constitution.md),
[`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md),
and [`docs/templates/module_contract.md`](../templates/module_contract.md).
This Codex B task creates no implementation, submission, operational, or rung
authority.

## Source Evidence And Decision

The controlling accepted #813 behavior remains defined by:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/contracts/role_pool_codex_app_native_direct_task_adapter.md` | 50531 | `00267797596c2de27e1bfcf06444534f66464370c7e4f2b25ff4090d3f6938d4` |
| `docs/contracts/role_pool_codex_app_native_direct_task_downstream_binding_transition.md` | 23177 | `a4cf1c7eefbe723486c195ee444b0e503578b1e2c7253e79c4298471eba5b809` |
| `docs/contracts/role_pool_codex_app_native_direct_task_downstream_binding_scope_reconciliation.md` | 23007 | `89355b489613566ee30c6ae9b3882913a621ea32cc28c91afa873c75426d76bb` |
| `docs/implementation_handoffs/role_pool_codex_app_native_direct_task_pr_815_review_fixer.md` | 8958 | `3b1eb93d2f3108be6cd659c87ea5bf72a84306e57f2a3cf1939b3f716c9f67e3` |

The supplied independent Codex E handoff confirms the two concrete adapter
findings fixed, `131` focused tests passing, and no adapter repair required.
Its remaining finding is `ME-RP-813-E-007`:
`open_blocking_successor_binding_transition`. The remaining nine failures are
exact-byte successor-binding failures, not observed behavior regressions.

Decision: authorize a later implementation to update exactly eight
same-length lowercase SHA-256 literals in five existing files. No source path,
schema, fixture algorithm, KAT algorithm, lifecycle, authority, runtime
behavior, or historical evidence may change.

## Frozen Accepted Inputs

The independently reviewed current files below are immutable inputs to this
successor:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_direct_task_adapter.py` | 59095 | `a25394f3df664bfbde22851175fd8b747d0e48a33d4edfe7a6cf31747f81ff87` |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_trusted_native_app_direct_task_adapter.py` | 35368 | `6e781311f62fcd3d392cfe6c855f1bf4176f4b6ebf9ee864d7ccd20d6fff2b88` |
| `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py` | 477899 | `5e4a64391c14e0652fe30d333a1c9f2e33a048f67dd9fa08d08454d1f684e361` |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py` | 156038 | `a4b7a74925f16f12dc7c3b1de71a234bff832ea1aa645d884424466bad1fb93d` |
| `tools/check_role_pool_r0_bootstrap.py` | 46642 | `3b895032e576fcf9dafb3f0b4d99a558480c588237baa5ddca87b1e19a3045da` |
| `tests/test_check_role_pool_r0_bootstrap.py` | 57389 | `7593b426160f1b0c9c73586bcc692486c8e748d24cea1c43e312207a866faea2` |

The first three changed rows are accepted inputs to the Stage-3 transition.
The bootstrap tool and test are accepted inputs to the dependent current-tree
chain. A later implementation under this contract must not edit any row in
this table except the bootstrap test at the one exact span listed below.

## Exact Manifest And Tree Transition

The canonical Stage-3 manifest retains its existing algorithm, ordinal row
order, `38` Role Pool rows, and three frozen workflow rows. The frozen workflow
digests remain:

- `SKILL.md`:
  `04c229e2604ec965391d0044947d5a985049fc69508b79c88aec09e3732f14bb`;
- `agents/openai.yaml`:
  `0dc1f6b8acfac33f9f7a2628e093bc7fddbc2cb52a8bb41f9c22e56a57aa0c2f`;
- `scripts/accept_fallback_prompt.py`:
  `47aa25f3da14bfade71ed2862e4b7d85248c8356b1c90bdfd61222133b0a875d`.

The exact transition is:

| Projection | Rows | Canonical bytes | SHA-256 |
| --- | ---: | ---: | --- |
| accepted PR-head Stage-3 predecessor | 41 | 6052 | `5e60fedac417df668af1818c6026a960cd86ade28580ba4166223fe778843b85` |
| E-confirmed review-fix Stage-3 inputs | 41 | 6052 | `f8a8771b3849f29a8fce13146390bb7666d2deea99e73d660639b246abef2e5e` |
| final self-row successor | 41 | 6052 | `77f221e18d80cf7e63d6f946a74f411cd375d3cabfbb7fbba92dc48a995386c5` |

There are zero added, removed, renamed, reordered, duplicate, or case-varied
paths. Relative to the E-confirmed inputs, only the Stage-3 validator's own row
changes in the final manifest. The validator must not embed its prospective
file digest or the complete manifest digest; independent readback owns the
self-row check.

The repository-owned Role Pool install-tree projection retains `43` nodes,
`38` files, and `6840` canonical bytes:

| Projection | SHA-256 |
| --- | --- |
| accepted PR-head predecessor | `4025f00b8dd05fa674074ad1d12cbb0eba66fbc40819d9815592f285262b0759` |
| E-confirmed review-fix inputs | `933cb20bbe979e7b7307dc58fae7e8947a8e1c7be0a871d50011ec66bc9fac9d` |
| final successor | `d86a4f9811a0f9aa3152e4c9c48a79ef234afacc8e78f4a71b1323dd28539a4e` |

The accepted historical projection used by the direct-interpreter preflight
test is separately derived as `43` nodes, `38` files, `6840` bytes, SHA-256
`22d2ca28148196b221fd773559f8c1ab784b3ffac87e6746b00397c56571233d`.
That projection substitutes the reviewed historical Stage-3 validator and
test rows while retaining the accepted #813 successor inputs. It does not
relabel a historical observation or production preflight as current evidence.

## Closed Eight-Literal Delta

The later implementation may apply exactly these substitutions in ordinal
order. Every old literal must occur exactly once and its new literal zero times
before editing; the inverse must be true after editing.

| Ordinal | Path | Old literal | New literal |
| ---: | --- | --- | --- |
| 1 | `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | `fae7aa4aec168d02de0dbdd34ab6a181b9f545b85aba39110e8d741e8094dd98` | `a25394f3df664bfbde22851175fd8b747d0e48a33d4edfe7a6cf31747f81ff87` |
| 2 | same path | `48dee1083eb5f1a9b04af58e964946676b80d92c6f65d62f5137407897ab325e` | `6e781311f62fcd3d392cfe6c855f1bf4176f4b6ebf9ee864d7ccd20d6fff2b88` |
| 3 | same path | `8c9a0e3d063c601e000a5097a5dbeeac1dd6f0a33b5924f9df8186997bba935e` | `a4b7a74925f16f12dc7c3b1de71a234bff832ea1aa645d884424466bad1fb93d` |
| 4 | `tests/test_check_role_pool_r0_bootstrap.py` | `5b974517b6f56f7d9f35ca609ee936cf71846858a043e6bf5a31a7d2166856ea` | `9f37eac96dc321d9fad093dfad7cb91dbd121fd24ac496e79c7715e5063fcfd8` |
| 5 | `tests/test_check_role_pool_r0_offline_observation.py` | `954236dba7a39d3e6223fa114bc7190caf42ce853309870ed7c351ba12ae4289` | `3b895032e576fcf9dafb3f0b4d99a558480c588237baa5ddca87b1e19a3045da` |
| 6 | same path | `880c4e5c7b4692bbb156e87225b0451eedcfe4702ec31f19b3618c4d7fe2498f` | `86d183ca4f37432e879ea1a87b47926ef8e66b804014b0a5f2d6674371a2629b` |
| 7 | `tests/test_run_role_pool_r0_trusted_launch_observer.py` | `d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6` | `c43b57072c99c166a9e7f578f67ecffecb2ee53c28e67c3c040e66cf33deb86a` |
| 8 | `tests/test_run_role_pool_r0_direct_interpreter_preflight.py` | `f22d6557066a0449f3b7727621aa266bc3fda7ea5811965b30d964eebc4afc01` | `22d2ca28148196b221fd773559f8c1ab784b3ffac87e6746b00397c56571233d` |

The exact input and output artifacts are:

| Path | Input bytes | Input SHA-256 | Output bytes | Output SHA-256 |
| --- | ---: | --- | ---: | --- |
| `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py` | 56176 | `5b974517b6f56f7d9f35ca609ee936cf71846858a043e6bf5a31a7d2166856ea` | 56176 | `9f37eac96dc321d9fad093dfad7cb91dbd121fd24ac496e79c7715e5063fcfd8` |
| `tests/test_check_role_pool_r0_bootstrap.py` | 57389 | `7593b426160f1b0c9c73586bcc692486c8e748d24cea1c43e312207a866faea2` | 57389 | `86d183ca4f37432e879ea1a87b47926ef8e66b804014b0a5f2d6674371a2629b` |
| `tests/test_check_role_pool_r0_offline_observation.py` | 65511 | `d1952f5d4ca6d55f733f20e95b9d691767312fd3ed604439177d44531e171df6` | 65511 | `c43b57072c99c166a9e7f578f67ecffecb2ee53c28e67c3c040e66cf33deb86a` |
| `tests/test_run_role_pool_r0_trusted_launch_observer.py` | 41286 | `98e600ad2d5cb88f7a84b734486351120eac87a900d7ae3a18ac82edde41e1b4` | 41286 | `f0e5b6a05228a81571a901523e8418016b3ee52a699960ef4279e7d2f0f04910` |
| `tests/test_run_role_pool_r0_direct_interpreter_preflight.py` | 76010 | `b92db370554244a6e67cb69551296a01992a6961582e979fe165258d6507c7f0` | 76010 | `0e5c460f527e11f769c2b3aeb55c731d1881448d28453971573e77a74f9d72c3` |

No other byte change is permitted.

## Deterministic Consumer Closure

Exact path and digest searches establish this closed chain:

```text
three E-confirmed Role Pool rows
  -> Stage-3 manifest validator
  -> bootstrap current-successor assertion
  -> offline-observation current-successor assertions
  -> launch-observer current-successor assertion

accepted #813 successor projection
  -> direct-interpreter historical projection assertion
```

Included consumers are exactly the five files in the delta. The following
inspected candidates are excluded:

| Inspected consumer | Reason excluded |
| --- | --- |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_stage3_behavioral_planning.py` | It dynamically consumes validator constants and contains none of the eight changing literals. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_direct_task_adapter.py` | E-confirmed behavior input; no dependent literal changes. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_trusted_native_app_direct_task_adapter.py` | E-confirmed test input; no dependent literal changes. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py` | E-confirmed unchanged planner owner; no dependent literal changes. |
| `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py` | E-confirmed test input; its new digest is consumed, not edited. |
| `tools/check_role_pool_r0_bootstrap.py` | E-confirmed current owner; its new digest is consumed, not edited. |
| `tools/check_role_pool_r0_offline_observation.py` | Historical production owner; current-successor checks belong to its test. |
| `tools/run_role_pool_r0_trusted_launch_observer.py` | Historical production owner; current-successor checks belong to its test. |
| `tools/run_role_pool_r0_direct_interpreter_preflight.py` | Historical production owner; reviewed-tree projection belongs to its test. |
| `tools/check_role_pool_r0_prelaunch_gate_matrix.py` | Unchanged historical matrix owner with no changing literal. |
| Existing contracts, reports, and handoffs | Immutable lineage or descriptive evidence, not executable current-successor consumers. |

A sixth path, a ninth literal, or a required semantic change is an immediate
stop and returns to Codex B or the owner. It must not be absorbed as a repair.

## Preserved Behavior And Authority

This contract preserves unchanged:

- all accepted #813 adapter and planner behavior;
- every production owner and public interface;
- schemas, field order, status vocabularies, selectors, KAT algorithms,
  lifecycle rules, receipts, identities, and digest families;
- source/install, registry, claim, worktree, reconciliation, release, and
  R0-R8 controls;
- historical observations, receipts, consumption records, sequence IDs, and
  predecessor bindings as historical and nonreusable;
- no-echo, privacy, process, effect, cleanup, and fail-closed requirements;
- issue #769 and all protected surfaces; and
- every false installation, task, observation, receipt, R0-R8, Stage-4,
  submission, merge, deployment, assurance, and readiness authority field.

The eight updates are binding metadata adoption only. They do not make old
evidence current, prove installation equality, create R0 evidence, or grant an
operational capability.

## Future Implementation And Validation

Only after fresh independent Codex E acceptance and a separate exact owner
implementation decision may Codex C edit the five listed files. It must apply
the eight substitutions mechanically, in order, and stop on drift.

Required validation is:

1. verify all input sizes, hashes, literal occurrence counts, and frozen inputs;
2. recompute all five output hashes plus the Stage-3 and Role Pool projections;
3. run the repository-owned offline Role Pool gate with
   `py -B docs/codex_skills/mythic-edge-role-pool/scripts/run_release_tests.py`;
4. run the focused bootstrap, offline-observation, launch-observer, and
   direct-interpreter-preflight test modules;
5. rerun the accepted `131` adapter/planner focused tests unchanged;
6. run the aggregate repository test gate and require the nine classified
   successor-binding failures to disappear with zero new failure;
7. run Ruff on the five edited paths, `tools/check_agent_docs.py`,
   `git diff --check`, protected-surface and private-marker scans;
8. verify only the five authorized files changed from their bound inputs and
   no process or generated residue survives.

Operation-free tests may use only their existing synthetic fixtures and
temporary roots. No real task, observer, preflight, installer,
synchronization, registry, release, GitHub, network, or external operation is
permitted.

There is no repair budget or implementation authority in this contract.
Concrete in-scope implementation or review defects may route through the
normal Codex D then Codex E path only after the separate owner implementation
decision. Any out-of-scope path or semantic requirement returns to Codex B.

## Stop Conditions

Stop without editing or widening scope if:

- any bound input, reviewed head, literal count, manifest, or tree tuple drifts;
- the nine failures no longer have the exact binding causes above;
- any substitution changes file length or a nonliteral byte;
- another path or deterministic consumer is required;
- a production owner, schema, lifecycle, authority, safety rule, or runtime
  behavior must change;
- validation would need to be skipped, weakened, deleted, or made advisory;
- unrelated worktree changes cannot be preserved; or
- cleanup, process state, or result is ambiguous.

## Review And Handoff

A fresh-context Codex E reviewer must independently verify the exact source
artifacts, five-file/eight-literal closure, prospective hashes, manifest and
tree calculations, consumer exclusions, and false-authority boundaries. Only
an accepted review may make a separate owner implementation decision eligible.

```yaml
workflow_handoff:
  role_performed: "Codex B: Narrow Current Stage-3 and Dependent Successor-Binding Contract Writer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/813"
  pr: "https://github.com/Tahjali11/Mythic-Edge/pull/815"
  reviewed_predecessor: "7c71461a3f515c1b74904391afff693aea328abd"
  source_finding: "ME-RP-813-E-007"
  result: "contract_candidate_pending_independent_review"
  implementation_scope: "five existing files; eight same-length SHA-256 literals"
  production_behavior_change_authorized: false
  implementation_authorized: false
  submission_authorized: false
  operational_authority: false
  r0_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: independent current Stage-3 and dependent successor-binding contract reviewer"
```
