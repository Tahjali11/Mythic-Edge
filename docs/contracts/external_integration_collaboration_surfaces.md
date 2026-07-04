# External Integration And Collaboration Surfaces Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/79

Tracker: N/A

Branch target: future implementation branch must be confirmed by issue #79 or
the user before Codex C implementation. This contract-writing pass ran on
`main` with only this contract untracked.

Source artifacts inspected:

- issue #79
- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/module_contract.md`
- `docs/templates/constitution_feedback_packet.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- prior draft/source contract at this path

This is a contract-writing artifact only. It does not implement governance
changes, edit authority docs, create or edit ADRs, add runtime integrations,
change parser/runtime/workbook/webhook/App Script behavior, install or
authorize connectors/plugins/MCP servers, create or rotate secrets, change
environment variables, add OpenAI API runtime integration, edit live Google
Docs or Google Sheets, implement coaching evaluation, open a PR, merge
anything, or close issues.

## Module

External integration and collaboration surfaces governance.

Plain English: Mythic Edge may use external tools to collaborate, inspect,
research, publish, and explain. Those surfaces are useful, but by default they
are access, collaboration, research, evidence, transport, or explanation
layers. They must not silently become parser truth, deterministic analytics
truth, repo authority, schema authority, merge/deploy authority, credential
authority, or production state.

## Source Issue

https://github.com/Tahjali11/Mythic-Edge/issues/79

Issue #79 is the durable problem representation for this contract. It asks the
repo to define external tools and collaboration spaces as access and
collaboration surfaces, not truth or authority surfaces.

Issue #79 also states:

- OpenAI API runtime integration remains split to a separate issue and
  contract.
- Coaching evaluation remains split to a separate issue and contract.
- The likely implementation should include durable governance docs/rules and
  likely an ADR.

## Owning Layer

Owning layer: repository coordination, external integration governance, and
agent collaboration workflow.

Truth boundary:

- Parser/state remains the truth owner for MTGA event interpretation and
  normalized match/game facts.
- Deterministic local code owns future scoring or evaluation decisions only
  when separately contracted.
- AI/LLM output may explain, summarize, classify, compare, enrich, recommend,
  or hypothesize, but does not own parser-managed truth.
- External tools, connectors, plugins, MCP servers, Google Docs, Google
  Sheets, browser sessions, shell helpers, local skills, OpenAI documentation
  tooling, and external data sources are not authority surfaces by default.
- Repo authority remains governed by active instructions, `AGENTS.md`,
  `docs/agent_rules.yml`, `docs/agent_constitution.md`, current issues,
  current contracts, accepted ADRs, and reviewed workflow artifacts.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/external_integration_collaboration_surfaces.md`

Expected future implementation artifacts if issue #79 authorizes Codex C work:

- `docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md`
- a proposed ADR, likely
  `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md` or
  the next available ADR number
- `docs/decisions/README.md`, only to index the new ADR
- narrow entries in `docs/agent_rules.yml`
- narrow narrative references in `docs/agent_constitution.md` and
  `docs/codex_module_workflow.md`
- optional short entrypoint reminder in `AGENTS.md`
- optional narrow references in role docs or templates when needed

Future implementation must not create secrets, credentials, live external
connections, OpenAI API calls, Google Docs content, Google Sheets content,
MCP/plugin configuration, production deployments, raw data exports, workbook
exports, runtime code, or coaching evaluation behavior under this contract.

## Observed Current Behavior

Observed during this contract pass:

- Current branch was `main`.
- Working tree had only the untracked draft contract at this path.
- Issue #79 is open and labeled `workflow:problem`.
- Existing governance already protects parser truth, AI/LLM boundaries,
  protected surfaces, Codex H advisory status, and local artifact/secret
  safety.
- `docs/agent_rules.yml` already contains a `tool_surface_boundary` under
  `constitution_feedback`, but the repo does not yet have a dedicated durable
  ADR for external integration and collaboration surfaces.
- `docs/agent_threads/constitutional_lawyer.md` already tells Codex H to treat
  tools, plugins, connectors, MCP servers, and local skills as tool surfaces
  unless a repo artifact explicitly grants authority.
- `docs/codex_module_workflow.md` already says tools, plugins, connectors, MCP
  servers, and local skills should be treated as access or collaboration
  surfaces unless current repo authority says otherwise.
- Existing ADRs cover parser truth ownership, LLM explanation boundaries, and
  protected-surface authorization, but not external integration and
  collaboration-surface governance as its own durable decision.

Observed gap:

- External integration surfaces are not yet consolidated in one durable policy
  or ADR.
- Google Sheets and Google Docs future collaboration roles need explicit
  boundaries.
- Local skills, MCPs, plugins, and connectors need a durable boundary that is
  not limited to Codex H synthesis.
- OpenAI documentation tooling needs to stay clearly separate from OpenAI API
  runtime integration.
- Secret, credential, environment variable, data-retention, and human approval
  boundaries need one canonical external-tool policy.
- Coaching evaluation needs explicit split-to-separate-issue treatment.

## Public Interface

This contract defines governance vocabulary and boundaries, not runtime APIs.

### External Integration Surface

An external integration surface is any tool, service, account, connector,
plugin, API, document, spreadsheet, browser session, automation helper, or
remote system outside repo-owned parser/runtime code that can read, write,
transmit, store, summarize, or influence Mythic Edge work.

Examples:

- GitHub issues, PRs, comments, checks, and Actions
- Google Drive, Google Docs, Google Sheets, and Google Slides
- live Mythic Edge workbooks and deck-testing workbooks
- Google Apps Script deployments and webhook receivers
- OpenAI documentation tooling
- OpenAI API runtime integrations
- MCP servers
- plugins and connectors
- browser automation sessions
- shell automation helpers
- local Codex skills
- external card, metagame, matchup, or strategy data sources
- email, chat, calendar, or collaboration connectors
- file export/import tools

### Collaboration Surface

A collaboration surface is a place where humans and agents coordinate work.

Examples:

- GitHub issues and PRs
- Google Docs notes and comments
- Google Sheets planning or analysis tabs
- feedback packet issue comments
- Codex chat output
- local skill instructions
- implementation handoffs and review reports

Collaboration surfaces may carry evidence, discussion, handoffs, proposed
decisions, and user notes. They do not become repo authority until adopted by
the repo workflow.

### Authority Surface

Authority surfaces are sources that can govern Mythic Edge work under the
current constitution and rule index.

Examples:

- active system, developer, and current user instructions
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- current GitHub issue or problem representation
- current module contract
- accepted ADRs
- reviewed implementation handoffs, review reports, and PRs as scoped evidence

External tools, skills, plugins, connectors, MCP servers, Google Docs, Google
Sheets, and AI outputs are not authority surfaces by default.

## Required Guarantees

### Google Sheets Boundaries

Google Sheets may support:

- structured review
- human annotations
- testing queues
- experiment tracking
- analytics snapshots
- downstream storage for parser-produced rows
- dashboards, reports, helper tabs, and analysis views

Google Sheets must not own:

- parser truth
- workbook schema truth
- drift recovery truth
- deterministic scoring or evaluation authority
- merge/deploy authority

Workbook formulas, helper tabs, dashboards, and manually edited cells must not
override parser-managed facts such as match result, game result, play/draw,
mulligans, opening hand, card actions, deck submission, row identity, workbook
schema, or parser-managed fields.

For workbook-connected work, future threads must distinguish:

- repository code state
- live workbook state
- deployed Apps Script state
- local exported workbook files

Live Google Sheets edits require explicit user approval when they write cells,
change formulas, alter schema or tab names, change sharing/permissions, affect
dashboard/helper logic, import/export private workbook data, or affect
production-facing or personal analysis data.

Read-only Google Sheets connector use may support user-requested analysis, but
responses must identify source workbook/tab/range when accuracy matters and
must not treat a sheet view as parser truth.

### Google Docs Boundaries

Google Docs may support:

- AI-drafted and human-reviewed memos
- sideboard guides
- matchup notes
- tournament prep
- planning drafts
- comments
- constitution feedback packets
- research summaries

Google Docs content is not repo authority by default. A Google Doc becomes
repo-relevant only when a current issue, contract, PR, accepted ADR, or merged
repo artifact cites it as evidence or imports reviewed content.

Google Docs edits require explicit user approval when they change user-owned
documents, add or resolve comments, alter sharing/permissions, include private
deck/workbook/strategy/account details, or store sensitive material.

Do not store secrets, raw logs, webhook URLs, workbook IDs, credentials,
runtime status files, failed posts, generated data, or unrelated private
transcript content in Google Docs.

### Local Codex Skills

Local Codex skills are instruction helpers. They may provide routing guidance,
task-specific steps, reusable prompts, or helper-script references.

Local skills are not repo authority. If a local skill conflicts with current
repo docs, the current repo authority wins. If local skill behavior should
become durable policy, route it through issue, contract, implementation,
review, and PR.

Local skills must not:

- silently override `AGENTS.md`, `docs/agent_rules.yml`, or the constitution
- become parser truth
- create or store secrets without explicit approval
- commit local-only machine paths as durable repo policy
- bypass A-G workflow gates

### MCP, Plugin, And Connector Boundaries

MCP servers, plugins, and connectors are tool-access surfaces. They may help
read, search, write, comment, inspect, or automate external systems only when
the current user request and active workflow role authorize that action.

They are not truth or authority layers by default.

Connector output may be incomplete, stale, permission-limited, or unavailable.
Threads must name those limitations when they matter and fall back to safer
repo-local or CLI sources when appropriate.

Writes through MCPs, plugins, or connectors require explicit user intent and
must respect active workflow role boundaries.

Examples:

- Codex B must not use a connector to implement authority-doc changes.
- Codex E must not use a connector to silently fix code in review-only mode.
- Codex F may publish only reviewed scope after user authorization.
- Codex G may merge or deploy only after explicit user approval and gates pass.

Connector permissions must not be expanded, installed, or modified just because
a task would be easier with broader access. Ask the user when installation,
authorization, sharing, or permission changes are needed.

### OpenAI Docs Tooling Versus OpenAI API Runtime Integration

OpenAI documentation tooling means using official docs, docs connectors, or
developer references to answer questions or guide implementation.

OpenAI documentation tooling:

- is research/reference support
- does not create runtime project behavior
- does not require project API keys
- does not transmit Mythic Edge runtime data by itself
- does not make OpenAI docs or model output project authority

OpenAI API runtime integration means repo code, scripts, deployments, or
services that call the OpenAI API or another model provider during Mythic Edge
operation.

OpenAI API runtime integration requires a separate issue and module contract.
It must define:

- purpose and owning layer
- deterministic local decision owner
- model output labels
- prompt/data payload boundaries
- secret and environment variable contracts
- retention and logging policy
- validation plan
- failure/degradation behavior
- human approval requirements
- protected surfaces touched or explicitly not touched

This contract does not authorize OpenAI API runtime integration.

### Secret, Credential, Environment Variable, And Approval Boundaries

Secrets, credentials, API keys, tokens, webhook URLs, OAuth grants, service
accounts, connector permissions, and environment variable contracts are
protected surfaces.

Future implementation must not:

- invent, rotate, delete, print, commit, or overwrite credentials
- add API keys to docs, fixtures, tests, prompts, logs, comments, or examples
- include webhook URLs, workbook IDs, raw logs, failed posts, runtime status
  files, generated data, workbook exports, or local-only artifacts
- change environment variable names or required values without explicit issue,
  contract, review, and validation
- request broader OAuth scopes or connector permissions without human approval

If a task requires credential setup, the thread must stop and ask for human
approval, then document only redacted names and expected environment variable
keys.

### Data-Retention Boundaries

External systems can retain data. Future implementation must define retention
behavior before sending project data to a new external surface.

Default retention policy:

- do not send raw MTGA logs to external tools
- do not send secrets, webhook URLs, workbook IDs, failed posts, runtime
  status files, raw workbook exports, or generated local artifacts
- minimize shared data to the fields required for the task
- redact private identifiers where possible
- prefer summaries over raw private payloads
- do not create durable external copies unless explicitly authorized
- label any externally stored artifact as evidence, not parser truth

If a connector or API may log or retain data outside the repo, the thread must
name that risk before use when project-private data is involved.

### Human Approval Boundaries

Explicit human approval is required before:

- changing live Google Sheets, Google Docs, Drive permissions, or sharing
- changing Apps Script deployments or webhook receiver behavior
- creating, rotating, deleting, or exposing secrets or credentials
- adding OpenAI API runtime integration or model-provider dependencies
- sending raw or sensitive project data to an external API
- changing production deployment behavior
- merging to `main` or production branches
- installing or authorizing new connectors/plugins with broader account access
- changing external retention, export, or publication behavior
- performing destructive external operations

Read-only connector use is allowed when the user request clearly requires it
and the active workflow role permits it. If the data is sensitive or the tool's
retention behavior is unclear, pause and ask.

### AI And Coaching Boundaries

AI/LLM output may explain, summarize, classify, compare, enrich, recommend, or
hypothesize from parser-produced facts and deterministic analytics.

AI/LLM output must not own parser-managed facts, deterministic scoring,
workbook schema, merge/deploy readiness, credential policy, or accepted repo
authority.

Coaching evaluation must be split into a separate issue.

That future issue should define:

- coaching goals
- endpoints or outputs
- deterministic evaluation owner
- scoring or rubric logic
- source data
- prompt boundaries if AI is used
- confidence labels
- privacy policy
- validation evidence
- acceptance criteria

This external-integration contract may be cited by the future coaching issue
for tool, privacy, and data-sharing boundaries, but it must not become the
coaching evaluation contract.

## Inputs

Allowed inputs for future implementation:

- issue #79
- this contract
- final merged repo governance docs
- accepted ADRs
- local skill instructions as evidence only
- connector/plugin/MCP documentation as evidence only
- user-provided external integration requirements
- redacted examples of workflow friction

Forbidden inputs:

- secrets or credential values
- webhook URLs
- raw MTGA logs
- workbook IDs unless explicitly approved and redacted where possible
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- unrelated private transcript dumps

## Outputs

This Codex B pass outputs:

- `docs/contracts/external_integration_collaboration_surfaces.md`

Expected future implementation outputs if issue #79 authorizes them:

- proposed ADR for external integration and collaboration surfaces
- narrow updates to governance docs and rule index
- implementation handoff
- review or contract-test report
- PR that uses issue-closing language correctly

No output may create or modify parser/runtime behavior, workbook schema,
webhook payload shape, Apps Script behavior, live external documents,
connectors, credentials, environment variables, raw data, generated data,
OpenAI API runtime behavior, coaching evaluation behavior, or production
deployment behavior unless a separate scoped issue and contract explicitly
authorize it.

## Invariants

- External tools are access/collaboration layers unless repo authority says
  otherwise.
- External outputs are evidence, not authority by default.
- Parser/state remains parser truth owner.
- Deterministic local code owns future scoring/evaluation only when separately
  contracted.
- AI/LLM output is explanation, recommendation, enrichment, inference, or
  hypothesis, not parser truth.
- Google Sheets and Google Docs are collaboration/storage/display surfaces, not
  authority by default.
- Local Codex skills are helper instructions, not repo authority.
- MCPs, plugins, and connectors are access layers, not truth layers.
- OpenAI docs tooling is documentation research, not runtime integration.
- OpenAI API runtime integration requires a separate issue and contract.
- Coaching evaluation requires a separate issue and contract.
- Secrets, credentials, environment variable contracts, raw logs, and local
  artifacts remain protected.
- Human approval is required for live external writes, permission changes,
  credential work, production changes, and sensitive external data sharing.

## Error Behavior

If an external tool output conflicts with repo authority, follow repo authority
and record the conflict.

If a connector returns incomplete, stale, permission-limited, or unavailable
data, name the limitation and avoid treating the result as complete truth.

If a requested action would write to a live external system without explicit
approval, stop and ask for approval.

If a requested action would move parser truth into an external surface, stop
and route to Codex A or B for a scoped issue and contract.

If a requested action requires credentials, secrets, environment variables, or
permission changes, stop and request human approval before proceeding.

If coaching, evaluation, OpenAI API runtime integration, or model-backed
analytics enter scope, route to a separate issue and contract.

If future implementation cannot determine whether an integration is
collaboration-only or runtime-affecting, classify it as higher risk and route
back to Codex B.

## Side Effects

This contract-writing pass may only create or revise:

- `docs/contracts/external_integration_collaboration_surfaces.md`

Future implementation may only edit governance docs, ADRs, indexes, templates,
and handoff/report artifacts explicitly authorized by issue #79 and this
contract.

Forbidden side effects:

- live Google Docs or Google Sheets edits
- Google Drive permission or sharing changes
- Apps Script deployment changes
- webhook receiver changes
- parser/runtime code changes
- OpenAI API calls from project runtime
- new API keys, tokens, OAuth grants, or credentials
- environment variable contract changes
- connector/plugin/MCP installation or authorization changes
- raw data exports or retained external copies
- coaching evaluation implementation
- CI gate changes unless separately contracted

## Dependency Order

Recommended Codex C implementation order:

1. Confirm branch target and issue #79 scope with the user.
2. Compare current governance docs against this contract.
3. Create the next ADR, likely
   `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
   or the next available ADR number.
4. Update `docs/decisions/README.md` to index the ADR.
5. Add terse machine-readable entries to `docs/agent_rules.yml`.
6. Add concise narrative references to `docs/agent_constitution.md` and
   `docs/codex_module_workflow.md`.
7. Add only short entrypoint reminders to `AGENTS.md` if needed.
8. Update role docs or templates only when they need concrete tool-boundary
   prompts.
9. Produce an implementation handoff.
10. Route to Codex E for review or contract-test verification.

## Compatibility

This contract preserves:

- existing parser truth ownership
- existing protected-surface policy
- existing A-G workflow
- Codex H as auxiliary advisory synthesis
- existing Google Sheets workbook/downstream boundaries
- existing OpenAI/LLM boundary from ADR-0002
- existing secret and local artifact safety rules
- existing main-target approval gates

This contract does not replace any parser, workbook, webhook, Apps Script,
analytics, evidence-ledger, or coaching module contract.

## Does This Need An ADR?

Yes, durable implementation should include a new ADR.

The ADR policy says persistent external integration boundaries, privacy
boundaries, secrets policy, and data-retention policy require an ADR. Issue
#79 intentionally covers those durable cross-project boundaries.

The future ADR should record:

- tools and connectors are access/collaboration layers by default
- local skills are non-authoritative helpers
- Google Docs and Google Sheets are not repo authority or parser truth by
  default
- OpenAI docs tooling is distinct from OpenAI API runtime integration
- OpenAI API runtime integration requires separate issue, contract, privacy
  review, and validation
- coaching evaluation is separate from this governance policy
- human approval is required for live external writes, credential changes,
  sensitive data sharing, permission changes, and production changes

An ADR is not created in this contract-writing pass.

## Coaching Evaluation Split

Coaching evaluation must be split into a separate issue.

Reason:

- ADR-0002 already states that future OpenAI, LLM, coaching, or model-backed
  analytics implementation requires its own issue, module contract, validation
  plan, and privacy boundary review.
- Coaching evaluation needs feature-specific goals, scoring/rubric logic,
  source data, prompts, labels, user-facing uncertainty, validation data, and
  acceptance criteria.
- Bundling coaching evaluation here would blur external tool governance with
  analytics/coaching product behavior.

## Protected Surfaces And Forbidden Side Effects

This contract explicitly does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- parser event class changes
- match/game identity or deduplication changes
- live Google Sheets or Google Docs edits
- Google Drive permission or sharing changes
- connector/plugin/MCP installation or authorization changes
- OpenAI API runtime integration
- API key, OAuth, credential, token, webhook URL, or environment-variable
  changes
- sending raw or sensitive project data to external APIs
- coaching evaluation implementation
- CI gate changes unless separately contracted
- merging or production deployment

## Validation Requirements

Codex C should run at minimum:

```powershell
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
```

If `docs/agent_rules.yml` changes, run a YAML parse check, for example:

```powershell
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"
```

If ADR files change, verify ADR numbering and
`docs/decisions/README.md` index consistency.

If new docs files remain untracked during local validation, run a path-scoped
protected-surface check for the new files.

Codex E should verify:

- no parser/runtime/workbook/webhook/App Script behavior changed
- no live external systems were edited
- no secrets, raw logs, workbook IDs, failed posts, runtime status files,
  generated data, or workbook exports were included
- tools, skills, MCPs, plugins, connectors, Docs, Sheets, and AI output remain
  non-authoritative by default
- OpenAI docs tooling is separated from OpenAI API runtime integration
- OpenAI API runtime integration remains out of scope
- coaching evaluation is split to a separate issue
- an ADR is included or explicitly routed as required for durable policy
- human approval boundaries remain intact

## Acceptance Criteria

- `docs/contracts/external_integration_collaboration_surfaces.md` exists and
  links to issue #79.
- The contract defines external integration surfaces.
- The contract defines collaboration surfaces.
- The contract defines authority surfaces by contrast.
- The contract defines Google Sheets collaboration and truth boundaries.
- The contract defines Google Docs collaboration and authority boundaries.
- The contract defines local Codex skills as non-authoritative helpers.
- The contract defines MCP/plugin/connector boundaries.
- The contract separates OpenAI docs tooling from OpenAI API runtime
  integration.
- The contract defines secret, credential, environment variable,
  data-retention, and human approval boundaries.
- The contract says durable implementation needs a new ADR.
- The contract says coaching evaluation must be split into a separate issue.
- The contract preserves parser truth ownership and protected surfaces.
- The contract does not authorize external writes, runtime integrations,
  connector installation, credential changes, live data changes, OpenAI API
  runtime integration, or coaching evaluation.
- The contract includes validation expectations and a pasteable Codex C prompt.

## Unknowns And Open Questions

- What branch should issue #79 implementation target?
- Whether the future ADR should be ADR-0005 or a later number if another ADR
  lands first.
- Which governance docs need implementation edits beyond the ADR and rule
  index.
- Whether Google Drive/Docs/Sheets connector-specific examples should live in
  role docs, the ADR, or only this issue/contract.
- Whether external card/metagame/strategy data providers need a separate
  contract from collaboration-surface governance.
- Whether any current live workbook/Drive sharing or retention settings should
  be audited later as a separate safety issue. This contract does not inspect
  live sharing settings.

## Suspected Gaps

- Current governance docs contain tool-surface guidance, especially for Codex
  H, but do not yet provide one consolidated durable policy/ADR for external
  integrations and collaboration spaces.
- Current ADRs cover parser truth, LLM explanation boundaries, and protected
  surfaces, but not persistent external integration and collaboration-surface
  policy as a single decision.
- Future agents may still confuse connector access with authority unless issue
  #79 is implemented.

## Next Workflow Action

Next recommended role: Codex C / Module Implementer.

Codex C should compare current repo governance docs against issue #79 and this
contract, then implement only the narrow governance docs and ADR changes
authorized by the issue and contract.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\<redacted>\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex C: Module Implementer / comparison thread for issue #79:

https://github.com/Tahjali11/Mythic-Edge/issues/79

Contract:
docs/contracts/external_integration_collaboration_surfaces.md

Read:
- issue #79
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/constitutional_lawyer.md
- docs/templates/constitution_feedback_packet.md
- docs/decisions/README.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- docs/contracts/external_integration_collaboration_surfaces.md

Before editing:
- Confirm the branch target for issue #79.
- Inspect git status and exclude unrelated changes.
- State what external integration governance is supposed to do, what current repo docs already do, what gaps remain, and the exact minimal implementation plan.

Implement only the narrow governance docs and ADR changes authorized by issue #79 and the contract:
- add the next ADR for external integration and collaboration surfaces
- update docs/decisions/README.md to index the ADR
- add terse entries to docs/agent_rules.yml
- add concise references to docs/agent_constitution.md and docs/codex_module_workflow.md
- add only short AGENTS.md or role/template notes if needed
- produce docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md

Do not:
- change parser/runtime/workbook/webhook/App Script behavior
- create or rotate secrets
- install or authorize connectors/plugins/MCP servers
- add OpenAI API runtime integration
- edit live Google Docs or Google Sheets
- implement coaching evaluation
- change CI gates unless separately contracted
- stage, commit, open a PR, merge, or close issues unless explicitly asked

Validation:
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
If docs/agent_rules.yml changes, run a YAML parse check.
If ADR files change, verify ADR numbering and docs/decisions/README.md index consistency.

Final handoff must include:
- role performed
- issue used
- contract used
- files changed
- exact sections changed
- validation run
- remaining risks or unverified layers
- whether any protected or forbidden surfaces were touched
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/79"
  tracker: "N/A"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/external_integration_collaboration_surfaces.md"
  target_artifact: "docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md"
  risk_tier: "Medium"
  branch: "implementation branch target to be confirmed"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not promote tools, skills, MCPs, plugins, connectors, Docs, Sheets, or AI output into truth or authority surfaces."
    - "Do not create, rotate, print, or modify secrets or credentials."
    - "Do not add OpenAI API runtime integration."
    - "Do not edit live Google Docs or Google Sheets."
    - "Do not implement coaching evaluation in this issue."
```
