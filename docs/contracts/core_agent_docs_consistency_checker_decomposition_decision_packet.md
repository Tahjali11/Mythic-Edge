# Core Agent Docs Consistency Checker Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/667>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS gate issue: <https://github.com/Tahjali11/Mythic-Edge/issues/664>

Previous contract issue: <https://github.com/Tahjali11/Mythic-Edge/issues/665>

Previous PR: <https://github.com/Tahjali11/Mythic-Edge/pull/666>

Previous merge commit: `70191d1c11ac49d01ae308db1612e7669c304f9a`

Target candidate: `tools/check_agent_docs.py`

Candidate id: `agent_doc_consistency_check`

Candidate class: `local_advisory_check_surface`

## Purpose

This contract records the Phase 5 decomposition decision packet for the
repo-local agent docs consistency checker at `tools/check_agent_docs.py`.

The checker is a local advisory tool. It reads committed governance,
workflow, template, ADR, issue-template, and PR-template files; reports
deterministic consistency findings; and exits with a stable success or failure
code. It does not own governance truth, parser truth, security assurance,
privacy assurance, reliability readiness, release readiness, deploy readiness,
or production readiness.

This contract is planning-only. It does not implement decomposition, move files,
change CLI behavior, change checked-file coverage, change severity semantics,
change report schemas, change CI, or authorize any ARS or Refactor Scout run.

## Source Context

- Repository: `Tahjali11/Mythic-Edge`
- Target artifact:
  `docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md`
- Source candidate: `tools/check_agent_docs.py`
- Candidate surface class: `local_advisory_check_surface`
- Current target commit for this packet:
  `70191d1c11ac49d01ae308db1612e7669c304f9a`
- Current branch target for future implementation: a non-production
  issue-scoped branch, not `main`
- Implementation authorized by this contract: false
- File move authorized by this contract: false
- CI change authorized by this contract: false
- ARS run authorized by this contract: false
- Refactor Scout run authorized by this contract: false
- Source mutation authorized by this contract: false

## Packet Envelope

```yaml
packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/667"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
target_commit: "70191d1c11ac49d01ae308db1612e7669c304f9a"
candidate_scope: "governance_report_helper_only"
candidate_id: "agent_doc_consistency_check"
candidate_surface_class: "local_advisory_check_surface"
current_path: "tools/check_agent_docs.py"
target_artifact: "docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md"
phase_5_order_preserved: true
eventbus_support_deferred: true
api_frontend_live_capture_deferred: true
parser_state_deferred: true
implementation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
parser_behavior_change_authorized: false
eventbus_behavior_change_authorized: false
api_payload_change_authorized: false
frontend_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
ci_change_authorized: false
readiness_claimed: false
parser_truth_claimed: false
truth_or_assurance_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

## Observed Current Behavior

`tools/check_agent_docs.py` is a deterministic Python command-line tool with
this public invocation surface:

```bash
python3 tools/check_agent_docs.py
python3 tools/check_agent_docs.py --repo-root .
python3 tools/check_agent_docs.py --format text
python3 tools/check_agent_docs.py --format json
```

The checker currently:

- reads a fixed required-file list covering `AGENTS.md`,
  `docs/agent_rules.yml`, `docs/agent_constitution.md`,
  `docs/codex_module_workflow.md`, `docs/agent_threads/**`,
  `docs/templates/**`, `.github/ISSUE_TEMPLATE/module_workflow.yml`,
  `.github/pull_request_template.md`, and `docs/decisions/**`;
- extracts repo-local Markdown, YAML, and path references from active governance
  surfaces;
- validates canonical Codex role names and normal routing path
  `A -> B -> C -> E -> F -> G`;
- validates Codex D as loopback-only and Codex H as auxiliary-only;
- validates authority-order terms and protected-surface wording in active
  governance docs;
- validates workflow handoff and prompt schema expectations;
- validates ADR status vocabulary, ADR index entries, required ADR shape, and
  recommended ADR headings;
- validates local-artifact, parser-truth-boundary, and external-surface
  boundary language;
- performs an advisory check that the agent docs checker is not silently placed
  into `.github/workflows/repo-checks.yml` before enforcement is authorized;
- returns text or JSON reports;
- reports `error` and `warning` severities;
- exits `0` when there are no errors, `1` when errors exist, and `2` for
  configuration-level execution errors.

The command is consumed as a local validation helper by humans, Codex roles,
hardening/report helpers, validation selection logic, and implementation
handoffs. Its output is advisory evidence, not project truth.

## First Bad Values To Prevent

These values would make a later decomposition unsafe or out of scope:

- Treating a decomposition contract as permission to change checker behavior.
- Changing the public CLI path, options, stdout/stderr routing, exit codes,
  text report shape, JSON report keys, finding ordering, severity labels, or
  checked-file set while calling the change behavior-preserving.
- Treating a passing checker result as proof that governance docs are correct,
  complete, current, safe, or ready.
- Treating a warning from the checker as permission to continue through a
  higher-authority contract or protected-surface gate.
- Moving the checker to another repository before same-repo stability is proven.
- Adding CI enforcement, blocking status checks, or fail-open policy decisions
  as part of decomposition.
- Using stale ARS or Refactor Scout evidence as source truth or as authority to
  mutate this helper.

## Owning Layer And Truth Boundary

The checker owns only deterministic local consistency checks over committed repo
files. It may identify mismatches, missing references, stale schema terms, and
unauthorized-looking CI integration signals.

The checker does not own:

- repo authority;
- Codex role authority;
- current issue scope;
- current contract scope;
- parser truth;
- workbook, webhook, Apps Script, API, frontend, live-capture, EventBus, CI, or
  production behavior;
- security assurance;
- privacy assurance;
- readiness decisions.

Active governing docs, accepted ADRs, current issue scope, current contract
scope, and current handoff artifacts remain the authority sources. The checker
is evidence about consistency between those surfaces, not the authority itself.

## Decomposition Decision

Final decision for issue #667:
`same_repo_decomposition_candidate`.

This means a later Codex C thread may be routed to split the checker into
smaller same-repo units only after Codex E accepts this contract and the user
explicitly authorizes implementation. The current `tools/check_agent_docs.py`
path must remain the public command-line entrypoint unless a later contract
explicitly changes that public surface.

Cross-repo extraction is rejected for this candidate. The checker is tightly
coupled to Mythic Edge repo governance docs, templates, ADR vocabulary, and
validation selection conventions. Moving it outside the repo would increase
authority ambiguity and make behavior-preservation harder to prove.

## Candidate Row

| Field | Value |
| --- | --- |
| `candidate_id` | `agent_doc_consistency_check` |
| `candidate_surface_class` | `local_advisory_check_surface` |
| `current_path` | `tools/check_agent_docs.py` |
| `current_behavior` | Deterministic local consistency checker for Mythic Edge agent governance docs |
| `truth_or_authority_owner` | Active governance docs, current issue, current contract, accepted ADRs, and handoffs; not the checker |
| `upstream_dependencies` | Committed governance docs, role docs, templates, ADR files, GitHub issue template, PR template, optional workflow file presence |
| `downstream_consumers` | Local validation, validation selector, hardening/report helpers, Codex role handoffs, human review |
| `protected_surface_contact` | `read_only_reference` to committed governance docs only; no parser/runtime/source-repo/private-data contact |
| `proposed_destination` | Same repository, same public CLI path, optional private helper modules behind the existing entrypoint |
| `why_not_keep_local` | The current monolithic file combines constants, document inventory, rule checks, report rendering, and CLI handling; a later same-repo split may reduce maintenance risk while still keeping the helper local. |
| `why_not_move_to_existing_repo` | Existing adjacent repos do not own Mythic Edge governance truth or local validation selection |
| `why_not_create_new_repo` | Separate repo would create unnecessary authority and version-drift risk |
| `new_public_interface_needed` | `none` |
| `new_public_interface_description` | Not applicable; later implementation must preserve `python3 tools/check_agent_docs.py`, `--repo-root`, `--format text`, `--format json`, report keys, severity names, and exit codes. |
| `behavior_preservation_tests` | Focused tests for missing refs, role/routing mismatches, handoff schema, ADR status/index, CI advisory warning, text/JSON rendering, exit codes |
| `rollback_plan` | Revert decomposition commit; restore monolithic `tools/check_agent_docs.py`; keep reports and generated artifacts out of the change |
| `ars_refactor_evidence_status` | Not required for this contract-only same-repo local advisory candidate; see evidence section |
| `non_claims` | No readiness, truth, security, privacy, release, deploy, production, CI-enforcement, or parser-behavior claim |
| `final_decision` | `same_repo_decomposition_candidate` |

## Same-Repo Module Boundaries

A later implementation may split internal code only if these boundaries preserve
behavior exactly:

- Public entrypoint:
  `tools/check_agent_docs.py` remains executable and importable.
- Constants and schemas:
  role names, required files, prompt fields, handoff fields, ADR fields,
  forbidden terms, parser-truth boundary terms, result names, severity names,
  and exit-code mapping remain stable.
- Finding model:
  `Finding`, `CheckResult`, severity labels, result labels, sorting, and JSON
  serialization remain stable.
- Document inventory and read layer:
  required-file discovery, active-doc discovery, ADR discovery, reference
  extraction, and safe read behavior remain deterministic.
- Rule layer:
  role/routing checks, authority-order checks, handoff/prompt schema checks,
  ADR checks, protected-surface text checks, and CI advisory checks remain pure
  local checks.
- Report layer:
  text report headings, JSON keys, finding ordering, stdout/stderr routing, and
  exit codes remain stable.
- CLI layer:
  `argparse` options and `main(argv)` behavior remain stable.

Tests that import constants, functions, dataclasses, or `main()` from
`tools/check_agent_docs.py` must continue to work. If a later implementation
extracts helpers, `tools/check_agent_docs.py` must re-export any names that
current tests or known local tools rely on, or the change must be routed back to
Codex B as a public-interface change.

## Public Interface Preservation

The following are public for behavior-preservation purposes:

- file path: `tools/check_agent_docs.py`;
- CLI options: `--repo-root` and `--format`;
- accepted formats: `text` and `json`;
- report result values: `passed`, `warning`, `failed`, and `error`;
- severity values: `error` and `warning`;
- exit codes: `0` for no errors, `1` for findings with errors, `2` for
  configuration-level errors;
- JSON keys: `mode`, `checked_files`, `errors`, `warnings`, `findings`,
  `error`, and `result`;
- text heading: `Agent Docs Consistency Check`;
- deterministic finding sort order;
- stdout for normal reports and stderr for configuration errors;
- checked file inventory unless a later contract explicitly authorizes a
  checked-surface change.

Any later change to these items is not behavior-preserving and must be routed
back to Codex B before implementation.

## ARS And Refactor Scout Evidence Status

No current ARS or Refactor Scout evidence is claimed for this candidate.

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
ars_version_contract_bundle: "none"
current_target_commit: "70191d1c11ac49d01ae308db1612e7669c304f9a"
relevant_changes_since_review: "not_applicable"
evidence_status: "not_needed_for_contract_only"
fresh_scoped_evidence_needed: "no"
reason: "The candidate is a same-repo local advisory checker, and this packet does not authorize implementation, file moves, CI changes, private-data reads, source mutation, runtime changes, or readiness claims."
```

Fresh scoped ARS or Refactor Scout evidence is not required for this
contract-only packet because the candidate is a local advisory checker, the
recommended path is same-repo-only, and the contract does not authorize
implementation, file moves, CI changes, source mutation, runtime changes, or
private-data reads.

Fresh scoped evidence or a new Codex A/B framing becomes required if a later
proposal:

- changes the public CLI or report interface;
- changes checked-file coverage;
- changes severity or exit-code semantics;
- adds CI enforcement or blocking status checks;
- reads private, generated, runtime, source-repo, or local-only artifacts;
- touches parser, EventBus, API, frontend, live-capture, workbook, webhook,
  Apps Script, or deployment behavior;
- claims readiness, truth, security assurance, or privacy assurance;
- proposes cross-repo extraction.

## Allowed Later Implementation Boundary

After Codex E review and explicit user routing, a later Codex C implementation
may:

- keep `tools/check_agent_docs.py` as the public entrypoint;
- extract internal helper modules in the same repo;
- preserve existing CLI behavior and report schemas;
- preserve current tests and add focused behavior-preservation tests;
- compare before/after command output on representative fixtures;
- update no docs except the implementation handoff required by the workflow.

That later implementation must not:

- move the public entrypoint;
- change CLI options;
- change checked-file inventory;
- change category ids;
- change error/warning severity semantics;
- change output format or JSON keys;
- add CI enforcement;
- add network, private-data, source-repo, ARS, Refactor Scout, probe, replay,
  or runtime behavior;
- change parser behavior, parser event classes, EventBus behavior, API payloads,
  frontend behavior, workbook/webhook behavior, Apps Script behavior, or live
  capture behavior.

## Behavior-Preservation Validation Expectations

A later implementation must collect baseline evidence before editing and
compare it after the change. Minimum expected validation:

```bash
python3 tools/check_agent_docs.py
python3 tools/check_agent_docs.py --format json
python3 -m pytest -q tests/test_check_agent_docs.py
python3 -m py_compile tools/check_agent_docs.py
python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

The `paths-from-stdin` commands must receive only the intended changed paths for
the implementation. If helper modules are added, include those helper modules,
`tools/check_agent_docs.py`, `tests/test_check_agent_docs.py`, and any handoff
artifact.

Behavior-preservation evidence must include:

- before/after text report comparison for a passing repo;
- before/after JSON report comparison for a passing repo;
- focused fixture coverage for at least one error, one warning, and one
  configuration error;
- exit-code comparison for pass, findings-with-errors, and invalid repo root;
- checked-file count and checked-file list comparison;
- deterministic finding-order comparison;
- proof that no generated reports, runtime artifacts, private logs, source
  snippets, raw diffs, secrets, or local paths were committed.

## Rollback Plan

Rollback must be simple:

- revert the decomposition commit;
- restore all checker logic to `tools/check_agent_docs.py`;
- remove any same-repo helper modules introduced by the implementation commit;
- preserve the existing public CLI path and command behavior;
- do not update governance docs, CI, parser code, runtime code, source repos, or
  private artifacts as part of rollback unless a later issue explicitly
  authorizes that separate scope.

## Refusal And Downgrade Vocabulary

Future roles must fail closed using these statuses:

- `same_repo_decomposition_candidate`: internal same-repo extraction may be
  considered after review and explicit implementation routing.
- `same_repo_keep_current_path`: the checker should remain monolithic because
  behavior-preservation risk is higher than maintenance benefit.
- `request_fresh_ars_refactor_evidence`: scoped ARS or Refactor Scout evidence
  is needed before implementation.
- `request_scope_split_child`: proposed work combines decomposition with
  behavior, CI, governance, or protected-surface changes and needs a new issue.
- `reject_cross_repo_extraction`: moving the helper outside this repo is not
  allowed by this packet.
- `unsupported`: requested action lacks authority or evidence.
- `review_required`: contract or implementation needs Codex E review before the
  next role.
- `blocked`: implementation cannot continue without new issue authority or user
  approval.

## Non-Claims

This contract does not claim:

- agent governance docs are correct;
- agent governance docs are complete;
- `tools/check_agent_docs.py` is decomposition-ready without review;
- CI enforcement is authorized;
- parser behavior is ready;
- parser truth is established;
- reliability readiness;
- security assurance;
- privacy assurance;
- release readiness;
- deploy readiness;
- production readiness;
- ARS clearance;
- Refactor Scout clearance.

## Recommended Next Role

Next role: Codex E - Module Reviewer.

Codex E should review this contract against issue #667, issue #665, PR #666,
and `tools/check_agent_docs.py`. If the contract is accepted, Codex E may route
to Codex C for a behavior-preserving same-repo decomposition implementation.
If any public-interface, CI, checked-surface, severity, ARS evidence, or
cross-repo authority ambiguity remains, Codex E should route back to Codex B.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #667.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/667

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Related ARS gate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/664

Source artifact:
docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md

Target candidate:
tools/check_agent_docs.py

Review goal:
Review the contract-only decomposition decision packet for the agent docs
consistency checker. Verify that it uses the #665 decision-packet vocabulary,
keeps same-repo decomposition as the only allowed later implementation route,
preserves the public CLI/report/exit-code/checked-file contract, rejects
cross-repo extraction, and avoids false ARS/refactor/readiness/security/privacy
authority claims.

Protected boundaries:
Do not implement code, move files, open a PR, run ARS or Refactor Scout, run
probes, mutate source repos, change parser/EventBus/API/frontend/live-capture/
workbook/webhook/Apps Script/CI behavior, or claim readiness, parser truth,
security assurance, or privacy assurance.

Expected output:
Findings first. State whether the contract is ready for Codex C, needs Codex B
clarification, or should be blocked. Include validation reviewed, remaining
risk, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/667"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/665"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/666"
  previous_merge_commit: "70191d1c11ac49d01ae308db1612e7669c304f9a"
  completed_thread: "B"
  next_thread: "E"
  verdict: "agent_docs_consistency_checker_decomposition_decision_packet_ready_for_review"
  target_artifact: "docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md"
  candidate_surface: "tools/check_agent_docs.py"
  candidate_id: "agent_doc_consistency_check"
  candidate_surface_class: "local_advisory_check_surface"
  final_decision: "same_repo_decomposition_candidate"
  implementation_authorized: false
  file_move_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  source_mutation_authorized: false
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
