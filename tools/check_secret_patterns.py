"""Content scanner for repo-local secret and private-marker patterns."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    from tools.check_secret_patterns_detectors import (
        _append_artifact_payload_findings,
        _append_credential_findings,
        _append_player_log_findings,
        _append_private_path_findings,
        _append_webhook_findings,
        _fixture_is_sanitized,
        _has_placeholder_context,
        _is_policy_path,
        _make_finding,
        _safe_excerpt,
        scan_text,
    )
    from tools.check_secret_patterns_models import (
        MODE_ALL,
        MODE_CHANGED,
        MODE_STDIN,
        RESULT_ERROR,
        RESULT_FAILED,
        RESULT_PASSED,
        RESULT_WARNING,
        SEVERITY_ALLOWED,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
        Finding,
        ScanResult,
    )
except ModuleNotFoundError:  # pragma: no cover - used when this file is run as a script.
    from check_secret_patterns_detectors import (
        _append_artifact_payload_findings,
        _append_credential_findings,
        _append_player_log_findings,
        _append_private_path_findings,
        _append_webhook_findings,
        _fixture_is_sanitized,
        _has_placeholder_context,
        _is_policy_path,
        _make_finding,
        _safe_excerpt,
        scan_text,
    )
    from check_secret_patterns_models import (
        MODE_ALL,
        MODE_CHANGED,
        MODE_STDIN,
        RESULT_ERROR,
        RESULT_FAILED,
        RESULT_PASSED,
        RESULT_WARNING,
        SEVERITY_ALLOWED,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
        Finding,
        ScanResult,
    )

MAX_SCAN_BYTES = 1_000_000

__all__ = (
    "Finding",
    "MODE_ALL",
    "MODE_CHANGED",
    "MODE_STDIN",
    "RESULT_ERROR",
    "RESULT_FAILED",
    "RESULT_PASSED",
    "RESULT_WARNING",
    "SEVERITY_ALLOWED",
    "SEVERITY_FORBIDDEN",
    "SEVERITY_WARNING",
    "ScanResult",
    "_append_artifact_payload_findings",
    "_append_credential_findings",
    "_append_player_log_findings",
    "_append_private_path_findings",
    "_append_webhook_findings",
    "_fixture_is_sanitized",
    "_has_placeholder_context",
    "_is_policy_path",
    "_make_finding",
    "_safe_excerpt",
    "build_parser",
    "collect_changed_paths",
    "collect_tracked_paths",
    "evaluate_paths",
    "main",
    "normalize_candidate_paths",
    "normalize_path",
    "render_report",
    "run_all_scan",
    "run_changed_scan",
    "scan_text",
)


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    while text.startswith("//"):
        text = text[1:]
    parts = [part for part in text.split("/") if part and part != "."]
    return "/".join(parts)


def _read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _is_binary(data: bytes) -> bool:
    if not data:
        return False
    if b"\0" in data[:4096]:
        return True
    sample = data[:4096]
    control = sum(1 for byte in sample if byte < 9 or (13 < byte < 32))
    return control / len(sample) > 0.30


def _repo_relative_path(raw_path: str | Path, repo_root: Path) -> str:
    text = str(raw_path).strip().replace("\\", "/")
    if not text:
        return ""
    candidate = Path(text)
    if candidate.is_absolute():
        resolved = candidate.resolve(strict=False)
    elif ".." not in Path(normalize_path(text)).parts:
        return normalize_path(text)
    else:
        resolved = (repo_root / normalize_path(text)).resolve(strict=False)
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise ValueError(f"path is outside repository root: {raw_path}") from exc


def normalize_candidate_paths(
    paths: Iterable[str | Path],
    *,
    repo_root: str | Path = ".",
    strict_outside_root: bool = False,
) -> tuple[tuple[str, ...], str]:
    root = Path(repo_root).resolve()
    normalized: set[str] = set()
    for raw_path in paths:
        try:
            relative = _repo_relative_path(raw_path, root)
        except ValueError as exc:
            if strict_outside_root:
                return (), str(exc)
            continue
        if relative:
            normalized.add(relative)
    return tuple(sorted(normalized)), ""


def collect_changed_paths(
    base: str,
    *,
    repo_root: str | Path = ".",
    head: str = "HEAD",
) -> tuple[str, ...]:
    command = [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        f"{base}...{head}",
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


def collect_tracked_paths(*, repo_root: str | Path = ".") -> tuple[str, ...]:
    command = ["git", "ls-files"]
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
        raise RuntimeError(detail or f"git ls-files failed with exit code {completed.returncode}")
    return tuple(line for line in completed.stdout.splitlines() if line.strip())


def _skip_finding(path: str, category_id: str, reason: str) -> Finding:
    return Finding(
        severity=SEVERITY_WARNING,
        category_id=category_id,
        path=path,
        line=0,
        reason=reason,
        excerpt=f"<redacted:{category_id}>",
        rule_id=category_id,
    )


def _scan_file(path: str, *, repo_root: Path) -> tuple[tuple[Finding, ...], bool, str]:
    absolute_path = repo_root / path
    if not absolute_path.exists():
        return (
            (
                _skip_finding(
                    path,
                    "ambiguous_private_marker",
                    "Path was selected for scanning but does not exist; skipped.",
                ),
            ),
            False,
            "",
        )
    try:
        if absolute_path.is_symlink():
            target = absolute_path.resolve(strict=True)
            try:
                target.relative_to(repo_root)
            except ValueError:
                return (), False, f"symlink resolves outside repository root: {path}"
    except OSError as exc:
        return (), False, str(exc)

    if not absolute_path.is_file():
        return (), False, ""

    try:
        data = _read_file_bytes(absolute_path)
    except OSError as exc:
        return (), False, str(exc)

    if _is_binary(data):
        return (
            (
                _skip_finding(
                    path,
                    "binary_skipped",
                    "Binary file was not content-scanned.",
                ),
            ),
            False,
            "",
        )
    if len(data) > MAX_SCAN_BYTES:
        return (
            (
                _skip_finding(
                    path,
                    "oversized_skipped",
                    f"Text file exceeds {MAX_SCAN_BYTES} byte scan limit.",
                ),
            ),
            False,
            "",
        )

    decode_warning: tuple[Finding, ...] = ()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("utf-8", errors="replace")
        decode_warning = (
            _skip_finding(
                path,
                "decode_replacement_used",
                "UTF-8 decoding used replacement characters before scanning.",
            ),
        )
    return decode_warning + scan_text(path, text), True, ""


def _sort_findings(findings: Iterable[Finding]) -> tuple[Finding, ...]:
    severity_order = {SEVERITY_FORBIDDEN: 0, SEVERITY_WARNING: 1, SEVERITY_ALLOWED: 2}
    return tuple(
        sorted(
            findings,
            key=lambda item: (
                severity_order.get(item.severity, 9),
                item.path,
                item.line,
                item.category_id,
                item.reason,
            ),
        ),
    )


def evaluate_paths(
    paths: Iterable[str | Path],
    *,
    base: str,
    repo_root: str | Path = ".",
    mode: str = MODE_STDIN,
    head: str = "HEAD",
    strict_outside_root: bool = False,
) -> ScanResult:
    root = Path(repo_root).resolve()
    normalized_paths, error = normalize_candidate_paths(
        paths,
        repo_root=root,
        strict_outside_root=strict_outside_root,
    )
    if error:
        return ScanResult(mode, base, head, (), (), (), error=error)

    findings: list[Finding] = []
    scanned_paths: list[str] = []
    skipped_paths: list[str] = []
    for path in normalized_paths:
        path_findings, scanned, scan_error = _scan_file(path, repo_root=root)
        if scan_error:
            return ScanResult(
                mode,
                base,
                head,
                tuple(scanned_paths),
                tuple(skipped_paths),
                _sort_findings(findings),
                error=scan_error,
            )
        if scanned:
            scanned_paths.append(path)
        else:
            skipped_paths.append(path)
        findings.extend(path_findings)

    return ScanResult(
        mode=mode,
        base=base,
        head=head,
        scanned_paths=tuple(scanned_paths),
        skipped_paths=tuple(skipped_paths),
        findings=_sort_findings(findings),
    )


def run_changed_scan(base: str, *, repo_root: str | Path = ".") -> ScanResult:
    try:
        paths = collect_changed_paths(base, repo_root=repo_root)
    except RuntimeError as exc:
        return ScanResult(MODE_CHANGED, base, "HEAD", (), (), (), error=str(exc))
    return evaluate_paths(paths, base=base, repo_root=repo_root, mode=MODE_CHANGED)


def run_all_scan(*, repo_root: str | Path = ".", base: str = "<not-required>") -> ScanResult:
    try:
        paths = collect_tracked_paths(repo_root=repo_root)
    except RuntimeError as exc:
        return ScanResult(MODE_ALL, base, "HEAD", (), (), (), error=str(exc))
    return evaluate_paths(paths, base=base, repo_root=repo_root, mode=MODE_ALL)


def render_report(result: ScanResult) -> str:
    lines = [
        "Secret / Private Marker Scan",
        f"mode: {result.mode}",
        f"base: {result.base}",
        f"head: {result.head}",
        f"scanned_paths: {len(result.scanned_paths)}",
        f"skipped_paths: {len(result.skipped_paths)}",
        f"forbidden: {len(result.forbidden)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration {result.error}")
    else:
        for finding in result.findings:
            if finding.severity not in {SEVERITY_FORBIDDEN, SEVERITY_WARNING}:
                continue
            label = "FORBIDDEN" if finding.severity == SEVERITY_FORBIDDEN else "WARNING"
            lines.append(
                f"{label} {finding.category_id} {finding.path}:{finding.line} - "
                f"{finding.reason} [excerpt: {finding.excerpt}]",
            )

    if lines[-1] != "":
        lines.append("")
    lines.append(f"result: {result.result}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan repository text for secret/private markers.")
    parser.add_argument("--base", help="Base git ref for <base>...HEAD.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--paths-from-stdin",
        action="store_true",
        help="Read newline-delimited paths from stdin instead of running git diff.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all tracked files in advisory/report-only mode.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2

    if args.paths_from_stdin and args.all:
        print("--paths-from-stdin and --all cannot be used together", file=sys.stderr)
        return 2
    if not args.all and not args.base:
        print("--base is required unless --all is supplied", file=sys.stderr)
        return 2

    if args.all:
        result = run_all_scan(repo_root=args.repo_root, base=args.base or "<not-required>")
    elif args.paths_from_stdin:
        result = evaluate_paths(
            sys.stdin.read().splitlines(),
            base=args.base,
            repo_root=args.repo_root,
            mode=MODE_STDIN,
            strict_outside_root=True,
        )
    else:
        result = run_changed_scan(args.base, repo_root=args.repo_root)

    output = render_report(result)
    stream = sys.stderr if result.error else sys.stdout
    print(output, file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
