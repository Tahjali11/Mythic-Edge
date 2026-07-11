# Core Frontend API Client Residual Decomposition Decision Packet

Status: Revised draft contract for independent re-review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/732>

Parent residual queue: <https://github.com/Tahjali11/Mythic-Edge/issues/715>

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Target artifact:
`docs/contracts/core_frontend_api_client_residual_decomposition_decision_packet.md`

## Module

`core_frontend_api_client_residual_decomposition_decision_packet`

This contract decides the smallest coherent response-validation boundary that
remains inside `frontend/src/api.ts` after issue #695 and PR #696 completed the
first frontend API client decomposition.

Plain English: `frontend/src/api.ts` must remain the one stable API facade used
by the rest of the frontend. A later implementation may place one small,
private response validator family behind that facade, but it must not change
what is fetched, when it is fetched, what is accepted or rejected, which error
is raised, or what callers import.

This is a planning contract only. It does not authorize implementation, file
movement, ARS or Refactor Scout execution, source mutation, API behavior
changes, frontend behavior changes, or readiness or assurance claims.

## Source And Binding

- Repository: `Tahjali11/Mythic-Edge`
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/732>
- Parent residual queue: <https://github.com/Tahjali11/Mythic-Edge/issues/715>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Original decision issue: <https://github.com/Tahjali11/Mythic-Edge/issues/693>
- Original decision PR: <https://github.com/Tahjali11/Mythic-Edge/pull/694>
- First decomposition issue: <https://github.com/Tahjali11/Mythic-Edge/issues/695>
- First decomposition PR: <https://github.com/Tahjali11/Mythic-Edge/pull/696>
- First decomposition merge commit:
  `19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548`
- Inspected `origin/main` commit:
  `ea7bda2466bd78fa35a0529fa46a65cc7fb3a569`
- Inspected `frontend/src/api.ts` blob:
  `854d692fabc17075ce9c609f67100f8ba02f115c`
- Inspected `frontend/src/api.test.ts` blob:
  `62ecce496f018a76adf20bdcb5dcc6760d1c0c24`
- Candidate ID: `frontend_api_response_validation_residual`
- Selected child ID:
  `frontend_api_match_journal_response_validation`

If the target commit or either bound blob changes before a later evidence or
implementation pass, that pass must stop, classify the change, and refresh the
decision or evidence binding. A clean rebase alone does not prove that the
validator family is unchanged.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #732
- issue #715
- issues #693 and #695
- PRs #694 and #696
- `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`
- `docs/implementation_handoffs/core_frontend_api_client_boundary_decomposition_comparison.md`
- `frontend/src/api.ts`
- `frontend/src/api/errors.ts`
- `frontend/src/api/paths.ts`
- `frontend/src/api/request.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/types.ts`
- `frontend/package.json`
- Automation Artifacts issue #148 and its closeout comment

No private logs, local app data, SQLite contents, JSONL payloads, workbook
exports, runtime files, generated artifacts, secrets, credentials, endpoint
values, ARS output, or Refactor Scout output were read or created.

## Completed-Boundary Reconciliation

### Observed

Issue #695 and PR #696 are complete. Their merged boundary extracted:

- API error classes to `frontend/src/api/errors.ts`;
- endpoint paths to `frontend/src/api/paths.ts`; and
- loopback base-URL validation and request-guard transport helpers to
  `frontend/src/api/request.ts`.

`frontend/src/api.ts` still imports those private modules and re-exports the
same public errors and request helpers. It remains the stable public facade.
The current residual consists of public fetch/control orchestration plus
private response validators and type guards.

### Contract decision

The #695/#696 boundary is closed and must not be reopened. This packet does
not reconsider ownership of errors, paths, base-URL validation, request-guard
fetching, request-guard caching, or guarded mutating transport.

Any future implementation that moves those responsibilities again, changes
their interface, or bypasses them is outside this contract and must stop.

## Owning Layer And Truth Boundary

Primary area: Local App / frontend API bridge.

- Backend routes own their response payloads and lifecycle behavior.
- `frontend/src/types.ts` owns the current TypeScript constants and declared
  response shapes.
- `frontend/src/api.ts` owns the stable browser API facade, fetch sequencing,
  response parsing, strict validation calls, and safe API error mapping.
- Private validator modules may later own implementation details of validation
  only when called through the facade.
- Match Journal backend and persistence layers own journal behavior and journal
  records.
- Parser/state owns parser truth.
- Analytics owns only its contracted deterministic calculations and storage.

Frontend validation proves only that a response matches the currently expected
frontend contract. It does not prove parser correctness, Match Journal truth,
security, privacy, availability, or production readiness.

## Candidate Family Assessment

The following comparison is a contract decision, not implementation authority.

| Candidate family | Observed shape | Dependency/blast-radius assessment | Decision |
| --- | --- | --- | --- |
| Local-app and live status | Multiple top-level validators plus many nested heartbeat, process, lifecycle, diagnostics, and safety guards | High protected-surface and status-semantics contact | Defer |
| Analytics | Multiple envelope validators, row validators, dashboard validators, history summaries, card shapes, and safe-label guards | Largest and most interconnected validation family | Defer |
| Manual import | Job, adapter, quality, routing, source-artifact, and privacy validation | Import and private-artifact boundary is broader than the first child | Defer |
| Error report | Preview and external-submission validators plus status guards | Small, but directly security/privacy and external-write adjacent | Defer |
| Match Journal | One response validator, one private status guard, one required-field tuple | Smallest coherent domain family | Select |
| Shared primitives | Generic record, array, nullable, numeric, timestamp, and closed-label predicates used across domains | Genuinely shared; moving the whole family would touch every validator | Defer broad extraction; allow only two exact supporting leaves as described below |

## Selected Smallest Residual

Selected family:
`frontend_api_match_journal_response_validation`.

The family consists exactly of:

- `REQUIRED_MATCH_JOURNAL_FIELDS`;
- `validateMatchJournalResponse`; and
- `isMatchJournalStatus`.

These three definitions are domain-owned and must move together if a later
reviewed implementation is authorized. Moving only the validator while leaving
its closed status vocabulary behind would split one invariant across modules.

The following Match Journal responsibilities must remain in
`frontend/src/api.ts` during the first child:

- `fetchMatchJournal`;
- all public Match Journal submission functions;
- `postMatchJournal`;
- `parseMatchJournalResponse`;
- URL/query construction;
- calls to `guardedFetch`;
- `Response.json()` timing and failure mapping;
- `response.ok` handling; and
- the check that a non-OK journal envelope contains an error code.

This boundary keeps request orchestration and HTTP response semantics on the
facade while making only the pure payload validator private.

## Private Module Shape

After independent review, fresh scoped evidence, and a separately authorized
implementation child, the preferred same-repo private shape is:

```text
frontend/src/api.ts                              stable public facade
frontend/src/api/validation/primitives.ts       private shared leaf
frontend/src/api/validation/match_journal.ts    private domain validator
```

The exact filenames may be adjusted by a later reviewed implementation only
if the ownership and import direction remain identical.

Allowed import direction:

```text
frontend/src/api.ts
  -> frontend/src/api/validation/match_journal.ts

frontend/src/api/validation/match_journal.ts
  -> frontend/src/api/validation/primitives.ts
  -> frontend/src/api/errors.ts
  -> frontend/src/types.ts

frontend/src/api.ts
  -> frontend/src/api/validation/primitives.ts
```

The facade may also import the same primitive leaf for validators that remain
in `api.ts`. The private validator module must not import `frontend/src/api.ts`.
That prohibition prevents a circular import, meaning two modules loading each
other while they are still being initialized.

No caller outside `frontend/src/api.ts` may import the private Match Journal
validator. No new package export or barrel export may expose it.

The dependency edges above preserve existing authority:

- `MatchJournalApiError` remains defined and publicly re-exported from the
  already completed `frontend/src/api/errors.ts` boundary;
- `MATCH_JOURNAL_OBJECT`, `MATCH_JOURNAL_SCHEMA_VERSION`,
  `MatchJournalResponse`, and `MatchJournalStatus` remain defined by
  `frontend/src/types.ts`; and
- `isRecord` and `isStringArray` remain generic private validation primitives.

The future private validator may import those exact existing authorities. It
must not copy, rename, wrap, re-declare, re-export, or change ownership of the
error class, constants, types, or primitive semantics. `errors.ts` and
`types.ts` must not import the private validator or primitive leaf.

## Validator And Type-Guard Ownership

### Domain-owned and moved together

- `REQUIRED_MATCH_JOURNAL_FIELDS`
- `validateMatchJournalResponse`
- `isMatchJournalStatus`
- Match Journal-specific error messages embedded in the validator

Only `validateMatchJournalResponse` needs to be exported from the private
domain module. The required-field tuple and status guard remain private to that
module.

### Genuinely shared

- `isRecord`
- `isStringArray`

Those predicates are used by multiple response families and must not become
Match Journal-owned. A later implementation of the selected child may move
exactly those two existing predicates, unchanged, into the private primitive
leaf so both the facade and Match Journal validator can import them.

The child must not:

- duplicate their logic inside the Match Journal module;
- pass them through a dependency-injection object;
- export them from the public `frontend/src/api.ts` facade;
- move additional generic predicates opportunistically; or
- alter null, array, object, prototype, or element-type semantics.

Moving these two predicates is supporting work for an acyclic private module,
not a separate domain decomposition and not permission to reorganize all
validation helpers.

## Public Facade Preservation Contract

`frontend/src/api.ts` remains the only stable public API import path.

A later implementation must preserve:

- every current public function name and signature;
- every current public error-class export;
- `getApiBaseUrl` and `resetLocalRequestGuardForTests` exports;
- the import behavior used by `frontend/src/App.tsx`, tests, and private app
  components;
- Match Journal request and response types from `frontend/src/types.ts`;
- all current endpoint paths and HTTP methods;
- all current request headers, request bodies, and query serialization;
- local request-guard acquisition and header use for mutating calls; and
- the absence of any public validator export.

No direct consumer import from `frontend/src/api/validation/*` is permitted.
Tests must exercise the validator through the existing facade functions rather
than making the private module a de facto public interface.

## Exact Behavior-Preservation Requirements

The selected child is behavior-preserving only. It must preserve all of the
following exactly:

1. Non-object payloads raise `MatchJournalApiError` with code
   `malformed_response` and the existing safe message.
2. Missing required fields raise the existing `malformed_response` code and
   message.
3. A schema-version mismatch raises `incompatible_response` with the existing
   schema message.
4. An unsupported object name raises the existing `malformed_response` code
   and message.
5. Status accepts exactly `ok`, `degraded`, `empty`, `missing`, `unavailable`,
   and `error`.
6. `result` must remain a JSON-object-shaped record.
7. `warnings` and `errors` must remain arrays whose every element is a string.
8. The accepted payload is returned without cloning, normalization, defaulting,
   filtering, relabeling, or field reordering.
9. Malformed JSON is still mapped by `parseMatchJournalResponse` before domain
   validation.
10. A non-OK response with a valid envelope and at least one error still
    resolves to that envelope.
11. A non-OK response with no error code still raises the current safe
    malformed-response error after validation.
12. Fetch calls, guard acquisition, request order, and response parsing happen
    in the same sequence.

No new coercion, permissive optional field, recursive validation, safe-label
rule, schema rule, or stronger result-shape check may be added in this
decomposition. A validator improvement requires a separate behavior-changing
issue and contract.

## Error And Privacy Boundary

Errors must remain symbolic and public-safe. The implementation and tests must
not include or echo:

- raw response payloads;
- raw JSON text;
- local paths;
- Player.log content;
- JSONL content;
- SQLite data;
- request-guard values;
- secrets, credentials, tokens, API keys, webhook URLs, or environment values;
- stack traces or arbitrary exception text; or
- private Match Journal note or label content.

Test payloads must remain synthetic. Rejection tests must assert safe error
class, code, and message behavior without snapshotting raw payloads.

## Fresh Evidence Decision

Decision: `fresh_scoped_evidence_required_before_implementation`.

Automation Artifacts issue #148 closed as overtaken after #695/#696 proceeded
under an owner exception. Its closeout explicitly records that no ARS or
Refactor Scout evidence artifact was produced or merged. It therefore cannot
be reused as retained evidence for the post-#696 residual.

Before any later implementation-precondition review is routed, a new retained
scoped evidence packet must bind all of:

- issue #732;
- target commit;
- `frontend/src/api.ts` blob;
- candidate ID `frontend_api_response_validation_residual`;
- selected child ID `frontend_api_match_journal_response_validation`;
- the Match Journal validator family listed above;
- the two supporting shared predicates;
- the stable-facade and no-behavior-change boundaries; and
- an explicit single-use or otherwise bounded lifecycle status required by
  the owning evidence repository.

Fresh evidence may support review of the boundary. It does not authorize code,
file moves, source mutation, a PR, or any readiness or assurance claim.

The issue #732 v1 route does not permit an owner-exception bypass. A generic or
exact owner instruction to continue, decompose `api.ts`, waive evidence, or
reuse prior evidence is not evidence and cannot satisfy this packet. If the
owner later wants an exception route, Codex A must create a new problem
representation and Codex B must version this schema after a separately
reviewed durable lifecycle design. This v1 packet remains fail-closed until
retained matching evidence exists.

## Evidence And Owner-Exception Projection

The ARS/Refactor evidence object inherits every required field and allowed
status from the shared Phase 5 contract. This extension adds three closed
lineage fields:

- `actual_tool_evidence_result_ref`: a repo-relative retained ARS/Refactor
  result reference, or the exact string `none`;
- `evidence_lineage_issue_ref`: the public issue that routed or closed the
  evidence lane, or `none`; and
- `evidence_lineage_status`: exactly one of `retained_result_available`,
  `overtaken_without_retained_result`, `no_lineage_issue`, or
  `review_required`.

Current projection:

```yaml
ars_refactor_evidence_status:
  prior_ars_evidence_found: "no"
  prior_refactor_scout_evidence_found: "no"
  reviewed_repo: "none"
  reviewed_scope: "none"
  reviewed_commit: "none"
  ars_version_contract_bundle: "none"
  current_target_commit: "ea7bda2466bd78fa35a0529fa46a65cc7fb3a569"
  relevant_changes_since_review: "not_applicable"
  evidence_status: "fresh_scoped_evidence_required_before_implementation"
  fresh_scoped_evidence_needed: "yes"
  reason: "Issue #148 closed as overtaken without a retained ARS or Refactor Scout result for the post-#696 residual."
  actual_tool_evidence_result_ref: "none"
  evidence_lineage_issue_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/148"
  evidence_lineage_status: "overtaken_without_retained_result"
```

Issue, approval, exception, or implementation lineage is never a tool-result
reference. `actual_tool_evidence_result_ref: none` cannot be replaced by an
issue URL, owner comment, lifecycle claim, or planned evidence path.

### Owner-exception route

The closed v1 projection is:

```yaml
owner_exception_route: "unsupported_v1"
owner_exception_ref: "none"
owner_exception_lifecycle_status: "not_applicable"
owner_exception_recognized_as_evidence: false
owner_exception_authorizes_implementation: false
owner_exception_authorizes_file_move: false
```

These are the only valid values. Any missing, non-`none`, unknown,
caller-overridden, prose-contradicted, approval-like, consumed, replayed,
expired, or otherwise attempted exception value fails closed to
`final_decision: review_required`, preserves
`fresh_scoped_evidence_needed: yes`, and preserves
`ready_for_codex_c: false`. V1 has no exception consumption transition because
v1 recognizes no exception. This removes caller-asserted lifecycle state and
replay ambiguity rather than treating either as authority.

## Phase 5 Schema Extension

This packet is not a direct instance of
`core_governance_report_helper_phase_5_decomposition_decision_packet.v1`.
That base schema is limited to `governance_report_helper_only` and defers the
API/frontend/live-capture lane. This contract defines the issue-specific,
versioned extension:

`core_frontend_api_client_residual_decomposition_decision_packet.v1`.

Extension scope:
`frontend_api_response_validation_residual_only`.

Inherited without change:

- the shared decision vocabulary;
- the complete ARS/Refactor evidence fields and evidence statuses;
- same-repo-first and cross-repo rejection rules;
- candidate-row dependency, consumer, interface, testing, rollback, and
  non-claim requirements;
- false-authority semantics; and
- fail-closed handling.

Overridden or extended fields:

| Field | Extension rule |
| --- | --- |
| `packet_schema` | Uses the issue-specific extension literal, not the base literal. |
| `schema_extension_scope` | Exactly `frontend_api_response_validation_residual_only`. |
| `candidate_scope` | Exactly `match_journal_response_validation_only`. |
| `candidate_surface_class` | Adds exactly `frontend_api_response_validation_surface`. |
| `candidate_surface_kind` | Adds exactly `frontend_match_journal_response_validator_family`. |
| `api_frontend_live_capture_deferred` | Exactly `false` because this extension is the already-routed frontend API residual lane. This does not activate runtime behavior. |
| `selected_child_id` | Exactly `frontend_api_match_journal_response_validation`. |
| `completed_boundary_status` | Exactly `closed_preserve`. |
| `same_repo_child_assessment` | Non-authoritative assessment defined below; never a decision. |
| Evidence lineage fields | Adds the three closed fields above. |
| Owner-exception fields | Adds the closed `unsupported_v1` projection above; no bypass or lifecycle transition exists. |

For `candidate_surface_class: frontend_api_response_validation_surface`, the
allowed `final_decision` values are only
`request_fresh_ars_refactor_evidence`, `request_scope_split_child`, `defer`, or
`review_required`. The current evidence projection requires exactly
`request_fresh_ars_refactor_evidence`.

`same_repo_child_assessment` may be only
`preferred_after_required_evidence_and_separate_authority` or
`not_assessed`. It is architectural advice and cannot authorize implementation
or substitute for `final_decision`.

## Complete Phase 5 Extension Envelope

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
base_schema_direct_instance: false
packet_schema: "core_frontend_api_client_residual_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_frontend_api_client_residual_decomposition_decision_packet.md"
schema_extension_scope: "frontend_api_response_validation_residual_only"
repository: "Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/732"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
parent_residual_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
target_commit: "ea7bda2466bd78fa35a0529fa46a65cc7fb3a569"
candidate_scope: "match_journal_response_validation_only"
phase_5_order_preserved: true
eventbus_support_deferred: true
api_frontend_live_capture_deferred: false
parser_state_deferred: true
implementation_authorized: false
file_move_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
readiness_claimed: false
truth_or_assurance_claimed: false
review_required: true
ready_for_codex_c: false
```

## Canonical Candidate Row

The packet has exactly one candidate row and exactly one authoritative
decision field:

```yaml
candidate_id: "frontend_api_response_validation_residual"
selected_child_id: "frontend_api_match_journal_response_validation"
candidate_surface_class: "frontend_api_response_validation_surface"
candidate_surface_kind: "frontend_match_journal_response_validator_family"
current_path: "frontend/src/api.ts"
current_behavior: "The stable frontend API facade owns request orchestration and private domain response validation; the selected residual is the Match Journal response validator family."
truth_or_authority_owner: "frontend/src/api.ts facade for orchestration; frontend/src/api/errors.ts for MatchJournalApiError; frontend/src/types.ts for Match Journal constants and types; Match Journal backend for journal behavior"
upstream_dependencies:
  - "frontend/src/api/errors.ts"
  - "frontend/src/types.ts"
  - "frontend/src/api/request.ts"
  - "frontend/src/api/paths.ts"
downstream_consumers:
  - "frontend/src/App.tsx through frontend/src/api.ts"
  - "frontend/src/api.test.ts through frontend/src/api.ts"
protected_surface_contact: "mixed_review_required"
proposed_destination: "private same-repo validation modules behind frontend/src/api.ts after required evidence and separate implementation authority"
why_not_keep_local: "The selected family is a coherent private validation unit whose later extraction could reduce facade responsibility while retaining all orchestration and public imports on the facade."
why_not_move_to_existing_repo: "The validator is coupled to Core local-app response constants, errors, and tests and has no reviewed cross-repository interface."
why_not_create_new_repo: "A new repository would add versioning and authority drift for a private same-repo implementation detail."
new_public_interface_needed: "private_same_repo"
new_public_interface_description: "Only frontend/src/api.ts may import the private Match Journal validator; no caller-facing export is added."
behavior_preservation_tests:
  - "focused facade-level Match Journal accepted and rejected payload tests"
  - "request path, guard, payload, response, and exact safe-error tests"
  - "full frontend tests, typecheck, and build"
rollback_plan: "Restore the validator family and two exact shared predicates to frontend/src/api.ts, remove only new private validation modules/imports, preserve #695/#696 modules, and rerun focused/full frontend validation."
same_repo_child_assessment: "preferred_after_required_evidence_and_separate_authority"
ars_refactor_evidence_status:
  prior_ars_evidence_found: "no"
  prior_refactor_scout_evidence_found: "no"
  reviewed_repo: "none"
  reviewed_scope: "none"
  reviewed_commit: "none"
  ars_version_contract_bundle: "none"
  current_target_commit: "ea7bda2466bd78fa35a0529fa46a65cc7fb3a569"
  relevant_changes_since_review: "not_applicable"
  evidence_status: "fresh_scoped_evidence_required_before_implementation"
  fresh_scoped_evidence_needed: "yes"
  reason: "Issue #148 closed as overtaken without a retained ARS or Refactor Scout result for the post-#696 residual."
  actual_tool_evidence_result_ref: "none"
  evidence_lineage_issue_ref: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/148"
  evidence_lineage_status: "overtaken_without_retained_result"
owner_exception_route: "unsupported_v1"
owner_exception_ref: "none"
owner_exception_lifecycle_status: "not_applicable"
owner_exception_recognized_as_evidence: false
owner_exception_authorizes_implementation: false
owner_exception_authorizes_file_move: false
non_claims:
  - "not_implementation_authority"
  - "not_file_move_authority"
  - "not_ars_or_refactor_execution_authority"
  - "not_frontend_api_or_match_journal_behavior_change"
  - "not_parser_analytics_or_match_journal_truth"
  - "not_security_or_privacy_assurance"
  - "not_release_deploy_or_production_readiness"
final_decision: "request_fresh_ars_refactor_evidence"
```

There is no `candidate_decision` field. Unknown, missing, duplicate,
contradictory, placeholder, unsupported, or base-only validation of this
extension fails closed to `final_decision: review_required` and
`ready_for_codex_c: false`.

## Authorization And Non-Claims

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_repo_mutation_authorized: false
frontend_behavior_change_authorized: false
validator_behavior_change_authorized: false
public_facade_change_authorized: false
api_endpoint_change_authorized: false
request_method_change_authorized: false
request_payload_change_authorized: false
response_schema_change_authorized: false
request_guard_change_authorized: false
base_url_policy_change_authorized: false
fetch_sequence_change_authorized: false
safe_label_policy_change_authorized: false
backend_route_change_authorized: false
live_capture_behavior_change_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
analytics_truth_change_authorized: false
match_journal_truth_change_authorized: false
workbook_webhook_change_authorized: false
apps_script_change_authorized: false
ai_behavior_change_authorized: false
ci_change_authorized: false
deployment_change_authorized: false
production_behavior_change_authorized: false
private_evidence_read_authorized: false
readiness_claimed: false
decomposability_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
parser_truth_claimed: false
analytics_truth_claimed: false
match_journal_truth_claimed: false
release_readiness_claimed: false
production_readiness_claimed: false
```

## Codex E Finding Reconciliation

| Finding | Revision | Status for re-review |
| --- | --- | --- |
| `CT-732-E-001` | The complete non-base Phase 5 extension and single authoritative decision remain unchanged. | `fixed_state_preserved` |
| `CT-732-E-002` | Preserved the complete evidence projection and removed the owner-exception bypass from v1. The only owner-exception state is `unsupported_v1`; any attempted exception fails closed and fresh retained evidence remains mandatory. | `revised_ready_for_confirmation` |
| `CT-732-E-003` | The complete private import graph and ownership prohibitions remain unchanged. | `fixed_state_preserved` |

These revisions do not authorize evidence execution, an exception,
implementation, file movement, or Codex C.

## Future Validation Plan

### Evidence and precondition validation

Before implementation, a later role must verify:

- issue #732 remains open and owns the same candidate;
- #695/#696 remain completed and are not being reopened;
- the target branch is based on current `origin/main`;
- the target commit/blob binding is current or has been explicitly refreshed;
- fresh scoped evidence exists as a retained, current, matching-scope result;
- the implementation issue explicitly authorizes the selected child and two
  supporting predicates; and
- the worktree contains no unrelated changes in the target files.

### Focused frontend validation

A later implementation must add or preserve focused facade-level tests for:

- every accepted Match Journal status literal;
- every rejected unknown status;
- non-object payload rejection;
- each missing required-field class;
- wrong schema and wrong object rejection;
- non-record `result` rejection;
- non-array and non-string-element warning/error rejection;
- malformed JSON mapping;
- non-OK envelope behavior with and without an error code;
- GET query serialization;
- all existing guarded POST route calls; and
- exact error class, code, and safe message behavior.

Required commands:

```powershell
npm --prefix frontend test -- --run src/api.test.ts
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
py tools/check_agent_docs.py
py tools/check_protected_surfaces.py --base origin/main
py tools/check_secret_patterns.py --all
git diff --check
```

The repo-wide secret/private scan may report known baseline findings. The later
handoff must also run path-scoped scans over every changed path and require zero
new forbidden findings and zero new warnings in the selected scope.

No browser smoke, backend test, parser test, analytics test, or live-capture
test is required solely for this private validator move unless the actual diff
touches those surfaces. If it does, the implementation has exceeded this
contract and must stop rather than broaden validation after the fact.

## Rollback Plan

Rollback must be one behavior-preserving revert of the selected child only:

1. Restore `REQUIRED_MATCH_JOURNAL_FIELDS`,
   `validateMatchJournalResponse`, and `isMatchJournalStatus` to their original
   locations in `frontend/src/api.ts`.
2. Restore `isRecord` and `isStringArray` to their original locations if the
   private primitive leaf was created solely by this child.
3. Remove only the new private validation modules and imports.
4. Preserve all #695/#696 modules, public exports, endpoint paths, request
   guards, and transport helpers.
5. Rerun the focused and full frontend validation commands.

Rollback must not retain compatibility wrappers, duplicate validators, new
public exports, or changed tests that mask facade drift. It must not revert
unrelated changes made after the implementation branch was created.

## Protected Surfaces

This docs-only contract references but does not modify:

- browser-to-loopback API validation;
- request-guarded local mutations;
- Match Journal response and write-route handling;
- live-capture status and controls;
- analytics response validation;
- parser truth and final reconciliation;
- workbook, webhook, and Apps Script transport;
- private/local artifact boundaries; and
- CI, deployment, and production behavior.

The highest implementation risk is silent acceptance/rejection drift at the
browser-to-local-backend boundary. The second risk is accidental creation of a
second public API import path. Both fail closed under this contract.

## Risk Tier

High overall; Medium-High for the selected future child.

The chosen family is small and private, but it sits on a mutating local API
surface and shares generic predicates with every remaining response family.
Mechanical movement therefore needs exact evidence, focused malformed-response
tests, full frontend validation, and independent review.

## Acceptance Criteria

- The completed #695/#696 boundary is recorded and preserved.
- Exactly one residual family is selected: Match Journal response validation.
- The validator, required-field tuple, and private status guard are treated as
  one domain-owned unit.
- `isRecord` and `isStringArray` are classified as shared and are not copied or
  made public.
- `frontend/src/api.ts` remains the stable public facade and HTTP orchestrator.
- Exact acceptance, rejection, error, request-guard, path, payload, and fetch
  sequencing behavior is frozen.
- Fresh scoped evidence is mandatory before any implementation child; v1 has
  no owner-exception bypass.
- The Phase 5 extension is complete, is explicitly not a direct base-schema
  instance, and carries exactly one authoritative final decision.
- The evidence projection mechanically distinguishes no retained result from
  issue lineage and marks owner exceptions unsupported in v1.
- The private import graph preserves existing error, type, constant, and
  primitive ownership without duplication or re-export.
- Focused and full frontend validation and a narrow rollback are specified.
- No implementation, move, ARS/Refactor run, protected behavior change, or
  readiness/truth/assurance claim is authorized.

## Stop Conditions

Stop and route back to Codex B, Codex A, or the owner if a later thread asks to:

- implement directly from this packet;
- skip fresh evidence, treat owner approval as evidence, or attempt an
  owner-exception bypass;
- move more than the selected validator family and two supporting predicates;
- import private validators from any caller other than `frontend/src/api.ts`;
- change accepted statuses, required fields, errors, response handling, paths,
  methods, payloads, guards, base URL policy, or fetch ordering;
- split `frontend/src/api.test.ts` as an independent goal;
- reopen errors, paths, or request-helper ownership from #695/#696;
- run broad ARS/Refactor analysis;
- read private or local artifacts; or
- claim decomposability, correctness, readiness, security, privacy, parser
  truth, analytics truth, Match Journal truth, or production readiness.

## Recommended Next Role

Codex E: independent contract reviewer.

If Codex E accepts this packet, route only to a separately authorized fresh
scoped ARS/Refactor evidence lane. Do not route to Codex C from contract
acceptance alone.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Contract Reviewer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/732

Parent residual queue:
https://github.com/Tahjali11/Mythic-Edge/issues/715

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/568
- https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_frontend_api_client_residual_decomposition_decision_packet.md

Review the decision packet independently. Lead with findings. Verify that it
preserves the completed #695/#696 boundary, selects exactly the Match Journal
response-validation family as the smallest child, moves its private status
guard with it, treats isRecord and isStringArray as shared private predicates,
keeps frontend/src/api.ts as the only stable public facade and HTTP
orchestrator, freezes exact rejection/error/request/fetch behavior, requires
fresh scoped evidence with no v1 exception route, and provides sufficient
focused/full validation and rollback requirements.

Confirm the fixed state of CT-732-E-001 and CT-732-E-003. Re-review the remaining
CT-732-E-002 lifecycle finding and verify that v1 now has no owner-exception
bypass, no consumption transition, no caller-asserted waiver, and no route
around mandatory retained matching evidence.

Do not implement or move code. Do not run ARS or Refactor Scout. Do not change
frontend, API, backend, live-capture, parser, analytics, Match Journal,
workbook/webhook/Apps Script, AI, CI, deployment, or production behavior. Do
not authorize Codex C from contract acceptance alone.

Output findings, verdict, validation, remaining risks, next role, and a
workflow_handoff block.
```

## Instruction Context

```yaml
instruction_context:
  role: "Codex B: Module Contract Writer"
  risk_tier: "High"
  repo_agents_read: true
  issue_or_tracker_read: true
  protected_surfaces:
    - "frontend browser-to-loopback response validation"
    - "local request-guarded Match Journal routes"
    - "public frontend API facade"
    - "parser and analytics truth boundaries"
    - "private and local artifact boundaries"
  authority_conflicts_found: false
  authority_conflict_resolution: "CT-732-E-001 through CT-732-E-003 revised for independent confirmation"
  implementation_authorized: false
  stop_conditions:
    - "no implementation or file movement"
    - "no ARS or Refactor Scout execution"
    - "no public facade or validator behavior change"
    - "no protected runtime, truth, transport, CI, or deployment change"
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/732"
  parent_residual_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  completed_source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/695"
  completed_source_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/696"
  completed_source_merge_commit: "19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548"
  completed_thread: "B_owner_exception_route_removal"
  next_thread: "E_contract_confirmation"
  branch: "codex/frontend-api-validation-residual-732"
  base_commit: "ea7bda2466bd78fa35a0529fa46a65cc7fb3a569"
  target_artifact: "docs/contracts/core_frontend_api_client_residual_decomposition_decision_packet.md"
  review_artifact: "docs/contract_test_reports/core_frontend_api_client_residual_decomposition_decision_packet.md"
  packet_schema: "core_frontend_api_client_residual_decomposition_decision_packet.v1"
  base_schema_direct_instance: false
  schema_extension_scope: "frontend_api_response_validation_residual_only"
  candidate_id: "frontend_api_response_validation_residual"
  selected_child_id: "frontend_api_match_journal_response_validation"
  selected_family: "Match Journal response validator, required-field tuple, and private status guard"
  completed_boundary_status: "closed_preserve"
  candidate_surface_class: "frontend_api_response_validation_surface"
  same_repo_child_assessment: "preferred_after_required_evidence_and_separate_authority"
  final_decision: "request_fresh_ars_refactor_evidence"
  actual_tool_evidence_result_ref: "none"
  evidence_lineage_status: "overtaken_without_retained_result"
  owner_exception_route: "unsupported_v1"
  owner_exception_ref: "none"
  owner_exception_lifecycle_status: "not_applicable"
  fresh_scoped_evidence_needed_before_implementation: true
  public_facade: "frontend/src/api.ts"
  risk_tier: "High overall; Medium-High selected child"
  ready_for_codex_c: false
  implementation_authorized: false
  file_move_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  frontend_behavior_change_authorized: false
  validator_behavior_change_authorized: false
  public_facade_change_authorized: false
  api_payload_or_endpoint_change_authorized: false
  request_guard_change_authorized: false
  backend_or_live_capture_change_authorized: false
  parser_or_analytics_truth_change_authorized: false
  match_journal_truth_change_authorized: false
  workbook_webhook_apps_script_change_authorized: false
  ai_ci_deployment_production_change_authorized: false
  readiness_claimed: false
  decomposability_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  forbidden_scope_touched: false
  finding_status:
    CT-732-E-001: "fixed_state_preserved"
    CT-732-E-002: "revised_ready_for_confirmation"
    CT-732-E-003: "fixed_state_preserved"
```
