# Mythic Edge Issue-Wave Interface And Checkout-Family Implementation Handoff

## Source

- GitHub issue #859
- `docs/problem_representations/mythic_edge_issue_wave_interface_checkout_resolution.md`
- `docs/contracts/mythic_edge_issue_wave_interface_checkout_resolution.md`
- additive amendment to `docs/contracts/mythic_edge_issue_wave_skill.md`

## Role Performed

Codex C: Module Implementer.

## Intended Behavior

- Preserve preferred `mythicedgeissuewave`, `(A;)`, repository aliases, and
  backward-compatible `$mythic-edge-issue-wave` syntax.
- Treat Git's primary checkout and every linked worktree sharing one resolved
  common directory as one checkout family.
- Include Git-registered linked worktrees outside the workspace without
  searching there for independent clones.
- Report local branch, HEAD, dirty/untracked, upstream, ahead/behind, detached,
  missing, prunable, and locked evidence with no Git or network write.
- Keep multiple independent stores and fetch/push mismatch fail-closed.
- Let the root coordinator bind active worktrees from current authority and
  exclude only the exact bound issue from duplicate-work detection.
- Keep WIP-1, prerequisite, dependency, authority, and scope gates independent.

## Actual Behavior Before The Change

The pending invocation package accepted the intended shorter vocabulary, but
the source skill still prohibited helper Git reads and instructed the
coordinator to match exactly one local checkout folder. A primary checkout and
its normal registered task worktrees could therefore be mistaken for
independent clones.

## First Proven Failure Point

With a workspace-local temporary root, nine new contract-first tests failed:

- seven direct calls failed because `inventory_checkouts` did not exist;
- the CLI rejected `inventory-checkouts`; and
- the combined binding contract and controller wording did not exist.

An earlier attempt reached the restricted system temp directory and failed in
pytest fixture setup. That setup failure was classified separately and is not
implementation evidence.

## Exact Fix

### Invocation boundary

The earlier pending input-only changes remain intact:

- exact lowercase `mythicedgeissuewave` plus the original `$` token;
- one no-option trailing semicolon;
- canonical, full-name, and exact short repository selectors at public input;
- canonical downstream identities; and
- implicit discovery that loads instructions but grants no effect.

### Checkout inventory

Added the internal operation:

```text
inventory-checkouts --workspace-root <root> --repository <canonical>...
```

It scans only direct workspace children with `.git`, reads origin fetch/push
configuration, groups exact remote matches by resolved common directory, and
uses `git worktree list --porcelain -z` to identify the registered primary and
all linked worktrees. Every existing registered worktree is inspected through
a closed nine-command Git allowlist.

All subprocesses run without a shell, have a five-second timeout, set
`GIT_OPTIONAL_LOCKS=0`, disable prompts, and discard raw stdout/stderr on
failure. Each command supplies the exact inspected path as a command-local
`safe.directory` value so a sandbox can read owner-created checkouts without
changing global Git configuration. Remote normalization strips user
information; only canonical
repository identity is emitted. Nonmatching unusual remotes become one-way
opaque identities in memory.

The closed `mythic_edge_issue_wave_checkout_inventory.v1` result is printed
only for immediate coordinator consumption. No state-schema, ledger, manifest,
event, or public handoff field was added.

### Coordinator policy

The skill and controller now require current PR/issue evidence, a non-final
issue-wave ledger, or a current contract/handoff tied to an open issue for
authoritative binding. Branch and folder numbers are hints only. One bound
issue is excluded only from its own duplicate-work predicate. Clean historical
worktrees are ignored; dirty, ahead, in-progress, or open-PR work without one
exact binding blocks the repository.

## Files Changed

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

The three nomenclature-only untracked artifact names were replaced by the
combined names. The state-schema reference, installer implementation and
tests, historical issue-wave artifacts, legacy Role Pool, and R0-bound files
are unchanged.

## Contract-First And Focused Validation

```text
Contract-first regression:
  9 failed, 190 deselected
  Failures were the missing function, CLI, schema, and binding policy.

Focused corrected regression:
  9 passed, 190 deselected

D safe-directory contract-first regression:
  1 failed, 199 deselected

D corrected checkout/binding regressions:
  10 passed, 190 deselected

First E finding regressions before D:
  11 failed, 199 deselected

E-001 through E-004 corrected regressions:
  11 passed, 199 deselected

Locked-registration and direct-child path-alias regressions:
  2 passed, 210 deselected
```

## Codex D Correction

The first source-loaded live inventory failed every direct Git child with
Git's dubious-ownership protection because the sandbox account differs from
the checkout owner. Workspace paths and the current repository snapshot were
unchanged, but the result could not distinguish real families.

D added a failing command-construction regression, then supplied only the
exact current root through Git's command-local `-c safe.directory=<path>`
option. No global configuration, wildcard trust, persistent mapping, or file
write is used.

The first independent E review then reported four blocking findings. D made
only the bounded corrections requested by that report:

- `ME-IW-859-E-001`: remove ambient Git config-injection variables and apply
  only `core.fsmonitor=false` in the child environment, preventing configured
  file-monitor hooks from executing;
- `ME-IW-859-E-002`: preserve an existing-path prunable registration as a
  warning without probing it, while keeping `missing` and `prunable`
  independent;
- `ME-IW-859-E-003`: validate required HEAD/branch/detached record shape,
  compare direct HEAD and branch evidence, and require a second worktree-
  registration snapshot to match the first; and
- `ME-IW-859-E-004`: reconcile the helper's public Git capability wording and
  remove proposed ADR-0010 and ADR-0011 from `accepted_adrs_read` fields.

D also added the two non-blocking focused cases identified by E: a locked
registration and a real direct-child Windows path alias. Neither changes
classification or persistent state.

Fresh E independently verified `ME-IW-859-E-001` through E-004, then found
`ME-IW-859-E-005`: ambient Git repository or configuration variables could
redirect the helper to an outside store or fabricate a matching origin.

That finding required one B clarification because the contract's exact remote
command changed. B now requires `git config --local --get-all` for origin URL
and push URL evidence. D then removes every ambient `GIT_*` value plus ambient
`GCM_INTERACTIVE`, supplies only controlled no-system/null-global, file-
monitor, optional-lock, and prompt settings, and retains the exact inspected
path through command-local `safe.directory`. Real-Git regressions prove an
outside independent clone and injected global or system origin can no longer
replace the direct child's identity.

## Complete Post-D Validation

```text
Complete issue-wave suite:
  215 passed in 59.08s

Complete installer suite:
  46 passed, 3 skipped in 1.13s
  Skips: Windows directory-symlink capability only

Python compile:
  passed

Agent documents:
  55 checked, 0 errors, 0 warnings

Protected surfaces across the exact working package:
  11 paths, 0 forbidden, 0 warnings; passed

Secret patterns across the exact working package:
  11 paths, 0 forbidden, 0 warnings; passed

Tracked diff plus all changed/untracked path whitespace:
  passed
```

The E-005 contract-first selection produced four expected failures and one
unaffected pass. After B/D, the same selection produced five passes with 210
deselected.

Ruff is unavailable as a command and as a module in both available Python
runtimes. The official skill validator is unavailable because both runtimes
lack PyYAML. No dependency was installed. Compile, the complete issue-wave and
installer suites, metadata assertions, agent-doc validation, protected-surface
and secret checks provide the available source evidence; CI must still run
the repository-owned lint check after submission.

## Source-Loaded Live Inspect

The updated repo-owned skill was re-read in full, then
`mythicedgeissuewave Inspect(A;)` was parsed and run without installation.

Observed checkout results:

- zero Git scan failures;
- Mythic-Edge: one family containing 143 registered worktrees;
- Automation Artifacts: one family containing 25 worktrees;
- Corpus: one family containing one worktree;
- Fable Engine: one family containing seven worktrees;
- Governance: one family containing one worktree;
- Research and Development: one family containing seven worktrees;
- Security: one family containing 39 worktrees;
- Application Function: two true independent Git stores, correctly
  `checkout_unavailable_or_ambiguous`;
- Analytics and Feature Expansions: no matching checkout;
- no missing, prunable, or locked registration in a matched family.

Observed issue-level routing:

- the current dirty issue #859 lane bound exactly through the open issue,
  current combined contract, and handoff, so only #859 was excluded as active
  duplicate work;
- other Mythic-Edge issues remained independently WIP-incompatible while open
  PRs #374 and #391 exist, and additional dirty/ahead worktrees without one
  proven current issue binding block the repository;
- other single-family repositories with dirty/ahead unbound work remain
  blocked independently rather than being called checkout-ambiguous;
- Governance has a clean single checkout and no open PR, but only a README and
  no current A-through-F authority, so its open tracker issues #1 and #2 are
  authority-incompatible; #2 is also explicitly parked;
- no candidate satisfied every checkout, active-work, WIP-1, prerequisite,
  authority, dependency, and scope gate, so zero lanes was the correct result.

The earlier before/after live evidence proved the workspace path set, current
repository HEAD, status, refs, worktree registrations, config bytes, and index
bytes unchanged. The corrected real-Git regressions repeat those byte checks
for the new file-monitor, stale-registration, locked-registration, and path-
alias cases. A fresh GitHub read verified issue #859 remains open and PRs #374
and #391 remain the only open root PRs. No ledger, file, branch, worktree,
task, issue, comment, PR, check, or other local or GitHub write occurred.

After the E-005 isolation fix, the first full-allowlist live inventory failed
closed for three large active families as `checkout_family_inconsistent`.
Tracing the first root failure identified one transient `git status` failure
in an active linked worktree; the same exact bounded command immediately
succeeded. A new source-loaded selected-root
`mythicedgeissuewave Inspect (A; repos=Mythic-Edge)` then completed with zero
scan failures, exactly one family, 143 worktrees, one primary, and no missing,
prunable, or locked registrations. The transient run was therefore preserved
as conservative drift evidence rather than reclassified as clone ambiguity.

## Preserved Boundaries

- No saved-run schema or state transition changed.
- No Dispatch operation or authority changed.
- No fetch, prune, checkout, cleanup, repair, or remote request was added.
- No installer implementation, legacy Role Pool, R0-bound, credential,
  deployment, production, or unrelated file changed.
- No merge is authorized.
- The existing isolated worktree and unrelated user state are preserved.

## Remaining Review Focus

1. Confirm every Git command is both necessary and read-only with optional
   locks disabled.
2. Confirm path/common-directory grouping cannot merge independent stores.
3. Confirm malformed or changing Git evidence fails closed without leaking
   remotes or credentials.
4. Confirm exact-issue exclusion cannot waive WIP-1, dependency, authority, or
   scope gates.
5. Confirm the ephemeral inventory cannot enter saved schemas or public role
   packets.

## Next Workflow Action

Send the exact unstaged package back to a fresh independent Codex E review. E
must verify `ME-IW-859-E-005`, both ambient-state adversarial probes, the
local-only command clarification, the complete diff and untracked additions,
post-D validation, and the source-loaded selected-root Inspect evidence. E may
edit only
`docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md`.

```yaml
workflow_handoff:
  role_performed: "Codex D: Issue Fixer after Codex C implementation"
  repository: "Tahjali11/Mythic-Edge"
  issue: "#859"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_interface_checkout_resolution.md"
  target_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_interface_checkout_resolution.md"
  risk_tier: "high workflow risk; no product-runtime change"
  base_branch: "main"
  target_branch: "undecided; main requires explicit approval"
  branch: "codex/issue-wave-nomenclature"
  authority_notes:
    installation_scope: "one post-E sync of mythic-edge-issue-wave with exact predecessor snapshot and rollback"
    real_inspect_authorized: true
    dispatch_authorized: false
    github_issue_and_draft_pr_authorized: true
    merge_authorized: false
  stop_conditions:
    - "Any saved-run schema or Dispatch behavior would change."
    - "Any Git command outside the closed read-only allowlist is needed."
    - "Any legacy Role Pool, R0-bound, installer, deployment, or production edit."
    - "Any unapproved main-targeting or merge."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "D"
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
  authority_conflict_notes: "Issue #859 records the narrow explicit_user_override; main-targeting and merge remain separately gated."
```
