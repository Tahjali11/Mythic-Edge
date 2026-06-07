# Private Local V1 Private Artifact Scanner And Env Ignore Posture Contract

## Module

`private_local_v1_private_artifact_scanner_env_ignore_posture`

Plain English: this contract defines how Mythic Edge should triage
repo-wide secret/private-marker scanner findings and `.env*` ignore behavior
before claiming private-local-v1 private artifact safety.

This contract does not weaken scanner coverage and does not implement fixes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/252
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source baseline issue: https://github.com/Tahjali11/Mythic-Edge/issues/249
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- `docs/local_artifacts_manifest.json`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- `tools/check_local_environment.py`
- `tools/select_validation.py`
- `.gitignore`
- `.env.example`
- `pyproject.toml`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_local_environment.py`

## Owning Layer

Primary owner: Quality / Governance.

Supporting area: Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

## Truth Owner

The secret/private-marker scanner and local artifact manifest own safety
classification for repo-scanning and local artifact posture.

They do not own:

- parser truth;
- analytics truth;
- workbook truth;
- local app runtime truth;
- deployment readiness;
- AI truth;
- credential values.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
tracked repo files + scanner patterns + local artifact manifest
  -> redacted scanner findings
  -> triage categories
  -> issue #252 report / narrow scanner or ignore-policy fixes
```

Forbidden reverse flow:

- scanner triage must not authorize committing secrets or private artifacts;
- scanner triage must not change parser, analytics, workbook, transport, or AI
  behavior;
- scanner warning reduction must not remove useful detection coverage without
  explicit policy rationale.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`

Likely future implementation or review artifacts:

- `docs/implementation_handoffs/private_local_v1_private_artifact_scanner_env_ignore_posture_comparison.md`
- `docs/contract_test_reports/private_local_v1_private_artifact_scanner_env_ignore_posture.md`

Possible future implementation files, only if Codex C finds a concrete
contract gap:

- `.gitignore`
- `docs/local_artifacts_manifest.json`
- `tools/check_secret_patterns.py`
- `tools/check_local_environment.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_local_environment.py`

## Current Evidence Snapshot

Codex B inspected the current branch on 2026-06-03.

Current changed-path scanner status:

```text
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
mode: changed-files
scanned_paths: 0
forbidden: 0
warnings: 0
result: passed
```

Current all-repo advisory scanner status:

```text
py tools\check_secret_patterns.py --all
mode: all-repo-advisory
scanned_paths: 746
skipped_paths: 0
forbidden: 540
warnings: 898
result: failed
exit_code: 0
```

All-repo category counts observed:

| Category | Count |
| --- | ---: |
| `raw_player_log_content` | 335 |
| `runtime_status_payload` | 85 |
| `private_local_path` | 57 |
| `generated_data_dump` | 38 |
| `failed_post_payload` | 9 |
| `credential_value` | 10 |
| `live_webhook_url` | 3 |
| `workbook_export_marker` | 3 |
| `artifact_path_reference` | 632 |
| `sanitized_fixture_marker` | 174 |
| `ambiguous_private_marker` | 80 |
| `placeholder_secret_reference` | 9 |
| `decode_replacement_used` | 3 |

Current `.env*` posture:

- `.env.example` is tracked.
- Exact tracked `.env.example` is treated by
  `docs/local_artifacts_manifest.json` as repo-owned template source.
- Real `.env*` variants are classified as `Secret And Credential Surfaces`
  with `git_policy = never_commit`.
- `git check-ignore -v .env .env.local .env.example` returned no ignored
  entries in the current branch.
- `py tools\check_local_environment.py --profile clean_clone --format json`
  returned status `warning`, with `env_files` observed as
  `missing_not_ignored`.
- `py tools\check_local_environment.py --profile clean_install_transition_audit
  --format json` returned status `warning`, with `env_files` observed as
  `missing_not_ignored`.

Interpretation:

- Path-scoped scanner behavior is currently clean for this branch.
- All-repo scanner debt is real release-readiness debt until triaged.
- Exact tracked `.env.example` is allowed as a template, but broad `.env*`
  ignore coverage remains uncertain and should be resolved or explicitly
  documented.

## Private-Local-V1 Scanner Posture

Private-local-v1 readiness requires:

1. path-scoped scans for changed files continue to fail on forbidden findings;
2. all-repo scans may remain advisory, but every all-repo forbidden finding
   must be classified before release readiness is claimed;
3. warnings may remain when they are expected policy text, placeholders,
   sanitized fixtures, or known non-content skip warnings;
4. no unclassified live secret, live webhook URL, raw Player.log payload,
   private local path, workbook export marker, runtime payload, failed-post
   payload, generated data dump, or private JSONL payload may be accepted as
   release-ready;
5. `.env*` ignore behavior must protect real local env files while preserving
   exact tracked `.env.example` as a public blank/placeholder template.

This issue should prove safety posture, not require zero scanner output.

## Public Interface

Commands and surfaces governed by this contract:

```powershell
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile clean_install_transition_audit --format json
git check-ignore -v .env .env.local .env.production .env.example
```

The scanner may print redacted excerpts. Future #252 reports should summarize
counts and categories rather than copy every scanner line.

## Inputs

Allowed inputs:

- tracked repo file paths from `git ls-files`;
- changed repo file paths from `git diff --name-only`;
- path list from `--paths-from-stdin`;
- scanner regex and category definitions in `tools/check_secret_patterns.py`;
- local artifact policy in `docs/local_artifacts_manifest.json`;
- `.gitignore` ignore rules;
- tracked `.env.example` template status;
- Git metadata needed to determine whether `.env.example` is tracked,
  untracked, or modified.

Forbidden inputs:

- secret values;
- raw Player.log contents;
- private JSONL payloads;
- raw SQLite database contents;
- failed-post payload contents;
- runtime status payload contents;
- workbook export contents;
- API keys, OAuth tokens, webhook URLs, spreadsheet IDs, or LLM provider keys
  as plain text.

## Outputs

Required future report output:

- scanner command status;
- all-repo category counts;
- path-scoped scan status;
- `.env*` ignore status;
- exact tracked `.env.example` verdict;
- categorized finding families;
- concrete fix list;
- expected-warning list;
- false-positive list, if any;
- release-readiness verdict for private-local-v1 private artifact safety.

Forbidden report output:

- raw secret values;
- raw webhook URLs;
- raw spreadsheet IDs;
- raw local user paths;
- raw Player.log lines;
- raw JSONL payloads;
- raw SQLite data;
- private file contents;
- unredacted environment variable values.

## All-Repo Triage Categories

Future #252 triage must classify each finding family into exactly one primary
category.

### `expected_policy_or_contract_text`

Policy docs, contracts, templates, handoffs, and reports may discuss protected
surfaces, private artifacts, example paths, or placeholder secret concepts.

Allowed only when:

- the scanner output is warning-level; or
- a forbidden category appears only because policy text lacks placeholder
  context and the report explains the policy gap.

Preferred fix:

- add explicit placeholder/redacted wording to policy text rather than
  suppressing the scanner.

### `expected_synthetic_or_sanitized_fixture`

Tests and fixtures may contain synthetic markers that intentionally exercise
scanner behavior.

Allowed only when:

- fixture text is synthetic/sanitized;
- the test asserts redaction;
- no real private value is present;
- scanner category is warning-level or documented as a test-only expected
  forbidden sample.

Preferred fix:

- move dangerous-looking literals into split strings or synthetic builders when
  the scanner is supposed to detect scanner behavior without polluting all-repo
  release posture.

### `expected_placeholder_or_example`

Placeholder API keys, webhook labels, or local paths are allowed when they are
clearly blank, redacted, fake, placeholder, sample, synthetic, or configured as
examples.

Allowed only when:

- no real-looking value appears;
- output remains redacted;
- the value is needed for docs, tests, or template clarity.

### `scanner_false_positive`

A false positive is a finding where the scanner category is technically
matched, but the repo text is safe and not usefully made safer by rewriting.

False positives must include:

- path;
- category;
- reason the finding is not secret/private risk;
- why rewriting would reduce clarity or scanner value.

False positives must not be suppressed globally without tests.

### `concrete_fix_required`

Use this category when the finding is:

- a non-placeholder credential-looking value;
- a live webhook-looking URL;
- raw Player.log-style content outside sanitized fixture context;
- a private local user path outside placeholder/policy context;
- runtime, failed-post, generated data, workbook export, or SQLite-like payload
  content outside sanctioned synthetic tests;
- any `.env*` file other than exact tracked `.env.example`;
- any modified `.env.example` containing non-placeholder values;
- any scanner output that prints a raw private value.

Concrete fixes should prefer:

- remove the value;
- replace with placeholder/redacted text;
- move local/private data outside the repo;
- update `.gitignore` or local artifact policy;
- add focused scanner tests only when scanner behavior changes.

## `.env*` Ignore And Allow Policy

### Real local env files

These must never be committed:

- `.env`
- `.env.local`
- `.env.production`
- `.env.development`
- `.env.test`
- any other `.env.*` file unless a future contract explicitly authorizes a
  tracked example template.

Expected posture:

- missing real env files: ok or info;
- present ignored real env files: warning or info, depending profile;
- present not ignored real env files: blocked;
- tracked real env files: forbidden unless they are exact tracked
  `.env.example` and pass template policy.

### Exact tracked `.env.example`

Exact tracked `.env.example` is allowed as repo-owned source when it is a
blank/placeholder template.

Allowed content shape:

- blank assignments;
- commented example assignments;
- placeholder values such as `<you>`, `<placeholder>`, or redacted labels;
- instructions saying not to commit real secrets or personal paths.

Forbidden content shape:

- real API keys;
- live webhook URLs;
- spreadsheet IDs;
- OAuth tokens;
- passwords;
- LLM provider keys;
- raw private local paths without placeholder context.

Policy recommendation:

- keep `.env.example` tracked;
- ignore real `.env*` variants through `.gitignore`;
- unignore exact `.env.example` if broad `.env*` ignore rules are added.

Recommended `.gitignore` shape for future Codex C evaluation:

```text
.env
.env.*
!.env.example
```

Codex C must verify this does not accidentally hide other intended source
files and does not stage real local env files.

## Scanner Output Privacy Requirements

The scanner and #252 reports must:

- redact credential values;
- redact live webhook URLs;
- redact local user path names;
- redact raw Player.log-like content;
- redact runtime/failed-post/generated-data payload content;
- limit excerpts to safe redacted summaries;
- report category counts and paths without dumping private contents.

The scanner and #252 reports must not:

- print raw secret values;
- print raw local paths;
- print private JSONL payloads;
- print raw SQLite contents;
- print raw Player.log lines;
- print local app state contents.

## Path-Scoped Scanner Preservation Requirements

Normal workflow scans must preserve current strict behavior:

- changed-path scan exits nonzero for forbidden findings;
- changed-path scan exits zero for warnings only;
- path-scoped scan can be used for reviewed file sets;
- all-repo `--all` mode remains advisory unless a later release-readiness
  contract explicitly makes it a gate;
- scanner tests must continue proving redaction of credentials, webhooks,
  local paths, and raw-log markers.

Do not convert path-scoped forbidden findings into warnings just to pass #252.

## Error Behavior

If scanner commands fail:

- record the command, exit code, and high-level reason;
- do not treat missing scanner evidence as passed;
- do not paste raw secret/private output into reports;
- route to Codex C or D if the scanner itself crashes or prints unsafe
  content.

If all-repo findings cannot be fully classified:

- keep #252 open;
- report the unknown categories and path families;
- do not claim private-local-v1 release-grade private artifact safety.

If `.env*` ignore behavior is ambiguous:

- keep the private-local-v1 posture at warning or blocked, depending evidence;
- prefer a narrow `.gitignore`/manifest/test fix over accepting ambiguity.

## Side Effects

Codex B side effects:

- create this contract only.

Future Codex C side effects, if needed:

- create an implementation handoff;
- update `.gitignore` for real `.env*` ignore coverage;
- update local artifact manifest language if needed;
- update scanner/local-environment tests if behavior changes;
- create or update a contract-test report.

Forbidden side effects:

- reading private local artifact contents;
- committing local env files;
- committing SQLite databases or sidecars;
- committing raw logs, private JSONL artifacts, runtime files, failed posts, or
  workbook exports;
- changing parser, analytics, workbook, transport, local app runtime, AI, or
  production behavior;
- rotating, creating, or modifying credentials.

## Dependency Order

Recommended implementation/review order:

1. Re-run current scanner and local-environment evidence.
2. Generate a summarized all-repo finding matrix by category and path family.
3. Classify findings into the triage categories in this contract.
4. Decide whether `.gitignore` needs the narrow `.env*` ignore fix.
5. If `.gitignore` changes, update or add focused tests proving exact tracked
   `.env.example` remains allowed and real env variants remain blocked/ignored.
6. Produce the #252 report with no raw private values.
7. Run focused scanner/local-environment tests.
8. Run path-scoped protected-surface and secret/private-marker scans over the
   touched #252 files.

## Compatibility

Preserve:

- exact tracked `.env.example` as allowed template source;
- path-scoped secret/private-marker scanner strictness;
- all-repo scanner as advisory/report-only by default;
- local environment checker no-content-read behavior;
- current private-local-v1 install mechanics from #253;
- existing developer app and parser behavior.

## Tests Required

Minimum tests if only docs/report artifacts change:

```powershell
git diff --check
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
```

Required tests if `.gitignore`, manifest, scanner, or local-environment tooling
changes:

```powershell
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile clean_install_transition_audit --format json
git check-ignore -v .env .env.local .env.production .env.example
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
```

Validation reports must summarize all-repo scanner output by count/category, not
paste every finding line.

## Acceptance Criteria

- The #252 report classifies current all-repo scanner findings by category and
  path family.
- No unclassified all-repo forbidden finding remains when claiming
  private-local-v1 private artifact readiness.
- Exact tracked `.env.example` remains allowed only as a blank/placeholder
  template.
- Real `.env*` variants are ignored or blocked and never tracked.
- Path-scoped scanner strictness is preserved.
- Scanner/local-environment output does not print secret values, raw local
  paths, raw logs, private JSONL payloads, SQLite contents, or local artifact
  contents.
- Any suppression or downgrade has explicit policy rationale and tests.
- Any concrete fix is narrow, reviewed, and validated.
- No parser, analytics, workbook, transport, production, local app runtime, or
  AI behavior changes occur.

## Open Questions / Contract Risks

- The current all-repo scanner result is large. The first #252 implementation
  may need a generated summary helper or temporary script, but any helper must
  avoid writing private excerpts.
- Some all-repo forbidden findings may be intentional scanner tests. Codex C
  should decide whether to rewrite those as split synthetic strings, classify
  them as test-only expected findings, or leave them as documented debt.
- `.gitignore` currently does not ignore `.env*`. The likely fix is narrow, but
  it still touches local artifact safety policy and needs focused tests.
- All-repo zero findings are not required, but all-repo unclassified forbidden
  findings are not acceptable for private-local-v1 private artifact readiness.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #252.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/252

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source contract:
docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md

Current intended branch:
codex/analytics-foundation

Goal:
Compare the current repo against the #252 contract, implement the smallest
private-local-v1 scanner/env-ignore posture package needed, and produce the
implementation handoff.

Likely target artifact:
docs/implementation_handoffs/private_local_v1_private_artifact_scanner_env_ignore_posture_comparison.md

Likely later review/report artifact:
docs/contract_test_reports/private_local_v1_private_artifact_scanner_env_ignore_posture.md

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- issue #252
- issue #136
- issue #249
- docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md
- docs/contracts/engineering_maturity_index_open_framework.md
- docs/contract_test_reports/engineering_maturity_baseline.md
- docs/local_artifacts_manifest.json
- tools/check_secret_patterns.py
- tools/check_local_environment.py
- .gitignore
- .env.example
- tests/test_check_secret_patterns.py
- tests/test_check_local_environment.py
- tests/test_check_protected_surfaces.py

Implementation tasks:
1. Re-run the current scanner/local-environment evidence.
2. Summarize all-repo scanner findings by category and path family without
   printing raw private values.
3. Classify findings using the contract categories:
   expected_policy_or_contract_text,
   expected_synthetic_or_sanitized_fixture,
   expected_placeholder_or_example,
   scanner_false_positive,
   concrete_fix_required.
4. Evaluate the `.env*` ignore gap.
5. If safe and contract-aligned, implement the narrow `.gitignore` posture:
   ignore real `.env*` variants while preserving exact tracked `.env.example`.
6. Add or update focused tests only if scanner/local-environment behavior
   changes.
7. Produce the implementation handoff and route to Codex E.

Important boundaries:
- Do not weaken scanner coverage casually.
- Do not suppress findings without explicit policy rationale.
- Do not print or commit secret values, raw logs, private JSONL payloads,
  SQLite files, runtime files, failed posts, workbook exports, app-data files,
  local env files, or local-only artifacts.
- Do not change parser behavior, parser state reconciliation, analytics schema
  or migrations, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets behavior, production behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, credential policy, or environment variable contracts.
- Do not target main.
- Do not close #249 or tracker #136.

Validation:
- py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
- py tools\check_local_environment.py --profile clean_clone --format json
- py tools\check_local_environment.py --profile clean_install_transition_audit --format json
- git check-ignore -v .env .env.local .env.production .env.example
- py tools\check_secret_patterns.py --all
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
- git diff --check
- py tools\check_agent_docs.py
- py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation

Output:
- role performed
- contract compared
- files changed
- all-repo scanner summary
- `.env*` policy result
- implementation summary
- validation run
- protected-surface status
- secret/private-marker status
- remaining risk
- next recommended role: Codex E
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/252"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/252"
  target_artifact: "docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch"
    - "gh issue view 252 --comments"
    - "gh issue view 136 --comments"
    - "gh issue view 249 --comments"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, 46 checked, 0 errors, 0 warnings"
    - "path-scoped protected-surface scan over this contract -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over this contract -> warning, forbidden 0, warnings 1 on scanner category literal"
    - "py tools\\check_secret_patterns.py --all -> advisory result failed, exit 0, forbidden 540, warnings 898"
    - "py tools\\check_secret_patterns.py --base origin/codex/analytics-foundation -> passed, forbidden 0, warnings 0"
    - "git check-ignore -v .env .env.local .env.example -> no ignored entries"
    - "py tools\\check_local_environment.py --profile clean_clone --format json -> warning, blocked 0"
    - "py tools\\check_local_environment.py --profile clean_install_transition_audit --format json -> warning, blocked 0"
  stop_conditions:
    - "Do not print or commit secret/private values or local artifacts."
    - "Do not weaken scanner coverage without explicit policy rationale and tests."
    - "Do not change parser, analytics, workbook, transport, production, AI, or credential behavior."
```
