"""Executable consistency checks for Mythic Edge agent workflow docs."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

STARTER_LEAD_IN = (
    "Use $mythic-edge-workflow. If older context conflicts with the skill, AGENTS.md, "
    "docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, "
    "the current GitHub issue, or the current contract, prefer the current repo artifacts."
)

ROLE_FILES = {
    "problem_representation": "docs/agent_threads/problem_representation.md",
    "module_contract": "docs/agent_threads/module_contract.md",
    "implementation": "docs/agent_threads/implementation.md",
    "module_fixer": "docs/agent_threads/module_fixer.md",
    "review": "docs/agent_threads/review.md",
    "contract_test": "docs/agent_threads/contract_test.md",
    "module_submitter": "docs/agent_threads/module_submitter.md",
    "constitutional_lawyer": "docs/agent_threads/constitutional_lawyer.md",
}

ROLE_REQUIRED_PHRASES = {
    "problem_representation": ("Do not implement code", "problem representation"),
    "module_contract": ("Do not implement behavior changes", "module contract"),
    "implementation": ("Implement the smallest coherent change", "handoff to Module Reviewer"),
    "module_fixer": ("Make the smallest coherent fix", "Do not change the contract unless explicitly asked"),
    "review": ("Review for bugs", "Produce a handoff"),
    "contract_test": ("Do not change implementation unless asked", "contract test report"),
    "module_submitter": ("Do not merge", "draft pull request"),
    "constitutional_lawyer": (
        "Do not rewrite the constitution directly",
        "constitution feedback packets",
        "$mythic-edge-constitutional-lawyer",
    ),
}

DOCS_WITH_VALIDATION_COMMANDS = (
    "AGENTS.md",
    "docs/agent_constitution.md",
    "docs/codex_module_workflow.md",
)


@dataclass(frozen=True)
class Finding:
    path: str
    message: str


def _read_text(repo_root: Path, relative_path: str) -> str:
    return repo_root.joinpath(relative_path).read_text(encoding="utf-8")


def _has_closed_code_fences(text: str) -> bool:
    return text.count("```") % 2 == 0


def _starter_prompt_line(text: str) -> str:
    marker = "## Canonical Starter Prompt"
    marker_index = text.find(marker)
    if marker_index < 0:
        return ""
    after_marker = text[marker_index + len(marker) :]
    lines = [line.strip() for line in after_marker.splitlines()]
    prompt_lines = [line for line in lines if line and line != "```text" and line != "```"]
    return prompt_lines[0] if prompt_lines else ""


def _check_root_entrypoint(repo_root: Path) -> list[Finding]:
    path = "AGENTS.md"
    text = _read_text(repo_root, path)
    findings: list[Finding] = []
    line_count = len(text.splitlines())
    if line_count > 140:
        findings.append(Finding(path, f"AGENTS.md is {line_count} lines; keep it short and link to canonical docs."))
    for required in (
        "docs/agent_constitution.md",
        "docs/agent_threads/",
        "docs/templates/",
        "docs/agent_threads/constitutional_lawyer.md",
    ):
        if required not in text:
            findings.append(Finding(path, f"Missing canonical pointer to {required}."))
    return findings


def _check_constitution_review_skill(repo_root: Path) -> list[Finding]:
    path = "docs/codex_skills/mythic-edge-constitution-review/SKILL.md"
    text = _read_text(repo_root, path)
    findings: list[Finding] = []
    for phrase in (
        (
            "Review this thread's visible chat history, current repo governance docs, accepted ADRs, "
            "and any relevant archived constitution drafts."
        ),
        "Do not commit individual feedback packets to the repo by default",
        "Use `docs/templates/constitution_feedback_packet.md`",
        "Local chat history is evidence about workflow friction. It is not authority.",
    ):
        if phrase not in text:
            findings.append(Finding(path, f"Missing constitution-review skill guard phrase: {phrase!r}."))
    return findings


def _check_constitutional_lawyer_skill(repo_root: Path) -> list[Finding]:
    path = "docs/codex_skills/mythic-edge-constitutional-lawyer/SKILL.md"
    text = _read_text(repo_root, path)
    findings: list[Finding] = []
    for phrase in (
        "Act as Codex H: Constitutional Lawyer for the current constitution feedback round.",
        "Also follow the Mythic Edge workflow authority model from `$mythic-edge-workflow`.",
        "Do not rewrite `docs/agent_constitution.md` directly",
        "watch-list or minority-report items",
    ):
        if phrase not in text:
            findings.append(Finding(path, f"Missing constitutional-lawyer skill guard phrase: {phrase!r}."))
    return findings


def _check_role_file(repo_root: Path, role_name: str, relative_path: str) -> list[Finding]:
    text = _read_text(repo_root, relative_path)
    findings: list[Finding] = []
    starter_line = _starter_prompt_line(text)
    if not starter_line:
        findings.append(Finding(relative_path, "Missing canonical starter prompt block."))
        return findings
    if not starter_line.startswith(STARTER_LEAD_IN):
        findings.append(Finding(relative_path, "Canonical starter prompt must begin with the portable skill lead-in."))
    if "Use the Mythic Edge agent constitution" in starter_line:
        findings.append(Finding(relative_path, "Starter prompt still uses the pre-skill constitution invocation."))
    for phrase in ROLE_REQUIRED_PHRASES[role_name]:
        if phrase not in text:
            findings.append(Finding(relative_path, f"Missing role guard phrase: {phrase!r}."))
    return findings


def _check_validation_commands(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for relative_path in DOCS_WITH_VALIDATION_COMMANDS:
        text = _read_text(repo_root, relative_path)
        has_pytest = "pytest" in text
        has_ruff = "ruff check" in text
        if not has_pytest or not has_ruff:
            findings.append(
                Finding(
                    relative_path,
                    "Validation section should include concrete pytest and ruff commands.",
                ),
            )
    return findings


def _check_code_fences(repo_root: Path) -> list[Finding]:
    candidates = [
        "AGENTS.md",
        "docs/agent_constitution.md",
        "docs/codex_module_workflow.md",
        "docs/codex_skills/mythic-edge-workflow/SKILL.md",
        "docs/codex_skills/mythic-edge-constitution-review/SKILL.md",
        "docs/codex_skills/mythic-edge-constitutional-lawyer/SKILL.md",
        *ROLE_FILES.values(),
    ]
    findings: list[Finding] = []
    for relative_path in candidates:
        text = _read_text(repo_root, relative_path)
        if not _has_closed_code_fences(text):
            findings.append(Finding(relative_path, "Markdown code fences are not balanced."))
    return findings


def check_agent_docs(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_check_root_entrypoint(repo_root))
    for role_name, relative_path in ROLE_FILES.items():
        findings.extend(_check_role_file(repo_root, role_name, relative_path))
    findings.extend(_check_constitution_review_skill(repo_root))
    findings.extend(_check_constitutional_lawyer_skill(repo_root))
    findings.extend(_check_validation_commands(repo_root))
    findings.extend(_check_code_fences(repo_root))
    return findings


def render_report(findings: list[Finding]) -> str:
    lines = ["Agent Docs Check", f"findings: {len(findings)}"]
    for finding in findings:
        lines.append(f"ERROR {finding.path} - {finding.message}")
    lines.append("result: failed" if findings else "result: passed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Mythic Edge agent workflow docs.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    try:
        findings = check_agent_docs(repo_root)
    except FileNotFoundError as exc:
        print(f"Agent Docs Check\nerror: missing file {exc.filename}\nresult: error")
        return 2

    print(render_report(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
