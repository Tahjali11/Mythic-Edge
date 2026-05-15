# Agent Constitution V1 vs V2 Comparison Report

Date: 2026-05-13

Reviewer role: Codex A / Thinker-style synthesis review

## Source Versions Compared

V1 source:

- `origin/main:docs/agent_constitution.md`
- Last V1-related commit on `main`: `7cecbde` / PR #4

V2 source:

- `HEAD:docs/agent_constitution.md`
- `HEAD:docs/agent_rules.yml`
- V2 merge commit: `9ca3f7978b62bc24a3838675f30bcf22f0a4a01e`
- PR: https://github.com/Tahjali11/Mythic-Edge/pull/19
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/18

## Verdict

V2 is a material improvement over V1.

The improvement is strongest in operational reliability, Codex readability,
GitHub lifecycle clarity, tracker hygiene, and merge/closure safety. V2
preserves the V1 sacred rules and adds a machine-readable rule index,
`docs/agent_rules.yml`, without changing parser/runtime/workbook/App Script
behavior.

Recommendation:

- Treat V2 as the active constitution package.
- Archive V1 for posterity before the final integration branch-to-main step.
- Keep a stable active filename, `docs/agent_constitution.md`, for Codex
  discoverability.
- Add adoption metadata to the active constitution rather than renaming it away
  from the known path.
- Keep `docs/agent_rules.yml` as the terse Codex-optimized source.
- Keep V2 draft files only under `docs/archive/agent_constitution_v2_drafts/`
  with explicit no-authority labeling.

## Validation Evidence

Fresh checks run during this comparison:

```bash
git diff --check origin/main..HEAD
```

Result: passed with no output.

```bash
ruby -e 'require "yaml"; YAML.load_file("docs/agent_rules.yml"); YAML.load_file(".github/ISSUE_TEMPLATE/module_workflow.yml"); puts "yaml ok"'
```

Result: `yaml ok`.

```bash
ruby -e 'require "yaml"; data=YAML.load_file("docs/agent_rules.yml"); required=%w[version status authority_order source_priority conflict_triage sacred_rules protected_surfaces roles routing risk_tiers issue_lifecycle pr_lifecycle tracker_hygiene branch_policy validation_gates prompt_schema handoff_schema current_status_schema archive_policy]; missing=required.reject{|k| data.key?(k)}; roles=%w[A B C D E F G].reject{|k| data.fetch("roles",{}).key?(k)}; abort("missing keys: #{missing.join(",")}") unless missing.empty?; abort("missing roles: #{roles.join(",")}") unless roles.empty?; puts "agent rules shape ok"'
```

Result: `agent rules shape ok`.

```bash
git diff --name-only 9ca3f7978b62bc24a3838675f30bcf22f0a4a01e^..9ca3f7978b62bc24a3838675f30bcf22f0a4a01e -- src tests tools data main.py live_print_filtered_v11_match_summary.py tools/google_apps_script/Code.gs
```

Result: passed with no output.

```bash
python3 -m pytest -q
```

Result: `396 passed in 0.92s`.

```bash
python3 -m ruff check src tests
```

Result: `All checks passed!`.

## Comparison Summary

| Area | V1 | V2 | Assessment |
| --- | --- | --- | --- |
| Authority order | Present, mostly prose | Expanded, includes `docs/agent_rules.yml`, issue/contract/handoff ordering, and draft no-authority rule | Improved |
| Machine readability | Low to moderate | High: `docs/agent_rules.yml` with stable rule areas and role IDs | Improved |
| Truth ownership | Strong | Stronger: explicitly includes parser-state, final reconciliation, parser-owned classification, webhook transport, and AI boundary | Improved |
| Sacred safety rules | Strong | Preserved and encoded in YAML | Improved |
| Role model | A-F | A-G, with submitter/deployer split | Improved |
| PR lifecycle | Basic submitter guidance | Draft/ready/merge gates, `Closes` vs `Refs`, post-merge duties | Improved |
| Issue lifecycle | Basic issue workflow | Tracker/module/bug/planning/constitution closure rules | Improved |
| Tracker hygiene | Implied | Explicit update triggers and required fields | Improved |
| Current status summaries | Not formalized | Machine-readable `repo_status` schema | Improved |
| Conflict resolution | Authority order only | Dedicated conflict triage order | Improved |
| Prompt shape | Handoff block only | Full prompt contract plus handoff schema | Improved |
| Archive policy | Not explicit | Draft archive policy exists | Improved |
| Token efficiency | Single long prose doc | Terse YAML index plus modular docs | Improved, with maintenance caveat |
| Human readability | Good | Still good, slightly more operational | Maintained |

## Sacred Rule Preservation

V2 preserves the V1 non-negotiables:

- No secrets, webhook URLs, API keys, local MTGA logs, failed posts, runtime
  status files, generated card data, or raw workbook exports.
- Parser-owned truth must not move into workbook formulas, dashboard logic,
  Apps Script transport, webhook transport, or AI interpretation.
- Webhook payload shape, workbook schema, Apps Script assumptions, match
  identity, game identity, deduplication, winner fields, play/draw fields,
  mulligan counts, and final reconciliation remain protected high-risk
  surfaces.
- High-risk changes still require problem representation, contract,
  implementation against contract, review/contract-test, and validation
  evidence.
- Agents still may not silently expand scope.
- Agents still may not claim validation without evidence.
- Agents still may not delete archive/raw/debug/helper/summary/observability or
  generated-data layers without approval and rollback path.
- Module audit work still must not target `main` without explicit approval.

No V1 sacred rule was found weakened in V2.

## Material Improvements

### 1. Codex Can Read Less And Decide Faster

V1 required Codex to read a prose constitution and infer operational rules.
V2 adds `docs/agent_rules.yml`, which gives Codex a fast index for:

- authority order
- source priority
- sacred rules
- protected surfaces
- roles A-G
- routing
- risk tiers
- issue lifecycle
- PR lifecycle
- tracker hygiene
- validation gates
- prompt and handoff schemas
- archive policy

This directly addresses token-truncation risk.

### 2. Submitter And Deployer Are Correctly Split

V1 made F responsible for PR submission but did not clearly define who merges,
closes issues, and updates trackers. V2 adds Codex G: Integration Deployer.

This is a significant reliability improvement because it separates:

- preparing a PR
- merging a PR
- closing issues
- updating trackers
- confirming completion evidence

That matches the workflow that emerged in real use.

### 3. GitHub Lifecycle Is Now Governed

V1 said to use GitHub issues and PRs. V2 defines when issues can close, when
trackers stay open, when PRs can be marked ready or merged, and what Codex must
record after merge.

This reduces the exact confusion seen during issue #7, #14, #16, #18, and
tracker #5 work.

### 4. V2 Adds Better Drift Protection

V1 had workbook/deployment drift rules. V2 expands them with:

- protected surface bundles
- parser evidence and uncertainty expectations
- explicit status summaries
- source priority and conflict triage

This is a better fit for a volatile `Player.log` parser project.

### 5. Draft Confusion Is Reduced

V2 archives role-labeled v2 drafts under:

```text
docs/archive/agent_constitution_v2_drafts/
```

The active constitution explicitly says archived drafts have no authority
unless a prompt names them. This is enough to prevent ordinary Codex confusion.

## Remaining Risks

### Risk 1: No Dedicated V1 Archive Exists Yet

V1 is recoverable from git history, but it is not yet preserved as a
human-visible archive file. If the user wants posterity without needing `git
show`, archive V1 explicitly.

Recommended path:

```text
docs/archive/agent_constitution_v1_2026-05-11.md
```

### Risk 2: Active Constitution Has No Adoption Metadata Block

`docs/agent_constitution.md` is the correct stable active filename, but it
should include a small metadata block near the top:

```yaml
version: 2
status: active
adopted_on: 2026-05-13
adoption_pr: "#19"
adoption_commit: "9ca3f7978b62bc24a3838675f30bcf22f0a4a01e"
supersedes: "V1 constitution from PR #4 / 7cecbde"
```

Recommendation: add metadata without renaming the active file.

### Risk 3: Archived V2 Drafts Lack A README

The current active constitution says archived drafts have no authority, but the
archive folder itself has no local README. A future thread browsing the archive
would benefit from one.

Recommended path:

```text
docs/archive/agent_constitution_v2_drafts/README.md
```

### Risk 4: `docs/agent_constitution.md` And `docs/agent_rules.yml` Can Drift

V2 intentionally has both human-readable and machine-readable sources. This is
worth it, but it creates maintenance risk.

Mitigation already present:

- V2 defines conflict triage.
- V2 says `docs/agent_rules.yml` is the terse rule index.
- V2 says `docs/agent_constitution.md` is human-readable.

Recommended future improvement:

- Add a tiny validation script later that checks required top-level YAML keys
  and roles A-G.

## Recommended Cleanup Plan

Do not delete active V2 files. Do not rename `docs/agent_constitution.md`.

Recommended next cleanup issue:

```text
[workflow] Finalize active constitution archive metadata
```

Scope:

- add `docs/archive/agent_constitution_v1_2026-05-11.md` from
  `origin/main:docs/agent_constitution.md`
- add adoption metadata to `docs/agent_constitution.md`
- add `docs/archive/agent_constitution_v2_drafts/README.md`
- verify issue #1 and issue #18 remain closed
- verify no unarchived v2 draft files remain outside `docs/archive/`

Out of scope:

- deleting role-labeled V2 draft history unless the user explicitly approves
- changing parser/runtime/workbook/App Script behavior
- targeting `main` without explicit approval

## Final Recommendation

V2 should replace V1 as the active constitution.

However, the safest file strategy is:

- keep active constitution at `docs/agent_constitution.md`
- add version/adoption metadata inside that file
- archive V1 under a dated archival filename
- keep role-labeled V2 drafts archived or delete them only with explicit user
  approval

This gives Codex a stable active path while preserving the project history the
user wants.
