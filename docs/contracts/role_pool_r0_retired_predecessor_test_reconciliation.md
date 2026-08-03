# R0 Retired-Predecessor Test Reconciliation Contract

## Findings First

1. The accepted proportionate-observation implementation is exact. Its
   independent review found no blocking implementation regression.
2. The complete repository test run has exactly three failures. Each failure
   is an assertion that a retired #780 or #795 loader still accepts the current
   observation harness bytes.
3. The retired loaders correctly reject those changed bytes before loading the
   parent harness, reading private input, or entering a process boundary. Their
   frozen digests are historical evidence and must not be updated.
4. The smallest truthful repair is test-only: replace the three stale success
   expectations with exact fail-closed predecessor-drift expectations. No
   runtime, contract, schema, receipt, observation, or authority behavior
   changes.

Classification: `expected_predecessor_drift_test_reconciliation`.

## Authority And Scope

- Repository: `Tahjali11/Mythic-Edge`.
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/776>.
- Retired preflight issue: <https://github.com/Tahjali11/Mythic-Edge/issues/780>.
- Retired diagnostic issue: <https://github.com/Tahjali11/Mythic-Edge/issues/795>.
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>.
- Protected issue: <https://github.com/Tahjali11/Mythic-Edge/issues/769>.
- Base: `origin/main@be840bc1160678a9678d792d3cfd6074ac86ebca`.
- Branch:
  `codex/role-pool-r0-proportionate-observation-successor-776`.
- Role: Codex B, Module Contract Writer.
- Risk tier: high because this reconciles tests guarding historical execution
  boundaries.

The current owner invocation continues the issue-776 loopback only for this
contract. It creates no implementation or operational authority and does not
activate #780 or #795.

## Exact Accepted Parent

| Artifact | Exact SHA-256 |
| --- | --- |
| Proportionate-observation successor contract | `129ceb8f2bb21f4773e8258ad04238784d986c14168179e1d009b30c584588ae` |
| Accepted contract review | `465af80ae12e10f7e7417dcf93a902807d9155041e8b1f781da8babca46b7b32` |
| Accepted implementation review | `846ecd6ca8f98f6a5c3fbe5f6037800b419f877ee8bad4bee94679fac2030b14` |
| Current observation harness | `ec6fc359bbf630b031784f422e24c7ff560b2e47929af6eb92ea5055545bb8e5` |
| Current observation harness test | `79a60e13d26c49f778c867d9111581bd883240a18f6cee12433d227a967b3784` |

The implementation review verdict is
`accepted_exact_r0_proportionate_offline_observation_successor_implementation`.
Its aggregate result is `2758 passed; 4 skipped; 3 expected predecessor-drift
failures`; no other failure may be absorbed into this reconciliation.

## Exact Three-Function Starting Scope

Codex C may later modify only the bodies and, when needed for truthful naming,
the names of these three existing test functions:

1. `tests/test_run_role_pool_r0_direct_interpreter_preflight.py`
   - starting file SHA-256:
     `435aedabf5d73e02df1cede397f937da6c44b2cecd4ee3ae21b0645bf44e490b`;
   - function:
     `test_exact_public_bindings_are_current_and_targets_are_ordinary`.
2. `tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py`
   - starting file SHA-256:
     `64e6ba5bae8bf75908212f521658853e100ca53686005495255b767653a47493`;
   - function:
     `test_public_bindings_are_exact_without_private_or_process_access`.
3. `tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py`
   - starting file SHA-256:
     `5d44579a85ff21f26e15e40291699d9575d7be17c9c65eae36ca5831f6a4415f`;
   - function:
     `test_actual_loader_validates_frozen_public_artifacts_without_runtime_probe`.

No fixture, helper, import, adjacent assertion, parameterization, runtime file,
accepted report, or other test may change unless an exact syntax/import failure
inside one of these three functions proves a same-file mechanical requirement.
Such a requirement must be reported before expansion; it is not implicit.

## Required Reconciled Assertions

### Retired #780 preflight

The first function must call the existing `_public_bindings()` against the
current repository and prove:

- `exact` is false;
- the parent API is the existing unloaded-parent sentinel rather than the
  current observation harness module;
- no private path or process operation occurs; and
- current executor and test measurements, if asserted, are observations only
  and do not make the historical binding exact.

### Retired #795 identity characterizer

The second function must call the existing `_public_bindings()` and prove:

- `exact` is false;
- the existing zero-digest and unloaded-parent failure projection is returned;
- the current observation harness is not loaded; and
- no private path or process operation occurs.

### Retired #795 secure ingress

The third function must call the existing `load_accepted_characterizer()` and
prove:

- it raises the existing public-safe `SecureIngressError`;
- failure occurs during frozen public-artifact validation;
- runtime validation, console construction, private ingress, and process
  execution are not reached; and
- no raw path, digest mismatch detail, or private diagnostic is emitted.

The tests must pass by asserting deterministic rejection. `skip`, `xfail`,
exception swallowing, conditional acceptance, hash substitution, and deleting
coverage are prohibited.

## Frozen Historical Boundary

Do not change any #780/#795 runtime module, frozen digest, accepted contract,
review report, implementation report, result, or historical identity. In
particular, do not replace the historical harness digests
`001127acf0db441fde6d57c4eaa3545e945fc7275543975b62ef286b23934aa6`
or
`3d9c0403c93ad0db14a51adfe905e7e3be33af13f8787b5b0276380e39ab67c3`
with current hashes.

Those values continue to mean "the exact historical parent accepted by this
retired lane." The current parent remains intentionally different. Rejection
therefore preserves, rather than weakens, the predecessor boundary.

## Validation And Acceptance

Codex C must run, and independent Codex E must repeat or inspect:

```powershell
py -B -m pytest tests/test_run_role_pool_r0_direct_interpreter_preflight.py -q -p no:cacheprovider
py -B -m pytest tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py -q -p no:cacheprovider
py -B -m pytest tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py -q -p no:cacheprovider
py -B -m pytest tests/test_check_role_pool_r0_offline_observation.py -q -p no:cacheprovider
py -B -m pytest -q -p no:cacheprovider
py -B -m ruff check tests/test_run_role_pool_r0_direct_interpreter_preflight.py tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer.py tests/test_run_role_pool_r0_direct_interpreter_identity_characterizer_secure_ingress.py
git diff --check
py -B tools/check_agent_docs.py
py -B tools/check_protected_surfaces.py --base origin/main
py -B tools/check_secret_patterns.py --base origin/main
```

Acceptance requires:

- exactly the three named test functions changed;
- all runtime and accepted implementation bytes unchanged;
- all three tests prove fail-closed historical rejection before private or
  process access;
- no test is skipped, xfailed, weakened, or deleted;
- the focused proportionate suite remains `187 passed`;
- the aggregate suite has the same inventory with the three former failures
  passing and no new failure; absent unrelated drift, the expected result is
  `2761 passed; 4 skipped` plus the existing warning;
- issue #769 remains open with zero comments;
- matching task processes and generated residue are zero.

A different aggregate failure, a runtime edit, any attempt to update a frozen
digest, or inability to prove pre-private/pre-process rejection stops and
returns to Codex B. This contract does not waive CI.

## Authority And Nonclaims

Contract acceptance makes only a separate owner Codex C test-reconciliation
decision eligible. Implementation acceptance may make submission routing
eligible; it does not authorize submission itself.

Implementation, observation, authority consumption, receipt publication,
release mutation, registry/index mutation, installation, task/process launch,
dispatch, canary, R1-R8, Stage 4, submission, merge, deployment, readiness,
security, privacy, or assurance authority is false.

## Next Role

Next role: Codex E, independent retired-predecessor test-reconciliation
contract reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent R0 Retired-Predecessor Test Reconciliation
Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/776
Protected issue: https://github.com/Tahjali11/Mythic-Edge/issues/769

Review only:
docs/contracts/role_pool_r0_retired_predecessor_test_reconciliation.md

Verify the exact contract SHA-256 from the Codex B handoff. Confirm the
accepted proportionate implementation and its review bindings, then verify
that the future scope changes only the three named historical test functions.
The tests must assert deterministic fail-closed rejection of current harness
bytes by retired #780/#795 loaders before private or process access.

Reject any runtime edit, frozen-digest update, skip/xfail, relaxed loader,
new schema, new lane, or attempt to reinterpret historical evidence as
current. Confirm the expected aggregate transition is only the three known
failures becoming passes, with no observation or operational authority.

Do not implement, execute an observation, publish a receipt, mutate issue
#769 or release state, submit, merge, deploy, authorize R1-R8 or Stage 4, or
claim readiness. Findings lead. If exact, route to a separate owner Codex C
decision for only the three contracted test functions.
```

```yaml
instruction_context:
  role: "B"
  risk_tier: "high"
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
  proposed_adrs_read:
    - "ADR-0010"
  protected_surfaces:
    - "retired #780/#795 frozen public bindings"
    - "R0 observation aggregate CI"
    - "issue #769 no-comment boundary"
  authority_conflicts_found: false
  stop_conditions:
    - "a runtime or frozen digest must change"
    - "more than the three named test functions must change"
    - "a failure other than the three reviewed predecessor-drift failures appears"
```

```yaml
workflow_handoff:
  role_performed: "Codex B: R0 Retired-Predecessor Test Reconciliation Contract Writer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/776"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_r0_retired_predecessor_test_reconciliation.md"
  target_artifact: "docs/contract_test_reports/role_pool_r0_retired_predecessor_test_reconciliation.md"
  base_branch: "origin/main"
  target_branch: "unselected_pending_contract_acceptance"
  branch: "codex/role-pool-r0-proportionate-observation-successor-776"
  base_commit: "be840bc1160678a9678d792d3cfd6074ac86ebca"
  contract_sha256: "reported_externally_by_codex_b_to_avoid_self_digest_cycle"
  implementation_scope: "three named test functions; no runtime files"
  implementation_authorized: false
  observation_authorized: false
  receipt_publication_authorized: false
  submission_authorized: false
  r1_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  generated_residue_count: 0
  next_recommended_role: "Codex E: independent retired-predecessor test-reconciliation contract reviewer"
```
