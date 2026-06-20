# Repo-Scoped Workflow Handoffs Contract

## Module

`repo_scoped_workflow_handoffs`

Plain English: future Mythic Edge workflow handoffs must identify the GitHub
repository they belong to before a later Codex thread continues work. Public
handoff artifacts use repository-safe GitHub identity. Local machine worktree
paths may appear only in generated local prompts, outside public handoff
blocks.

This is a Codex B contract-writing artifact. It does not implement behavior
changes, open a PR, rewrite historical handoffs, mutate other repositories, or
change parser, runtime, workbook, analytics, app, AI, release, deployment, or
production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/506
- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Base branch: `main`
- Target branch: `main`
- Risk tier: Medium

Observed during this Codex B pass:

- Issue #506 is open.
- The operating checkout's `origin` remote normalized to
  `https://github.com/Tahjali11/Mythic-Edge`.
- The operating checkout was on `main` and clean before this contract edit.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/problem_representation.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/module_contract.md`
- `docs/templates/contract_test_report.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_submitter.md`
- `docs/agent_threads/integration_deployer.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `docs/contracts/workflow_freshness_guard.md`
- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`

`docs/workflow_status/mythic_edge_active_lanes.md` was requested for
inspection if present, but it was not present in this checkout during the
contract pass.

## Owning Layer

Primary owner: Quality / Governance.

This contract owns workflow routing metadata only. It does not own parser
truth, analytics truth, workbook truth, Match Journal truth, local-app truth,
AI truth, CI truth, merge readiness, deploy readiness, production readiness, or
tracker completion.

## Files Owned By This Contract

This Codex B pass creates:

- `docs/contracts/repo_scoped_workflow_handoffs.md`

Future Codex C implementation for issue #506 may edit:

- `docs/templates/workflow_handoff.md`
- `docs/templates/problem_representation.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/module_contract.md`
- `docs/templates/contract_test_report.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_submitter.md`
- `docs/agent_threads/integration_deployer.md`
- `tools/check_agent_docs.py`
- `tests/test_check_agent_docs.py`
- `docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md`

Future Codex C may update `docs/workflow_status/mythic_edge_active_lanes.md`
only if that file is present or separately created by an authorized workflow
status issue. This contract does not require creating it.

This contract does not authorize edits to source code, parser behavior, runtime
logic, analytics logic, app behavior, CI gates beyond static docs-check
planning, release policy, deploy policy, production behavior, generated data,
private artifacts, local-only files, or historical GitHub comments and PR
bodies.

## Observed Current Behavior

- `docs/templates/workflow_handoff.md` includes issue, tracker, role, artifact,
  risk, branch, validation, stop condition, and optional freshness metadata.
- The handoff template does not require `repository` or `repository_url`.
- Several other templates include embedded `workflow_handoff` examples that
  also omit repository identity.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` asks for expected branch, source
  artifacts, target artifact, scope, validation, and stop conditions, but does
  not ask for repository identity.
- `.github/pull_request_template.md` includes a workflow handoff block without
  repository identity.
- `tools/check_agent_docs.py` already validates static governance docs and
  handoff template keys through `HANDOFF_BLOCK_KEYS`.
- `tools/check_agent_docs.py` does not currently require repository identity in
  the workflow handoff template.
- `docs/contracts/workflow_freshness_guard.md` defines freshness metadata and
  routing checks, but does not define repo-scoped identity or mismatch stops.

This is not a product behavior bug. The gap is cross-repository workflow
routing safety.

## Required Public Handoff Fields

Every new public `workflow_handoff` should include these repository identity
fields:

- `repository`: GitHub owner/name slug, such as `Tahjali11/Mythic-Edge`.
- `repository_url`: canonical public HTTPS URL without a trailing `.git`, such
  as `https://github.com/Tahjali11/Mythic-Edge`.

These fields are routing metadata. They do not authorize protected-surface
changes and do not override live GitHub or local Git evidence.

### Required Branch Routing Fields

New handoffs should distinguish branch concepts when branch routing matters:

- `base_branch`: branch the work should start from or compare against.
- `target_branch`: branch future PR or integration work should target.
- `branch`: current, working, implementation, or handoff branch.

`branch` may remain for backward compatibility and compact prompts, but it must
not replace `base_branch` and `target_branch` when those differ or when a
handoff crosses from problem representation to implementation, submission, or
deployment.

### Recommended Public Shape

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: ""
  tracker: ""
  completed_thread: ""
  next_thread: ""
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
  internal_project_area: ""
  truth_owner: ""
  bridge_code_status: ""
  allowed_read_only_references:
    - repository: ""
      repository_url: ""
      purpose: ""
  freshness:
    current_branch: ""
    intended_branch: ""
    upstream_branch: ""
    branch_ahead_behind: ""
    issue_state: ""
    tracker_state: ""
    source_artifact_status: ""
    target_artifact_status: ""
    local_dirty_state: ""
    untracked_artifacts:
      - ""
    worktree_classification: ""
    freshness_verdict: ""
    recommended_route: ""
    verified_at: ""
  validation:
    - ""
  stop_conditions:
    - ""
```

`allowed_read_only_references` is optional. When omitted or empty, sibling
repositories are out of scope.

## Public Handoff Versus Local Prompt Rules

Public artifacts include GitHub issues, PR bodies, PR comments, committed docs,
templates, workflow handoff examples, and tracker updates.

Public artifacts must not include:

- local absolute paths;
- private worktree locations;
- exact local app-data paths;
- raw private log paths;
- machine-specific home-directory paths;
- local-only artifact locations unless explicitly redacted or described with a
  placeholder.

Generated local prompts may include a separate local execution hint outside the
public `workflow_handoff` block:

```text
Operating repo/worktree:
`<local path supplied privately for this machine>`
```

Local prompts that include an operating worktree path must also tell Codex to
verify the checkout remote before reading, editing, staging, committing,
pushing, cleaning, stashing, resetting, or otherwise mutating repository
content.

Do not copy the local `Operating repo/worktree:` value into public GitHub
issues, PR bodies, committed templates, committed contracts, or workflow
handoff blocks.

## Checkout Mismatch Rules

Before mutating repository content, a continuing Codex thread must verify that
the local checkout remote matches the public handoff identity.

Recommended normalization:

- Strip a trailing `.git` suffix.
- Strip trailing slashes.
- Treat `https://github.com/<owner>/<repo>` as the canonical public URL.
- Treat an equivalent `git@github.com:<owner>/<repo>.git` remote as matching
  only after converting it to the same canonical HTTPS URL.
- Compare repository owner/name case-insensitively for GitHub routing, while
  preserving the handoff's original spelling in public artifacts.

Mismatch or unverifiable states must hard stop before mutation. Stop when:

- no repository remote can be found;
- the remote normalizes to a different repository;
- multiple remotes make the intended repository ambiguous;
- the current checkout is not a Git repository;
- the handoff lacks `repository` or `repository_url` and the next action would
  mutate a repo;
- the prompt asks to inspect or mutate a sibling repo that is not listed under
  `allowed_read_only_references`.

The stop report should name:

- expected `repository`;
- expected `repository_url`;
- observed remote URLs, if safe to show;
- current branch, if safe to show;
- the requested next action that was blocked;
- the user action needed, such as providing the correct checkout or revising
  the handoff.

A mismatch stop must not stage, commit, push, clean, stash, reset, delete,
move, sanitize, or rewrite files.

## Allowed Read-Only Sibling References

Sibling repositories may be inspected only when explicitly listed under
`allowed_read_only_references`.

Each allowed reference should include:

- `repository`;
- `repository_url`;
- `purpose`;
- optional `source_artifacts` when the reference is narrow.

Read-only sibling reference permission allows inspection and summary only. It
does not allow edits, staging, commits, pushes, branch switches, cleanup,
artifact generation, issue closure, PR creation, or mutation in that sibling
repo.

If a sibling repo needs edits, that work must be routed through its own
repo-scoped handoff with that sibling repository as `repository` and
`repository_url`.

## Workflow Status Index Rules

Workflow status indexes, when present, may include repository identity to help
humans scan active lanes across repositories.

Workflow status indexes are convenience indexes only. They must not override:

- live GitHub issue state;
- live PR state;
- local Git remote evidence;
- current branch evidence;
- accepted contracts;
- Codex G merge/deploy verification;
- explicit user instructions.

Public workflow status indexes must not include local absolute paths. If local
worktree context is useful, use public-safe labels such as `primary checkout`,
`sibling worktree`, or `local-only worktree selected by user`, without spelling
the local path.

## Required Guarantees

- New handoffs include public-safe repository identity.
- New handoffs do not rely on implicit repository context.
- New local prompts may include local worktree context only outside public
  handoff blocks.
- A local checkout whose remote does not match the handoff repository hard
  stops before mutation.
- Sibling repositories remain out of scope unless explicitly listed as
  read-only references.
- Historical issue comments, PR bodies, and old handoffs are not rewritten.
- The workflow freshness guard remains complementary: freshness metadata
  explains state drift; repo-scoped identity explains which repository owns the
  work.
- Static docs checker updates remain limited to governance docs/template
  consistency and do not become live GitHub, live remote, or CI policy gates
  unless a later contract explicitly authorizes that.

## Unknowns

- Whether every future Mythic Edge sibling repository will use the same A-G
  role docs or only the same public handoff schema.
- Whether future repository-dispatch automation will need a stricter machine
  schema. This contract does not authorize cross-repo automation.
- Whether a future workflow status index will exist in every repository. This
  contract treats it as optional.
- Whether `repository_url` should allow non-GitHub mirrors in future. For this
  contract, GitHub HTTPS is the canonical public form.

## Suspected Gaps

- Existing templates and embedded examples need coordinated updates so Codex
  roles do not keep emitting repo-implicit handoffs.
- `tools/check_agent_docs.py` and `tests/test_check_agent_docs.py` likely need
  small static-schema updates to require `repository`, `repository_url`,
  `base_branch`, and `target_branch` in canonical templates.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` likely needs public repository
  identity fields or guidance so problem-representation issues start with the
  correct repo scope.
- The PR template's handoff block likely needs the same fields so Codex F/G
  submission and deployment handoffs remain repo-scoped.
- Role docs should warn that local worktree paths belong in generated local
  prompts, not public artifacts.

## Compatibility Expectations

- Existing historical handoffs remain valid historical artifacts.
- Future continuation threads should verify repository identity live before
  mutation, even when the handoff came from an older artifact.
- Old handoffs without repository identity should route to a freshness or
  repo-scope clarification step before mutation if the repo context is not
  obvious from the current issue, branch, and checkout.
- Adding `repository` and `repository_url` must not break current role names,
  `next_thread` values, freshness metadata, internal project vocabulary, or
  branch policy.

## Codex C Implementation Scope

Codex C should implement the smallest governance/docs/checker slice that makes
future handoffs repo-scoped:

- update canonical templates and embedded examples with `repository`,
  `repository_url`, `base_branch`, and `target_branch`;
- add guidance for `Operating repo/worktree:` in local prompts only;
- add checkout mismatch stop language to workflow docs/role docs;
- add optional `allowed_read_only_references` guidance;
- update `.github/ISSUE_TEMPLATE/module_workflow.yml` and
  `.github/pull_request_template.md` with public-safe repo identity fields or
  examples;
- update `docs/agent_rules.yml` schema expectations where appropriate;
- update `tools/check_agent_docs.py` and `tests/test_check_agent_docs.py` so the
  static docs checker catches missing required public handoff fields in the
  canonical template;
- produce
  `docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md`.

Codex C must not:

- implement live remote-check automation beyond static docs-check expectations;
- create cross-repo automation;
- rewrite historical handoffs;
- add local absolute paths to public docs or examples;
- mutate other repositories or worktrees;
- change product behavior or protected surfaces.

## Validation Obligations

Codex C should run at minimum:

```bash
python3 tools/check_agent_docs.py
python3 -m pytest -q tests/test_check_agent_docs.py
git diff --check
```

Codex C should also run path-scoped protected-surface and secret/private-marker
checks if available in the checkout.

Codex E should verify:

- the canonical handoff template contains `repository` and `repository_url`;
- branch routing uses `base_branch` and `target_branch` where relevant;
- public examples contain no local absolute paths;
- local prompt guidance keeps `Operating repo/worktree:` outside public
  handoff blocks;
- checkout mismatch behavior is a hard stop before mutation;
- sibling references are read-only unless a separate repo-scoped handoff owns
  mutation;
- checker tests cover the new static schema expectations.

Codex F/G should verify PR and deployment handoffs contain repository identity
and do not leak local paths.

## Protected Surfaces

Do not change parser behavior, parser state final reconciliation, parser event
classes, router semantics, analytics schema or view semantics, Match Journal
behavior, overlay behavior, Google Sheets sync behavior, workbook schema,
webhook payload shape, Apps Script behavior, output transport,
OpenAI/model-provider behavior, AI/coaching behavior, release policy, deploy
policy, production behavior, secrets, credentials, tokens, API keys, raw logs,
generated/private/runtime artifacts, SQLite files, workbook exports, or
local-only files.

Do not add CI gates beyond static docs-check planning unless a later contract
explicitly authorizes them.

## Recommended Next Role

Codex C: Module Implementer.

The implementation should proceed as a governance docs/template/checker update
only.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #506.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Base branch:
main

Target branch:
main

Operating repo/worktree:
`<local path supplied privately by the user for this machine>`

Goal:
Implement the smallest governance docs/template/checker update needed to make future Mythic Edge workflow handoffs repo-scoped.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/506
- docs/contracts/repo_scoped_workflow_handoffs.md
- AGENTS.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/templates/workflow_handoff.md
- docs/templates/problem_representation.md
- docs/templates/implementation_handoff.md
- docs/templates/module_contract.md
- docs/templates/contract_test_report.md
- docs/agent_threads/problem_representation.md
- docs/agent_threads/module_contract.md
- docs/agent_threads/implementation.md
- docs/agent_threads/module_submitter.md
- docs/agent_threads/integration_deployer.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- .github/pull_request_template.md
- tools/check_agent_docs.py
- tests/test_check_agent_docs.py

Before editing:
1. Verify the local checkout remote normalizes to `https://github.com/Tahjali11/Mythic-Edge`.
2. Hard stop before mutation if the checkout repository does not match the contract.
3. Inspect `git status --short --branch`.

Do:
- Add `repository` and `repository_url` to canonical public handoff templates and embedded examples.
- Add `base_branch` and `target_branch` where branch routing matters.
- Preserve `branch` for compatibility where useful.
- Add public-safe guidance for generated local prompts that may include `Operating repo/worktree:` outside the public `workflow_handoff` block.
- Add checkout mismatch hard-stop guidance.
- Add optional read-only sibling repository reference guidance.
- Update `tools/check_agent_docs.py` and focused tests so static governance checks cover the required template fields.
- Produce `docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md`.

Do not:
- Rewrite historical issue comments, PR bodies, or old handoffs.
- Add local absolute paths to public docs, issues, PR templates, or handoff examples.
- Mutate any other repository or worktree.
- Implement live remote-check automation, cross-repo automation, or new CI gates.
- Change parser behavior, analytics behavior, Match Journal behavior, overlay behavior, OpenAI/model-provider behavior, workbook/webhook/App Script behavior, release policy, deploy policy, production behavior, secrets, raw logs, generated/private/runtime artifacts, or local-only files.

Validation:
- python3 tools/check_agent_docs.py
- python3 -m pytest -q tests/test_check_agent_docs.py
- git diff --check
- Run path-scoped protected-surface and secret/private-marker checks if available.

Expected output:
- Files changed
- Comparison artifact
- Validation evidence
- Residual risks
- Pasteable Codex E prompt
- workflow_handoff block with repository and repository_url
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/506"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #506 and docs/contracts/repo_scoped_workflow_handoffs.md"
  target_artifact: "docs/implementation_handoffs/repo_scoped_workflow_handoffs_comparison.md"
  risk_tier: "Medium"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  internal_project_area: "Quality / Governance"
  truth_owner: "workflow routing metadata; GitHub/git remain authoritative"
  bridge_code_status: "N/A"
  allowed_read_only_references: []
  validation:
    - "Codex B docs-only validation; see final response."
  stop_conditions:
    - "Hard stop before mutation if the local checkout remote does not match repository_url."
    - "Do not add local absolute paths to public docs, issues, PR templates, or handoff examples."
    - "Do not rewrite historical issue comments, PR bodies, or old handoffs."
    - "Do not mutate any other repository or worktree."
    - "Do not change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior."
```
