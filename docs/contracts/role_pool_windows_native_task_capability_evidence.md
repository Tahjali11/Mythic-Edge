# Role Pool Windows Native-Task Capability Evidence Contract

Status: `contract_review_pending`

Risk tier: `high`

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/757

Phase 8 tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

Completed profile source:
https://github.com/Tahjali11/Mythic-Edge/issues/744

Completed authority-index source:
https://github.com/Tahjali11/Mythic-Edge/issues/755

Authority references:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/contracts/trusted_owner_native_role_pool_profile.md`

## Findings And Binding Reconciliation

1. The profile-contract SHA-256 supplied to Codex B was
   `2389a39359df156908bc7dc8aa2aa00bf0025c3f5cdba531ba5e92831b436269`.
   It does not match the repository artifact or issue #757. The current
   repository artifact and live issue independently bind
   `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322`.
   This contract uses the recomputed current value and does not treat the
   supplied stale value as accepted evidence.
2. The production installer observer currently returns false because no exact
   production capability evidence is bound. This is a fail-closed current
   state, not evidence that the host can or cannot provide the first-party
   capability.
3. The repository's one-use synthetic adapter and its tests prove only the
   in-repository adapter contract. They do not prove that the Windows Codex
   host exposes the production task capability.
4. The current authority index predates the issue #755 closure and PR #756
   merge. It is navigation only and is stale for this decision. This contract
   reads the owning issue, accepted profile, canonical source, and current
   GitHub state directly.

## Module And Ownership

Module: read-only Windows native-task capability evidence and verdict
derivation for the trusted-owner Role Pool profile.

Internal project area: `Quality / Governance`.

Truth owner:

- the first-party Codex runtime owns whether it exposes a capability and the
  metadata that describes that capability;
- the accepted trusted-owner profile owns the required launcher identity,
  request, cardinality, receipt, timeout, unknown-outcome, no-retry, and
  no-fallback guarantees; and
- this contract owns only the evidence requirements, public-safe projections,
  and deterministic verdict derivation.

Generic subagent behavior, a successful task observed elsewhere, repository
tests, mocks, adapters, comments, memory, and this contract do not own
production capability truth.

Bridge-code status: `shared_support`.

## Files Owned By This Contract

Codex B may create only:

`docs/contracts/role_pool_windows_native_task_capability_evidence.md`

A later independently authorized Codex E contract review may create only:

`docs/contract_test_reports/role_pool_windows_native_task_capability_evidence_contract_review.md`

A later independently authorized evidence pass may create:

`docs/contract_test_reports/role_pool_windows_native_task_capability_evidence.md`

The contract-review report accepts or rejects only this contract. It is not a
capability observation. The later evidence report is a public-safe evidence
projection. Neither report is a capability provider, launcher, registry,
release-state record, installation receipt, R0 record, or authority source.

## Current Exact Bindings

| Binding | Current exact value |
| --- | --- |
| Core base | `origin/main@9dbc34e74d067c094bb2995480e47852eb3ab671` |
| Source issue | `https://github.com/Tahjali11/Mythic-Edge/issues/757` |
| Phase 8 tracker | `https://github.com/Tahjali11/Mythic-Edge/issues/746` |
| Accepted profile contract | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `2389a3936b80fbc2fd83366df51bc1ae7a80f0a3ce46470e657aed54a4b09322` |
| Canonical Role Pool source | `docs/codex_skills/mythic-edge-role-pool/` |
| Canonical source file count | `34` |
| Canonical source byte count | `2001219` |
| Canonical manifest byte count | `4921` |
| Reviewed source manifest SHA-256 | `6c9d9e4a5bf41c3bc5a33fa4f64ca1342f1f90f03cf03402577279a1686b1175` |
| Installed Role Pool observation | `target_differs / drift`, read-only observation with no installation or synchronization |
| Required host class | trusted runtime observation where `os.name == "nt"` and `sys.platform == "win32"` |
| Required launcher identity | `codex:native-task-create/v1` |
| Current production observer | unavailable and fail-closed; no accepted production observation |
| Repository registry | `docs/role_pool/trusted_owner_repository_registry.v1.json`, absent |
| Release state | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`, absent |

Every later inspection must refresh these values before observing capability
metadata. Drift selects `insufficient_evidence`; it does not authorize an
in-place update, inferred replacement, task, installation, or R0 action.

## ADR-0008 WIP-1 Reconciliation

PRs #374 and #391 remain open and unresolved. The owner's current invocation
records this bounded exception:

```yaml
lane_activation:
  exception_name: "explicit_user_override"
  repository: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #757 Windows native-task capability evidence contract"
  blocked_active_issue_or_pr:
    - "PR #374"
    - "PR #391"
  reason: "The owner explicitly authorized one narrow Codex B contract while the two unrelated PR lanes remain open."
  allowed_scope:
    - "read current public repository and GitHub authority"
    - "create only docs/contracts/role_pool_windows_native_task_capability_evidence.md"
    - "run the contract validation named below"
    - "produce one Codex E contract-review handoff"
  expiration_condition: "This Codex B contract and handoff are complete, or the owner revokes or redirects the lane."
  authorized_by: "Tahjali11 current user instruction"
  recorded_in: "docs/contracts/role_pool_windows_native_task_capability_evidence.md"
```

The exception does not transfer to Codex E, a metadata inspector, a synthetic
characterization role, an installer, or an R0 role. Each later role must
reconcile WIP-1 independently and obtain its own authority when required.

## Closed Verdicts

The capability evidence report must use exactly one of these verdicts:

1. `exact_capability_supported`
2. `capability_unavailable`
3. `insufficient_evidence`

No alias, success-like intermediate verdict, partial-support verdict,
fallback-supported verdict, readiness verdict, or inferred verdict is
permitted.

Each capability fact uses one evidence state:

- `established`: current authoritative evidence directly proves the exact
  predicate;
- `contradicted`: current authoritative evidence directly proves the exact
  predicate false; or
- `not_established`: evidence is missing, partial, stale, indirect,
  contradictory, untrusted, or cannot be inspected without unauthorized
  effects.

Evidence states are fact-level observations, not verdicts.

## Nine Capability Facts

The report must contain these nine rows in this order. Every row is
independently reviewable and must cite only public-safe evidence references.

| Order | Fact ID | Exact predicate |
| --- | --- | --- |
| 1 | `windows_host_identity` | Trusted runtime observation reports both `os.name == "nt"` and `sys.platform == "win32"` before caller input can influence host classification. No caller-controlled platform field or override exists. |
| 2 | `exact_launcher_available_and_compatible` | Authoritative first-party metadata identifies the available compatible launcher exactly as `codex:native-task-create/v1`. Missing, differently named, version-incompatible, or weaker launchers do not satisfy this fact. |
| 3 | `request_binding` | The launcher accepts the exact `trusted_owner_native_task_request.v1` shape and binds one canonical request digest, claim observation, lane packet, repository, issue, role, base, worktree observation, isolated context, no forked turns, issuance time, and self-digest without ambient conversation or caller-selected host data. |
| 4 | `one_task_cardinality` | One accepted invocation can create at most one task for the exact request. It cannot fan out, create a sibling task, or accept a second invocation under the same single-use authority. |
| 5 | `receipt_binding` | One accepted task returns a `trusted_owner_native_task_receipt.v1` binding the exact request digest, one fresh task ID, acceptance time, first-party platform receipt reference and digest, and receipt self-digest. A generic task result or repository-generated receipt is insufficient. |
| 6 | `timeout_enforcement` | The exact launcher enforces the contracted timeout and routes timeout to the accepted ordered failure and reconciliation behavior without creating a replacement task. |
| 7 | `unknown_outcome_fail_closed` | An unknown creation or terminal state preserves observed objects, blocks replacement task creation, requires read-only reconciliation, and remains unknown when identity or terminal state cannot be established. |
| 8 | `automatic_retry_forbidden` | The capability and its integration cannot automatically invoke task creation again after rejection, timeout, ambiguity, unknown outcome, or another failure. |
| 9 | `fallback_forbidden` | Missing, incompatible, failed, timed-out, or unknown native capability cannot invoke a shell, subprocess, `codex exec`, broker, repository executable, generic subagent launcher, alternate task surface, weaker receipt, or silent fallback. |

Combining exact launcher identity, availability, and compatibility in fact 2
preserves the issue's nine-fact acceptance boundary while keeping each
remaining contracted guarantee distinct.

## Metadata-Only Inspection

Metadata-only inspection is always the first capability phase. It is read-only
and may inspect only first-party capability metadata already exposed to the
current Codex runtime. It must occur before any task-creating operation.

The inspector must:

1. refresh all public bindings and WIP authority;
2. derive the host class from trusted runtime observation, never a request
   field;
3. inspect only an already exposed first-party capability descriptor or
   equivalent read-only runtime metadata;
4. project each of the nine facts to one evidence state;
5. derive one closed verdict;
6. retain only the public-safe report; and
7. stop without creating a task, claim, worktree, command, process, registry,
   release record, installation staging object, or other persistent workflow
   mutation.

This contract does not invent or assert that a host metadata API, descriptor,
provenance field, task receipt, or proof mechanism exists. If the current
runtime exposes no authoritative metadata source, the relevant facts are
`not_established` and the verdict is `insufficient_evidence`.

The following are never substitutes for authoritative production metadata:

- successful generic subagent or task behavior;
- the availability of multi-agent or thread tools;
- a task created outside this issue and exact boundary;
- repository source, tests, fixtures, mocks, or the one-use synthetic adapter;
- shell output, process discovery, executable discovery, or environment
  variables; and
- remembered, summarized, or user-entered claims about host capability.

No task may be created merely to discover whether task creation is authorized.

## Deterministic Verdict Derivation

Derive the verdict in this order:

1. Use `capability_unavailable` when current authoritative evidence directly
   contradicts one or more of the nine exact predicates. This includes an
   unsupported trusted host observation, an explicitly absent exact launcher,
   an incompatible exact launcher, or an authoritative guarantee that is
   false.
2. Otherwise use `insufficient_evidence` when any fact is
   `not_established`, any binding is stale, metadata provenance is not
   authoritative, sources disagree, inspection would require a task or
   forbidden operation, or public-safe projection cannot be completed.
3. Use `exact_capability_supported` only when all nine facts are
   `established` from current authoritative evidence and no contradictory,
   stale, fallback, or private-value evidence exists.

An authoritative negative is distinct from missing or conflicting evidence.
Missing, partial, indirect, contradictory, stale, or uninspectable evidence
must not be relabeled as capability absence.

## Optional Single-Use Synthetic Characterization

Metadata inspection stops after its report. If metadata alone does not
establish all nine facts, this contract grants no task authority.

A later single-use synthetic task characterization requires all of the
following before any task-creating call:

1. an accepted independent Codex E review of this contract and the exact
   metadata-only result;
2. a separate explicit owner decision naming the exact contract, metadata
   result, host, launcher, bounded request, timeout, one-task limit, no-retry,
   no-fallback, expiry, cleanup, and unknown-outcome route;
3. a separately reviewed activation or equivalent authority artifact that
   makes one task the maximum and is atomically consumed before invocation;
4. authoritative metadata establishing enough of the exact launcher identity,
   availability, compatibility, and containment behavior to make the one task
   itself authorized rather than exploratory authority discovery; and
5. a public-safe evidence and independent-review route fixed before execution.

That later authority may permit at most one inert task characterization. It
must not permit a second task, automatic retry, alternate launcher, fallback,
repository mutation, installation, registry or release-state mutation,
dispatch lane, canary, or R0 action.

This contract does not define the host API, activation schema, task payload,
platform receipt provenance, or cleanup mechanism for that future operation.
Those are unresolved owner and runtime inputs. If they cannot be defined
without guessing, the task remains unauthorized and the current result remains
`insufficient_evidence`.

## Public-Safe Evidence Report

The later evidence report is human-readable Markdown and contains, in this
order:

1. source issue, tracker, Core base, profile-contract digest, and source
   manifest digest;
2. inspection mode, either `metadata_only` or, only after separately accepted
   authority, `single_use_synthetic_characterization`;
3. the nine fact IDs in contract order, each with one evidence state and
   public-safe evidence reference;
4. exactly one closed verdict;
5. `task_creation_count`;
6. `automatic_retry_count`;
7. `fallback_attempt_count`;
8. `persistent_workflow_mutation_count`;
9. independent review reference and reviewed artifact digest, when review is
   complete; and
10. all authority and readiness non-claims.

For metadata-only inspection, all four counts are zero. For a separately
authorized synthetic characterization, `task_creation_count` may be one and
the other three counts remain zero. A count outside those bounds selects
`insufficient_evidence`, preserves observed objects, and stops routing.

Only these values may be projected about the launcher identity:

- `exact_launcher_identity_observed`
- `launcher_absent`
- `other_or_incompatible_launcher_observed`
- `launcher_identity_not_established`

The report must not serialize or echo:

- task transcripts, prompts, responses, or raw runtime output;
- private paths, worktree paths, installed paths, task IDs, or handle values;
- credentials, tokens, environment names or values, account identities, or
  access-control data;
- raw capability descriptors, exception text, stack traces, command output, or
  unrelated host details; or
- caller-provided claims as runtime observations.

Task and platform receipt identities, if a later operation is authorized, are
represented only by the exact public-safe reference and SHA-256 binding
permitted by that later authority. No raw receipt is copied into this report.

## Stale, Unknown, And Failure Behavior

- Binding drift, stale evidence, unknown fields, malformed evidence, provenance
  ambiguity, private-value risk, and partial inspection fail closed to
  `insufficient_evidence`.
- An unsupported host or authoritative exact-capability failure yields
  `capability_unavailable` and leaves the manual one-issue, one-role workflow
  available.
- Unknown outcome never creates a replacement task or upgrades evidence.
- No current outcome may activate a fallback.
- The first accepted immutable evidence report is preserved. A later changed
  host, runtime, profile, launcher, contract, manifest, or evidence source
  requires a fresh versioned observation and independent review; it must not
  overwrite or reinterpret the earlier report.
- Any attempted side effect during metadata-only inspection invalidates the
  inspection and selects `insufficient_evidence`.

## Routing And Authority Effect

`exact_capability_supported` permits only routing to frame and independently
authorize the next R0 prerequisite. It does not authorize installation,
synchronization, registry population, scheduling-surface creation,
release-state creation, task dispatch, canary execution, or R0 entry or
advancement.

`capability_unavailable` blocks the native R0-R8 ladder on the observed host.
It does not block the existing manual workflow and does not authorize an
alternate launcher or external-isolation profile.

`insufficient_evidence` blocks capability-dependent installation and R0
routing until current evidence is sufficient or a separate safe
characterization path is accepted and authorized.

Every capability result requires fresh independent Codex E review before it
can affect installation or R0 routing. Contract acceptance is not capability
acceptance.

Any later operational R0 decision must also refresh or supersede the stale
current-authority index through its own scoped workflow.

## Protected Boundaries And Non-Claims

Current, contract-review, metadata-inspection, and terminal authority keep all
of these false:

- task creation;
- claim or worktree creation;
- shell, subprocess, `codex exec`, broker, repository executable, alternate
  launcher, or fallback execution;
- Role Pool installation or synchronization;
- registry or release-state creation or mutation;
- command-registry or allowlist population;
- lane dispatch or automatic role transition;
- synthetic characterization without separate exact owner authority;
- canary execution;
- R0 entry or R0-R8 advancement;
- Stage 4 execution or advancement;
- submission, merge, deployment, readiness, assurance, or live use.

Codex B must not probe the capability, create an evidence report, inspect
private evidence, edit the accepted profile or canonical Role Pool source, or
alter Project fields.

## Validation Required

Codex E must independently verify:

- current repository, issue, tracker, open PR, ADR-0008, contract, source, and
  manifest bindings;
- the supplied stale profile digest is not used as accepted evidence;
- the current production observer remains fail-closed and the existing adapter
  remains synthetic-only;
- exactly three verdicts and nine ordered facts exist;
- verdict derivation is deterministic for all combinations of established,
  contradicted, and not-established facts;
- metadata-only inspection cannot create a task or another side effect;
- generic subagent behavior cannot satisfy any production fact;
- no fallback can satisfy or bypass the exact launcher;
- no private value or raw host output is permitted;
- contract acceptance and every verdict preserve the authority boundaries
  above;
- only this contract changed; and
- these commands pass:

```powershell
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main
py tools\check_secret_patterns.py --base origin/main
```

Validator decomposition remains an evidence-triggered watch item and is
outside this issue.

## Acceptance Criteria

- The current Core, accepted profile, canonical source manifest, issue,
  tracker, and open-PR state are exact and refreshed.
- All nine capability facts are closed, ordered, and independently reviewable.
- Metadata-only inspection precedes and is authority-separate from any
  task-creating characterization.
- No task is created to discover whether task creation is authorized.
- Every unknown, partial, contradictory, stale, indirect, or untrusted
  observation fails closed.
- Exactly one verdict is derived without fallback or inference from generic
  task behavior.
- Public evidence is bounded and no-echo.
- A supported verdict grants only routing to the next prerequisite.
- An unavailable verdict preserves the manual workflow.
- All installation, registry, release, dispatch, canary, R0, Stage 4,
  submission, merge, deployment, assurance, and readiness authority remains
  false.

## Remaining Unknowns

1. Whether the current Windows Codex host exposes authoritative read-only
   first-party metadata for `codex:native-task-create/v1`.
2. The exact provenance and semantics of any such host metadata.
3. Whether metadata alone can establish all nine capability facts.
4. If metadata is insufficient, whether the owner will authorize a separately
   contracted single-use synthetic characterization.
5. The future exact task authority, request transport, first-party platform
   receipt, timeout, unknown-state reconciliation, and cleanup mechanism.

These unknowns do not permit Codex B or Codex E to invent an API, infer support,
or create a task.

## Next Workflow Action

Next role: Codex E, independent contract reviewer.

Codex E reviews only the exact contract bytes and public repository/GitHub
bindings. It may create only the contract-review report named above. It must
not perform metadata inspection or task characterization. After accepted
contract review, a separate owner decision may authorize one metadata-only
inspection role.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/757"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "docs/contracts/role_pool_windows_native_task_capability_evidence.md"
  target_artifact: "docs/contract_test_reports/role_pool_windows_native_task_capability_evidence_contract_review.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/role-pool-native-task-capability-evidence-757"
  internal_project_area: "Quality / Governance"
  truth_owner: "first-party Codex runtime metadata plus the accepted trusted-owner profile"
  bridge_code_status: "shared_support"
  capability_probe_authorized: false
  task_creation_authorized: false
  installation_or_sync_authorized: false
  registry_or_release_state_authorized: false
  dispatch_or_canary_authorized: false
  r0_entry_or_advancement_authorized: false
  stage4_authorized: false
  submission_or_merge_authorized: false
  live_ready: false
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "py tools/check_protected_surfaces.py --base origin/main"
    - "py tools/check_secret_patterns.py --base origin/main"
  stop_conditions:
    - "repository, issue, tracker, contract, source, or manifest binding drift"
    - "no current ADR-0008 lane authority for the reviewing role"
    - "need to inspect host capability metadata or create a task"
    - "need to invent a host API, provenance, receipt, or proof mechanism"
    - "need to edit accepted profile or canonical Role Pool source"
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
  accepted_adrs_read:
    - "docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md"
  protected_surfaces:
    - "first-party Codex task capability and launcher identity"
    - "task creation, receipt, timeout, unknown-outcome, retry, and fallback boundaries"
    - "Role Pool installation, registry, release state, dispatch, canary, and R0 authority"
  authority_conflicts_found: true
  authority_conflict_notes: "The owner supplied a stale profile digest; live issue #757 and the repository artifact agree on the refreshed current digest used by this contract. Open PRs #374 and #391 require the recorded B-only explicit_user_override."
  stop_conditions:
    - "binding drift"
    - "ambiguous capability truth ownership"
    - "private or task-creating evidence required"
    - "scope expands beyond one contract"
```
