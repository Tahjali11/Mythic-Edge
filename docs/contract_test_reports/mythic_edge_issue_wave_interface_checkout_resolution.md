# Contract Test Report: Issue-Wave Interface And Checkout-Family Resolution

## Decision

`approve`

`report_lifecycle: final_approval`

The exact issue #859 source package is approved for the contract's guarded
single-skill synchronization and installed read-only Inspect, followed by
Codex F only after target-base authority is explicit. Fresh Codex E
independently verified `ME-IW-859-E-005`: every ambient `GIT_*` value and
ambient `GCM_INTERACTIVE` are removed, only the contracted controlled Git
settings are supplied, origin evidence is local-only, and hostile repository,
global-config, system-config, and fsmonitor cases no longer escape the bounded
read-only inspection. No blocking finding remains. This approval is not Codex
G readiness and grants no merge, Dispatch, deployment, or production authority.

## Issue

- <https://github.com/Tahjali11/Mythic-Edge/issues/859>
- Live state verified on 2026-08-14: `OPEN`, with no comments.
- The issue-scoped `explicit_user_override` remains narrow and current. Live
  PRs #374 and #391 are both still open, so the ordinary WIP-1 evidence named
  by the issue has not disappeared.

## Tracker

N/A.

## Contract

- [Current issue #859 contract](../contracts/mythic_edge_issue_wave_interface_checkout_resolution.md)
- [Additively amended issue-wave contract](../contracts/mythic_edge_issue_wave_skill.md)
- [Agent constitution](../agent_constitution.md)
- [Contract-test role rules](../agent_threads/contract_test.md)
- [Contract-test report template](../templates/contract_test_report.md)

## Implementation Under Test

- Branch: `codex/issue-wave-nomenclature`
- Review base: `origin/main@1cef39a37fa4964730a328f1f1aa98b437478cd6`
- Worktree `HEAD`: `1cef39a37fa4964730a328f1f1aa98b437478cd6`
- Ahead/behind from `origin/main`: `0/0`
- No PR exists for this package, and the future PR base remains undecided.
  Targeting `main` still requires separate explicit authority.

The complete follow-up package contains exactly these eleven paths:

1. `docs/problem_representations/mythic_edge_issue_wave_interface_checkout_resolution.md`
2. `docs/contracts/mythic_edge_issue_wave_interface_checkout_resolution.md`
3. `docs/contracts/mythic_edge_issue_wave_skill.md`
4. `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
5. `docs/codex_skills/mythic-edge-issue-wave/agents/openai.yaml`
6. `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
7. `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
8. `docs/codex_skills.md`
9. `tests/test_mythic_edge_issue_wave_skill.py`
10. `docs/implementation_handoffs/mythic_edge_issue_wave_interface_checkout_resolution.md`
11. `docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md`

## Contract Summary

The package must preserve the existing V2 saved-run and Dispatch model while
adding the preferred `mythicedgeissuewave` vocabulary, canonicalizing public
repository aliases, and producing one closed ephemeral checkout inventory.
The inventory must group a primary checkout with all worktrees registered to
the same resolved Git common directory, keep independent Git stores
ambiguous, use only bounded local read-only Git evidence, suppress optional
locks and prompts, execute no configured or shell-mediated effect, emit no
credentials, and perform no write or network request. Missing or prunable
registrations must remain warnings whose issue-level effect depends on current
authority. Malformed or changing Git evidence must fail closed. The root
coordinator alone binds active work to an issue and may exclude only that
exact issue at the duplicate-work gate; WIP-1, prerequisites, dependencies,
authority, and scope remain independent.

## Internal Project Area Reviewed

Quality / Governance, with local Git and current GitHub metadata used only as
evidence surfaces.

## Bridge-Code Status Reviewed

`shared_support`

## Findings

### ME-IW-859-E-001 - P1 - configured fsmonitor escapes the zero-write boundary

- `finding_lifecycle`: `fixed_state_followup`
- `finding_status`: `fixed and independently verified`
- `blocking_status`: `not_blocking`
- Affected code: `issue_wave_state.py`, `_run_git_read_only` and
  `_inspect_registered_worktree`, especially lines 2741-2763 and 2991-2993.
- Expected: contract lines 151-157 require a bounded command-local read with
  no shell or mutation, and lines 322-326 state that inventory creates no file,
  index refresh, network request, or other side effect.
- Original actual: the helper copied repository configuration into each Git process but
  does not suppress `core.fsmonitor`. `git status` can therefore invoke a
  repository-configured fsmonitor hook. `--no-optional-locks` prevents an
  optional Git lock; it does not disable that configured process.
- Reproduction: a disposable real repository configured an fsmonitor hook
  that writes a marker, initialized the fsmonitor index extension, removed the
  marker, and called `inventory_checkouts`. The result was
  `classification=usable`, `reason=exactly_one_checkout_family`, while
  `fsmonitor_hook_executed=True` and the marker was recreated.
- Impact: a read-only Inspect can execute repository-configured code. Such a
  hook can write locally or access the network, so the implementation does not
  satisfy the automation gate or its no-write/no-network claim even though the
  current live repositories happened not to produce that effect.
- Exact D boundary: prevent all allowed Git probes from consulting or invoking
  configured fsmonitor behavior while keeping `safe.directory` exact and
  command-local. A command-scope environment override of
  `core.fsmonitor=false` was independently shown to suppress the hook without
  changing the closed Git subcommand allowlist. If the fix instead changes the
  contract's exact command prefix, stop and route that syntax change to B.
- Required regression: initialize a real repository with a writing fsmonitor
  hook, run inventory, prove the hook marker remains absent, and compare refs,
  registrations, configuration, indexes, and working bytes before and after.
  Also assert the sanitizing environment cannot be overridden by ambient Git
  config-injection variables.
- Follow-up verification: the child environment now removes ambient
  config-injection keys, supplies only `core.fsmonitor=false`, and preserves
  the exact command-local `safe.directory` argument. The real initialized
  fsmonitor regression left its marker absent and preserved refs,
  registrations, config, index, and working bytes. The focused follow-up set
  passed independently.
- `next_route`: `none`

### ME-IW-859-E-002 - P1 - an existing prunable worktree becomes an unconditional family failure

- `finding_lifecycle`: `fixed_state_followup`
- `finding_status`: `fixed and independently verified`
- `blocking_status`: `not_blocking`
- Affected code: `issue_wave_state.py`, `_inspect_registered_worktree`, lines
  2950-2970.
- Expected: contract lines 228-229 and 246-247 require missing or prunable
  registrations to remain warnings without cleanup; the coordinator blocks
  only when current authority still depends on the registration.
- Original actual: the helper short-circuited only when the registered path did not
  exist. If the directory still exists but its `.git` file is gone, Git marks
  the registration `prunable`; the helper then executes `rev-parse` in the
  stale directory, converts the failure into `checkout_family_inconsistent`,
  drops the prunable warning, and unconditionally blocks the family.
- Reproduction: a disposable linked worktree was created, only its `.git` file
  was removed, and the worktree directory was preserved. Git porcelain
  contained `prunable`, but inventory returned
  `checkout_unavailable_or_ambiguous` /
  `checkout_family_inconsistent` with `warnings=[]`.
- Impact: a stale registration that the contract deliberately leaves for
  authority-aware root handling is instead collapsed into unconditional
  checkout ambiguity.
- Exact D boundary: treat a `prunable` registration as unreadable registration
  evidence even when its path exists. Preserve `missing` and `prunable`
  independently, return null for fields that cannot safely be read, retain the
  family and warning, and perform no cleanup or probe inside the stale path.
- Required regression: remove only `.git` from an existing linked worktree and
  assert `missing=false`, `prunable=true`, null unreadable fields, a
  `prunable_worktree_registration` warning, usable one-family classification,
  and byte-identical registration/config/index evidence.
- Follow-up verification: `_inspect_registered_worktree` now returns the
  registered HEAD/branch plus null unreadable worktree fields when either
  `missing` or `prunable` is true. The existing-path prunable real-Git
  regression remained usable, retained the warning, and preserved registration
  and file evidence.
- `next_route`: `none`

### ME-IW-859-E-003 - P1 - malformed and racing worktree evidence is accepted

- `finding_lifecycle`: `fixed_state_followup`
- `finding_status`: `fixed and independently verified`
- `blocking_status`: `not_blocking`
- Affected code: `issue_wave_state.py`, `_parse_worktree_porcelain`,
  `_registered_branch`, `_registered_head`, and
  `_inspect_registered_worktree`, lines 2867-2912 and 2930-2990.
- Expected: contract lines 313-320 require malformed worktree porcelain to
  become `checkout_family_inconsistent`; the implementation handoff lines
  227-231 asks E to confirm that malformed or changing Git evidence fails
  closed.
- Original actual: the parser accepted a missing or non-hex `HEAD` and a branch that was
  not a `refs/heads/...` ref. The accessors silently convert malformed values
  to `None`; the later inspection then skips the registered-HEAD comparison
  and never compares the registered branch/detached state to the direct
  symbolic-ref result.
- Reproduction: direct parser probes accepted all of `HEAD not-a-commit`, a
  record with no `HEAD`, and `branch not-a-ref`. A controlled full inspection
  then accepted both malformed fields and a same-HEAD branch race, returning
  the later branch instead of `checkout_family_inconsistent`.
- Impact: the inventory can accept corrupt or detectably changing registration
  evidence. HEAD/branch evidence participates in the root's PR and active-work
  reconciliation, so silently normalizing the mismatch weakens the exact
  binding gate.
- Exact D boundary: validate required record fields and their closed
  cross-field combinations, compare registered HEAD, branch, and detached
  state with the direct probes, and detect a changed worktree-registration
  snapshot before returning. Preserve the special null-field route for a
  genuinely missing or prunable registration.
- Required regressions: invalid/missing HEAD, invalid branch ref, contradictory
  branch-plus-detached state, same-HEAD branch race, HEAD race, and a changed
  registration list must each fail closed without raw Git output.
- Follow-up verification: records now require a valid 40-hex HEAD and exactly
  one valid branch or detached state; direct HEAD/branch evidence is compared
  with registration evidence; and the final registration snapshot must match
  the initial bytes. The malformed-record, same-HEAD branch-race, and changed-
  snapshot regressions passed independently.
- `next_route`: `none`

### ME-IW-859-E-004 - P2 - public and authority evidence is internally inconsistent

- `finding_lifecycle`: `fixed_state_followup`
- `finding_status`: `fixed and independently verified`
- `blocking_status`: `not_blocking`
- Affected documentation:
  - `docs/codex_skills.md` lines 73-79 says the helper owns read-only Git
    inventory and then says no helper performs Git operations.
  - The problem representation lines 215-219, current contract lines 440-444,
    and implementation handoff lines 285-289 list ADR-0010 and ADR-0011 under
    `accepted_adrs_read`.
- Expected: vocabulary and authority evidence must be coherent and current.
- Original actual: the first statement contradicted the implemented interface. The ADR
  packets also promote two proposed, non-precedential ADRs into an
  accepted-only field. ADR-0010 and ADR-0011 each state `Status: Proposed`, and
  accepted ADR-0012 lines 204-205 expressly preserves that status.
- Impact: the public skill boundary misstates helper capability, and the
  durable A/B/C packets overstate the authority level used for this protected
  workflow change.
- Exact D boundary: state that the helper performs only the closed local Git
  inventory and no GitHub, mutating, or networked Git operation. Remove
  ADR-0010 and ADR-0011 from each `accepted_adrs_read` list; if they remain
  useful context, label them separately as proposed and non-precedential.
  Preserve accepted ADR-0008 and ADR-0012 and add other accepted ADRs only when
  the responsible role actually re-reads them.
- Required regression/check: current-status assertions for referenced ADRs and
  a docs assertion that does not simultaneously grant and deny helper Git
  inventory.
- Follow-up verification: `docs/codex_skills.md` now distinguishes the bounded
  local Git inventory from forbidden GitHub, mutating, and networked Git
  operations. The A/B/C packets list only accepted ADR-0008 and ADR-0012, and
  the status regression confirms ADR-0010/ADR-0011 remain Proposed.
- `next_route`: `none`

### ME-IW-859-E-005 - P1 - ambient Git state can replace exact checkout identity

- `finding_lifecycle`: `fixed_state_followup`
- `finding_status`: `fixed and independently verified`
- `blocking_status`: `not_blocking`
- Affected code: `issue_wave_state.py`, `_run_git_read_only` and
  `_probe_checkout_root`, especially lines 2741-2753 and 2850-2863.
- Expected: the combined contract lines 116-129 requires inspection of each
  direct child's own origin and resolved common directory, and lines 152-160
  plus 306-309 require an exact, local, deterministic boundary independent of
  ambient identity injection.
- Original actual: `_run_git_read_only` copied the complete ambient environment and
  removes only `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_*`,
  `GIT_CONFIG_VALUE_*`, and `GIT_CONFIG_PARAMETERS`. Git still honors
  repository selectors such as `GIT_DIR`, `GIT_WORK_TREE`, and
  `GIT_COMMON_DIR`, plus alternate global/system configuration selectors such
  as `GIT_CONFIG_GLOBAL`. Also, `_probe_checkout_root` calls `git config
  --get-all` without a local-only configuration boundary.
- Reproduction A: a disposable workspace contained one direct child, while
  `GIT_DIR` and `GIT_WORK_TREE` named a separate same-remote clone outside the
  workspace. Inventory returned `usable` / `exactly_one_checkout_family` and
  reported the external independent clone as primary instead of the direct
  child.
- Reproduction B: a disposable direct child had no local `origin`, while
  `GIT_CONFIG_GLOBAL` named a file containing a matching remote. Inventory
  again returned `usable` even though `git config --local --get-all
  remote.origin.url` proved the direct child had no origin.
- Impact: ambient caller state can introduce an independent clone that the
  bounded workspace scan is explicitly forbidden to discover, or fabricate
  repository identity for a checkout with no local matching remote. The root
  can then bind issues and judge active work against the wrong Git store.
- Exact D boundary: sanitize the ambient Git variables that can redirect the
  repository, worktree, common directory, index, object/ref namespace, or
  configuration sources before every allowed probe. Ensure fetch/push remote
  evidence comes only from the inspected repository's local configuration,
  while preserving the exact command-local `safe.directory`,
  `core.fsmonitor=false`, optional-lock, timeout, no-prompt, generic-error, and
  nine-command boundaries. If local-only remote inspection requires changing
  a contracted command form, route only that syntax point to Codex B.
- Required regressions: with hostile ambient `GIT_DIR`/`GIT_WORK_TREE`, prove
  an outside independent clone cannot replace the direct child; with hostile
  global/system configuration selectors, prove a checkout with no local
  origin cannot acquire one; and prove ordinary local-origin inventory plus
  the E-001 fsmonitor regression remains unchanged and zero-write.
- Follow-up verification: B clarified the two origin probes to use
  `git config --local --get-all`. D now removes all inherited `GIT_*` keys and
  inherited `GCM_INTERACTIVE`, then supplies only the controlled null-global,
  no-system, `core.fsmonitor=false`, optional-lock, prompt, and credential-
  manager settings while preserving exact command-local `safe.directory` and
  the closed nine-command set. Disposable real repositories proved that
  hostile `GIT_DIR`/`GIT_WORK_TREE` cannot substitute an outside clone and
  hostile `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_SYSTEM` cannot fabricate an
  origin. The retained fsmonitor hook remained unexecuted and checked Git and
  working bytes stayed unchanged.
- `next_route`: `none`

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ME-IW-859-E-001` | P1 | `fixed_state_followup` | fixed and independently verified | not_blocking | zero-side-effect Git boundary | initialized fsmonitor/config-injection regressions passed with unchanged Git and working bytes | none |
| `ME-IW-859-E-002` | P1 | `fixed_state_followup` | fixed and independently verified | not_blocking | prunable registrations warn conditionally | existing-path prunable regression remained usable with null unreadable fields and unchanged evidence | none |
| `ME-IW-859-E-003` | P1 | `fixed_state_followup` | fixed and independently verified | not_blocking | malformed/changing evidence fails closed | malformed, branch-race, and registration-snapshot regressions passed | none |
| `ME-IW-859-E-004` | P2 | `fixed_state_followup` | fixed and independently verified | not_blocking | vocabulary and accepted-authority coherence | helper boundary and ADR-status assertions passed | none |
| `ME-IW-859-E-005` | P1 | `fixed_state_followup` | fixed and independently verified | not_blocking | direct-child repository and local-origin identity must not come from ambient Git state | outside-store, global/system-origin, exact-environment, and fsmonitor real-Git regressions passed; selected-root source inventory remained zero-write | none |

## Checks Run

```text
Final independent E-005 checks:

gh issue view 859; gh pr view 374; gh pr view 391
  -> #859 OPEN with no comments; #374 OPEN draft to main; #391 OPEN to main

py -3.13 -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py
  -k "uses_command_local_exact_safe_directory or
      ignores_ambient_repository_redirection or
      ignores_ambient_remote_configuration or
      suppresses_configured_fsmonitor_hook"
  -p no:cacheprovider --basetemp <unique-workspace-local-temp>
  -> 5 passed, 210 deselected

py -3.13 -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py
  -p no:cacheprovider --basetemp <unique-workspace-local-temp>
  -> 215 passed in 56.84s

py -3.13 -B -m pytest -q tests/test_install_codex_skills.py
  -p no:cacheprovider --basetemp <unique-workspace-local-temp>
  -> 46 passed, 3 skipped in 1.08s; skips are Windows directory-symlink
     capability only

source-loaded parse plus selected-root checkout inventory with before/after
HEAD, status, refs, registrations, config, index, and workspace-path snapshot
  -> parse Inspect/A and canonical Mythic-Edge selector; schema v1; 0 scan
     failures; usable; exactly 1 family, 143 worktrees, and 1 primary; 0
     missing/prunable/locked; complete checked snapshot unchanged

residue-safe Python compile
  -> passed

py -3.13 -B tools/check_agent_docs.py
  -> 55 checked, 0 errors, 0 warnings

protected-surface and secret-pattern scans over the exact eleven paths
  -> 11 paths, 0 forbidden, 0 warnings in each scan

tracked plus all untracked path whitespace checks
  -> passed

The D handoff's earlier post-E-005 full-allowlist live attempt is retained as
conservative evidence: one transient linked-worktree `git status` failure made
three large families fail closed as `checkout_family_inconsistent`. The next
separate selected-root Inspect succeeded. Final E's fresh selected-root run
also succeeded; E did not reclassify or erase the transient fail-closed result.

Fresh follow-up E checks:

gh issue view 859; gh pr view 374; gh pr view 391
  -> #859 OPEN; #374 OPEN draft to main; #391 OPEN to main

py -3.13 -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py
  -k "configured_fsmonitor or existing_path_prunable or malformed_worktree or
      same_head_branch_race or changed_registration_snapshot or
      command_local_exact_safe_directory or locked_registration or
      direct_child_path_alias or docs_keep_git_capability"
  -p no:cacheprovider --basetemp <workspace-local-temp>
  -> 13 passed, 199 deselected

py -3.13 -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py
  -p no:cacheprovider --basetemp <workspace-local-temp>
  -> 212 passed in 53.52s

source-loaded parse plus Mythic-Edge checkout inventory with before/after
HEAD, status, registrations, refs, index, and config comparisons
  -> parse Inspect/A; 0 scan failures; usable one-family result; 143
     worktrees; exactly 1 primary; 0 missing/prunable/locked; every checked
     before/after value unchanged

disposable ambient GIT_DIR/GIT_WORK_TREE redirection probe
  -> FAIL: returned usable and reported an outside independent clone as the
     primary instead of the workspace direct child

disposable ambient GIT_CONFIG_GLOBAL remote-injection probe
  -> FAIL: returned usable for a direct child proven to have no local origin

py -3.13 -B tools/check_agent_docs.py
  -> 55 checked, 0 errors, 0 warnings

protected-surface and secret-pattern scans over the exact eleven paths
  -> 11 paths, 0 forbidden, 0 warnings in each scan

tracked plus report whitespace checks
  -> passed

Initial E checks retained as original finding evidence:

git -c safe.directory=<exact-review-worktree> fetch --prune origin main
  -> passed; origin/main remained 1cef39a37fa4964730a328f1f1aa98b437478cd6

gh issue view 859 --repo Tahjali11/Mythic-Edge --json ...
  -> issue OPEN; exact issue body and empty comment set read

gh pr view 374 ...; gh pr view 391 ...
  -> both PRs OPEN, matching issue #859's WIP-1 exception evidence

py -3.13 -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py
  -k "checkout_inventory or repository_selector or preferred_dispatch or metadata_supports or checkout_binding"
  -p no:cacheprovider --basetemp <external-temp>
  -> 24 passed, 176 deselected

py -3.13 -B -m pytest -q tests/test_mythic_edge_issue_wave_skill.py
  -p no:cacheprovider --basetemp <external-temp>
  -> 200 passed in 41.19s

py -3.13 -B -m pytest -q tests/test_install_codex_skills.py
  -p no:cacheprovider --basetemp <external-temp>
  -> 46 passed, 3 skipped; skips are Windows directory-symlink capability

py -3.13 -B -c "compile(...)"
  -> passed without repository bytecode output

source helper inventory-checkouts against the current workspace, summarized
without emitting paths
  -> schema v1; 0 scan failures; 1 Mythic-Edge family; 143 worktrees;
     exactly 1 primary; 0 missing/prunable/locked; 15 dirty; 2 ahead

disposable real-Git existing-path prunable probe
  -> FAIL: prunable=true evidence became checkout_family_inconsistent

controlled malformed/racing porcelain probes
  -> FAIL: malformed HEAD/branch, missing HEAD, and branch race were accepted

disposable initialized core.fsmonitor hook probe
  -> FAIL: fsmonitor_hook_executed=True while inventory returned usable

ruff command/module availability
  -> unavailable; no dependency installed

skill-creator quick_validate.py
  -> unavailable because PyYAML is not installed; no dependency installed

py -3.13 -B tools/check_agent_docs.py
  -> 55 checked, 0 errors, 0 warnings; passed

py -3.13 -B tools/check_protected_surfaces.py --base origin/main
  --paths-from-stdin <exact eleven-path package>
  -> 11 changed paths, 0 forbidden, 0 warnings; passed

py -3.13 -B tools/check_secret_patterns.py --base origin/main
  --paths-from-stdin <exact eleven-path package>
  -> 11 scanned paths, 0 forbidden, 0 warnings; passed

git diff --check plus git diff --no-index --check for all four untracked files
  -> passed
```

## Governance Checks Reviewed

- Public-safe/no-echo behavior: remote normalization and generic subprocess
  failures do not emit the tested credential-bearing URL. The new inventory is
  internal and path-bearing, so it must remain ephemeral.
- Vocabulary coherence: E-004 is fixed and independently verified.
- Authority semantics: exact issue exclusion remains documented as a
  duplicate-work-only effect; WIP-1, prerequisite, dependency, authority, and
  scope gates remain independent. Installation, Dispatch, F, G, merge,
  deployment, and production authority remain separate.
- Fail-closed schemas: the inventory does not enter the saved-run, event, or
  Inspect V2 schemas. E-002 and E-003 remain fixed. E-005 now removes ambient
  Git identity/configuration selectors before the first probe, and the real-
  Git redirection/configuration checks fail closed without changing the
  inventory schema.
- Protected-surface rollout: source-only review remains inside issue #859.
  No skill installation, Dispatch, staging, commit, push, PR change, merge,
  issue closeout, deployment, or production effect occurred.

## Confirmed Contract Matches

- Preferred and backward-compatible command tokens, `(A;)`, segment-only
  terminators, full repository names, short aliases, case-insensitive public
  matching, canonical output, and canonical-only internal repository
  arguments are implemented and tested.
- One normal primary checkout plus linked worktrees inside and outside the
  workspace forms one family in both disposable tests and current live
  inventory.
- Two independent normal Git stores with the same remote remain ambiguous.
- Fetch/push mismatch and missing-repository reasons remain distinct.
- The tested credential-bearing HTTPS remote normalizes without echoing its
  user information.
- The exact command-local `safe.directory` argument, five-second subprocess
  timeout, list-form `subprocess.run`, prompt disabling, captured output,
  `core.fsmonitor=false`, and nine-subcommand allowlist are present. E-001's
  configured-hook defect remains fixed. E-005 additionally proves that all
  inherited `GIT_*` and inherited `GCM_INTERACTIVE` values are removed, global
  and system configuration are disabled, and origin evidence comes only from
  local configuration.
- Checkout inventory is absent from the saved state-schema reference and from
  V2 run/event/Inspect projections. Dispatch transitions, leases,
  reservations, recovery, and reviewed-package bindings have no implementation
  diff.
- No installer implementation, state-schema reference, legacy Role Pool path,
  or R0-bound path appears in the candidate diff.
- Current issue #859 and open PR #374/#391 state agrees with the recorded
  `explicit_user_override`. The override does not waive any downstream gate.

## Contract Mismatches

- None.

## Missing Tests

- None in the contracted issue #859 boundary. Ambient repository redirection,
  global/system origin injection, fsmonitor, existing-path prunable,
  malformed/racing registration, locked-registration, and real direct-child
  path-alias cases all have focused passing regressions.

## Drift Notes

- Repository drift: none observed. Review `HEAD` and refreshed `origin/main`
  exactly match the contracted base.
- Issue lifecycle drift: none observed; #859 remains open.
- PR lifecycle drift: none for the WIP evidence; #374 and #391 remain open.
- Local checkout drift: the current source inventory still reports the same
  one-family/143-worktree summary recorded by C, with all independently checked
  before/after values unchanged. The focused disposable repositories now cover
  the hostile ambient Git identity and configuration states that produced
  E-005.
- Saved-schema/Dispatch drift: none found in the exact diff.
- Installation drift: still unverified. This final source approval permits only
  the contract's already authorized exact predecessor snapshot, one atomic
  synchronization of `mythic-edge-issue-wave`, byte-equality proof, and one
  installed read-only Inspect with rollback on failure.
- Deployment drift: unverified and unauthorized.
- Workbook, parser, transport, and product-runtime drift: not applicable to
  this Quality / Governance package.

## Recommendation

`approve`

No blocking finding remains. Proceed only with the guarded single-skill
synchronization and installed read-only Inspect required by the contract. If
that validation passes, route the unchanged E-approved package to Codex F after
the future PR base is explicitly authorized. Codex G remains a later readiness
review after a draft PR exists; this report does not authorize merge.

## Historical Codex D Route For E-005 (Superseded)

The following blocker packet is retained as original finding evidence. It is
not the current route; `ME-IW-859-E-005` is fixed and independently verified
above.

Codex D may edit only the smallest necessary subset of these current
issue-owned paths:

- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
  only if needed to clarify ambient Git isolation
- `docs/contracts/mythic_edge_issue_wave_interface_checkout_resolution.md`
  only if the exact local-config command or environment boundary must be
  clarified; route that syntax point to B rather than changing it in D
- `docs/implementation_handoffs/mythic_edge_issue_wave_interface_checkout_resolution.md`
  only to record D's exact fixes and fresh validation

D must not edit this E report, the historical issue-wave artifacts, the
state-schema reference, installer implementation, `agents/openai.yaml`, legacy
Role Pool or R0-bound files, saved schemas, Dispatch behavior, credentials, or
any unrelated path. D must not install, Dispatch, stage, commit, push, create
or update GitHub state, target a PR, merge, deploy, clean, or alter worktrees.

Focused validation required before the complete suites:

1. ambient repository/worktree/common-dir/index/object/ref selectors cannot
   replace the direct child's Git store;
2. ambient global/system configuration selectors cannot supply origin evidence
   absent from the inspected repository's local configuration; and
3. normal local-origin inventory and E-001's fsmonitor suppression remain
   exact and zero-write.

Then rerun the complete issue-wave and installer suites, residue-safe compile,
agent-document, protected-surface, secret-pattern, and tracked-plus-untracked
diff checks. Ruff and quick validation remain classified unavailable unless
they become available without dependency installation.

### Pasteable D Prompt

```text
Use the Mythic Edge agent constitution and mythic-edge-workflow skill. Act as
Codex D for issue #859 on branch codex/issue-wave-nomenclature from exact base
origin/main@1cef39a37fa4964730a328f1f1aa98b437478cd6. Read issue #859, both
issue-wave contracts, the C handoff, and
docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md.
Fix only ME-IW-859-E-005 within the exact D path boundary in that report.

Sanitize ambient Git variables that can redirect the repository, worktree,
common directory, index, objects/refs, or configuration sources, and ensure
origin evidence comes only from the inspected repository's local config.
Preserve exact command-local safe.directory, core.fsmonitor=false, the closed
nine-command allowlist, five-second timeouts, no prompts, generic/no-echo
errors, no network, and no writes. Add both real-Git adversarial regressions
named by E and retain the existing E-001 through E-004 regressions, then run
focused and complete residue-safe validation.

Do not change saved schemas, Dispatch rules, installer implementation,
agents/openai.yaml, historical artifacts, legacy Role Pool, R0-bound bytes,
credentials, deployment, production, or any unrelated file. Do not install,
Dispatch, stage, commit, push, create/update GitHub state, target a PR, merge,
clean, or alter worktrees. If the expected contract or exact Git command prefix
must change, stop and route that point to Codex B. Return the exact changed
paths, finding-by-finding evidence, unavailable checks, and a fresh E handoff.
```

```yaml
historical_blocker_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "#859"
  tracker: "N/A"
  completed_thread: "E"
  next_thread: "D"
  source_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md"
  target_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_interface_checkout_resolution.md"
  risk_tier: "high workflow risk; no product-runtime change"
  base_branch: "main"
  target_branch: "undecided; main requires explicit approval"
  branch: "codex/issue-wave-nomenclature"
  internal_project_area: "Quality / Governance"
  truth_owner: "Git owns local checkout evidence; the root coordinator owns issue binding and eligibility"
  bridge_code_status: "shared_support"
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: "issue #859"
    lane_status: "active_second_lane_under_explicit_user_override"
    tracker_selected_next_lane: ""
    exception:
      name: "explicit_user_override"
      blocked_active_issue_or_pr: "open PRs #374 and #391"
      reason: "Complete the bounded issue-wave interface and checkout-family correction."
      allowed_scope: "Exact issue #859 D corrections and fresh E review only."
      expiration_condition: "Issue #859 merge and closeout, explicit park/cancel/reassignment, owner revocation, or current authority change."
      authorized_by: "Human owner in issue #859"
      recorded_in: "GitHub issue #859"
  freshness:
    current_branch: "codex/issue-wave-nomenclature"
    intended_branch: "codex/issue-wave-nomenclature"
    upstream_branch: "origin/main"
    branch_ahead_behind: "0/0 before the unstaged package"
    issue_state: "OPEN"
    tracker_state: "N/A"
    source_artifact_status: "follow-up E report; E-001 through E-004 fixed, E-005 blocking"
    target_artifact_status: "existing D handoff; narrow E-005 update required"
    local_dirty_state: "exact eleven-path issue #859 package including this E report"
    untracked_artifacts:
      - "issue #859 problem representation"
      - "issue #859 current contract"
      - "issue #859 implementation handoff"
      - "this E report"
    worktree_classification: "isolated issue #859 review worktree; preserve all unrelated state"
    historical_freshness_verdict: "current but not approved"
    recommended_route: "D then fresh E"
    verified_at: "2026-08-14"
  validation:
    - "fresh focused E checks: 13 passed, 199 deselected"
    - "fresh complete issue-wave suite: 212 passed"
    - "source parse/inventory: one family, 143 worktrees, 0 scan failures, checked state unchanged"
    - "ambient repository redirection probe: blocking E-005 failure reproduced"
    - "ambient global-config origin probe: blocking E-005 failure reproduced"
    - "D handoff installer suite evidence: 46 passed, 3 capability skips"
  stop_conditions:
    - "Any file or semantic scope outside ME-IW-859-E-005 is needed."
    - "The exact local-config command contract must change; route only that syntax point to B."
    - "Any saved schema, Dispatch, installer, legacy Role Pool, R0, credential, deployment, or production change is needed."
    - "Any installation, submission, GitHub mutation, main-targeting, merge, cleanup, or worktree alteration would occur."
```

```yaml
historical_instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high workflow risk; no product-runtime change"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
    - "ADR-0012"
  protected_surfaces:
    - "workflow invocation and Dispatch admission vocabulary"
    - "local Git read-only and checkout-identity boundary"
    - "active-work exclusion, WIP-1, dependency, authority, and scope gates"
    - "legacy Role Pool and R0-bound files (forbidden)"
  authority_conflicts_found: false
  authority_conflict_notes: "E-004 corrected the A/B/C accepted-ADR lists; E-005 is an implementation defect, not an authority conflict."
  stop_conditions:
    - "No F, installation, installed Inspect, Dispatch, G, merge, issue closeout, deployment, or production action before D and fresh E."
```

## Current Next Workflow Action

Next action: perform the already authorized guarded synchronization of only
`mythic-edge-issue-wave`, prove source/installed byte equality, and run one
installed read-only `mythicedgeissuewave Inspect(A;)`. Restore the exact
pre-sync snapshot if installed validation fails. After successful installed
validation, Codex F may bind and submit only this eleven-path package once the
future PR base has explicit authority.

```text
Use the Mythic Edge agent constitution. Continue issue #859 only from the
final Codex E approval in
docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md.
Preserve an exact temporary snapshot of the currently installed
mythic-edge-issue-wave, atomically synchronize only that skill from the
E-approved repo source, prove complete source/installed byte equality, and run
one installed read-only mythicedgeissuewave Inspect(A;). If installed
validation fails, restore the exact predecessor and stop. Do not Dispatch,
stage, commit, push, create or update a PR, target main, merge, close issue
#859, deploy, clean, or alter unrelated state during installation validation.
After a successful installed check, route the unchanged exact package to Codex
F only after the owner explicitly authorizes the PR target base.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "#859"
  tracker: "N/A"
  completed_thread: "E"
  next_thread: "guarded installed-skill validation, then F"
  source_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md"
  target_artifact: "installed read-only validation evidence, then draft pull request"
  risk_tier: "high workflow risk; no product-runtime change"
  base_branch: "main"
  target_branch: "undecided; main requires explicit approval"
  branch: "codex/issue-wave-nomenclature"
  validation:
    - "final E ambient-state/fsmonitor selection: 5 passed, 210 deselected"
    - "final E complete issue-wave suite: 215 passed"
    - "final E installer suite: 46 passed, 3 Windows symlink capability skips"
    - "final E selected-root source inventory: one family, 143 worktrees, zero scan failures, checked snapshot unchanged"
    - "ME-IW-859-E-001 through ME-IW-859-E-005: fixed and independently verified"
  stop_conditions:
    - "Installed source equality or installed read-only Inspect fails; restore the exact predecessor and stop."
    - "The E-approved eleven-path package changes before F binds it."
    - "The future PR base lacks explicit authority."
    - "Any Dispatch, merge, deployment, issue closure, cleanup, or production effect would occur."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "E"
  risk_tier: "high workflow risk; no product-runtime change"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
    - "ADR-0012"
  protected_surfaces:
    - "workflow invocation and Dispatch admission vocabulary"
    - "local Git read-only and checkout-identity boundary"
    - "active-work exclusion, WIP-1, dependency, authority, and scope gates"
    - "legacy Role Pool and R0-bound files (forbidden)"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #859 records the narrow explicit_user_override; main-targeting and merge remain separately gated."
  stop_conditions:
    - "No package drift before F."
    - "No F submission before installed validation and explicit target-base authority."
    - "No Dispatch, G merge, issue closeout, deployment, or production action from E approval."
```
