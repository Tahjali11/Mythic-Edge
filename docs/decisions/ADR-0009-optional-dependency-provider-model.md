# ADR-0009: Optional Dependency Provider Model

Status: Proposed

Date: 2026-06-21

Decision owners / workflow role:

- Codex A: ADR-focused refresh for issue #341.
- Codex B: Module Contract Writer for
  `docs/contracts/optional_dependency_provider_model.md`.
- Codex C: Module Implementer for this docs-only ADR proposal.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/341
- https://github.com/Tahjali11/Mythic-Edge/issues/340
- https://github.com/Tahjali11/Mythic-Edge/issues/535
- https://github.com/Tahjali11/Mythic-Edge/issues/543

Related PRs:

- TBD

Related contracts, handoffs, or review reports:

- `docs/contracts/optional_dependency_provider_model.md`
- `docs/implementation_handoffs/optional_dependency_provider_model_comparison.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/private_local_v1_operator_guide.md`

Related ADRs:

- `ADR-0002: Local Deterministic Scorer Decides, LLM Explains`
- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0005: External Integration And Collaboration Surfaces`
- `ADR-0006: Repository Boundary Strategy`
- `ADR-0008: Repo WIP-1 Lane Activation Policy`

## Context

Mythic Edge is moving toward a hub-and-spokes architecture. The base
repository must remain complete, installable, privacy-forward, and useful
without optional providers. Optional public, private, local-only, packaged,
experimental, research, analytics, UI, corpus/provenance, AI, or process-memory
providers may become useful later, but they must extend the base through
base-owned interfaces instead of becoming hidden required dependencies.

Issue #341 originally named the risk that a private analytics repository could
become a required dependency. The refreshed issue broadens that into a general
provider-model policy: optional providers can add capabilities when installed
or explicitly configured, but they must not own parser truth, analytics truth,
workbook truth, AI/coaching truth, release readiness, deploy readiness,
production behavior, hidden-card truth, or gameplay advice.

The current base package has only `app` and `dev` optional dependency groups
and no provider entry-point group. This ADR records the architecture policy
before any provider registry, discovery, adapter, checker, test, or UI work is
implemented.

## Decision

The base Mythic Edge repository must install, import, launch, capture parser
events, run manual import, ingest into SQLite, run built-in analytics, and
navigate the base UI with zero optional providers installed.

The base repository owns the optional provider vocabulary, provider interface
direction, provider registry direction, provider status vocabulary, capability
model, discovery boundary, and safe failure behavior. Optional providers are
consumers or extensions of base-owned interfaces. They are not truth owners.

The base-owned provider family vocabulary for future contracts is:

- `analytics_foundation_extension`
- `analytics_intelligence`
- `corpus_provenance_tooling`
- `local_app_ui_extension`
- `ai_or_model_provider`
- `process_memory_provider`
- `cloud_service`
- `shared_support_tooling`

Provider family labels are routing vocabulary only. They do not authorize code,
provider execution, privileged access, sibling-repo adoption, or dependency
changes.

The allowed ADR-level provider status vocabulary is:

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

Future provider contracts must preserve these status meanings unless a later
ADR or contract explicitly changes the vocabulary. Provider status is metadata
about an optional module. It is not parser truth, analytics truth, release
readiness, deploy readiness, or production readiness.

Provider capabilities must be declarative labels that describe what a provider
can do and which access tier it requests. Capability labels are never
permissions by themselves. Any privileged capability needs a separate issue,
contract, and approval path before implementation or local execution.

Future provider input and output envelopes must remain base-owned. Default
input envelopes may contain only approved parser-normalized facts, derived
views, stable DTOs, evidence labels, and non-sensitive config. Provider output
is downstream enrichment or advisory output unless a later issue and contract
define a narrower deterministic truth boundary.

Future provider discovery should be hybrid:

- packaged providers may use a future Python entry-point group such as
  `mythic_edge.providers`;
- local/dev providers may use explicit manifest or config under a later
  contract;
- imports must be guarded and allowed only inside future provider discovery or
  adapter paths;
- no module-level optional-provider imports are allowed in base startup paths;
- no arbitrary-folder scanning is allowed by default;
- no private GitHub access is required for base install or setup.

Provider data access is tiered.

Default read-only access may be designed later around parser-normalized SQLite
facts, deterministic SQL views, stable base-owned DTOs,
evidence/provenance/confidence/finality/degradation labels, non-sensitive
capability config, and symbolic provider status metadata.

Privileged local or external access requires a separate issue and contract.
Privileged access includes raw Player.log, raw UTC_Log, raw JSONL, local
absolute paths, local runtime artifacts, app-data contents, memory-derived
facts, process attachment, process-memory reads, network access, external
provider APIs, external writes, cloud upload, credentials, OAuth grants,
service accounts, tokens, API keys, secrets, webhook URLs, OpenAI runtime
behavior, or model-provider runtime behavior.

Process-memory providers are a future high-risk optional provider category.
This ADR names them for boundary planning only. It does not authorize process
attachment, memory reads, memory dumps, hooks, game client manipulation,
hidden-information use, cloud upload of process data, parser-truth
replacement, or implementation of issue #535.

The following provider inputs and behaviors remain forbidden unless a future
human, legal, or product decision creates a new explicit rule outside this ADR:

- hidden opponent hand or library information;
- unrevealed card state;
- internal simulation state not visible to the user;
- game manipulation, automation, injection, hooks, memory writes, or patches;
- provider output used to override parser facts.

Optional-provider failure must be non-breaking:

- missing providers report `not_installed` or `unavailable`;
- disabled providers report `disabled` and must not be imported or executed;
- incompatible providers report `incompatible` with public-safe compatibility
  metadata;
- misconfigured providers report `misconfigured` without exposing private
  paths, secrets, tokens, API keys, webhook URLs, or raw payloads;
- provider exceptions report `error` for the optional provider while base
  parser, ingest, and UI routes remain available;
- unauthorized privileged-access requests report `blocked_privileged_access`
  and must not grant access.

Provider absence must not make the base product appear broken. The base UI
should hide optional provider absence by default in ordinary flows and show
provider presence as an added capability. Setup/status surfaces may use neutral
wording such as `No optional providers configured` when provider status is
relevant.

Future provider-boundary tooling should start with narrow hard gates and may
add advisory checks later. Any checker implementation or CI escalation needs
its own issue and contract.

Future provider-boundary checks should fail on:

- unguarded optional-provider imports in base startup paths;
- provider interfaces that expose raw logs, local paths, secrets, credentials,
  tokens, API keys, webhook URLs, raw hashes, private payloads, generated local
  artifacts, or local-only artifacts;
- arbitrary-folder scanning.

Future provider runtime implementation contracts should include focused tests
for:

- base imports without providers installed;
- base launch, status, and navigation without providers installed;
- fake or sample provider discovery through an approved discovery path;
- missing provider state;
- disabled provider state;
- incompatible provider state;
- misconfigured provider state;
- provider exception or error state;
- unauthorized privileged-access request state;
- no arbitrary-folder scanning;
- no module-level optional-provider imports on base startup paths;
- no private GitHub access during base install;
- no raw Player.log, raw JSONL, local path, raw hash, secret, credential, API
  key, webhook URL, generated SQLite, or local-only artifact exposure.

## Scope

This ADR governs future optional provider architecture for
`Tahjali11/Mythic-Edge`.

It covers architecture policy and future contract direction for:

- core dependency versus optional provider vocabulary;
- provider family and provider status vocabulary;
- base-owned provider interface and registry direction;
- packaged-provider and local/dev-provider discovery boundaries;
- guarded optional-provider import boundaries;
- default and privileged data-access tiers;
- process-memory provider future/high-risk status;
- UI absence/presence behavior;
- later provider-boundary checker direction;
- later fake/sample-provider and provider error-state testing expectations.

## Non-Goals

This ADR does not:

- implement provider code
- implement a provider registry
- implement provider discovery
- implement provider adapters, services, CLIs, manifests, or SDKs
- implement a provider-boundary script
- add tests
- change UI behavior
- edit `pyproject.toml`
- add dependency groups, entry points, package dependencies, or private GitHub
  requirements
- require any optional provider for base install, launch, parser capture,
  manual import, SQLite ingest, built-in analytics, setup/status, Match
  Journal, or base UI navigation
- create sibling-repo adoption issues
- mutate sibling repositories
- authorize raw Player.log, raw UTC_Log, raw JSONL, local path,
  process-memory, credential, network, external write, OpenAI/model-provider,
  hidden-card, gameplay advice, AI, coaching, release, deploy, or production
  behavior
- change parser behavior, parser state final reconciliation, parser event
  classes, match identity, game identity, deduplication, analytics truth,
  workbook schema, webhook payload shape, Apps Script behavior, or Google
  Sheets behavior

## Alternatives Considered

- Let optional providers be ordinary Python imports. Rejected because module
  imports in base startup paths can turn optional providers into hidden core
  dependencies.
- Limit the policy to private analytics providers. Rejected because the same
  boundary applies to public providers, local/dev providers, corpus helpers,
  UI extensions, AI/model providers, cloud services, and future process-memory
  providers.
- Discover providers by scanning arbitrary folders. Rejected because it risks
  privacy leaks, local path dependence, unreviewed code loading, and confusing
  base-install behavior.
- Treat provider output as parser or analytics truth. Rejected because
  optional extensions must not override upstream truth owners.
- Implement a registry, checker, and fake provider in this ADR slice. Rejected
  because this issue authorizes policy only; runtime implementation needs
  later contracts.

## Consequences

Future provider work has a narrow path: first define base-owned interfaces,
registry shape, discovery rules, capability metadata, status values, and
failure behavior under separate contracts. Runtime implementation cannot rely
on this ADR alone.

The benefit is that the base product remains complete without optional
providers and future providers can be reviewed as explicit extensions. The
cost is that even useful provider ideas need more ceremony before code exists.
That ceremony is intentional because providers can touch privacy, optional
private repos, packaging, local artifacts, raw logs, process memory, external
services, credentials, and AI/model-provider surfaces.

## Truth Ownership Impact

This ADR preserves parser truth ownership and downstream analytics boundaries.

Parser/state remains the truth owner for MTGA event interpretation,
parser-managed match/game/card/action facts, match identity, game identity,
deduplication, and final reconciliation.

Analytics consumes parser-normalized facts and approved provenance. SQLite is
local queryable storage, not parser truth. Optional providers consume
base-owned DTOs, parser-normalized SQLite facts, deterministic SQL views, and
approved evidence labels when later contracts authorize those interfaces.

Optional providers must not own parser truth, analytics truth, workbook truth,
AI/coaching truth, release readiness, deploy readiness, production behavior,
hidden-card truth, gameplay advice, or merge readiness.

## Protected Surfaces Touched

No runtime protected surfaces are touched by this ADR.

This ADR does not authorize changes to parser behavior, parser state final
reconciliation, parser event classes, workbook schema, webhook payload shape,
Apps Script behavior, Google Sheets behavior, analytics schema, analytics
ingest, local app behavior, frontend behavior, CI gates, release policy,
deploy policy, production behavior, secrets, raw logs, generated artifacts,
private artifacts, local-only files, process-memory access, network access,
external writes, OpenAI runtime behavior, or model-provider runtime behavior.

## Validation Or Review Evidence

This ADR proposal is docs-only. Runtime tests are not required because no
runtime code changed.

Expected implementation validation is recorded in
`docs/implementation_handoffs/optional_dependency_provider_model_comparison.md`.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Review this proposed ADR through the normal Codex E, F, and G path before
  treating it as accepted durable precedent.
- Create a separate provider-interface and registry contract before writing
  provider runtime code.
- Create a separate discovery contract before adding entry points,
  local/dev manifests, config, or import paths.
- Create a separate provider-boundary checker contract before adding scripts
  or CI gates.
- Create separate contracts for any analytics provider, UI extension,
  AI/model-provider, cloud service, local/dev provider, or process-memory
  provider.
- Keep issue #535 as deferred research/audit context for process-memory
  providers unless explicitly activated later.

## Notes

Optional provider presence should feel additive. Provider absence should not
make the base local product feel broken, incomplete, or dependent on a private
spoke.
