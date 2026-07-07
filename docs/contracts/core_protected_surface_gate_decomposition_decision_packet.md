# Core Protected Surface Gate Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/687>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS evidence gate: <https://github.com/Tahjali11/Mythic-Edge/issues/664>

Source contract:
`docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`

Target candidate: `tools/check_protected_surfaces.py`

Candidate id: `protected_surface_gate`

Candidate class: `local_advisory_check_surface`

## Module

`core_protected_surface_gate_decomposition_decision_packet`

This contract is the Phase 5 decomposition decision packet for the protected
surface gate helper.

Plain English: `tools/check_protected_surfaces.py` is a local validation
helper that looks at repo-relative file paths and classifies them as allowed,
warning-only protected surfaces, or forbidden local/private/generated
surfaces. This packet decides whether it may later be split into smaller
same-repo modules while preserving behavior. It does not implement that split.

This contract is planning-only. It does not implement code, move files, open a
PR, change protected-surface categories, change path rules, change severity
semantics, change report output, change command-line arguments, change exit
codes, change checked-file selection, change validation selector behavior,
change CI, run ARS, run Refactor Scout, inspect private evidence, inspect or
mutate source repos, or claim readiness, security assurance, privacy
assurance, parser truth, reliability readiness, release readiness, deploy
readiness, or production readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/687>
- Project roadmap / tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Broad decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Related ARS evidence gate: <https://github.com/Tahjali11/Mythic-Edge/issues/664>
- Target artifact:
  `docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md`

## Source Artifacts Inspected

- GitHub issue #687
- GitHub issue #568
- GitHub issue #463
- GitHub issue #664
- GitHub PR #666 and its contract artifact context
- GitHub issue #667 / PR #668 as the first concrete helper decomposition
  path
- GitHub issue #669, issue #681, issue #684, and PR #686 as the
  secret/private-marker scanner helper decomposition path
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md`
- `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- `docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`

No private logs, private evidence, local app-data, runtime artifacts, failed
posts, workbook exports, generated data dumps, credentials, secret values,
live endpoint values, ARS run artifacts, Refactor Scout artifacts, private
scan outputs, source-repo mutation surfaces, raw diffs, or private source
snippets were read, created, imported, or modified.

## Owning Layer

Primary layer: repository workflow safety and local advisory validation.

`tools/check_protected_surfaces.py` owns only the mechanics of classifying
repo-relative paths for the local protected-surface gate. It does not own
parser truth, EventBus behavior, API payload shape, frontend behavior,
live-capture behavior, workbook/webhook behavior, Apps Script behavior, CI
policy, security assurance, privacy assurance, reliability readiness, release
readiness, deploy readiness, or production readiness.

## Internal Project Area

Quality and Governance local advisory checks.

The candidate remains a repo-local advisory helper. Its output helps humans
and workflow roles notice when a change touches forbidden local/private or
generated paths, or warning-only protected surfaces. Its output is not a
readiness claim and is not proof that a change is safe.

## Truth Owner

- `tools/check_protected_surfaces.py` owns the current command surface, path
  classification rules, warning/forbidden result semantics, report rendering,
  git changed-path collection, stdin path handling, and exit-code behavior.
- `tests/test_check_protected_surfaces.py` owns the current
  behavior-preservation test expectations for the helper.
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
  owns the general Phase 5 decomposition packet vocabulary.
- Repo governance docs, current issues, current contracts, accepted ADRs, and
  human owner decisions remain authoritative for workflow routing.

## Bridge-Code Status

`not_bridge_code`

This helper does not bridge parser facts, EventBus delivery, API payloads,
frontend state, live capture, workbook data, webhook data, or Apps Script. It
is a governance validation helper that classifies paths before future workflow
roles decide what additional review is needed.

## Files Owned By This Contract

- `docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md`

Files referenced but not owned:

- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md`
- `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- `docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
protected_surface_gate_behavior_change_authorized: false
cli_contract_change_authorized: false
classification_rule_change_authorized: false
path_rule_change_authorized: false
severity_semantics_change_authorized: false
report_output_change_authorized: false
exit_code_change_authorized: false
checked_file_set_change_authorized: false
validation_selector_change_authorized: false
ci_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_repo_inspection_authorized: false
source_mutation_authorized: false
private_evidence_inspection_authorized: false
parser_behavior_change_authorized: false
parser_event_class_change_authorized: false
eventbus_behavior_change_authorized: false
api_payload_change_authorized: false
frontend_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
workbook_webhook_change_authorized: false
apps_script_change_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
```

Any future handoff, evidence packet, review, or implementation plan that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Codex E Schema And Vocabulary Reconciliation

This section resolves:

- `PROTSURF-DECOMP-E-001`
- `PROTSURF-DECOMP-E-002`

The packet must consume the #665 decision-packet schema literally. It must not
invent parallel field names or values that look equivalent to #665 terms but
are not accepted by the source contract.

Canonical corrections:

- the packet envelope uses the #665 `current_path` field exactly and does not
  introduce alternate path-field names;
- the packet envelope includes required #665 false-authority fields
  `source_mutation_authorized: false` and
  `truth_or_assurance_claimed: false`;
- the candidate row uses the allowed #665 `protected_surface_contact` value
  `read_only_reference`, not a custom contact label;
- `request_fresh_ars_refactor_evidence` remains the single
  `final_decision` because fresh scoped evidence or explicit owner acceptance
  is required before implementation;
- all local shorthand remains explanatory prose only and must not be treated as
  schema vocabulary by future roles.

## Packet Envelope

```yaml
packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/687"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
source_contract: "docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md"
target_artifact: "docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md"
target_commit: "15595d72ca45c596e86b33edb5bbd17310c2417a"
candidate_scope: "governance_report_helper_only"
candidate_id: "protected_surface_gate"
candidate_surface_class: "local_advisory_check_surface"
current_path: "tools/check_protected_surfaces.py"
phase_5_order_preserved: true
eventbus_support_deferred: true
api_frontend_live_capture_deferred: true
parser_state_deferred: true
final_decision: "request_fresh_ars_refactor_evidence"
implementation_authorized: false
file_move_authorized: false
protected_surface_gate_behavior_change_authorized: false
ci_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
readiness_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
parser_truth_claimed: false
truth_or_assurance_claimed: false
```

## Observed Current Behavior

The helper is a deterministic path-classification gate.

Current public command surface:

```bash
python3 tools/check_protected_surfaces.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main --repo-root .
printf "%s\n" docs/example.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Observed behavior:

- `--base` is required.
- `--repo-root` defaults to `.`.
- `--paths-from-stdin` switches path collection from git diff to newline input
  from stdin.
- Without `--paths-from-stdin`, the helper collects changed paths using
  `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`.
- Paths are normalized to slash-separated repo-relative form.
- Empty path segments and `.` path segments are removed.
- Forbidden rules are evaluated before warning rules.
- Documented fixture paths under `tests/fixtures/` bypass the local log and
  raw workbook export forbidden categories.
- Token/credential-like filenames are treated as credential-adjacent
  forbidden paths when matched by the current filename heuristic.
- Unknown paths are allowed by default.
- The report heading is `Protected Surface Gate`.
- The report includes `base`, `head`, `changed_paths`, `forbidden`,
  `warnings`, classified findings, and a final `result`.
- Normal reports are written to stdout.
- Git or operating-system configuration errors become result `error` and
  return exit code `2`.

Current severity/result behavior:

- `allowed`: no finding; does not fail.
- `warning`: protected surface touched; report records the category; exit code
  remains `0`.
- `forbidden`: local/private/generated/review artifact path touched; report
  records the category; exit code is `1`.
- `error`: git/configuration failure; exit code is `2`.

Current forbidden category ids include:

- `local_mtga_log`
- `runtime_log`
- `runtime_status`
- `failed_posts`
- `bad_events`
- `generated_card_data`
- `raw_workbook_export`
- `secret_file`
- `webhook_api_credential`
- `local_review_artifact`

Current warning category ids include:

- `parser_event_classes`
- `parser_state_final_reconciliation`
- `extractor_behavior`
- `match_game_identity`
- `workbook_schema`
- `webhook_payload_shape`
- `apps_script_behavior`
- `environment_runtime_paths`
- `workflow_authority_docs`

The category names are path-classification labels, not claims that the helper
has inspected source contents or validated runtime behavior.

## Problem Statement And First Bad Values

The intended workflow is:

1. use this packet to decide the future decomposition boundary for
   `tools/check_protected_surfaces.py`;
2. keep the current command, output, category, severity, exit-code, and path
   selection behavior stable;
3. require Codex E review before any submitter or implementation route;
4. require fresh scoped ARS/refactor evidence or explicit owner acceptance
   before any later implementation;
5. route to Codex C only after explicit user routing and only for a
   behavior-preserving same-repo implementation.

The first bad value is treating this contract as implementation authority.

The second bad value is treating the helper as proof that protected-surface
changes are safe.

The third bad value is treating a warning-only protected-surface result as
approval to change parser, EventBus, API, frontend, live-capture, workbook,
webhook, Apps Script, CI, or production behavior.

The fourth bad value is changing category ids, path rules, severity values,
result values, report shape, stdout/stderr routing, or exit codes during a
decomposition.

The fifth bad value is treating absent, stale, broad, mismatched, ambiguous,
or private-only ARS/refactor material as current scoped clearance.

The sixth bad value is treating owner acceptance as a blanket waiver. Owner
acceptance must name this issue, candidate, current path, target commit or
branch, allowed next role, and preserved boundaries.

## Public Interface

This contract does not change the public protected-surface gate interface. For
later implementation planning, the preserved public interface remains:

- command path: `tools/check_protected_surfaces.py`;
- CLI options: `--base`, `--repo-root`, and `--paths-from-stdin`;
- result values: `passed`, `failed`, and `error`;
- severity values: `allowed`, `warning`, and `forbidden`;
- exit code `0` for allowed and warning-only results;
- exit code `1` for forbidden findings;
- exit code `2` for configuration-level errors;
- report heading: `Protected Surface Gate`;
- report count fields: `base`, `head`, `changed_paths`, `forbidden`, and
  `warnings`;
- finding line shape:
  `FORBIDDEN|WARNING <category_id> <path> - <reason>`;
- forbidden and warning category ids covered by
  `tests/test_check_protected_surfaces.py`;
- stdout for normal reports and stderr for command usage errors;
- stderr-backed parser usage errors for missing required arguments;
- deterministic classification order by input path order;
- changed-file git command:
  `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`;
- stdin path collection behavior for `--paths-from-stdin`;
- documented-fixture bypass behavior for allowed test fixtures.

Any proposed change to these items is outside this decision packet and must
route back to Codex B.

## Decomposition Decision

Decision: `request_fresh_ars_refactor_evidence`

Same-repo decomposition is eligible for later consideration, but it is not
authorized by this contract. The helper is a local advisory check surface, and
the right decomposition direction is same-repo-first behind the existing
public command path. Cross-repo extraction is rejected.

Fresh scoped ARS/refactor evidence or explicit owner acceptance is required
before implementation because this helper guards the workflow's protected
surface warnings and forbidden local/private/generated path boundaries.
Accidental behavior drift could loosen safety checks, misreport protected
surface contact, or create false authority in later handoffs.

This contract does not itself run ARS, run Refactor Scout, collect evidence,
or satisfy that precondition.

If the owner explicitly accepts implementation without fresh scoped
ARS/refactor evidence, that acceptance must be issue-scoped, candidate-scoped,
commit-scoped or branch-scoped, and must preserve all protected boundaries in
this packet. It must not become general ARS clearance, security assurance,
privacy assurance, CI readiness, or protected-surface behavior authority.

## Candidate Row

| Field | Value |
| --- | --- |
| `candidate_id` | `protected_surface_gate` |
| `candidate_surface_class` | `local_advisory_check_surface` |
| `current_path` | `tools/check_protected_surfaces.py` |
| `current_behavior` | Deterministic repo-local path classifier for allowed, warning-only protected surface, forbidden local/private/generated/review artifact, and configuration-error outcomes |
| `truth_or_authority_owner` | Helper owns only advisory path-classification mechanics; active repo authority and human owner decisions remain authoritative for workflow routing and protected-surface changes |
| `upstream_dependencies` | Git diff changed-path list, stdin path list, repo-relative path normalization, rule constants, category ids, severity labels, documented fixture exception behavior |
| `downstream_consumers` | Humans, Codex role handoffs, docs-only validation bundles, CI workflow invocation, submitter/deployer validation evidence, validation-selector-adjacent routing |
| `protected_surface_contact` | `read_only_reference`; classifies repo-relative paths and does not read source contents as part of classification |
| `proposed_destination` | Same repository, same public CLI path, optional private helper modules behind `tools/check_protected_surfaces.py` only after required preconditions |
| `why_not_keep_local` | The current monolithic helper combines rule vocabulary, path normalization, matcher logic, git collection, classification, report rendering, and CLI handling; a later same-repo split may reduce review fatigue while preserving behavior. |
| `why_not_move_to_existing_repo` | Adjacent repos do not own Mythic Edge's protected-surface gate vocabulary or its current validation workflow. |
| `why_not_create_new_repo` | A separate repo would add authority, dependency, version, and rollout ambiguity for a helper tightly coupled to this repo's governance and protected-surface rules. |
| `new_public_interface_needed` | `none` |
| `new_public_interface_description` | Not applicable; later implementation must preserve `python3 tools/check_protected_surfaces.py`, `--base`, `--repo-root`, `--paths-from-stdin`, report shape, category ids, severities, result values, stdout/stderr behavior, and exit codes. |
| `behavior_preservation_tests` | Focused tests for path normalization, forbidden categories, allowed fixture exceptions, warning categories, forbidden-over-warning precedence, exit behavior, report shape, git diff path collection, git/OS errors, required CLI args, stdin mode, and CI workflow invocation expectations |
| `rollback_plan` | Revert implementation commit; restore all protected-surface gate logic to `tools/check_protected_surfaces.py`; remove any same-repo helper modules introduced by the implementation; do not alter CI, parser, runtime, private artifacts, or source repos. |
| `ars_refactor_evidence_status` | Fresh scoped evidence or explicit owner acceptance required before implementation; see evidence block below. |
| `non_claims` | No readiness, reliability readiness, parser truth, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, ARS clearance, Refactor Scout clearance, protected-surface behavior approval, or CI enforcement authority |
| `final_decision` | `request_fresh_ars_refactor_evidence` |

## Same-Repo Module Boundaries

A later implementation may split internal code only if these boundaries
preserve behavior exactly:

- Public entrypoint:
  `tools/check_protected_surfaces.py` remains executable and importable.
- Contract vocabulary:
  severity labels, result labels, category ids, rule ids, reason wording,
  documented-fixture exceptions, path matching behavior, and report labels
  remain behavior-compatible.
- Data models:
  `Rule`, `Classification`, `GateResult`, `forbidden`, `warnings`, `result`,
  and `exit_code` semantics remain stable.
- Rule layer:
  forbidden and warning category ids remain stable unless a later contract
  explicitly changes protected-surface policy.
- Path normalization and matching layer:
  slash normalization, `.` segment removal, leading slash handling, glob
  matching, basename matching, and token/credential-like filename heuristic
  remain stable.
- Path collection layer:
  `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`,
  `--paths-from-stdin`, repo-root handling, and git/configuration error
  behavior remain stable.
- Report layer:
  `Protected Surface Gate` heading, base/head/changed_paths/forbidden/
  warnings counts, finding line shape, error result shape, stdout/stderr
  routing, and final result line remain stable.
- CLI layer:
  `--base`, `--repo-root`, `--paths-from-stdin`, missing-base usage errors,
  and `main(argv)` behavior remain stable.

Tests that import constants, functions, dataclasses, or `main()` from
`tools/check_protected_surfaces.py` must continue to work. If a later
implementation extracts helpers, `tools/check_protected_surfaces.py` must
re-export any names that current tests or known local tools rely on, or the
change must route back to Codex B as a public-interface change.

## ARS And Refactor Scout Evidence Status

No current ARS or Refactor Scout evidence is claimed for this candidate.

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
ars_version_contract_bundle: "none"
current_target_commit: "15595d72ca45c596e86b33edb5bbd17310c2417a"
relevant_changes_since_review: "not_applicable"
evidence_status: "fresh_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed: "yes"
explicit_owner_acceptance_alternative: "allowed_if_issue_scoped_candidate_scoped_and_commit_or_branch_scoped"
reason: "The candidate is same-repo and local-advisory, but it controls protected-surface warning and forbidden-path behavior used by workflow validation. Fresh scoped ARS/refactor evidence or explicit owner acceptance is required before any implementation."
```

Fresh scoped ARS or Refactor Scout evidence is not required for this
contract-only packet because no implementation, file move, CI change, private
evidence read, source mutation, protected-surface gate behavior change, or
readiness claim is authorized here.

Fresh scoped evidence or explicit owner acceptance is required before a later
Codex C implementation because the candidate:

- controls forbidden path categories for local/private/generated/review
  artifacts;
- controls warning categories for parser, workbook, webhook, Apps Script,
  environment, and workflow authority surfaces;
- controls warning-only versus blocking exit behavior;
- is referenced by docs-only and submitter/deployer validation bundles;
- can create false workflow authority if decomposed carelessly.

Fresh evidence or owner acceptance must be renewed if the implementation
target commit, helper scope, ARS/refactor version bundle, proposed module
boundary, public interface, category vocabulary, path rule vocabulary, or
protected-surface contact changes.

## Allowed Later Implementation Boundary

After Codex E review and explicit user routing, a later Codex C
implementation may proceed only if the ARS/refactor or owner-acceptance
precondition above is satisfied.

If authorized, the later implementation may:

- keep `tools/check_protected_surfaces.py` as the public entrypoint;
- extract internal helper modules in the same repo;
- preserve existing CLI behavior and report shape;
- preserve current tests and add focused behavior-preservation tests;
- compare before/after command output on public-safe synthetic path lists;
- update only the implementation handoff required by the workflow.

That later implementation must not:

- move the public entrypoint;
- change CLI options;
- change changed-file or stdin path selection;
- change category ids, rule ids, reasons, severities, result values, or exit
  codes;
- weaken forbidden path matching;
- convert warning-only categories into pass/fail policy without a separate
  contract;
- add CI enforcement or blocking status checks;
- run ARS, Refactor Scout, probes, module sweeps, replay audits, private
  evidence checks, or live-capture checks unless separately authorized;
- inspect private logs, failed posts, runtime status files, generated data,
  workbook exports, local app-data, live MTGA data, or source repos;
- change parser behavior, parser event classes, EventBus behavior, API
  payloads, frontend behavior, workbook/webhook behavior, Apps Script
  behavior, live-capture behavior, or CI behavior.

## Behavior-Preservation Validation Expectations

A later implementation must collect baseline evidence before editing and
compare it after the change. Minimum expected validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_check_protected_surfaces.py
python3 tools/check_protected_surfaces.py --base origin/main
printf "%s\n" tools/check_protected_surfaces.py tests/test_check_protected_surfaces.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
python3 -m py_compile tools/check_protected_surfaces.py
python3 -m ruff check tools/check_protected_surfaces.py tests/test_check_protected_surfaces.py
git diff --check
printf "%s\n" <changed-paths> | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
printf "%s\n" <changed-paths> | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
printf "%s\n" <changed-paths> | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

If helper modules are added, include those helper modules,
`tools/check_protected_surfaces.py`, `tests/test_check_protected_surfaces.py`,
and the implementation handoff artifact in the path-scoped scans.

Behavior-preservation evidence must include:

- before/after report comparison for a clean changed-file scan;
- before/after report comparison for `paths-from-stdin` mode;
- exit-code comparison for allowed-only, warning-only, forbidden, invalid
  base, missing base, git failure, and operating-system failure cases;
- category-id comparison for all categories currently covered by
  `tests/test_check_protected_surfaces.py`;
- path-normalization comparison for Windows-style separators, redundant
  separators, leading slash input, and `.` segments;
- documented-fixture exception comparison;
- forbidden-over-warning precedence comparison;
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
- restore all protected-surface gate logic to
  `tools/check_protected_surfaces.py`;
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
- `same_repo_keep_current_path`: the helper should remain monolithic because
  behavior-preservation risk is higher than maintenance benefit.
- `request_fresh_ars_refactor_evidence`: scoped ARS or Refactor Scout evidence
  or explicit owner acceptance is needed before implementation.
- `request_scope_split_child`: proposed work combines decomposition with
  behavior, CI, protected-surface, private-evidence, parser, EventBus, API,
  frontend, live-capture, workbook, webhook, Apps Script, or production
  semantic changes and needs a new issue.
- `reject_cross_repo_extraction`: moving the helper outside this repo is not
  allowed by this packet.
- `unsupported`: requested action lacks authority or evidence.
- `review_required`: contract or implementation needs Codex E review before
  the next role.
- `blocked`: implementation cannot continue without new issue authority, fresh
  evidence, or owner approval.

## Non-Claims

This contract does not claim:

- `tools/check_protected_surfaces.py` is implementation-ready;
- `tools/check_protected_surfaces.py` is decomposition-ready without review
  and the evidence/owner precondition;
- the protected-surface gate proves a change is safe;
- warning-only output proves a protected-surface change is approved;
- forbidden output proves a source file contains private data;
- allowed output proves no private data exists;
- allowed output proves no protected-surface risk exists;
- security assurance;
- privacy assurance;
- reliability readiness;
- release readiness;
- deploy readiness;
- production readiness;
- parser truth;
- ARS clearance;
- Refactor Scout clearance;
- CI enforcement authority.

## Recommended Next Role

Next role: Codex E - Module Reviewer.

Codex E should review this packet against issue #687, the #665 Phase 5
decomposition packet contract, #568, #463, #664,
`tools/check_protected_surfaces.py`, and
`tests/test_check_protected_surfaces.py`.

If the contract is accepted, Codex E may route to Codex F for docs-only
submission. After the contract is merged, a later role may create or reconcile
a fresh scoped ARS/refactor evidence preflight child, unless the owner
explicitly accepts implementation without fresh evidence for this exact
candidate and target branch or commit.

If any public-interface, classification-rule, path-rule, severity, exit-code,
CI, evidence, owner-acceptance, or cross-repo authority ambiguity remains,
Codex E should route back to Codex B.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #687.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/687

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Related ARS evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/664

Source artifact:
docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md

Target candidate:
tools/check_protected_surfaces.py

Review goal:
Review the contract-only decomposition decision packet for the protected
surface gate. Verify that it uses the #665 decision-packet vocabulary,
classifies the candidate as a local advisory check surface, keeps same-repo
decomposition as the only possible later implementation route, rejects
cross-repo extraction, preserves the public CLI/report/category/severity/
exit-code/path-selection contract, and requires fresh scoped ARS/refactor
evidence or explicit owner acceptance before implementation because the helper
guards protected-surface workflow safety.

Protected boundaries:
Do not implement code, move files, open a PR, change protected-surface gate
behavior, change CLI/output/category/severity/exit-code semantics, change
checked-file selection, change CI, run ARS or Refactor Scout, inspect private
evidence, mutate source repos, change parser/EventBus/API/frontend/
live-capture/workbook/webhook/Apps Script behavior, or claim readiness,
reliability readiness, parser truth, security assurance, or privacy assurance.

Expected output:
Findings first. State whether the contract is ready for docs-only submission,
needs Codex B clarification, or should be blocked. Include validation
reviewed, remaining risk, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/687"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  completed_thread: "B"
  next_thread: "E"
  verdict: "protected_surface_gate_decomposition_decision_packet_ready_for_review"
  target_artifact: "docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md"
  risk_tier: "High"
  candidate_surface: "tools/check_protected_surfaces.py"
  candidate_id: "protected_surface_gate"
  candidate_surface_class: "local_advisory_check_surface"
  final_decision: "request_fresh_ars_refactor_evidence"
  implementation_authorized: false
  file_move_authorized: false
  protected_surface_gate_behavior_change_authorized: false
  cli_contract_change_authorized: false
  classification_rule_change_authorized: false
  path_rule_change_authorized: false
  severity_semantics_change_authorized: false
  report_output_change_authorized: false
  exit_code_change_authorized: false
  checked_file_set_change_authorized: false
  validation_selector_change_authorized: false
  ci_change_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  parser_behavior_change_authorized: false
  eventbus_behavior_change_authorized: false
  api_payload_change_authorized: false
  frontend_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  parser_truth_claimed: false
```
