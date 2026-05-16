# Repo-Wide Secret And Private-Marker Scanner Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/84

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Source artifact:

- `docs/contract_test_reports/repo_wide_hardening_baseline.md`

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Related hardening contracts and workflow surfaces:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `.gitignore`
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- `tests/fixtures/`

Branch target: `codex/repo-wide-hardening-run`

This contract defines a deterministic content scanner for secret and private
markers in repository text files. It is a contract artifact only. It does not
implement the scanner, add tests, change CI, change parser/runtime behavior,
change workbook or webhook shape, change Apps Script behavior, add fixtures,
commit secrets, or mark tracker #82 complete.

## Module

Repo-wide hardening secret and private-marker scanner.

Likely implementation artifact:

- `tools/check_secret_patterns.py`

Likely tests:

- `tests/test_check_secret_patterns.py`

The scanner should inspect text content in changed files and report risky
markers that path-only classification can miss:

- live webhook or Apps Script deployment URLs
- API keys, tokens, OAuth values, passwords, auth headers, and credential-like
  assignments
- private local paths, especially MTGA `Player.log` paths under user profiles
- raw Player.log markers outside approved sanitized fixture contexts
- failed-post, runtime status, runtime log, generated data, and workbook export
  artifact markers
- ambiguous private markers that should be warning-only until the policy is
  made stricter

Plain English: the existing protected-surface gate asks "is this path safe to
commit?" This scanner asks "does this changed text look like it contains
private or sensitive material, even though the path itself looks allowed?"

## Owning Layer

Repository coordination and code-hardening workflow.

Truth boundary:

- The scanner owns deterministic repository content-safety classification and
  report formatting.
- The scanner does not own parser truth, parser event interpretation,
  workbook schema, webhook payload shape, Apps Script behavior, match identity,
  game identity, deduplication, runtime status truth, fixture provenance truth,
  or final reconciliation.
- `tools/check_protected_surfaces.py` owns path-based forbidden/protected
  classification. This scanner complements it and must not replace it.
- Module contracts, issue scope, fixture policy, PR drift budgets, and reviews
  own whether a warning is authorized or requires follow-up.
- The golden fixture policy owns committed fixture redaction and provenance
  requirements. The scanner is an enforcement aid, not a fixture sanitizer.
- Workbook formulas, dashboard logic, Apps Script, webhook transport, output
  transport, and AI-generated interpretation must not become sources of
  scanner policy or parser-owned truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/repo_wide_secret_private_marker_scanner.md`

Expected future implementation files owned by this contract:

- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md`
- `docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md`

Related files referenced but not owned by this contract:

- `docs/contract_test_reports/repo_wide_hardening_baseline.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- `.gitignore`
- `.github/workflows/repo-checks.yml`
- `.github/pull_request_template.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_independent_test_authoring_policy.md`
- `docs/contracts/code_hardening_drift_detector_baseline_policy.md`
- `tests/fixtures/`

## Observed Current Behavior

Observed on `codex/repo-wide-hardening-run` during this contract pass:

- `tools/check_secret_patterns.py` does not exist.
- `tests/test_check_secret_patterns.py` does not exist.
- The baseline report records a clean hardening starting point:
  - `HEAD`: `3da1242`
  - `HEAD...origin/main`: `0 0`
  - `python3 -m pytest -q tests`: `670 passed`
  - `python3 -m ruff check src tests tools`: all checks passed
  - `python3 -m pyright`: `0 errors, 0 warnings, 0 informations`
  - `python3 tools/check_protected_surfaces.py --base origin/main`: passed
  - `git diff --check`: passed
- The protected-surface gate already blocks forbidden paths such as local MTGA
  logs, runtime status files, failed posts, generated card/tier data, workbook
  exports, secret filenames, and credential filenames.
- The protected-surface gate intentionally allows documented fixtures under
  `tests/fixtures/` by path.
- Schema snapshot tests already reject selected forbidden value snippets inside
  schema snapshots, but there is no general repo text scanner.
- The golden fixture policy anticipates a future `tools/check_secret_patterns.py`
  and requires committed fixtures to be sanitized or synthetic.

Current gap:

- A changed allowed-path text file can still contain private or sensitive
  content that the path-based gate cannot see.

## Public Interface

### Primary CLI

Required changed-file gate:

```bash
python3 tools/check_secret_patterns.py --base <git-ref>
```

Windows-compatible invocation:

```powershell
py tools\check_secret_patterns.py --base <git-ref>
```

Required behavior:

- Compute changed paths from `<git-ref>...HEAD`.
- Scan only added, copied, modified, renamed, type-changed, unmerged, unknown,
  or broken paths that exist in the working tree.
- Exclude deleted paths from content scanning.
- Scan text content for the categories defined in this contract.
- Print a deterministic text report.
- Exit according to the severity rules in this contract.

Required argument:

- `--base <git-ref>`: explicit base branch or ref for changed-file mode.

Required optional arguments:

- `--repo-root <path>`: repository root to inspect, default `"."`.
- `--paths-from-stdin`: read newline-delimited paths from stdin instead of
  running `git diff`. This is required as a test seam and for focused local
  checks.
- `--all`: scan all tracked repository files in advisory mode. This mode must
  not be a failing CI gate until a future baseline/allowlist policy authorizes
  stricter behavior.

Allowed future optional arguments:

- `--format text|json`
- `--head <git-ref>`
- `--max-bytes <n>`
- `--include-warnings-as-failures`
- `--github-annotations`

These future flags must not be required for the baseline local invocation.
Escalating warnings to failures requires explicit issue and contract authority.

### Python Helper Surface

The stable public interface is the CLI. The implementation may expose small
helpers for tests, such as:

- path normalization
- changed-path collection
- tracked-path collection for `--all`
- text/binary detection
- line scanning
- finding classification
- redaction
- report rendering

If helpers are exposed, they are test-facing implementation details. Do not
create runtime parser dependencies on them.

## Inputs

### Base Ref

Type: `str`

Source:

- local user command
- GitHub Actions pull request base ref
- Codex handoff validation command

Examples:

- `origin/main`
- `origin/codex/repo-wide-hardening-run`

Contract:

- The caller must pass the intended base explicitly.
- The scanner must not silently assume `main`.
- Missing or invalid base refs are usage/configuration errors.

### Changed Paths

Primary command:

```bash
git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD
```

Required path behavior:

- Normalize paths to repo-relative forward-slash form.
- Strip leading `./`.
- Deduplicate normalized paths.
- Sort paths lexicographically before scanning for stable reports.
- Ignore paths outside the repository root.
- Skip deleted paths unless explicitly supplied through `--paths-from-stdin`
  and still present on disk.

Changed-file mode is the only mode allowed to fail CI in the first
implementation.

### Explicit Paths From Stdin

When `--paths-from-stdin` is supplied:

- Read newline-delimited paths from stdin.
- Apply the same normalization, deduplication, sorting, and repo-root
  containment checks.
- Treat missing files as warnings in local/test mode unless the path is outside
  repo root or cannot be inspected because of an OS/configuration error.

This mode exists for tests and focused local scans. It is not a broader
authorization to scan or print local private files outside the repo.

### All-Repo Advisory Mode

When `--all` is supplied:

- Scan tracked files from `git ls-files`.
- Do not scan ignored files, untracked files, local runtime artifacts, or files
  outside the repository.
- Report findings using the same categories and redaction rules.
- Return exit code `0` when findings are present, unless a configuration error
  occurs.
- Print `mode: all-repo-advisory` in the report.

Rationale:

- The current branch predates a content scanner baseline and allowlist. All-repo
  findings may include legacy placeholder or policy text. They should be
  review signals until a future issue defines a stable baseline or allowlist.

### File Content

Input type: bytes read from repository files.

Required behavior:

- Do not follow symlinks that resolve outside the repository root.
- Detect likely binary files deterministically.
- Skip binary files with a warning unless the path gate already forbids the
  file by path.
- Decode text as UTF-8. If UTF-8 decoding fails, decode with replacement and
  emit a warning that replacement decoding was used.
- Preserve line numbers using `splitlines()` semantics.
- Never print full matched sensitive values.

Large-file behavior:

- The first implementation may impose a documented per-file byte limit for CI
  safety.
- If a changed text file exceeds that limit, emit a warning and continue.
- Do not silently pass an oversized changed text file without reporting that
  it was not fully scanned.

## Finding Categories

The scanner must use stable category IDs. A category's severity may depend on
path context, placeholder context, and scanner mode.

### Forbidden In Changed-File Mode

These categories should fail changed-file mode when they are detected with
live-looking, non-placeholder content:

| Category ID | Meaning |
| --- | --- |
| `live_webhook_url` | A live-looking webhook, Apps Script deployment, or similar integration endpoint URL. |
| `credential_value` | API key, token, OAuth value, bearer/auth header, password, client secret, private key marker, or credential assignment with a non-placeholder value. |
| `private_local_path` | Absolute local user path, especially MTGA `Player.log`, Arena log directories, user-profile paths, or machine-local runtime paths. |
| `raw_player_log_content` | Raw Player.log-style content outside approved sanitized fixture contexts. |
| `failed_post_payload` | Failed webhook payload or queue content committed as text outside approved test/policy contexts. |
| `runtime_status_payload` | Runtime status snapshot content committed as text outside approved test/policy contexts. |
| `generated_data_dump` | Generated card, deck, tier, or oracle data dump content committed as source outside an explicitly authorized fixture/snapshot. |
| `workbook_export_marker` | Raw workbook export content, exported workbook filenames, or spreadsheet/workbook identifiers that look live/private rather than placeholder text. |

### Warning In Changed-File Mode

These categories should not fail the first implementation, but must be visible:

| Category ID | Meaning |
| --- | --- |
| `placeholder_secret_reference` | Obvious placeholder/test/redacted secret examples. |
| `artifact_path_reference` | References to ignored local artifact paths in docs, tests, policies, or comments. |
| `sanitized_fixture_marker` | Player.log-style markers inside a documented sanitized fixture path. |
| `ambiguous_private_marker` | A token, URL, path, or log marker that looks relevant but is not clearly live/private. |
| `binary_skipped` | A changed binary file was not content-scanned. |
| `oversized_skipped` | A changed file exceeded the implemented scan limit. |
| `decode_replacement_used` | A file required replacement decoding before text scanning. |

### Allowed Contexts

Allowed does not mean unscanned. It means the scanner may avoid reporting
known-safe placeholder or policy text when it is clearly not a private value.

Allowed contexts include:

- obvious placeholder values containing markers such as `example`, `fake`,
  `dummy`, `placeholder`, `redacted`, `test`, `sample`, `configured`, or
  `not-real`
- angle-bracket placeholders such as `<redacted>` or `<placeholder-token>`
- `YOUR_*` style documentation placeholders
- sanitized parser fixture labels such as `local-user`, `opponent-user`,
  `match-regression-*`, and `deck-uuid`
- policy documents that discuss forbidden categories without embedding
  live-looking values

Allowed context limits:

- A real-looking webhook URL or credential value must still be forbidden even
  inside docs or tests.
- A fixture path under `tests/fixtures/` is not proof of sanitization by
  itself. It may lower raw Player.log markers to warnings only when the content
  has clear sanitized fixture context, but live-looking secrets must still
  fail.
- Inline suppressions are not authorized in the first implementation. Do not
  add a `noqa`-style marker that could hide real secrets without a future
  contract.

## Severity And Exit Codes

Severity values:

- `forbidden`
- `warning`
- `allowed`

Result values:

- `passed`: no forbidden findings and no warnings
- `warning`: warnings present, no forbidden findings
- `failed`: one or more forbidden findings
- `error`: usage, git, repo-root, filesystem, or configuration error

Exit codes:

- `0`: `passed` or `warning` result
- `1`: `failed` result in changed-file mode
- `2`: `error` result

All-repo advisory mode:

- Must return `0` for `passed`, `warning`, or `failed`-looking findings in the
  initial implementation.
- Must still return `2` for configuration errors.
- Must label the report so the user knows findings are advisory.

## Report Shape

Required text report:

```text
Secret / Private Marker Scan
mode: changed-files
base: origin/main
head: HEAD
scanned_paths: <n>
skipped_paths: <n>
forbidden: <n>
warnings: <n>

FORBIDDEN <category> <path>:<line> - <reason> [excerpt: <redacted-preview>]
WARNING <category> <path>:<line> - <reason> [excerpt: <redacted-preview>]

result: passed|warning|failed|error
```

Required report behavior:

- Findings are sorted by severity (`FORBIDDEN` before `WARNING`), path, line,
  category, then reason.
- Each finding includes category, path, line number, and reason.
- The report never prints full secret values.
- The report never prints full private local paths with usernames.
- The report never prints full webhook URLs, deployment IDs, spreadsheet IDs,
  bearer tokens, passwords, or credential values.
- If no excerpt can be made safely, use `[excerpt: <redacted>]`.

Allowed redacted preview examples:

- `WEBHOOK_URL=<redacted:live_webhook_url>`
- `Authorization: Bearer <redacted:credential_value>`
- `/Users/<redacted>/.../Player.log`
- `[Client GRE] <redacted:raw_player_log_content>`
- `<redacted:failed_post_payload>`

Do not include actual live secret examples in code, tests, docs, reports, or
fixtures.

## Redaction Rules

Required guarantees:

- Redaction happens before report rendering.
- Full matched sensitive values are never stored in rendered `Finding` strings.
- Tests must assert that forbidden raw values do not appear in reports.
- Redacted previews are capped to a small deterministic length.
- Redaction preserves enough context for a reviewer to understand why the line
  was flagged without exposing the sensitive material.
- If a scanner rule cannot produce a safe redacted preview, it must produce only
  category, path, line, and reason.

Stable finding identity:

- If the implementation needs a finding fingerprint, it must derive it from
  category, normalized path, line number, and rule ID, not from the raw secret
  value.
- Do not hash or print secret values for "safe" display. Hashes can still be
  sensitive when the input is guessable.

## Fixture And Placeholder Policy

Committed fixtures must follow
`docs/contracts/code_hardening_golden_fixture_policy.md`.

Scanner fixture behavior:

- `tests/fixtures/*.log` may contain Player.log-style parser evidence only when
  sanitized or synthetic.
- Existing fixture paths are allowed by the path gate, but content scanning
  should still catch live-looking secrets, private local paths, failed-post
  payloads, runtime status snapshots, generated data dumps, and workbook export
  markers.
- Player.log-style markers inside existing sanitized fixture slices should be
  warnings or allowed context, not forbidden by default.
- New or substantially changed fixtures should trigger review through the
  golden fixture policy even when the scanner passes.

Test placeholder behavior:

- Tests must not commit real secrets or values copied from live systems.
- Tests that need forbidden-looking values should construct synthetic values
  from clearly test-owned fragments at runtime, or use values labeled fake/test
  while still proving redaction behavior.
- Placeholder allowlists must be rule-based and reviewable. They must not
  contain real secret values.

## Binary, Large, And Unreadable Files

Binary files:

- In changed-file mode, binary files are skipped with `binary_skipped` warning
  unless another rule can classify them without reading content.
- The path-based protected-surface gate remains responsible for forbidding raw
  workbook export extensions and local artifact paths.

Large files:

- If a scan limit exists and a changed text file exceeds it, report
  `oversized_skipped`.
- Do not emit `passed` without mentioning skipped oversized files.

Unreadable files:

- A file inside the changed-file set that exists but cannot be read because of
  filesystem errors should produce result `error` and exit `2`.
- A missing file from git diff should be ignored only if it is a deletion or
  no longer exists after a rename/delete. Otherwise report a warning or error
  according to the implementation's deterministic path handling.

Symlinks:

- Do not follow symlinks outside the repository root.
- Outside-root symlinks are configuration errors in changed-file mode.

## CI Integration Policy

CI integration is allowed but not required in the first implementation PR.

If Codex C includes CI integration, it must:

- run only on pull requests in `.github/workflows/repo-checks.yml`
- use the pull request base ref explicitly:

```powershell
py tools\check_secret_patterns.py --base origin/${{ github.base_ref }}
```

- run after checkout with `fetch-depth: 0`
- fail only for exit code `1` forbidden changed-file findings or exit code `2`
  configuration errors
- keep warnings non-failing in the first rollout
- not run `--all` as a failing CI gate
- not replace pytest, Ruff, Pyright advisory checks, or the protected-surface
  gate

If CI integration is deferred, the implementation handoff must say so and list
the exact local command reviewers should run.

Escalating all-repo findings, warnings, protected-surface warnings, fixture
metadata gaps, or advisory findings into failing CI requires a future issue and
contract update.

## Side Effects

Allowed side effects:

- Read git metadata.
- Read tracked or explicitly provided repository files.
- Print a report to stdout or stderr.
- Return a deterministic exit code.

Forbidden side effects:

- Do not write files.
- Do not modify runtime status.
- Do not write failed posts, raw logs, generated data, workbook exports, or
  fixture files.
- Do not call network services or third-party secret scanners.
- Do not mutate environment variables or secret configuration.
- Do not post webhooks.
- Do not access live workbooks or Apps Script deployments.
- Do not change parser/runtime behavior.

## Error Behavior

Usage errors:

- Missing `--base` in changed-file mode exits `2`.
- Mutually incompatible flags exit `2` with a concise usage message.

Git errors:

- Invalid base refs, missing git, or git command failures exit `2`.
- Reports must include `result: error`.

Scan errors:

- Filesystem errors for changed files exit `2` unless the path is a deletion or
  deterministic skip covered by this contract.
- Binary or oversized changed files warn and exit `0` unless a future contract
  escalates them.

Policy ambiguity:

- Prefer warning over failing when a marker is ambiguous.
- Prefer forbidden when a live-looking secret, private local path, or private
  runtime artifact is clearly present.
- Route back to Codex B if implementation cannot distinguish a required
  placeholder allowance from a forbidden live-looking value without changing
  this contract.

## Relationship To Protected-Surface Gate

The scanner and path gate are separate checks.

Required relationship:

- `tools/check_protected_surfaces.py` continues to classify changed paths.
- `tools/check_secret_patterns.py` classifies text content in allowed or
  protected paths.
- A path-gate warning does not authorize content findings.
- A clean content scan does not authorize protected-surface code changes.
- A clean path gate does not prove file content is safe.
- Both checks should appear in submitter/deployer validation when the scanner
  exists.

The scanner may reuse small helper logic from the path gate only if tests lock
the shared behavior and the dependency does not make either report harder to
understand.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event kind values
- parser payload shapes
- match identity
- game identity
- deduplication
- secrets or environment variable semantics
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- tracker completion
- direct targeting of `main`

Allowed implementation surfaces, if scoped to this contract:

- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md`
- `docs/contract_test_reports/repo_wide_secret_private_marker_scanner.md`
- `.github/workflows/repo-checks.yml`, only if CI integration follows this
  contract exactly
- PR template or workflow docs are not authorized in the first implementation
  unless the issue is explicitly updated.

## Required Tests

Focused tests for `tests/test_check_secret_patterns.py`:

- CLI usage:
  - missing `--base` exits `2`
  - invalid git base exits `2`
  - `--paths-from-stdin` scans supplied paths
  - `--all` is advisory and non-failing for findings
- Path collection:
  - changed-file mode uses `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`
  - paths are normalized, deduplicated, sorted, and constrained to repo root
  - deleted paths do not create false content failures
- Text scanning:
  - live-looking webhook URLs fail in changed-file mode
  - credential assignments fail when values are non-placeholder
  - obvious placeholder/redacted/test values warn or pass according to category
  - private user paths fail with usernames redacted
  - raw Player.log markers outside fixtures fail
  - sanitized fixture markers under `tests/fixtures/` do not fail by default
  - failed-post/runtime-status/generated-data/workbook-export markers are
    classified with stable categories
- Redaction:
  - reports never contain the full forbidden value used by tests
  - reports redact webhook URLs, auth headers, tokens, passwords, local user
    names, spreadsheet IDs, deployment IDs, and raw private snippets
  - finding fingerprints, if any, do not use raw secret values
- File handling:
  - binary files warn as skipped
  - oversized files warn as skipped when a limit is configured
  - decode replacement warns but still scans
  - unreadable changed files exit `2`
  - symlinks outside repo root exit `2`
- Report and exit behavior:
  - summary fields are present
  - forbidden findings produce exit `1` in changed-file mode
  - warning-only reports produce exit `0`
  - config errors produce exit `2`
  - findings are sorted deterministically
- Compatibility:
  - existing `tests/fixtures/` sanitized slices do not fail the scanner
  - `tests/test_check_protected_surfaces.py` still passes

Implementation validation:

```bash
python3 -m pytest -q tests/test_check_secret_patterns.py
python3 -m pytest -q tests/test_check_protected_surfaces.py
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
python3 -m ruff check src tests tools
git diff --check
```

If CI integration is included:

```bash
python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
rg -n "check_secret_patterns.py --base" .github/workflows/repo-checks.yml
```

Before submitter work:

```bash
python3 -m pytest -q tests
python3 -m ruff check src tests tools
python3 -m pyright
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

## Acceptance Criteria

- `docs/contracts/repo_wide_secret_private_marker_scanner.md` exists and links
  issue #84 and tracker #82.
- The contract names repository content-safety classification as the owning
  layer.
- The contract defines changed-file scanning, optional all-repo advisory
  scanning, CLI behavior, report shape, categories, severities, exit codes,
  redaction rules, fixture allowances, binary/unreadable handling, CI policy,
  protected surfaces, and test obligations.
- The contract keeps parser/runtime/workbook/App Script behavior out of scope.
- The contract does not commit real secret examples, raw logs, generated data,
  runtime status files, failed posts, or workbook exports.
- The contract routes implementation to Codex C and does not mark tracker #82
  complete.

## Open Questions And Contract Risks

- Exact regexes for each category should be chosen in implementation and
  reviewed against false-positive risk.
- Existing docs and tests may contain policy references that look sensitive in
  all-repo mode; all-repo findings stay advisory until a baseline/allowlist
  policy exists.
- Fixture sanitization remains partly policy-driven because existing fixtures
  do not have machine-readable provenance metadata.
- CI integration could be noisy if included before the scanner is proven
  locally. Deferring CI is acceptable if the implementation handoff records the
  local command.
- Redaction must be tested carefully; a scanner that reports the secret value
  creates the risk it is meant to prevent.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer.

Codex C should compare the current repo against this contract, implement the
smallest deterministic scanner and focused tests needed to satisfy it, and
produce an implementation handoff. CI integration is allowed but not required;
if included, it must follow this contract exactly.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #84 and docs/contracts/repo_wide_secret_private_marker_scanner.md.

Goal:
Compare the current repo-wide hardening state against the secret/private-marker scanner contract. Implement only the smallest deterministic scanner, focused tests, and handoff needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/84
- https://github.com/Tahjali11/Mythic-Edge/issues/82
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/repo_wide_secret_private_marker_scanner.md
- docs/contract_test_reports/repo_wide_hardening_baseline.md
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- .gitignore
- .github/workflows/repo-checks.yml
- .github/pull_request_template.md
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- tests/fixtures/

Do:
- Implement tools/check_secret_patterns.py.
- Add focused tests in tests/test_check_secret_patterns.py.
- Preserve deterministic local-only behavior and redacted reports.
- Make changed-file mode fail only on clearly forbidden live/private content.
- Keep --all advisory/report-only unless a future contract says otherwise.
- Preserve the existing protected-surface path gate.
- Produce docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md with comparison, changes made, validation run, open risks, CI integration decision, and next recommended role.

Do not:
- Commit real secret examples, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Print full secret values in reports or tests.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, runtime semantics, or protected surfaces outside this contract.
- Add network calls or third-party secret scanning services.
- Make all-repo mode or warnings fail CI.
- Target main directly; work should continue on codex/repo-wide-hardening-run.
- Stage or commit unless explicitly asked.
- Mark tracker #82 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/84"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/repo_wide_secret_private_marker_scanner.md"
  target_artifact: "docs/implementation_handoffs/repo_wide_secret_private_marker_scanner_comparison.md"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  validation:
    - "python3 -m pytest -q tests/test_check_secret_patterns.py"
    - "python3 -m pytest -q tests/test_check_protected_surfaces.py"
    - "python3 tools/check_secret_patterns.py --base origin/main"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not commit real secret examples, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not print full secret values in scanner reports."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces outside this contract."
    - "Do not add network calls or third-party secret scanning services."
    - "Do not make all-repo mode or warnings fail CI."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
