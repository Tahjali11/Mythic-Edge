#!/usr/bin/env python3
"""Regenerate the frozen fallback bundle through the old-workflow ingress."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from check_fallback_pickup import validate_fallback_pickup_bundle
from pool_test_fixtures import (
    FALLBACK_SOURCE_ARTIFACT,
    NOW,
    NOW_TEXT,
    OLD_WORKFLOW_INGRESS,
    OLD_WORKFLOW_SKILL,
    fallback_injection,
    old_workflow_prompt,
)


SKILL_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = SKILL_ROOT / "references" / "fallback-pickup-fixture"


class DuplicateKeyError(ValueError):
    pass


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _pretty_bytes(value: object) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("utf-8")


def _load_strict(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain one JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Regenerate the typed fallback fixture and require the pickup to be "
            "created by the independently hash-bound old-workflow ingress."
        )
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace the existing frozen prompt, injection, and pickup bundle.",
    )
    args = parser.parse_args(argv)
    if not args.replace and any(
        (FIXTURE_ROOT / name).exists()
        for name in ("prompt.json", "injection.json", "pickup.json")
    ):
        print("refusing to replace the frozen fixture without --replace", file=sys.stderr)
        return 2

    prompt = old_workflow_prompt()
    injection = fallback_injection(prompt)
    FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fallback-fixture-", dir=FIXTURE_ROOT) as temporary:
        staging = Path(temporary)
        prompt_path = staging / "prompt.json"
        injection_path = staging / "injection.json"
        pickup_path = staging / "pickup.json"
        prompt_path.write_bytes(_pretty_bytes(prompt))
        injection_path.write_bytes(_pretty_bytes(injection))
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(OLD_WORKFLOW_INGRESS),
                str(injection_path),
                "--prompt",
                str(prompt_path),
                "--source-artifact",
                str(FALLBACK_SOURCE_ARTIFACT),
                "--output",
                str(pickup_path),
                "--now",
                NOW_TEXT,
            ],
            cwd=SKILL_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if completed.returncode != 0:
            print("old-workflow pickup producer rejected the bundle", file=sys.stderr)
            return 1
        pickup = _load_strict(pickup_path)
        errors = validate_fallback_pickup_bundle(
            prompt=prompt,
            injection=injection,
            pickup=pickup,
            workflow_skill=OLD_WORKFLOW_SKILL,
            pickup_producer=OLD_WORKFLOW_INGRESS,
            source_artifact=FALLBACK_SOURCE_ARTIFACT,
            now=NOW,
        )
        if errors:
            print("generated fallback bundle failed strict validation", file=sys.stderr)
            return 1
        for name in ("prompt.json", "injection.json", "pickup.json"):
            os.replace(staging / name, FIXTURE_ROOT / name)

    for name in ("prompt.json", "injection.json", "pickup.json"):
        payload = (FIXTURE_ROOT / name).read_bytes()
        print(f"{name} {len(payload)} {hashlib.sha256(payload).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
