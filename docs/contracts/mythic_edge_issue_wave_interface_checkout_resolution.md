# Mythic Edge Issue-Wave Interface And Checkout-Family Contract

## Module

`mythic_edge_issue_wave_interface_checkout_resolution`

This contract extends the invocation and candidate-checkout boundaries in
`docs/contracts/mythic_edge_issue_wave_skill.md`. Every saved-run, event,
lease, reservation, recovery, reviewed-package, role, Dispatch, and stop rule
not explicitly amended here remains unchanged.

## Source Issue

- GitHub issue #859
- `docs/problem_representations/mythic_edge_issue_wave_interface_checkout_resolution.md`

Historical issues #855 and #857 remain closed evidence only.

## Tracker

N/A.

## Owning Layer

Quality / Governance.

## Internal Project Area

Quality / Governance, with local Git and current GitHub metadata as evidence
surfaces.

## Truth Owners

- The invocation parser owns accepted syntax and canonical selector output.
- Git owns checkout-family registration, primary-worktree identity, common-
  directory identity, refs, branches, index/worktree status, and upstream
  relationships.
- Current GitHub issues and PRs plus current repo contracts, handoffs, and
  non-final issue-wave ledgers own durable active-issue evidence.
- The root coordinator owns evidence reconciliation, issue binding, WIP-1,
  prerequisites, authority, dependency and scope gates, ranking, and lane
  selection.

The helper is not a truth owner for GitHub state or issue eligibility.

## Bridge-Code Status

`shared_support`

## Files Owned By This Contract

- `docs/problem_representations/mythic_edge_issue_wave_interface_checkout_resolution.md`
- `docs/contracts/mythic_edge_issue_wave_interface_checkout_resolution.md`
- `docs/contracts/mythic_edge_issue_wave_skill.md`
- `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
- `docs/codex_skills/mythic-edge-issue-wave/agents/openai.yaml`
- `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `docs/codex_skills.md`
- `tests/test_mythic_edge_issue_wave_skill.py`
- `docs/implementation_handoffs/mythic_edge_issue_wave_interface_checkout_resolution.md`
- `docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md`

The state-schema reference, installer implementation, legacy Role Pool and
R0-bound files, historical issue-wave artifacts, and unrelated tests are
read-only.

## Public Invocation Interface

Preferred form:

```text
mythicedgeissuewave <Inspect|Dispatch> (<role-or-segment>;[ <option>[; <option> ...]])
```

Backward-compatible form:

```text
$mythic-edge-issue-wave <Inspect|Dispatch> (<role-or-segment>[; <option>[; <option> ...]])
```

The exact lowercase token `mythicedgeissuewave` is discoverable. Discovery
loads instructions only and grants no execution or Dispatch authority.

A single trailing semicolon is accepted only when the body contains a role or
segment and no option, making `(A;)` and `(A-B;)` valid. Empty options, doubled
semicolons, and a trailing semicolon after an option fail closed.

`repos=` and `anchor=` accept, case-insensitively:

1. canonical `owner/repository` identity;
2. the full repository name; or
3. the exact non-empty suffix after `Mythic-Edge-`.

Every selector becomes the existing canonical `Tahjali11/...` identity before
duplicate checks or downstream use. The root repository accepts
`Tahjali11/Mythic-Edge` and `Mythic-Edge`; it gains no invented nickname.
Internal manifests and run state remain canonical-only.

No user-facing path option, checkout-path selector, or persistent local
checkout map is added.

## Internal Checkout-Inventory Operation

```text
inventory-checkouts --workspace-root <root> --repository <canonical>...
```

The operation accepts one existing directory and one or more unique canonical
allowlisted repository identities. Repository aliases are rejected at this
internal boundary.

It must:

1. resolve the workspace root without creating it;
2. examine only direct child directories containing a `.git` directory or
   file;
3. read each direct child's origin fetch and push configuration, normalize the
   identities without emitting raw URLs, and resolve its Git common directory;
4. group matching direct children by resolved Git common directory;
5. use Git's registered primary worktree as the family's main checkout;
6. enumerate all registered linked worktrees from that family, including
   worktrees located outside the workspace root;
7. report every registered worktree's path, branch, HEAD, dirty and untracked
   state, upstream name, ahead/behind counts, detached state, missing state,
   prunable state, locked state, and primary status;
8. report multiple independent Git stores, fetch/push mismatch, missing
   repositories, and bounded Git-inspection failures distinctly; and
9. return deterministic ordering with no timestamp or ambient identifier.

Independent clones outside the workspace are not searched. A linked worktree
outside it is included only because the selected family's Git registration
names it.

### Read-only Git command boundary

The helper may invoke only this closed command set:

```text
git -c safe.directory=<exact-path> --no-optional-locks -C <path> config --local --get-all remote.origin.url
git -c safe.directory=<exact-path> --no-optional-locks -C <path> config --local --get-all remote.origin.pushurl
git -c safe.directory=<exact-path> --no-optional-locks -C <path> rev-parse --git-common-dir
git -c safe.directory=<exact-path> --no-optional-locks -C <path> worktree list --porcelain -z
git -c safe.directory=<exact-path> --no-optional-locks -C <path> rev-parse --verify HEAD
git -c safe.directory=<exact-path> --no-optional-locks -C <path> symbolic-ref --quiet --short HEAD
git -c safe.directory=<exact-path> --no-optional-locks -C <path> status --porcelain=v1 -z --untracked-files=all
git -c safe.directory=<exact-path> --no-optional-locks -C <path> rev-parse --abbrev-ref --symbolic-full-name @{upstream}
git -c safe.directory=<exact-path> --no-optional-locks -C <path> rev-list --left-right --count HEAD...@{upstream}
```

`safe.directory` is an exact resolved path applied to that command only; the
helper never reads or writes the user's global allowlist. Every command uses
`GIT_OPTIONAL_LOCKS=0`, disables terminal prompting, runs without a shell,
captures output, has a five-second timeout, and returns only generic failure
codes. Before invoking Git, the helper removes every ambient `GIT_*` value and
the ambient `GCM_INTERACTIVE` value. It then supplies only controlled optional-
lock and prompt settings, a command-scoped `core.fsmonitor=false` override, a
null global-config source, and disabled system-config loading. Remote evidence
comes only from `git config --local`; merged global or system configuration
cannot supply an origin. This prevents repository redirection, configuration
injection, and configured file-system monitor processes during inventory. The
final worktree-registration snapshot must exactly match the initial snapshot
or the family fails closed. The helper must never fetch, pull, push, prune,
repair, checkout, switch, reset, clean, add, commit, remove, create, lock,
unlock, or write configuration.

No raw Git stdout, stderr, or remote URL may enter an error or result. Remote
normalization strips user information before comparison. Non-GitHub local or
unusual remotes may be represented internally by a one-way digest, but only a
normalized exact GitHub identity can match an allowlisted repository.

## Ephemeral Checkout-Inventory Schema

The operation returns the closed
`mythic_edge_issue_wave_checkout_inventory.v1` object:

```json
{
  "schema_version": "mythic_edge_issue_wave_checkout_inventory.v1",
  "scan_failures": [
    {
      "path": "<resolved direct child>",
      "reason": "git_inspection_failed"
    }
  ],
  "repositories": [
    {
      "repository": "Tahjali11/Mythic-Edge",
      "classification": "usable",
      "reason": "exactly_one_checkout_family",
      "conflicts": [],
      "warnings": [],
      "families": [
        {
          "git_common_dir": "<resolved path>",
          "primary_worktree": "<resolved path>",
          "remote_identity": "Tahjali11/Mythic-Edge",
          "worktrees": [
            {
              "path": "<resolved path>",
              "primary": true,
              "head": "<40 lowercase hex or null>",
              "branch": "main",
              "detached": false,
              "dirty": false,
              "untracked": false,
              "upstream": "origin/main",
              "ahead": 0,
              "behind": 0,
              "missing": false,
              "prunable": false,
              "locked": false
            }
          ]
        }
      ]
    }
  ]
}
```

For an unavailable or ambiguous repository, `classification` is exactly
`checkout_unavailable_or_ambiguous`. `reason` is one of:

- `repository_not_found`;
- `multiple_independent_git_stores`;
- `fetch_push_remote_mismatch`;
- `git_inspection_failed`; or
- `checkout_family_inconsistent`.

For a usable repository, `reason` is exactly
`exactly_one_checkout_family`. `conflicts` contains only resolved direct-child
paths and a closed reason. `warnings` is a sorted unique list drawn from
`missing_worktree_registration` and `prunable_worktree_registration`.

Missing worktree fields that cannot be read are null, while `missing` and
`prunable` preserve Git/OS evidence. A stale registration is not altered.

This object is consumed in memory. It is never written to `.codex`, appended
to an issue-wave ledger, added to a saved-run schema, quoted in a public role
packet, or retained in a handoff. A coordinator may summarize its current
classification and safe evidence without persisting local paths.

## Checkout-Family Classification

- Exactly one matched common directory is one usable checkout family.
- More than one matched common directory is multiple independent Git stores
  and remains `checkout_unavailable_or_ambiguous`, even when every remote and
  worktree is clean.
- A fetch/push mismatch touching the selected identity blocks that repository.
- No matched family is `repository_not_found`.
- Any direct Git child that cannot be inspected makes the scan fail closed;
  the helper cannot prove that it is unrelated.
- Missing or prunable registrations warn without cleanup. The coordinator
  blocks only when current run authority still depends on that registration.

Path aliases resolving to the same common directory do not create a second
family. Matching remotes alone never merge distinct common directories.

## Active-Issue Binding And Duplicate Exclusion

The root coordinator, not the helper, reconciles each current worktree against:

1. current open PR head/base/issue linkage and current issue state;
2. non-final issue-wave ledgers with exact repository and issue identity; or
3. current repo-authorized contracts or handoffs tied to an open issue.

A binding is usable only when these sources support exactly one repository
issue. Branch and folder issue numbers are query hints only; they may direct a
read but cannot establish a binding.

When current evidence proves a worktree is active and bound to one issue, the
duplicate-work check must exclude only that exact issue. Every other issue in
the repository proceeds to its own WIP-1, prerequisite, authority, dependency,
checkout, active-work, and scope checks. The binding does not create a WIP
exception and does not make any other issue eligible.

A clean historical worktree with no current active-work evidence is ignored.
A dirty or untracked worktree, an ahead worktree, a non-final ledger lane, or
an open-PR worktree without exactly one authoritative issue binding blocks the
repository. A clean detached worktree or issue-shaped branch name is not by
itself active-work proof; current durable evidence decides whether it is
historical or active.

If issue X is the exact binding, exclude X at the duplicate-work gate and
evaluate issue Y normally. If the worktree cannot bind exactly, block the
repository before selecting X or Y.

## Inspect Output Contract

Inspect records, separately for every considered issue:

- checkout identity or checkout ambiguity;
- the exact active issue excluded as duplicate work, when any;
- WIP-1 compatibility or the exact current issue-scoped exception;
- prerequisite and dependency status;
- repository authority compatibility;
- scope and submission-lane conflicts; and
- final admitted or excluded status.

Zero selected lanes is valid when these independent gates exclude every issue.
The output must not collapse all reasons into checkout ambiguity.

## Invariants

- Nomenclature aliases affect only public invocation parsing.
- Checkout paths are supplied only through the internal operation by the
  coordinator; users receive no new path syntax.
- Common-directory identity, not folder count or remote equality alone,
  defines a checkout family.
- The registered primary worktree is the main checkout.
- Git inventory is bounded, local, deterministic, read-only, and network-free.
- Optional Git locks remain disabled for every command.
- No remote credentials are emitted.
- The checkout inventory never becomes saved state or public handoff data.
- Active-issue binding is current-evidence-based and exact.
- Duplicate exclusion never waives WIP-1, dependency, authority, or scope.
- Existing invocation V2 and state/event/inspect V2 schemas do not change.
- Legacy Role Pool and R0-bound bytes do not change.

## Error Behavior

Invalid workspace roots, noncanonical or duplicate repository arguments, and
unsupported command forms return `invalid_command` without echoing unsafe
input. Local Git failures and timeouts become generic
`git_inspection_failed` evidence. Malformed worktree porcelain or inconsistent
common-directory identity becomes `checkout_family_inconsistent`. The helper
never retries or repairs.

## Side Effects

The inventory operation has none. It creates no file, directory, lock,
worktree, branch, ref, index refresh, config update, network request, ledger,
or saved-run object.

After complete validation and fresh E approval, the owner authorizes one
rollback-capable synchronization of only the installed
`mythic-edge-issue-wave`, followed by byte-equality proof and one installed
read-only Inspect. That later operation is distinct from inventory and grants
no Dispatch, merge, deployment, or production authority.

## Dependency Order

1. Add failing nomenclature, inventory, and binding-rule tests.
2. Publish this combined A/B package under issue #859.
3. Implement the bounded inventory operation and protocol changes.
4. Run focused then complete local validation.
5. Run a source-loaded read-only Inspect and reconcile zero-write evidence.
6. Route concrete findings through D and repeat validation.
7. Obtain a fresh independent E report for the exact package.
8. Preserve the installed baseline, sync one skill, prove equality, and run
   installed Inspect; restore the baseline if validation fails.
9. F submits only E's reviewed package to a draft PR after target-base
   authority is explicit.
10. G verifies exact identity, checks, review threads, issue/WIP state, and
    live-test evidence, then stops before merge.

## Compatibility

All previously valid `$mythic-edge-issue-wave` invocations and canonical
repository selectors remain supported. No saved data migration exists or is
needed. The legacy Role Pool is unchanged.

## Tests Required

- preferred and backward-compatible commands, `(A;)`, explicit segment
  terminators, all repository selector forms, canonical output, and malformed
  input rejection;
- one primary checkout with linked worktrees inside and outside the workspace;
- exact-issue exclusion without excluding unrelated issues from WIP-1,
  dependency, authority, and scope gates;
- clean historical worktrees;
- dirty, untracked, ahead, detached, and unbound active work;
- two independent clones using the same remote;
- fetch/push mismatch, missing repository, resolved path aliases, stale or
  prunable registration, Git failure, timeout, and credential-safe remotes;
- exact refs, worktree registrations, configuration, indexes, and working-file
  bytes before and after inventory;
- internal canonical-only CLI input and zero saved state;
- a closed allowlist of Git commands with no network or mutating verb;
- complete issue-wave and installer suites plus lint, skill, docs,
  protected-surface, secret, and diff validation.

## Acceptance Criteria

- Git's primary worktree and registered linked worktrees form exactly one
  family when they share one resolved common directory.
- Independent clones remain ambiguous.
- Every required worktree state is reported without writing.
- Credentials never appear in output or errors.
- The root can exclude only that exact issue when authoritative active-work
  evidence binds a worktree, while unrelated issues still face every normal
  gate.
- A clean historical worktree does not block selection.
- Unbound active-looking work blocks the repository.
- Missing/prunable registrations are preserved and classified according to
  current authority dependency.
- Inspect distinguishes checkout, duplicate issue, WIP-1, dependency,
  authority, and scope reasons.
- No V2 saved schema, Dispatch rule, installer implementation, legacy Role
  Pool path, R0-bound byte, credential, deployment, or production behavior
  changes.
- Source-loaded and installed read-only Inspect evidence passes, a fresh E
  report has no blocking findings, F submits the exact reviewed package, and G
  stops before merge.

## Next Workflow Action

Next role: Codex C, Module Implementer.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "#859"
  tracker: "N/A"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/mythic_edge_issue_wave_interface_checkout_resolution.md"
  target_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_interface_checkout_resolution.md"
  risk_tier: "high workflow risk; no product-runtime change"
  base_branch: "main"
  target_branch: "undecided; main requires explicit approval"
  branch: "codex/issue-wave-nomenclature"
  validation:
    - "Nine contract-first tests fail at the missing inventory function, CLI, schema, and combined binding contract."
  stop_conditions:
    - "Any saved-run schema, Dispatch, installer implementation, legacy Role Pool, or R0-bound change."
    - "Any Git command outside the closed read-only allowlist."
    - "Any persistence of checkout inventory or local paths in public handoffs."
    - "Any unapproved main-targeting or merge."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
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
    - "local checkout identity and active-work exclusion"
    - "legacy Role Pool and R0-bound files (forbidden)"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #859 records the narrow explicit_user_override; draft-PR base and merge authority remain separate gates."
```
