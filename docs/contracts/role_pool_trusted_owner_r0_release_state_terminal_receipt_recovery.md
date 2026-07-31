# Role Pool Trusted-Owner R0 Terminal Receipt Recovery Contract

## Module

Exact terminal disposition and fresh-attempt recovery after the issue #771 R0
bootstrap consumption comment was published with noncanonical bytes.

## Source Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/771>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/746>

Dedicated coordination surface:
<https://github.com/Tahjali11/Mythic-Edge/issues/769>

## Role And Risk

- Role: Codex B, Module Contract Writer
- Risk tier: `high`
- Repository: `Tahjali11/Mythic-Edge`
- Base: `origin/main@0e1c58496725b9df5cdde561a5aac0a3c4cb8edd`
- Branch: `codex/role-pool-r0-terminal-receipt-recovery-771`
- ADR-0008 disposition: continuation of the active issue #771 lane after a
  fail-closed Codex C attempt; no second WIP slot is activated

## Findings

1. `ME-RP-771-C-002` is
   `blocking_terminal_consumption_receipt_transport_nonconformance`.
2. The Codex C handoff reports that the single permitted POST returned
   success, and GitHub created comment `5139603966`, but the exact comment body
   is not JSON. Its object keys and string values lack the quotation marks
   required by the accepted canonical receipt schema.
3. The malformed body is `861` UTF-8 bytes, has one final LF, and has exact
   SHA-256
   `482e14a2acb0e69b7bdf97b2d45c4287cd3e0a0f8cf6dad6a9cbb6e2169f91b5`.
   It is owner-authored and unedited at
   `2026-07-31T05:28:17Z`.
4. The exact canonical receipt that was prepared from the accepted public
   bindings would have been `907` bytes with self-digest
   `bf74dc0e0ae70d6aca26b3a7831b3a1b5bf951c86772954990c05bd78c5f9371`
   and complete artifact SHA-256
   `850f51628bd6aec24b69698d7bbac7d7c707821141622442d9e69b864d5a823c`.
   Those prospective bytes are comparison evidence only. They are not the
   bytes GitHub stored and must not be reconstructed as historical success.
5. The accepted parent contract therefore selects `CP-03` and terminal result
   `r0_bootstrap_consumption_ambiguous`. The owner decision is
   `consumed_nonreusable`; no second read, comment edit, delete, repost,
   release write, index write, or retry is permitted for that decision.
6. The release-state destination remains absent, the current-authority index
   remains byte-identical, the implementation handoff is absent, and the C
   worktree is clean.
7. The local matcher failure in the C handoff is not the first bad value. The
   first proven failure is the noncanonical body stored by GitHub. Recovery
   must fix future byte transport and exact-body reconciliation together.
8. Issue #769 remains open with zero top-level comments. Open PRs #374 and
   #391 are unrelated.

## Owning Layer And Truth

Internal project area: `Governance / Role Pool`.

Bridge-code status: `shared_support`.

Truth ownership is:

- GitHub comment readback owns the exact historical body, URL, author, and
  timestamps.
- The accepted parent contract owns the 12-field consumption schema, canonical
  bytes, self-digest rule, release record, index finalization, lifecycle, and
  R0 offline-only ceiling.
- This companion owns only the exact terminal classification of comment
  `5139603966`, permanent nonreuse of decision `5139572911`, and the
  byte-preserving transport and matcher requirements for one later distinct
  attempt.
- The current-authority index remains navigational and grants no authority.

This contract does not relabel malformed bytes as a canonical receipt. It does
not make a local handoff, inferred intent, declared digest, or AI
interpretation the owner of GitHub comment truth.

## Exact Current Bindings

| Binding | Exact value |
| --- | --- |
| Repository base | `origin/main@0e1c58496725b9df5cdde561a5aac0a3c4cb8edd` |
| Accepted bootstrap contract | `docs/contracts/role_pool_trusted_owner_r0_release_state_bootstrap.md`, SHA-256 `a96936c4237652ea1c74b3d63164fa6918bd9c90f509fd3d9f2fce24bb9bb61d` |
| Accepted bootstrap review | `docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_bootstrap_sequencing.md`, SHA-256 `c3f07e5ba5dd51cc3bcfcbe3dbe9f2ba301da16c5988636e42d3d680bfb27ffd` |
| Eligibility comment | `https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139550089`, 2764 bytes, SHA-256 `831b687f5df120f32e1b05143dab3bf52ec7f5c794c2cb395c185dac6a2e12c5`, unedited |
| Spent owner decision | `https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139572911`, 3174 bytes, SHA-256 `2ae7a827033c21fa0ac25e12f872f7fbba44340c7b036599047d3ea51499c331`, unedited |
| Historical malformed comment | `https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139603966`, 861 bytes, SHA-256 `482e14a2acb0e69b7bdf97b2d45c4287cd3e0a0f8cf6dad6a9cbb6e2169f91b5`, unedited |
| Historical terminal result | `r0_bootstrap_consumption_ambiguous` |
| Historical owner status | `consumed_nonreusable` |
| Historical record ID | `r0.bootstrap.e2c7cb44b7d3eb144c4b87d819c09128` |
| Intended receipt preimage | 819 bytes; SHA-256 `bf74dc0e0ae70d6aca26b3a7831b3a1b5bf951c86772954990c05bd78c5f9371` |
| Intended complete receipt | 907 bytes; SHA-256 `850f51628bd6aec24b69698d7bbac7d7c707821141622442d9e69b864d5a823c` |
| Current authority index | `docs/role_pool_current_authority_index.md`, SHA-256 `4fd141f4abcd725ec18779e14b3d82bfb0a651f834b90bbe637235c411ace274` |
| Release-state destination | `docs/role_pool/trusted_owner_native_release_state.v1.jsonl`, absent |
| Implementation handoff destination | `docs/implementation_handoffs/role_pool_trusted_owner_r0_release_state_bootstrap_comparison.md`, absent |
| Registry | `docs/role_pool/trusted_owner_repository_registry.v1.json`, artifact SHA-256 `4979007fac80231fdcee54db43cb24e6651defc9bf37535579ab81dfccd8ecbb`, self-digest `93a29e72b6e66ffff2879a427632d08e6b2424422745f6b1a5e1c3ac056d69a7` |
| Source and installed Role Pool tree | 41 nodes, 36 files, SHA-256 `18c71ce37f79c8984b992d263a549b0bf354b66bb898a1a00a6b28ca8c50251f` |
| Validator bundle | SHA-256 `ec792e6c3141e9e4138c4d14621b289dfa39617101db52ebdbd6a94cf77ea8a5` |

Every later role must refetch public comments and recompute repository bytes.
Drift, edit history, missing bytes, duplicate related comments, release-state
appearance, index drift, or issue #769 comments stop before fresh authority.

## Files Owned By This Contract

Codex B creates only:

- `docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md`

Independent Codex E review may create only:

- `docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md`

No existing contract, review, implementation, index, registry, release,
installed skill, issue comment, or test belongs to this B scope.

## Parent Contract Relationship

The accepted bootstrap contract remains unchanged and controlling for:

- the consumption and release schemas;
- canonical JSON and self-digest rules;
- the preconsumption index plan;
- exclusive release creation and readback;
- lifecycle phases and terminal outcomes;
- the three-repository-file implementation envelope; and
- the R0 offline-only authority ceiling.

This companion is higher precedence only for:

1. the exact terminal disposition of owner decision `5139572911` and comment
   `5139603966`;
2. the prohibition on treating that comment as a receipt or retry target;
3. the additional historical-attempt bindings required by a future fresh
   eligibility review and owner decision;
4. exact binary-safe request construction for a later receipt POST; and
5. exact-body reconciliation scoped to a later distinct owner-decision URL.

No existing schema, lifecycle result, authority profile, gate family, or
repository writer is versioned or replaced.

## Historical Terminal Disposition

The immutable historical state is:

- `attempt_status=terminal`;
- `lifecycle_result=r0_bootstrap_consumption_ambiguous`;
- `owner_decision_status=consumed_nonreusable`;
- `consumption_comment_status=present_malformed_immutable_nonreceipt`;
- `canonical_consumption_receipt_created=false`;
- `release_state_created=false`;
- `authority_index_modified=false`;
- `implementation_handoff_created=false`;
- `r0_accepted=false`;
- `retry_authorized=false`; and
- `comment_repair_authorized=false`.

The malformed comment must never be edited, deleted, hidden, minimized,
reposted, wrapped, quoted in place, or counted as canonical. Its declared
self-digest may be checked only as evidence of the intended candidate. It
cannot substitute for exact stored bytes.

The prospective 907-byte canonical candidate may be regenerated in memory only
as a known-answer comparison. It must never be published under the spent owner
decision or represented as historical receipt bytes.

## Fresh Attempt Eligibility

This contract creates no fresh attempt authority.

Only after this contract and an independent review are integrated may fresh
Codex E publish one new eligibility comment on issue #771. That eligibility
must bind:

- the then-current `origin/main`;
- the parent and recovery contracts and accepted reviews;
- the exact three historical public comments and hashes above;
- `historical_attempt_status=terminal_malformed_receipt_nonreusable`;
- absent release state and unchanged index;
- exact source/install, registry, validator, and #761 packet bindings;
- issue #769 open with zero top-level comments;
- all effect counts zero; and
- all authority flags false.

Only after accepted fresh eligibility may Tahjali11 issue one new owner
decision. It must use a URL distinct from every historical decision and bind:

- the fresh eligibility reference and digest;
- this recovery contract and review;
- the parent bootstrap contract and review;
- all three historical comment references and digests;
- the historical terminal classification;
- the then-current base, index, tree, registry, validators, release
  destination, and three-file C envelope;
- `attempt_limit=1`, `single_use=true`, and `reuse_authorized=false`; and
- a 12-hour whole-second GitHub timestamp expiry.

That decision may authorize one new attempt. It is not a retry, continuation,
repair, or reuse of decision `5139572911`.

## Exact Byte-Preserving Comment Transport

A future Codex C must generate the complete canonical receipt bytes `B` in
bounded memory under the unchanged parent schema.

It must then generate request bytes `W` as canonical UTF-8 JSON:

```text
W = canonical_json({"body": decode_utf8_strict(B)})
```

`W` has exactly one key, `body`; no BOM, insignificant whitespace, or final LF
is added to `W`. The final LF in `B` is encoded inside the JSON string.
Before consumption, strict decoding of `W` must produce exactly one string
whose UTF-8 encoding is byte-identical to `B`.

The existing non-publishable 906-byte parent receipt KAT produces:

- request-wrapper byte count: `964`;
- request-wrapper SHA-256:
  `f1a817216a8379fe1906540b24fbc7c4537f7a7463ac75ffd5318521766d6f1e`;
  and
- exact decoded body equality with the 906-byte KAT: `true`.

The sole permitted real POST uses a direct non-shell child process with this
exact argv shape:

```text
["gh","api","--method","POST",
 "repos/Tahjali11/Mythic-Edge/issues/771/comments","--input","-"]
```

Required process behavior:

- `shell=false`;
- binary stdin receives exactly `W`;
- the canonical receipt is never embedded in a command line;
- at most one POST process is started;
- stdout and stderr are separately bounded to 1 MiB;
- timeout is 30 seconds;
- timeout or unknown termination enters parent unknown-outcome
  reconciliation;
- no automatic retry, replacement process, alternate endpoint, or fallback is
  permitted; and
- raw stdout, stderr, command line, credentials, token state, or executable
  path is not persisted or echoed.

The following are forbidden:

- PowerShell interpolation or argument transport for `B` or `W`;
- `gh issue comment --body`;
- `gh issue comment --body-file`;
- shell redirection, shell pipelines, `Invoke-Expression`, `cmd /c`, or
  `powershell -Command` carrying receipt bytes;
- GraphQL, browser, connector, SDK, curl, alternate executable, or manual
  paste fallback; and
- editing or deleting a comment after publication.

This is a one-operation transport boundary, not a general subprocess or GitHub
mutation capability.

A future exact owner decision may authorize that one helper invocation only as
the implementation mechanism for its separately authorized issue-comment
POST. It does not make Role Pool process, task, command, dispatch, or general
network authority true. No executable launched by the helper may outlive the
bounded POST operation.

## Exact Reconciliation

Before consumption, C freezes `B`, its self-digest, complete SHA-256, and `W`.
After the one POST call, C performs only the parent contract's one bounded
read-only reconciliation.

Matching is byte-first:

1. Fetch issue #771 comments once after the POST call.
2. Encode each returned `body` string as UTF-8 without adding or removing a
   final LF.
3. Count exact byte equality with `B`.
4. Require exactly one exact match.
5. Require that comment to be owner-authored, unedited, on issue #771, and to
   have the response `html_url` when the response URL is observable.
6. Strictly parse only the exact body and rerun the parent schema and
   self-digest validation.
7. Treat any non-exact comment containing the exact fresh
   `owner_decision_ref` as a related malformed match.

Outcomes remain the parent outcomes:

- exactly one valid body, with reported success or unknown call result:
  `CP-01 receipt_exact`;
- known call failure and no exact or related match:
  `CP-02 known_failure_absent`; and
- zero or multiple exact matches, any related malformed match, unreadable
  comments, response contradiction, wrong issue or author, edit history, or
  any other uncertainty:
  `CP-03 publication_ambiguous`.

No substring, regular-expression, unquoted-field, object-property, shell
output, or locally reconstructed matcher may establish `receipt_exact`.
Release creation remains forbidden until `CP-01` is independently derived.

## Closed Recovery Preflight

A future attempt evaluates these nine Boolean predicates in order:

1. `parent_and_recovery_bindings_exact`;
2. `historical_comments_exact_and_unedited`;
3. `historical_terminal_disposition_exact`;
4. `release_absent_and_index_unchanged`;
5. `fresh_eligibility_exact`;
6. `fresh_owner_decision_exact_and_distinct`;
7. `fresh_receipt_and_index_plan_exact`;
8. `binary_transport_kat_exact`; and
9. `no_fresh_owner_related_attempt_evidence`.

The first false predicate selects `TRP-01` through `TRP-09`. All true selects
`TRP-10` and permits entry only to the parent `consumption_publication` phase.
No false result consumes the fresh decision unless existing attempt evidence
makes nonuse uncertain.

The finite selector is:

- preflight predicate vectors: `512`;
- parent consumption tuples: `12`;
- total audited tuples: `524`;
- recovery rows: `10`;
- reused parent consumption rows: `3`;
- total reachable rows: `13`;
- `overlap_count=0`;
- `uncovered_count=0`; and
- `unreachable_row_count=0`.

`TRP-01` through `TRP-09` are terminal
`blocked_r0_terminal_receipt_recovery_preflight` with the first failed
predicate as the public-safe subcondition. `TRP-10` grants no release or R0
authority; it only permits the separately owner-authorized attempt to enter
the unchanged parent consumption phase.

## Side Effects And Authority

Current authority is entirely false:

```yaml
historical_comment_edit_or_delete_authorized: false
historical_owner_decision_reuse_authorized: false
fresh_eligibility_publication_authorized: false
fresh_owner_decision_authorized: false
consumption_receipt_publication_authorized: false
release_state_creation_authorized: false
authority_index_refresh_authorized: false
implementation_handoff_creation_authorized: false
registry_mutation_authorized: false
installation_or_sync_authorized: false
process_or_task_authorized: false
claim_or_command_authorized: false
network_authorized: false
secrets_authorized: false
dispatch_authorized: false
canary_authorized: false
r0_acceptance_authorized: false
r1_r8_advancement_authorized: false
stage4_authorized: false
submission_authorized: false
merge_authorized: false
deployment_authorized: false
trusted_owner_native_profile_ready: false
live_ready: false
```

Contract acceptance permits only contract submission and integration routing.
After integration, a fresh eligibility review and a separate owner decision
remain required. Even a later successful integration permits only R0 offline
validation under the parent ceiling.

## Tests And Validation

Codex B and independent Codex E must:

```powershell
git diff --check
py -B tools\check_agent_docs.py
py -B tools\check_role_pool_r0_bootstrap.py
py -B -m pytest -q tests\test_check_role_pool_r0_bootstrap.py -k release_state -p no:cacheprovider
py -B -m unittest test_check_pool_plan.TrustedOwnerNativeProfileTests.test_external_isolation_classification_and_release_ladder
py -B tools\check_protected_surfaces.py --base origin/main
py -B tools\check_secret_patterns.py --base origin/main
```

Run the unittest from
`docs/codex_skills/mythic-edge-role-pool/scripts`. Because the new file is
untracked during B and E review, also pass its exact repository path through
`--paths-from-stdin` to both path-scoped safety checks.

Independent mechanical validation must additionally:

1. refetch all three current comments and verify URLs, authors, timestamps,
   edit state, byte counts, final-LF state, and hashes;
2. prove strict JSON parsing rejects the 861-byte historical body;
3. derive the historical record ID from the owner URL;
4. reproduce the 819-byte intended preimage, self-digest, 907-byte complete
   candidate, and complete artifact digest without treating them as history;
5. reproduce the 906-to-964-byte transport KAT and wrapper digest;
6. require exact wrapper round-trip body equality;
7. test quote loss, missing LF, CRLF, body prefix/suffix, duplicate exact
   bodies, related malformed bodies, wrong issue, wrong author, edited
   comment, response contradiction, and unreadable comments;
8. enumerate all 524 selector tuples with audit counts `0/0/0`;
9. verify issue #769 remains open with zero comments;
10. verify release and implementation-handoff destinations remain absent and
    the index remains exact;
11. require zero matching task processes, network operations, and generated
    residue; and
12. require this contract to be the only changed path.

No validation in B or contract-review E may post a comment, execute the real
transport, create release state, modify the index, or consume authority.

## Acceptance Criteria

1. The malformed comment and spent decision are exact, immutable, terminal,
   and nonreusable.
2. No historical byte, receipt, comment, or success state is reconstructed.
3. The release, index, and handoff remain untouched.
4. A future attempt requires fresh integrated contracts, fresh eligibility,
   and a distinct fresh owner decision.
5. Canonical receipt bytes enter the GitHub CLI only through binary stdin and
   a single direct non-shell API process.
6. Exact GitHub body-byte equality, not a local field matcher, owns receipt
   acceptance.
7. The existing parent schema, lifecycle, release process, index process,
   three-file scope, and authority ceiling remain unchanged.
8. The recovery selector is closed and every uncertain state fails closed.
9. Contract acceptance grants no implementation, comment, release, R0,
   process, dispatch, Stage-4, submission, merge, deployment, or readiness
   authority.

## Remaining Unknowns

- The exact local command construction that removed the quotation marks is not
  durably available. This contract does not need or invent that transcript.
- The real GitHub transport is not exercised during contract review. It
  remains a separately owner-authorized future operation guarded by exact
  request-wrapper and response-readback checks.

Neither unknown permits repair or reuse of the historical attempt.

## Next Workflow Action

Next role: Codex E, independent terminal-receipt recovery contract reviewer.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent R0 Terminal-Receipt Recovery Contract Reviewer.

Repository: Tahjali11/Mythic-Edge
Issue: https://github.com/Tahjali11/Mythic-Edge/issues/771
Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/746
Branch: codex/role-pool-r0-terminal-receipt-recovery-771

Review only:
docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md

Use the exact SHA-256 from the Codex B handoff. Independently refetch issue
#771 comments 5139550089, 5139572911, and 5139603966. Verify that the last is
an unedited 861-byte non-JSON body with SHA-256
482e14a2acb0e69b7bdf97b2d45c4287cd3e0a0f8cf6dad6a9cbb6e2169f91b5,
while the mechanically derived intended canonical body is 907 bytes with
self-digest bf74dc0e0ae70d6aca26b3a7831b3a1b5bf951c86772954990c05bd78c5f9371
and artifact SHA-256
850f51628bd6aec24b69698d7bbac7d7c707821141622442d9e69b864d5a823c.

Confirm CP-03, r0_bootstrap_consumption_ambiguous, permanent nonreuse, no
historical repair, absent release state, unchanged index, issue #769 with zero
comments, and no repository changes from C.

Reproduce the 906-byte receipt to 964-byte API-wrapper KAT and wrapper SHA-256
f1a817216a8379fe1906540b24fbc7c4537f7a7463ac75ffd5318521766d6f1e.
Review the direct non-shell binary-stdin transport, exact-body reconciliation,
related-malformed detection, no-retry rules, fresh-decision separation, and
524-tuple/13-row selector audit with overlap, uncovered, and unreachable
counts all zero.

Run every contract-required repository and safety gate without posting,
editing, or deleting comments or creating release state. Confirm this one
contract is the only changed path.

If and only if no blocker remains, create:
docs/contract_test_reports/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md

Acceptance permits only contract submission/integration routing. Fresh
eligibility and a distinct owner decision remain ineligible until integration.
End with a workflow_handoff to separately approved Codex F.
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
    - "GitHub consumption evidence"
    - "release-state authority"
    - "current-authority index"
    - "R0-R8 and Stage 4 authority"
  authority_conflicts_found: false
  authority_conflict_notes: "This is the same active #771 lane returning from a terminal fail-closed C attempt. PRs #374 and #391 are unrelated."
  stop_conditions:
    - "public comment or repository binding drift"
    - "historical comment edit, deletion, or duplicate related marker"
    - "issue #769 receives a top-level comment"
    - "release-state destination appears"
    - "scope beyond this one contract"
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/771"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/746"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/771#issuecomment-5139603966"
  target_artifact: "docs/contracts/role_pool_trusted_owner_r0_release_state_terminal_receipt_recovery.md"
  risk_tier: "high"
  base_branch: "origin/main"
  target_branch: "unselected_pending_submission_authority"
  branch: "codex/role-pool-r0-terminal-receipt-recovery-771"
  finding_status:
    ME-RP-771-C-002: "terminal_recovery_contract_authored_review_pending"
  historical_lifecycle_result: "r0_bootstrap_consumption_ambiguous"
  historical_owner_decision_status: "consumed_nonreusable"
  canonical_consumption_receipt_created: false
  release_state_created: false
  r0_accepted: false
  owner_implementation_decision_eligible: false
  stage4_authorized: false
  live_ready: false
  validation:
    - "historical comment and intended canonical body comparison"
    - "906-to-964-byte binary transport KAT"
    - "524-tuple, 13-row selector audit 0/0/0"
    - "R0 checker and focused release validation"
    - "agent-doc and path-scoped safety checks"
  stop_conditions:
    - "binding drift or historical comment mutation"
    - "release-state or index mutation"
    - "scope beyond the one contract"
  next_recommended_role: "Codex E: independent terminal-receipt recovery contract reviewer"
```
