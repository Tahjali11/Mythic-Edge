# Release Remediation Matrix

This is the exact traceability ledger for all 30 packet entries. It preserves
the reconciler classification vocabulary: 19 `confirmed`, 8 `duplicate`, two
`accepted risk`, and one `requires behavioral experiment`. There are no
`unsupported` entries. Duplicate rows point to the same enforced root so no
packet observation disappears.

Passing `scripts/run_release_tests.py` proves only the offline deterministic
gate. It does not prove runtime receipts or the required behavioral canaries.
Its in-process Python guard is a trusted-code regression aid, not a security or
isolation boundary. Any untrusted executable/script or live behavioral proof
requires a separately verified external OS-enforced read-only/no-network
boundary around its execution component.

| Packet finding ID | Classification | Severity | Consolidated root | Remediation and deterministic regression |
| --- | --- | --- | --- | --- |
| MEPOOL-RC-001 | confirmed | high | RC-H02 | Readiness-only pooled G; exact G plan/result gates and no integration action tests |
| MEPOOL-RC-002 | confirmed | high | RC-H01 | Implicit invocation disabled; exact request hash, conservative normalizer, role/verb binding tests |
| MEPOOL-RC-003 | confirmed | high | RC-H03 | Strict v3 required/unknown fields, typed role evidence/results, deletion tests |
| MEPOOL-RC-004 | confirmed | high | RC-H04 | Exact per-role action sets, file paths, output transitions, and scope regressions |
| MEPOOL-RC-005 | confirmed | high | RC-H03 | Narrowed duplicate symptom; strict typed state and result binding cover it |
| MEPOOL-RC-006 | confirmed | high | RC-H08 | Exact named-repository full-read derivation, request/repository provenance, lane-consumption manifests, unlisted-read denial, and no-echo tests |
| MEPOOL-RC-007 | confirmed | high | RC-H07 | Central claim, refreshed winner proof, canonical reservations, and idempotency tests |
| MEPOOL-RC-008 | duplicate | high | RC-H07 | Same claim/reservation root and regressions as MEPOOL-RC-007 |
| MEPOOL-RC-009 | confirmed | high | RC-H12 | Strict lane result, handoff, journal, digest, and fallback-causality tests |
| ME-RC-01 | confirmed | high | RC-H06 | Independent discovery/worktree observations bind inventory, candidates, scopes, active waves, and physical identity |
| ME-RC-02 | confirmed | high | RC-H05 | WIP-1 slot ownership plus typed, scoped, current, durable exceptions |
| ME-RC-03 | duplicate | high | RC-H12 | Same typed-result and recovery root as MEPOOL-RC-009 |
| ME-RC-04 | confirmed | high | RC-H12 | Exact journal order, unique logical intent, receipt/key binding, and no automatic retry |
| ME-RC-05 | duplicate | high | RC-H03 | Same strict schema and role-contract root as MEPOOL-RC-003 |
| ME-RC-06 | duplicate | high | RC-H07 | Same claim identity and winner-readback root as MEPOOL-RC-007 |
| ME-RC-07 | confirmed | high | RC-H07 | Released/lost/expired claims cannot win; slot and every-lane winner proofs are required |
| ME-RC-08 | confirmed | medium | RC-M02 | Lease expiry is separated from fresh runtime; expired unlaunched reservations fail |
| ME-RC-09 | confirmed | high | RC-H12 | Causal wave/lane/result matrices and exact A-G next-role routing |
| ME-RC-10 | confirmed | high | RC-H13 | F publication and G readiness bind exact plans plus independent Git/PR outcome readbacks |
| ME-RC-11 | confirmed | high | RC-H07 | Unique per-lane reservation receipts, comment IDs, keys, and preclaim/prelaunch freeze |
| ME-RC-12 | accepted risk | low | RC-L01 | Deterministic oldest/tie fairness is enforced; human policy quality remains reviewable |
| MRP-RC-001 | accepted risk | high | RC-H09 | `codex:exec-single-start/v2` requests `gpt-5.6-sol`/`max` only when locally advertised, otherwise omits both preferences and records nullable actual-request fields; full launcher preflight, selected executable, minimal child environment, and strict receipt bindings are enforced while effective model/effort readback remains advisory and non-blocking |
| MRP-RC-002 | confirmed | high | RC-H09 | Strict local preflight, exact executable/argument/packet bindings, and direct-launcher single-start regressions remain offline controls; direct Popen is now machine-rejected for production, while `external-isolation-broker.md` requires broker-owned creation plus verifier-held reservation and boundary-ready/start/terminal-or-abort receipts before Stage 4 or live use |
| MRP-RC-003 | requires behavioral experiment | high | RC-H10 | Raw hostile text omitted from normal packets; a strict standalone exception permits only the malicious fresh-agent canary needed to collect closure evidence |
| MRP-RC-004 | confirmed | high | RC-H11 | Canonical lower-case dependencies/contracts/protected/external state and derived overlap/order tests |
| MRP-RC-005 | duplicate | high | RC-H12 | Same typed-result, journal, and recovery root as MEPOOL-RC-009 |
| MRP-RC-006 | duplicate | high | RC-H07 | Same exclusive claim/reservation root as MEPOOL-RC-007 |
| MRP-RC-007 | duplicate | high | RC-H05/RC-H13 | WIP enforcement plus exact F/G publication/readiness binding cover both roots |
| MRP-RC-008 | confirmed | medium | RC-M01 | Canonical executable fixtures, exact CLI sidecars, independent old-workflow pickup producer/verifier, documentation contract tests |
| MRP-RC-009 | duplicate | high | RC-H07 | Same refreshed claim winner and identity root as MEPOOL-RC-007 |

## Requirement-To-Enforcement Matrix

| Requirement | Enforcement | Evidence and remaining boundary |
| --- | --- | --- |
| Explicit action, role, and repository set | Deterministic | Exact request digest, conservative mode parser, compact or standalone exact repository bindings, named public/private read grants, and role/action equality tests; exceptional and mutating authority remains separate |
| Inventory, candidates, active waves, and worktrees | Deterministic structure plus runtime-observable source truth | Independent discovery/worktree sidecars bind exact identities; the collector receipt must still be verified on its authority surface |
| WIP-1 and exceptions | Deterministic | Slot-owner-only binding, exact scoped exception, current request or repository authority, expiry, and durable record tests |
| Launch configuration, context separation, and packet | Deterministic direct-launcher tests plus an unreviewed broker/verifier implementation candidate | Newest compatible executable, exact flags/arguments/hash/length, packet/script/attempt bindings, minimal environment, and content-free direct receipts remain tested offline and permanently non-live. Stage 4 and later live use require `codex:broker-single-start/v1`, verifier-held pre-create reservation, broker-owned atomic process creation, independently verifier-constructed boundary-ready/start/terminal-or-abort receipts, sole writable temp, controlled process tree, tool-network denial, control-plane separation, and credential/caller-profile denial. The successor preparation package implements the fixed producer and validators but is uninstalled, unprovisioned, and pending independent review; `gpt-5.6-sol`/`max` remains a non-blocking preference |
| Untrusted external text | Deterministic packet omission plus behavioral experiment | Normal renderer omits content; the exact-field Stage-4 exception is separate from pool plans and the fresh-agent malicious-content canary remains mandatory |
| Compatibility | Deterministic | The standalone `mythic_edge_role_pool_stage3_behavioral_planning.v1` contract binds the accepted Stage-2 pair, derives exact three-pair coverage for a synthetic three-repository/three-lane same-role proof, and fail-closes missing evidence, unlisted scope, dependency cycles, overlapping paths, shared contracts, protected surfaces, and external effects; the production v3 validator remains unchanged |
| Claims and reservations | Deterministic binding plus runtime-observable server truth | One central wave claim may repeat only as each lane's claim journal receipt; reservations and every lane-specific receipt remain unique, with slot-and-lane winner checks and exact preclaim freeze |
| Per-role actions and paths | Deterministic | Exact action, file, issue, role-evidence, transition, and journal operation sets |
| Result, handoff, receipts, and fallback | Deterministic | Typed result/handoff digests, unique typed receipts, causal journal-to-fallback mapping, old-workflow route tests, consumer-produced pickup bound to prompt/injection/consumer digests, and a fail-closed missing-pickup regression |
| F publication | Deterministic binding plus runtime-observable Git/GitHub truth | Typed accepted E review, all-passed head-bound validation, reviewed/staged file equality, commit/push/draft-PR receipts, and independent outcome readback |
| G readiness | Deterministic binding plus runtime-observable GitHub truth | No integration actions or waivers, exact checks/findings/scope state, independent readback, and condition-18 fallback for not-ready |

## Missing Deterministic Tests

No known original packet control lacks an offline deterministic regression.
Successful fallback injection without pickup now fails closed, and the positive
fixture requires a receipt produced by the old workflow's own hash-bound
ingress. This gate includes a complete positive synthetic
three-repository/three-lane same-role plan/result proof, a fake-only direct
single-start launcher suite, and deterministic broker/verifier candidate tests.
Those tests do not prove the installed Windows service/kernel boundary. The
broker schemas, client, process creation, fixed receipt protocol, lifecycle,
and adversarial tests exist only in the successor preparation package and
remain blocked on independent review, separate installation authority, and
current-service evidence.

The remaining required evidence includes broker implementation/review and the
staged runtime canary sequence, especially the fresh isolated malicious-content
experiment. `scripts/check_stage4_canary_exception.py` machine-checks the sole
evidence-collection exception without treating it as a pool plan, dispatch,
stage-advancement receipt, or finding-resolution receipt.
`scripts/check_stage3_behavioral_planning.py` separately validates the
zero-effect deterministic planning observation and review-ready pair bindings;
its effect counters remain assertions that independent review must confirm
against command and before/after operation evidence.

## Readiness Gates

- Inspect-only: eligible only for the exact two-repository Analytics/Corpus
  canary after the rebuilt offline gate passes; no third repository may be
  inferred or backfilled. Any live behavioral execution component must also
  have the independently verified external OS boundary required above.
- Stage-3 deterministic planning: eligible only through
  `mythic_edge_role_pool_stage3_behavioral_planning.v1`; two passing synthetic
  zero-effect observations go to independent review. Pair acceptance is
  separate from stage advancement and leaves `MRP-RC-003` unresolved.
- Stage-4 evidence collection: eligible only through a current, validated
  `MRP-RC-003` exception and an independently accepted implementation of
  `mythic_edge_role_pool_external_isolation_broker.v1`. Require one exact broker
  launch request and its reservation/boundary-ready/start/terminal-or-abort
  receipt chain. Direct
  Popen is non-live. The observation does not advance a stage or resolve the
  finding.
- Low-risk dispatch: not ready until stages 1-5 pass twice consecutively under
  independent review. Its first three-lane proof must use one shared role and
  may write only scheduling comments plus durable local role artifacts; commit,
  push, PR, and integration actions remain prohibited.
- F: not ready until every prior stage and the F canary pass twice.
- G: not ready until every prior stage and the readiness-only G canary pass
  twice.
- Live-ready: prohibited until all stages pass twice with no unresolved
  critical or high finding.

## Release Status

All original confirmed high, medium, and low packet findings retain their
offline deterministic controls and regressions. The accepted-risk rows cover
deterministic fairness policy and the explicit decision that model/effort
readback is non-blocking. The later process-ownership audit proved that the
direct Popen production claim cannot satisfy the external-boundary requirement;
the broker implementation candidate fail-closes that path but is not installed,
provisioned, or independently accepted.
`MRP-RC-003` cannot be closed by unit tests, and the standalone exception only
enables its evidence-gathering canary after the broker boundary exists. The
skill remains **not live-ready** until broker implementation/review and every
staged canary in `fallback-and-recovery.md` pass under their current contracts.
