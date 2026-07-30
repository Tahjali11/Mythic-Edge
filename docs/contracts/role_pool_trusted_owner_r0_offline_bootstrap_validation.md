# Role Pool Trusted-Owner R0 Offline Bootstrap Validation Contract

Status: `contract_re_review_pending`

Risk tier: `high`

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/761

Phase 8 tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/746

Authority references:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/contracts/trusted_owner_native_role_pool_profile.md`
- `docs/contracts/role_pool_codex_app_server_native_task_adapter.md`
- `docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md`

## Findings And Scope Decisions

1. The repository has owning validators for registry objects, release records
   and chains, the Stage-3 package manifest, source/install equality, terminal
   selection, and the fake App Server transport. The missing behavior is one
   read-only coordinator that evaluates those owners against the same current
   inputs and emits one public-safe result.
2. The current canonical Stage-3 package is exactly 39 files: 36 Role Pool
   files plus three frozen workflow rows. Its 5,729 canonical bytes have
   SHA-256
   `cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06`.
3. A fresh installer `--check` returned `target_differs / drift`. The current
   source tree contains 36 files while the installed tree contains 34 files.
   No installation or synchronization occurred.
4. The production repository registry and release-state files are both
   absent. Registry absence is blocking. Release-state absence is the required
   bootstrap-candidate state and is not itself an R0 record or acceptance.
5. The issue's suggested checker location inside the installed Role Pool would
   increase the frozen package from 39 to 41 files and force another unrelated
   Stage-3 manifest transition. The smallest coherent implementation instead
   places the coordinator in Core `tools/` and its test in Core `tests/`.
   Existing Role Pool source, its release runner, and its 39-row manifest then
   remain unchanged.
6. `run_release_tests.py` already owns the complete Role Pool gate. Because the
   new focused test is a Core test rather than a Role Pool test module, no
   required-module registration is mechanically necessary. That file is
   outside the Codex C edit envelope.
7. The authority index produced by issue #755 is navigational only and is
   stale under its own refresh rule after issue #758. It is not an input or
   authority source for this decision.
8. The fixed `docs/role_pool` parent is currently absent. The shared
   fixed-input observation rule below proves both exact child inputs absent
   from the stable ordinary `docs` ancestor without creating, enumerating, or
   normalizing any path.
9. `ADR-0011-role-scoped-protected-mutations.md` is proposed and
   non-precedential. It is not an authority reference or accepted ADR for this
   contract.

## Module And Ownership

Module: deterministic read-only R0 bootstrap eligibility validation for the
trusted-owner Role Pool profile.

Internal project area: `Quality / Governance`.

Truth owner:

- the accepted trusted-owner profile owns registry, release-state, source and
  installed-tree, terminal-outcome, authority, and R0 ladder semantics;
- the accepted App Server companion and its exact source own fake-transport
  protocol and lifecycle validation;
- `check_stage3_behavioral_planning.py` owns the 39-row package manifest;
- `tools/install_codex_skills.py` owns source discovery, installed-root
  derivation, unsafe-path rejection, and exact source/install comparison;
- `check_pool_plan.py` owns registry and release-record validation; and
- this contract owns only the cross-bound input set, result schema,
  first-failure selector, no-echo projection, and review-eligibility meaning.

The checker, its result, tests, comments, memory, and AI interpretation do not
own installation, registry, release, dispatch, R0 acceptance, or readiness
truth.

Bridge-code status: `shared_support`.

## ADR-0008 WIP-1 Reconciliation

PRs #374 and #391 remain open and separate. The owner's current invocation is
recorded as this task-scoped exception:

```yaml
lane_activation:
  exception_name: "explicit_user_override"
  repository: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #761 R0 offline bootstrap validation contract"
  blocked_active_issue_or_pr:
    - "PR #374"
    - "PR #391"
  allowed_scope:
    - "read current public repository and GitHub authority"
    - "create only docs/contracts/role_pool_trusted_owner_r0_offline_bootstrap_validation.md"
    - "run contract validation"
    - "produce one Codex E contract-review handoff"
  expiration_condition: "This Codex B contract and handoff are complete, or the owner revokes or redirects the lane."
  authorized_by: "Tahjali11 current user instruction"
```

The exception does not transfer to Codex E, Codex C, installation,
synchronization, registry or release creation, process or task creation, R0,
or another issue.

## Files Owned By This Contract

Codex B creates only:

`docs/contracts/role_pool_trusted_owner_r0_offline_bootstrap_validation.md`

After independent Codex E acceptance and a separate owner implementation
decision, Codex C may create exactly:

1. `tools/check_role_pool_r0_bootstrap.py`
2. `tests/test_check_role_pool_r0_bootstrap.py`

No existing file is in the implementation edit envelope.

In particular, these files remain unchanged:

- `docs/codex_skills/mythic-edge-role-pool/scripts/run_release_tests.py`;
- every file in `docs/codex_skills/mythic-edge-role-pool/`;
- `tools/install_codex_skills.py`;
- every accepted contract and review artifact;
- the production registry; and
- the production release state.

If implementation cannot satisfy this contract in the two named files, Codex
C must stop and route the exact mismatch to Codex B. It must not add a Role
Pool file, change the 39-row manifest, or register another release test.

## Current Exact Bindings

| Binding | Current exact value |
| --- | --- |
| Core base | `origin/main@10d4a4a79053fe33297a612599667d9b58bb4296` |
| Source issue | `https://github.com/Tahjali11/Mythic-Edge/issues/761` |
| Tracker | `https://github.com/Tahjali11/Mythic-Edge/issues/746` |
| Repository database ID | `1235264383` |
| Canonical repository name | `tahjali11/mythic-edge` |
| Accepted profile | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `4a0ba9efe5c987735c09df66f94f42924a92a40ca68fd15a84ffb2c41842c94d` |
| Accepted App Server companion | `docs/contracts/role_pool_codex_app_server_native_task_adapter.md`, SHA-256 `814ac91c4e099216ae4870458d7524a3d65bfba7459cbfda7de82a5fc79067e8` |
| Stage-3 transition contract | `docs/contracts/role_pool_stage3_manifest_37_to_39_amendment.md`, SHA-256 `de17a909d68fa1427d26ea42f5ff575addccf76185c77b93c03499e25bea48fa` |
| Capability-evidence contract | `docs/contracts/role_pool_windows_native_task_capability_evidence.md`, SHA-256 `d165838cf77ff1e9d9f765ece0f68dd86d89b6370a4515f1d6b55b0ccae9ebef` |
| Stage-3 manifest | 39 files, 5,729 canonical bytes, SHA-256 `cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06` |
| Canonical Role Pool install tree | 41 nodes, 36 files, 6,495 canonical bytes, SHA-256 `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Current installed Role Pool tree | 39 nodes, 34 files, 6,159 canonical bytes, SHA-256 `ab56582b39474db9e2cb50f83e7e05a341376efa7c9a10f0b1ec306c94d2009e` |
| Installer owner | `tools/install_codex_skills.py`, SHA-256 `7954d1c6b4cd816b4fb9d09be68a42ea89df9f6ffff20e13b76bab97e965dbda` |
| Registry validator owner | `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py`, SHA-256 `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` |
| Stage-3 validator owner | `docs/codex_skills/mythic-edge-role-pool/scripts/check_stage3_behavioral_planning.py`, SHA-256 `8946eb85257109670cc9f72970972d2458c9f56486127d1c4571e530240dc3b6` |
| Fake-transport owner | `docs/codex_skills/mythic-edge-role-pool/scripts/trusted_native_app_server_adapter.py`, SHA-256 `9a24c6b2f39a327aa6ad0728ba54263f0da134165e9c1bacf9414f50729f9a18` |
| Complete Role Pool gate owner | `docs/codex_skills/mythic-edge-role-pool/scripts/run_release_tests.py`, SHA-256 `1ac0dd02df447a35e7e95e3b534d89a2c7e0b3e5901266b780b5ba13238f8a75` |
| Production registry | `docs/role_pool/trusted_owner_repository_registry.v1.json`, absent |
| Production release state | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`, absent |
| Installed comparison | `target_differs / drift`; no mutation |

Every later implementation or review must recompute all bindings. A mismatch
stops that role. No current digest can be updated by inference.

## Public Interface

The future checker exposes exactly one production CLI:

```text
py -B tools/check_role_pool_r0_bootstrap.py
```

The production CLI accepts no positional arguments, root overrides, output
path, environment selector, registry selector, release selector, skip flag,
fix flag, or mutation mode.

It:

1. derives the repository root from its own ordinary non-reparse file;
2. derives the canonical source root from the fixed repository-relative path;
3. requires `CODEX_HOME` to be absent;
4. derives the installed root through the installer's default current-user
   Codex-home rule and the fixed skill basename;
5. derives the three frozen workflow inputs from that same default skills
   root;
6. derives registry and release-state inputs from their fixed
   repository-relative paths;
7. performs only bounded reads and in-memory validation;
8. emits exactly one canonical public-safe packet to stdout; and
9. performs no other output or side effect.

The module may expose one private typed evaluation seam to its focused tests.
That seam may accept only test-owned temporary roots and must never be callable
through the production CLI. Synthetic results are test evidence only and
cannot use `eligible_for_independent_review` as a durable production claim.

## Input Derivation And Owning Validators

The coordinator must call or import the existing owner named below. Copying
its logic into the checker is prohibited.

| Input or check | Owning implementation | Required coordinator behavior |
| --- | --- | --- |
| Source discovery and installed-root derivation | `tools/install_codex_skills.py` | Use the fixed `mythic-edge-role-pool` source and default target. Reject an ambient `CODEX_HOME` override for production evidence. |
| Ordinary/non-reparse tree safety and equality | installer `_source_tree_unsafe_reason`, `_target_tree_unsafe_reason`, `_tree_snapshot`, and `_directories_match` | Use exact owner results; do not normalize, ignore, repair, or synchronize drift. |
| Stage-3 39-row manifest | `check_stage3_behavioral_planning.py` | Bind the source Role Pool plus exactly the three frozen workflow rows and call the existing manifest validation. |
| Registry parsing and validation | `check_pool_plan.parse_trusted_native_json` and `validate_trusted_native_registry` | Reject duplicate/unknown fields and require exact self-digest and cross-field validity. |
| Release record and chain | `check_pool_plan.parse_trusted_native_json`, `validate_trusted_native_release_record`, and `validate_trusted_native_release_chain` | Parse each nonempty JSONL row strictly; no reconstruction or skipped line. |
| Fake-transport fixed bindings and lifecycle | `trusted_native_app_server_adapter.validate_fixed_contract_bytes` and `validate_lifecycle_registry` | Run only these in-memory checks. Do not call the real process entrypoint. |
| Terminal selection | this contract's ordered table | Select the first non-passing component exactly once. |
| Canonical output | `check_pool_plan.trusted_native_canonical_bytes` and `trusted_native_self_digest` | Preserve profile canonical rules and final LF. |

Private underscore-prefixed installer functions remain installer-owned. Their
reuse is permitted only as a read-only internal Core call by this exact
checker. A later installer refactor must either preserve this behavior or
version this checker contract.

## Manifest And Tree Derivations

### Stage-3 Manifest

The 39-row manifest remains owned by
`check_stage3_behavioral_planning.current_skill_manifest` and its validation.
The coordinator may set only the module's three workflow snapshot paths to the
fixed default installed workflow sibling before invoking the owner. It may not
change expected rows, digests, counts, allowed additions, or modified paths.

Success requires:

- exactly 39 rows;
- exactly 5,729 canonical bytes;
- SHA-256
  `cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06`;
  and
- all existing Stage-3 semantic validation.

### Install-Tree Evidence Digest

Installer equality remains the accepting comparison. The evidence digest does
not replace it.

For each exact `_tree_snapshot` tuple, create one row with fields in this
order:

1. `path`: relative POSIX path;
2. `kind`: exactly `directory` or `file`;
3. `byte_count`: nonnegative integer, zero for a directory; and
4. `sha256`: SHA-256 of the exact payload, including the empty payload for a
   directory.

Rows retain the installer's ordinal relative-path order. Wrap them in an
object with fields `schema_version` and `rows`, where `schema_version` is
`trusted_owner_role_pool_install_tree.v1`. Encode with the profile canonical
JSON rules and one final LF, then SHA-256 the complete bytes.

No node is ignored. `__pycache__`, bytecode, an extra directory, an extra
file, a missing node, a renamed node, case drift, content drift, a symlink, a
junction, or another reparse point prevents equality.

The current source known-answer vector is:

- node count: `41`;
- file count: `36`;
- canonical byte count: `6495`;
- SHA-256:
  `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f`.

The current installed observation is lineage only:

- node count: `39`;
- file count: `34`;
- canonical byte count: `6159`;
- SHA-256:
  `ab56582b39474db9e2cb50f83e7e05a341376efa7c9a10f0b1ec306c94d2009e`;
  and
- equality result: `installed_drift`.

The current installed digest is not an accepted target. A later eligible
result requires exact equality with the then-reviewed source bytes.

## Registry And Bootstrap Release Semantics

### Fixed Input Parent Observation

The checker derives only these fixed repository-relative components:

1. existing ancestor `docs`;
2. optional parent `docs/role_pool`;
3. registry basename `trusted_owner_repository_registry.v1.json`; and
4. release-state basename
   `trusted_owner_native_release_state.v1.jsonl`.

It must not enumerate a directory, search for a sibling, follow a
caller-selected path, accept a case variant, or normalize an alternate path.
It observes each existing component with non-following metadata.

The checker first requires `docs` to be one stable ordinary non-reparse
directory. It then applies exactly one of these parent projections:

- If `docs/role_pool` is absent before and after the bounded fixed-child
  observations while `docs` remains identity-stable, both exact final paths
  are proven absent. The registry projects `registry_status=absent`; the
  release state projects
  `release_state_status=absent_bootstrap_candidate`. Both digests are null.
- If `docs/role_pool` exists, it must be one stable ordinary non-reparse
  directory. Each exact final path is then observed beneath it and classified
  by its owning rules below.
- If either fixed component is unreadable, nonordinary, a reparse point,
  identity-unstable, case-ambiguous, or otherwise not safely observable, the
  affected component status is `unknown`. Parent absence must not be inferred
  from an access failure.

The before/after observations are metadata-only and bounded to these fixed
components. They authorize no directory creation, reservation, enumeration,
content access through an absent prefix, or cleanup.

### Registry

The registry is valid for this checker only when:

- the fixed path is one ordinary non-reparse file;
- strict parsing and `validate_trusted_native_registry` return no error;
- its self-digest is exact;
- it contains exactly one entry with `repository_id=1235264383`;
- that entry has
  `canonical_name=tahjali11/mythic-edge`, `status=active`, and
  `offline_validation` in `permitted_operations`; and
- no duplicate ID, duplicate canonical name, stale review trigger,
  unauthorized command, or unknown field exists.

The checker does not require or authorize an operational command, scheduling
claim, or live launcher. It only validates the reviewed registry object.

### Release State

The exact bootstrap-candidate state is proven by either:

- the fixed parent-absent projection above; or
- an absent exact release-state path beneath a validated stable ordinary
  non-reparse `docs/role_pool` parent.

Either absence projection means:

- `release_state_status=absent_bootstrap_candidate`;
- `release_state_sha256=null`; and
- no file is created, proposed, synthesized, or reserved.

If the file is present, every line must still be strictly parsed and the
existing record and chain validators must run. A valid existing chain means
bootstrap has already occurred and this operation is no longer applicable. An
invalid, forked, duplicate, partial, empty, or stale chain is a conflict. Both
known states select `blocked_release_state_conflict`; the component status
distinguishes `present_valid_chain` from
`present_invalid_or_forked`.

Unreadable, reparse, or ambiguous existence is `unknown`.

## Validator Bundle Custody

The validator bundle is one canonical object with fields in this order:

1. `schema_version`: exactly `trusted_owner_r0_validator_bundle.v1`;
2. `profile_contract_sha256`;
3. `app_server_contract_sha256`;
4. `stage3_manifest_sha256`;
5. `installer_sha256`;
6. `r0_contract_sha256`;
7. `r0_checker_sha256`;
8. `r0_checker_test_sha256`.

Encode the complete object with the profile canonical rules and one final LF.
Its SHA-256 is `validator_bundle_sha256`.

The first four content bindings are fixed by this contract. The R0 contract,
checker, and checker-test digests become exact only after:

1. this contract is independently accepted;
2. Codex C implements the exact two-file scope;
3. Codex E hashes and reviews those exact bytes; and
4. the checker result and E review recompute the same bundle.

The checker may compute its own and its test's digests, but that computation
does not self-accept those bytes. It only makes them eligible for independent
comparison.

## Component Statuses

The following component vocabularies are closed.

`contract_binding_status`:

- `exact`
- `known_invalid`
- `unknown`

`manifest_status`:

- `exact`
- `known_invalid`
- `unknown`

`source_install_status`:

- `identical`
- `installed_missing`
- `installed_drift`
- `unsafe_or_unreadable`
- `unknown`

`registry_status`:

- `valid_exact`
- `absent`
- `invalid`
- `unknown`

`release_state_status`:

- `absent_bootstrap_candidate`
- `present_valid_chain`
- `present_invalid_or_forked`
- `unknown`

`validator_bundle_status`:

- `exact`
- `known_invalid`
- `unknown`

`offline_validation_status`:

- `passed`
- `failed`
- `unknown`

`offline_validation_status=passed` means all bounded in-memory owner calls,
canonical known-answer checks, selector checks, and result-schema checks
completed exactly. It does not mean the source/install, registry, or release
prerequisites passed.

## Terminal Status And First-Failure Precedence

The result uses exactly one of these terminal statuses:

1. `blocked_contract_binding_invalid`
2. `blocked_validator_bundle_invalid`
3. `blocked_manifest_invalid`
4. `blocked_skill_source_drift`
5. `blocked_registry_missing_or_invalid`
6. `blocked_release_state_conflict`
7. `blocked_offline_validation_failed`
8. `unknown_outcome_reconciliation_required`
9. `eligible_for_independent_review`

Evaluate components in this exact order:

| Priority | Component | Known failure | Unknown |
| ---: | --- | --- | --- |
| 1 | contract bindings | `blocked_contract_binding_invalid` | `unknown_outcome_reconciliation_required` |
| 2 | validator bundle | `blocked_validator_bundle_invalid` | `unknown_outcome_reconciliation_required` |
| 3 | Stage-3 manifest | `blocked_manifest_invalid` | `unknown_outcome_reconciliation_required` |
| 4 | source/install | `blocked_skill_source_drift` | `unknown_outcome_reconciliation_required` |
| 5 | registry | `blocked_registry_missing_or_invalid` | `unknown_outcome_reconciliation_required` |
| 6 | release state | `blocked_release_state_conflict` | `unknown_outcome_reconciliation_required` |
| 7 | bounded offline validation | `blocked_offline_validation_failed` | `unknown_outcome_reconciliation_required` |
| 8 | all prior components pass | `eligible_for_independent_review` | not applicable |

The selector chooses the first component that is not passing. It records later
independent component observations in their own fields but never changes the
terminal status. Known and unknown values are mutually exclusive. Unknown
never becomes a known blocker or eligibility.

The current live facts deterministically select
`blocked_skill_source_drift`. `registry_status=absent` is also retained as a
lower-priority observed blocker. Release-state absence remains
`absent_bootstrap_candidate`.

An exhaustive selector test must prove:

- every allowed component vector selects exactly one terminal status;
- overlap count is zero;
- uncovered count is zero;
- every terminal row is reachable; and
- changing only a later component cannot override an earlier failure.

## Public-Safe Result Schema

The packet schema is
`trusted_owner_r0_offline_bootstrap_evidence.v1`.

It contains exactly these 37 fields in this order:

| Order | Field | Type and rule |
| ---: | --- | --- |
| 1 | `schema_version` | Exact schema string. |
| 2 | `operation` | Exactly `evaluate_r0_bootstrap_eligibility_read_only`. |
| 3 | `repository_id` | Exactly `1235264383`. |
| 4 | `repository_name` | Exactly `tahjali11/mythic-edge`. |
| 5 | `issue_url` | Exact issue #761 URL. |
| 6 | `base_commit` | Exact bound 40-character commit. |
| 7 | `profile_contract_sha256` | Exact accepted profile digest. |
| 8 | `app_server_contract_sha256` | Exact accepted companion digest. |
| 9 | `r0_contract_sha256` | Exact independently accepted digest of this contract. |
| 10 | `contract_binding_status` | Closed component enum. |
| 11 | `stage3_manifest_file_count` | Nonnegative integer; `39` when exact. |
| 12 | `stage3_manifest_byte_count` | Nonnegative integer; `5729` when exact. |
| 13 | `stage3_manifest_sha256` | SHA-256 or null only when unobservable. |
| 14 | `manifest_status` | Closed component enum. |
| 15 | `source_tree_node_count` | Nonnegative integer or null when unobservable. |
| 16 | `source_tree_file_count` | Nonnegative integer or null when unobservable. |
| 17 | `source_tree_manifest_byte_count` | Nonnegative integer or null when unobservable. |
| 18 | `source_tree_sha256` | SHA-256 or null when unobservable. |
| 19 | `installed_tree_node_count` | Nonnegative integer or null when missing or unobservable. |
| 20 | `installed_tree_file_count` | Nonnegative integer or null when missing or unobservable. |
| 21 | `installed_tree_manifest_byte_count` | Nonnegative integer or null when missing or unobservable. |
| 22 | `installed_tree_sha256` | SHA-256 or null when missing or unobservable. |
| 23 | `source_install_status` | Closed component enum. |
| 24 | `registry_status` | Closed component enum. |
| 25 | `registry_sha256` | Exact self-digest or null when absent or unobservable. |
| 26 | `release_state_status` | Closed component enum. |
| 27 | `release_state_sha256` | SHA-256 of complete exact bytes or null when absent or unobservable. |
| 28 | `checker_sha256` | SHA-256 of the ordinary checker file. |
| 29 | `checker_test_sha256` | SHA-256 of the ordinary focused test file. |
| 30 | `validator_bundle_sha256` | Exact bundle digest. |
| 31 | `validator_bundle_status` | Closed component enum. |
| 32 | `offline_validation_status` | Closed component enum. |
| 33 | `terminal_status` | Closed terminal enum. |
| 34 | `eligible_for_independent_review` | Boolean; true only for the exact eligible terminal. |
| 35 | `effect_counts` | Exact effect-count object below. |
| 36 | `authority_flags` | Exact 16-field profile authority object below. |
| 37 | `evidence_sha256` | Self-digest. |

`effect_counts` contains exactly:

1. `app_server_process_start_count`
2. `task_creation_count`
3. `network_operation_count`
4. `repository_command_count`
5. `persistent_mutation_count`

Every value is the JSON integer `0`.

`authority_flags` reuses the exact 16 fields and order from
`TRUSTED_NATIVE_AUTHORITY_FIELDS`:

1. `repository_mutation_authorized`
2. `implementation_authorized`
3. `publication_authorized`
4. `merge_authorized`
5. `deployment_authorized`
6. `installation_authorized`
7. `package_operations_authorized`
8. `network_authorized`
9. `secrets_authorized`
10. `external_isolation_authorized`
11. `canary_authorized`
12. `stage4_authorized`
13. `stage_advancement_authorized`
14. `dispatch_authorized`
15. `live_ready`
16. `trusted_owner_native_profile_ready`

Every authority value is JSON `false`.

Cross-field rules:

- `eligible_for_independent_review` is true if and only if
  `terminal_status=eligible_for_independent_review`.
- Eligibility requires exact contract, bundle, manifest, identical
  source/install trees, valid registry, absent bootstrap-candidate release
  state, passed offline validation, zero effects, and all-false authority.
- Any other terminal requires eligibility false.
- Non-null counts and digests must agree with their component status.
- A missing installed tree has all installed count/digest fields null.
- An absent registry has `registry_sha256=null`.
- An absent release state has `release_state_sha256=null`.
- Unknown fields, duplicate fields, wrong order, aliases, floats, nonfinite
  values, or an inconsistent cross-field combination are rejected.

## Canonical Bytes And Self-Digest

The packet uses the accepted profile canonical rules:

- object keys in the declared order at every depth;
- arrays in contract order;
- UTF-8 without BOM;
- no insignificant whitespace;
- no duplicate or unknown fields; and
- exactly one final LF.

For `evidence_sha256`, remove only that member, preserve every other value and
the final LF, and hash the resulting complete canonical bytes. The complete
packet restores the digest member and final LF.

The same input bytes and component observations must produce byte-identical
packets. The packet has no wall-clock time, random reference, host path,
username, process ID, or environment-derived display value.

## CLI Outcomes

The CLI writes only the canonical packet to stdout.

- Exit `0`: `eligible_for_independent_review`.
- Exit `2`: any known blocking terminal.
- Exit `3`: `unknown_outcome_reconciliation_required`.

Stderr remains empty after a valid packet. If packet sealing itself cannot be
completed, the CLI exits `3`, emits only the fixed ASCII line
`r0_bootstrap_packet_unavailable`, and emits no partial JSON.

No output file, staging file, cache, receipt, registry, release record, or
runtime status file is created.

## No-Echo And Privacy

The packet and all error paths must not contain:

- an absolute path or drive letter;
- a username, home directory, environment value, SID, ACL, or file identity;
- registry or release content;
- command output, test output, transcript, exception text, stack trace, or raw
  OS error;
- credential, token, secret, process ID, handle, task ID, thread ID, turn ID,
  claim ID, or worktree path; or
- private installed-tree inventory.

Only the fixed repository-relative references, counts, digests, component
enums, terminal enum, zero effect counts, and false authority flags may leave
bounded memory.

The checker must not print or persist the installer owner's existing
path-bearing CLI lines. It calls the owner in-process and projects only the
closed categories.

## Side Effects And Protected Boundaries

The production checker may:

- read exact public contract and source bytes;
- read metadata and bytes from the fixed installed Role Pool and workflow
  roots;
- read the fixed registry and release-state files if present;
- execute existing pure Python validator functions in-process; and
- write one canonical packet to stdout.

It may not:

- write, create, delete, rename, normalize, chmod, synchronize, install, or
  repair a file or directory;
- invoke a shell, subprocess, repository command, App Server, Codex process,
  task API, broker, service, plugin, hook, MCP server, or network endpoint;
- create a claim, task, thread, turn, worktree, branch, issue, registry entry,
  release record, receipt, or cache;
- access credentials or source outside the fixed inputs;
- perform fallback or retry; or
- authorize implementation, installation, R0, dispatch, canary, R0-R8
  advancement, Stage 4, readiness, or assurance.

`eligible_for_independent_review` is prerequisite evidence only. It permits
only a fresh Codex E review of the exact checker, tests, packet, and bindings.
It is not `R0`, an accepted bootstrap record, an activation, or a release
decision.

## Synthetic Temporary-Root Testing

Focused tests may create only test-owned roots beneath the test framework's
temporary directory. They must clean them on success and failure.

Required cases include:

1. exact synthetic eligible inputs;
2. each of the nine terminal statuses;
3. each component enum;
4. first-failure precedence with every later component also failing;
5. missing, extra, duplicate, reordered, case-varied, and digest-mismatched
   Stage-3 rows;
6. missing, extra, renamed, content-drifted, nonordinary, and reparse source
   or installed nodes;
7. missing, malformed, duplicate-key, unknown-field, wrong-self-digest,
   wrong-repository, inactive-entry, and missing-offline-operation registry;
8. absent `docs/role_pool` beneath a stable ordinary `docs` ancestor, proving
   both fixed inputs absent without mutation or enumeration;
9. present ordinary `docs/role_pool` with an absent release state as candidate;
10. nonordinary, reparse, unreadable, identity-unstable, and case-ambiguous
    fixed ancestors, each projecting `unknown` rather than false absence;
11. valid existing R0 chain, valid later chain, invalid line, fork, duplicate,
    empty file, partial final line, and unreadable release state;
12. owner-validator drift and checker/test bundle drift;
13. deterministic packet equality across two evaluations;
14. packet self-digest and final-LF known-answer tests;
15. rejection of every unknown field and invalid cross-field combination;
16. no absolute path, username, environment value, transcript, raw exception,
    or private diagnostic in stdout or stderr;
17. `CODEX_HOME` override rejection before installed-tree access;
18. zero process, task, network, command, and persistent mutation counts;
19. cleanup after every synthetic success and failure; and
20. no retry, fallback, install, sync, registry write, or release write call.

Mocks may observe forbidden call counts but may not replace the owner
validators in acceptance-path tests.

## Validation And Evidence

Codex C must run, in order:

```powershell
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py tests\test_install_codex_skills.py
```

Then reproduce the accepted Role Pool evidence in an isolated reviewed layout
containing the exact 39-row package:

```powershell
py -B -m unittest test_trusted_native_app_server_adapter.py test_check_pool_plan.py
py -B -m unittest test_stage3_behavioral_planning.py
py -B scripts\run_release_tests.py
```

Expected unchanged predecessor evidence is:

- adapter/planner focused gate: `128` passed;
- Stage-3 focused gate: `88` passed;
- complete offline Role Pool gate: `419` passed and both structural
  validations passed;
- real App Server process starts: `0`;
- tasks created: `0`; and
- generated residue: `0`.

The exact new Core focused-test count is evidence produced by Codex C and
independently reproduced by Codex E. It is not guessed in this contract.

Contract and implementation validation also requires:

```powershell
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

Codex E must independently:

- recompute every exact binding;
- review the exact two-file implementation diff;
- reproduce all focused and aggregate gates;
- run the production checker without path overrides;
- confirm the current terminal remains `blocked_skill_source_drift`;
- confirm `registry_status=absent`;
- confirm `release_state_status=absent_bootstrap_candidate`;
- confirm the absent fixed `docs/role_pool` parent is derived only from the
  stable ordinary non-reparse `docs` ancestor and is not created or
  enumerated;
- verify canonical bytes, self-digest, no-echo, zero effects, and false
  authority; and
- preserve current blocked state rather than installing or populating inputs.

## Acceptance Criteria

- One exact read-only operation binds all named prerequisites.
- Existing owners remain authoritative and are reused rather than copied.
- The production CLI has no root, output, skip, fix, or mutation override.
- The current 39-row manifest reproduces exactly.
- Source/install equality uses the installer owner and fails on every extra or
  missing node.
- Registry absence and invalidity are deterministic blockers.
- Release-state absence, whether proven through the absent fixed parent or
  beneath its validated ordinary parent, is a bootstrap candidate and never
  an accepted record.
- Existing or invalid release state blocks this bootstrap operation.
- The terminal selector is complete, deterministic, and first-failure ordered.
- The packet is canonical, deterministic, public-safe, and self-digested.
- Every effect count is zero and every authority field is false.
- The Core-only two-file implementation leaves the Role Pool source and
  Stage-3 manifest unchanged.
- Independent review eligibility is not represented as R0 acceptance,
  activation, readiness, or authority.
- Current live state remains blocked by installed drift, with registry absence
  also retained.

## Remaining Unknowns And Stop Conditions

- The future checker and focused-test digests are unknown until Codex C creates
  and Codex E reviews them.
- The future exact registry digest is unknown because the production registry
  is absent.
- Real App Server compatibility remains deferred to R2 and is not inspected
  here.
- Installation and registry population require separate issues, contracts,
  owner decisions, and review.
- Stop if the base, accepted contracts, 39-row manifest, owner validators,
  current issue authority, or two-file implementation envelope drifts.
- Stop if a complete result would require a subprocess, network call, private
  echo, write, fallback, retry, or a third implementation file.

## Next Workflow Action

Next role: Codex E, consolidated R0 offline bootstrap validation contract
re-reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Consolidated R0 Offline Bootstrap Validation Contract
Re-reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/761
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746

Review only:
docs/contracts/role_pool_trusted_owner_r0_offline_bootstrap_validation.md

Reviewed predecessor SHA-256:
9afb52ded485152f24b693b4b3c95d8ba90822c1753ec666763fc40fd17a25ed

Source findings:
- ME-RP-761-E-001
- ME-RP-761-E-002

Use a fresh worktree from current origin/main and bind the exact contract
SHA-256 supplied by the Codex B handoff. Independently verify the issue,
accepted profile and App Server contracts, Stage-3 39-row manifest, installer
and validator ownership, current installed drift, absent registry, absent
release state, Core-only two-file implementation envelope, packet schema,
first-failure selector, no-echo boundary, test inventory, and all false
authority.

Confirm specifically that placing the future checker in tools/ and its test in
tests/ leaves the 39-row Role Pool package unchanged and makes a
run_release_tests.py edit unnecessary. Confirm that current live evaluation
must select blocked_skill_source_drift while also retaining registry_status
absent and release_state_status absent_bootstrap_candidate. Confirm that the
currently absent fixed docs/role_pool parent is proven only from a stable,
ordinary, non-reparse docs ancestor without creation, normalization, or
enumeration. Confirm that proposed ADR-0011 is not treated as accepted or
precedential authority.

Confirm that the revision changes only the fixed-parent absence semantics,
their mechanically dependent tests and review instructions, the
nonprecedential ADR reference, and the review-cycle metadata. Report both
source findings fixed_confirmed only if those exact corrections are complete.

Do not implement, edit the installed skill, install or synchronize, populate
the registry, create a release record, start App Server, create a process or
task, dispatch, run a canary, advance R0-R8 or Stage 4, submit, merge, deploy,
or claim readiness. Return findings first and route an accepted contract only
to a separate owner Codex C implementation decision.
```

```yaml
workflow_handoff:
  role_performed: "Codex B: Consolidated R0 Offline Bootstrap Validation Contract Reviser"
  repository: "Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/761"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  source_commit: "10d4a4a79053fe33297a612599667d9b58bb4296"
  predecessor_contract_sha256: "9afb52ded485152f24b693b4b3c95d8ba90822c1753ec666763fc40fd17a25ed"
  contract_artifact: "docs/contracts/role_pool_trusted_owner_r0_offline_bootstrap_validation.md"
  finding_status:
    ME-RP-761-E-001: "corrected_re_review_pending"
    ME-RP-761-E-002: "corrected_re_review_pending"
  implementation_scope:
    - "tools/check_role_pool_r0_bootstrap.py"
    - "tests/test_check_role_pool_r0_bootstrap.py"
  role_pool_manifest: "39 files; 5729 bytes; cc88860794f918afbb050d6149df3cd11d195fab098b907be06f44ed88de7e06"
  current_source_install_status: "installed_drift"
  current_registry_status: "absent"
  current_release_state_status: "absent_bootstrap_candidate"
  current_terminal_status: "blocked_skill_source_drift"
  contract_review_status: "pending_independent_codex_e_re_review"
  implementation_authorized: false
  installation_or_sync_authorized: false
  registry_or_release_state_authorized: false
  process_or_task_authorized: false
  dispatch_or_canary_authorized: false
  r0_r8_authorized: false
  stage4_authorized: false
  live_ready: false
  next_recommended_role: "Codex E: consolidated R0 offline bootstrap validation contract re-reviewer"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "high"
  global_router_read: false
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
  protected_surfaces:
    - "Role Pool canonical source"
    - "installed Role Pool deployment copy"
    - "repository registry"
    - "trusted-owner release state"
    - "App Server process and task boundary"
    - "R0-R8 release ladder"
  authority_conflicts_found: false
  authority_conflict_notes: "PRs #374 and #391 remain separate; the owner supplied this task-scoped explicit_user_override."
  stop_conditions:
    - "binding or authority drift"
    - "need for a third implementation file"
    - "need for installation, registry, release, process, task, network, or other mutation"
```
