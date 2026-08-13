# Mythic Edge Issue Wave Skill Implementation Handoff

## Issue

[Issue #855](https://github.com/Tahjali11/Mythic-Edge/issues/855)

## Tracker

N/A.

## Contract

`docs/contracts/mythic_edge_issue_wave_skill.md`

## Internal Project Area

Quality / Governance, with External / Collaboration Surface and Generated /
Local Artifacts as adjacent boundaries.

## Truth Owner

Current GitHub and Git evidence owns collaboration and checkout facts. Each
lane's current repo authority, issue, contract, handoff, diff, and tests own
its workflow facts. The root Codex owns candidate and overlap judgment.
`events.jsonl` owns ordered local transition history, while `run.json` is its
atomic projection. The helper owns mechanical validation only.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer.

## What Changed

Added the repo-owned, explicit-only `$mythic-edge-issue-wave` skill. It can
source-load a zero-write Inspect protocol or coordinate an expressly requested
Dispatch through fresh A/B/C/E/F waves. A standard-library helper provides
strict invocation parsing, supplied-manifest validation, fail-closed local
state transitions, a hash-chained event ledger, atomic projection recovery,
and redacted public inspection. GitHub/Git reads and writes, candidate
judgment, native-agent creation, and consequential workflow decisions remain
root-Codex responsibilities.

## Files Changed

- `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
- `docs/codex_skills/mythic-edge-issue-wave/agents/openai.yaml`
- `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
- `docs/codex_skills/mythic-edge-issue-wave/references/state-schema.md`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- `tests/test_install_codex_skills.py`
- `docs/codex_skills.md`
- `docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md`

The pre-existing untracked B contract was read but not edited. Its SHA-256
remained `3fcf0b0ba2c3833d69932672d0e3abbe9ae0d35ef1b560c987ab56e5e70cc64f`.

## Code Changed

No product runtime code changed. The new local workflow helper is deterministic,
network-free, agent-free, and limited to parsing, validation, local ledger
state, projection recovery, and redacted inspection.

## Tests Added Or Updated

- Added 54 focused tests for the full invocation grammar, deterministic
  admission, all forward/stop transitions and forbidden shortcuts, locking,
  revisions, schema strictness, hash-chain integrity, crash recovery,
  permission immutability, path redaction, no-echo failures, and governance
  routing.
- Synthetic Dispatch tests use disposable local Git repositories and remotes,
  fake role outcomes, and mocked PR/check boundaries. They cover one-, two-,
  and three-lane runs, A ambiguity, post-A conflicts without backfill,
  unaffected-lane continuation, A-through-F success, E-to-D routing, CI pass,
  failure, timeout, unknown outcomes, recovery, and governance fallback.
- Extended installer tests for list, dry-run, and temporary-target install
  behavior without installing into the real Codex skills directory.
- Added a deterministic legacy Role Pool tree assertion.

## Interface Changes

- Added explicit grammar:
  `$mythic-edge-issue-wave <Inspect|Dispatch> (A[; option ...])`.
- Added helper CLI commands `parse`, `init`, `transition`, and `inspect`.
- Added strict candidate-manifest, event-update, run-projection, governance,
  and redacted-inspection schemas documented in the skill references.
- Added UI metadata with `allow_implicit_invocation: false`; the display-name
  overlap therefore cannot silently replace the legacy skill.
- Existing product, workbook, webhook, credential, deployment, issue, and PR
  interfaces are unchanged.

## Contracted Area Status

Implementation stayed within the contract's file allowlist and Quality /
Governance area. No parser, analytics, workbook, webhook, deployment, runtime,
credential, or R0-bound surface changed. The legacy
`docs/codex_skills/mythic-edge-role-pool` tree remains exactly
`950768b80b760a0e0dfe3040df023de20eadaf81` with 38 tracked files, no diff,
and no untracked additions.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: strict no-echo error envelopes, local path
  redaction, and governance-packet allowlisting are implemented and tested.
- Vocabulary and example coherence: mode, state, stop, check, and role terms
  use the contract's closed vocabulary.
- Authority/readiness semantics: passing validation stops at
  `g_consideration_ready`; it grants no merge, deployment, installation, or
  real-Dispatch authority.
- Fail-closed schema or validator checks: unknown/duplicate fields, duplicate
  JSON keys, stale revisions, broken chains, invalid tails, drift, and unknown
  agent outcomes fail closed.
- Protected-surface rollout phase: implementation and local validation only;
  independent E review and later F submission remain required.

## Source-Loaded Live Inspect

Observed read-only evidence for `$mythic-edge-issue-wave Inspect (A)`:

- `Tahjali11/Mythic-Edge` had 38 matching local checkout directories, so exact
  checkout identity was ambiguous and the repository was excluded.
- `Tahjali11/Mythic-Edge-Security` had one matching checkout. It had active
  issue #118, a dirty branch, and no complete durable repo-specific A/B/C/E/F
  convention set, so it was excluded.
- The other eight allowlisted repositories existed on GitHub but had no
  matching local checkout and were excluded.
- Zero candidates were selected and no A prompt was emitted.

Before/after evidence matched: current worktree status, issue #855 and #118
timestamps, and absence of the local role-pool run-state root were unchanged.
Only read operations were used on GitHub. No run manifest, event, lock,
worktree, branch, commit, PR, issue, check, task, or other local/GitHub write
was created.

## Validation Run

```text
py -m pytest tests/test_mythic_edge_issue_wave_skill.py -q
54 passed

py -m pytest tests/test_install_codex_skills.py -q
45 passed, 3 skipped (directory symlinks unsupported by this filesystem)

py -B tools/install_codex_skills.py --list
passed; four repo-owned skills listed, including mythic-edge-issue-wave

py -B tools/check_agent_docs.py
passed; 55 files, 0 errors, 0 warnings

py -B tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
passed; 9 contracted changed paths, 0 forbidden, 0 warnings

py -B tools/check_secret_patterns.py --base origin/main --paths-from-stdin
passed; 9 contracted changed paths, 0 forbidden, 0 warnings

py -B -m py_compile <changed Python files>
passed with bytecode redirected outside the repository

git diff --check
passed
```

## ME-IW-855-E-008 Codex D Addendum

Codex D fixed only `ME-IW-855-E-008` from
`docs/contract_test_reports/mythic_edge_issue_wave_skill.md`. The fault was a
concrete implementation mismatch inside the existing lease/recovery contract:
ordinary checkpoint and terminal release could record a release after the
active five-minute lease had expired, bypassing the recovery-proof route.

`release_run` now applies the existing shared monotonic-time check and then,
before constructing or persisting a release event, rejects an unreleased
lease when the requested timestamp is later than `expires_at_utc`. The stable
error is `recovery_proof_required`. Because rejection precedes `_persist_event`,
both `run.json` and `events.jsonl` remain byte-identical. The comparison is
strictly later-than, so an otherwise-valid checkpoint or terminal release at
exactly the expiry timestamp remains accepted.

This D pass changed only:

- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- this implementation handoff

It did not change the contract, E report, monotonic-time helper, renewal,
transition, recovery-proof, segment, reviewed-package, retry, concurrency,
legacy Role Pool, or R0-bound behavior.

Focused regression coverage proves both release forms reject expiry plus one
second with `recovery_proof_required` and zero durable-byte mutation, then
accept the same otherwise-valid release at exact expiry.

Current D validation:

```text
expiry-boundary regression slice: 2 passed, 158 deselected
focused issue-wave suite: 160 passed
installer suite: 45 passed, 3 filesystem-capability skips
installer list: passed; four repo-owned skills listed
Ruff on helper and focused test: passed
agent docs: 55 checked, 0 errors, 0 warnings
protected-surface scan: 11 changed paths, 0 forbidden, 0 warnings
secret/private-marker scan: 11 changed paths, 0 forbidden, 0 warnings
Python compile and git diff --check: passed
legacy Role Pool: tree 950768b80b760a0e0dfe3040df023de20eadaf81,
38 tracked files, zero changed paths
official skill-creator validator: unavailable because its interpreter lacks PyYAML
```

Fresh independent Codex E must reproduce the checkpoint and terminal expiry
boundaries on the exact final bytes, confirm the rejection is pre-persistence,
and verify exact-expiry acceptance. No staging, commit, push, PR update,
installation, real Dispatch, G work, merge, deployment, cleanup, or issue
closure was performed by this correction.

### Pasteable Next-Thread Prompt

```text
Act as fresh independent Mythic Edge Codex E for issue #855 on branch
agent/mythic-edge-issue-wave-855. Invoke $mythic-edge-workflow and refresh the
live issue and PR, current repo authority, accepted ADR-0008/0012, contract
SHA-256 aa29efa936e08068358860c10f7f9e78040ea6e44312cc5a537080ca76bc2e2b,
the exact current implementation handoff and diff, and
docs/contract_test_reports/mythic_edge_issue_wave_skill.md. Review the exact
final package, with special focus on ME-IW-855-E-008. Independently prove that
ordinary checkpoint and terminal release at lease expiry plus one second fail
with recovery_proof_required before any run.json/events.jsonl mutation, while
an otherwise-valid release at exact expiry succeeds. Confirm no renewal,
transition, recovery-proof, segment, package-binding, retry, concurrency,
legacy Role Pool, or R0 behavior drift. Rerun the focused, installer, Ruff,
skill, docs, protected-surface, secret, compile, diff, and legacy checks.
Update only the E report. Route any concrete defect through D; otherwise hand
off to F. Do not stage, commit, push, update PR #856, install, perform a real
Dispatch, invoke G, merge, deploy, clean preserved state, or close #855.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/855"
  pr: "https://github.com/Tahjali11/Mythic-Edge/pull/856"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md#ME-IW-855-E-008"
  target_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main"
  branch: "agent/mythic-edge-issue-wave-855"
  finding_status:
    ME-IW-855-E-008: "fix_implemented_pending_fresh_e"
  validation:
    - "2 expiry-boundary regression tests passed"
    - "160 focused issue-wave tests passed"
    - "45 installer tests passed; 3 filesystem-capability skips"
    - "Ruff, docs, protected-surface, secret, compile, diff, and legacy identity checks passed"
    - "Official skill-creator validator could not start because PyYAML is unavailable"
  stop_conditions:
    - "fresh independent E required before F"
    - "legacy Role Pool or R0-bound byte change"
    - "staging, commit, push, PR update, installation, real Dispatch, G, merge, deployment, cleanup, or issue closure"
  next_recommended_role: "fresh independent Codex E"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "D"
  risk_tier: "high workflow risk"
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
    - "workflow coordination, reservations, leases, and recovery"
    - "Git branches, worktrees, commits, pushes, and draft PRs"
    - "legacy Role Pool and R0-bound files, explicitly forbidden"
  authority_conflicts_found: false
  authority_conflict_notes: "ME-IW-855-E-008 is a concrete implementation defect within the unchanged issue #855 contract."
  stop_conditions:
    - "contract or authority ambiguity requiring A or B"
    - "legacy Role Pool or R0-bound byte change"
    - "staging, commit, push, PR update, installation, real Dispatch, G, merge, deployment, cleanup, or issue closure"
```

## ME-IW-855-E-005 Monotonic Coordination-Time Codex D Addendum

Codex D addressed only `ME-IW-855-E-005` from
`docs/contract_test_reports/mythic_edge_issue_wave_skill.md`. The fault was a
narrow implementation mismatch: lane transitions rejected event timestamps
earlier than the current projection, while other mutating coordination
operations could append an earlier event and move durable time backward.

The helper now applies one shared pre-event monotonic-time validation to lane
transitions, lease renewal, checkpoint and terminal release, saved-segment
authorization, and expired-run recovery. A timestamp earlier than
`updated_at_utc` fails with `invalid_time` before an event is constructed or
persisted, leaving `events.jsonl` and `run.json` byte-identical. Equality
remains allowed by the monotonic boundary. Focused coverage proves equal-time
success for renewal, both release forms, and segment authorization; equal-time
recovery continues to fail for its independent and correct reason that the
lease is not expired.

This D pass changed only:

- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- this implementation handoff

Current D validation:

```text
new monotonic-time regression slice: 5 passed
focused issue-wave suite: 158 passed
installer suite: 45 passed, 3 filesystem symlink skips
Ruff on the changed helper and focused test: passed
agent docs: 55 checked, 0 errors, 0 warnings
protected-surface scan: 11 changed paths, 0 forbidden, 0 warnings
secret/private-marker scan: 11 changed paths, 0 forbidden, 0 warnings
AST compile and git diff --check: passed
legacy Role Pool: tree 950768b80b760a0e0dfe3040df023de20eadaf81,
38 tracked files, zero changed paths
official skill-creator validator: unavailable because its environment lacks PyYAML
```

Fresh independent Codex E must reproduce the five operation boundaries,
confirm zero mutation on every backward-time rejection, and verify equal-time
behavior against the unchanged contract. No staging, commit, push, PR update,
installation, real Dispatch, G work, merge, deployment, or issue closure was
performed or authorized by this correction.

### Pasteable Next-Thread Prompt

```text
Act as fresh Mythic Edge Codex E for issue #855 on branch
agent/mythic-edge-issue-wave-855. Invoke $mythic-edge-workflow and refresh the
live issue, current repo authority, accepted ADR-0008/0012, the contract,
implementation handoff, exact diff, and
docs/contract_test_reports/mythic_edge_issue_wave_skill.md. Independently
review ME-IW-855-E-005 on the exact current bytes. Reproduce backward-time
rejection with zero run.json/events.jsonl mutation for lease renewal,
checkpoint release, terminal release, segment authorization, and expired-run
recovery. Confirm equal timestamps remain accepted wherever the operation is
otherwise valid and that equal-time recovery still fails only because its
lease is not expired. Rerun the focused, installer, Ruff, skill, docs, safety,
compile, diff, and legacy-identity checks. Update only the review report and
route any concrete defect through D; otherwise hand off to F. Do not stage,
commit, push, update PR #856, install, perform a real Dispatch, merge, deploy,
or close issue #855.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/855"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md#ME-IW-855-E-005"
  target_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main"
  branch: "agent/mythic-edge-issue-wave-855"
  finding_status:
    ME-IW-855-E-005: "fix_implemented_pending_fresh_e"
  validation:
    - "5 monotonic coordination-time regression tests passed"
    - "158 focused issue-wave tests passed"
    - "45 installer tests passed; 3 filesystem symlink skips"
    - "Ruff passed on the changed helper and focused test"
    - "Agent docs, protected-surface, secret, AST compile, diff, and legacy identity checks passed"
    - "Official skill-creator validator could not start because PyYAML is unavailable"
  stop_conditions:
    - "contract or authority ambiguity requiring A or B"
    - "legacy Role Pool or R0-bound byte change"
    - "staging, commit, push, PR update, installation, real Dispatch, G, merge, deployment, or issue closure"
  next_recommended_role: "fresh independent Codex E"
```

## Checkpoint And Two-Wave Revision (Current Codex C)

This section supersedes earlier V1 implementation status for the current
uncommitted issue #855 package. Codex C implemented the B-owned contract at
SHA-256 `aa29efa936e08068358860c10f7f9e78040ea6e44312cc5a537080ca76bc2e2b`.

### Codex D correction after current independent E

Codex D fixed only `ME-IW-855-E-005`, reactivated `ME-IW-855-E-002`,
reactivated `ME-IW-855-E-004`, `ME-IW-855-E-006`, and `ME-IW-855-E-007` from
`docs/contract_test_reports/mythic_edge_issue_wave_skill.md`. No contract or
product-runtime behavior changed.

- Every lane transition now fails closed after the 60-second renewal deadline
  or five-minute lease expiry, before recording an event or projection change.
- First-worktree binding holds the shared admission lock and rejects equal or
  nested paths against every unreleased run's checkouts and worktrees.
- Public text rejects all lexical POSIX absolute paths and both UNC separator
  forms while preserving HTTPS and repository-relative references.
- Resume authorization validates a closed per-lane proof of exact repository
  heads and durable artifact identities, then binds its canonical SHA-256 into
  both the authorization event and immutable segment history.
- Inspect exposes continuation prompts and commands only at a released,
  checkpointed, exactly aligned boundary.

Focused adversarial coverage includes 60/61/300/301-second transition edges,
both cross-run nesting directions with zero loser mutation, POSIX/UNC
punctuation and Markdown forms with no echo, missing/tampered resume identities,
deterministic proof binding, and active/stopped/terminal/checkpointed Inspect
output. The focused suite passed `153 passed` using an isolated writable pytest
temporary root after the default Windows temporary root reproduced the known
permission failure. Fresh independent Codex E remains required.

The helper now exposes V2 invocation, run, event, event-request, and Inspect
schemas while preserving candidate-manifest and reviewed-package V1. Bare
Dispatch remains autonomous through F. Explicit A-A/A-B/A-C/A-E/A-F segments
stop at an inclusive checkpoint; saved segments begin only at the exact next
role. The state projection records execution status, current/next segments,
immutable segment history, reservations, five-minute leases, recovery proof,
and public-safe checkpoint prompts.

Admission now waits at most five seconds, permits two simultaneous disjoint
waves and six lanes, and rejects a third wave, shared repository, cross-run
scope, or cross-run path overlap before repository effects. Lease renewal is
bounded to 60 seconds. Checkpoint and terminal release preserve all work and
history. Expiry writes nothing and blocks reuse pending recovery proof.
Recovery accepts mechanically verified termination or explicit owner
confirmation only after all agents are stopped and preserved state is stable
and inactive. An interrupted running role becomes `unknown_agent_outcome` and
cannot resume. False resume revalidation detects manual drift and records no
segment authorization.

Current Codex C changed only these contract-owned implementation paths:

- `docs/codex_skills.md`
- `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
- `docs/codex_skills/mythic-edge-issue-wave/agents/openai.yaml`
- `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
- `docs/codex_skills/mythic-edge-issue-wave/references/state-schema.md`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_install_codex_skills.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- this implementation handoff

The B-owned contract is also modified in the worktree and was not edited by C.
No product runtime, parser, workbook, webhook, credential, deployment, legacy
Role Pool, or R0-bound path changed.

Current validation:

```text
focused issue-wave suite: 138 passed
new segment/concurrency/lease/recovery slice: 15 passed
installer suite: 45 passed, 3 filesystem symlink skips
installer list: passed; four repo-owned skills listed
Ruff on changed Python: passed
agent docs: 55 checked, 0 errors, 0 warnings
protected-surface scan: 11 PR paths, 0 forbidden, 0 warnings
secret/private-marker scan: 11 PR paths, 0 forbidden, 0 warnings
source-loaded Inspect parse: V2 output; git status unchanged; no state root before/after
git diff --check: passed
legacy Role Pool: tree 950768b80b760a0e0dfe3040df023de20eadaf81,
38 tracked files, zero changed paths
```

The official skill-creator validator remains unavailable because its Python
environment lacks PyYAML. No dependency was installed. Broad full-repository
tests and GitHub CI were not rerun in this bounded C pass; the focused,
synthetic, installer, lint, docs, safety, and identity checks above are current.

Next role is fresh independent Codex E. E must review the exact current
uncommitted package, especially V2 replay integrity, segment-end enforcement,
two-wave race behavior, expired-unreleased admission, manual-drift refusal,
checkpoint governance behavior, and the unchanged E/F package handshake.

### Pasteable Next-Thread Prompt

```text
Act as fresh Mythic Edge Codex E for issue #855 on branch
agent/mythic-edge-issue-wave-855. Invoke $mythic-edge-workflow and refresh the
live issue, draft PR #856, current repo authority, accepted ADR-0008/0012, and
docs/contracts/mythic_edge_issue_wave_skill.md at SHA-256
aa29efa936e08068358860c10f7f9e78040ea6e44312cc5a537080ca76bc2e2b.
Independently review the exact uncommitted checkpoint/two-wave package against
the contract. Reproduce the V2 grammar, exact checkpoint stops, aligned resume
authorization, two simultaneous three-lane disjoint waves, third/shared/scope/
path rejection, lease renewal/expiry, fail-closed recovery, unknown outcome,
manual-drift refusal, checkpoint governance, source-loaded Inspect zero-write,
installer, Ruff, docs, safety scans, and legacy Role Pool identity. Confirm the
candidate-manifest/reviewed-package V1 and E/F handshake remain unchanged.
Write only docs/contract_test_reports/mythic_edge_issue_wave_skill.md. Route a
concrete defect to D; otherwise hand off to F. Do not stage, commit, push,
update PR #856, install, perform a real Dispatch, merge, deploy, or close #855.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/855"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md"
  target_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md"
  risk_tier: "high workflow risk"
  base_branch: "main"
  target_branch: "main"
  branch: "agent/mythic-edge-issue-wave-855"
  validation:
    - "138 focused issue-wave tests passed"
    - "45 installer tests passed; 3 filesystem-only skips"
    - "Ruff, docs, protected-surface, secret, diff, Inspect-zero-write, and legacy identity checks passed"
  stop_conditions:
    - "concrete finding requiring D"
    - "contract or authority ambiguity requiring B or A"
    - "legacy Role Pool or R0-bound byte change"
    - "commit, push, PR update, installation, real Dispatch, G, merge, deployment, or issue closure"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "C"
  risk_tier: "high workflow risk"
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
    - "workflow coordination, reservations, leases, and recovery"
    - "Git branches, worktrees, commits, pushes, and draft PRs"
    - "legacy Role Pool and R0-bound files, explicitly forbidden"
  authority_conflicts_found: false
  authority_conflict_notes: "The explicit issue #855 override and exact B contract cover the implemented scope without requiring a service or cross-machine controller."
  stop_conditions:
    - "out-of-contract implementation"
    - "unproven recovery or uncertain agent outcome"
    - "real external write, installation, merge, or deployment"
```

## Codex D Corrective Addendum

Codex D addressed only the three blocking findings in
`docs/contract_test_reports/mythic_edge_issue_wave_skill.md`. The corrected
Codex B contract remains unchanged at SHA-256
`6b09ec4d24fc81e4954f155c6d3539b15d4b33160c1a4a835a4b7c320e4b024d`.

Finding disposition pending fresh independent E review:

| finding_id | D disposition | corrective evidence |
| --- | --- | --- |
| `ME-IW-855-E-001` | `fix_implemented_pending_e` | E now binds only the uncommitted reviewed package and E evidence; draft PR and checks stay null before F. The `f_complete` event must newly record the F-only identities, reassert the already-bound branch, and supply the positive draft PR; submission fields are immutable afterward, and check evidence is accepted only on its exact checks transition. |
| `ME-IW-855-E-002` | `fix_implemented_pending_e` | Pairwise equality and ancestor/descendant overlap are rejected across the state root, every target checkout, and every recorded or proposed worktree; replayed collisions fail integrity validation. |
| `ME-IW-855-E-003` | `fix_implemented_pending_e` | One state-root admission lock now covers duplicate-lane inspection through atomic publication; concurrent same-lane admission permits at most one run and stale or ownership-changed locks fail closed. |

D changed only:

- `docs/codex_skills/mythic-edge-issue-wave/SKILL.md`
- `docs/codex_skills/mythic-edge-issue-wave/references/controller-protocol.md`
- `docs/codex_skills/mythic-edge-issue-wave/references/state-schema.md`
- `docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py`
- `tests/test_mythic_edge_issue_wave_skill.py`
- this implementation handoff

Root verification after the D patch:

```text
focused issue-wave tests: 95 passed
installer tests: 45 passed, 3 filesystem symlink skips
Ruff: passed
agent docs: 55 checked, 0 errors, 0 warnings
D-path protected-surface scan: 6 paths, 0 forbidden, 0 warnings
D-path secret/private-marker scan: 6 paths, 0 forbidden, 0 warnings
git diff --check: passed
legacy Role Pool: tree 950768b80b760a0e0dfe3040df023de20eadaf81, 38 tracked files, unchanged
```

Current Codex D transition-scope follow-up:

```text
project .venv Python -m pytest tests/test_mythic_edge_issue_wave_skill.py -q
  -p no:cacheprovider --basetemp <isolated-temp>
107 passed in 25.21s

project .venv Python -m ruff check
  docs/codex_skills/mythic-edge-issue-wave/scripts/issue_wave_state.py
  tests/test_mythic_edge_issue_wave_skill.py
passed

git diff --check
passed
```

The added adversarial coverage rejects E/pre-F draft-PR and check claims;
missing, null, or mismatched F branch/PR evidence; and post-F branch/PR
mutation. It also proves that the four check transitions accept only their
contracted `running`, `passed`, `failed`, or `pending` status. The truthful
three-lane synthetic F/PR/check path remains passing with F explicitly
reasserting each lane's already-bound issue branch.

The complete 11-path secret scan also found two local absolute interpreter
paths in the initial E report. Those are review-artifact sanitization findings,
not D implementation findings. Fresh E must replace them with public-safe
symbolic command names while updating that report's finding lifecycle; F
remains blocked until the complete changed-path scan passes.

The earlier full-suite result remains `3233 passed, 4 skipped, 2 failed`; both
failures reproduce at unchanged `origin/main` and are not issue #855
regressions. Official skill-creator validation still cannot start because
PyYAML is unavailable; its source-equivalent structural checks passed. No
dependency was installed.

Next role: fresh independent Codex E. E must reproduce the three adversarial
boundaries, verify the successful synthetic path remains uncommitted and
unpushed through E, review the increased helper size against the lean-helper
contract, sanitize its own report, rerun the complete changed-path scans, and
issue a new exact verdict. No commit, push, PR, installation, real Dispatch,
G work, merge, or deployment is authorized by this addendum.

`PYTEST_ADDOPTS` directed the two commands' temporary roots outside the
repository and disabled its cache. Generated bytecode was removed after the
exact-command rerun.

Earlier default-environment limitations, superseded where current evidence is
recorded above:

- The skill-creator `quick_validate.py` could not start because this Python
  environment lacks `yaml`. Its complete source was inspected and the same
  delimiter, allowed-key, name, and description constraints were checked
  manually; those checks passed.
- The default interpreter lacked `ruff`; the current D follow-up used the
  project virtual environment and Ruff passed.
- The full repository pytest run stopped during collection with 39 import
  errors because optional application dependencies `fastapi` and `requests`
  are absent. Both focused suites above collect and pass.
- The repository-wide advisory private-marker scan reports established
  findings outside this change. The required changed-path scan passes.

## Still Unverified

- Independent Codex E contract review and contract-test report.
- Official skill-creator validation in a dependency-complete environment.
- Full repository tests in a dependency-complete environment.
- GitHub CI, commit, push, draft PR creation, and F/G lifecycle state.
- Installation and any real write-enabled Mythic Edge Dispatch, intentionally
  forbidden in this role.

## Reviewer Focus

Ask Codex E to pay special attention to:

- the root-Codex/helper authority boundary and absence of network, Git, or
  native-agent imports in the helper;
- strict transition coverage, one-event recovery, and unknown-outcome refusal;
- manifest scope-token evidence, anchor/WIP admission, and immutable resume
  permissions;
- source-loaded Inspect's zero-write proof and public path redaction;
- UI explicit-only routing and exact legacy Role Pool preservation; and
- whether the helper remains sufficiently lean for the V1 contract.

## Next Workflow Action

Next role: Codex E: Contract Test Reviewer.

### ME-IW-855-E-004 Codex D disposition

`fix_implemented_pending_e`: `_public_text` now detects drive-rooted Windows,
contracted Unix local-root, and UNC share paths regardless of punctuation or
Markdown adjacency. The detector remains lexical and local: it performs no
filesystem, network, Git, or path-resolution operation. Focused tests cover
start, whitespace, punctuation, Markdown, drive, Unix, and UNC forms across
eligibility, list, and check-summary validation; errors do not echo the input.
Safe repository-relative, symbolic, and HTTPS text remains accepted.

This correction changed only the helper, focused test, and this handoff. Fresh
independent Codex E must confirm E-004 on the final bytes before F.

Pasteable prompt:

```text
Act as fresh Mythic Edge Codex E for issue #855 in the isolated issue
worktree on branch agent/mythic-edge-issue-wave-855. Invoke
$mythic-edge-workflow and read current repo authority, issue #855,
docs/contracts/mythic_edge_issue_wave_skill.md, the exact diff,
docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md, and
the focused tests. Independently review only the contract allowlist. Verify
the root-Codex/helper authority boundary, exact invocation and state schemas,
all transitions and recovery behavior, source-loaded Inspect zero-write
evidence, synthetic disposable Dispatch boundaries, UI explicit-only routing,
and exact preservation of the legacy Role Pool tree and R0-bound files. Run
all feasible required validation, classify environment-only gaps, and write
only docs/contract_test_reports/mythic_edge_issue_wave_skill.md. Route any
concrete finding through Codex D then fresh E. Do not commit, push, open or
update a PR, install the skill, create GitHub writes, perform a real Dispatch,
or advance to G.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/855"
  tracker: "N/A"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/mythic_edge_issue_wave_skill_comparison.md"
  target_artifact: "docs/contract_test_reports/mythic_edge_issue_wave_skill.md"
  risk_tier: "medium"
  base_branch: "main"
  target_branch: "main"
  branch: "agent/mythic-edge-issue-wave-855"
  validation:
    - "focused skill tests: 54 passed"
    - "installer tests: 45 passed, 3 environment skips"
    - "docs, protected-surface, changed-path private-marker, compile, and diff checks passed"
    - "source-loaded live Inspect selected zero lanes and proved zero writes"
    - "legacy Role Pool tree 950768b80b760a0e0dfe3040df023de20eadaf81 preserved with 38 files"
  stop_conditions:
    - "contract or authority ambiguity"
    - "any required change outside the contracted file list"
    - "legacy Role Pool or R0-bound byte change"
    - "concrete review finding requiring Codex D"
    - "real Dispatch, installation, GitHub write, merge, or deployment"
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "C"
  risk_tier: "medium"
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
    - "workflow coordination and native subagent dispatch"
    - "Git branches, worktrees, commits, pushes, and draft pull requests"
    - "local resumable run state"
    - "legacy Role Pool and R0-bound artifacts"
  authority_conflicts_found: false
  authority_conflict_notes: "No ambiguity required a change outside the B contract."
  stop_conditions:
    - "contract or authority ambiguity"
    - "out-of-scope or R0-bound change"
    - "real external write or Dispatch"
```
