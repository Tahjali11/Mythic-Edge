# Repo-Wide Agent Docs Consistency Checker Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/86

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Source handoff:

- PR #85 merged into `codex/repo-wide-hardening-run`
- Issue #84 closed
- Tracker #82 remains open

Related artifacts:

- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`

Agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Related ADRs:

- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`

Branch target: `codex/repo-wide-hardening-run`

This contract defines a deterministic consistency checker for Mythic Edge
agent, workflow, template, and ADR governance documents. It is a contract
artifact only. It does not implement the checker, edit CI, rewrite agent docs,
change parser/runtime/workbook/App Script behavior, target `main`, or mark
tracker #82 complete.

## Module

Repo-wide agent docs consistency checker.

Likely implementation artifact:

- `tools/check_agent_docs.py`

Likely tests:

- `tests/test_check_agent_docs.py`

The checker should inspect repo-owned governance documents for concrete drift:

- missing required files
- missing referenced repo-local files
- role-name and role-letter mismatches
- role-doc reference drift
- critical authority-order mismatches
- workflow handoff template/schema drift
- prompt and handoff schema reference drift
- ADR status and index mismatches
- archived document references being treated as active authority
- stale workflow, template, or protected-surface references

Plain English: this tool should catch obvious contradictions in the instructions
Codex threads use before those contradictions turn into wrong branch targets,
wrong role routing, stale handoff fields, or protected-surface mistakes.

## Owning Layer

Repository coordination and code-hardening workflow.

Truth boundary:

- The checker owns deterministic consistency validation for committed
  governance docs.
- The checker does not own the governance rules themselves. `AGENTS.md`,
  `docs/agent_rules.yml`, `docs/agent_constitution.md`, workflow docs, ADRs,
  current issues, and contracts remain the authority sources.
- The checker does not own parser truth, runtime behavior, workbook schema,
  webhook payload shape, Apps Script behavior, parser event classes, match/game
  identity, deduplication, final reconciliation, secrets, environment
  variables, raw logs, generated data, runtime status files, failed posts, or
  workbook exports.
- A clean checker result does not authorize governance rewrites or protected
  surface changes.
- A checker finding is a review signal. Fixing the finding may require a
  follow-up issue/contract when the fix changes authority or policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_agent_docs_consistency_checker.md`

Expected future implementation files owned by this contract:

- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md`
- `docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md`

Related files referenced but not owned by this contract:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/*.md`
- `docs/templates/*.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-*.md`
- `.github/workflows/repo-checks.yml`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this contract pass:

- PR #85 is merged into `codex/repo-wide-hardening-run`.
- Issue #84 is closed.
- `tools/check_secret_patterns.py` and `tests/test_check_secret_patterns.py`
  exist.
- `.github/workflows/repo-checks.yml` runs tests, protected-surface gate, and
  Ruff. It does not currently run `tools/check_secret_patterns.py` or any
  future `tools/check_agent_docs.py`.
- No stable agent-doc checker exists under `tools/check_agent_docs.py`.
- `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, and
  `docs/codex_module_workflow.md` all define the A-G workflow and Codex H
  auxiliary role, but no deterministic tool verifies that those definitions
  remain aligned.
- `docs/templates/workflow_handoff.md` defines the machine-readable handoff
  block shape.
- `docs/decisions/README.md` defines ADR status values, file naming, required
  fields, and an ADR index.
- `docs/agent_rules.yml` is machine-readable YAML-like configuration, but the
  project does not include PyYAML as a dependency. The first checker should not
  add a dependency just to parse this file unless a future contract authorizes
  dependency changes.

Current gap:

- Governance docs can drift without a focused local check catching missing
  files, stale references, role-name mismatches, authority-order mismatches,
  handoff field drift, or ADR index/status drift.

## Public Interface

### Primary CLI

Required repo-mode command:

```bash
python3 tools/check_agent_docs.py
```

Windows-compatible invocation:

```powershell
py tools\check_agent_docs.py
```

Required optional arguments:

- `--repo-root <path>`: repository root to inspect, default `"."`.
- `--format text|json`: text is required; JSON is optional in the first
  implementation.

Allowed future optional arguments:

- `--strict`
- `--warnings-as-errors`
- `--github-annotations`
- `--paths-from-stdin`
- `--base <git-ref>`

Those future flags must not be required for the baseline local invocation.
Changed-file or CI enforcement behavior requires a future contract update.

### Python Helper Surface

The stable public interface is the CLI. The implementation may expose helpers
for tests, such as:

- required-file manifest construction
- repo-local reference extraction
- simple YAML-like section extraction
- role registry extraction
- authority-order normalization
- workflow handoff block extraction
- ADR index extraction
- report rendering

These helpers are test-facing implementation details. Do not create runtime
parser dependencies on them.

## Inputs

### Required Governance Files

The checker must verify that these files exist:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_fixer.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/module_submitter.md`
- `docs/agent_threads/integration_deployer.md`
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/current_status.md`
- `docs/templates/constitution_feedback_packet.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`

The checker must also inspect every committed file matching:

- `docs/decisions/ADR-*.md`, excluding `docs/decisions/ADR_TEMPLATE.md`

### Machine-Readable Rule Index

Input file:

- `docs/agent_rules.yml`

Required parse scope:

- top-level `version`
- top-level `status`
- `document_architecture`
- `authority_order`
- `conflict_triage.order`
- `architecture_decision_records.statuses`
- `roles`
- `auxiliary_roles`
- `routing.normal_path`
- `prompt_schema.required`
- `handoff_schema.required`
- `branch_policy`
- `validation_gates`
- `archive_policy`

Parser constraint:

- The first implementation should use a small deterministic parser for this
  file's known shape or another standard-library-only approach.
- Do not add PyYAML or another dependency in this issue unless the contract is
  updated to authorize dependency changes.

### Markdown Governance Docs

Input files:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/*.md`
- `docs/templates/*.md`
- `.github/pull_request_template.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-*.md`

Required parse scope:

- repo-local paths in backticks
- repo-local Markdown links
- role names and role letters
- authority-order lists and critical ordering phrases
- workflow handoff template fields
- ADR status lines and README index table entries

Markdown parsing must stay conservative. The checker is not a full Markdown
link validator in the first implementation.

### GitHub Issue Template YAML

Input file:

- `.github/ISSUE_TEMPLATE/module_workflow.yml`

Required parse scope:

- referenced agent docs in the opening Markdown block
- form field `id` values
- risk tier options
- protected-surface default text

Parser constraint:

- Use a deterministic standard-library approach for the known file shape.
- Do not introduce a YAML dependency in this issue.

## Canonical Role Registry

The checker must treat this as the canonical role registry for this issue:

| ID | Canonical name | Required role doc | Normal path member |
| --- | --- | --- | --- |
| `A` | `Thinker` | `docs/agent_threads/problem_representation.md` | yes |
| `B` | `Module Contract Writer` | `docs/agent_threads/module_contract.md` | yes |
| `C` | `Module Implementer` | `docs/agent_threads/implementation.md` | yes |
| `D` | `Module Fixer` | `docs/agent_threads/module_fixer.md` | loopback |
| `E` | `Module Reviewer` | `docs/agent_threads/review.md` and `docs/agent_threads/contract_test.md` | yes |
| `F` | `Module Submitter` | `docs/agent_threads/module_submitter.md` | yes |
| `G` | `Integration Deployer` | `docs/agent_threads/integration_deployer.md` | yes |
| `H` | `Constitutional Lawyer` | `docs/agent_threads/constitutional_lawyer.md` | auxiliary only |

Allowed display aliases:

- `Codex A: Thinker`
- `Codex B: Module Contract Writer`
- `Codex C: Module Implementer`
- `Codex D: Module Fixer`
- `Codex E: Module Reviewer / Contract Tester`
- `Codex F: Module Submitter`
- `Codex G: Integration Deployer`
- `Codex H: Constitutional Lawyer`

Required role rules:

- A-G are the normal workflow roles.
- D is a loopback role, not part of the normal happy path.
- H is auxiliary governance, not part of the A-G implementation path.
- E may include contract-test mode, but E2 must not be treated as a permanent
  role unless a future contract authorizes it.

## Checks Required

### Required File Presence

Category: `missing_required_file`

The checker must error when a required governance file is missing.

### Referenced Repo-Local Files

Categories:

- `missing_referenced_file`
- `stale_path_reference`
- `archived_reference_active_context`

Required behavior:

- Extract repo-local paths from backticks and Markdown links in active
  governance docs.
- Ignore URLs, issue/PR links, anchors, shell commands, placeholders, and
  globs that are not meant to resolve to one file.
- For glob references such as `docs/agent_threads/*.md`, require at least one
  matching file.
- Do not treat files under `docs/archive/` as active authority.
- Warn when an active doc appears to cite an archived role-labeled draft as an
  active authority source.

### Role Consistency

Categories:

- `role_registry_mismatch`
- `role_doc_reference_mismatch`
- `normal_path_mismatch`
- `auxiliary_role_mismatch`

Required behavior:

- Compare `docs/agent_rules.yml` role IDs and names against the canonical role
  registry.
- Verify that every role doc named by the canonical registry exists.
- Verify that `AGENTS.md`, `docs/agent_constitution.md`, and
  `docs/codex_module_workflow.md` reference the A-G roles and Codex H
  auxiliary role.
- Verify that `routing.normal_path` in `docs/agent_rules.yml` and the normal
  path text in `docs/codex_module_workflow.md` both preserve:

```text
A -> B -> C -> E -> F -> G
```

- Verify that D is described as a loopback role.
- Verify that H is described as auxiliary/advisory and not a normal path
  member.

### Authority Order Consistency

Category: `authority_order_mismatch`

The checker must verify critical relative ordering, not exact prose equality.

Required critical ordering:

1. active system/developer instructions outrank repo docs
2. current user instructions outrank repo docs
3. `AGENTS.md` outranks `docs/agent_rules.yml`
4. `docs/agent_rules.yml` outranks `docs/agent_constitution.md`
5. current issue/problem representation and current contract outrank older
   handoffs, reports, examples, memory, and chat history
6. accepted ADRs are durable precedent below active governing docs and scoped
   issue/contract authority, and above stale memory or older examples
7. role docs and templates are workflow aids, not higher authority than the
   constitution/rule index/current issue/current contract
8. archived drafts are not active authority unless a current prompt explicitly
   names them as source artifacts

Allowed current-document nuance:

- `docs/agent_constitution.md` may express accepted ADR authority in its ADR
  section rather than as a separate numbered item in the main authority list.
  The checker should accept that if the critical relative ordering is preserved.

Do not require exact string equality between `authority_order` in YAML and
human-readable prose. That would be brittle and would create false positives
for harmless wording edits.

### Workflow Handoff Schema

Category: `handoff_schema_mismatch`

The checker must verify that `docs/templates/workflow_handoff.md` includes
these YAML block keys:

- `issue`
- `tracker`
- `completed_thread`
- `next_thread`
- `source_artifact`
- `target_artifact`
- `risk_tier`
- `branch`
- `validation`
- `stop_conditions`

The checker must verify that valid `next_thread` values are documented as:

- `A`
- `B`
- `C`
- `D`
- `E`
- `F`
- `G`
- `none`

The checker should verify that role docs and `docs/codex_module_workflow.md`
still require durable artifacts plus pasteable prompts plus workflow handoff
blocks for continuing work.

### Prompt And Handoff Rule Index Schema

Categories:

- `prompt_schema_mismatch`
- `handoff_rule_mismatch`

Required behavior:

- Verify that `docs/agent_rules.yml` includes `prompt_schema.required`.
- Verify that `docs/agent_rules.yml` includes `handoff_schema.required`.
- Verify that `docs/codex_module_workflow.md` has corresponding prompt and
  next-thread/handoff expectations.
- Verify that `.github/ISSUE_TEMPLATE/module_workflow.yml` includes source
  artifact, target artifact, branch, protected surfaces, validation, and stop
  condition fields.

### ADR Status And Index Checks

Categories:

- `adr_status_mismatch`
- `adr_index_mismatch`
- `adr_required_field_missing`

Required behavior:

- Extract allowed ADR statuses from `docs/decisions/README.md`.
- Extract allowed ADR statuses from
  `docs/agent_rules.yml:architecture_decision_records.statuses`.
- Error if those status sets differ.
- For every `docs/decisions/ADR-*.md` file except `ADR_TEMPLATE.md`, verify:
  - filename matches `ADR-0001-short-kebab-title.md` style
  - file has a `Status:` line
  - status is one of the allowed values
  - file appears in the README ADR index
  - README index status matches the file status
- Verify the README index does not point to a missing ADR file.
- Verify `ADR_TEMPLATE.md` exists and is not treated as a numbered ADR.

Recommended first implementation field checks:

- `# ADR-`
- `Status:`
- `Date:`
- `Decision owners / workflow role:`
- `Related issues:`
- `Related PRs:`
- `Related contracts, handoffs, or review reports:`
- `## Context`
- `## Decision`
- `## Scope`
- `## Non-Goals`
- `## Consequences`
- `## Truth Ownership Impact`
- `## Protected Surfaces`
- `## Validation Or Review Evidence`
- `## Supersedes`
- `## Superseded By`
- `## Follow-Ups`

If a current accepted ADR lacks a recommended field because of title casing or
minor heading wording, prefer warning over failure unless the README index or
status is wrong.

### Protected Surface And External Integration Rule Checks

Categories:

- `protected_surface_rule_mismatch`
- `external_surface_rule_mismatch`

Required behavior:

- Verify that the core forbidden local-artifact list appears in active docs:
  secrets, webhook URLs, API keys/tokens/credentials, local MTGA logs, failed
  posts, runtime status files, generated card data, and raw workbook exports.
- Verify that parser-owned truth must not move into workbook formulas,
  dashboard logic, Apps Script transport, webhook transport, or AI-generated
  interpretation.
- Verify that external tools/connectors/plugins/MCP servers/Google Docs/Google
  Sheets/OpenAI tooling are described as access/collaboration/evidence or
  transport surfaces by default, not repo authority or parser truth owners.
- These checks should be text-presence and relationship checks, not full
  natural-language proof.

### CI And Workflow Integration Check

Category: `ci_integration_unauthorized`

Required behavior:

- The first implementation must not edit `.github/workflows/repo-checks.yml`.
- The checker may inspect the workflow to report whether it is integrated, but
  it must not require integration.
- If `tools/check_agent_docs.py` is already present in CI without a future
  contract authorizing it, warn rather than fail in this issue.

## Findings And Severities

Severity values:

- `error`
- `warning`

Result values:

- `passed`: no findings
- `warning`: one or more warnings, no errors
- `failed`: one or more errors
- `error`: checker configuration/runtime failure

Exit codes:

- `0`: `passed` or `warning`
- `1`: `failed`
- `2`: `error`

Error severity should be used for:

- missing required governance files
- unreadable required files
- `docs/agent_rules.yml` shape errors that prevent role/authority extraction
- role registry mismatches that would change the meaning of A-G or H
- missing required workflow handoff fields
- ADR status set mismatches
- ADR README index entries that point to missing files
- numbered ADR files missing from the README index
- critical authority-order inversions

Warning severity should be used for:

- extra role docs not referenced by the current registry
- archived docs referenced in a way that could be confusing but not clearly
  active authority
- minor ADR heading wording differences where status/index still match
- non-critical stale local path references in examples or older reports
- future `check_agent_docs.py` CI integration before this contract authorizes
  enforcement
- governance concepts that are present but phrased differently enough that a
  reviewer should inspect them

The first implementation is a local/advisory tool. It must not be wired into CI
or made a required gate in this issue.

## Report Shape

Required text report:

```text
Agent Docs Consistency Check
mode: repo
checked_files: <n>
errors: <n>
warnings: <n>

ERROR <category> <path> - <reason>
WARNING <category> <path> - <reason>

result: passed|warning|failed|error
```

Required report behavior:

- Sort errors before warnings.
- Sort findings by category, path, then reason within severity.
- Keep reasons concise and actionable.
- Do not print raw private data, secrets, webhook URLs, workbook IDs, or raw
  logs if a future governance doc accidentally contains them. The secret
  scanner remains the primary tool for secret/private-marker redaction.
- Prefer stable category IDs over prose-only findings so Codex handoffs can
  cite exact failure modes.

## Compatibility And Archived Docs

Archived docs:

- Files under `docs/archive/` are not active authority.
- The checker should ignore archived files unless an active doc references
  them.
- A reference to an archived prior constitution as an archive is allowed.
- A reference that appears to make an archived draft active authority should
  warn.

Role-labeled V2 drafts:

- Role-labeled V2 drafts are archived artifacts after adoption.
- The checker should not require old role-labeled drafts to remain beside
  active rule files.

Current human-vs-machine source split:

- `docs/agent_constitution.md` remains human-readable.
- `docs/agent_rules.yml` remains the terse machine-readable rule index.
- The checker should compare critical invariants between them without forcing
  every human sentence to duplicate YAML.

## Side Effects

Allowed side effects:

- Read committed repo files.
- Read git metadata only if needed for path discovery.
- Print a deterministic report.
- Return a deterministic exit code.

Forbidden side effects:

- Do not write files.
- Do not edit CI.
- Do not rewrite agent docs.
- Do not update ADRs or templates.
- Do not open issues, PRs, or tracker comments.
- Do not call network services.
- Do not change parser/runtime/workbook/App Script behavior.
- Do not touch secrets, environment variables, raw logs, generated data,
  runtime status files, failed posts, or workbook exports.

## Error Behavior

Usage/configuration errors:

- invalid `--repo-root`
- unreadable repository root
- mutually incompatible flags if future flags are added
- filesystem errors that prevent reading required files

Policy ambiguity:

- Prefer warning over failure when a human-readable document preserves the
  concept but not the exact wording.
- Prefer error when a machine-readable source, required file, role registry,
  required handoff field, or ADR status/index entry is missing or contradictory.
- Route back to Codex B if implementing a check requires redefining authority,
  role names, ADR policy, workflow handoff schema, or CI enforcement.

## Dependency Order

Future implementation should proceed in this order:

1. Implement the report dataclasses/constants and CLI skeleton in
   `tools/check_agent_docs.py`.
2. Add required-file and repo-local-reference checks.
3. Add role registry and normal-path checks.
4. Add workflow handoff schema checks.
5. Add ADR status/index checks.
6. Add protected-surface/external-surface text-presence checks.
7. Add focused tests in `tests/test_check_agent_docs.py`.
8. Produce
   `docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md`.

Stop and route back to Codex B before:

- adding a dependency
- changing governance docs
- changing CI
- making warnings fail
- changing role definitions
- changing ADR policy
- changing protected-surface policy

## Required Tests

Focused tests for `tests/test_check_agent_docs.py`:

- CLI/report:
  - `python3 tools/check_agent_docs.py` reports the required shape
  - warning-only results exit `0`
  - error findings exit `1`
  - configuration/runtime errors exit `2`
  - findings are sorted deterministically
- Required files:
  - missing required governance file yields `missing_required_file`
  - existing required files pass
- Repo-local references:
  - missing backticked or Markdown-linked local file yields
    `missing_referenced_file`
  - globs require at least one matching file
  - URLs and anchors are ignored
  - archived references are ignored or warned according to context
- Roles:
  - A-G and H match the canonical registry
  - D is loopback-only
  - H is auxiliary and not part of the normal path
  - `routing.normal_path` preserves `A -> B -> C -> E -> F -> G`
  - role docs referenced in `AGENTS.md`, `agent_rules.yml`, constitution, and
    workflow docs exist
- Authority:
  - critical relative ordering is preserved
  - harmless wording differences do not fail
  - archived drafts are not treated as active authority
- Handoff/template:
  - `docs/templates/workflow_handoff.md` contains all required keys
  - valid `next_thread` values are documented
  - `.github/ISSUE_TEMPLATE/module_workflow.yml` includes source artifact,
    target artifact, branch, protected surfaces, validation, and stop condition
    fields
- ADR:
  - allowed status set in README matches `docs/agent_rules.yml`
  - ADR files have allowed statuses
  - README index matches ADR files and statuses
  - `ADR_TEMPLATE.md` is not treated as a numbered ADR
- Protected/external surfaces:
  - forbidden local-artifact and parser-truth ownership phrases are detected in
    active docs
  - external integration default-boundary phrasing is detected
- Compatibility:
  - `tools/check_secret_patterns.py --base origin/main` still exits `0`
  - `tools/check_protected_surfaces.py --base origin/main` still exits `0`

Implementation validation:

```bash
python3 -m pytest -q tests/test_check_agent_docs.py
python3 tools/check_agent_docs.py
python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
python3 -m ruff check src tests tools
git diff --check
```

Before submitter work:

```bash
python3 -m pytest -q tests
python3 -m ruff check src tests tools
python3 -m pyright
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Do not add CI validation for `check_agent_docs.py` in this issue.

## Acceptance Criteria

- `docs/contracts/repo_wide_agent_docs_consistency_checker.md` exists and links
  issue #86 and tracker #82.
- The contract names repository coordination and code-hardening workflow as the
  owning layer.
- The contract defines required files, expected references, role-name and
  role-letter consistency, authority-order consistency, handoff fields, ADR
  checks, archive handling, report shape, severity/exit behavior,
  advisory/blocking policy, tests, and validation obligations.
- The contract keeps CI edits, agent-doc rewrites, parser/runtime/workbook/App
  Script changes, and protected-surface changes out of scope for the contract
  writer pass.
- The contract routes implementation to Codex C and does not mark tracker #82
  complete.

## Open Questions And Contract Risks

- Human-readable authority prose will never match YAML one-to-one. The checker
  should enforce critical relative ordering, not exact wording.
- Standard-library-only parsing of YAML-like docs is intentionally narrow. If
  future docs become more complex, a dependency decision may need a separate
  contract.
- ADR required-field checks can be noisy if heading casing differs. The first
  implementation should prioritize status/index correctness.
- CI integration is explicitly deferred. The tool can still be useful as a
  local validation command and in Codex handoffs.
- The checker must not become a substitute for Codex review; it catches obvious
  consistency drift, not semantic governance quality.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer.

Codex C should implement the smallest deterministic repo-mode checker and
focused tests needed to satisfy this contract. It should not edit CI or rewrite
agent docs unless the implementation discovers a narrow blocker and routes back
for authorization first.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #86 and docs/contracts/repo_wide_agent_docs_consistency_checker.md.

Goal:
Compare the current repo-wide hardening governance docs against the agent docs consistency checker contract. Implement only the smallest deterministic checker, focused tests, and handoff needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/86
- https://github.com/Tahjali11/Mythic-Edge/issues/82
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/repo_wide_agent_docs_consistency_checker.md
- docs/contracts/repo_wide_secret_private_marker_scanner.md
- docs/contract_test_reports/repo_wide_hardening_baseline.md
- tools/check_secret_patterns.py
- tests/test_check_secret_patterns.py
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- AGENTS.md
- docs/agent_threads/*.md
- docs/templates/*.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- .github/pull_request_template.md
- docs/decisions/README.md
- docs/decisions/ADR-*.md

Do:
- Implement tools/check_agent_docs.py.
- Add focused tests in tests/test_check_agent_docs.py.
- Preserve deterministic local-only behavior and stable report output.
- Use standard-library-only parsing for the first implementation unless routed back for dependency authorization.
- Enforce concrete invariants: required files, repo-local references, roles, normal path, handoff fields, critical authority order, ADR status/index checks, protected-surface text presence, and external-surface boundary presence.
- Keep warnings non-failing.
- Produce docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md with comparison, changes made, validation run, open risks, CI decision, and next recommended role.

Do not:
- Edit CI unless separately authorized.
- Rewrite agent docs as part of this implementation unless a narrow blocker is routed back and approved.
- Add dependencies without contract authorization.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or protected surfaces outside this contract.
- Target main directly; work should continue on codex/repo-wide-hardening-run.
- Stage or commit unless explicitly asked.
- Mark tracker #82 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/86"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/repo_wide_agent_docs_consistency_checker.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "python3 -m pytest -q tests/test_check_agent_docs.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py"
    - "python3 tools/check_secret_patterns.py --base origin/main"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not edit CI unless separately authorized."
    - "Do not rewrite agent docs unless a narrow blocker is routed back and approved."
    - "Do not add dependencies without contract authorization."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces outside this contract."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
