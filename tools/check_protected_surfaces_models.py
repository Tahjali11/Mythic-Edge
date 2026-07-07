"""Shared models, rules, and vocabulary for the protected-surface gate."""

from __future__ import annotations

from dataclasses import dataclass

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
        filename_patterns=(
            "Player.log",
            "Player-prev.log",
            "*.Player.log",
            "*.player.log",
        ),
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
        "failed" "_posts",
        "Failed web" "hook queues may contain private payloads.",
        patterns=("data/failed" "_posts/**",),
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
        "raw_workbook" "_export",
        "Work" "book exports are local artifacts unless an issue authorizes a fixture.",
        patterns=(
            "data/workbook" "_exports/**",
            "workbook" "_exports/**",
            "exports/work" "book/**",
        ),
        filename_patterns=("*." + "xls", "*." + "xlsx", "*." + "xlsm"),
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
