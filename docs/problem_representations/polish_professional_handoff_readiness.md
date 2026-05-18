# Professional Handoff Readiness

## Summary

Mythic Edge should eventually be organized so that a professional development
team with no prior project context can clone the repo, understand the system,
install it, validate it, identify the current roadmap, and safely distinguish
active source from historic or local artifacts.

This artifact records the presentation and organization work that should be
added to the Polish and Discipline suite. It intentionally does not duplicate
the existing setup, CI, corpus regression, sanitizer, or type-discipline
modules. Instead, it defines the professional handoff layer that should sit on
top of those modules.

## Source Request

Source request: add the recommendations under "Making it presentable to a
professional team" to the `codex/polish-and-discipline-suite` branch without
duplicating items already in that branch.

Related suite artifacts:

- `docs/problem_representations/polish_and_discipline_suite.md`
- `docs/problem_representations/polish_installer_setup_parity_audit.md`
- `docs/problem_representations/polish_corpus_regression_parity_with_manasight.md`

## What This Should Accomplish

The professional handoff layer should make Mythic Edge readable to an outside
team without requiring them to reconstruct project history from Codex chats,
old branches, or scattered implementation handoffs.

An outside team should be able to answer:

- what the project does
- what it explicitly does not do
- how to install it
- how to run it
- how to validate it
- which layers own truth
- which docs are current authority
- which folders are source, tests, docs, tools, generated data, archives, or
  local/private artifacts
- how to add parser, ledger, analytics, or workflow changes safely
- which old files can be deleted, archived, or left alone

## Non-Goals

This artifact does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- parser event class or event kind changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- raw Player.log fixture imports
- generated card/tier/oracle data commits
- runtime status, failed-post, workbook export, or local-only artifact commits
- deletion of historic files without a reviewable inventory and explicit
  approval

## Section 1: Clear Entry Points

Goal:

- Make the project understandable from the first page a developer opens.

Recommended work:

- Update the top-level `README.md` so it explains:
  - what Mythic Edge is
  - what problem it solves
  - what it does not claim to solve
  - the current primary user flow
  - how parser truth, evidence ledger, analytics, workbook, and AI boundaries
    relate
  - how to install the project
  - how to run the parser or local operator tools
  - how to run the smallest useful validation command
  - where to find deeper architecture, governance, and roadmap docs
- Add or update a concise architecture overview that explains:
  - MTGA `Player.log` as observable evidence
  - parser/state as truth-producing interpretation
  - evidence ledger and drift detector as provenance and quality assurance
  - analytics as deterministic downstream calculation
  - workbook/webhook/Apps Script as transport or collaboration surfaces
  - AI coaching as explanation, hypothesis, and recommendation only
- Keep marketing-style prose out of the handoff. The repo should read like a
  serious engineering project, not a pitch deck.

Avoid duplicating:

- detailed setup commands already owned by the Python version and lockfile
  module
- CI expansion details already owned by the CI/security/smoke module
- corpus details already owned by the corpus regression parity artifact

## Section 2: One-Command Setup And Validation

Goal:

- Give a new developer one obvious way to set up and one obvious way to check
  the repo.

Recommended work:

- Keep this section linked to, not duplicated from, the existing setup polish
  modules.
- After the version/lockfile and one-command validation modules exist, make the
  README point to:
  - the supported Python version
  - the recommended development Python version
  - Windows setup command
  - macOS setup command
  - parser runtime install command
  - development/workflow install command
  - focused validation command
  - full local validation command
- Make the difference between parser runtime dependencies and development /
  Codex workflow dependencies explicit.
- Document what to do when optional tooling is missing.

Existing suite coverage:

- `docs/problem_representations/polish_and_discipline_suite.md` already owns
  Python version, `.python-version`, `uv`/lockfile support, one-command local
  checks, CI/security expansion, public sanitizer docs, and type-discipline
  ladder.
- `docs/problem_representations/polish_installer_setup_parity_audit.md`
  compares those setup surfaces against Manasight.

This handoff module should ensure those pieces are discoverable from the
front-door documentation once they are implemented.

## Section 3: Repo Map And Artifact Taxonomy

Goal:

- Make the directory tree legible and reduce the chance that a future
  developer mistakes historic, generated, or local/private artifacts for active
  source.

Recommended work:

- Add a repo map that briefly explains:
  - `src/`
  - `tests/`
  - `tests/fixtures/`
  - `docs/contracts/`
  - `docs/problem_representations/`
  - `docs/implementation_handoffs/`
  - `docs/contract_test_reports/`
  - `docs/decisions/`
  - `docs/archive/`
  - `tools/`
  - `.github/`
  - `data/`
- Classify each major path as one of:
  - active source
  - active tests
  - durable workflow artifact
  - accepted architectural authority
  - generated or local-only data
  - historic/archive material
  - external integration/tooling surface
- Add README files where a folder is easy to misunderstand, especially:
  - `docs/archive/`
  - `data/`
  - `tests/fixtures/`
  - any legacy bridge/tool folder retained for compatibility
- For generated or local-only directories, state whether files may be committed
  and under what review policy.

Recommended future child issue:

```text
[polish] Repo map and artifact taxonomy
```

## Section 4: Contribution Workflow For A New Team

Goal:

- Translate the Codex-heavy workflow into a form that humans and outside
  engineering teams can follow.

Recommended work:

- Add a contributor-facing workflow guide that explains:
  - how to add a parser module
  - how to update event/schema snapshots
  - how to add sanitized golden fixtures
  - how to run the protected-surface check
  - how to run the secret/private-marker scanner when available
  - how to decide whether a change needs an ADR
  - how the Codex A-G/H workflow maps to normal engineering roles
- Keep the Codex role docs as workflow authorities for Codex threads, but add a
  shorter human-readable layer for professional review.
- Make clear that external teams should not bypass the protected-surface,
  fixture, secret, or truth-ownership policies.

Recommended future child issue:

```text
[polish] Contributor workflow guide for parser, fixture, and governance changes
```

## Section 5: Professional Hygiene And Release Readiness

Goal:

- Ensure the project looks intentional, reviewable, and safe to operate from a
  fresh clone.

Recommended work:

- Ensure CI status is easy to find and explain.
- Document which checks are required, advisory, report-only, or future.
- Keep the secret scanner and protected-surface scanner visible in the
  contribution path.
- Document sanitizer usage as the boundary before any log evidence is shared.
- Ensure issue templates, PR template, security policy, and contribution docs
  are consistent with current repo authority.
- Keep roadmap docs current enough that a new developer knows whether the next
  phase is parser reliability, evidence ledger, analytics, AI coaching, or
  polish.
- Avoid leaving untracked or uncommitted planning artifacts as the only record
  of major decisions.

Existing suite coverage:

- CI/security/dependency/smoke expansion belongs to the broader polish suite.
- Corpus parity belongs to the corpus regression parity artifact.
- Sanitizer/security presentation belongs to the public sanitizer module.

This section should make the outputs of those modules visible and coherent.

## Repository Cleanup And Historic File Triage

Goal:

- Safely identify obsolete, duplicated, historic, generated, or local-only files
  without deleting useful observability or workflow history by accident.

Recommended approach:

1. Run a read-only folder-by-folder inventory.
2. Classify each file or folder before recommending deletion.
3. Separate deletion candidates from archive candidates.
4. Check whether any path is referenced by tests, docs, tools, CI, packaging,
   launcher code, Apps Script, or workflow templates.
5. Prefer moving unclear historic materials to an archive with a README before
   deleting them.
6. Delete only after explicit user approval and a narrow commit.

Suggested classification labels:

- active source
- active test
- active fixture
- generated fixture
- local/private data
- workflow artifact
- accepted authority
- archived authority
- legacy compatibility
- dead duplicate
- deletion candidate
- unknown, needs owner decision

Suggested future child issue:

```text
[polish] Folder-by-folder repository cleanup and historic file triage
```

This should be a read-only audit first. It should not delete archive, raw,
debug, helper, summary, observability, generated-data, fixture, or local-data
layers without explicit approval and a rollback path.

## Suggested Issue Queue Additions

Add these to the Polish and Discipline suite after the existing setup, CI,
sanitizer, corpus, and type-discipline items are framed:

1. `[polish] Professional handoff README and architecture overview`
2. `[polish] Repo map and artifact taxonomy`
3. `[polish] Contributor workflow guide for parser, fixture, and governance changes`
4. `[polish] Folder-by-folder repository cleanup and historic file triage`

## Validation Evidence Needed

For this planning artifact:

```powershell
git diff --check
```

Recommended path-scoped safety check:

```powershell
@'
docs/problem_representations/polish_and_discipline_suite.md
docs/problem_representations/polish_professional_handoff_readiness.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/polish-and-discipline-suite --paths-from-stdin
```

Future cleanup audits should also run reference searches before proposing
deletion:

```powershell
rg -n "<candidate path or filename>"
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "recommended child issues under future polish tracker"
  tracker: "recommended tracker: [polish] Setup polish and Python type-discipline suite"
  completed_thread: "local docs update"
  next_thread: "Codex A or Codex B"
  source_artifact: "user request: professional-team presentation recommendations"
  target_artifact: "docs/problem_representations/polish_professional_handoff_readiness.md"
  risk_tier: "Low"
  branch: "codex/polish-and-discipline-suite"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check"
  stop_conditions:
    - "Do not delete files during the first cleanup pass."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not commit raw logs, secrets, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts."
    - "Do not treat docs cleanup as permission to rewrite accepted ADRs or workflow authority."
```
