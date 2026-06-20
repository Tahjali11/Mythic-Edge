"""Deterministic consistency checker for Mythic Edge agent governance docs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"

RESULT_PASSED = "passed"
RESULT_WARNING = "warning"
RESULT_FAILED = "failed"
RESULT_ERROR = "error"

MODE_REPO = "repo"

REQUIRED_FILES: tuple[str, ...] = (
    "AGENTS.md",
    "docs/agent_rules.yml",
    "docs/agent_constitution.md",
    "docs/codex_module_workflow.md",
    "docs/agent_threads/problem_representation.md",
    "docs/agent_threads/module_contract.md",
    "docs/agent_threads/implementation.md",
    "docs/agent_threads/module_fixer.md",
    "docs/agent_threads/review.md",
    "docs/agent_threads/contract_test.md",
    "docs/agent_threads/module_submitter.md",
    "docs/agent_threads/integration_deployer.md",
    "docs/agent_threads/constitutional_lawyer.md",
    "docs/templates/problem_representation.md",
    "docs/templates/module_contract.md",
    "docs/templates/implementation_handoff.md",
    "docs/templates/contract_test_report.md",
    "docs/templates/workflow_handoff.md",
    "docs/templates/current_status.md",
    "docs/templates/constitution_feedback_packet.md",
    ".github/ISSUE_TEMPLATE/module_workflow.yml",
    ".github/pull_request_template.md",
    "docs/decisions/README.md",
    "docs/decisions/ADR_TEMPLATE.md",
)

REFERENCE_DOCS: tuple[str, ...] = (
    "AGENTS.md",
    "docs/agent_constitution.md",
    "docs/codex_module_workflow.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/module_workflow.yml",
    "docs/decisions/README.md",
)

CANONICAL_ROLES: dict[str, tuple[str, tuple[str, ...]]] = {
    "A": ("Thinker", ("docs/agent_threads/problem_representation.md",)),
    "B": ("Module Contract Writer", ("docs/agent_threads/module_contract.md",)),
    "C": ("Module Implementer", ("docs/agent_threads/implementation.md",)),
    "D": ("Module Fixer", ("docs/agent_threads/module_fixer.md",)),
    "E": (
        "Module Reviewer",
        ("docs/agent_threads/review.md", "docs/agent_threads/contract_test.md"),
    ),
    "F": ("Module Submitter", ("docs/agent_threads/module_submitter.md",)),
    "G": ("Integration Deployer", ("docs/agent_threads/integration_deployer.md",)),
    "H": ("Constitutional Lawyer", ("docs/agent_threads/constitutional_lawyer.md",)),
}

NORMAL_PATH = ("A", "B", "C", "E", "F", "G")
HANDOFF_BLOCK_KEYS = (
    "repository",
    "repository_url",
    "issue",
    "tracker",
    "completed_thread",
    "next_thread",
    "source_artifact",
    "target_artifact",
    "risk_tier",
    "base_branch",
    "target_branch",
    "branch",
    "validation",
    "stop_conditions",
)
VALID_NEXT_THREADS = ("A", "B", "C", "D", "E", "F", "G", "none")
ISSUE_TEMPLATE_IDS = (
    "repository",
    "repository_url",
    "source_artifacts",
    "target_artifact",
    "base_branch",
    "target_branch",
    "branch",
    "protected_surfaces",
    "validation",
    "stop_conditions",
)
PROMPT_SCHEMA_REQUIRED = (
    "constitution_instruction",
    "role",
    "issue",
    "source_artifacts",
    "target_artifact",
    "risk_tier",
    "branch",
    "goal",
    "forbidden_surfaces_or_bundle",
    "validation",
    "stop_conditions",
    "expected_output",
)
HANDOFF_SCHEMA_REQUIRED = (
    "role_performed",
    "source_issue",
    "source_artifact",
    "artifact_produced",
    "risk_tier",
    "files_changed",
    "code_changed",
    "tests_changed",
    "interface_changes",
    "validation_evidence",
    "still_unverified_layers",
    "next_recommended_role",
    "pasteable_next_thread_prompt",
    "workflow_handoff",
)
ADR_RECOMMENDED_FIELDS = (
    "# ADR-",
    "Status:",
    "Date:",
    "Decision owners / workflow role:",
    "Related issues:",
    "Related PRs:",
    "Related contracts, handoffs, or review reports:",
    "## Context",
    "## Decision",
    "## Scope",
    "## Non-Goals",
    "## Consequences",
    "## Truth Ownership Impact",
    "## Protected Surfaces",
    "## Validation Or Review Evidence",
    "## Supersedes",
    "## Superseded By",
    "## Follow-Ups",
)
FORBIDDEN_LOCAL_ARTIFACT_TERMS = (
    "secrets",
    "webhook urls",
    "api keys",
    "tokens",
    "credentials",
    "local mtga logs",
    "failed posts",
    "runtime status files",
    "generated card data",
    "raw workbook exports",
)
PARSER_TRUTH_BOUNDARY_TERMS = (
    "workbook formulas",
    "dashboard logic",
    "apps script transport",
    "webhook transport",
    "ai-generated interpretation",
)
D_LOOPBACK_ONLY_RE = re.compile(r"\b(?:codex\s+)?d\b(?=.{0,160}\bonly\b)(?=.{0,160}\bloopback\b)")


@dataclass(frozen=True)
class Finding:
    severity: str
    category_id: str
    path: str
    reason: str


@dataclass(frozen=True)
class CheckResult:
    mode: str
    checked_files: tuple[str, ...]
    findings: tuple[Finding, ...]
    error: str = ""

    @property
    def errors(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == SEVERITY_ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity == SEVERITY_WARNING)

    @property
    def result(self) -> str:
        if self.error:
            return RESULT_ERROR
        if self.errors:
            return RESULT_FAILED
        if self.warnings:
            return RESULT_WARNING
        return RESULT_PASSED

    @property
    def exit_code(self) -> int:
        if self.error:
            return 2
        if self.errors:
            return 1
        return 0


@dataclass(frozen=True)
class Reference:
    source_path: str
    raw_target: str
    resolved_target: str
    context: str
    is_glob: bool


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    while text.startswith("//"):
        text = text[1:]
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _normalized_text(text: str) -> str:
    return " ".join(text.lower().split())


def _add_finding(
    findings: list[Finding],
    severity: str,
    category_id: str,
    path: str,
    reason: str,
) -> None:
    findings.append(Finding(severity, category_id, normalize_path(path), reason))


def _sort_findings(findings: Iterable[Finding]) -> tuple[Finding, ...]:
    severity_order = {SEVERITY_ERROR: 0, SEVERITY_WARNING: 1}
    return tuple(
        sorted(
            findings,
            key=lambda item: (
                severity_order.get(item.severity, 9),
                item.category_id,
                item.path,
                item.reason,
            ),
        ),
    )


def _safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_required_files(repo_root: Path, findings: list[Finding]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for relative in REQUIRED_FILES:
        path = repo_root / relative
        if not path.exists():
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "missing_required_file",
                relative,
                "Required governance file is missing.",
            )
            continue
        try:
            texts[relative] = _safe_read(path)
        except OSError as exc:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "missing_required_file",
                relative,
                f"Required governance file cannot be read: {exc}",
            )
    return texts


def _section_text(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line == f"{heading}:":
            start = index + 1
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        if line and not line.startswith(" ") and not line.startswith("\t"):
            break
        collected.append(line)
    return "\n".join(collected)


def _extract_top_level_list(text: str, heading: str) -> tuple[str, ...]:
    section = _section_text(text, heading)
    values: list[str] = []
    for line in section.splitlines():
        match = re.match(r"\s*-\s+(.+?)\s*$", line)
        if match:
            values.append(match.group(1).strip().strip('"'))
    return tuple(values)


def _extract_nested_list(text: str, section: str, nested_key: str) -> tuple[str, ...]:
    section_body = _section_text(text, section)
    lines = section_body.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(rf"\s+{re.escape(nested_key)}:\s*$", line):
            start = index + 1
            break
    if start is None:
        return ()
    values: list[str] = []
    for line in lines[start:]:
        if line and re.match(r"\s{2,}\S[^:]*:\s*(?:$|.+)", line) and not re.match(r"\s+-\s+", line):
            break
        match = re.match(r"\s*-\s+(.+?)\s*$", line)
        if match:
            values.append(match.group(1).strip().strip('"'))
    return tuple(values)


def _extract_roles(agent_rules: str) -> dict[str, str]:
    roles_body = _section_text(agent_rules, "roles")
    roles: dict[str, str] = {}
    current_id = ""
    for line in roles_body.splitlines():
        role_match = re.match(r"\s{2}([A-G]):\s*$", line)
        if role_match:
            current_id = role_match.group(1)
            continue
        name_match = re.match(r"\s{4}name:\s*(.+?)\s*$", line)
        if current_id and name_match:
            roles[current_id] = name_match.group(1).strip()
    aux_body = _section_text(agent_rules, "auxiliary_roles")
    aux_match = re.search(r"^\s{2}H:\s*$.*?^\s{4}name:\s*(.+?)\s*$", aux_body, re.M | re.S)
    if aux_match:
        roles["H"] = aux_match.group(1).strip()
    return roles


def _extract_aux_normal_member(agent_rules: str) -> str:
    aux_body = _section_text(agent_rules, "auxiliary_roles")
    match = re.search(r"^\s{4}normal_path_member:\s*(.+?)\s*$", aux_body, re.M)
    return match.group(1).strip().lower() if match else ""


def _looks_like_local_reference(raw_target: str, source_path: str, *, markdown_link: bool) -> bool:
    target = raw_target.strip().strip('"').strip("'")
    if not target or target.startswith(("#", "<")):
        return False
    lowered = target.lower()
    if "://" in lowered or lowered.startswith(("mailto:", "app://")):
        return False
    if ":" in target and not re.match(r"^[A-Za-z]:[\\/]", target):
        return False
    if any(marker in target for marker in (" ", "{", "}", "$", "|")):
        return False
    rootish_prefixes = (
        "AGENTS.md",
        "docs/",
        "tools/",
        "tests/",
        "src/",
        ".github/",
        "README.md",
        "pyproject.toml",
    )
    if target.startswith(rootish_prefixes):
        return True
    if markdown_link and source_path and re.search(r"\.(?:md|yml|yaml|py|json|txt)$", target):
        return True
    return False


def _strip_reference_suffix(raw_target: str) -> str:
    target = raw_target.strip()
    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    return target


def _resolve_reference(source_path: str, raw_target: str, *, markdown_link: bool) -> str:
    target = _strip_reference_suffix(raw_target).strip().strip('"').strip("'")
    if target.startswith(("AGENTS.md", "docs/", "tools/", "tests/", "src/", ".github/", "README.md", "pyproject.toml")):
        return normalize_path(target)
    if markdown_link:
        return normalize_path(Path(source_path).parent / target)
    return normalize_path(target)


def _line_for_offset(text: str, offset: int) -> str:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end]


def extract_repo_local_references(path: str, text: str) -> tuple[Reference, ...]:
    refs: list[Reference] = []
    for match in re.finditer(r"`([^`\n]+)`", text):
        raw_target = match.group(1)
        if not _looks_like_local_reference(raw_target, path, markdown_link=False):
            continue
        refs.append(
            Reference(
                source_path=path,
                raw_target=raw_target,
                resolved_target=_resolve_reference(path, raw_target, markdown_link=False),
                context=_line_for_offset(text, match.start()),
                is_glob="*" in raw_target,
            ),
        )
    for match in re.finditer(r"\[[^\]]+\]\(([^)\s]+)\)", text):
        raw_target = match.group(1)
        if not _looks_like_local_reference(raw_target, path, markdown_link=True):
            continue
        refs.append(
            Reference(
                source_path=path,
                raw_target=raw_target,
                resolved_target=_resolve_reference(path, raw_target, markdown_link=True),
                context=_line_for_offset(text, match.start()),
                is_glob="*" in raw_target,
            ),
        )
    return tuple(refs)


def _check_required_references(
    repo_root: Path,
    texts: dict[str, str],
    findings: list[Finding],
) -> None:
    active_docs = list(REFERENCE_DOCS)
    active_docs.extend(
        str(path.relative_to(repo_root))
        for path in sorted((repo_root / "docs/agent_threads").glob("*.md"))
    )
    active_docs.extend(str(path.relative_to(repo_root)) for path in sorted((repo_root / "docs/templates").glob("*.md")))
    active_docs.extend(
        str(path.relative_to(repo_root))
        for path in sorted((repo_root / "docs/decisions").glob("ADR-*.md"))
    )

    for path in active_docs:
        text = texts.get(path)
        if text is None:
            file_path = repo_root / path
            if not file_path.exists():
                continue
            try:
                text = _safe_read(file_path)
                texts[path] = text
            except OSError as exc:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "missing_required_file",
                    path,
                    f"Governance file cannot be read: {exc}",
                )
                continue

        for reference in extract_repo_local_references(path, text):
            target = reference.resolved_target
            if target == "docs/archive" or target.startswith("docs/archive/"):
                if "archive" not in reference.context.lower():
                    _add_finding(
                        findings,
                        SEVERITY_WARNING,
                        "archived_reference_active_context",
                        path,
                        f"Archived document reference may be read as active authority: {target}",
                    )
                continue
            if reference.is_glob:
                if not tuple(repo_root.glob(target)):
                    _add_finding(
                        findings,
                        SEVERITY_ERROR,
                        "missing_referenced_file",
                        path,
                        f"Referenced glob has no matches: {target}",
                    )
                continue
            if not (repo_root / target).exists():
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "missing_referenced_file",
                    path,
                    f"Referenced repo-local file does not exist: {target}",
                )


def _check_roles(texts: dict[str, str], findings: list[Finding]) -> None:
    agent_rules = texts.get("docs/agent_rules.yml", "")
    roles = _extract_roles(agent_rules)
    for role_id, (expected_name, role_docs) in CANONICAL_ROLES.items():
        actual = roles.get(role_id)
        if actual != expected_name:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "role_registry_mismatch",
                "docs/agent_rules.yml",
                f"Role {role_id} name should be {expected_name!r}, found {actual!r}.",
            )
        for role_doc in role_docs:
            if role_doc not in REQUIRED_FILES:
                continue
            if role_doc not in texts:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "role_doc_reference_mismatch",
                    role_doc,
                    f"Canonical role {role_id} doc is missing.",
                )

    normal_path = _extract_nested_list(agent_rules, "routing", "normal_path")
    if normal_path != NORMAL_PATH:
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "normal_path_mismatch",
            "docs/agent_rules.yml",
            f"routing.normal_path should be {' -> '.join(NORMAL_PATH)}.",
        )
    if "D" in normal_path:
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "normal_path_mismatch",
            "docs/agent_rules.yml",
            "Codex D is loopback-only and must not be in routing.normal_path.",
        )
    if "H" in normal_path or _extract_aux_normal_member(agent_rules) != "false":
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "auxiliary_role_mismatch",
            "docs/agent_rules.yml",
            "Codex H must be auxiliary only and not a normal path member.",
        )

    for path in ("AGENTS.md", "docs/agent_constitution.md", "docs/codex_module_workflow.md"):
        lowered = _normalized_text(texts.get(path, ""))
        for role_id, (role_name, _) in CANONICAL_ROLES.items():
            if role_name.lower() not in lowered and f"({role_id.lower()})" not in lowered:
                _add_finding(
                    findings,
                    SEVERITY_ERROR,
                    "role_doc_reference_mismatch",
                    path,
                    f"Active governance doc does not reference role {role_id}: {role_name}.",
                )
        if "auxiliary" not in lowered:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "auxiliary_role_mismatch",
                path,
                "Active governance doc does not describe Codex H as auxiliary.",
            )

    workflow = texts.get("docs/codex_module_workflow.md", "")
    normal_path_text = (
        "A Thinker -> B Module Contract Writer -> C Module Implementer -> "
        "E Module Reviewer -> F Module Submitter -> G Integration Deployer"
    )
    if normal_path_text not in workflow:
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "normal_path_mismatch",
            "docs/codex_module_workflow.md",
            "Workflow normal path text must preserve A -> B -> C -> E -> F -> G.",
        )
    if not D_LOOPBACK_ONLY_RE.search(_normalized_text(workflow)):
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "normal_path_mismatch",
            "docs/codex_module_workflow.md",
            "Workflow docs must describe Codex D as loopback-only, not part of the normal happy path.",
        )


def _check_order(order: tuple[str, ...], before: str, after: str) -> bool:
    try:
        return order.index(before) < order.index(after)
    except ValueError:
        return False


def _check_authority_order(texts: dict[str, str], findings: list[Finding]) -> None:
    agent_rules = texts.get("docs/agent_rules.yml", "")
    order = _extract_top_level_list(agent_rules, "authority_order")
    required_pairs = (
        ("system_and_developer", "AGENTS.md"),
        ("current_user_instruction", "AGENTS.md"),
        ("AGENTS.md", "docs/agent_rules.yml"),
        ("docs/agent_rules.yml", "docs/agent_constitution.md"),
        ("current_contract", "current_handoff_or_report"),
        ("current_contract", "older_docs_examples_memory"),
        ("accepted_architecture_decision_records", "older_docs_examples_memory"),
        ("docs/agent_threads", "older_docs_examples_memory"),
        ("docs/templates", "older_docs_examples_memory"),
    )
    for before, after in required_pairs:
        if not _check_order(order, before, after):
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "authority_order_mismatch",
                "docs/agent_rules.yml",
                f"Authority order must keep {before} above {after}.",
            )

    constitution = texts.get("docs/agent_constitution.md", "")
    authority_terms = (
        "active system and developer instructions",
        "explicit user instructions",
        "AGENTS.md",
        "docs/agent_rules.yml",
        "docs/agent_constitution.md",
        "current GitHub issue",
        "current module contract",
        "current implementation handoff",
        "role-specific files",
        "workflow templates",
        "older docs",
    )
    for term in authority_terms:
        if term not in constitution:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "authority_order_mismatch",
                "docs/agent_constitution.md",
                f"Authority-order prose is missing critical term: {term}.",
            )
    normalized_constitution = _normalized_text(constitution)
    if (
        "draft files under `docs/archive/`" not in normalized_constitution
        or "no authority" not in normalized_constitution
    ):
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "authority_order_mismatch",
            "docs/agent_constitution.md",
            "Archived drafts must be described as non-authoritative unless explicitly named.",
        )
    if "Accepted ADRs sit below active governing docs" not in constitution:
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "authority_order_mismatch",
            "docs/agent_constitution.md",
            "Accepted ADR authority relationship must be present.",
        )


def _extract_workflow_handoff_keys(template: str) -> tuple[str, ...]:
    block_match = re.search(r"```yaml\n(.*?)\n```", template, re.S)
    if not block_match:
        return ()
    keys: list[str] = []
    for line in block_match.group(1).splitlines():
        match = re.match(r"\s{2}([A-Za-z_]+):", line)
        if match:
            keys.append(match.group(1))
    return tuple(keys)


def _check_handoff_and_prompt_schema(texts: dict[str, str], findings: list[Finding]) -> None:
    template = texts.get("docs/templates/workflow_handoff.md", "")
    keys = _extract_workflow_handoff_keys(template)
    for key in HANDOFF_BLOCK_KEYS:
        if key not in keys:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "handoff_schema_mismatch",
                "docs/templates/workflow_handoff.md",
                f"workflow_handoff template is missing key: {key}.",
            )
    for value in VALID_NEXT_THREADS:
        if value not in template:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "handoff_schema_mismatch",
                "docs/templates/workflow_handoff.md",
                f"Valid next_thread value is not documented: {value}.",
            )

    agent_rules = texts.get("docs/agent_rules.yml", "")
    prompt_required = _extract_nested_list(agent_rules, "prompt_schema", "required")
    handoff_required = _extract_nested_list(agent_rules, "handoff_schema", "required")
    for item in PROMPT_SCHEMA_REQUIRED:
        if item not in prompt_required:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "prompt_schema_mismatch",
                "docs/agent_rules.yml",
                f"prompt_schema.required is missing: {item}.",
            )
    for item in HANDOFF_SCHEMA_REQUIRED:
        if item not in handoff_required:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "handoff_rule_mismatch",
                "docs/agent_rules.yml",
                f"handoff_schema.required is missing: {item}.",
            )

    workflow = texts.get("docs/codex_module_workflow.md", "").lower()
    for term in ("durable artifact", "pasteable next-thread prompt", "workflow_handoff"):
        if term not in workflow:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "handoff_rule_mismatch",
                "docs/codex_module_workflow.md",
                f"Workflow handoff expectations are missing: {term}.",
            )

    issue_template = texts.get(".github/ISSUE_TEMPLATE/module_workflow.yml", "")
    ids = set(re.findall(r"^\s+id:\s*([A-Za-z0-9_]+)\s*$", issue_template, re.M))
    for field_id in ISSUE_TEMPLATE_IDS:
        if field_id not in ids:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "prompt_schema_mismatch",
                ".github/ISSUE_TEMPLATE/module_workflow.yml",
                f"Issue template is missing field id: {field_id}.",
            )
    if "Do not change workbook schema" not in issue_template:
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "protected_surface_rule_mismatch",
            ".github/ISSUE_TEMPLATE/module_workflow.yml",
            "Issue template protected-surface default text is missing.",
        )


def _extract_readme_statuses(readme: str) -> tuple[str, ...]:
    section_match = re.search(r"## Status Values(.*?)(?:\n## |\Z)", readme, re.S)
    if not section_match:
        return ()
    return tuple(re.findall(r"^- `([^`]+)`:", section_match.group(1), re.M))


def _extract_adr_index(readme: str) -> dict[str, str]:
    index: dict[str, str] = {}
    for match in re.finditer(r"\|\s*\[[^\]]+\]\((ADR-\d{4}-[^)]+\.md)\)\s*\|\s*([^|]+?)\s*\|", readme):
        index[f"docs/decisions/{match.group(1)}"] = match.group(2).strip()
    return index


def _extract_status(text: str) -> str:
    match = re.search(r"^Status:\s*(.+?)\s*$", text, re.M)
    return match.group(1).strip() if match else ""


def _check_adrs(repo_root: Path, texts: dict[str, str], findings: list[Finding]) -> None:
    readme = texts.get("docs/decisions/README.md", "")
    readme_statuses = set(_extract_readme_statuses(readme))
    rule_statuses = set(
        _extract_nested_list(
            texts.get("docs/agent_rules.yml", ""),
            "architecture_decision_records",
            "statuses",
        ),
    )
    if readme_statuses != rule_statuses:
        _add_finding(
            findings,
            SEVERITY_ERROR,
            "adr_status_mismatch",
            "docs/decisions/README.md",
            "ADR status set differs between README and docs/agent_rules.yml.",
        )

    index = _extract_adr_index(readme)
    for indexed_file, status in index.items():
        if not (repo_root / indexed_file).exists():
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_index_mismatch",
                "docs/decisions/README.md",
                f"README ADR index points to missing file: {indexed_file}.",
            )
        if status not in readme_statuses:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_status_mismatch",
                "docs/decisions/README.md",
                f"README ADR index uses unknown status {status!r} for {indexed_file}.",
            )

    for path in sorted((repo_root / "docs/decisions").glob("ADR-*.md")):
        relative = normalize_path(path.relative_to(repo_root))
        if relative.endswith("ADR_TEMPLATE.md"):
            continue
        if not re.match(r"docs/decisions/ADR-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$", relative):
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_index_mismatch",
                relative,
                "Numbered ADR filename must use ADR-0001-short-kebab-title.md style.",
            )
        try:
            text = texts.get(relative) or _safe_read(path)
        except OSError as exc:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_required_field_missing",
                relative,
                f"ADR file cannot be read: {exc}",
            )
            continue
        status = _extract_status(text)
        if not status:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_required_field_missing",
                relative,
                "ADR is missing a Status line.",
            )
        elif status not in readme_statuses:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_status_mismatch",
                relative,
                f"ADR status is not allowed: {status}.",
            )
        if relative not in index:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_index_mismatch",
                relative,
                "Numbered ADR file is missing from docs/decisions/README.md index.",
            )
        elif index[relative] != status:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "adr_index_mismatch",
                relative,
                f"ADR status {status!r} does not match README index status {index[relative]!r}.",
            )
        for field in ADR_RECOMMENDED_FIELDS:
            if field.lower() not in text.lower():
                _add_finding(
                    findings,
                    SEVERITY_WARNING,
                    "adr_required_field_missing",
                    relative,
                    f"ADR recommended field or heading may be missing: {field}.",
                )


def _check_surface_text(texts: dict[str, str], findings: list[Finding]) -> None:
    combined = _normalized_text(
        "\n".join(
            texts.get(path, "")
            for path in (
                "AGENTS.md",
                "docs/agent_rules.yml",
                "docs/agent_constitution.md",
                "docs/codex_module_workflow.md",
            )
        ),
    )
    for term in FORBIDDEN_LOCAL_ARTIFACT_TERMS:
        if term not in combined:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "protected_surface_rule_mismatch",
                "AGENTS.md",
                f"Core forbidden local-artifact term is missing from active docs: {term}.",
            )
    for term in PARSER_TRUTH_BOUNDARY_TERMS:
        if term not in combined:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "protected_surface_rule_mismatch",
                "docs/agent_constitution.md",
                f"Parser truth downstream boundary term is missing: {term}.",
            )
    external_terms = (
        "external tools",
        "connectors",
        "google docs",
        "google sheets",
        "openai documentation tooling",
        "access or collaboration surfaces",
        "not own project truth or repo authority by default",
    )
    for term in external_terms:
        if term not in combined:
            _add_finding(
                findings,
                SEVERITY_ERROR,
                "external_surface_rule_mismatch",
                "docs/agent_constitution.md",
                f"External-surface boundary text is missing: {term}.",
            )


def _check_ci_integration(repo_root: Path, findings: list[Finding]) -> None:
    workflow_path = repo_root / ".github/workflows/repo-checks.yml"
    if not workflow_path.exists():
        return
    try:
        workflow_text = _safe_read(workflow_path)
    except OSError as exc:
        _add_finding(
            findings,
            SEVERITY_WARNING,
            "ci_integration_unauthorized",
            ".github/workflows/repo-checks.yml",
            f"Workflow file could not be read for advisory CI integration check: {exc}",
        )
        return
    if "check_agent_docs.py" in workflow_text:
        _add_finding(
            findings,
            SEVERITY_WARNING,
            "ci_integration_unauthorized",
            ".github/workflows/repo-checks.yml",
            "Agent docs checker appears in CI before this contract authorizes enforcement.",
        )


def run_check(repo_root: str | Path = ".") -> CheckResult:
    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        return CheckResult(MODE_REPO, (), (), error=f"invalid repository root: {repo_root}")

    findings: list[Finding] = []
    texts = _read_required_files(root, findings)
    _check_required_references(root, texts, findings)
    _check_roles(texts, findings)
    _check_authority_order(texts, findings)
    _check_handoff_and_prompt_schema(texts, findings)
    _check_adrs(root, texts, findings)
    _check_surface_text(texts, findings)
    _check_ci_integration(root, findings)

    checked_files = tuple(sorted(texts))
    return CheckResult(MODE_REPO, checked_files, _sort_findings(findings))


def render_report(result: CheckResult) -> str:
    lines = [
        "Agent Docs Consistency Check",
        f"mode: {result.mode}",
        f"checked_files: {len(result.checked_files)}",
        f"errors: {len(result.errors)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration {result.error}")
    else:
        for finding in result.findings:
            label = "ERROR" if finding.severity == SEVERITY_ERROR else "WARNING"
            lines.append(f"{label} {finding.category_id} {finding.path} - {finding.reason}")
    if lines[-1] != "":
        lines.append("")
    lines.append(f"result: {result.result}")
    return "\n".join(lines)


def render_json(result: CheckResult) -> str:
    return json.dumps(
        {
            "mode": result.mode,
            "checked_files": list(result.checked_files),
            "errors": len(result.errors),
            "warnings": len(result.warnings),
            "findings": [asdict(finding) for finding in result.findings],
            "error": result.error,
            "result": result.result,
        },
        indent=2,
        sort_keys=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Mythic Edge agent governance docs for consistency.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Report format.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    result = run_check(args.repo_root)
    output = render_json(result) if args.format == "json" else render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
