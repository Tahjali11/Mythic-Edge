# Core Sanitized Parser-Fact Producer Boundary Review

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/731

## Contract

`docs/contracts/core_sanitized_parser_fact_producer_boundary.md`

## Cross-Repository Predecessor

- R&D issue: https://github.com/Tahjali11/Mythic-Edge-Research-and-Development/issues/21
- R&D PR: https://github.com/Tahjali11/Mythic-Edge-Research-and-Development/pull/22
- R&D merge commit: `951a9c11422758e76ac553a5ad466dafa40f0b05`

## Implementation Under Test

No implementation is under test. This is an independent docs-only contract
review on branch `codex/sanitized-parser-fact-producer-boundary-731` at Core
commit `d235bcfdc2e913e2305d81a6a86414ba6781918a`.

## Report Lifecycle

`report_lifecycle: final_approval`

## Findings

### CT-731-E-001 - P1 - Fixed-state follow-up

`finding_lifecycle: fixed_state_followup`

Original finding:

Availability mappings did not bind every absent, present, null, false,
contradictory, ineligible, withheld, and unsupported source state.

Verification evidence:

- The revised contract defines closed `single_row_availability` and
  `row_set_availability` reducers.
- Every R&D v1 availability key now has an exact match/game rule covering
  record-kind exclusion, missing physical rows, ineligible rows, cardinality
  conflicts, null or malformed required values, closed source statuses, and
  specialized boolean/count behavior.
- `withheld_private`, `not_yet_supported`, `not_applicable`, `not_observed`, and
  `unknown` remain distinct and cannot be caller-selected.

Derived:

The same contracted source state now has one deterministic availability result
or one fail-closed outcome. CT-731-E-001 is fixed and no longer blocking.

### CT-731-E-002 - P1 - Fixed-state follow-up

`finding_lifecycle: fixed_state_followup`

Original finding:

Mixed `final` and `reconciled` contributors were collapsed to `final`, erasing
the stronger reconciled provenance state.

Verification evidence:

- All contributing rows must now have one uniform finality.
- All-`final` emits `final`; all-`reconciled` emits `reconciled`.
- Any mixed final/reconciled linked family is blocked before construction as
  `blocked_mixed_source_finality`; dropping a contributor to hide the conflict
  is forbidden.
- The required synthetic matrix now includes uniform acceptance and mixed-family
  rejection.

Derived:

The revision preserves parser-owned finality without inventing a precedence
rule. CT-731-E-002 is fixed and no longer blocking.

### CT-731-E-003 - P1 - Fixed-state confirmation

`finding_lifecycle: fixed_state_followup`

Original finding:

The immutable package had no closed mechanism for later expiry, revocation,
supersession, deletion, incident invalidation, replay rejection, or current-state
observation.

Verification evidence:

- Package issuance and every append-only lifecycle record now fix both
  supersession references to exactly `none`.
- The profile-v1 status and reason vocabularies contain no supersession state or
  reason, the transition matrix contains no supersession row, and every
  supersession literal/reference is explicitly invalid.
- `effective_at_utc` cannot precede package approval and must be greater than or
  equal to the immediately prior record's effective time. The transition matrix
  separately forbids backdating.
- The permanent seal, immutable package, and sequence-1 `active_local` record
  become visible together only through one atomic compare-and-publish
  transaction. Exactly one concurrent transaction may succeed.
- Pre-commit failure leaves the seal unused and requires staged-object cleanup;
  post-commit failure never rolls the seal back; commit ambiguity fails closed
  to review until independently authorized recovery proves one complete
  pre-commit or post-commit state.
- The future synthetic test matrix now requires effective-time regression,
  every supersession value, atomic publication, concurrent single-winner,
  pre-commit rollback, ambiguous-commit, and permanent post-commit tests.

Derived:

The reciprocal first-write cycle has been removed rather than deferred to an
implementation choice, lifecycle time cannot regress, and publication has one
atomic visibility boundary. CT-731-E-003 is fixed and no longer blocking.

### CT-731-E-004 - P1 - Fixed-state confirmation

`finding_lifecycle: fixed_state_followup`

Original finding:

The disclosure screen omitted availability/provenance and used a subjective
"unusual combination" decision.

Verification evidence:

- The complete released-value vector still includes every availability value,
  provenance scalar, and canonical provenance list. Generalization, fixed-point
  family omission, one-way/two-way projections, complementary arithmetic, and
  rare-combination predicates remain deterministic.
- Profile v1 now permits exactly one issued package across all purposes,
  operators, source database instances, attempts, and time. Expiry, revocation,
  deletion, or abandonment never restores issuance eligibility.
- Any later generation attempt checks only the permanent seal before SQLite or
  private-source access and is rejected as
  `blocked_profile_release_already_issued` once issued.
- Missing, unreadable, duplicated, contradictory, or unknown seal state fails
  closed rather than being treated as unused.
- The package, seal, and lifecycle chain contain no source IDs, private
  membership hashes, source-derived membership index, or retained
  source-to-pseudonym mapping. The ephemeral map is destroyed after every
  attempt.
- Future tests must prove permanent rejection of every second profile-v1
  generation attempt before private access and absence of durable mapping state.

Derived:

The contract no longer requires unavailable prior source identity. The
permanent source-ID-free seal supplies an implementable, fail-closed profile-v1
cross-release boundary. CT-731-E-004 is fixed and no longer blocking.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-731-E-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Availability mappings did not bind all absent/null/boolean combinations. | Closed reducers and exhaustive per-key matrix at contract lines 510-562. | none |
| CT-731-E-002 | P1 | `fixed_state_followup` | fixed | not_blocking | Mixed final/reconciled contributors were collapsed to `final`. | Uniform finality and full-family mixed rejection at contract lines 276-280 and 572-580. | none |
| CT-731-E-003 | P1 | `fixed_state_followup` | fixed | not_blocking | Immutable package lacked later lifecycle closure. | Supersession is unsupported and rejected, effective times are nondecreasing, and seal/package/sequence-1 visibility is one atomic transaction with closed failure behavior. | none |
| CT-731-E-004 | P1 | `fixed_state_followup` | fixed | not_blocking | Disclosure screen omitted released provenance/availability and used subjective rarity. | Full-vector controls remain closed; one permanent source-ID-free profile seal prevents every second profile-v1 release before private access. | none |

## Contract Summary

The proposed Core producer would, under later separate authority, read an exact
allowlist of parser-normalized SQLite facts, sanitize them entirely inside
Core, and produce the R&D-owned `sanitized_parser_fact_local_dataset.v1`
interface. It must preserve parser truth/provenance while removing raw
identifiers, exact timestamps, card/deck content, private paths, and other
private material. Generation, transfer, and R&D access remain separate gated
operations.

## Internal Project Area Reviewed

`core_parser_and_runtime`, with a high-risk
`cross_repository_evidence_bridge`. Parser/state remains truth owner; SQLite is
only persistence, and the producer may own only the contracted sanitization and
lifecycle boundary.

## Bridge-Code Status Reviewed

No bridge code exists or is authorized. The contract describes a possible
future producer-side bridge only.

## Confirmed Contract Matches

- Core is the only selected v1 producer; R&D is not permitted to receive raw
  data for sanitization.
- The contract is bound to the merged R&D predecessor and current Core schema
  commit with no relevant schema drift.
- The migration's 31 tables are completely partitioned into 16 allowlisted and
  15 prohibited tables; allowlisted columns exist in migration `0001`.
- Dynamic discovery, `SELECT *`, arbitrary SQL, attached databases, extensions,
  and schema fallback are prohibited.
- Source rows must be final/reconciled, tied to completed approved ingest kinds,
  and internally consistent.
- CT-731-E-001 is fixed: availability reducers and the per-key matrix are
  exhaustive and preserve all closed missingness/privacy statuses.
- CT-731-E-002 is fixed: uniform finality is required and mixed linked families
  fail closed without relabeling parser provenance.
- CT-731-E-003 is fixed: lifecycle effective times are nondecreasing,
  supersession is unsupported and rejected throughout profile v1, and the
  permanent seal, package, and initial lifecycle row publish atomically.
- CT-731-E-004 is fixed: a permanent source-ID-free seal prevents every second
  profile-v1 release before SQLite/private access, including after expiry,
  revocation, or deletion.
- The revised lifecycle chain closes issuance, expiry, revocation, incident,
  deletion, replay/fork, and read-time current-state behavior.
- The revised disclosure screen covers the complete released vector and has
  deterministic generalization, fixed-point omission, projection, and
  complementary-disclosure rules.
- The R&D v1 package, record keys, vocabularies, and exact non-claim list are
  reproduced.
- Pseudonyms are random, release-local, non-derived, and held only in ephemeral
  producer memory.
- Exact source/gameplay timestamps are reduced to calendar quarter or duration
  buckets and cannot enter diagnostics.
- Card/deck/action detail and all linkage except release-local match-to-game
  linkage are prohibited.
- Unknown schema, fields, values, provenance labels, surfaces, and unsafe
  diagnostics fail closed.
- Generation and transfer/access require distinct later owner approvals.
- SQLite/private access, implementation, package generation/transfer, R&D
  access, Codex C, downstream activation, and truth/readiness/assurance claims
  remain false.

## Contract Mismatches

No remaining mismatch was found for CT-731-E-001 through CT-731-E-004. This
fixed-state verdict approves only the docs contract for submission. It does not
authorize implementation, SQLite/private access, package generation, transfer,
R&D access, or Codex C.

## Missing Tests Or Safeguards

No contract-level test or safeguard gap remains for the four reviewed findings.
The later implementation gate still requires the complete synthetic matrix,
including atomic publication, concurrency, pre/post/ambiguous commit behavior,
effective-time regression, supersession rejection, permanent second-release
refusal before private access, no durable mapping state, and exact no-echo and
false-authority/non-claim checks. No implementation or test execution is
authorized by this report.

## Checks Run

```text
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
gh issue view 731 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body,comments
py tools/check_agent_docs.py
git diff --check
py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
py tools/select_validation.py --base origin/main --paths-from-stdin
ASCII, final-newline, Markdown-fence, and untracked-file whitespace checks
```

## Results

- Branch and `origin/main` matched at
  `d235bcfdc2e913e2305d81a6a86414ba6781918a` with left/right count `0 0`.
- Issue #731 is open. The R&D predecessor is durably merged and its exact blobs
  are recorded in issue lineage.
- The prior independent review's merged-predecessor and migration/allowlist
  checks remain the confirmed basis for CT-731-E-001 and CT-731-E-002. This
  narrow re-review did not reopen SQLite, source-schema, or private-evidence
  inspection.
- Agent-doc consistency passed with errors 0 and warnings 0.
- `git diff --check` passed.
- Protected-surface scan passed over both reviewed artifacts with forbidden 0
  and warnings 0.
- Secret/private-marker scan passed over both reviewed artifacts with forbidden
  0 and warnings 0.
- Validation selection passed with warnings 0 and selected the expected
  docs-only gates.
- Both reviewed artifacts are ASCII, end with a newline, have balanced Markdown
  fences, and have no untracked-file whitespace errors.
- No runtime tests were run because no implementation exists or is authorized.
- No SQLite database, Player.log, JSONL, private path, or local dataset was
  opened or created.

## Drift Notes

- Branch drift: none; branch and `origin/main` are synchronized.
- Source-schema drift: none observed between the issue-preflight and current
  contract base.
- Cross-repository contract drift: none observed; the exact merged R&D contract
  remains the consumer authority.
- Contract ambiguity: none observed in CT-731-E-001 through CT-731-E-004. All
  four findings are fixed-state confirmed.

## Recommendation

Approve the revised docs-only contract for Codex F submission. Do not route to
Codex C, implementation, SQLite access, package generation, transfer, or R&D
access. Any implementation contract or execution requires a separate owner
decision after this documentation package is durably reviewed and merged.

## Next Workflow Action

Next role: Codex F, limited to staging and submitting the reviewed contract and
contract-test report. No implementation file belongs in that submission.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/731"
  completed_thread: "E_contract_re_review"
  next_thread: "F_docs_submission"
  source_artifact: "docs/contracts/core_sanitized_parser_fact_producer_boundary.md"
  target_artifact: "docs/contract_test_reports/core_sanitized_parser_fact_producer_boundary.md"
  risk_tier: "High"
  base_branch: "origin/main"
  branch: "codex/sanitized-parser-fact-producer-boundary-731"
  reviewed_commit: "d235bcfdc2e913e2305d81a6a86414ba6781918a"
  finding_status:
    CT-731-E-001: "fixed_state_confirmed"
    CT-731-E-002: "fixed_state_confirmed"
    CT-731-E-003: "fixed_state_confirmed"
    CT-731-E-004: "fixed_state_confirmed"
  final_decision: "revised_contract_accepted_docs_only"
  sqlite_access_authorized: false
  implementation_authorized: false
  package_generation_authorized: false
  package_transfer_authorized: false
  r_and_d_dataset_access_authorized: false
  ready_for_codex_c: false
  forbidden_scope_touched: false
  generated_private_artifacts_kept: false
  next_recommended_role: "Codex F: submit only the reviewed contract and report"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "High"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "docs/decisions/ADR-0001-parser-owns-truth.md"
    - "docs/decisions/ADR-0003-player-log-drift-policy.md"
    - "docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md"
    - "docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md"
  protected_surfaces:
    - "parser truth and final reconciliation"
    - "local analytics SQLite schema and private facts"
    - "match/game identity and provenance"
    - "card/deck/action privacy"
    - "cross-repository evidence transfer"
    - "retention, revocation, and deletion lifecycle"
  authority_conflicts_found: false
  authority_conflict_notes: "No authority conflict or remaining contract finding; docs-only acceptance does not authorize implementation routing."
  stop_conditions:
    - "Do not access SQLite or private evidence."
    - "Do not implement producer code or tests."
    - "Do not generate or transfer a package."
    - "Do not authorize R&D access or Codex C."
```
