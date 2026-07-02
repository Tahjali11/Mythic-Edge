# Security Quality Gate Policy Readiness Contract

## Module

`security_quality_gate_policy_readiness`

Plain English: this contract defines when public-safe security-quality evidence
is strong enough to discuss a future advisory-to-blocking gate policy. It does
not create the gate, change CI, mutate CodeQL alerts, or claim that Mythic Edge
is secure, private, release-ready, deploy-ready, production-ready, or parser
truth-ready.

## Source Issue

- Child issue: <https://github.com/Tahjali11/Mythic-Edge/issues/644>
- Parent security workflow:
  <https://github.com/Tahjali11/Mythic-Edge/issues/330>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Predecessor evidence issue:
  <https://github.com/Tahjali11/Mythic-Edge/issues/639>
- Predecessor evidence PR:
  <https://github.com/Tahjali11/Mythic-Edge/pull/641>
- Predecessor merge commit:
  `f4234edbe2d76c13d4f26fece130d0682a8fd33e`

## Tracker

Parent security workflow #330 remains open. Project roadmap #568 remains open.

## Owning Layer

Quality / Governance security reporting.

This contract owns only readiness vocabulary for deciding whether evidence can
be reviewed as a future gate-policy candidate. It does not own scanner truth,
CodeQL alert lifecycle truth, vulnerability truth, parser truth, CI policy, or
release/deploy/production readiness.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- GitHub CodeQL lifecycle evidence;
- local CWE-mapped validation profile evidence;
- protected-surface and secret/private-marker scanner summaries;
- GitHub Actions / repo-check status summaries;
- security-quality report artifacts under `docs/quality_reports/security/`.

## Truth Owner

Truth ownership stays split:

- GitHub CodeQL/code scanning owns live CodeQL alert lifecycle state.
- `tools/check_cwe_mapped_local_validation_profile.py` owns local CWE profile
  manifest validation results.
- `tools/generate_cwe_profile_advisory_report.py` owns public-safe CWE
  advisory report shape.
- `tools/check_protected_surfaces.py` owns protected-surface path
  classification for the scoped paths it inspects.
- `tools/check_secret_patterns.py` owns secret/private-marker scan results for
  the scoped paths or tracked file set it inspects.
- GitHub Actions owns workflow/check conclusions.
- `tools/generate_security_quality_summary.py` owns only the public-safe
  aggregate report shape.
- This contract owns only gate-policy readiness vocabulary and review routing.

No source may be promoted into security assurance, privacy assurance, formal
CWE compliance, release readiness, deploy readiness, production readiness,
parser truth, analytics truth, AI truth, or coaching truth.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
current public-safe security-quality evidence bundle
  -> gate-policy readiness classification
  -> later Codex A/B gate-policy problem representation and contract, if selected
```

Forbidden reverse flow:

- readiness classification must not mutate CodeQL alerts;
- readiness classification must not change CI;
- readiness classification must not weaken protected-surface or secret scanner
  behavior;
- readiness classification must not change parser, runtime, workbook, webhook,
  Apps Script, analytics, AI/coaching, Line Tracer, deployment, or production
  behavior.

## Files Owned By This Contract

This Codex B pass owns:

- `docs/contracts/security_quality_gate_policy_readiness.md`

This contract references but does not replace:

- `docs/contracts/security_quality_current_evidence_bundle.md`
- `docs/contracts/security_quality_scanner_summary_aggregation.md`
- `docs/contracts/security_cwe_mapped_local_validation_profile.md`
- `docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md`
- `docs/contract_test_reports/security_quality_current_evidence_bundle.md`
- `docs/quality_reports/security/security_quality_summary/*.json`
- `docs/quality_reports/security/cwe_mapped_local_validation_profile/*.json`

## Current Context

Issue #639 / PR #641 produced a refreshed public-safe evidence bundle measured
at commit `3f571ec3abd2800c2df2d6a8e79cec1a0f5896ce`. The reviewed bundle
included:

- CodeQL lifecycle count summary for `refs/heads/main`;
- CWE profile advisory report summary;
- protected-surface scanner count/status summary;
- secret/private-marker scanner count/status summary;
- GitHub CodeQL and repo-check workflow status summary;
- explicit non-claim booleans preserving advisory-only status.

The #639 bundle is a valid input to this contract. It is not authorization to
create a blocking gate.

## Problem Statement And First Bad Value

The first bad value is treating `advisory_passed` as if it means
`blocking_gate_ready`.

Those are different states:

- `advisory_passed` means the evidence packet was public-safe, current enough,
  and validation-clean for review.
- `blocking_gate_ready` would mean Mythic Edge has approved a specific CI or
  policy gate, its exact failure behavior, its rollback path, and its protected
  surface impact.

This contract prevents that collapse by defining an intermediate
`blocking_candidate` state. A `blocking_candidate` is eligible for a later
gate-policy issue. It is not an active gate.

## Scope Decision

In scope:

- readiness vocabulary for future advisory-to-blocking gate policy;
- minimum evidence package before a gate-policy issue may be considered;
- public/private evidence boundary;
- stale, missing, conflicting, unsafe, and non-public-safe evidence handling;
- explicit approval boundaries for later CI or blocking behavior;
- validation evidence expected from later Codex C/E work.

Out of scope:

- implementation code;
- CI changes;
- CodeQL alert mutation;
- gate activation;
- advisory checks promoted to blocking;
- raw SARIF or raw CodeQL payload handling;
- public vulnerability reproduction details;
- private logs, local artifacts, secrets, or private paths;
- parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior;
- release, deploy, production, security, privacy, parser, analytics, AI, or
  coaching truth claims.

## Readiness State Vocabulary

### `advisory_only`

Default state for all security-quality evidence. Evidence may be reviewed,
summarized, and routed, but no blocking gate may be created from this state.

Use when:

- evidence is useful but incomplete for gate-policy discussion;
- evidence is complete but no later gate-policy issue is approved;
- evidence is intentionally report-only.

### `review_required`

Evidence is public-safe enough to inspect, but a human or Codex E review must
resolve ambiguity before classifying it as a future gate candidate.

Use when:

- warnings are present but not yet classified;
- CodeQL, scanner, or CI freshness differs across sources;
- evidence is current but the exact future gate failure mode is not defined;
- the gate would affect developer workflow or protected surfaces.

### `blocking_candidate`

Evidence may be used as input to a later gate-policy issue. This state still
does not authorize CI change, enforcement, or gate activation.

Required conditions:

- all required evidence families are current for the intended base or explicitly
  tied to the same reviewed PR;
- CodeQL lifecycle summary is count-only and public-safe;
- CWE profile advisory report validates with no errors;
- protected-surface summary has forbidden count `0`;
- secret/private-marker summary has forbidden count `0`;
- CI/repo-check summaries are current and successful for the same commit or
  reviewed branch;
- no raw/private data is present;
- no source has unresolved contradictory status;
- non-claim booleans remain false for assurance/readiness/truth claims;
- a later issue names the exact proposed gate, failure mode, affected files,
  rollback plan, and review path.

### `blocked`

Evidence prevents gate-policy discussion until a follow-up resolves it.

Use when:

- CodeQL open count is greater than `0`;
- required CodeQL lifecycle counts cannot be safely collected or verified;
- any required scanner summary has forbidden count greater than `0`;
- secret/private-marker warnings are unexplained and could represent unsafe
  public content;
- protected-surface warnings are unexplained and could represent unauthorized
  protected-surface change;
- source evidence requires raw SARIF, raw CodeQL payloads, raw scanner finding
  lists, source snippets, exploit detail, private paths, secrets, logs, or
  generated/private artifacts;
- validation fails;
- evidence is stale relative to the intended gate target and cannot be
  refreshed safely;
- a report claims security/privacy/release/deploy/production readiness or
  parser truth.

### `parked`

Gate-policy discussion is intentionally paused even if evidence is otherwise
reviewable.

Use when:

- another repository lane owns the active security decision;
- the human owner defers enforcement sequencing;
- a broader roadmap issue must choose gate order first;
- missing follow-up contracts are needed before enforcement can be considered.

## Minimum Evidence Package

A future gate-policy discussion must start from a current public-safe evidence
package containing these source families:

| Source family | Required public-safe fields | Blocking candidate requirement |
| --- | --- | --- |
| CodeQL lifecycle | repository, ref, measured commit, open/fixed/dismissed counts, source method, freshness | open count `0`, count-only summary, no alert payloads |
| CWE profile advisory report | schema, measured ref/commit, overall status, validator errors/warnings, family count, non-claims | current report, validator errors `0`, no formal compliance claim |
| Protected-surface scan | tool, mode, base/head, scanned path count, forbidden count, warnings count, result | current scoped summary, forbidden `0`, warnings explained or absent |
| Secret/private-marker scan | tool, mode, base/head, scanned path count, forbidden count, warnings count, result | current scoped summary, forbidden `0`, warnings explained or absent |
| CI/repo checks | workflow/check name, conclusion, commit/ref, run URL when safe, freshness | successful current checks for the same target |
| Review artifacts | contract, implementation handoff, contract-test/review report when present | no unresolved blocker findings |

The package may include repo-relative report paths, public issue/PR links,
public commit IDs, symbolic category counts, booleans, and non-claim text.

## Advisory Versus Blocking Boundary

Advisory evidence may:

- describe source freshness and validation status;
- identify blockers, watch-list items, and review-required sources;
- recommend a later gate-policy issue;
- support human review of whether a gate is worth designing.

Advisory evidence must not:

- create or edit CI workflow behavior;
- turn a check into a failing gate;
- set fail-under or blocking thresholds;
- mutate CodeQL alerts;
- dismiss, reopen, or close security alerts;
- claim that security, privacy, release, deploy, production, parser, analytics,
  AI, or coaching truth is established.

A blocking gate may only be designed later by a separate issue and contract
that names:

- the exact gate source;
- the exact blocking condition;
- the exact affected command or workflow;
- the expected failure message shape;
- the rollback plan;
- the owner approval record;
- the Codex E review expectation;
- the Codex F/G submitter and deployer boundaries.

## Private / Public Evidence Boundary

Allowed public evidence:

- counts;
- symbolic statuses;
- booleans;
- public issue, PR, workflow, and commit references;
- repo-relative artifact paths;
- public-safe scanner modes;
- non-claim text.

Forbidden public evidence:

- raw SARIF;
- raw CodeQL API responses;
- CodeQL alert body text, locations, traces, code flows, or snippets;
- exploit reproduction steps;
- bypass details;
- vulnerability proof payloads;
- raw protected-surface or secret/private-marker finding lists;
- raw scanner excerpts;
- raw logs;
- raw JSONL payloads;
- SQLite contents;
- local app data;
- workbook exports;
- failed-post payloads;
- runtime artifacts;
- private decklists;
- local absolute paths;
- secrets, credentials, tokens, keys, endpoints, webhook URLs, spreadsheet IDs,
  or environment values;
- arbitrary user files or screenshots with sensitive data.

If a source contains forbidden evidence, the output must fail closed with a
symbolic status such as `blocked_unsafe_input` and must not echo the unsafe
value.

## Source-Specific Interpretation Rules

### CodeQL Lifecycle

CodeQL lifecycle counts are external evidence from GitHub. Count `0` for open
alerts is necessary for `blocking_candidate`, but it is not sufficient for
security assurance.

Gate-policy readiness must stop if CodeQL cannot be queried or summarized
without raw alert payloads. It must also stop if current open count is greater
than `0`, unless a later security issue explicitly defines a narrow exception
for an already-reviewed false positive. This contract does not create such an
exception.

### CWE Profile

The CWE profile is a local validation vocabulary. A current advisory report
with validator errors `0` may support `blocking_candidate` discussion.

It must not be described as formal CWE compliance, proof of no weaknesses, or
authorization to mutate CodeQL alerts.

### Protected-Surface Scan

Protected-surface summaries are scoped to the mode used. A path-scoped clean
scan only supports claims about that path set. It does not support all-repo
protected-surface readiness unless a later contract defines and validates an
all-repo mode.

Warnings require review before `blocking_candidate`.

### Secret / Private-Marker Scan

Secret/private-marker summaries are scoped to the mode used. A clean
changed-path scan is enough for the current evidence artifact path set, but not
for repo-wide privacy readiness.

Any forbidden result blocks gate-policy discussion. Warnings require symbolic
classification and review without exposing values or private paths.

### CI / Repo Checks

Successful checks show workflow status only. They do not prove that a proposed
future gate is safe or that the repo is ready for release, deploy, or
production use.

Failed, missing, cancelled, or stale required checks route to `review_required`
or `blocked` depending on whether the source can be refreshed safely.

## Stale, Missing, Conflicting, And Unsafe Evidence

Stale evidence must be labeled `stale` and cannot support `blocking_candidate`
unless a later issue explicitly narrows the gate to historical/report-only
interpretation.

Missing evidence must be labeled `not_collected` or `deferred_with_reason`.
Required source families that are missing route to `review_required` or
`blocked`.

Conflicting evidence must be labeled `conflict` and route to `review_required`
until the conflict is resolved. A conflict must not be resolved by deleting,
ignoring, or weakening scanner output.

Unsafe evidence must be labeled `blocked_unsafe_input` and must not be echoed,
persisted, summarized with raw values, or committed.

## Future Gate Approval Preconditions

A later advisory-to-blocking gate issue must have:

1. explicit human approval to design a blocking policy;
2. a fresh public-safe evidence package;
3. a Codex B gate-specific contract;
4. a Codex C implementation plan limited to the named gate;
5. Codex E review or contract-test approval;
6. Codex F submitter handoff that stages only reviewed files;
7. Codex G deployer review before merge or activation;
8. rollback instructions;
9. proof that the change does not mutate CodeQL alerts or expose private data;
10. explicit non-claims preserved in the final artifact.

Without those preconditions, the strongest allowed state is
`blocking_candidate`.

## False Authority Flags

Any future readiness artifact must preserve these booleans unless a later
approved contract explicitly changes one:

```yaml
implementation_authorized: false
ci_change_authorized: false
security_gate_activation_authorized: false
codeql_alert_mutation_authorized: false
security_assurance_claimed: false
privacy_assurance_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
parser_truth_claimed: false
analytics_truth_claimed: false
ai_truth_claimed: false
coaching_truth_claimed: false
```

## Side Effects

This contract allows only documentation output:

- `docs/contracts/security_quality_gate_policy_readiness.md`

It does not authorize:

- code changes;
- CI changes;
- CodeQL alert changes;
- scanner behavior changes;
- issue lifecycle changes;
- PR creation;
- security gate creation;
- public vulnerability disclosure;
- private artifact reads or writes.

## Error Behavior

If a later thread cannot prove an evidence source is current, public-safe, and
scoped to the intended target, it must choose the least-authoritative status:

1. `blocked_unsafe_input` for unsafe/private/raw source content;
2. `blocked_validation_failure` for failed validation;
3. `review_required` for ambiguous source status;
4. `parked` when sequencing or human approval is missing;
5. `advisory_only` when evidence is clean but no future gate is approved.

Automation must not promote itself from `advisory_only` to an active blocking
policy.

## Validation Evidence Required Later

A later Codex C or Codex E pass for gate-policy readiness should validate:

```bash
git status --short --branch
python3 -m json.tool docs/quality_reports/security/security_quality_summary/<current-report>.json
python3 -m json.tool docs/quality_reports/security/cwe_mapped_local_validation_profile/<current-report>.json
python3 tools/check_cwe_mapped_local_validation_profile.py docs/security/cwe_mapped_local_validation_profile.v1.json
python3 -m pytest -q tests/test_security_quality_summary.py tests/test_cwe_profile_advisory_report.py tests/test_cwe_mapped_local_validation_profile.py
python3 -m ruff check tools/generate_security_quality_summary.py tools/generate_cwe_profile_advisory_report.py tools/check_cwe_mapped_local_validation_profile.py
python3 tools/check_agent_docs.py
git diff --check
```

Path-scoped safety scans should include every changed public artifact:

```bash
printf '%s\n' \
  docs/contracts/security_quality_gate_policy_readiness.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

printf '%s\n' \
  docs/contracts/security_quality_gate_policy_readiness.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

If a future pass touches report artifacts, include those report paths in the
same scans. If a future pass requires live CodeQL verification, it may collect
count-only lifecycle summaries but must not persist or echo raw alert payloads.

## Acceptance Criteria

- The contract defines advisory, review-required, blocking-candidate, blocked,
  and parked states.
- The contract requires a current public-safe evidence package before later
  gate-policy discussion.
- The contract distinguishes advisory evidence from active blocking gates.
- The contract forbids private/raw evidence and requires fail-closed handling
  for unsafe inputs.
- The contract preserves all non-claims and false-authority flags.
- The contract routes future gate design to a separate approved issue and
  contract.

## Next Workflow Action

Next recommended role: Codex E review / contract-test.

Codex E should review whether this contract overclaims the #639 evidence bundle
or allows an accidental advisory-to-blocking promotion without a separate
approved gate issue.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / contract-test for security-quality issue #644.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/644

Parent tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract artifact:
docs/contracts/security_quality_gate_policy_readiness.md

Review focus:
- Verify the contract keeps #639 evidence advisory-only.
- Verify `blocking_candidate` does not authorize CI changes, gates, CodeQL
  mutation, public vulnerability detail, private evidence, or readiness claims.
- Verify the public/private evidence boundary is strict enough for future gate
  policy discussion.
- Verify stale, missing, conflicting, unsafe, and warning evidence fail closed
  or route to review.
- Verify future Codex C/F/G boundaries remain explicit.

Do not implement code, change CI, mutate CodeQL alerts, activate gates, inspect
private logs, expose secrets/private paths, open a PR, or claim security
assurance, privacy assurance, release readiness, deploy readiness, production
readiness, parser truth, analytics truth, AI truth, or coaching truth.

Expected output:
- Findings first, if any.
- Contract-test verdict.
- Validation run.
- Recommended next role.
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/644"
  parent_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  source_artifacts:
    - "docs/contracts/security_quality_current_evidence_bundle.md"
    - "docs/contracts/security_quality_scanner_summary_aggregation.md"
    - "docs/contract_test_reports/security_quality_current_evidence_bundle.md"
    - "docs/quality_reports/security/security_quality_summary/2026-07-02-3f571ec-security-quality-summary.json"
    - "docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-02-3f571ec-cwe-profile-advisory-report.json"
  target_artifact: "docs/contracts/security_quality_gate_policy_readiness.md"
  risk_tier: "High"
  base_branch: "main"
  branch: "codex/security-quality-gate-policy-readiness-644"
  current_status: "advisory_only_policy_defined"
  blocking_gate_authorized: false
  ci_change_authorized: false
  codeql_alert_mutation_authorized: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  release_readiness_claimed: false
  deploy_readiness_claimed: false
  production_readiness_claimed: false
  parser_truth_claimed: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/security_quality_gate_policy_readiness.md"
    - "path-scoped secret/private-marker scan for docs/contracts/security_quality_gate_policy_readiness.md"
    - "git diff --check"
  stop_conditions:
    - "Do not implement code."
    - "Do not change CI or activate security gates."
    - "Do not mutate CodeQL alerts."
    - "Do not expose public vulnerability details, raw SARIF, raw CodeQL payloads, raw scanner findings, private logs, secrets, or private paths."
    - "Do not claim security assurance, privacy assurance, release readiness, deploy readiness, production readiness, parser truth, analytics truth, AI truth, or coaching truth."
```
