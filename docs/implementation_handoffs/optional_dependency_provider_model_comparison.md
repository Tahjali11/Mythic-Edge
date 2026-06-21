# Optional Dependency Provider Model Implementation Handoff

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer for ODP-E-001 and ODP-E-002 reviewer follow-up.

## Source Issue

- https://github.com/Tahjali11/Mythic-Edge/issues/341

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/340
- https://github.com/Tahjali11/Mythic-Edge/issues/535
- https://github.com/Tahjali11/Mythic-Edge/issues/543

## Source Artifact

- `docs/contracts/optional_dependency_provider_model.md`
- GitHub issue #341 plus Codex A ADR-focused refresh comment.

## Contract Comparison

Confirmed matches:

- Proposed ADR-0009 was created at the contracted path because no
  `ADR-0009-*` file existed at implementation start.
- ADR-0009 is `Proposed` and does not claim acceptance before review/merge.
- ADR-0009 records base completeness with zero optional providers installed.
- ADR-0009 covers all optional provider categories, not only private analytics
  providers.
- ADR-0009 keeps base ownership over provider vocabulary, interface direction,
  registry direction, status vocabulary, capability model, discovery boundary,
  and safe failure behavior.
- ADR-0009 now spells out the contract's provider family vocabulary, allowed
  provider status values, capability-label authority boundary, base-owned
  provider envelope direction, non-breaking failure behavior, future
  boundary-checker gates, and later fake/sample-provider plus provider-error
  test expectations.
- ADR-0009 defines packaged-provider and local/dev-provider discovery
  boundaries without adding entry points, manifests, config, or code.
- ADR-0009 defines default read-only and privileged data-access tiers without
  authorizing privileged access.
- ADR-0009 names process-memory providers as future/high-risk only and links
  issue #535 as deferred context.
- ADR-0009 defines UI absence/presence semantics without changing UI code.
- ADR-0009 documents future boundary-checker and fake/sample-provider testing
  direction without implementing either.
- `docs/decisions/README.md` now indexes ADR-0009 as `Proposed`.

Contract boundaries preserved:

- No provider code, registry, discovery, adapters, boundary scripts, tests, or
  UI were implemented.
- `pyproject.toml` was not edited.
- No dependency groups, entry points, package dependencies, or private GitHub
  requirements were added.
- No sibling repositories were inspected or mutated.
- No parser, runtime, analytics, workbook, webhook, Apps Script, Google
  Sheets, OpenAI/model-provider, AI/coaching, release, deploy, or production
  behavior changed.
- No GitHub issues, PRs, labels, trackers, automations, worktrees, or stashes
  were mutated.

Codex D fixer notes:

- ODP-E-001 fixed by replacing broad ADR claims about provider status and
  capability ownership with explicit contract vocabulary and non-breaking
  status semantics.
- ODP-E-002 fixed by adding the missing future provider-boundary checker and
  fake/sample-provider plus provider-error-state test obligations to ADR-0009.
- The fixer pass remained docs-only and did not edit runtime code,
  dependencies, provider discovery, provider registry behavior, UI, parser,
  analytics, workbook, webhook, Apps Script, Google Sheets, AI/model-provider,
  release, deploy, production, or sibling-repo behavior.

## Files Changed

- `docs/contracts/optional_dependency_provider_model.md`
- `docs/decisions/ADR-0009-optional-dependency-provider-model.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/optional_dependency_provider_model_comparison.md`

## Key Decisions

- Kept the ADR docs-only and policy-only.
- Preserved the base repo as complete without optional providers.
- Framed provider presence as additive and provider absence as non-degrading.
- Kept process-memory providers visible as a future high-risk category without
  implementation or local execution authority.
- Left provider registry, discovery, entry points, manifests, boundary scripts,
  tests, and UI for later separately contracted slices.

## Validation Run

Final validation:

- `python3 tools/check_agent_docs.py` passed with 36 checked files, 0 errors,
  and 0 warnings.
- `git diff --check` passed.
- Path-fed `python3 tools/check_secret_patterns.py --base origin/main
  --paths-from-stdin` passed for 4 changed docs files with 0 forbidden
  findings and 0 warnings.
- Path-fed `python3 tools/check_protected_surfaces.py --base origin/main
  --paths-from-stdin` passed for 4 changed docs files with 0 forbidden
  findings and 0 warnings.
- Path-fed `python3 tools/select_validation.py --base origin/main
  --paths-from-stdin --format text` returned `selection_status: ok`.
- ASCII scan found no non-ASCII matches in changed files.
- Local absolute path marker scan found no matches in changed files.

Codex D fixer validation:

- `python3 tools/check_agent_docs.py` passed with 36 checked files, 0 errors,
  and 0 warnings.
- `git diff --check` passed.
- Path-fed `python3 tools/check_secret_patterns.py --base origin/main
  --paths-from-stdin` passed for 4 changed docs files with 0 forbidden
  findings and 0 warnings.
- Path-fed `python3 tools/check_protected_surfaces.py --base origin/main
  --paths-from-stdin` passed for 4 changed docs files with 0 forbidden
  findings and 0 warnings.
- Path-fed `python3 tools/select_validation.py --base origin/main
  --paths-from-stdin --format text` returned `selection_status: ok`.
- ASCII scan found no non-ASCII matches in changed files.
- Local absolute path marker scan found no matches in changed files.

## Remaining Risks

- ADR-0009 is only `Proposed` until reviewed and merged.
- Future provider interface, registry, discovery, boundary checker, fake
  provider, UI status, and provider-specific behavior all require separate
  contracts.
- Issue #535 remains deferred research/audit context for process-memory
  providers and is not implemented or activated by this ADR.
- `Tahjali11/Mythic-Edge-Analytics` and other sibling repos remain related
  context only; no adoption or mutation occurred.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

Review focus:

- Confirm ADR-0009 preserves base completeness without optional providers.
- Confirm provider absence is non-degrading and provider presence is additive.
- Confirm the ADR does not authorize provider runtime implementation.
- Confirm privileged local/external access remains behind later issue and
  contract gates.
- Confirm process-memory provider language does not activate issue #535.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #341.

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

Contract:
docs/contracts/optional_dependency_provider_model.md

Implementation handoff:
docs/implementation_handoffs/optional_dependency_provider_model_comparison.md

Branch:
main

Goal:
Adversarially review the docs-only Optional Dependency Provider Model ADR
package against the contract. Confirm proposed ADR-0009 preserves base
completeness with zero optional providers, keeps provider interfaces and
registry direction base-owned, and does not authorize provider runtime code or
privileged data access.

Review:
- docs/contracts/optional_dependency_provider_model.md
- docs/decisions/ADR-0009-optional-dependency-provider-model.md
- docs/decisions/README.md
- docs/implementation_handoffs/optional_dependency_provider_model_comparison.md

Check especially:
- ADR-0009 is `Proposed`, linked to issue #341, and does not claim acceptance
  before review/merge.
- ADR-0009 covers all optional provider categories, not only private analytics
  providers.
- Base install, launch, parser capture, manual import, SQLite ingest, built-in
  analytics, setup/status, Match Journal, and base UI navigation remain
  complete with zero optional providers installed.
- Provider discovery remains future-only, guarded, explicit, non-magical, and
  not based on arbitrary-folder scanning.
- Default provider access is parser-normalized/read-only; privileged local and
  external access require later issue/contract authority.
- Process-memory providers are future/high-risk only and issue #535 is not
  implemented or activated.
- No runtime code, tests, pyproject, dependency groups, entry points, provider
  registry/discovery/adapters/boundary scripts/UI, sibling repos, parser
  behavior, analytics truth, workbook/webhook/App Script/Google Sheets
  behavior, OpenAI/model-provider behavior, AI/coaching behavior, release,
  deploy, or production behavior changed.

Validation:
- python3 tools/check_agent_docs.py
- git diff --check
- path-fed secret/private marker scan for changed docs files
- path-fed protected-surface scan for changed docs files
- path-fed validation selector for changed docs files
- ASCII and local absolute path marker scans for changed docs files

Do not:
- Edit files while reviewing unless the user explicitly asks for fixer work.
- Stage, commit, push, open a PR, merge, close, relabel, or update trackers.
- Implement provider code, registry, discovery, adapters, boundary scripts,
  tests, or UI.
- Edit pyproject.toml or add dependency groups, entry points, package
  dependencies, or private GitHub requirements.
- Create sibling-repo adoption issues or mutate sibling repos.
- Treat ADR-0009 as accepted before review and merge.

End with:
- findings first, ordered by severity;
- validation run;
- residual risks;
- recommendation for next role;
- workflow_handoff block.
```

## workflow_handoff

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
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/optional_dependency_provider_model.md"
  target_artifact: "docs/implementation_handoffs/optional_dependency_provider_model_comparison.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  proposed_adr: "docs/decisions/ADR-0009-optional-dependency-provider-model.md"
  internal_project_area: "Quality / Governance; Shared Support; External / Collaboration Surface"
  bridge_code_status: "deferred_future_boundary"
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: "https://github.com/Tahjali11/Mythic-Edge/issues/341"
    lane_status: "active"
    tracker_selected_next_lane: ""
    exception:
      name: ""
      blocked_active_issue_or_pr: ""
      reason: ""
      allowed_scope: ""
      expiration_condition: ""
      authorized_by: ""
      recorded_in: ""
  validation:
    - "python3 tools/check_agent_docs.py passed with 36 checked files, 0 errors, and 0 warnings."
    - "git diff --check passed."
    - "Path-fed secret/private marker scan passed for 4 changed docs files with 0 forbidden findings and 0 warnings."
    - "Path-fed protected-surface scan passed for 4 changed docs files with 0 forbidden findings and 0 warnings."
    - "Path-fed validation selector returned selection_status: ok."
    - "ASCII scan found no non-ASCII matches in changed files."
    - "Local absolute path marker scan found no matches in changed files."
  stop_conditions:
    - "Do not implement provider code, registry, discovery, adapters, boundary script, tests, or UI in the ADR-only Codex C pass."
    - "Do not edit pyproject.toml or add dependency groups, entry points, package dependencies, or private GitHub requirements."
    - "Do not create sibling-repo adoption issues or mutate sibling repos."
    - "Do not authorize raw log, process-memory, credential, network, external write, OpenAI/model-provider, analytics truth, parser truth, workbook, webhook, Apps Script, Google Sheets, release, deploy, production, hidden-card, gameplay advice, or coaching behavior changes."
    - "Do not make any optional provider required for base install, launch, parser capture, manual import, SQLite ingest, built-in analytics, or base UI navigation."
```
