# Security CWE-Mapped Local Validation Profile Contract

## Module

`security_cwe_mapped_local_validation_profile`

Plain English: this contract defines a repo-owned, local validation profile that
maps Mythic Edge's preventive security checks to exact CWE IDs. A CWE is a
"Common Weakness Enumeration" entry: a public identifier for a class of
software weakness. This profile should make local security checks easier to
explain, review, and extend without changing CI, enforcing new gates, mutating
CodeQL alerts, or claiming security assurance.

This is a Codex B contract artifact only. It does not implement code, change
CI, enable enforcement, update CodeQL alert state, change parser behavior, read
private data, or certify that Mythic Edge is secure.

## Source Issue

- Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/590
- Parent security issue: https://github.com/Tahjali11/Mythic-Edge/issues/330
- Previous alert-triage issue: https://github.com/Tahjali11/Mythic-Edge/issues/331
- Previous alert-triage PR: https://github.com/Tahjali11/Mythic-Edge/pull/336
- Contract artifact:
  `docs/contracts/security_cwe_mapped_local_validation_profile.md`

## Risk Tier

High.

Reasons:

- security vocabulary can create false confidence if it is too broad;
- CWE mappings must use exact, active, vulnerability-mappable entries;
- local validation output may mention sensitive paths, snippets, or artifact
  categories if not constrained;
- CodeQL currently has no open alerts, so this contract must preserve
  preventive posture without pretending that "0 open alerts" means security
  assurance;
- future enforcement would affect developer workflow and CI, but enforcement
  is not authorized by this issue.

## Owning Layer

Primary owner: Quality / Governance security validation.

Supporting owners:

- GitHub CodeQL/code scanning for external alert evidence;
- `tools/check_secret_patterns.py` for content-based private-marker and secret
  scanning;
- `tools/check_protected_surfaces.py` for repo-relative protected and
  forbidden path classification;
- focused tests for workflow permission posture and future profile validators.

## Internal Project Area

Quality / Governance.

Adjacent areas:

- External / Collaboration Surface for GitHub code scanning and workflow
  permissions;
- Generated / Local Artifacts for logs, private outputs, and local evidence;
- Local App / UI where operator-selected paths may enter the system;
- Parser only as a protected surface that must not be changed by this contract.

## Truth Owner

This profile owns only deterministic security-validation vocabulary and
reporting boundaries.

It does not own:

- parser truth;
- parser behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- CodeQL alert truth or alert lifecycle state;
- vulnerability existence truth;
- security assurance or privacy assurance.

CodeQL findings are evidence signals, not implementation authority and not final
project truth. A future local validation profile may reference CodeQL rule IDs
as provenance, but it must not dismiss alerts, mutate alerts, or treat old
alerts as permission to change unrelated code.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
Issue #590 contract
  -> exact CWE vocabulary and local validation profile schema
  -> later reviewed docs/profile/test implementation, if authorized
  -> optional future advisory local reports
  -> optional future enforcement issue only after clean baseline and approval
```

Forbidden reverse flow:

- local security validation must not change parser truth or parser behavior;
- CodeQL alert state must not mutate profile decisions automatically;
- scanner success must not claim security assurance;
- profile rows must not authorize CI blocking or broad cleanup;
- local/private evidence must not be committed to justify CWE status.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`
- issue #590
- parent issue #330
- previous issue #331
- previous PR #336
- `docs/contracts/codeql_code_scanning_alert_triage.md`
- `docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md`
- `docs/contract_test_reports/codeql_code_scanning_alert_triage.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/repo_wide_protected_surface_authorization_checker.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_protected_surfaces.py`
- `tests/test_github_workflow_permissions.py`
- public CWE reference pages and CodeQL query-help pages for the mapped
  weakness families.

## Observed Current Behavior

Observed in the issue-specific clean worktree for this contract pass:

- branch:
  `codex/security-cwe-mapped-local-validation-profile-590`;
- base:
  `origin/main`;
- current CodeQL alert count from GitHub API:
  - open: `0`;
  - fixed: `3`;
  - dismissed: `14`.

Existing repo support:

- `tools/check_secret_patterns.py` can classify secret/private-marker content
  and already redacts sensitive excerpts.
- `tools/check_protected_surfaces.py` can classify forbidden and protected
  paths by repo-relative path.
- `tests/test_github_workflow_permissions.py` verifies the repo checks workflow
  uses read-only token permissions.
- The previous CodeQL contract and handoffs document prior path-injection,
  URL-host validation, and workflow-permission findings.

Current gap:

- There is no single repo-owned profile that maps these local preventive checks
  to exact CWE families, distinguishes scanner provenance from project claims,
  and defines advisory-versus-enforcement rollout rules.

## Problem Statement And First Bad Value

The first bad value is an imprecise security label that cannot be reviewed
against an exact weakness family.

Examples:

- "path validation issue" without distinguishing CWE-22 path traversal from
  CWE-73 external control of filename/path;
- "workflow permission issue" mapped to CWE-275 as a finding ID even though
  CWE-275 is a CWE category and not a directly vulnerability-mappable weakness;
- "information exposure" mapped to broad or discouraged entries such as
  CWE-2000 or CWE-200 rather than an active, specific entry such as CWE-538 or
  CWE-532;
- "URL issue" without distinguishing general input validation from substring
  denylist problems or redirect/fetch behavior.

The contract fix is a constrained local profile schema with exact CWE IDs,
approved mapping rules, and fail-closed behavior for ambiguous or placeholder
mappings.

## Scope Decision

In scope for this contract:

- CWE-mapped local validation profile vocabulary;
- exact v1 risk-family mappings;
- advisory report shape;
- local output safety rules;
- future profile/validator implementation boundaries;
- future enforcement preconditions.

Out of scope for this contract:

- implementation code;
- CI changes;
- CodeQL alert mutation;
- enforcement or fail-under behavior;
- private evidence reads;
- parser behavior changes;
- broad security cleanup;
- source or dependency updates;
- claims that the repo is secure or private.

## CWE Mapping Policy

A profile row must use exact, active CWE IDs.

Allowed profile finding IDs:

- CWE entries with MITRE vulnerability mapping status `ALLOWED`;
- CWE entries with mapping status `ALLOWED-WITH-REVIEW` or equivalent limited
  review wording, when the row explains why the entry is specific enough for
  the finding family;
- related CWE IDs that clarify narrower adjacent risk, when the primary CWE is
  still exact and vulnerability-mappable.

Forbidden profile finding IDs:

- placeholder or invented IDs;
- broad CWE views, categories, pillars, or organizational buckets;
- CWE IDs with MITRE vulnerability mapping status `DISCOURAGED` as a primary
  profile finding ID;
- CWE IDs with MITRE vulnerability mapping status `PROHIBITED`;
- `CWE-2000` or similar comprehensive dictionary/view identifiers;
- `CWE-275` as a profile finding ID. It may appear only as CodeQL scanner
  provenance for workflow-permission alerts because it is a CWE category, not
  the profile's directly mapped weakness.
- `CWE-20` and `CWE-200` as primary profile finding IDs. They may appear only
  as CodeQL scanner provenance, umbrella context, or rationale for choosing a
  more specific CWE because MITRE marks them `DISCOURAGED`.

Required fields for each CWE mapping:

- `primary_cwe_id`;
- `primary_cwe_title`;
- `primary_cwe_mapping_status`;
- `primary_cwe_reference`;
- `related_cwe_ids`;
- `scanner_cwe_provenance`;
- `discouraged_or_prohibited_cwe_provenance`;
- `mapping_rationale`;
- `mapping_review_status`.

Allowed `mapping_review_status` values:

- `accepted_exact`;
- `accepted_related`;
- `needs_review`;
- `rejected_too_broad`;
- `rejected_discouraged_mapping`;
- `rejected_prohibited_mapping`;
- `rejected_placeholder_or_invented`.

Fail-closed rule:

- If a future profile row cannot name an exact allowed or allowed-with-review
  primary CWE, the row must use `mapping_review_status: needs_review` or a
  `rejected_*` status and must not appear in enforcement, blocking output,
  review-ready output, or assurance language.
- If a scanner maps a query to a discouraged CWE, the profile row must preserve
  that scanner tag only as provenance and select a more specific allowed
  primary CWE before any advisory finding is considered review-ready.

Reviewer-blocker repair:

- `CWE-PROFILE-E-001` is addressed by preventing `url_host_validation` from
  using discouraged CWE-20 as its primary finding ID.
- `CWE-PROFILE-E-002` is addressed by preventing
  `secret_private_artifact_exposure` from using discouraged CWE-200 as its
  primary finding ID.
- `CWE-PROFILE-E-003` is addressed by clarifying that
  `workflow_permission_scope` uses CWE-732 as the local profile's primary
  mapping for workflow token permission assignment, keeps CWE-276 as related
  default-permission context, and keeps CWE-275 as prohibited CodeQL scanner
  provenance only.

## V1 Risk-Family Map

| Family ID | Primary CWE | Related CWE IDs | Intended local validation surface | Current status |
| --- | --- | --- | --- | --- |
| `local_path_traversal` | CWE-22 Improper Limitation of a Pathname to a Restricted Directory | CWE-73 | Operator-selected local paths, imports, generated path joins, path containment checks | contract-only/advisory |
| `generated_filename_id_to_path` | CWE-73 External Control of File Name or Path | CWE-22 | Status filenames, IDs transformed into filesystem names, generated artifact paths | contract-only/advisory |
| `subprocess_command_line_invocation` | CWE-78 Improper Neutralization of Special Elements used in an OS Command | CWE-88 | `subprocess` and shell command construction in repo-owned tools | contract-only/advisory |
| `url_host_validation` | CWE-187 Partial String Comparison | CWE-1023, CWE-184, optional CWE-601 only for redirect behavior, optional CWE-918 only for outbound fetch/proxy behavior, CodeQL CWE-20 as scanner provenance only | URL parsing, exact-host checks, substring host validation avoidance | contract-only/advisory |
| `secret_private_artifact_exposure` | CWE-538 Insertion of Sensitive Information into Externally-Accessible File or Directory | CWE-532, CWE-200 as discouraged umbrella context only | Secret/private marker output, local paths, raw logs, workbook exports, runtime artifacts | contract-only/advisory |
| `temporary_file_handling` | CWE-377 Insecure Temporary File | optional CWE-378/CWE-379 only if permissions/location semantics are directly present | Temporary files and temporary directories in tools or reports | contract-only/advisory |
| `workflow_permission_scope` | CWE-732 Incorrect Permission Assignment for Critical Resource | CWE-276 for inherited/default permission posture; CodeQL CWE-275 as scanner provenance only | GitHub Actions `permissions:` posture and least-privilege workflow defaults | contract-only/advisory |

## Family Details

### `local_path_traversal`

Purpose:

- Detect local path handling that could escape an intended directory or accept
  unsafe path components.

Primary CWE:

- CWE-22.

Related CWE:

- CWE-73 when external input controls a path or filename before containment is
  applied.

Allowed evidence:

- repo-relative source locations;
- tests that use synthetic paths;
- CodeQL rule provenance such as `py/path-injection`;
- public-safe sanitized reports.

Forbidden evidence:

- real local absolute paths;
- raw Player.log paths;
- user home directory paths;
- private app-data paths;
- raw source snippets in public reports when the scanner output is intended to
  be symbolic.

Expected status behavior:

- `advisory_match` for an observed local check finding;
- `no_finding` when a validated containment helper rejects traversal;
- `review_required` when the path source or intended containment root is
  unclear;
- `unsupported` for paths outside this repo's authority.

### `generated_filename_id_to_path`

Purpose:

- Detect generated filenames or IDs that reach filesystem operations without a
  safe, deterministic slug/filename boundary.

Primary CWE:

- CWE-73.

Related CWE:

- CWE-22 when path traversal or directory escape is possible.

Allowed evidence:

- synthetic IDs;
- repo-relative generated-output code references;
- public-safe unit tests;
- symbolic filename examples such as `<synthetic-id>`.

Forbidden evidence:

- real match IDs from private logs;
- raw runtime status filenames from local app data;
- local generated artifact paths.

Expected status behavior:

- `advisory_match` when untrusted or semi-trusted IDs can influence filenames;
- `review_required` when an ID source is unclear;
- `no_finding` when the helper restricts output to an approved filename
  alphabet and fixed directory.

### `subprocess_command_line_invocation`

Purpose:

- Detect shell or subprocess usage that may allow command injection, argument
  injection, or unsafe option injection.

Primary CWE:

- CWE-78.

Related CWE:

- CWE-88 when the risk is argument, option, or switch injection rather than
  shell metacharacter execution.

Allowed evidence:

- repo-relative tool paths;
- symbolic command component names;
- synthetic argument examples;
- test-only command doubles.

Forbidden evidence:

- real secrets in command examples;
- private paths;
- executable payload strings;
- exploit reproduction or bypass instructions.

Expected status behavior:

- `advisory_match` for `shell=True`, command string assembly, or untrusted
  command fragments;
- `no_finding` for fixed argv lists with validated repo-relative inputs;
- `blocked` when an example would require exploit payload details.

### `url_host_validation`

Purpose:

- Detect URL validation that uses unsafe substring checks or incomplete parsing.

Primary CWE:

- CWE-187.

Primary mapping rationale:

- The historical CodeQL query is tagged with CWE-20, but CWE-20 is
  `DISCOURAGED` by MITRE and must not be used as the profile's primary finding
  ID.
- The Mythic Edge v1 profile family is narrower than generic input validation:
  it is about partial or substring comparison of URL text instead of parsing
  the URL and checking the host component. CWE-187 is an allowed variant-level
  mapping for partial string comparison.

Related CWE:

- CWE-1023 as the broader incomplete-comparison parent family;
- CWE-184 when the issue is incomplete denylist or blacklist behavior;
- CWE-601 only when redirect behavior is actually present;
- CWE-918 only when server-side request/fetch/proxy behavior is actually
  present.

Discouraged scanner provenance:

- CodeQL `py/incomplete-url-substring-sanitization` currently carries
  `external/cwe/cwe-020`. The local profile may record that as
  `scanner_cwe_provenance: ["CWE-20"]`, but it must also record
  `primary_cwe_id: "CWE-187"` for this family unless a later review identifies
  an even more specific allowed CWE for the exact sink.

Allowed evidence:

- symbolic URLs such as `https://allowed.example.invalid/path`;
- exact-host parser tests;
- CodeQL provenance such as `py/incomplete-url-substring-sanitization`.

Forbidden evidence:

- live webhook URLs;
- workbook URLs;
- private deployment URLs;
- credential-bearing query strings.

Expected status behavior:

- `advisory_match` when substring host checks are used;
- `no_finding` when a parsed hostname, scheme, and exact allowlist are used;
- `review_required` when the URL sink is unclear.

### `secret_private_artifact_exposure`

Purpose:

- Detect private or sensitive material in public docs, reports, tests, fixtures,
  logs, or generated artifacts.

Primary CWE:

- CWE-538.

Primary mapping rationale:

- CWE-200 is `DISCOURAGED` by MITRE and describes information exposure at a
  broad class level. It must not be used as the profile's primary finding ID.
- Mythic Edge's local profile family is narrower: it is about inserting or
  allowing sensitive/private information into public repository files,
  externally visible reports, or log-like artifacts. CWE-538 is allowed for
  sensitive information placed into externally accessible files or directories.

Related CWE:

- CWE-532 when sensitive data is written to logs or log-like artifacts;
- CWE-200 as discouraged umbrella context only, not as a primary or blocking
  profile finding label.

Allowed evidence:

- scanner category IDs;
- redacted excerpts;
- symbolic private-marker categories;
- repo-relative paths when paths are public-safe.

Forbidden evidence:

- raw secret values;
- API keys;
- tokens;
- webhook URLs;
- local absolute paths;
- private log content;
- raw Player.log or UTC_Log content;
- workbook exports;
- SQLite databases;
- runtime/generated private artifacts.

Expected status behavior:

- `advisory_match` or `blocked` for sensitive output depending on exposure
  severity;
- `warning_only` for explicitly redacted placeholder examples in policy docs;
- `no_finding` for synthetic examples with safe placeholder context.

### `temporary_file_handling`

Purpose:

- Detect temporary file creation patterns that may create predictable,
  reusable, or permission-unsafe temporary files.

Primary CWE:

- CWE-377.

Related CWE:

- CWE-378 or CWE-379 only if a later implementation distinguishes insecure
  permissions or insecure temporary directory location.

Allowed evidence:

- repo-relative source locations;
- symbolic temporary filenames;
- synthetic tests.

Forbidden evidence:

- real local temporary paths;
- raw generated private artifacts;
- private runtime file contents.

Expected status behavior:

- `advisory_match` for predictable temporary names or deprecated unsafe helpers;
- `review_required` for legitimate durable local output that is not temporary;
- `no_finding` for standard-library safe temporary file APIs used without
  leaking private content.

### `workflow_permission_scope`

Purpose:

- Detect GitHub Actions workflows that rely on broad default token permissions
  or request write scopes without issue-specific authorization.

Primary CWE:

- CWE-732.

Primary mapping rationale:

- The local profile classifies a GitHub Actions workflow permission finding as
  an incorrect permission assignment for a security-critical automation
  resource: the workflow token and its repository/API access scope.
- CWE-732 is `ALLOWED-WITH-REVIEW` and covers security-critical resources that
  can be read or modified by unintended actors when permissions are assigned
  too broadly.
- For this profile, the "critical resource" is not a deployed production
  system and not parser/runtime behavior. It is the repository automation token
  and the workflow-level or job-level permission declaration that constrains
  that token.
- CWE-732 must be used only for local validation findings about workflow
  permission scope shape, such as missing explicit permissions, broader-than
  needed write scopes, or write scopes without issue-specific justification.
  It must not be generalized into a claim that the repository is vulnerable,
  exploited, production-unsafe, or security-assured.

Related CWE:

- CWE-276 when the specific concern is inherited or implicit default
  permissions, such as a workflow with no explicit `permissions:` block relying
  on repository or organization defaults.

Related mapping rationale:

- CWE-276 is `ALLOWED` and is useful as related context for default permission
  posture, but it is not the primary profile mapping because MITRE's description
  is centered on installed file permissions. The Mythic Edge workflow finding is
  about automation token scope and permission assignment, so CWE-732 is the
  profile primary.

Scanner provenance:

- CodeQL may tag missing workflow permissions under external CWE category
  CWE-275. This profile must not use CWE-275 as the finding ID because CWE-275
  is a category-level entry with prohibited vulnerability mapping.
- CodeQL's `actions/missing-workflow-permissions` rule remains allowed as
  scanner provenance. The local profile must record it separately from the
  profile mapping as:
  - `codeql_rule_ids: ["actions/missing-workflow-permissions"]`;
  - `scanner_cwe_provenance: ["CWE-275"]`;
  - `discouraged_or_prohibited_cwe_provenance: ["CWE-275"]`;
  - `primary_cwe_id: "CWE-732"`;
  - `related_cwe_ids: ["CWE-276"]` when the trigger is missing or inherited
    default permissions.

Allowed evidence:

- workflow filenames;
- symbolic permission names;
- tests such as `tests/test_github_workflow_permissions.py`;
- public workflow YAML snippets only when no secrets are present.

Forbidden evidence:

- workflow tokens;
- secrets;
- credential names with live values;
- changes to GitHub settings or alerts.

Expected status behavior:

- `advisory_match` for a missing top-level or job-level `permissions:` block
  when the workflow would otherwise inherit repository or organization token
  defaults;
- `advisory_match` for explicit write scopes that lack issue-specific
  justification in the local validation context;
- `no_finding` for explicit least-privilege read-only posture, such as
  `contents: read`, when no write scope is needed for that workflow;
- `review_required` for workflows that appear to need write scope, because a
  human contract/review must verify whether the scope is intentionally required
  before any future implementation changes workflow YAML;
- `unsupported` when classification would require inspecting GitHub
  organization/repository token default settings, secrets, live run context, or
  external workflow runtime state not available in public repo files.

Non-authoritative boundaries:

- A local `workflow_permission_scope` finding is a report-only advisory signal.
- It does not prove the effective runtime `GITHUB_TOKEN` permissions, because
  organization and repository defaults may differ and the profile must not
  inspect or mutate GitHub settings in this issue.
- It does not authorize editing workflow YAML, changing CI, enabling
  enforcement, dismissing CodeQL alerts, or adding status checks.
- It does not claim exploitability, production risk, release readiness,
  security assurance, or privacy assurance.
- It must not be used as a general permission or authorization finding for
  application code; it is scoped to GitHub Actions workflow permission
  declarations and the local advisory profile only.

## Local Profile Schema

A later implementation may add a profile manifest only after review authorizes
that implementation. Recommended path:

- `docs/security/cwe_mapped_local_validation_profile.v1.json`

The manifest must be public-safe and deterministic.

Required envelope fields:

- `schema_version`: string, initially `1`;
- `profile_id`: `mythic_edge.security.cwe_mapped_local_validation_profile`;
- `repository`: `Tahjali11/Mythic-Edge`;
- `repository_url`: `https://github.com/Tahjali11/Mythic-Edge`;
- `contract_ref`:
  `docs/contracts/security_cwe_mapped_local_validation_profile.md`;
- `source_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/590`;
- `parent_issue`: `https://github.com/Tahjali11/Mythic-Edge/issues/330`;
- `generated_at_policy`: `manual_or_test_only`;
- `profile_status`: one of `contract_only`, `advisory_profile`,
  `advisory_local_check`, `blocking_candidate`, `blocking_enabled`;
- `enforcement_authorized`: boolean, must remain `false` until a later issue
  explicitly authorizes enforcement;
- `codeql_alert_mutation_authorized`: boolean, must remain `false`;
- `families`: array of family records.

Required family fields:

- `family_id`;
- `title`;
- `summary`;
- `primary_cwe_id`;
- `primary_cwe_title`;
- `primary_cwe_mapping_status`;
- `primary_cwe_reference`;
- `related_cwe_ids`;
- `scanner_cwe_provenance`;
- `discouraged_or_prohibited_cwe_provenance`;
- `codeql_rule_ids`;
- `local_detector_ids`;
- `local_test_refs`;
- `allowed_evidence`;
- `forbidden_evidence`;
- `reporting_policy`;
- `rollout_status`;
- `non_claims`.

The manifest must not contain:

- local absolute paths;
- raw source snippets;
- secrets;
- private evidence;
- raw logs;
- generated runtime artifacts;
- CodeQL alert dismissal metadata;
- vulnerability proof payloads;
- exploit steps;
- production readiness claims.

## Advisory Report Shape

A future local report may be produced only as an advisory artifact unless a
later issue authorizes enforcement.

Required report envelope fields:

- `schema_version`;
- `profile_id`;
- `repository`;
- `base_ref`;
- `head_ref`;
- `source_profile_ref`;
- `run_mode`;
- `overall_status`;
- `families_checked`;
- `findings`;
- `warnings`;
- `blocked_items`;
- `non_claims`;
- `validation_commands`.

Allowed `run_mode` values:

- `local_changed_files_advisory`;
- `local_all_repo_advisory`;
- `contract_review_only`;
- `ci_report_only_candidate`.

Allowed `overall_status` values:

- `passed_advisory`;
- `warning_advisory`;
- `failed_advisory`;
- `blocked`;
- `unsupported`;

Report findings may include:

- family ID;
- primary CWE ID;
- related CWE IDs;
- detector ID;
- severity label;
- repo-relative path when public-safe;
- line number only when it does not expose private data;
- symbolic reason category;
- redacted excerpt only when the scanner proves it is safe;
- recommended next review role.

Report findings must not include:

- raw source snippets by default;
- fix edits;
- local absolute paths;
- private marker filenames when the filename itself is private;
- secret values;
- raw log values;
- workbook exports;
- raw CodeQL SARIF blobs;
- exploit reproduction details.

## Status Vocabulary

Allowed profile-row statuses:

- `contract_only`;
- `advisory_available`;
- `advisory_match`;
- `warning_only`;
- `no_finding`;
- `review_required`;
- `blocked`;
- `unsupported`;
- `blocking_candidate`;
- `blocking_enabled`.

Allowed readiness flags:

- `implementation_authorized`;
- `ci_change_authorized`;
- `enforcement_authorized`;
- `codeql_alert_mutation_authorized`;
- `parser_behavior_change_authorized`;
- `security_assurance_claimed`;
- `privacy_assurance_claimed`.

For this issue, all readiness flags above must remain `false`.

## Advisory Versus Enforcement Boundary

This contract authorizes only contract text.

Advisory profile work in a later issue may:

- add a public-safe profile manifest;
- add a validator that checks manifest schema and CWE mapping policy;
- add focused tests for the manifest/validator;
- run existing local scanners manually and summarize only public-safe symbolic
  output.

Advisory profile work must not:

- add CI gates;
- fail PRs;
- block merges;
- dismiss CodeQL alerts;
- write GitHub status checks;
- update workflow permissions unless that future issue explicitly authorizes
  the workflow edit;
- claim security or privacy assurance.

Blocking enforcement requires a later issue and contract proving:

- clean advisory baseline;
- no unresolved false-positive classes;
- reviewed public-safe report output;
- explicit user approval for enforcement;
- documented rollback path;
- Codex E review;
- Codex F/G submitter/deployer routing.

## CodeQL Relationship

CodeQL is an upstream scanner and evidence source.

This profile may reference CodeQL rule IDs, including:

- `py/path-injection`;
- `py/incomplete-url-substring-sanitization`;
- `actions/missing-workflow-permissions`.

This profile must not:

- mutate CodeQL alert state;
- dismiss alerts;
- reopen alerts;
- treat alert absence as proof of security;
- treat an old alert as permission for broad refactors;
- use CodeQL category tags as direct profile finding IDs when the CWE entry is
  not vulnerability-mappable.

If future CodeQL state changes, the profile remains valid as preventive
vocabulary but any report that references alert counts must refresh live state.

## Inputs

Allowed inputs:

- this contract;
- public repo source files;
- public repo docs;
- public repo tests;
- public GitHub issue and PR metadata;
- public CodeQL rule IDs and alert counts;
- public MITRE CWE reference pages;
- existing scanner outputs that contain only public-safe symbolic values;
- synthetic test examples.

Forbidden inputs:

- private Player.log or UTC_Log files;
- app-data contents;
- live MTGA data;
- private smoke data;
- local absolute paths;
- secrets;
- tokens;
- API keys;
- webhook URLs;
- workbook exports;
- SQLite databases;
- raw CodeQL SARIF containing private local paths or snippets;
- exploit payloads or bypass details;
- generated/private/runtime artifacts.

## Outputs

This contract outputs:

- `docs/contracts/security_cwe_mapped_local_validation_profile.md`

Future outputs, only if separately authorized:

- public-safe profile manifest;
- public-safe schema tests;
- public-safe advisory validation reports;
- implementation handoff comparison.

No current output may:

- create or update CI;
- create or update GitHub Actions permissions;
- create CodeQL alert comments or dismissals;
- write private artifacts;
- publish security findings;
- claim security assurance.

## Protected-Surface Invariants

- Parser behavior must remain unchanged.
- Parser truth ownership must remain unchanged.
- Workbook, webhook, Apps Script, analytics, AI, and production behavior must
  remain unchanged.
- Existing local private-data boundaries must remain intact.
- Local validation output must be symbolic and redacted by default.
- CWE IDs must be exact and reviewable.
- Broad/placeholder CWE mappings must fail closed.
- Scanner success must not become readiness, release, deployment, security, or
  privacy assurance.

## Error And Refusal Behavior

The future profile or validator must refuse with symbolic reasons when:

- a family lacks an exact primary CWE;
- a primary CWE has prohibited vulnerability mapping;
- a row uses a placeholder/invented CWE;
- a row tries to include private evidence;
- a report tries to emit raw source snippets, fix edits, secrets, local paths,
  raw logs, or private marker filenames;
- a caller asks the advisory profile to enforce CI without explicit authority;
- a caller asks the profile to mutate CodeQL alert state;
- a caller asks the profile to claim security or privacy assurance.

Allowed refusal reason IDs:

- `cwe_mapping_missing`;
- `cwe_mapping_too_broad`;
- `cwe_mapping_prohibited`;
- `cwe_mapping_placeholder_or_invented`;
- `private_evidence_forbidden`;
- `unsafe_report_output`;
- `enforcement_not_authorized`;
- `codeql_alert_mutation_not_authorized`;
- `security_assurance_not_authorized`;
- `unsupported_surface`.

## Compatibility

The profile must remain compatible with:

- existing CodeQL triage docs for #331;
- existing repo-wide secret/private-marker scanner behavior;
- existing protected-surface checker behavior;
- existing workflow-permission tests.

The profile must not require old CodeQL alerts to remain open. Historical alert
IDs may be mentioned only as provenance in docs, not as current truth.

## Future Validation Expectations

Later Codex C, if explicitly authorized after review, should provide:

```bash
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
python3 -m pytest -q tests/test_github_workflow_permissions.py
python3 -m pytest -q <future_profile_validator_tests>
git diff --check
```

If a JSON profile manifest is introduced:

```bash
python3 -m json.tool docs/security/cwe_mapped_local_validation_profile.v1.json >/dev/null
python3 <future_profile_validator> docs/security/cwe_mapped_local_validation_profile.v1.json
```

Validation must not:

- run private logs;
- run live MTGA;
- run private smoke checks;
- mutate GitHub alerts;
- change CI;
- enable enforcement.

## Acceptance Criteria

- The contract names exact CWE mappings for each v1 risk family.
- The contract rejects broad, placeholder, prohibited, or invented CWE IDs.
- The contract distinguishes CodeQL scanner provenance from Mythic Edge profile
  finding IDs.
- The contract preserves advisory-only status for issue #590.
- The contract defines public-safe profile and report shapes for later work.
- The contract preserves all protected surfaces and false readiness flags.
- Validation confirms the contract is public-safe and whitespace clean.

## Next Workflow Action

Next role: Codex E reviewer.

Codex E should review the contract for exact CWE mapping accuracy, false
authority language, public-safe output policy, and whether the workflow should
route to a later docs/profile implementation issue or back to Codex B.

Pasteable Codex E prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #590.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/590

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/331

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/336

Artifact to review:
docs/contracts/security_cwe_mapped_local_validation_profile.md

Review focus:
- exact CWE mapping accuracy;
- rejection of broad, placeholder, prohibited, or invented CWE IDs;
- CodeQL provenance versus Mythic Edge profile finding IDs;
- advisory-only boundary and absence of enforcement/CI/alert mutation authority;
- public-safe report output policy;
- protected-surface and non-claim preservation.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not change CI.
- Do not enable enforcement.
- Do not mutate CodeQL alerts.
- Do not run private logs or read private artifacts.
- Do not change parser behavior.
- Do not claim security assurance or privacy assurance.

Expected output:
- Findings first, if any.
- Review verdict.
- Validation evidence reviewed.
- Recommended next role.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/590"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/331"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/336"
  completed_thread: "B"
  next_thread: "E"
  verdict: "cwe_mapped_local_validation_profile_contract_ready_for_review"
  target_artifact: "docs/contracts/security_cwe_mapped_local_validation_profile.md"
  risk_tier: "High"
  branch: "codex/security-cwe-mapped-local-validation-profile-590"
  wip_exception: "security_preventive_profile_planning"
  implementation_authorized: false
  ci_change_authorized: false
  enforcement_authorized: false
  codeql_alert_mutation_authorized: false
  parser_behavior_change_authorized: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  validation:
    - "python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin < changed-path list"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "git diff --check"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change CI or enable enforcement."
    - "Do not mutate CodeQL alerts."
    - "Do not run private logs or inspect private artifacts."
    - "Do not change parser behavior or parser truth ownership."
    - "Do not claim security assurance or privacy assurance."
```
