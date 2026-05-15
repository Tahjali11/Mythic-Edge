"""Content-based secret scanner for high-confidence Mythic Edge leaks."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PLACEHOLDER_MARKERS = (
    "example",
    "placeholder",
    "replace",
    "redacted",
    "dummy",
    "test",
    "fake",
    "secret-value",
    "supersecret",
)

SKIP_PATH_PREFIXES = (
    ".git/",
    ".venv/",
    "__pycache__/",
    ".pytest_cache/",
    ".ruff_cache/",
    "_review_",
    ".github/Mythic-Edge/",
    "data/match_logs/",
    "data/runtime_logs/",
    "data/status/",
    "data/failed_posts/",
    "data/bad_events/",
    "data/oracle_data/",
    "data/decklists/",
)

SECRET_PATTERNS = (
    (
        "openai_api_key",
        re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
        "Possible OpenAI API key.",
    ),
    (
        "google_apps_script_webhook",
        re.compile(r"https://script\.google\.com/macros/s/([^/\"'<>\s]+)/exec"),
        "Possible Google Apps Script webhook URL.",
    ),
    (
        "bearer_token",
        re.compile(r"\bBearer\s+[A-Za-z0-9._-]{24,}\b"),
        "Possible bearer token.",
    ),
    (
        "assigned_secret",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|webhook[_-]?url|sheets[_-]?webhook)"
            r"\s*[:=]\s*[\"']?(https?://[^\"'\s#]+|sk-(?:proj-)?[A-Za-z0-9_-]{20,}|[A-Za-z0-9_-]{32,})",
        ),
        "Possible assigned secret value.",
    ),
)


@dataclass(frozen=True)
class Finding:
    path: str
    line_number: int
    category_id: str
    message: str


def normalize_path(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    return text.lstrip("/")


def _is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def _should_skip(path: str) -> bool:
    normalized = normalize_path(path)
    return any(normalized.startswith(prefix) for prefix in SKIP_PATH_PREFIXES)


def _candidate_files_all(repo_root: Path) -> tuple[str, ...]:
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git ls-files failed")
    return tuple(path for path in completed.stdout.splitlines() if path.strip())


def _candidate_files_changed(repo_root: Path, base: str) -> tuple[str, ...]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base}...HEAD"],
        cwd=repo_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"git diff failed for base {base}")
    return tuple(path for path in completed.stdout.splitlines() if path.strip())


def _read_text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="ignore")


def scan_file(repo_root: Path, relative_path: str) -> list[Finding]:
    normalized = normalize_path(relative_path)
    if _should_skip(normalized):
        return []
    text = _read_text(repo_root.joinpath(normalized))
    if text is None:
        return []

    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category_id, pattern, message in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                candidate = match.group(1) if match.groups() else match.group(0)
                if _is_placeholder(candidate) or _is_placeholder(line):
                    continue
                findings.append(Finding(normalized, line_number, category_id, message))
    return findings


def scan_paths(repo_root: Path, paths: tuple[str, ...]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        findings.extend(scan_file(repo_root, path))
    return findings


def render_report(findings: list[Finding]) -> str:
    lines = ["Secret Pattern Check", f"findings: {len(findings)}"]
    for finding in findings:
        lines.append(f"ERROR {finding.category_id} {finding.path}:{finding.line_number} - {finding.message}")
    lines.append("result: failed" if findings else "result: passed")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan tracked or changed files for high-confidence secrets.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--base", default="origin/main", help="Base ref used with --changed.")
    parser.add_argument("--all", action="store_true", help="Scan all tracked files.")
    parser.add_argument("--changed", action="store_true", help="Scan files changed against --base.")
    parser.add_argument("--paths-from-stdin", action="store_true", help="Read paths from stdin.")
    parser.add_argument("--paths", nargs="*", default=(), help="Explicit paths to scan.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    try:
        if args.all:
            paths = _candidate_files_all(repo_root)
        elif args.changed:
            paths = _candidate_files_changed(repo_root, args.base)
        elif args.paths_from_stdin:
            paths = tuple(line.strip() for line in sys.stdin if line.strip())
        else:
            paths = tuple(args.paths)
        findings = scan_paths(repo_root, tuple(normalize_path(path) for path in paths))
    except RuntimeError as exc:
        print(f"Secret Pattern Check\nerror: {exc}\nresult: error")
        return 2

    print(render_report(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
