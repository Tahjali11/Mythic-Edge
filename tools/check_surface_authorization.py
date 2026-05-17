"""Advisory authorization evidence checker for protected-surface changes."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

MODE_CHANGED = "changed-files"
MODE_STDIN = "paths-from-stdin"

AUTHORIZATION_STATUS_OK = "ok"
AUTHORIZATION_STATUS_REVIEW = "review"
AUTHORIZATION_STATUS_ERROR = "error"

CATEGORY_AUTHORIZED = "AUTHORIZED"
CATEGORY_MISSING = "MISSING_AUTHORIZATION"
CATEGORY_FORBIDDEN = "FORBIDDEN_PATH"
CATEGORY_NOT_PROTECTED = "NOT_PROTECTED"
CATEGORY_UNVERIFIABLE = "UNVERIFIABLE_SOURCE"
CATEGORY_SCOPE_WARNING = "SCOPE_WARNING"

SOURCE_KINDS = ("issue", "contract", "handoff", "report", "pr", "generic")
SOURCE_KIND_ORDER = {kind: index for index, kind in enumerate(SOURCE_KINDS)}

ACCEPTED_MARKERS = (
    "authorized",
    "explicitly authorized",
    "authorized drift",
    "accepted drift",
    "contract authorizes",
    "issue authorizes",
    "scope includes",
    "in scope",
    "allowed change",
    "allowed protected surface",
)

REJECTED_EVIDENCE_PHRASES = (
    "all protected surfaces authorized",
    "parser downstream surfaces",
    "protected surfaces unchanged or authorized",
    "workbook schema unchanged or authorized",
    "webhook payload shape unchanged or authorized",
    "do not change workbook schema",
    "do not change parser behavior",
    "not authorized",
    "not explicitly authorized",
    "not in scope",
    "out of scope",
    "outside scope",
    "no drift",
)

PROTECTED_CATEGORY_ALIASES: dict[str, tuple[str, ...]] = {
    "parser_event_classes": (
        "parser_event_classes",
        "parser event classes",
        "event class shape",
        "parser event surface",
    ),
    "parser_state_final_reconciliation": (
        "parser_state_final_reconciliation",
        "parser state final reconciliation",
        "final reconciliation",
        "parser state surface",
    ),
    "extractor_behavior": (
        "extractor_behavior",
        "extractor behavior",
        "extractor surface",
    ),
    "match_game_identity": (
        "match_game_identity",
        "match/game identity",
        "match identity",
        "game identity",
        "deduplication",
        "match/game identity and deduplication",
    ),
    "workbook_schema": (
        "workbook_schema",
        "workbook schema",
        "sheet schema",
        "workbook-facing row shape",
        "workbook exports",
    ),
    "webhook_payload_shape": (
        "webhook_payload_shape",
        "webhook payload shape",
        "webhook shape",
        "output payload shape",
    ),
    "apps_script_behavior": (
        "apps_script_behavior",
        "Apps Script behavior",
        "deployed Apps Script",
        "Apps Script receiver behavior",
    ),
    "environment_runtime_paths": (
        "environment_runtime_paths",
        "environment variables",
        "runtime paths",
        "environment/runtime path surface",
        "CI behavior",
    ),
    "workflow_authority_docs": (
        "workflow_authority_docs",
        "workflow authority docs",
        "agent docs",
        "workflow docs",
        "validation gates",
        "branch policy",
        "issue lifecycle",
        "PR lifecycle",
    ),
}

@dataclass(frozen=True)
class AuthorizationSource:
    kind: str
    path: str
    text: str


@dataclass(frozen=True)
class Evidence:
    category_id: str
    source_kind: str
    source_path: str
    excerpt: str


@dataclass(frozen=True)
class AuthorizationFinding:
    category_id: str
    path: str
    evidence: Evidence


@dataclass(frozen=True)
class MissingAuthorization:
    category_id: str
    path: str
    reason: str


@dataclass(frozen=True)
class UnverifiableSource:
    category_id: str
    path: str
    reason: str


@dataclass(frozen=True)
class ScopeWarning:
    category_id: str
    source_kind: str
    source_path: str
    reason: str
    excerpt: str


@dataclass(frozen=True)
class AuthorizationCheckResult:
    mode: str
    base: str
    head: str
    changed_paths: tuple[str, ...]
    classifications: tuple[object, ...]
    authorization_sources: tuple[AuthorizationSource, ...]
    authorized: tuple[AuthorizationFinding, ...]
    missing_authorization: tuple[MissingAuthorization, ...]
    forbidden_paths: tuple[object, ...]
    not_protected: tuple[object, ...]
    unverifiable_sources: tuple[UnverifiableSource, ...]
    scope_warnings: tuple[ScopeWarning, ...]
    error: str = ""

    @property
    def protected(self) -> tuple[object, ...]:
        gate = _load_protected_surface_gate()
        return tuple(
            item
            for item in self.classifications
            if getattr(item, "severity") == gate.SEVERITY_WARNING
        )

    @property
    def authorization_status(self) -> str:
        if self.error:
            return AUTHORIZATION_STATUS_ERROR
        if (
            self.missing_authorization
            or self.forbidden_paths
            or self.unverifiable_sources
            or self.scope_warnings
        ):
            return AUTHORIZATION_STATUS_REVIEW
        return AUTHORIZATION_STATUS_OK

    @property
    def exit_code(self) -> int:
        return 2 if self.error else 0


@lru_cache(maxsize=1)
def _load_protected_surface_gate():
    module_path = Path(__file__).with_name("check_protected_surfaces.py")
    module_name = "check_protected_surfaces_for_authorization"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load tools/check_protected_surfaces.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _normalize_for_match(text: str) -> str:
    lowered = text.casefold()
    lowered = re.sub(r"[_/\-]+", " ", lowered)
    lowered = re.sub(r"[`*_:\[\](),.;]+", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


_NORMALIZED_ALIASES = {
    category: tuple(_normalize_for_match(alias) for alias in aliases)
    for category, aliases in PROTECTED_CATEGORY_ALIASES.items()
}
_NORMALIZED_MARKERS = tuple(_normalize_for_match(marker) for marker in ACCEPTED_MARKERS)
_NORMALIZED_REJECTED_PHRASES = tuple(
    _normalize_for_match(phrase) for phrase in REJECTED_EVIDENCE_PHRASES
)


def _contains_phrase(normalized_text: str, normalized_phrase: str) -> bool:
    return f" {normalized_phrase} " in f" {normalized_text} "


def _collapse_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _iter_evidence_blocks(text: str) -> tuple[str, ...]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks: list[str] = []
    for line in normalized.splitlines():
        collapsed = _collapse_text(line)
        if collapsed:
            blocks.append(collapsed)
    for paragraph in re.split(r"\n\s*\n", normalized):
        collapsed = _collapse_text(paragraph)
        paragraph_lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
        if any(line.startswith(("-", "*", "|")) for line in paragraph_lines):
            continue
        if collapsed and "\n" in paragraph.strip():
            blocks.append(collapsed)
    return tuple(dict.fromkeys(blocks))


def _categories_in_block(normalized_block: str) -> tuple[str, ...]:
    categories = {
        category
        for category, aliases in _NORMALIZED_ALIASES.items()
        if any(_contains_phrase(normalized_block, alias) for alias in aliases)
    }
    return tuple(sorted(categories))


def _has_marker(normalized_block: str) -> bool:
    return any(_contains_phrase(normalized_block, marker) for marker in _NORMALIZED_MARKERS)


def _has_rejected_evidence(normalized_block: str) -> bool:
    if normalized_block in {"n a", "na"}:
        return True
    if (
        normalized_block.startswith("authorized ")
        and not normalized_block.startswith(("authorized drift", "authorized protected surfaces"))
        and _categories_in_block(normalized_block)
    ):
        return True
    return any(
        _contains_phrase(normalized_block, phrase)
        for phrase in _NORMALIZED_REJECTED_PHRASES
    )


def _mentions_broad_protected_surface(normalized_block: str) -> bool:
    return (
        _contains_phrase(normalized_block, "protected surfaces")
        or _contains_phrase(normalized_block, "protected surface")
    )


def _has_required_citation(block: str) -> bool:
    return bool(
        re.search(r"#\d+\b", block)
        or re.search(r"https?://", block)
        or "docs/contracts/" in block
        or "docs/implementation_handoffs/" in block
        or "docs/contract_test_reports/" in block
    )


def _source_needs_citation(source_kind: str) -> bool:
    return source_kind in {"pr", "generic"}


def _scope_warning(
    *,
    category_id: str,
    source: AuthorizationSource,
    reason: str,
    block: str,
) -> ScopeWarning:
    return ScopeWarning(
        category_id,
        source.kind,
        source.path,
        reason,
        block,
    )


def _dedupe_scope_warnings(warnings: Iterable[ScopeWarning]) -> tuple[ScopeWarning, ...]:
    return tuple(
        sorted(
            dict.fromkeys(warnings),
            key=lambda item: (
                item.category_id,
                SOURCE_KIND_ORDER[item.source_kind],
                item.source_path,
                item.reason,
                item.excerpt,
            ),
        ),
    )


def _select_primary_evidence(items: Iterable[Evidence]) -> Evidence:
    return sorted(
        items,
        key=lambda item: (
            SOURCE_KIND_ORDER[item.source_kind],
            item.source_path,
            item.excerpt,
        ),
    )[0]


def _display_source_path(raw_path: str, resolved_path: Path, repo_root: Path) -> str:
    try:
        return resolved_path.resolve(strict=False).relative_to(repo_root).as_posix()
    except ValueError:
        return raw_path.replace("\\", "/")


def _parse_authorization_file_arg(raw_arg: str) -> tuple[str, str]:
    kind, separator, raw_path = raw_arg.partition("=")
    kind = kind.strip()
    raw_path = raw_path.strip()
    if not separator or not kind or not raw_path:
        raise ValueError(f"invalid --authorization-file syntax: {raw_arg}")
    if kind not in SOURCE_KINDS:
        raise ValueError(f"unknown authorization source kind: {kind}")
    return kind, raw_path


def read_authorization_sources(
    authorization_file_args: Iterable[str],
    *,
    repo_root: str | Path = ".",
) -> tuple[tuple[AuthorizationSource, ...], str]:
    root = Path(repo_root).resolve()
    sources: list[AuthorizationSource] = []
    seen: set[tuple[str, str]] = set()
    try:
        parsed_args = [_parse_authorization_file_arg(raw_arg) for raw_arg in authorization_file_args]
    except ValueError as exc:
        return (), str(exc)

    for kind, raw_path in parsed_args:
        source_path = Path(raw_path)
        resolved_path = source_path if source_path.is_absolute() else root / source_path
        display_path = _display_source_path(raw_path, resolved_path, root)
        dedupe_key = (kind, display_path)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        try:
            text = resolved_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            return (), f"unable to read authorization source {kind}={display_path}: {exc}"
        sources.append(AuthorizationSource(kind, display_path, text))

    return (
        tuple(
            sorted(
                sources,
                key=lambda item: (SOURCE_KIND_ORDER[item.kind], item.path),
            ),
        ),
        "",
    )


def _find_authorization_evidence(
    protected_categories: tuple[str, ...],
    sources: tuple[AuthorizationSource, ...],
) -> tuple[dict[str, Evidence], tuple[ScopeWarning, ...]]:
    evidence_by_category: dict[str, list[Evidence]] = {
        category: [] for category in protected_categories
    }
    scope_warnings: list[ScopeWarning] = []
    mismatched_blocks: list[tuple[AuthorizationSource, str, tuple[str, ...]]] = []

    for source in sources:
        for block in _iter_evidence_blocks(source.text):
            normalized_block = _normalize_for_match(block)
            mentioned_categories = _categories_in_block(normalized_block)
            touched_mentions = tuple(
                category for category in mentioned_categories if category in protected_categories
            )
            has_marker = _has_marker(normalized_block)
            has_rejected = _has_rejected_evidence(normalized_block)
            mentions_broad_surface = _mentions_broad_protected_surface(normalized_block)

            if has_rejected and (touched_mentions or mentions_broad_surface):
                warning_categories = touched_mentions or protected_categories
                for category in warning_categories:
                    scope_warnings.append(
                        _scope_warning(
                            category_id=category,
                            source=source,
                            reason="Rejected or weak authorization wording.",
                            block=block,
                        ),
                    )
                continue

            if has_marker and mentions_broad_surface and not mentioned_categories:
                for category in protected_categories:
                    scope_warnings.append(
                        _scope_warning(
                            category_id=category,
                            source=source,
                            reason="Authorization wording is broad and not category-specific.",
                            block=block,
                        ),
                    )
                continue

            if has_marker and mentioned_categories and not touched_mentions:
                mismatched_blocks.append((source, block, mentioned_categories))
                continue

            if not has_marker:
                continue

            for category in touched_mentions:
                if _source_needs_citation(source.kind) and not _has_required_citation(block):
                    scope_warnings.append(
                        _scope_warning(
                            category_id=category,
                            source=source,
                            reason="PR or generic authorization evidence lacks a citation.",
                            block=block,
                        ),
                    )
                    continue
                evidence_by_category[category].append(
                    Evidence(category, source.kind, source.path, block),
                )

    primary_evidence = {
        category: _select_primary_evidence(items)
        for category, items in evidence_by_category.items()
        if items
    }

    for source, block, mentioned_categories in mismatched_blocks:
        for category in protected_categories:
            if category in primary_evidence:
                continue
            scope_warnings.append(
                _scope_warning(
                    category_id=category,
                    source=source,
                    reason=(
                        "Authorization evidence names a different protected category: "
                        f"{', '.join(mentioned_categories)}."
                    ),
                    block=block,
                ),
            )

    return primary_evidence, _dedupe_scope_warnings(scope_warnings)


def _normalize_paths(paths: Iterable[str | Path]) -> tuple[str, ...]:
    gate = _load_protected_surface_gate()
    normalized = {gate.normalize_path(path) for path in paths}
    return tuple(sorted(path for path in normalized if path))


def _error_result(
    *,
    mode: str,
    base: str,
    error: str,
) -> AuthorizationCheckResult:
    return AuthorizationCheckResult(
        mode=mode,
        base=base,
        head="HEAD",
        changed_paths=(),
        classifications=(),
        authorization_sources=(),
        authorized=(),
        missing_authorization=(),
        forbidden_paths=(),
        not_protected=(),
        unverifiable_sources=(),
        scope_warnings=(),
        error=error,
    )


def run_authorization_check(
    base: str,
    *,
    repo_root: str | Path = ".",
    paths: Iterable[str | Path] | None = None,
    authorization_file_args: Iterable[str] = (),
    mode: str = MODE_CHANGED,
) -> AuthorizationCheckResult:
    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        return _error_result(
            mode=mode,
            base=base,
            error=f"invalid repository root: {repo_root}",
        )

    sources, source_error = read_authorization_sources(
        authorization_file_args,
        repo_root=root,
    )
    if source_error:
        return _error_result(mode=mode, base=base, error=source_error)

    gate = _load_protected_surface_gate()
    if paths is None:
        try:
            raw_paths = gate.collect_changed_paths(base, repo_root=root)
        except RuntimeError as exc:
            return _error_result(mode=mode, base=base, error=str(exc))
    else:
        raw_paths = tuple(paths)

    changed_paths = _normalize_paths(raw_paths)
    classifications = gate.classify_paths(changed_paths)
    protected = tuple(
        item for item in classifications if item.severity == gate.SEVERITY_WARNING
    )
    forbidden = tuple(
        item for item in classifications if item.severity == gate.SEVERITY_FORBIDDEN
    )
    not_protected = tuple(
        item for item in classifications if item.severity == gate.SEVERITY_ALLOWED
    )
    protected_categories = tuple(sorted({item.category_id for item in protected}))

    evidence_by_category, scope_warnings = _find_authorization_evidence(
        protected_categories,
        sources,
    )

    authorized: list[AuthorizationFinding] = []
    missing: list[MissingAuthorization] = []
    unverifiable: list[UnverifiableSource] = []
    for item in protected:
        evidence = evidence_by_category.get(item.category_id)
        if evidence is None:
            missing.append(
                MissingAuthorization(
                    item.category_id,
                    item.path,
                    "No accepted category-specific authorization evidence found.",
                ),
            )
            if not sources:
                unverifiable.append(
                    UnverifiableSource(
                        item.category_id,
                        item.path,
                        "No authorization source supplied.",
                    ),
                )
            continue
        authorized.append(
            AuthorizationFinding(
                item.category_id,
                item.path,
                evidence,
            ),
        )

    return AuthorizationCheckResult(
        mode=mode,
        base=base,
        head="HEAD",
        changed_paths=changed_paths,
        classifications=classifications,
        authorization_sources=sources,
        authorized=tuple(authorized),
        missing_authorization=tuple(missing),
        forbidden_paths=forbidden,
        not_protected=not_protected,
        unverifiable_sources=tuple(unverifiable),
        scope_warnings=scope_warnings,
    )


def _classification_dict(item: object) -> dict[str, str]:
    return {
        "path": str(getattr(item, "path")),
        "severity": str(getattr(item, "severity")),
        "category_id": str(getattr(item, "category_id")),
        "reason": str(getattr(item, "reason")),
    }


def render_json(result: AuthorizationCheckResult) -> str:
    return json.dumps(
        {
            "mode": result.mode,
            "base": result.base,
            "head": result.head,
            "changed_paths": list(result.changed_paths),
            "classifications": [_classification_dict(item) for item in result.classifications],
            "authorization_sources": [
                {"kind": item.kind, "path": item.path} for item in result.authorization_sources
            ],
            "authorized": [asdict(item) for item in result.authorized],
            "missing_authorization": [
                asdict(item) for item in result.missing_authorization
            ],
            "forbidden_paths": [
                _classification_dict(item) for item in result.forbidden_paths
            ],
            "not_protected": [_classification_dict(item) for item in result.not_protected],
            "unverifiable_sources": [
                asdict(item) for item in result.unverifiable_sources
            ],
            "scope_warnings": [asdict(item) for item in result.scope_warnings],
            "authorization_status": result.authorization_status,
        },
        indent=2,
        sort_keys=True,
    )


def render_report(result: AuthorizationCheckResult) -> str:
    lines = [
        "Protected Surface Authorization Check",
        f"mode: {result.mode}",
        f"base: {result.base}",
        f"head: {result.head}",
        f"changed_paths: {len(result.changed_paths)}",
        f"protected: {len(result.protected)}",
        f"forbidden: {len(result.forbidden_paths)}",
        f"authorized: {len(result.authorized)}",
        f"missing_authorization: {len(result.missing_authorization)}",
        f"scope_warnings: {len(result.scope_warnings)}",
        f"unverifiable_sources: {len(result.unverifiable_sources)}",
        "",
    ]

    if result.error:
        lines.append(f"ERROR configuration - {result.error}")
    else:
        for item in result.authorized:
            lines.append(f"{CATEGORY_AUTHORIZED} {item.category_id} {item.path}")
            lines.append(
                "evidence: "
                f"{item.evidence.source_kind}={item.evidence.source_path} - "
                f"{item.evidence.excerpt}",
            )
            lines.append("")
        for item in result.missing_authorization:
            lines.append(
                f"{CATEGORY_MISSING} {item.category_id} {item.path} - {item.reason}",
            )
        for item in result.forbidden_paths:
            lines.append(
                f"{CATEGORY_FORBIDDEN} {item.category_id} {item.path} - "
                "Forbidden path cannot be authorized by ordinary workflow text.",
            )
        for item in result.not_protected:
            lines.append(f"{CATEGORY_NOT_PROTECTED} {item.category_id} {item.path}")
        for item in result.unverifiable_sources:
            lines.append(
                f"{CATEGORY_UNVERIFIABLE} {item.category_id} {item.path} - {item.reason}",
            )
        for item in result.scope_warnings:
            lines.append(
                f"{CATEGORY_SCOPE_WARNING} {item.category_id} "
                f"{item.source_kind}={item.source_path} - {item.reason}",
            )
            lines.append(f"evidence: {item.excerpt}")

    if lines[-1] != "":
        lines.append("")
    lines.append(f"authorization_status: {result.authorization_status}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check explicit authorization evidence for protected-surface changes.",
    )
    parser.add_argument("--base", required=True, help="Base git ref for <base>...HEAD.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths from stdin instead of running git diff.",
    )
    parser.add_argument(
        "--authorization-file",
        action="append",
        default=[],
        help="Repeatable authorization source in kind=path form.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Report format.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.paths_from_stdin:
        result = run_authorization_check(
            args.base,
            repo_root=args.repo_root,
            paths=sys.stdin.read().splitlines(),
            authorization_file_args=args.authorization_file,
            mode=MODE_STDIN,
        )
    else:
        result = run_authorization_check(
            args.base,
            repo_root=args.repo_root,
            authorization_file_args=args.authorization_file,
            mode=MODE_CHANGED,
        )

    output = render_json(result) if args.format == "json" else render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
