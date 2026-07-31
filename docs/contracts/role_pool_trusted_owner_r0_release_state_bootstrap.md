# Role Pool Trusted-Owner R0 Release-State Bootstrap Contract

## Source And Role

- Repository: `Tahjali11/Mythic-Edge`
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/771>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/746>
- Dedicated coordination surface:
  <https://github.com/Tahjali11/Mythic-Edge/issues/769>
- Role: Codex B, Module Contract Writer
- Risk tier: `high`
- Governing guidance:
  - `AGENTS.md`
  - `docs/agent_rules.yml`
  - `docs/agent_constitution.md`
  - `docs/codex_module_workflow.md`
  - `docs/agent_threads/module_contract.md`
  - `docs/templates/module_contract.md`
  - `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`

## Findings

1. At `origin/main@2417287195b19d418f72bac3be25dea80740287f`,
   the canonical registry is valid, the source and installed Role Pool trees
   are identical, and the fixed release-state path is absent.
2. The production R0 checker returns
   `terminal_status=eligible_for_independent_review`, evidence self-digest
   `142d768a20aeed30eaa1f3510926ec94ee6d544e4c7f23dfad3d5685dbad3033`,
   all five effect counts at zero, and all 16 authority flags false.
3. The accepted profile and `check_pool_plan.py` already own the exact
   15-field release-record schema, canonical encoding, self-digest, chain
   validation, and current-rung derivation. No new repository writer, release
   schema, validator, gate family, scheduler, or release framework is
   required.
4. The #761 checker intentionally treats any present release chain as a
   pre-bootstrap conflict. It owns eligibility before creation, not the
   post-creation R0 decision. Post-creation acceptance therefore requires
   direct reuse of the existing release-record and release-chain validators
   plus fresh independent readback.
5. `docs/role_pool_current_authority_index.md` truthfully records absent
   release state and becomes stale when the fixed release path appears. Its
   refresh belongs in the same reviewed future implementation package.
6. Issue #769 is open with zero top-level comments. This contract and every
   later approval, review, and handoff must use issue #771, tracker #746, a
   pull request, or a repository artifact instead of commenting on #769.
7. Open PRs #374 and #391 are unrelated. This correction continues the
   already active #771 lane after its stopped Codex C preconsumption attempt;
   it does not activate a second ADR-0008 WIP slot.

### Consolidated Review Corrections

Independent review of predecessor SHA-256
`aefd9ce4756951377665a4e8e6ced5ac6c073e89a8c5392dd122e8ff91b1b78b`
opened:

- `ME-RP-771-E-001`: `blocking_durable_consumption_gap`; and
- `ME-RP-771-E-002`: `blocking_lifecycle_precedence_overlap`.

This revision closes both together:

1. one canonical public-safe consumption receipt must be durably published as
   a unique issue #771 comment and read back before any release-path write;
2. the receipt permanently spends the owner decision even if no release file
   is later created;
3. unknown comment publication is reconciled once by read-only issue-comment
   observation and is never retried; and
4. lifecycle selection is phase-qualified, with every row explicitly
   excluding earlier predicates and all later phases.

The consumption receipt is the minimum new evidence shape proved necessary by
review. It is not a release record, claim, task, registry entry, command,
schedule, or general authority mechanism.

### Preconsumption Sequencing Correction

Codex C stopped cleanly against accepted contract SHA-256
`c7c53b7f0bd7cb6a27b8fab49193d10ba58d3131e976bc3fcb4e1c4058dde90f`
at base `2417287195b19d418f72bac3be25dea80740287f`. The exact
blocking finding is:

- `ME-RP-771-C-001`:
  `blocking_preconsumption_index_receipt_reference_cycle`.

The contract required complete refreshed-index bytes before consumption while
also requiring those bytes to contain the consumption-comment URL. GitHub
assigns that URL only after successful comment publication. No compliant
implementation can satisfy both requirements simultaneously.

The stopped attempt preserved:

- owner decision
  <https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139189967>
  with exact body SHA-256
  `c083406f87c31488eb7a3731e7d75406e7044c6e2855655e3f82e8ba824ad069`
  as `approved_unconsumed`;
- `consumption_receipt_created=false`;
- `release_state_created=false`;
- zero repository-file changes; and
- a clean C worktree.

This revision changes only sequencing. Before consumption, C validates the
receipt, release record, and an exact index refresh plan with one deliberately
unresolved scalar. After exact consumption-comment readback, C inserts the
returned URL, validates the complete index bytes, and only then may attempt
exclusive release creation.

The observed eligibility and owner comments remain immutable historical
lineage. They bind the predecessor contract and therefore do not transfer
authority to this revision. Neither is edited, deleted, consumed, or
reinterpreted. After this revision is independently accepted and integrated,
fresh eligibility and a fresh owner decision are required.

## Module And Truth Ownership

Module: first trusted-owner R0 release-state record and independent rung
decision.

Internal project area: `Governance / Role Pool`.

Bridge-code status: `shared_support`.

Truth ownership is divided as follows:

- `docs/contracts/trusted_owner_native_role_pool_profile.md` owns the
  release-record schema, canonicalization, chain rules, rung order, and R0
  authority ceiling.
- `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py` owns
  record validation, chain validation, self-digest calculation, and
  current-rung derivation.
- `tools/check_role_pool_r0_bootstrap.py` owns the read-only pre-bootstrap
  eligibility packet. It does not own post-publication R0 acceptance.
- A fresh Codex E eligibility artifact owns the independent statement that
  the then-current prerequisite packet and public bindings are acceptable.
- A separate owner comment on issue #771 owns the exact, expiring, single-use
  R0 creation decision.
- A canonical `trusted_owner_r0_bootstrap_consumption.v1` comment on issue
  #771 owns durable proof that the exact owner decision was spent before any
  release-path write.
- The future exact
  `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` owns current
  rung state only after exact implementation acceptance and integration.
- `docs/role_pool_current_authority_index.md` remains navigational and grants
  no authority of its own.

## Exact Current Bindings

| Binding | Exact value |
| --- | --- |
| Contract base | `origin/main@2417287195b19d418f72bac3be25dea80740287f` |
| Issue | `https://github.com/Tahjali11/Mythic-Edge/issues/771` |
| Tracker | `https://github.com/Tahjali11/Mythic-Edge/issues/746` |
| Coordination surface | `https://github.com/Tahjali11/Mythic-Edge/issues/769`, open, zero top-level comments |
| Accepted predecessor bootstrap contract | `docs/contracts/role_pool_trusted_owner_r0_release_state_bootstrap.md`, SHA-256 `c7c53b7f0bd7cb6a27b8fab49193d10ba58d3131e976bc3fcb4e1c4058dde90f` |
| Accepted predecessor review | `docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_bootstrap.md`, SHA-256 `32defd765d98485830ce05ffdd438d377f6a059f37579bac8b1e9aabcd7fc24c` |
| Historical eligibility comment | `https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139113990`, SHA-256 `c566d485c7a86b19d80c96f3b58567521a1de50544c8dfb850eb22ec3c25671e`, predecessor-only |
| Historical owner decision | `https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139189967`, SHA-256 `c083406f87c31488eb7a3731e7d75406e7044c6e2855655e3f82e8ba824ad069`, `approved_unconsumed_predecessor_only` |
| Trusted-owner profile | `docs/contracts/trusted_owner_native_role_pool_profile.md`, SHA-256 `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| R0 eligibility contract | `docs/contracts/role_pool_trusted_owner_r0_offline_bootstrap_validation.md`, SHA-256 `9793951fa1a5a2e6ca7d1bb6325e89e9c2ca185aa4609b19481891405ef32a03` |
| Current R0 binding successor | SHA-256 `07ab1c7153ba1312533bdc27d984789127fb7fc02190d26853ffae1849c2ac82` |
| Registry-bootstrap contract | `docs/contracts/role_pool_canonical_repository_registry_bootstrap.md`, SHA-256 `f64dc584f780b0454d0dab59224796928e85f07c2f1bfb7a0574f7e0e217ac77` |
| Registry-bootstrap review | `docs/contract_test_reports/role_pool_canonical_repository_registry_bootstrap.md`, SHA-256 `198e10e6f193999b66f7d22b430fe5897fdf6b64aec2ac0d82151b6573d4c002` |
| Registry artifact | `docs/role_pool/trusted_owner_repository_registry.v1.json`, 1478 bytes, artifact SHA-256 `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb` |
| Registry self-digest | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Current-authority-index contract | `docs/contracts/role_pool_current_authority_index.md`, SHA-256 `0bf511be26724fb0963525a14e682cb8cbb47fe7169c603348c0358de1f2e5e0` |
| Current authority index | `docs/role_pool_current_authority_index.md`, SHA-256 `4fd141f4abcd725ec18779e14b3d82bfb0a651f834b90bbe637235c411ace274` |
| Canonical and installed Role Pool tree | 41 nodes, 36 files, 6495 canonical bytes, SHA-256 `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Release validator owner | `docs/codex_skills/mythic-edge-role-pool/scripts/check_pool_plan.py`, SHA-256 `af9b9aed5b74bc508c08ce6ab51ce2ee9377aecef5657fca884145fa80c4e62d` |
| Release validator tests | `docs/codex_skills/mythic-edge-role-pool/scripts/test_check_pool_plan.py`, SHA-256 `60201804ed1700d5d75b615a39fc06ad0585b7073ca0a48d07e4fc99579f7b49` |
| R0 checker | `tools/check_role_pool_r0_bootstrap.py`, SHA-256 `34e7eddb31d2e476c74f857a010d441ee1e199915658964bd8cc0f0da2f5d914` |
| R0 checker tests | `tests/test_check_role_pool_r0_bootstrap.py`, SHA-256 `976aaac0fab0d8651b89122c2bdcd46ce3abf10a3f0764083574c2243381ac34` |
| Validator bundle | SHA-256 `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| Current eligibility packet | 2621 bytes, artifact SHA-256 `894973a726fc0837064eee8d1df630994e0a3006817464f4bd317adfdf045802` |
| Current eligibility self-digest | `142d768a20aeed30eaa1f3510926ec94ee6d544e4c7f23dfad3d5685dbad3033` |
| Current eligibility result | `eligible_for_independent_review=true`; all effects zero; all authority false |
| Release-state destination | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`, absent |

Every future review or implementation must refresh these values from its
current base. Drift stops before owner-decision use or repository mutation.
No digest may be reconstructed from an older prompt, index, or handoff.

## Files Owned By This Contract

Codex B creates only:

- `docs/contracts/role_pool_trusted_owner_r0_release_state_bootstrap.md`

The accepted predecessor report remains immutable:

- `docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_bootstrap.md`

Independent review of this revision may create exactly one versioned report:

- `docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_bootstrap_sequencing.md`

After contract acceptance and integration, the fresh eligibility review is a
public-safe GitHub issue-comment artifact on issue #771. It is not a comment
on #769 and is not a repository file.

After that eligibility artifact and a separate exact owner decision, Codex C
may publish exactly one contract-defined consumption-receipt comment on issue
#771 and may change exactly these repository paths:

1. create
   `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`;
2. refresh `docs/role_pool_current_authority_index.md`; and
3. create
   `docs/implementation_handoffs/role_pool_trusted_owner_r0_release_state_bootstrap_comparison.md`.

No source, validator, checker, test, registry, installed-skill, workflow,
schema, or other repository path belongs to the implementation envelope. The
one consumption-receipt comment is not a fourth file and grants no issue,
claim, or command authority beyond its own exclusive publication. If that one
comment plus these three paths are insufficient, Codex C must stop and return
to Codex B.

The historical eligibility and owner comments listed above are not that future
eligibility artifact or owner decision. They must not be used to enter
consumption under this revised contract.

## Existing Release Record And Exact Bootstrap Projection

The future release file contains exactly one canonical JSON line with the
existing 15 fields in this order:

| Order | Field | Exact bootstrap rule |
| ---: | --- | --- |
| 1 | `schema_version` | `trusted_owner_native_release_record.v1` |
| 2 | `record_id` | `r0.bootstrap.` plus the first 32 lowercase hexadecimal characters of SHA-256 over the ASCII `owner_decision_ref` |
| 3 | `predecessor_record_sha256` | null |
| 4 | `from_rung` | null |
| 5 | `to_rung` | `R0` |
| 6 | `contract_sha256` | `944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f` |
| 7 | `skill_tree_sha256` | `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| 8 | `registry_sha256` | `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| 9 | `validator_bundle_sha256` | `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |
| 10 | `observation_receipt_sha256s` | empty array |
| 11 | `codex_e_review_ref` | exact fresh issue #771 eligibility-comment URL |
| 12 | `codex_e_review_sha256` | SHA-256 of the exact UTF-8 eligibility-comment body returned by GitHub |
| 13 | `owner_decision_ref` | exact later owner-decision comment URL on issue #771 |
| 14 | `accepted_at_utc` | GitHub-created whole-second UTC timestamp of the owner-decision comment |
| 15 | `record_sha256` | existing self-digest algorithm |

Canonical bytes use UTF-8 without BOM, no insignificant whitespace, existing
field order, and exactly one final LF. The record self-digest preimage is the
canonical object with only `record_sha256` omitted and the final LF retained.
The complete file is exactly the complete canonical record bytes; there is no
blank line, CR, second line, staging marker, wrapper, or metadata header.

The dynamic review and owner references prevent this contract from naming the
future final self-digest. Codex C must derive it only after both public
references exist and all fixed bindings remain exact.

### Non-Publishable Known-Answer Vector

This vector proves the existing algorithm only. Its `kat` references and
digest of repeated `1` characters are synthetic and forbidden for release:

```json
{"schema_version":"trusted_owner_native_release_record.v1","record_id":"r0.bootstrap.6413117c0ab4f2d8ec64ae978754e4dc","predecessor_record_sha256":null,"from_rung":null,"to_rung":"R0","contract_sha256":"944c1a85d9e2454fb82a5df3e2a2ac572191e3cd135c7854e0c012ffc07ab43f","skill_tree_sha256":"18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f","registry_sha256":"93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7","validator_bundle_sha256":"ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5","observation_receipt_sha256s":[],"codex_e_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-kat-review","codex_e_review_sha256":"1111111111111111111111111111111111111111111111111111111111111111","owner_decision_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-kat-owner","accepted_at_utc":"2026-07-31T00:00:00Z","record_sha256":"4486727ab750ea82e70ecfda99ec115302a5f9e5356ab0c712c5e54bfbfbe5e9"}
```

The code block contains a final LF. Exact vector results are:

- derived record ID:
  `r0.bootstrap.6413117c0ab4f2d8ec64ae978754e4dc`;
- self-digest preimage: `897` bytes;
- complete record: `980` bytes;
- self-digest:
  `4486727ab750ea82e70ecfda99ec115302a5f9e5356ab0c712c5e54bfbfbe5e9`;
- complete artifact SHA-256:
  `acde429344fee760597fb9e52d9ce53fd4a7e35781116ff43ce5180b70c41aaf`;
- `validate_trusted_native_release_record`: no errors;
- `validate_trusted_native_release_chain([record])`: no errors; and
- `trusted_native_current_rung([record])`: `R0`.

## Fresh Independent Eligibility Review

Contract review is not eligibility review. After this contract and its review
are integrated, fresh Codex E must reobserve the then-current repository and
publish exactly one public-safe eligibility artifact as an issue #771 comment.

The comment must include, as labeled plain text:

- role `Codex E: R0 bootstrap eligibility reviewer`;
- verdict `accepted_exact_r0_bootstrap_eligibility`;
- current `origin/main` commit;
- this integrated contract path and SHA-256;
- accepted contract-review reference and digest;
- exact #761 packet artifact SHA-256 and evidence self-digest;
- `registry_status=valid_exact`;
- `release_state_status=absent_bootstrap_candidate`;
- `terminal_status=eligible_for_independent_review`;
- source/install tree equality and exact tree SHA-256;
- exact registry artifact SHA-256 and self-digest;
- exact validator-bundle SHA-256;
- current-authority-index SHA-256 and truthful absent-release row;
- issue #769 open with zero top-level comments;
- all five effect counts zero;
- all 16 authority flags false;
- release creation, R0 acceptance, R1-R8, dispatch, Stage 4, and readiness
  explicitly false; and
- a terminal statement that a separate owner R0 decision may be considered.

The review reference is the immutable GitHub comment URL. The review digest is
SHA-256 of the exact UTF-8 `body` string returned by the GitHub API, with its
existing LF characters and with no added or removed final LF. The comment must
be unedited: GitHub `created_at` and `updated_at` must match. Codex C and the
later implementation reviewer must refetch the comment, reproduce the digest,
and reject a body, timestamp, author, issue, or URL mismatch.

This uses the existing release record's `public_ref` and `sha256` fields. It
does not create a new persistent schema, validator, release status, or gate
family.

## Separate Owner R0 Decision

Only after accepted fresh eligibility may Tahjali11 post one exact decision on
issue #771. The decision must:

- identify actor ID `229644849`;
- authorize exactly one direct creation attempt for the first R0 record and
  same-package authority-index refresh;
- bind the current main commit, this contract and review, the fresh
  eligibility reference and digest, profile contract, skill tree, registry,
  validator bundle, current index, release destination, and three-file Codex C
  scope;
- authorize exactly one canonical consumption-receipt comment on issue #771
  before the first release-path write;
- require `attempt_limit=1`, `single_use=true`, and
  `reuse_authorized=false`;
- expire exactly 12 hours after its GitHub-created whole-second UTC timestamp;
- state that its GitHub comment URL is `owner_decision_ref`;
- state that its GitHub-created timestamp is the record's
  `accepted_at_utc`; and
- retain every R1-R8, process, task, claim, command, dispatch, Stage-4,
  submission, merge, deployment, and readiness authority as false.

The comment must be unedited and owner-authored. Its owner-decision digest is
SHA-256 of the exact UTF-8 `body` string returned by GitHub, preserving its
existing LF characters and adding or removing no final LF. C must derive the
exact record ID from its URL as specified above. Missing, stale, edited,
expired, already attempted, ambiguous, or differently bound decisions fail
closed.

Read-only preflight does not consume the decision. After every precondition
and both in-memory candidates pass, the decision becomes permanently spent
immediately before the single permitted consumption-receipt POST. A known
comment failure, unknown comment result, release collision, unknown release
call result, write failure, readback failure, or later index failure never
restores or transfers it. Every result after that boundary must record
`owner_decision_status=consumed_nonreusable`.

## Durable Consumption Receipt

The sole durable consumption evidence is one canonical, public-safe issue
#771 comment with schema
`trusted_owner_r0_bootstrap_consumption.v1`. It has exactly 12 fields in this
order:

| Order | Field | Type and exact rule |
| ---: | --- | --- |
| 1 | `schema_version` | string; `trusted_owner_r0_bootstrap_consumption.v1` |
| 2 | `owner_decision_ref` | string; exact owner-comment URL |
| 3 | `owner_decision_sha256` | string; lowercase 64-hex digest of the exact owner-comment body |
| 4 | `eligibility_review_ref` | string; exact accepted eligibility-comment URL |
| 5 | `eligibility_review_sha256` | string; lowercase 64-hex digest of the exact eligibility-comment body |
| 6 | `bootstrap_contract_sha256` | string; lowercase 64-hex digest of this integrated contract |
| 7 | `owner_bound_base_commit` | string; lowercase 40-hex commit bound by the owner |
| 8 | `release_state_path` | string; exactly `docs/role_pool/trusted_owner_native_release_state.v1.jsonl` |
| 9 | `record_id` | string; exact value derived from `owner_decision_ref` |
| 10 | `attempt_limit` | integer; exactly `1` |
| 11 | `consumption_status` | string; exactly `consumed_nonreusable` |
| 12 | `consumption_sha256` | string; lowercase 64-hex self-digest |

Unknown, missing, duplicate, reordered, or differently typed fields are
invalid. Canonical bytes use UTF-8 without BOM, no insignificant whitespace,
the field order above, and exactly one final LF. The self-digest preimage omits
only `consumption_sha256` and retains the final LF. The comment body is exactly
the complete canonical bytes, with no Markdown fence, prose, heading, or
wrapper.

This non-publishable vector proves the receipt algorithm only:

```json
{"schema_version":"trusted_owner_r0_bootstrap_consumption.v1","owner_decision_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-kat-owner","owner_decision_sha256":"2222222222222222222222222222222222222222222222222222222222222222","eligibility_review_ref":"https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-kat-review","eligibility_review_sha256":"1111111111111111111111111111111111111111111111111111111111111111","bootstrap_contract_sha256":"3333333333333333333333333333333333333333333333333333333333333333","owner_bound_base_commit":"2417287195b19d418f72bac3be25dea80740287f","release_state_path":"docs/role_pool/trusted_owner_native_release_state.v1.jsonl","record_id":"r0.bootstrap.6413117c0ab4f2d8ec64ae978754e4dc","attempt_limit":1,"consumption_status":"consumed_nonreusable","consumption_sha256":"c1a27275f03f166ca52df60dc573c3e48fb40a92d63a9cefa545003a03247479"}
```

The code block contains a final LF. Exact vector results are:

- field count: `12`;
- self-digest preimage: `818` bytes;
- complete receipt: `906` bytes;
- self-digest:
  `c1a27275f03f166ca52df60dc573c3e48fb40a92d63a9cefa545003a03247479`;
- complete artifact SHA-256:
  `ad36c3ccf378d370a1ab5027857d852845ecdee9896b9da7df7f0f3330beb509`.

Before publishing, C must enumerate all issue #771 comments and prove no
receipt names the same `owner_decision_ref`. C then generates and validates
the complete receipt in memory, permanently marks the decision spent, and
attempts exactly one comment creation. It must refetch all issue #771 comments
once after that call and accept only one unedited comment whose body is exactly
the prepared bytes and whose self-digest is exact.

A reported success or unknown call result with exactly one exact receipt
advances to release publication. A known call failure with no matching receipt
is terminal and spent. Zero matching receipts after an unknown call, multiple
matches, malformed matches, unreadable comments, a known-failure/result
contradiction, or any other uncertain publication state is terminal and
ambiguous. Comment creation is never retried. The comment is never edited,
deleted, replaced, or treated as release, R0, claim, task, command, or
submission authority.

## Pre-Creation Preconditions

Before consumption, future Codex C must:

1. use a fresh worktree from the owner-bound current `origin/main`;
2. recompute every public artifact and current tree binding;
3. refetch and validate the fresh eligibility and owner comments, including
   the exact owner-comment body digest;
4. verify the owner decision is unexpired and has no prior matching
   consumption receipt or other attempt evidence;
5. rerun the production #761 checker and require the exact accepted
   `eligible_for_independent_review` packet;
6. confirm issue #769 remains open with zero top-level comments;
7. confirm the registry remains the exact active Core validation-only object;
8. confirm source/install equality and the exact validator bundle;
9. confirm the current index exactly and its absent-release row remains
   truthful;
10. observe `docs` and `docs/role_pool` as stable ordinary non-reparse
    directories;
11. require the exact final release path to be absent;
12. build the complete consumption receipt, complete release record, and exact
    index refresh plan in bounded memory;
13. validate both canonical receipts, the release record, one-record chain,
    current rung, source index, every fixed index edit, the one deferred index
    scalar, and all exact bindings in memory; and
14. require the worktree to have no unrelated changes.

No broad search, alternate path, case variant, symlink, junction, caller path,
environment override, registry change, or #769 comment is permitted.

## Index Refresh Plan And Post-Consumption Finalization

The preconsumption index refresh plan is bounded in-memory state, not a
durable schema, artifact, placeholder file, or second implementation path. It
must bind:

1. the exact current index bytes and SHA-256
   `4fd141f4abcd725ec18779e14b3d82bfb0a651f834b90bbe637235c411ace274`;
2. every fixed edit required by `Current-Authority Index Refresh`;
3. the already known consumption-receipt self-digest;
4. exactly one unresolved public scalar named `consumption_receipt_ref`; and
5. an exact renderer that places that scalar once in a new Snapshot Bindings
   bullet and nowhere else.

Before consumption, C must prove that the renderer accepts one well-formed
issue #771 comment URL, rejects a different repository, issue, fragment,
missing value, additional value, or second occurrence, and preserves the
index title, six-column table, 12-family order, unrelated rows, and final LF.
The synthetic URL used for this pure check is discarded in memory. It is never
treated as evidence or placed in candidate bytes.

No guessed URL, sentinel text, null, empty string, marker, later text
replacement, partially rendered index, or publishable placeholder is valid.
The unresolved scalar is allowed only in the in-memory plan and only until
exact consumption readback.

After `CP-01`, C must use the exact immutable `html_url` returned by readback
of the sole matching consumption comment. It then renders the complete index
exactly once and requires:

- the URL identifies repository `Tahjali11/Mythic-Edge`, issue #771, and the
  exact read-back comment;
- the URL appears exactly once in Snapshot Bindings and nowhere else;
- the receipt self-digest and every other fixed fact are exact;
- no unresolved scalar or synthetic value remains;
- the complete index parses under its existing structural rules;
- the diff is limited to the contracted refresh; and
- the complete bytes and SHA-256 are frozen before release publication.

Known finalization failure selects
`r0_bootstrap_index_finalization_invalid`. Unreadable, contradictory, or
otherwise uncertain finalization selects
`r0_bootstrap_index_finalization_unknown`. Both preserve the consumption
comment, keep the owner decision spent, create no release state, perform no
index write, and permit no retry.

## Exclusive Creation And Independent Readback

No persistent writer is introduced. Codex C may use one bounded in-memory
construction command that imports the existing canonical and validation
owners and opens only the fixed final path with exclusive create-new binary
semantics equivalent to Python `xb`.

The ordered operation is:

1. complete all preconditions and in-memory validation;
2. mark the owner decision consumed and nonreusable immediately before the
   one permitted issue #771 receipt-publication call;
3. publish or fail-closed reconcile exactly one canonical consumption receipt;
4. only after exact receipt readback, finalize and validate the complete index
   bytes as defined above;
5. only after exact index finalization, exclusively create the absent final
   release path;
6. write the complete canonical line once;
7. flush, synchronize, and close the handle;
8. reopen the fixed path read-only;
9. require exact byte equality and exact complete SHA-256;
10. strictly parse its only line;
11. require the existing record and one-record chain validators to return no
   errors;
12. require current rung `R0`;
13. write only the frozen, finalized current-authority index bytes;
14. read back the index and require exact frozen-byte equality; and
15. write the implementation handoff with the exact consumption reference,
   consumption self-digest, result, and consumed decision disposition.

No repository staging path, rename, overwrite, replacement, append to an
existing file, repair in place, alternate writer, second comment call, second
release creation call, or automatic retry is allowed.

Codex E must later perform an independent fresh-process readback of the exact
release bytes, chain, index, GitHub references, and authority ceiling. The
candidate record has no current rung effect before that review and separately
approved integration.

## Current-Authority Index Refresh

The same future package must preserve the index's title, authority
precedence, stale behavior, six-column table, 12-family order, public-safe
references, manual refresh model, and no-authority rule.

It must:

1. bind the implementation base and refresh date;
2. add this contract, its accepted review, the fresh eligibility reference
   and digest, owner-decision reference, consumption-receipt reference and
   self-digest, release-record self-digest, and complete release artifact
   SHA-256 to snapshot facts;
3. preserve the exact profile, 41-node source/install equality, registry, and
   validator bindings;
4. change only the `trusted_owner_release_state` row from absent state to
   classification `current_normative_authority` and lifecycle
   `active_r0_offline_only_release_state`;
5. state that the candidate row becomes current only after exact
   implementation acceptance and integration;
6. state that R0 permits offline validation only and creates no process, task,
   claim, command, dispatch, R1-R8, Stage-4, or readiness authority;
7. add the accepted release-bootstrap artifacts to
   `current_implementation_and_review_evidence`; and
8. preserve every unrelated row and Security/watch-item disposition.

The consumption-receipt reference appears exactly once in Snapshot Bindings.
The evidence table may name the repository contract, review, and
implementation-handoff paths but must not repeat that URL. This exact
cardinality owns the single deferred scalar in the refresh plan.

No change to `docs/contracts/role_pool_current_authority_index.md` is
authorized. This contract supplies the narrow event-triggered successor
instruction for the release-state appearance.

## Closed Lifecycle And Failure Precedence

Lifecycle selection uses one explicit active phase. Phases are monotonic and
closed:

1. `preflight`
2. `consumption_publication`
3. `index_finalization`
4. `release_publication`
5. `release_readback`
6. `index_refresh`
7. `candidate_complete`
8. `implementation_review`
9. `integration`

An observation from an earlier or later phase is not eligible while another
phase is active. A phase advances only through the exact transition row below.
Terminal rows never advance. This phase discriminator prevents a broad
preflight predicate from shadowing a later collision, ambiguous commit,
readback, review, or integration result.

The `preflight` phase evaluates these six Boolean predicates in order:

1. `public_bindings_exact`;
2. `eligibility_exact`;
3. `owner_decision_exact`;
4. `destination_safe_and_absent`;
5. `preconsumption_candidates_and_plan_exact`; and
6. `consumption_precondition_exact`.

Its normalized observation is the first false predicate, or `all_exact` when
all six are true. Therefore each later preflight row explicitly requires all
earlier predicates true.

The `consumption_publication` raw domain is the Cartesian product of call
result `{reported_success, known_failure, unknown}` and read-only comment
reconciliation `{exact_one, none, multiple_or_invalid, unreadable}`.
`receipt_exact` requires `exact_one` with call result `reported_success` or
`unknown`; `known_failure_absent` requires `known_failure` plus `none`; every
other tuple is `publication_ambiguous`.

The `index_finalization` domain is exactly
`{exact, known_invalid, unknown_or_ambiguous}`. It begins only after `CP-01`.
It uses the exact read-back comment URL to complete and freeze the index.
Only `exact` advances to release publication.

The `release_publication` raw domain is call result
`{reported_success, known_collision, known_other_failure, unknown}` crossed
with final-path observation `{absent, present, unreadable}`. A known collision
always selects `known_collision`; a known other failure plus proven absence
selects `known_failure_final_absent`; a known other failure without proven
absence or any unknown call selects `unknown_write_state`; and reported
success selects `reported_success` for exact readback.

All remaining phases use only the exact observations shown:

| Row | Active phase | Exact normalized observation | Result and required disposition |
| --- | --- | --- | --- |
| `PF-01` | `preflight` | `public_bindings_exact=false` | Terminal `blocked_r0_bootstrap_binding_drift`; stop before consumption or write. |
| `PF-02` | `preflight` | first false is `eligibility_exact` | Terminal `blocked_r0_bootstrap_eligibility_invalid`. |
| `PF-03` | `preflight` | first false is `owner_decision_exact` | Terminal `blocked_r0_bootstrap_owner_decision_invalid`. |
| `PF-04` | `preflight` | first false is `destination_safe_and_absent` | Terminal `blocked_r0_bootstrap_destination_unsafe`; preserve all objects. |
| `PF-05` | `preflight` | first false is `preconsumption_candidates_and_plan_exact` | Terminal `blocked_r0_bootstrap_candidate_invalid`. |
| `PF-06` | `preflight` | first false is `consumption_precondition_exact` | Terminal `blocked_r0_bootstrap_consumption_precondition`; the decision is already spent if prior evidence makes reuse uncertain. |
| `PF-07` | `preflight` | `all_exact` | Advance only to `consumption_publication`. |
| `CP-01` | `consumption_publication` | `receipt_exact` | Advance only to `index_finalization`; decision is durably spent. |
| `CP-02` | `consumption_publication` | `known_failure_absent` | Terminal `r0_bootstrap_consumption_failed_known`; no release write and no retry. |
| `CP-03` | `consumption_publication` | `publication_ambiguous` | Terminal `r0_bootstrap_consumption_ambiguous`; preserve comments, perform no release write, and never retry. |
| `IF-01` | `index_finalization` | `exact` | Advance only to `release_publication`; complete index bytes and SHA-256 are frozen. |
| `IF-02` | `index_finalization` | `known_invalid` | Terminal `r0_bootstrap_index_finalization_invalid`; preserve the comment, create no release, and never retry. |
| `IF-03` | `index_finalization` | `unknown_or_ambiguous` | Terminal `r0_bootstrap_index_finalization_unknown`; preserve the comment, create no release, and never retry. |
| `RP-01` | `release_publication` | `known_collision` | Terminal `r0_bootstrap_collision_after_consumption`; preserve the appeared object. |
| `RP-02` | `release_publication` | `known_failure_final_absent` | Terminal `r0_bootstrap_release_failed_known_absent`; receipt and decision remain spent. |
| `RP-03` | `release_publication` | `unknown_write_state` | Terminal `r0_bootstrap_unknown_write_state`; preserve every uncertain object. |
| `RP-04` | `release_publication` | `reported_success` | Advance only to `release_readback`. |
| `RR-01` | `release_readback` | `exact` | Advance only to `index_refresh`. |
| `RR-02` | `release_readback` | `known_invalid` | Terminal `r0_bootstrap_readback_invalid`; preserve the final. |
| `RR-03` | `release_readback` | `unreadable_or_unstable` | Terminal `r0_bootstrap_unknown_write_state`; preserve the final. |
| `IR-01` | `index_refresh` | `exact` | Advance only to `candidate_complete`. |
| `IR-02` | `index_refresh` | `known_invalid` | Terminal `r0_bootstrap_index_refresh_invalid`; preserve observed state. |
| `IR-03` | `index_refresh` | `unknown_or_ambiguous` | Terminal `r0_bootstrap_index_refresh_unknown`; preserve observed state. |
| `CC-01` | `candidate_complete` | `handoff_exact` | Terminal `r0_bootstrap_candidate_created_pending_review`; route to fresh Codex E. |
| `CC-02` | `candidate_complete` | `handoff_known_invalid` | Terminal `r0_bootstrap_handoff_invalid`; R0 remains inactive. |
| `CC-03` | `candidate_complete` | `handoff_unknown_or_ambiguous` | Terminal `r0_bootstrap_handoff_unknown`; R0 remains inactive. |
| `ER-01` | `implementation_review` | `accepted` | Terminal `r0_bootstrap_implementation_accepted_pending_integration`; integration still requires separate authority. |
| `ER-02` | `implementation_review` | `rejected` | Terminal `r0_bootstrap_implementation_rejected`; route concrete fixes under separate authority. |
| `ER-03` | `implementation_review` | `missing_or_ambiguous` | Terminal `r0_bootstrap_implementation_review_unresolved`; do not integrate. |
| `IN-01` | `integration` | `completed_exact` | Terminal `r0_bootstrap_integrated_r0_offline_only`; current rung is R0 with only the offline ceiling. |
| `IN-02` | `integration` | `pending_or_not_authorized` | Terminal `r0_bootstrap_implementation_accepted_pending_integration`. |
| `IN-03` | `integration` | `mismatched_or_unknown` | Terminal `r0_bootstrap_integration_unresolved`; do not infer R0. |

The finite selector audit covers 106 raw tuples: 64 preflight predicate
vectors, 12 consumption tuples, three index-finalization observations, 12
release-publication tuples, and three observations for each of the five later
phases. Exact results are
`overlap_count=0`, `uncovered_count=0`, and `unreachable_row_count=0` across
all 32 rows.

There is no cleanup of a consumption comment or a present or ambiguously
present final release path. In-memory buffers are discarded after use. Any
generated cache or helper file is residue and blocks acceptance. A preflight
failure leaves the owner decision unconsumed only when no receipt-publication
call was reached; every consumption or later result is terminal and
nonreusable for that decision.

## Validation

Codex B and independent contract-review Codex E must run:

```powershell
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_role_pool_r0_bootstrap.py
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py -k release_state
py -B -m unittest test_check_pool_plan.TrustedOwnerNativeProfileTests.test_external_isolation_classification_and_release_ladder
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

Run the unittest command from
`docs/codex_skills/mythic-edge-role-pool/scripts`; run the others from the
repository root.

Before creation, the production checker must return
`eligible_for_independent_review`. After a release file exists, its deliberate
`blocked_release_state_conflict` result is not a post-publication verdict and
must not be relabeled as failure of a valid R0 chain.

Future C and implementation-review E must additionally:

- reproduce the 12-field consumption-receipt KAT, self-digest, artifact
  digest, uniqueness check, and one-call reconciliation;
- reproduce the record-ID derivation;
- reproduce the exact dynamic self-digest and complete artifact digest;
- require one LF-terminated line and no BOM, CR, blank, or second line;
- call `validate_trusted_native_release_record`,
  `validate_trusted_native_release_chain`, and
  `trusted_native_current_rung`;
- reject a one-at-a-time change to every record field, order, digest, line
  ending, review binding, owner binding, or fixed path;
- verify exclusive create-new collision behavior without replacing the
  accepted candidate;
- verify that the preconsumption index plan has exactly one deferred scalar,
  rejects every malformed completion, and cannot emit publishable bytes before
  exact receipt readback;
- verify that exact receipt readback completes the index once, leaves no
  placeholder, and freezes valid bytes before release publication;
- verify the refreshed index against the exact release readback;
- mechanically enumerate the 106 lifecycle tuples and require
  `overlap_count=0`, `uncovered_count=0`, and
  `unreachable_row_count=0`;
- run the complete existing Role Pool release gate and structural validation;
  and
- require no generated residue, task process, network operation, or unrelated
  file change.

## R0 Authority Ceiling And Non-Claims

Contract acceptance, eligibility acceptance, owner decision, candidate
creation, and implementation review are separate states. Only exact
implementation acceptance followed by separately approved integration makes
the R0 record current.

The observed owner decision ending in comment `5139189967` remains
`approved_unconsumed_predecessor_only`. It grants no authority under this
revision and cannot be consumed, revived, edited, or transferred. A fresh
eligibility review and fresh owner decision are required after this revision
is accepted and integrated.

Current and candidate authority remains:

```yaml
consumption_receipt_comment_authorized: false
release_state_creation_authorized: false
r0_acceptance_authorized: false
r1_r8_advancement_authorized: false
registry_mutation_authorized: false
installation_or_sync_authorized: false
claim_or_command_authorized: false
process_or_task_authorized: false
dispatch_authorized: false
canary_authorized: false
stage4_authorized: false
submission_authorized: false
merge_authorized: false
deployment_authorized: false
trusted_owner_native_profile_ready: false
live_ready: false
```

A later exact owner decision may authorize only one consumption-receipt
comment on issue #771 and the three-file C attempt defined here. It authorizes
no other GitHub mutation. Even after integration, R0 authorizes offline
validation only. It does not authorize App Server, task creation, claims,
commands, dispatch, canaries, R1-R8, Stage 4, installation, deployment, or
readiness.

## Acceptance Criteria

1. The contract reuses the existing release record, chain, canonicalization,
   and digest owners without adding a persistent writer or release schema.
2. Fresh eligibility review, owner decision, creation, implementation review,
   and integration remain distinct.
3. One canonical issue #771 receipt durably and non-reusably consumes the
   owner decision before any release write; unknown publication never retries.
4. Preconsumption validates an exact index plan with one deferred receipt URL;
   exact comment readback completes and freezes the index before any release
   write.
5. The release path must be absent and may be created exactly once without
   overwrite, replacement, append, or retry.
6. The bootstrap line is one valid R0 record with null predecessor and
   `from_rung`, empty observations, exact current fixed bindings, and fresh
   review and owner references.
7. Every stale, consumption, index-finalization, collision, unknown-write,
   readback, index,
   review, integration, and cleanup state selects exactly one phase-qualified
   row and fails closed where required.
8. The future C repository scope is exactly three files plus the sole
   consumption-receipt comment, with no code or test edit.
9. The index truthfully records only the R0 offline ceiling after accepted
   integration.
10. Issue #769 stays open and receives no comments.
11. The predecessor eligibility and approved-unconsumed owner decision remain
    immutable, nontransferable historical lineage.
12. No current role receives release, R0, process, dispatch, Stage-4,
   submission, merge, deployment, or readiness authority.

## Next Workflow Action

Next role: Codex E, independent R0 bootstrap sequencing-correction contract
reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent R0 Bootstrap Sequencing-Correction Contract
Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/771
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Coordination surface: https://github.com/Tahjali11/Mythic-Edge/issues/769
Branch: codex/role-pool-r0-release-bootstrap-sequencing-771

Review only:
docs/contracts/role_pool_trusted_owner_r0_release_state_bootstrap.md

Recompute the contract SHA-256 from the exact Codex B handoff. Review
`ME-RP-771-C-001`, the preconsumption index/receipt-reference cycle, against
accepted predecessor SHA-256
`c7c53b7f0bd7cb6a27b8fab49193d10ba58d3131e976bc3fcb4e1c4058dde90f`
and accepted predecessor-review SHA-256
`32defd765d98485830ce05ffdd438d377f6a059f37579bac8b1e9aabcd7fc24c`.
Refresh origin/main and all public bindings. Verify issue #769 remains open
with zero top-level comments, release state remains absent, the #761 checker returns
eligible_for_independent_review, source/install equality and the registry are
exact, and the current index truthfully records absent release state.

Verify that the existing 15-field release-record schema, self-digest, chain
validator, and current-rung owner remain unchanged. Independently reproduce
both non-publishable known-answer vectors, including the 12-field consumption
receipt's 818/906 byte counts and exact self/artifact digests. Verify its
unique issue #771 publication, one-call reconciliation, permanent
non-reusability, and no release write before exact receipt readback.

Verify the bounded preconsumption index plan has exactly one unresolved scalar,
cannot emit publishable bytes, and is completed only with the exact read-back
consumption-comment URL. Require complete frozen index validation before
release creation and exact one-occurrence URL cardinality.

Mechanically enumerate the 106 lifecycle tuples across the nine phases.
Require all 32 rows reachable with overlap, uncovered, and unreachable counts
all zero. Verify record-ID derivation, exclusive create-new behavior, exact
one-comment plus three-file future C envelope, index refresh, and R0
offline-only ceiling.

Confirm the historical eligibility and owner comments are exact and unedited,
no consumption receipt or release state exists, and the owner decision remains
approved_unconsumed_predecessor_only with no authority under the revision.

Run the contract-required focused, R0 checker, agent-doc, protected-surface,
secret, process, and residue validation. Do not comment on #769, create release
state, approve R0, implement, install, dispatch, submit, merge, or advance any
rung.

Preserve the accepted predecessor report byte-for-byte. If and only if there
are no blocking findings, create the versioned durable report at:
docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_bootstrap_sequencing.md

State that acceptance permits only contract submission/integration routing.
The fresh eligibility review must occur later against the integrated contract;
no owner R0 decision or Codex C work is yet eligible.

End with a workflow_handoff to Codex F for separately approved contract-only
submission.
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
    - "workflow and release-state authority"
    - "current-authority index"
    - "issue and tracker lifecycle"
    - "R0-R8 and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "PRs #374 and #391 remain separate. This is the same active #771 lane returning from a stopped C preconsumption attempt."
  stop_conditions:
    - "public binding or validator drift"
    - "issue #769 receives a top-level comment"
    - "release-state destination appears"
    - "scope beyond this one contract file"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/771"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  predecessor_contract_sha256: "c7c53b7f0bd7cb6a27b8fab49193d10ba58d3131e976bc3fcb4e1c4058dde90f"
  predecessor_review_sha256: "32defd765d98485830ce05ffdd438d377f6a059f37579bac8b1e9aabcd7fc24c"
  finding_status:
    ME-RP-771-C-001: "sequencing_correction_authored_review_pending"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/771"
  target_artifact: "docs/contracts/role_pool_trusted_owner_r0_release_state_bootstrap.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_future_submission_authority"
  branch: "codex/role-pool-r0-release-bootstrap-sequencing-771"
  validation:
    - "current #761 eligibility packet exact"
    - "12-field durable consumption receipt KAT exact"
    - "one-deferred-scalar index plan closure"
    - "106-tuple phase-qualified lifecycle selector audit 0/0/0"
    - "existing release-record and chain validator tests"
    - "agent-doc and diff validation"
    - "protected-surface and secret-pattern scans"
  stop_conditions:
    - "contract or current public binding drift"
    - "issue #769 receives any top-level comment"
    - "release-state destination appears"
    - "future implementation requires more than the sole comment plus exact three-file envelope"
  release_state_created: false
  consumption_receipt_created: false
  historical_owner_decision_status: "approved_unconsumed_predecessor_only"
  owner_implementation_decision_eligible: false
  r0_accepted: false
  r1_r8_authorized: false
  process_or_task_authorized: false
  stage4_authorized: false
  live_ready: false
```
