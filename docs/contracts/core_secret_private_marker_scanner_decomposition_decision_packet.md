# Core Secret/Private Marker Scanner Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/669>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS gate issue: <https://github.com/Tahjali11/Mythic-Edge/issues/664>

Previous governance/report/helper packet contract:
<https://github.com/Tahjali11/Mythic-Edge/issues/665>

Previous concrete decomposition child:
<https://github.com/Tahjali11/Mythic-Edge/issues/667>

Previous merged PR:
<https://github.com/Tahjali11/Mythic-Edge/pull/668>

Previous merge commit: `4c2b95e7fce5d0c40d5c7cc98ecfd7cf3d0bb55e`

Target candidate: `tools/check_secret_patterns.py`

Candidate id: `secret_private_marker_scan`

Candidate class: `local_advisory_check_surface`

## Purpose

This contract records the Phase 5 decomposition decision packet for the
repo-local secret/private marker scanner at `tools/check_secret_patterns.py`.

Plain English: this scanner helps keep private values out of committed work.
It scans repo-local text for secret-looking values, private local paths, raw
Arena log markers, failed-post/runtime/generated-data markers, workbook export
markers, and related private-marker patterns. It reports public-safe findings
with redacted excerpts and stable exit-code behavior.

This packet is planning-only. It does not implement decomposition, move files,
change scanner behavior, change CLI arguments, change scan modes, change exit
codes, change finding categories, change severity semantics, change safe
excerpt behavior, change public-safe/no-echo behavior, change checked-file
selection, change CI, run ARS, run Refactor Scout, inspect private evidence,
or claim readiness, security assurance, privacy assurance, or parser truth.

## Source Context

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: https://github.com/Tahjali11/Mythic-Edge
- Target artifact:
  `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- Source contract:
  `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- Source candidate: `tools/check_secret_patterns.py`
- Candidate surface class: `local_advisory_check_surface`
- Current target commit for this packet:
  `4c2b95e7fce5d0c40d5c7cc98ecfd7cf3d0bb55e`
- Current branch target for any future implementation: a non-production
  issue-scoped branch, not `main`
- Implementation authorized by this contract: false
- File move authorized by this contract: false
- Cross-repo extraction authorized by this contract: false
- CI change authorized by this contract: false
- ARS run authorized by this contract: false
- Refactor Scout run authorized by this contract: false
- Private evidence inspection authorized by this contract: false
- Source mutation authorized by this contract: false

## Source Artifacts Inspected

- GitHub issue #669
- GitHub issue #568
- GitHub issue #463
- GitHub issue #664
- GitHub issue #667
- GitHub PR #668
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`

No raw Player.log files, UTC_Log files, private evidence, local app-data,
runtime artifacts, failed posts, workbook exports, generated data dumps,
credentials, tokens, API keys, webhook URLs, ARS artifacts, Refactor Scout
artifacts, private scan outputs, or source-repo mutation surfaces were read,
created, imported, or modified.

## Packet Envelope

```yaml
packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/669"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
source_contract: "docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md"
previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/667"
previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/668"
previous_merge_commit: "4c2b95e7fce5d0c40d5c7cc98ecfd7cf3d0bb55e"
target_commit: "4c2b95e7fce5d0c40d5c7cc98ecfd7cf3d0bb55e"
candidate_scope: "governance_report_helper_only"
candidate_id: "secret_private_marker_scan"
candidate_surface_class: "local_advisory_check_surface"
current_path: "tools/check_secret_patterns.py"
target_artifact: "docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md"
phase_5_order_preserved: true
eventbus_support_deferred: true
api_frontend_live_capture_deferred: true
parser_state_deferred: true
implementation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
private_evidence_inspection_authorized: false
source_mutation_authorized: false
parser_behavior_change_authorized: false
eventbus_behavior_change_authorized: false
api_payload_change_authorized: false
frontend_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
workbook_webhook_change_authorized: false
apps_script_change_authorized: false
ci_change_authorized: false
scanner_behavior_change_authorized: false
cli_contract_change_authorized: false
safe_excerpt_change_authorized: false
no_echo_boundary_change_authorized: false
readiness_claimed: false
parser_truth_claimed: false
truth_or_assurance_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

If any future packet or implementation handoff sets one of the protected
authorization flags to true without a separate reviewed issue and explicit
owner approval, it must fail closed and route back to Codex B or Codex A.

## Observed Current Behavior

`tools/check_secret_patterns.py` is a deterministic Python command-line tool
with this public invocation surface:

```bash
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 tools/check_secret_patterns.py --base origin/main --repo-root .
```

The scanner currently:

- scans changed files from `git diff --name-only --diff-filter=ACMRTUXB
  <base>...HEAD`;
- scans newline-delimited paths from standard input in `paths-from-stdin` mode;
- scans all tracked files in advisory/report-only mode with `--all`;
- normalizes repo-relative paths and rejects outside-root paths when strict
  stdin mode is used;
- skips missing, binary, oversized, or decode-replacement files with warning
  categories where appropriate;
- detects live-looking webhook URLs, authorization headers, credential
  assignments, private key markers, private local user paths, raw Arena
  Player.log-style markers, failed-post payload markers, runtime-status
  payload markers, generated-data dump markers, spreadsheet IDs or URLs, and
  workbook export markers;
- distinguishes placeholder/redacted examples and sanitized fixture contexts
  from forbidden private values;
- returns `Finding` and `ScanResult` dataclasses with stable fields;
- emits a text report headed `Secret / Private Marker Scan`;
- reports `FORBIDDEN` and `WARNING` lines with category ids, paths, line
  numbers, reasons, and redacted excerpts;
- returns result values `passed`, `warning`, `failed`, and `error`;
- exits `0` when no forbidden findings exist, when only warnings exist, or
  when `--all` finds forbidden items in advisory mode;
- exits `1` when non-`--all` scanning finds forbidden items;
- exits `2` for configuration-level errors;
- writes normal reports to stdout and error reports to stderr.

The scanner is consumed by humans, Codex roles, docs-only validation bundles,
submission handoffs, local quality checks, path-scoped protected-surface
validation, and future behavior-preservation checks. Its output is advisory
evidence about repo-local content. It is not security assurance or privacy
assurance.

## First Bad Values To Prevent

These values would make a later decomposition unsafe or out of scope:

- Treating this decision packet as implementation authority.
- Changing scanner behavior while calling the change behavior-preserving.
- Changing the public command path, CLI options, modes, stdout/stderr routing,
  report heading, report fields, finding ordering, finding category ids,
  severity values, result values, or exit-code semantics.
- Weakening safe excerpts, redaction, no-echo behavior, local-path redaction,
  private-marker redaction, or placeholder/sanitized-fixture handling.
- Treating `--all` advisory behavior as a blocking CI gate.
- Treating scanner success as proof that the repo has no secrets, no privacy
  risk, no raw logs, no generated artifacts, or no unsafe private values.
- Treating stale, absent, or broad ARS/Refactor Scout evidence as current
  clearance for a security/privacy-adjacent helper.
- Moving the scanner to another repository before same-repo stability is
  proven.
- Adding CI enforcement, blocking status checks, ARS runs, Refactor Scout runs,
  private-evidence reads, source mutation, or protected-surface behavior
  changes as part of decomposition.

## Owning Layer And Truth Boundary

Primary internal project area: Quality / Governance local advisory check
surface.

Bridge-code status: `not_bridge_code`.

Truth and authority boundary:

- The scanner owns only its local advisory scan mechanics and report shape.
- Active repo governance docs, current issues, current contracts, accepted
  ADRs, and reviewed handoffs own workflow authority.
- Parser/state code owns parser truth.
- Security/privacy assurance remains a human/project governance decision and
  cannot be inferred from scanner output.
- The scanner may provide evidence for a review. It does not prove secrets are
  absent, private data is absent, privacy is assured, security is assured,
  parser behavior is correct, or release/deploy/production readiness exists.

The scanner currently has read-only contact with committed repo files selected
by git diff, stdin paths, or tracked-file inventory. This packet does not
authorize source mutation, private evidence reads, runtime artifact reads, or
CI gate changes.

## Decomposition Decision

Same-repo decomposition is appropriate only as a future behavior-preserving
candidate, not as immediate implementation authority.

Final decision for issue #669:
`request_fresh_ars_refactor_evidence`.

This means:

- the candidate is eligible for same-repo decomposition behind the existing
  public CLI entrypoint;
- cross-repo extraction is rejected;
- no implementation may proceed from this packet alone;
- because the scanner is security/privacy-adjacent and controls public-safe
  no-echo behavior, a later Codex C implementation requires either fresh
  scoped ARS/refactor evidence for this exact candidate and target commit, or
  explicit owner acceptance that the implementation may proceed without fresh
  scoped evidence;
- any later implementation must preserve every public CLI, output, exit-code,
  category, severity, redaction, safe-excerpt, and no-echo behavior.

If the owner explicitly accepts implementation without fresh scoped
ARS/refactor evidence, that acceptance must be issue-scoped, candidate-scoped,
commit-scoped or branch-scoped, and must preserve all protected boundaries in
this packet. It must not become general ARS clearance or security/privacy
assurance.

## Candidate Row

| Field | Value |
| --- | --- |
| `candidate_id` | `secret_private_marker_scan` |
| `candidate_surface_class` | `local_advisory_check_surface` |
| `current_path` | `tools/check_secret_patterns.py` |
| `current_behavior` | Deterministic repo-local scanner for secret-looking values, private markers, raw-log markers, local paths, generated/runtime artifact markers, workbook export markers, safe excerpts, and public-safe reports |
| `truth_or_authority_owner` | Scanner owns only advisory scan/report mechanics; active repo authority and human owner decisions remain authoritative for security/privacy decisions |
| `upstream_dependencies` | Git diff, git tracked-file inventory, stdin path list, repo-relative path normalization, committed text files, regex rule vocabulary, placeholder/sanitized-fixture policy, policy-path allow/warning contexts |
| `downstream_consumers` | Humans, Codex role handoffs, docs-only validation bundles, path-scoped safety scans, local quality checks, future submitter/deployer validation evidence |
| `protected_surface_contact` | `read_only_reference` to committed repo files; security/privacy-adjacent because it detects private markers and redacts excerpts |
| `proposed_destination` | Same repository, same public CLI path, optional private helper modules behind `tools/check_secret_patterns.py` only after required preconditions |
| `why_not_keep_local` | The current monolithic scanner combines rule vocabulary, redaction/safe-excerpt logic, git/path collection, file scanning, result models, rendering, and CLI handling; a later same-repo split may reduce review fatigue while preserving behavior. |
| `why_not_move_to_existing_repo` | Adjacent repos do not own Mythic Edge's repo-local secret/private-marker safety policy or current validation workflow. |
| `why_not_create_new_repo` | Separate repo would add authority, dependency, version, and rollout ambiguity for a helper whose behavior is tightly coupled to this repo's protected-surface and local-artifact rules. |
| `new_public_interface_needed` | `none` |
| `new_public_interface_description` | Not applicable; later implementation must preserve `python3 tools/check_secret_patterns.py`, `--base`, `--repo-root`, `--paths-from-stdin`, `--all`, text report shape, finding fields, category ids, severities, result values, stdout/stderr behavior, and exit codes. |
| `behavior_preservation_tests` | Focused tests for CLI usage errors, git diff path collection, path normalization, stdin mode, all-repo advisory mode, forbidden/warning categories, redaction/no-echo behavior, sanitized fixture handling, binary/oversized/decode warnings, outside-repo symlink errors, and deterministic finding ordering |
| `rollback_plan` | Revert implementation commit; restore all scanner logic to `tools/check_secret_patterns.py`; remove any same-repo helper modules introduced by the implementation; do not alter CI, parser, runtime, private artifacts, or source repos. |
| `ars_refactor_evidence_status` | Fresh scoped evidence or explicit owner acceptance required before implementation; see evidence block below. |
| `non_claims` | No readiness, parser truth, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, CI enforcement, no-secret proof, or no-private-data proof |
| `final_decision` | `request_fresh_ars_refactor_evidence` |

## Same-Repo Module Boundaries

A later implementation may split internal code only if these boundaries
preserve behavior exactly:

- Public entrypoint:
  `tools/check_secret_patterns.py` remains executable and importable.
- Contract vocabulary:
  severity labels, result labels, scan modes, category ids, rule ids, reason
  wording, placeholder markers, sanitized fixture markers, scan byte limits,
  excerpt length limits, and regex policy remain behavior-compatible.
- Data models:
  `Finding`, `ScanResult`, `forbidden`, `warnings`, `result`, and `exit_code`
  semantics remain stable.
- Safe excerpt and no-echo layer:
  redaction behavior for secrets, webhook URLs, private paths, raw-log markers,
  failed-post/runtime/generated-data markers, workbook markers, credential
  values, and long lines remains stable or stricter only under a separate
  contract.
- Rule layer:
  webhook, credential, private-path, raw-log, artifact-payload, spreadsheet,
  workbook, placeholder, sanitized-fixture, binary, oversized, decode, symlink,
  and outside-root behavior remains stable.
- Path collection layer:
  `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`,
  `git ls-files`, stdin path normalization, repo-root handling, and
  outside-root failure behavior remain stable.
- Report layer:
  `Secret / Private Marker Scan` heading, mode/base/head/scanned/skipped/
  forbidden/warnings counts, finding line shape, error line shape, result line,
  stdout/stderr routing, and deterministic sorting remain stable.
- CLI layer:
  `--base`, `--repo-root`, `--paths-from-stdin`, `--all`, mutual-exclusion
  errors, missing-base errors, and `main(argv)` behavior remain stable.

Tests that import constants, functions, dataclasses, or `main()` from
`tools/check_secret_patterns.py` must continue to work. If a later
implementation extracts helpers, `tools/check_secret_patterns.py` must
re-export any names that current tests or known local tools rely on, or the
change must route back to Codex B as a public-interface change.

## Public Interface Preservation

The following are public for behavior-preservation purposes:

- file path: `tools/check_secret_patterns.py`;
- CLI options: `--base`, `--repo-root`, `--paths-from-stdin`, and `--all`;
- mode values: `changed-files`, `paths-from-stdin`,
  `all-repo-advisory`;
- result values: `passed`, `warning`, `failed`, and `error`;
- severity values: `allowed`, `warning`, and `forbidden`;
- exit codes: `0` for no forbidden findings and for advisory `--all` mode,
  `1` for forbidden findings in changed/stdin modes, and `2` for
  configuration-level errors;
- report heading: `Secret / Private Marker Scan`;
- report count fields: `mode`, `base`, `head`, `scanned_paths`,
  `skipped_paths`, `forbidden`, and `warnings`;
- finding line shape:
  `FORBIDDEN|WARNING <category_id> <path>:<line> - <reason> [excerpt: <safe>]`;
- safe excerpt redaction vocabulary such as `<redacted:credential_value>`,
  `<redacted:live_webhook>`, `<redacted:private_local_path>`-style private
  path redaction, and category-specific redaction tokens;
- category ids tested by `tests/test_check_secret_patterns.py`;
- deterministic finding sort order;
- stdout for normal reports and stderr for configuration errors;
- changed-file git command and advisory `--all` non-blocking exit behavior.

Any later change to these items is not behavior-preserving and must route back
to Codex B before implementation.

## ARS And Refactor Scout Evidence Status

No current ARS or Refactor Scout evidence is claimed for this candidate.

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
ars_version_contract_bundle: "none"
current_target_commit: "4c2b95e7fce5d0c40d5c7cc98ecfd7cf3d0bb55e"
relevant_changes_since_review: "not_applicable"
evidence_status: "fresh_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed: "yes"
explicit_owner_acceptance_alternative: "allowed_if_issue_scoped_candidate_scoped_and_commit_or_branch_scoped"
reason: "The candidate is same-repo and local-advisory, but it is security/privacy-adjacent and owns safe-excerpt/no-echo behavior. Fresh scoped ARS/refactor evidence or explicit owner acceptance is required before any implementation."
```

Fresh scoped ARS or Refactor Scout evidence is not required for this
contract-only packet because no implementation, file move, CI change, private
evidence read, source mutation, scanner behavior change, or readiness claim is
authorized here.

Fresh scoped evidence or explicit owner acceptance is required before a later
Codex C implementation because the candidate:

- controls secret/private-marker detection categories;
- controls redaction and safe-excerpt behavior;
- controls advisory-vs-blocking exit behavior for scanner modes;
- is used by docs-only and submitter validation bundles;
- can create false security/privacy authority if decomposed carelessly.

Fresh evidence or owner acceptance must be renewed if the implementation target
commit, scanner scope, ARS/refactor version bundle, proposed module boundary,
public interface, or protected-surface contact changes.

## Allowed Later Implementation Boundary

After Codex E review and explicit user routing, a later Codex C implementation
may proceed only if the ARS/refactor or owner-acceptance precondition above is
satisfied.

If authorized, the later implementation may:

- keep `tools/check_secret_patterns.py` as the public entrypoint;
- extract internal helper modules in the same repo;
- preserve existing CLI behavior and report shape;
- preserve current tests and add focused behavior-preservation tests;
- compare before/after command output on public-safe synthetic fixtures;
- update only the implementation handoff required by the workflow.

That later implementation must not:

- move the public entrypoint;
- change CLI options or modes;
- change scan target selection;
- change category ids, rule ids, reasons, severities, result values, or exit
  codes;
- weaken or broaden safe-excerpt/no-echo behavior without a separate contract;
- change advisory `--all` behavior into CI enforcement;
- add CI enforcement or blocking status checks;
- run ARS, Refactor Scout, probes, module sweeps, replay audits, or private
  evidence checks unless separately authorized;
- inspect private logs, failed posts, runtime status files, generated data,
  workbook exports, local app-data, live MTGA data, or source repos;
- change parser behavior, parser event classes, EventBus behavior, API
  payloads, frontend behavior, workbook/webhook behavior, Apps Script
  behavior, live-capture behavior, or CI behavior.

## Behavior-Preservation Validation Expectations

A later implementation must collect baseline evidence before editing and
compare it after the change. Minimum expected validation:

```bash
python3 tools/check_secret_patterns.py --base origin/main
printf "%s\n" tools/check_secret_patterns.py tests/test_check_secret_patterns.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 -m pytest -q tests/test_check_secret_patterns.py
python3 -m py_compile tools/check_secret_patterns.py
python3 -m ruff check tools/check_secret_patterns.py tests/test_check_secret_patterns.py
git diff --check
printf "%s\n" <changed-paths> | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf "%s\n" <changed-paths> | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf "%s\n" <changed-paths> | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

If helper modules are added, include those helper modules,
`tools/check_secret_patterns.py`, `tests/test_check_secret_patterns.py`, and
the implementation handoff artifact in the path-scoped scans.

Behavior-preservation evidence must include:

- before/after report comparison for a clean changed-file scan;
- before/after report comparison for `paths-from-stdin` mode;
- before/after report comparison for `--all` advisory mode;
- exit-code comparison for pass, warning-only, forbidden changed/stdin scan,
  advisory `--all` forbidden scan, invalid base, missing base, mode-conflict,
  unreadable file, and outside-root symlink cases;
- category-id comparison for all categories currently covered by
  `tests/test_check_secret_patterns.py`;
- redaction/no-echo comparison for live webhook URL, credential value, private
  Unix path, private Windows path with spaced user, raw player-log marker,
  failed-post/runtime/generated/workbook markers, and placeholder values;
- deterministic finding ordering comparison;
- proof that no generated reports, runtime artifacts, private logs, source
  snippets, raw diffs, secrets, local paths, failed posts, workbook exports, or
  generated data were committed.

Validation must not:

- run private evidence;
- run ARS, Refactor Scout, probes, module sweeps, replay audits, or live
  capture unless separately authorized;
- change CI;
- create durable runtime artifacts unless separately authorized;
- claim readiness, parser truth, reliability readiness, security assurance, or
  privacy assurance.

## Rollback Plan

Rollback must be simple:

- revert the decomposition implementation commit;
- restore all scanner logic to `tools/check_secret_patterns.py`;
- remove any same-repo helper modules introduced by the implementation commit;
- preserve the existing public CLI path and command behavior;
- do not update CI, parser code, runtime code, source repos, private
  artifacts, raw logs, generated data, failed posts, workbook exports, or
  private evidence as part of rollback unless a later issue explicitly
  authorizes that separate scope.

## Refusal And Downgrade Vocabulary

Future roles must fail closed using these statuses:

- `same_repo_decomposition_candidate`: internal same-repo extraction may be
  considered after review and explicit implementation routing.
- `same_repo_keep_current_path`: the scanner should remain monolithic because
  behavior-preservation risk is higher than maintenance benefit.
- `request_fresh_ars_refactor_evidence`: scoped ARS or Refactor Scout evidence
  or explicit owner acceptance is needed before implementation.
- `request_scope_split_child`: proposed work combines decomposition with
  behavior, CI, protected-surface, governance, private-evidence, or scanner
  semantic changes and needs a new issue.
- `reject_cross_repo_extraction`: moving the scanner outside this repo is not
  allowed by this packet.
- `unsupported`: requested action lacks authority or evidence.
- `review_required`: contract or implementation needs Codex E review before
  the next role.
- `blocked`: implementation cannot continue without new issue authority,
  fresh evidence, or owner approval.

## Non-Claims

This contract does not claim:

- `tools/check_secret_patterns.py` is implementation-ready;
- `tools/check_secret_patterns.py` is decomposition-ready without review and
  the evidence/owner precondition;
- scanner output proves no secrets are present;
- scanner output proves no private data is present;
- scanner output proves security assurance;
- scanner output proves privacy assurance;
- scanner output proves release readiness;
- scanner output proves deploy readiness;
- scanner output proves production readiness;
- scanner output proves parser truth;
- ARS clearance;
- Refactor Scout clearance;
- CI enforcement authority.

## Recommended Next Role

Next role: Codex E - Module Reviewer.

Codex E should review this packet against issue #669, issue #665, #568 Phase 5,
#664, `tools/check_secret_patterns.py`, and `tests/test_check_secret_patterns.py`.
If the contract is accepted, Codex E may route to either:

- Codex A/B for fresh scoped ARS/refactor evidence or explicit owner-acceptance
  framing; or
- Codex C only if the required evidence/owner-acceptance precondition is
  already satisfied by a current handoff.

If any public-interface, safe-excerpt/no-echo, scanner category, exit-code,
CI, evidence, owner-acceptance, or cross-repo authority ambiguity remains,
Codex E should route back to Codex B.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #669.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/669

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Related ARS gate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/664

Source artifact:
docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md

Target candidate:
tools/check_secret_patterns.py

Review goal:
Review the contract-only decomposition decision packet for the secret/private
marker scanner. Verify that it uses the #665 decision-packet vocabulary,
classifies the candidate as a local advisory check surface, keeps same-repo
decomposition as the only possible later implementation route, rejects
cross-repo extraction, preserves the public CLI/report/category/severity/
exit-code/safe-excerpt/no-echo contract, and requires fresh scoped ARS/refactor
evidence or explicit owner acceptance before implementation because the scanner
is security/privacy-adjacent.

Protected boundaries:
Do not implement code, move files, open a PR, change scanner behavior, change
CLI/output/exit-code semantics, change safe-excerpt/no-echo behavior, change
CI, run ARS or Refactor Scout, inspect private evidence, mutate source repos,
change parser/EventBus/API/frontend/live-capture/workbook/webhook/Apps Script
behavior, or claim readiness, parser truth, security assurance, or privacy
assurance.

Expected output:
Findings first. State whether the contract is ready for the next governance
step, needs Codex B clarification, or should be blocked. Include validation
reviewed, remaining risk, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/669"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/667"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/668"
  previous_merge_commit: "4c2b95e7fce5d0c40d5c7cc98ecfd7cf3d0bb55e"
  completed_thread: "B"
  next_thread: "E"
  verdict: "secret_private_marker_scanner_decomposition_decision_packet_ready_for_review"
  target_artifact: "docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md"
  candidate_surface: "tools/check_secret_patterns.py"
  candidate_id: "secret_private_marker_scan"
  candidate_surface_class: "local_advisory_check_surface"
  final_decision: "request_fresh_ars_refactor_evidence"
  implementation_authorized: false
  file_move_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_evidence_inspection_authorized: false
  source_mutation_authorized: false
  scanner_behavior_change_authorized: false
  cli_contract_change_authorized: false
  safe_excerpt_change_authorized: false
  no_echo_boundary_change_authorized: false
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
