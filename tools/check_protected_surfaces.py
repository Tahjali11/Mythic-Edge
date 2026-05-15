"""Path-based protected-surface diff gate for Mythic Edge."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SEVERITY_ALLOWED = "allowed"
SEVERITY_FORBIDDEN = "forbidden"
SEVERITY_WARNING = "warning"


@dataclass(frozen=True)
class Rule:
    category_id: str
    reason: str
    patterns: tuple[str, ...] = ()
    filename_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class Classification:
    path: str
    severity: str
    category_id: str
    reason: str


@dataclass(frozen=True)
class GateResult:
    base: str
    head: str
    changed_paths: tuple[str, ...]
    classifications: tuple[Classification, ...]
    error: str = ""

    @property
    def forbidden(self) -> tuple[Classification, ...]:
        return tuple(
            item for item in self.classifications if item.severity == SEVERITY_FORBIDDEN
        )

    @property
    def warnings(self) -> tuple[Classification, ...]:
        return tuple(
            item for item in self.classifications if item.severity == SEVERITY_WARNING
        )

    @property
    def exit_code(self) -> int:
        if self.error:
            return 2
        if self.forbidden:
            return 1
        return 0


FORBIDDEN_RULES: tuple[Rule, ...] = (
    Rule(
        "local_mtga_log",
        "Raw local MTGA logs must not be committed.",
        patterns=("data/match_logs/**",),
        filename_patterns=("Player.log", "Player-prev.log", "*.Player.log", "*.player.log"),
    ),
    Rule(
        "runtime_log",
        "Local runtime output must not be committed.",
        patterns=("data/runtime_logs/**",),
        filename_patterns=("*.runtime.log",),
    ),
    Rule(
        "runtime_status",
        "Runtime status snapshots are local generated state.",
        patterns=("data/status/**",),
    ),
    Rule(
        "failed_posts",
        "Failed webhook queues may contain private payloads.",
        patterns=("data/failed_posts/**",),
    ),
    Rule(
        "bad_events",
        "Local diagnostic captures may contain raw private data.",
        patterns=("data/bad_events/**",),
    ),
    Rule(
        "generated_card_data",
        "Generated or local card, deck, and tier data must not silently become source.",
        patterns=("data/oracle_data/**", "data/tier_sources/**", "data/decklists/**"),
    ),
    Rule(
        "raw_workbook_export",
        "Workbook exports are local artifacts unless an issue authorizes a fixture.",
        patterns=("data/workbook_exports/**", "workbook_exports/**", "exports/workbook/**"),
        filename_patterns=("*.xls", "*.xlsx", "*.xlsm"),
    ),
    Rule(
        "secret_file",
        "Obvious secret-bearing files must fail by path alone.",
        filename_patterns=(
            ".env",
            ".env.*",
            "*.pem",
            "*.key",
            "*.p12",
            "*.pfx",
            "id_rsa",
            "id_dsa",
            "credentials.json",
            "client_secret*.json",
            "token.json",
            "secrets.*",
        ),
    ),
    Rule(
        "webhook_api_credential",
        "Integration credential files must not be committed.",
        filename_patterns=("webhook_url*", "webhook*.secret", "api_key*"),
    ),
    Rule(
        "local_review_artifact",
        "Ignored local workflow artifacts must not be committed.",
        patterns=("_review_*/**", ".github/Mythic-Edge/**"),
    ),
)


PROTECTED_RULES: tuple[Rule, ...] = (
    Rule(
        "parser_event_classes",
        "Protected parser event surface; issue/contract must authorize this change.",
        patterns=("src/mythic_edge_parser/events.py",),
    ),
    Rule(
        "parser_state_final_reconciliation",
        "Protected parser state surface; issue/contract must authorize this change.",
        patterns=(
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/models.py",
        ),
    ),
    Rule(
        "extractor_behavior",
        "Protected extractor surface; issue/contract must authorize this change.",
        patterns=("src/mythic_edge_parser/app/extractors.py",),
    ),
    Rule(
        "match_game_identity",
        "Protected match/game identity surface; issue/contract must authorize this change.",
        patterns=(
            "src/mythic_edge_parser/app/gameplay_actions.py",
            "src/mythic_edge_parser/app/state.py",
            "src/mythic_edge_parser/app/transforms.py",
            "src/mythic_edge_parser/parsers/**",
        ),
    ),
    Rule(
        "workbook_schema",
        "Protected workbook-facing surface; issue/contract must authorize this change.",
        patterns=(
            "src/mythic_edge_parser/app/sheet_schema.py",
            "src/mythic_edge_parser/app/sheet_exports.py",
            "src/mythic_edge_parser/app/transforms.py",
        ),
    ),
    Rule(
        "webhook_payload_shape",
        "Protected webhook payload surface; issue/contract must authorize this change.",
        patterns=(
            "src/mythic_edge_parser/app/outputs.py",
            "src/mythic_edge_parser/app/runner.py",
            "src/mythic_edge_parser/app/transforms.py",
        ),
    ),
    Rule(
        "apps_script_behavior",
        "Protected Apps Script surface; issue/contract must authorize this change.",
        patterns=("tools/google_apps_script/**",),
    ),
    Rule(
        "environment_runtime_paths",
        "Protected environment/runtime path surface; issue/contract must authorize this change.",
        patterns=(
            ".github/workflows/**",
            "src/mythic_edge_parser/app/config.py",
            "tools/run_repo_checks.ps1",
            "tools/run_touched_file_checks.ps1",
        ),
    ),
    Rule(
        "workflow_authority_docs",
        "Protected workflow authority surface; issue/contract must authorize this change.",
        patterns=(
            ".github/ISSUE_TEMPLATE/**",
            ".github/pull_request_template.md",
            "docs/agent_constitution.md",
            "docs/agent_rules.yml",
            "docs/agent_threads/**",
            "docs/codex_module_workflow.md",
            "docs/templates/**",
        ),
    ),
)


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    text = text.lstrip("/")
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _matches_pattern(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        if any(marker in prefix for marker in "*?[]"):
            return fnmatch.fnmatchcase(path, pattern)
        return path == prefix or path.startswith(f"{prefix}/")
    return fnmatch.fnmatchcase(path, pattern)


def _matches_rule(path: str, rule: Rule) -> bool:
    name = path.rsplit("/", 1)[-1]
    return any(_matches_pattern(path, pattern) for pattern in rule.patterns) or any(
        fnmatch.fnmatchcase(name, pattern) for pattern in rule.filename_patterns
    )


def _is_documented_fixture(path: str) -> bool:
    return path.startswith("tests/fixtures/")


def _is_safe_env_example(path: str) -> bool:
    return path == ".env.example" or path.endswith("/.env.example")


def _is_token_credential_filename(path: str) -> bool:
    name = path.rsplit("/", 1)[-1].lower()
    stem, dot, extension = name.rpartition(".")
    if not dot:
        stem = name
        extension = ""
    credential_extensions = {"", "env", "json", "secret", "txt", "key", "pem", "yml", "yaml"}
    if extension not in credential_extensions:
        return False
    return (
        stem == "token"
        or stem.startswith("token_")
        or stem.startswith("token-")
        or stem.endswith("_token")
        or stem.endswith("-token")
        or "api_token" in stem
        or "access_token" in stem
        or "refresh_token" in stem
        or "auth_token" in stem
        or "webhook_token" in stem
    )


def classify_path(path: str | Path) -> Classification:
    normalized = normalize_path(path)

    for rule in FORBIDDEN_RULES:
        if rule.category_id == "secret_file" and _is_safe_env_example(normalized):
            continue
        if rule.category_id in {"local_mtga_log", "raw_workbook_export"} and _is_documented_fixture(
            normalized,
        ):
            continue
        if _matches_rule(normalized, rule):
            return Classification(
                normalized,
                SEVERITY_FORBIDDEN,
                rule.category_id,
                rule.reason,
            )

    if _is_token_credential_filename(normalized):
        return Classification(
            normalized,
            SEVERITY_FORBIDDEN,
            "webhook_api_credential",
            "Integration credential files must not be committed.",
        )

    for rule in PROTECTED_RULES:
        if _matches_rule(normalized, rule):
            return Classification(
                normalized,
                SEVERITY_WARNING,
                rule.category_id,
                rule.reason,
            )

    return Classification(
        normalized,
        SEVERITY_ALLOWED,
        "allowed",
        "No protected-surface classification.",
    )


def classify_paths(paths: Iterable[str | Path]) -> tuple[Classification, ...]:
    return tuple(classify_path(path) for path in paths)


def evaluate_paths(
    paths: Iterable[str | Path],
    *,
    base: str,
    head: str = "HEAD",
    error: str = "",
) -> GateResult:
    normalized_paths = tuple(normalize_path(path) for path in paths)
    return GateResult(
        base=base,
        head=head,
        changed_paths=normalized_paths,
        classifications=classify_paths(normalized_paths),
        error=error,
    )


def collect_changed_paths(base: str, *, repo_root: str | Path = ".") -> tuple[str, ...]:
    command = [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        f"{base}...HEAD",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(detail or f"git diff failed with exit code {completed.returncode}")
    return tuple(line for line in completed.stdout.splitlines() if line.strip())


def run_gate(base: str, *, repo_root: str | Path = ".") -> GateResult:
    try:
        changed_paths = collect_changed_paths(base, repo_root=repo_root)
    except RuntimeError as exc:
        return evaluate_paths((), base=base, error=str(exc))
    return evaluate_paths(changed_paths, base=base)


def render_report(result: GateResult) -> str:
    lines = [
        "Protected Surface Gate",
        f"base: {result.base}",
        f"head: {result.head}",
        f"changed_paths: {len(result.changed_paths)}",
        f"forbidden: {len(result.forbidden)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration {result.error}")
    else:
        for item in result.forbidden:
            lines.append(f"FORBIDDEN {item.category_id} {item.path} - {item.reason}")
        for item in result.warnings:
            lines.append(f"WARNING {item.category_id} {item.path} - {item.reason}")

    if lines[-1] != "":
        lines.append("")
    if result.error:
        lines.append("result: error")
    elif result.forbidden:
        lines.append("result: failed")
    else:
        lines.append("result: passed")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check protected-surface file diffs.")
    parser.add_argument("--base", required=True, help="Base git ref for <base>...HEAD.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths from stdin instead of running git diff.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.paths_from_stdin:
        result = evaluate_paths(sys.stdin.read().splitlines(), base=args.base)
    else:
        result = run_gate(args.base, repo_root=args.repo_root)

    output = render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
