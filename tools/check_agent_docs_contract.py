"""Stable contract vocabulary for the agent docs consistency checker."""

from __future__ import annotations

import re

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
D_LOOPBACK_ONLY_RE = re.compile(
    r"\b(?:codex\s+)?d\b(?=.{0,160}\bonly\b)(?=.{0,160}\bloopback\b)",
)
