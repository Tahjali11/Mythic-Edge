#!/usr/bin/env python3
"""Strictly verify a Role Pool fallback injection and independent pickup receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from check_pool_plan import FALLBACK_CONDITION_IDS


PROMPT_SCHEMA = "mythic_edge_old_workflow_prompt.v1"
INJECTION_SCHEMA = "mythic_edge_role_pool_fallback_injection.v1"
PICKUP_SCHEMA = "mythic_edge_old_workflow_pickup.v1"
CONSUMER_ID = "mythic-edge-workflow"
CONSUMER_CONTRACT_REF = "skill:mythic-edge-workflow/SKILL.md"
CONSUMER_INGRESS_REF = (
    "skill:mythic-edge-workflow/scripts/accept_fallback_prompt.py"
)
OLD_WORKFLOW_MODE = "one_issue_one_role_old_workflow"
ALLOWED_ROLES = {"Codex A", "Codex B", "Codex D", "Codex E", "Codex F", "Codex G"}
MAX_PICKUP_DELAY = timedelta(minutes=5)
EXPECTED_WORKFLOW_ROOT = Path(__file__).resolve().parents[2] / CONSUMER_ID
ROLE_POOL_ROOT = Path(__file__).resolve().parents[1]
PROMPT_KEYS = {
    "schema_version",
    "route_id",
    "prompt_ref",
    "created_at",
    "lane_id",
    "repository_id",
    "issue",
    "role",
    "mode",
    "fallback_condition",
    "source_artifact_ref",
    "source_artifact_sha256",
    "dispatch_authorized",
    "mutation_authorized",
    "raw_content_included",
    "digest",
}
INJECTION_KEYS = {
    "schema_version",
    "injection_id",
    "receipt_ref",
    "injected_at",
    "status",
    "fallback_condition",
    "route_id",
    "route_receipt_ref",
    "lane_id",
    "repository_id",
    "issue",
    "role",
    "mode",
    "prompt_ref",
    "prompt_sha256",
    "consumer_id",
    "consumer_contract_ref",
    "consumer_contract_sha256",
    "consumer_ingress_ref",
    "consumer_ingress_sha256",
    "task_created",
    "agent_launched",
    "mutation_performed",
    "digest",
}
PICKUP_KEYS = {
    "schema_version",
    "pickup_id",
    "receipt_ref",
    "picked_up_at",
    "pickup_kind",
    "pickup_status",
    "consumer_id",
    "consumer_contract_ref",
    "consumer_contract_sha256",
    "consumer_ingress_ref",
    "consumer_ingress_sha256",
    "injection_ref",
    "injection_sha256",
    "fallback_condition",
    "route_id",
    "route_receipt_ref",
    "lane_id",
    "repository_id",
    "issue",
    "role",
    "mode",
    "prompt_ref",
    "prompt_sha256",
    "task_created",
    "agent_launched",
    "mutation_performed",
    "digest",
}
PROMPT_INJECTION_BINDINGS = (
    "route_id",
    "lane_id",
    "repository_id",
    "issue",
    "role",
    "mode",
    "fallback_condition",
    "prompt_ref",
)
INJECTION_PICKUP_BINDINGS = (
    "fallback_condition",
    "route_id",
    "route_receipt_ref",
    "lane_id",
    "repository_id",
    "issue",
    "role",
    "mode",
    "prompt_ref",
    "prompt_sha256",
    "consumer_id",
    "consumer_contract_ref",
    "consumer_contract_sha256",
    "consumer_ingress_ref",
    "consumer_ingress_sha256",
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
REPOSITORY_RE = re.compile(r"^[a-z0-9_.-]+/[a-z0-9_.-]+$")
REFERENCE_RE = re.compile(
    r"^[a-z][a-z0-9_-]{0,31}:[A-Za-z0-9._/#-]{1,255}$"
)


def canonical_payload_digest(document: dict[str, Any]) -> str:
    """Hash canonical JSON after removing the document's self-digest field."""

    payload = {key: value for key, value in document.items() if key != "digest"}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def with_digest(document: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy with its canonical self-digest populated."""

    result = dict(document)
    result.pop("digest", None)
    result["digest"] = canonical_payload_digest(result)
    return result


def _file_sha256(path: Path, errors: list[str], context: str) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        errors.append(f"{context}: cannot read file")
        return None


def _expected_source_artifact_ref(
    path: Path, errors: list[str]
) -> str | None:
    try:
        relative = path.resolve().relative_to(ROLE_POOL_ROOT.resolve())
    except ValueError:
        errors.append(
            "source_artifact: must be inside the canonical installed "
            "mythic-edge-role-pool skill"
        )
        return None
    return f"skill:mythic-edge-role-pool/{relative.as_posix()}"


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def _check_keys(
    value: object, required: set[str], errors: list[str], context: str
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{context}: must be an object")
        return None
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required)
    if missing:
        errors.append(f"{context}: missing fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{context}: unknown fields are not permitted")
    return value


def _require_string(value: object, errors: list[str], context: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{context}: must be a non-empty string")
        return None
    if value != value.strip():
        errors.append(f"{context}: surrounding whitespace is not permitted")
    return value.strip()


def _require_exact(value: object, expected: object, errors: list[str], context: str) -> None:
    if isinstance(expected, bool):
        matches = value is expected
    else:
        matches = value == expected
    if not matches:
        errors.append(f"{context}: must equal {expected!r}")


def _validate_sha256(value: object, errors: list[str], context: str) -> str | None:
    text = _require_string(value, errors, context)
    if text is not None and not SHA256_RE.fullmatch(text):
        errors.append(f"{context}: must be a lowercase SHA-256 digest")
        return None
    return text


def _validate_uuid(value: object, errors: list[str], context: str) -> str | None:
    text = _require_string(value, errors, context)
    if text is not None and not UUID_RE.fullmatch(text):
        errors.append(f"{context}: must be a lowercase UUID")
        return None
    return text


def _validate_reference(
    value: object,
    errors: list[str],
    context: str,
    *,
    prefix: str | None = None,
) -> str | None:
    text = _require_string(value, errors, context)
    if text is None:
        return None
    if not REFERENCE_RE.fullmatch(text):
        errors.append(f"{context}: must be a canonical typed reference")
        return None
    _, remainder = text.split(":", 1)
    segments = remainder.split("/")
    if (
        remainder.startswith("/")
        or remainder.endswith("/")
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        errors.append(f"{context}: must use canonical non-ambiguous segments")
        return None
    if prefix is not None and not text.startswith(prefix):
        errors.append(f"{context}: must use {prefix} provenance")
        return None
    return text


def _validate_timestamp(
    value: object, errors: list[str], context: str, now: datetime
) -> datetime | None:
    parsed = _parse_timestamp(value)
    if parsed is None:
        errors.append(f"{context}: must be a timezone-aware ISO timestamp")
        return None
    if value != _format_timestamp(parsed):
        errors.append(f"{context}: must use canonical UTC whole-second Z format")
    if parsed > now:
        errors.append(f"{context}: cannot be in the future")
    return parsed


def _validate_document_digest(
    document: dict[str, Any], errors: list[str], context: str
) -> None:
    observed = _validate_sha256(document.get("digest"), errors, f"{context}.digest")
    expected = canonical_payload_digest(document)
    if observed is not None and observed != expected:
        errors.append(f"{context}.digest: does not match canonical payload")


def _validate_route(document: dict[str, Any], errors: list[str], context: str) -> None:
    _validate_uuid(document.get("route_id"), errors, f"{context}.route_id")
    repository = _require_string(
        document.get("repository_id"), errors, f"{context}.repository_id"
    )
    repository_invalid = repository is not None and (
        repository != repository.lower()
        or repository.endswith(".git")
        or not REPOSITORY_RE.fullmatch(repository)
        or any(
            segment in {".", ".."}
            or not any(character.isalnum() for character in segment)
            for segment in repository.split("/")
        )
    )
    if repository_invalid:
        errors.append(
            f"{context}.repository_id: must be canonical lowercase owner/repository"
        )
    issue = document.get("issue")
    if isinstance(issue, bool) or not isinstance(issue, int) or issue <= 0:
        errors.append(f"{context}.issue: must be a positive integer")
    lane_id = _require_string(document.get("lane_id"), errors, f"{context}.lane_id")
    if (
        repository is not None
        and not repository_invalid
        and isinstance(issue, int)
        and not isinstance(issue, bool)
    ):
        expected_lane = f"{repository}#{issue}"
        if lane_id != expected_lane:
            errors.append(
                f"{context}.lane_id: must bind canonical repository_id and issue"
            )
    if document.get("role") not in ALLOWED_ROLES:
        errors.append(f"{context}.role: must be a poolable old-workflow role")
    _require_exact(document.get("mode"), OLD_WORKFLOW_MODE, errors, f"{context}.mode")
    if document.get("fallback_condition") not in FALLBACK_CONDITION_IDS:
        errors.append(f"{context}.fallback_condition: must be an exact fallback condition")


def _validate_prompt(
    value: object, errors: list[str], now: datetime
) -> tuple[dict[str, Any] | None, datetime | None]:
    prompt = _check_keys(value, PROMPT_KEYS, errors, "prompt")
    created_at: datetime | None = None
    if prompt is None:
        return None, None
    _require_exact(prompt.get("schema_version"), PROMPT_SCHEMA, errors, "prompt.schema_version")
    _validate_route(prompt, errors, "prompt")
    _validate_reference(
        prompt.get("prompt_ref"),
        errors,
        "prompt.prompt_ref",
        prefix="artifact:old-workflow-prompt/",
    )
    issue = prompt.get("issue")
    if isinstance(issue, int) and not isinstance(issue, bool) and issue > 0:
        _require_exact(
            prompt.get("prompt_ref"),
            f"artifact:old-workflow-prompt/{issue}",
            errors,
            "prompt.prompt_ref",
        )
    created_at = _validate_timestamp(prompt.get("created_at"), errors, "prompt.created_at", now)
    _validate_reference(
        prompt.get("source_artifact_ref"), errors, "prompt.source_artifact_ref"
    )
    _validate_sha256(
        prompt.get("source_artifact_sha256"), errors, "prompt.source_artifact_sha256"
    )
    for field in ("dispatch_authorized", "mutation_authorized", "raw_content_included"):
        _require_exact(prompt.get(field), False, errors, f"prompt.{field}")
    _validate_document_digest(prompt, errors, "prompt")
    return prompt, created_at


def _validate_injection(
    value: object, errors: list[str], now: datetime
) -> tuple[dict[str, Any] | None, datetime | None]:
    injection = _check_keys(value, INJECTION_KEYS, errors, "injection")
    injected_at: datetime | None = None
    if injection is None:
        return None, None
    _require_exact(
        injection.get("schema_version"), INJECTION_SCHEMA, errors, "injection.schema_version"
    )
    _validate_route(injection, errors, "injection")
    injection_id = _validate_uuid(
        injection.get("injection_id"), errors, "injection.injection_id"
    )
    if injection_id is not None:
        _require_exact(
            injection.get("receipt_ref"),
            f"receipt:fallback-injection/{injection_id}",
            errors,
            "injection.receipt_ref",
        )
    injected_at = _validate_timestamp(
        injection.get("injected_at"), errors, "injection.injected_at", now
    )
    _require_exact(injection.get("status"), "succeeded", errors, "injection.status")
    _validate_reference(
        injection.get("route_receipt_ref"),
        errors,
        "injection.route_receipt_ref",
        prefix="receipt:route/",
    )
    _validate_reference(
        injection.get("prompt_ref"),
        errors,
        "injection.prompt_ref",
        prefix="artifact:old-workflow-prompt/",
    )
    issue = injection.get("issue")
    if isinstance(issue, int) and not isinstance(issue, bool) and issue > 0:
        _require_exact(
            injection.get("route_receipt_ref"),
            f"receipt:route/{issue}",
            errors,
            "injection.route_receipt_ref",
        )
        _require_exact(
            injection.get("prompt_ref"),
            f"artifact:old-workflow-prompt/{issue}",
            errors,
            "injection.prompt_ref",
        )
    _validate_sha256(injection.get("prompt_sha256"), errors, "injection.prompt_sha256")
    _require_exact(injection.get("consumer_id"), CONSUMER_ID, errors, "injection.consumer_id")
    _require_exact(
        injection.get("consumer_contract_ref"),
        CONSUMER_CONTRACT_REF,
        errors,
        "injection.consumer_contract_ref",
    )
    _validate_sha256(
        injection.get("consumer_contract_sha256"),
        errors,
        "injection.consumer_contract_sha256",
    )
    _require_exact(
        injection.get("consumer_ingress_ref"),
        CONSUMER_INGRESS_REF,
        errors,
        "injection.consumer_ingress_ref",
    )
    _validate_sha256(
        injection.get("consumer_ingress_sha256"),
        errors,
        "injection.consumer_ingress_sha256",
    )
    for field in ("task_created", "agent_launched", "mutation_performed"):
        _require_exact(injection.get(field), False, errors, f"injection.{field}")
    _validate_document_digest(injection, errors, "injection")
    return injection, injected_at


def _validate_pickup(
    value: object, errors: list[str], now: datetime
) -> tuple[dict[str, Any] | None, datetime | None]:
    pickup = _check_keys(value, PICKUP_KEYS, errors, "pickup")
    picked_up_at: datetime | None = None
    if pickup is None:
        return None, None
    _require_exact(pickup.get("schema_version"), PICKUP_SCHEMA, errors, "pickup.schema_version")
    _validate_route(pickup, errors, "pickup")
    pickup_id = _validate_uuid(pickup.get("pickup_id"), errors, "pickup.pickup_id")
    if pickup_id is not None:
        _require_exact(
            pickup.get("receipt_ref"),
            f"receipt:old-workflow-pickup/{pickup_id}",
            errors,
            "pickup.receipt_ref",
        )
    picked_up_at = _validate_timestamp(
        pickup.get("picked_up_at"), errors, "pickup.picked_up_at", now
    )
    _require_exact(
        pickup.get("pickup_kind"),
        "ingress_acknowledgement",
        errors,
        "pickup.pickup_kind",
    )
    _require_exact(
        pickup.get("pickup_status"), "accepted_no_launch", errors, "pickup.pickup_status"
    )
    _require_exact(pickup.get("consumer_id"), CONSUMER_ID, errors, "pickup.consumer_id")
    _require_exact(
        pickup.get("consumer_contract_ref"),
        CONSUMER_CONTRACT_REF,
        errors,
        "pickup.consumer_contract_ref",
    )
    _validate_sha256(
        pickup.get("consumer_contract_sha256"),
        errors,
        "pickup.consumer_contract_sha256",
    )
    _require_exact(
        pickup.get("consumer_ingress_ref"),
        CONSUMER_INGRESS_REF,
        errors,
        "pickup.consumer_ingress_ref",
    )
    _validate_sha256(
        pickup.get("consumer_ingress_sha256"), errors, "pickup.consumer_ingress_sha256"
    )
    _validate_reference(
        pickup.get("injection_ref"),
        errors,
        "pickup.injection_ref",
        prefix="receipt:fallback-injection/",
    )
    _validate_sha256(pickup.get("injection_sha256"), errors, "pickup.injection_sha256")
    _validate_reference(
        pickup.get("route_receipt_ref"),
        errors,
        "pickup.route_receipt_ref",
        prefix="receipt:route/",
    )
    _validate_reference(
        pickup.get("prompt_ref"),
        errors,
        "pickup.prompt_ref",
        prefix="artifact:old-workflow-prompt/",
    )
    issue = pickup.get("issue")
    if isinstance(issue, int) and not isinstance(issue, bool) and issue > 0:
        _require_exact(
            pickup.get("route_receipt_ref"),
            f"receipt:route/{issue}",
            errors,
            "pickup.route_receipt_ref",
        )
        _require_exact(
            pickup.get("prompt_ref"),
            f"artifact:old-workflow-prompt/{issue}",
            errors,
            "pickup.prompt_ref",
        )
    _validate_sha256(pickup.get("prompt_sha256"), errors, "pickup.prompt_sha256")
    for field in ("task_created", "agent_launched", "mutation_performed"):
        _require_exact(pickup.get(field), False, errors, f"pickup.{field}")
    _validate_document_digest(pickup, errors, "pickup")
    return pickup, picked_up_at


def validate_fallback_pickup_bundle(
    *,
    prompt: object,
    injection: object,
    pickup: object | None,
    workflow_skill: Path,
    pickup_producer: Path,
    source_artifact: Path,
    now: datetime,
) -> list[str]:
    """Return every strict schema, provenance, digest, and binding error."""

    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    now = now.astimezone(timezone.utc)
    errors: list[str] = []
    prompt_doc, prompt_created = _validate_prompt(prompt, errors, now)
    injection_doc, injected_at = _validate_injection(injection, errors, now)

    pickup_doc: dict[str, Any] | None = None
    picked_up_at: datetime | None = None
    if pickup is None:
        if isinstance(injection_doc, dict) and injection_doc.get("status") == "succeeded":
            errors.append("pickup: required after successful fallback injection")
    else:
        pickup_doc, picked_up_at = _validate_pickup(pickup, errors, now)

    expected_workflow_skill = EXPECTED_WORKFLOW_ROOT / "SKILL.md"
    expected_pickup_producer = (
        EXPECTED_WORKFLOW_ROOT / "scripts" / "accept_fallback_prompt.py"
    )
    if workflow_skill.resolve() != expected_workflow_skill.resolve():
        errors.append(
            "workflow_skill: must be the canonical installed sibling "
            "mythic-edge-workflow/SKILL.md"
        )
    if pickup_producer.resolve() != expected_pickup_producer.resolve():
        errors.append(
            "pickup_producer: must be the canonical installed sibling "
            "mythic-edge-workflow/scripts/accept_fallback_prompt.py"
        )
    contract_sha = _file_sha256(workflow_skill, errors, "workflow_skill")
    ingress_sha = _file_sha256(pickup_producer, errors, "pickup_producer")
    source_sha = _file_sha256(source_artifact, errors, "source_artifact")
    expected_source_ref = _expected_source_artifact_ref(source_artifact, errors)

    if (
        prompt_doc is not None
        and source_sha is not None
        and prompt_doc.get("source_artifact_sha256") != source_sha
    ):
        errors.append(
            "binding.source_artifact_sha256: prompt does not match supplied source artifact"
        )
    if (
        prompt_doc is not None
        and expected_source_ref is not None
        and prompt_doc.get("source_artifact_ref") != expected_source_ref
    ):
        errors.append(
            "binding.source_artifact_ref: prompt does not identify the supplied "
            "canonical Role Pool source artifact"
        )

    if prompt_doc is not None and injection_doc is not None:
        for field in PROMPT_INJECTION_BINDINGS:
            if prompt_doc.get(field) != injection_doc.get(field):
                errors.append(f"binding.{field}: prompt and injection must match exactly")
        if injection_doc.get("prompt_sha256") != prompt_doc.get("digest"):
            errors.append("binding.prompt_sha256: injection must equal prompt.digest")
        if (
            prompt_created is not None
            and injected_at is not None
            and injected_at < prompt_created
        ):
            errors.append("binding.timestamps: injection cannot precede prompt creation")

    if injection_doc is not None:
        if (
            contract_sha is not None
            and injection_doc.get("consumer_contract_sha256") != contract_sha
        ):
            errors.append(
                "binding.consumer_contract_sha256: injection does not match current old-workflow SKILL.md"
            )
        if (
            ingress_sha is not None
            and injection_doc.get("consumer_ingress_sha256") != ingress_sha
        ):
            errors.append(
                "binding.consumer_ingress_sha256: injection does not match current old-workflow ingress"
            )

    if injection_doc is not None and pickup_doc is not None:
        for field in INJECTION_PICKUP_BINDINGS:
            if injection_doc.get(field) != pickup_doc.get(field):
                errors.append(f"binding.{field}: injection and pickup must match exactly")
        if pickup_doc.get("injection_ref") != injection_doc.get("receipt_ref"):
            errors.append("binding.injection_ref: pickup must equal injection.receipt_ref")
        if pickup_doc.get("injection_sha256") != injection_doc.get("digest"):
            errors.append("binding.injection_sha256: pickup must equal injection.digest")
        expected_pickup_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                "mythic-edge-old-workflow-pickup:"
                f"{injection_doc.get('digest')}:{pickup_doc.get('picked_up_at')}",
            )
        )
        if pickup_doc.get("pickup_id") != expected_pickup_id:
            errors.append(
                "binding.pickup_id: must be deterministically derived from "
                "injection.digest and pickup.picked_up_at"
            )
        if injected_at is not None and picked_up_at is not None:
            if picked_up_at < injected_at:
                errors.append("binding.timestamps: pickup cannot precede injection")
            elif picked_up_at - injected_at > MAX_PICKUP_DELAY:
                errors.append("binding.timestamps: pickup must occur within five minutes of injection")
        if contract_sha is not None and pickup_doc.get("consumer_contract_sha256") != contract_sha:
            errors.append(
                "binding.consumer_contract_sha256: pickup does not match current old-workflow SKILL.md"
            )
        if ingress_sha is not None and pickup_doc.get("consumer_ingress_sha256") != ingress_sha:
            errors.append(
                "binding.consumer_ingress_sha256: pickup does not match current old-workflow ingress"
            )

    if prompt_doc is not None and pickup_doc is not None:
        if pickup_doc.get("prompt_ref") != prompt_doc.get("prompt_ref"):
            errors.append("binding.prompt_ref: pickup must equal prompt.prompt_ref")
        if pickup_doc.get("prompt_sha256") != prompt_doc.get("digest"):
            errors.append("binding.prompt_sha256: pickup must equal prompt.digest")

    return errors


def _load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_reject_duplicate_keys)


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key is not permitted")
        result[key] = value
    return result


def _now_argument(value: str) -> datetime:
    parsed = _parse_timestamp(value)
    if parsed is None:
        raise argparse.ArgumentTypeError("must be a timezone-aware ISO timestamp")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify a canonical fallback prompt, successful injection, and independent "
            "old-workflow pickup receipt."
        )
    )
    parser.add_argument("injection", type=Path, help="fallback injection JSON")
    parser.add_argument("--prompt", required=True, type=Path, help="old-workflow prompt JSON")
    parser.add_argument(
        "--pickup",
        type=Path,
        help="old-workflow pickup JSON; semantically required after successful injection",
    )
    parser.add_argument(
        "--workflow-skill", required=True, type=Path, help="old-workflow SKILL.md"
    )
    parser.add_argument(
        "--pickup-producer", required=True, type=Path, help="old-workflow ingress script"
    )
    parser.add_argument(
        "--source-artifact",
        required=True,
        type=Path,
        help="exact source artifact whose SHA-256 is bound by the prompt",
    )
    parser.add_argument(
        "--now",
        type=_now_argument,
        default=None,
        help="verification timestamp for deterministic offline tests",
    )
    args = parser.parse_args(argv)
    now = args.now or datetime.now(timezone.utc)
    workflow_skill = args.workflow_skill.resolve()
    pickup_producer = args.pickup_producer.resolve()
    source_artifact = args.source_artifact.resolve()

    try:
        for verification_path in (
            workflow_skill,
            pickup_producer,
            source_artifact,
        ):
            with verification_path.open("rb") as handle:
                handle.read(1)
        prompt = _load_json(args.prompt)
        injection = _load_json(args.injection)
        pickup = _load_json(args.pickup) if args.pickup is not None else None
    except (OSError, UnicodeError, ValueError):
        print(
            "fallback pickup input error: input is unreadable, malformed, or ambiguous",
            file=sys.stderr,
        )
        return 2

    errors = validate_fallback_pickup_bundle(
        prompt=prompt,
        injection=injection,
        pickup=pickup,
        workflow_skill=workflow_skill,
        pickup_producer=pickup_producer,
        source_artifact=source_artifact,
        now=now,
    )
    if errors:
        print("fallback pickup validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "fallback pickup validation passed: injection and independent "
        "old-workflow pickup are fully bound"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
