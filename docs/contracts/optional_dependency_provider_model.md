# Optional Dependency Provider Model Contract

## Module

Optional dependency provider model for Mythic Edge hub-and-spokes architecture.

This contract defines the architecture policy and ADR implementation boundary
for optional public, private, local-only, and future high-risk providers. It is
not a provider runtime implementation contract.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/341
- Source refresh comment:
  https://github.com/Tahjali11/Mythic-Edge/issues/341#issuecomment-4763250481

Related context:

- https://github.com/Tahjali11/Mythic-Edge/issues/340
- https://github.com/Tahjali11/Mythic-Edge/issues/535
- https://github.com/Tahjali11/Mythic-Edge/issues/543

## Tracker

N/A.

## Owning Layer

Primary owner: Quality / Governance.

Future runtime ownership, if later separately contracted:

- Shared Support may own base provider interfaces and registry helpers.
- Analytics may consume parser-normalized facts through optional analytics
  providers.
- Local App / UI may display provider presence and status.
- External / Collaboration Surface may describe separately packaged public or
  private providers.
- Future AI Integration remains deferred and non-authorized.

## Internal Project Area

Quality / Governance; Shared Support; External / Collaboration Surface.

Adjacent areas:

- Analytics
- Local App / UI
- Corpus / Provenance
- Future AI Integration

Future AI Integration is deferred vocabulary only. Naming it in this contract
does not authorize OpenAI or model-provider runtime integration, AI coaching
evaluation, AI-owned parser truth, AI-owned analytics truth, hidden-card truth,
gameplay correctness truth, or strategic certainty.

## Truth Owner

The base Mythic Edge repository owns the optional provider policy, provider
interface vocabulary, and future registry/discovery contracts.

Parser/state remains the truth owner for MTGA event interpretation,
parser-managed match/game/card/action facts, match identity, game identity,
deduplication, and final reconciliation.

Analytics consumes parser-normalized facts and approved provenance. SQLite is
local queryable storage, not parser truth. Optional providers consume
base-owned DTOs, SQLite facts, and approved evidence labels. Optional providers
must not own parser truth, analytics truth, workbook truth, AI/coaching truth,
release readiness, deploy readiness, production behavior, hidden-card truth, or
gameplay advice.

## Bridge-Code Status

`deferred_future_boundary`

The ADR created after this contract may define future shared-support provider
interfaces and bridge-code boundaries, but this Codex B contract does not
authorize implementation.

## Risk Tier

High.

Reason: the immediate artifact is docs-only, but the policy defines future
dependency, privacy, provider discovery, optional private-repo, UI status, and
raw-data access boundaries. A weak policy could accidentally make private
providers required or create unsafe raw/private data paths.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/optional_dependency_provider_model.md`

Codex C may be authorized, under this contract, to create a docs-only ADR
package:

- `docs/decisions/ADR-0009-optional-dependency-provider-model.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/optional_dependency_provider_model_comparison.md`

This contract does not authorize edits to:

- runtime provider code;
- `pyproject.toml`;
- package dependencies or entry points;
- provider registry, discovery, adapters, services, CLIs, manifests, or SDKs;
- local app backend/frontend behavior;
- analytics schema, migrations, ingest, or views;
- parser behavior, parser state, parser event classes, or final
  reconciliation;
- workbook, webhook, Apps Script, Google Sheets, production, AI, model
  provider, or coaching surfaces;
- sibling repositories.

## Public Interface

The public interface for this slice is a docs/ADR policy interface, not a
runtime API.

Codex C should create proposed ADR-0009 unless the user explicitly reserves or
redirects ADR numbering. The ADR should define:

- base completeness without optional providers;
- provider vocabulary;
- provider interface and registry ownership;
- packaged-provider and local/dev-provider discovery boundaries;
- guarded import rules;
- data-access tiers;
- process-memory provider future/high-risk status;
- UI absence/presence behavior;
- boundary-script direction;
- fake/sample-provider and provider-error-state test expectations for later
  implementation;
- follow-up implementation slices that require separate contracts.

## Observed Current Behavior

- `main` currently includes ADR-0001 through ADR-0008.
- `ADR-0008` owns WIP-1 lane activation and is marked `Proposed`.
- `ADR-0009-optional-dependency-provider-model.md` does not currently exist.
- `pyproject.toml` currently declares only base dependencies and two optional
  dependency groups: `app` and `dev`.
- No provider entry-point group is currently defined.
- The README describes the base repo as local/open-core with parser,
  analytics, local app, setup tooling, tests, and docs in the local open core.
- Existing analytics contracts protect parser-normalized SQLite ingest and
  derived SQL views from raw Player.log storage or downstream truth ownership.
- Existing private-local-v1 docs treat local SQLite, JSONL imports, app logs,
  generated data, and Player.log evidence as private/local unless a later
  scoped contract explicitly authorizes safe handling.

## Inputs

### Governance Sources

Type: committed docs and current GitHub issue context.

Required sources for Codex C:

- issue #341 and latest Codex A refresh comment;
- related issues #340, #535, and #543;
- `AGENTS.md`;
- `docs/agent_constitution.md`;
- `docs/codex_module_workflow.md`;
- `docs/agent_rules.yml`;
- `docs/decisions/README.md`;
- `docs/decisions/ADR_TEMPLATE.md`;
- `docs/decisions/ADR-0001` through `docs/decisions/ADR-0008`;
- `pyproject.toml`;
- `README.md`;
- `docs/internal_project_map.md`;
- `docs/contracts/internal_project_boundaries.md`;
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`;
- `docs/private_local_v1_operator_guide.md`.

### Default Provider Inputs

These are the only default data classes a future provider model may treat as
eligible without a separate privileged-access contract:

- parser-normalized SQLite facts;
- deterministic SQL views over parser-normalized SQLite facts;
- stable base-owned DTOs;
- evidence, provenance, confidence, finality, degradation, and drift labels;
- non-sensitive provider capability config;
- provider status/config metadata that does not expose private paths, raw
  hashes, secrets, credentials, tokens, API keys, webhook URLs, raw payloads,
  or local-only artifacts.

### Privileged Provider Inputs

These inputs must require explicit capability flags plus a later issue and
contract. ADR-0009 may name them as privileged categories, but must not
authorize them:

- raw Player.log;
- raw UTC_Log;
- raw JSONL;
- local absolute paths;
- memory-derived facts;
- process-memory reads;
- credentials, secrets, tokens, API keys, OAuth grants, or webhook URLs;
- network access;
- external writes;
- OpenAI/model-provider runtime behavior;
- cloud upload or shared retention of private/local data.

### Forbidden Inputs

The provider model must not permit:

- hidden opponent hand, library, or unrevealed-card data;
- internal simulation state not visible to the user;
- memory writes, injection, patching, hooks, automation, or game
  manipulation;
- raw private logs or private JSONL payloads in committed provider fixtures;
- generated SQLite database files;
- workbook exports;
- runtime logs, failed posts, screenshots, private reports, or local-only
  artifacts;
- provider output as parser truth, analytics truth, workbook truth, AI truth,
  coaching truth, release readiness, deploy readiness, or production truth.

## Outputs

### Docs-Only ADR Package

Codex C should output:

- proposed ADR-0009 at
  `docs/decisions/ADR-0009-optional-dependency-provider-model.md`;
- ADR index update in `docs/decisions/README.md`;
- implementation handoff at
  `docs/implementation_handoffs/optional_dependency_provider_model_comparison.md`.

Runtime output, generated provider metadata, provider status files, registry
JSON, dependency changes, and UI changes are forbidden in this slice.

## Canonical Vocabulary

### `core_dependency`

A dependency required for base Mythic Edge install, import, parser capture,
manual import, SQLite ingest, built-in analytics, setup/status, and base UI
navigation.

Core dependencies must be public, installable without private GitHub access,
and safe for the base open-core path.

### `optional_provider`

A separately installed, configured, or discovered extension that may add
capabilities when present but is never required for base install, launch,
parser capture, manual import, SQLite ingest, built-in analytics, or base UI
navigation.

### `provider_family`

A coarse provider class such as:

- `analytics_foundation_extension`
- `analytics_intelligence`
- `corpus_provenance_tooling`
- `local_app_ui_extension`
- `ai_or_model_provider`
- `process_memory_provider`
- `cloud_service`
- `shared_support_tooling`

Family names are routing vocabulary only. They do not authorize implementation.

### `provider_registry`

The base-owned catalog of known or discovered providers, their identity,
capabilities, compatibility, status, and safe display metadata.

The registry must remain base-owned. Providers may supply metadata through an
approved interface, but they must not own the registry schema or base truth.

### `packaged_provider`

An optional provider installed as a Python package and discovered through a
future approved entry-point group.

Recommended future entry-point group:

```text
mythic_edge.providers
```

This contract does not add that entry-point group.

### `local_dev_provider`

An optional provider discovered through explicit local/dev manifest or config
under a later contract. Local/dev providers must not be discovered by arbitrary
folder scanning.

### `provider_capability`

A declarative capability label that tells the base app what a provider can do
and which access tier it requests. Capability labels are not permission by
themselves; privileged labels require a separate issue and contract.

### `provider_status`

A base-owned status value describing whether a provider is absent, present,
compatible, enabled, disabled, blocked, degraded, or failed.

Allowed ADR-level status vocabulary:

- `not_installed`
- `unavailable`
- `disabled`
- `available`
- `enabled`
- `incompatible`
- `misconfigured`
- `blocked_privileged_access`
- `error`
- `unknown`

### `provider_input_envelope`

A base-owned DTO or mapping passed to a provider. Default envelopes may include
only approved parser-normalized facts, derived views, stable DTOs, evidence
labels, and non-sensitive config.

### `provider_output_envelope`

A base-owned DTO or mapping returned by a provider. Provider output is
downstream enrichment or advisory output unless a later issue and contract
define a narrower deterministic truth boundary.

## Base Completeness Requirements

The base repo must work with zero optional providers installed.

The following must not require optional providers:

- package install;
- Python import of base modules;
- parser capture;
- manual JSONL import;
- local SQLite schema, migrations, ingest, and built-in analytics;
- local app setup/status;
- base UI navigation;
- built-in descriptive analytics;
- Match Journal base review surfaces;
- test suite execution for base features, except provider-specific tests gated
  by later contracts.

Provider absence must never be a startup exception, base navigation failure,
parser capture failure, manual import failure, SQLite ingest failure, or
built-in analytics failure.

## Discovery Model

The future provider discovery model should be hybrid:

1. Base repo owns provider registry and interface.
2. Packaged providers may use Python entry points.
3. Local/dev providers may use explicit manifest/config.
4. Imports are guarded and allowed only inside provider discovery or adapter
   paths.
5. No module-level imports from optional provider packages are allowed in base
   startup paths.
6. No arbitrary-folder scanning is allowed by default.
7. No private GitHub access is required for base install or setup.
8. No network, credential, external write, process-memory, or raw-log access is
   implied by provider discovery.

If a future provider needs service/API discovery, CLI execution, a local
service, or cross-repo package version negotiation, that provider class needs a
separate issue and contract.

## Version Compatibility Policy

A future provider must declare compatibility through base-owned metadata, such
as:

- provider id;
- provider family;
- provider version;
- provider interface version;
- minimum compatible base version;
- maximum compatible base version or compatibility range;
- required capabilities;
- requested data-access tier;
- optional feature flags.

Provider compatibility failure must degrade to `incompatible` or
`unavailable`, not crash the base app.

The ADR may recommend this metadata, but this Codex B contract does not
authorize implementing the metadata schema.

## Data-Access Tiers

### `default_read_only`

Allowed by default in the future provider model, subject to a later
implementation contract:

- parser-normalized SQLite facts;
- deterministic SQL views;
- stable base-owned DTOs;
- evidence/provenance/confidence/finality/degradation labels;
- non-sensitive provider capability config;
- symbolic provider status metadata.

### `privileged_local`

Requires a separate issue and contract:

- raw Player.log;
- raw UTC_Log;
- raw JSONL;
- local absolute paths;
- local runtime artifacts;
- local app-data contents;
- memory-derived facts;
- process attachment or process-memory reads.

### `privileged_external`

Requires a separate issue and contract:

- network access;
- external provider APIs;
- external writes;
- cloud upload;
- OAuth, service-account, token, credential, API key, secret, or webhook URL
  access;
- OpenAI/model-provider runtime behavior.

### `never_use`

Must remain forbidden unless a future human/legal/product decision creates a
new explicit rule outside this ADR:

- hidden opponent hand/library information;
- unrevealed card state;
- internal simulation state not visible to the user;
- game manipulation, automation, injection, hooks, memory writes, or patches;
- provider output used to override parser facts.

## Process-Memory Provider Boundary

Process-memory providers are a high-risk future optional provider category.
Issue #535 is the related deferred research/audit issue.

ADR-0009 may name process-memory providers as future/high-risk, but it must
explicitly not authorize:

- process attachment;
- memory reads;
- memory dumps;
- process hooks;
- game client manipulation;
- hidden-information use;
- cloud upload of process data;
- parser-truth replacement;
- implementation of #535.

Any future process-memory work requires its own issue, contract, privacy
review, capability matrix, stop conditions, and explicit user approval before
local execution.

## UI Absence And Presence Behavior

The base UI should not make users feel they have a broken or degraded product
when no optional providers are installed.

ADR-0009 should require:

- hide optional provider absence by default from ordinary base flows;
- show optional provider presence as added capability, not base repair;
- use neutral status text such as `No optional providers configured` only in
  setup/status surfaces where provider status is relevant;
- label provider errors as optional-module issues, not parser or base app
  failures;
- preserve built-in analytics as complete descriptive local analytics.

Forbidden UI behavior:

- base navigation disabled because a provider is absent;
- built-in analytics labeled as inferior, degraded, or incomplete solely
  because an optional provider is absent;
- exposing private provider names, paths, package URLs, credentials, or local
  details in public docs or committed fixtures.

## Boundary Script Policy

ADR-0009 may recommend a future provider-boundary checker, but must not
implement it.

Future checker direction:

- start with a narrow hard gate;
- use hardcoded privacy-forward invariants plus repo config;
- fail on forbidden unguarded optional-provider imports in base startup paths;
- fail on provider interfaces that expose raw logs, local paths, secrets,
  credentials, tokens, API keys, webhook URLs, raw hashes, private payloads, or
  generated local artifacts;
- fail on arbitrary-folder scanning;
- preserve breadcrumbs for later advisory checks that are not hard gates.

Any checker implementation or CI escalation needs its own issue and contract.

## Invariants

- Optional providers must never be required for base install, launch, parser
  capture, manual import, SQLite ingest, built-in analytics, or base UI
  navigation.
- Base repo owns the provider registry and interface vocabulary.
- Provider discovery must be explicit, guarded, and non-magical.
- Optional provider imports must not occur at module import time on base
  startup paths.
- Default provider data access is parser-normalized, read-only, and
  privacy-safe.
- Privileged local or external access requires separate issue and contract.
- Provider absence must degrade to status metadata, not base product failure.
- Provider output must not become parser truth, analytics truth, workbook
  truth, AI truth, coaching truth, release readiness, deploy readiness, or
  production truth.
- Process-memory providers remain future/high-risk and unauthorized here.
- ADR-0009 must not authorize runtime implementation by implication.

## Error Behavior

- Optional provider missing: report `not_installed` or `unavailable`; base
  behavior continues.
- Provider disabled: report `disabled`; do not import or execute provider.
- Provider incompatible: report `incompatible` with public-safe compatibility
  metadata; base behavior continues.
- Provider misconfigured: report `misconfigured` without exposing private
  paths, secrets, tokens, API keys, webhook URLs, or raw payloads.
- Provider throws an exception: report `error` for the optional provider; base
  parser, ingest, and UI routes remain available.
- Provider requests unauthorized privileged access: report
  `blocked_privileged_access`; do not grant access.
- Ambiguous provider interface or registry authority: route to Codex B before
  implementation.
- Existing ADR-0009 file found before Codex C starts: stop and ask the user or
  route back to Codex B for numbering reconciliation.

## Side Effects

Allowed Codex C side effects:

- add proposed ADR-0009;
- update ADR index;
- write implementation handoff;
- run docs validation and static scans.

Forbidden Codex C side effects under this contract:

- provider runtime code;
- dependency changes;
- entry-point groups;
- registry files;
- discovery code;
- boundary checker code;
- tests;
- UI changes;
- local app behavior changes;
- analytics schema or ingest changes;
- parser behavior changes;
- sibling-repo issues, PRs, or mutations;
- GitHub lifecycle changes beyond references in docs;
- staging, committing, pushing, opening PRs, merging, closing, or relabeling.

## Dependency Order

Codex C should edit in this order:

1. Verify checkout remote and current `main`.
2. Verify issue #341 remains the source issue and ADR-0009 is not already
   present.
3. Draft `docs/decisions/ADR-0009-optional-dependency-provider-model.md` from
   `docs/decisions/ADR_TEMPLATE.md`.
4. Update `docs/decisions/README.md`.
5. Write
   `docs/implementation_handoffs/optional_dependency_provider_model_comparison.md`.
6. Run validation.

## Compatibility

Existing base app install and development flows remain unchanged.

Existing optional dependency groups `app` and `dev` remain unchanged.

Existing analytics SQLite schema, migrations, ingest, and derived views remain
unchanged.

Existing private-local-v1 setup/install docs and symbolic-path privacy posture
remain unchanged.

Existing sibling-repo work remains related context only. This contract does not
adopt or mutate `Tahjali11/Mythic-Edge-Analytics`,
`Tahjali11/Mythic-Edge-Automation-Artifacts`, or any future spoke repo.

## Tests Required

For this Codex B contract:

```bash
python3 tools/check_agent_docs.py
git diff --check
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

For the later docs-only ADR implementation:

```bash
python3 tools/check_agent_docs.py
git diff --check
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

For later provider runtime implementation slices, each separate contract should
define focused tests for:

- base imports without providers installed;
- base launch/status/navigation without providers installed;
- fake/sample provider discovery through approved discovery path;
- missing provider state;
- disabled provider state;
- incompatible provider state;
- misconfigured provider state;
- provider exception/error state;
- unauthorized privileged-access request state;
- no arbitrary-folder scanning;
- no module-level optional-provider imports on base startup paths;
- no private GitHub access during base install;
- no raw Player.log, raw JSONL, local path, raw hash, secret, credential, API
  key, webhook URL, generated SQLite, or local-only artifact exposure.

## Acceptance Criteria

- Contract exists at `docs/contracts/optional_dependency_provider_model.md`.
- ADR-0009 is named as the recommended next ADR target unless the user
  explicitly reserves the number.
- Base completeness with zero optional providers is defined.
- Core dependency versus optional provider boundary is defined.
- Provider interface and registry ownership are defined.
- Packaged-provider and local/dev-provider discovery boundaries are defined.
- Guarded import boundaries are defined.
- Default and privileged data-access tiers are defined.
- Process-memory provider category is named as future/high-risk only.
- UI absence/presence behavior is defined.
- Boundary checker direction is defined without implementation.
- Later fake/sample-provider and provider-error-state test expectations are
  defined.
- Related issues #340 and #535 remain related/deferred, not implementation
  authority.
- No code, dependency, runtime, UI, parser, analytics, workbook, webhook, Apps
  Script, Google Sheets, AI/model-provider, coaching, release, deploy,
  production, or sibling-repo behavior is authorized.

## Open Questions Or Contract Risks

- A later issue must decide whether provider interfaces live in existing
  `src/mythic_edge_parser/app/` shared support, a new shared module, or a
  future package boundary.
- A later issue must decide exact DTO types, registry file shape, and provider
  entry-point group once implementation is authorized.
- A later issue must decide whether local/dev manifests are repo config,
  operator-local config, or both.
- A later issue must decide whether a provider-boundary checker is docs-only,
  advisory, or a required validation gate.
- A later issue must decide how `Tahjali11/Mythic-Edge-Analytics` consumes the
  base interface without becoming required for the base product.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Codex C should implement the docs-only ADR package. It must not implement
provider runtime behavior.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #341.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/341

Related issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/340
- https://github.com/Tahjali11/Mythic-Edge/issues/535
- https://github.com/Tahjali11/Mythic-Edge/issues/543

Base branch:
main

Contract:
docs/contracts/optional_dependency_provider_model.md

Goal:
Implement the docs-only Optional Dependency Provider Model ADR package. Create
proposed ADR-0009 unless the user explicitly reserves or redirects the number,
update the ADR index, and write the implementation handoff. Do not implement
provider code.

Target artifacts:
- docs/decisions/ADR-0009-optional-dependency-provider-model.md
- docs/decisions/README.md
- docs/implementation_handoffs/optional_dependency_provider_model_comparison.md

Before editing:
1. Verify the local checkout remote normalizes to
   https://github.com/Tahjali11/Mythic-Edge.
2. Fetch origin and verify the branch is based on current main.
3. Verify no ADR-0009 file already exists. If one exists, stop and route to
   Codex B or the user for numbering reconciliation.
4. Inspect issue #341, the Codex A refresh comment, the contract, ADR-0001
   through ADR-0008, pyproject.toml, README.md, docs/internal_project_map.md,
   docs/contracts/internal_project_boundaries.md,
   docs/contracts/live_app_parser_owned_fact_capture_sqlite.md, and
   docs/private_local_v1_operator_guide.md.

Protected boundaries:
- Do not implement provider registry, discovery, adapters, services, CLIs,
  manifests, SDKs, boundary scripts, tests, or UI.
- Do not edit pyproject.toml or add dependency groups, entry points, package
  dependencies, or private GitHub requirements.
- Do not create sibling-repo adoption issues or mutate sibling repos.
- Do not close or relabel existing issues.
- Do not authorize raw Player.log, raw UTC_Log, raw JSONL, local paths,
  process-memory reads, credentials, network access, external writes,
  OpenAI/model-provider runtime behavior, analytics truth, parser truth,
  workbook/webhook/App Script/Google Sheets behavior, release, deploy,
  production, hidden-card, gameplay advice, or coaching behavior changes.
- Do not make any optional provider required for base install, launch, parser
  capture, manual import, SQLite ingest, built-in analytics, or base UI
  navigation.
- Do not stage, commit, push, open a PR, merge, close, or relabel anything.

Validation:
- python3 tools/check_agent_docs.py
- git diff --check
- path-fed secret, protected-surface, and validation-selector checks for the
  changed docs files

Expected output:
- docs-only ADR package completed
- implementation handoff written
- validation summary
- remaining risks
- recommended next role
- workflow_handoff block with repository and repository_url
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/341"
  tracker: ""
  related_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/340"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/535"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/543"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #341 plus Codex A ADR-focused refresh comment"
  target_artifact: "docs/contracts/optional_dependency_provider_model.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  proposed_adr: "docs/decisions/ADR-0009-optional-dependency-provider-model.md"
  current_active_lane: "issue #341 selected by current user instruction"
  internal_project_area: "Quality / Governance; Shared Support; External / Collaboration Surface"
  truth_owner: "Parser/state owns parser truth; analytics consumes parser-normalized facts; optional providers consume base-owned interfaces and do not own upstream truth."
  bridge_code_status: "deferred_future_boundary"
  validation:
    - "Verified local main and origin/main at d330c7d43564065bbf5b6b8d5878189c988e20f7 before writing the contract."
    - "Verified docs/contracts/optional_dependency_provider_model.md did not already exist."
    - "Verified docs/decisions/ADR-0009-optional-dependency-provider-model.md did not already exist."
    - "Inspected issue #341, Codex A refresh comment, related issues #340/#535/#543, AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/module_contract.md, docs/templates/module_contract.md, docs/decisions/README.md, docs/decisions/ADR_TEMPLATE.md, ADR-0001 through ADR-0008, pyproject.toml, README.md, docs/internal_project_map.md, docs/contracts/internal_project_boundaries.md, docs/contracts/live_app_parser_owned_fact_capture_sqlite.md, and docs/private_local_v1_operator_guide.md."
    - "Ran git diff --check."
    - "Ran python3 tools/check_agent_docs.py."
    - "Ran python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin for docs/contracts/optional_dependency_provider_model.md."
    - "Ran python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin for docs/contracts/optional_dependency_provider_model.md."
    - "Ran python3 tools/select_validation.py --base origin/main --paths-from-stdin for docs/contracts/optional_dependency_provider_model.md."
    - "Ran ASCII and local-absolute-path marker scan on docs/contracts/optional_dependency_provider_model.md."
  stop_conditions:
    - "Do not implement provider code, registry, discovery, adapters, boundary script, tests, or UI in Codex B or the ADR-only Codex C pass."
    - "Do not edit pyproject.toml or add dependency groups, entry points, package dependencies, or private GitHub requirements."
    - "Do not create sibling-repo adoption issues or mutate sibling repos."
    - "Do not close or relabel existing work."
    - "Do not authorize raw log, process-memory, credential, network, external write, OpenAI/model-provider, analytics truth, parser truth, workbook, webhook, Apps Script, Google Sheets, release, deploy, production, hidden-card, gameplay advice, or coaching behavior changes."
    - "Do not make any optional provider required for the base repo install, launch, parser capture, manual import, SQLite ingest, built-in analytics, or base UI navigation."
```
