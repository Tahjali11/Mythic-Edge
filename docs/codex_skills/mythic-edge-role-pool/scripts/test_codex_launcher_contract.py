from __future__ import annotations

import hashlib
import inspect
import json
import os
import pickle
import subprocess
import tempfile
import unittest
from copy import copy as shallow_copy, deepcopy
from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import codex_launcher_contract as launcher_contract

from codex_launcher_contract import (
    AMBIENT_ENVIRONMENT_PROVENANCE,
    CHILD_ENVIRONMENT_POLICY,
    ChildEnvironment,
    EXTERNAL_ISOLATION_SCHEMA_VERSION,
    ExternalIsolationReceipt,
    ProductionVerificationContext,
    PREFERRED_MODEL,
    REQUIRED_EXEC_FLAGS,
    SingleStartGuard,
    _build_child_environment_from_source,
    _build_child_environment_for_test,
    _launch_once_for_test,
    _run_local_command,
    build_child_environment,
    build_codex_exec_args,
    canonical_digest,
    launch_once,
    resolve_launcher_preflight,
    validate_launch_receipt,
    validate_launch_receipt_against_context,
    validate_child_environment,
    validate_external_isolation_receipt,
    validate_preflight,
)


OBSERVED = "2026-07-14T12:00:00Z"


class FakeRunner:
    def __init__(self, versions: dict[str, str], models: dict[str, list[str]]) -> None:
        self.versions = versions
        self.models = models
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        command = list(args)
        self.calls.append(command)
        executable = Path(command[0]).name + ":" + Path(command[0]).parent.name
        if command[1:] == ["--version"]:
            return subprocess.CompletedProcess(command, 0, self.versions[executable], "")
        if command[1:] == ["exec", "--help"]:
            return subprocess.CompletedProcess(
                command,
                0,
                "\n".join(REQUIRED_EXEC_FLAGS),
                "",
            )
        if command[1:] == ["debug", "models", "--bundled"]:
            return subprocess.CompletedProcess(
                command,
                0,
                json.dumps({"models": [{"slug": slug} for slug in self.models[executable]]}),
                "",
            )
        raise AssertionError(command)


def make_candidates(root: Path) -> tuple[Path, Path]:
    old = root / "codex.exe"
    new = root / "current" / "codex.exe"
    new.parent.mkdir()
    old.write_bytes(b"old-cli")
    new.write_bytes(b"new-cli")
    return old, new


class LauncherPreflightTests(unittest.TestCase):
    @staticmethod
    def redigest(document: dict[str, object]) -> None:
        unsigned = dict(document)
        unsigned.pop("digest", None)
        document["digest"] = canonical_digest(unsigned)

    def test_local_probe_runner_uses_explicit_strict_utf8_decoding(self) -> None:
        completed = subprocess.CompletedProcess(["codex.exe", "--version"], 0, "ok", "")
        with patch("codex_launcher_contract.subprocess.run", return_value=completed) as run:
            self.assertIs(
                _run_local_command(["codex.exe", "--version"]), completed
            )
        self.assertEqual(run.call_args.kwargs["encoding"], "utf-8")
        self.assertEqual(run.call_args.kwargs["errors"], "strict")

    def test_newest_compatible_cli_and_gpt_56_sol_are_selected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = make_candidates(root)
            runner = FakeRunner(
                {
                    f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                    f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
                },
                {
                    f"{old.name}:{old.parent.name}": [],
                    f"{new.name}:{new.parent.name}": [PREFERRED_MODEL],
                },
            )
            preflight = resolve_launcher_preflight(
                root,
                runner=runner,
                observed_at=OBSERVED,
            )
            self.assertEqual(validate_preflight(preflight), [])
            self.assertEqual(preflight["selected_executable"]["path"], str(new.resolve()))
            self.assertEqual(preflight["selected_executable"]["cli_version"], "codex-cli 0.144.2")
            self.assertTrue(preflight["model_argument_enabled"])
            self.assertEqual(preflight["model_preference_status"], "available_and_will_request")
            self.assertFalse(preflight["codex_exec_started"])
            self.assertEqual(preflight["codex_exec_process_start_count"], 0)
            self.assertEqual(preflight["probe_process_count"], 6)

    def test_unavailable_preferred_model_uses_platform_default_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = make_candidates(root)
            runner = FakeRunner(
                {
                    f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                    f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
                },
                {
                    f"{old.name}:{old.parent.name}": [],
                    f"{new.name}:{new.parent.name}": ["platform-default"],
                },
            )
            preflight = resolve_launcher_preflight(
                root,
                runner=runner,
                observed_at=OBSERVED,
            )
            self.assertEqual(validate_preflight(preflight), [])
            self.assertEqual(preflight["status"], "ready")
            self.assertFalse(preflight["model_argument_enabled"])
            self.assertEqual(
                preflight["model_preference_status"],
                "unavailable_use_platform_default",
            )
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            self.assertNotIn("--model", args)
            self.assertNotIn("-c", args)
            self.assertFalse(preflight["reasoning_effort_argument_enabled"])

    def test_preflight_digest_and_required_fields_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = make_candidates(root)
            runner = FakeRunner(
                {
                    f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                    f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
                },
                {
                    f"{old.name}:{old.parent.name}": [],
                    f"{new.name}:{new.parent.name}": [PREFERRED_MODEL],
                },
            )
            preflight = resolve_launcher_preflight(root, runner=runner, observed_at=OBSERVED)
            unsigned = dict(preflight)
            digest = unsigned.pop("digest")
            self.assertEqual(digest, canonical_digest(unsigned))
            preflight["preferred_model"] = "different-model"
            errors = validate_preflight(
                preflight,
                expected_preferred_model=PREFERRED_MODEL,
            )
            self.assertTrue(any("preferred_model" in error for error in errors))
            self.assertTrue(any("digest" in error for error in errors))

    def test_nested_candidate_schema_and_path_containment_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = make_candidates(root)
            runner = FakeRunner(
                {
                    f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                    f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
                },
                {
                    f"{old.name}:{old.parent.name}": [],
                    f"{new.name}:{new.parent.name}": [PREFERRED_MODEL],
                },
            )
            preflight = resolve_launcher_preflight(root, runner=runner, observed_at=OBSERVED)
            tampered = deepcopy(preflight)
            tampered["inspected_candidates"][0]["unknown"] = True
            tampered["inspected_candidates"][0]["path"] = str(root.parent / "outside.exe")
            unsigned = dict(tampered)
            unsigned.pop("digest")
            tampered["digest"] = canonical_digest(unsigned)
            errors = validate_preflight(tampered)
            self.assertTrue(any("frozen candidate schema" in error for error in errors))
            self.assertTrue(any("contained by bin_root" in error for error in errors))

    def test_command_requests_gpt_56_sol_exactly_once_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = make_candidates(root)
            runner = FakeRunner(
                {
                    f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                    f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
                },
                {
                    f"{old.name}:{old.parent.name}": [],
                    f"{new.name}:{new.parent.name}": [PREFERRED_MODEL],
                },
            )
            preflight = resolve_launcher_preflight(root, runner=runner, observed_at=OBSERVED)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            model_index = args.index("--model")
            self.assertEqual(args[model_index + 1], PREFERRED_MODEL)
            self.assertEqual(args.count("--model"), 1)
            self.assertIn('model_reasoning_effort="max"', args)

    def test_flag_lookalike_does_not_satisfy_required_model_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            executable = root / "codex.exe"
            executable.write_bytes(b"cli")

            def runner(args: list[str]) -> subprocess.CompletedProcess[str]:
                command = list(args)
                if command[1:] == ["--version"]:
                    return subprocess.CompletedProcess(command, 0, "codex-cli 0.144.2", "")
                if command[1:] == ["exec", "--help"]:
                    flags = [flag for flag in REQUIRED_EXEC_FLAGS if flag != "--model"]
                    return subprocess.CompletedProcess(
                        command, 0, "\n".join([*flags, "--model-provider"]), ""
                    )
                raise AssertionError(command)

            preflight = resolve_launcher_preflight(
                root, runner=runner, observed_at=OBSERVED
            )
            self.assertEqual(validate_preflight(preflight), [])
            self.assertEqual(preflight["status"], "blocked")
            self.assertIn("--model", preflight["inspected_candidates"][0]["missing_exec_flags"])

    def test_malformed_bundled_catalog_is_advisory_and_omits_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            executable = root / "codex.exe"
            executable.write_bytes(b"cli")

            def runner(args: list[str]) -> subprocess.CompletedProcess[str]:
                command = list(args)
                if command[1:] == ["--version"]:
                    return subprocess.CompletedProcess(command, 0, "codex-cli 0.144.2", "")
                if command[1:] == ["exec", "--help"]:
                    return subprocess.CompletedProcess(
                        command, 0, "\n".join(REQUIRED_EXEC_FLAGS), ""
                    )
                if command[1:] == ["debug", "models", "--bundled"]:
                    return subprocess.CompletedProcess(command, 0, '{"models":', "")
                raise AssertionError(command)

            preflight = resolve_launcher_preflight(
                root, runner=runner, observed_at=OBSERVED
            )
            self.assertEqual(validate_preflight(preflight), [])
            self.assertEqual(preflight["status"], "ready")
            self.assertFalse(preflight["model_argument_enabled"])
            self.assertFalse(preflight["reasoning_effort_argument_enabled"])

    def test_preferred_model_availability_requires_bundled_catalog_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old, new = make_candidates(root)
            runner = FakeRunner(
                {
                    f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                    f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
                },
                {
                    f"{old.name}:{old.parent.name}": [],
                    f"{new.name}:{new.parent.name}": [PREFERRED_MODEL],
                },
            )
            preflight = resolve_launcher_preflight(root, runner=runner, observed_at=OBSERVED)
            selected_path = preflight["selected_executable"]["path"]
            for candidate in preflight["inspected_candidates"]:
                if candidate["path"] == selected_path:
                    candidate["bundled_model_catalog_available"] = False
            preflight["selected_executable"]["bundled_model_catalog_available"] = False
            self.redigest(preflight)
            errors = validate_preflight(preflight)
            self.assertTrue(any("bundled catalog evidence" in error for error in errors), errors)

    def test_child_environment_is_minimal_and_credential_free(self) -> None:
        environment = _build_child_environment_for_test(
            {
                "Path": r"C:\Windows\System32",
                "TEMP": r"C:\Temp",
                "GH_TOKEN": "never-forward-this",
                "OPENAI_API_KEY": "never-forward-this-either",
                "UNRELATED": "drop-me",
            },
            bindings={
                "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH": r"C:\Temp\packet.json",
                "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256": "a" * 64,
                "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES": "1",
            },
        )
        values = environment.as_dict()
        self.assertEqual(
            set(values),
            {
                "PATH",
                "TEMP",
                "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH",
                "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256",
                "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES",
            },
        )
        self.assertEqual(environment.sensitive_source_key_count, 2)
        self.assertEqual(environment.dropped_source_key_count, 3)
        self.assertNotIn("never-forward-this", repr(environment))
        with self.assertRaises(ValueError):
            _build_child_environment_for_test({}, bindings={"GH_TOKEN": "secret"})
        with self.assertRaises(ValueError):
            _build_child_environment_for_test({"Path": "one", "PATH": "two"})
        forged_entries = (("GH_TOKEN", "secret"),)
        forged = ChildEnvironment(
            policy_id=CHILD_ENVIRONMENT_POLICY,
            source_provenance="internal_test_fixture",
            safe_os_source_digest=canonical_digest(
                {
                    "source_provenance": "internal_test_fixture",
                    "safe_os_values": {},
                }
            ),
            entries=forged_entries,
            digest=canonical_digest(
                {
                    "policy_id": CHILD_ENVIRONMENT_POLICY,
                    "source_provenance": "internal_test_fixture",
                    "safe_os_source_digest": canonical_digest(
                        {
                            "source_provenance": "internal_test_fixture",
                            "safe_os_values": {},
                        }
                    ),
                    "values": dict(forged_entries),
                }
            ),
            source_key_count=1,
            retained_source_key_count=0,
            dropped_source_key_count=1,
            sensitive_source_key_count=1,
            binding_key_count=0,
        )
        self.assertTrue(validate_child_environment(forged))
        malformed_counts = ChildEnvironment(
            policy_id=CHILD_ENVIRONMENT_POLICY,
            source_provenance="internal_test_fixture",
            safe_os_source_digest=canonical_digest(
                {
                    "source_provenance": "internal_test_fixture",
                    "safe_os_values": {},
                }
            ),
            entries=(),
            digest=canonical_digest(
                {
                    "policy_id": CHILD_ENVIRONMENT_POLICY,
                    "source_provenance": "internal_test_fixture",
                    "safe_os_source_digest": canonical_digest(
                        {
                            "source_provenance": "internal_test_fixture",
                            "safe_os_values": {},
                        }
                    ),
                    "values": {},
                }
            ),
            source_key_count="1",  # type: ignore[arg-type]
            retained_source_key_count=0,
            dropped_source_key_count=0,
            sensitive_source_key_count=0,
            binding_key_count=0,
        )
        self.assertTrue(validate_child_environment(malformed_counts))


class FakeProcess:
    def __init__(self, stdout: bytes = b"typed-jsonl", stderr: bytes = b"") -> None:
        self.pid = 1234
        self.returncode = 0
        self.stdout = stdout
        self.stderr = stderr
        self.communicate_calls = 0

    def communicate(self, *, input: bytes | None = None, timeout: int | None = None):
        self.communicate_calls += 1
        return self.stdout, self.stderr

    def kill(self) -> None:
        self.returncode = -9


class TimeoutProcess(FakeProcess):
    def communicate(self, *, input: bytes | None = None, timeout: int | None = None):
        self.communicate_calls += 1
        if self.communicate_calls == 1:
            raise subprocess.TimeoutExpired("codex", timeout or 0)
        return b"partial-jsonl", b"timed-out"


class CommunicateErrorProcess(FakeProcess):
    def communicate(self, *, input: bytes | None = None, timeout: int | None = None):
        self.communicate_calls += 1
        if self.communicate_calls == 1:
            raise OSError("synthetic child I/O failure")
        return b"cleanup-stdout", b"cleanup-stderr"


class InvalidStateProcess(FakeProcess):
    def __init__(self) -> None:
        super().__init__()
        self.pid = "invalid"
        self.killed = False

    def kill(self) -> None:
        self.killed = True
        self.returncode = -9


class SingleStartReceiptTests(unittest.TestCase):
    @staticmethod
    def isolation_receipt(
        preflight: dict[str, object],
        packet: bytes,
        packet_path: Path,
        cwd: Path,
        additional_directory: Path,
        *,
        current_time: datetime | None = None,
    ) -> ExternalIsolationReceipt:
        selected = preflight["selected_executable"]
        assert isinstance(selected, dict)
        current = (current_time or datetime.now(timezone.utc)).astimezone(
            timezone.utc
        ).replace(microsecond=0)
        unsigned = {
            "schema_version": EXTERNAL_ISOLATION_SCHEMA_VERSION,
            "provider": "synthetic-os-isolator",
            "evidence_source": "synthetic-independent-os-observer",
            "provider_production_eligible": True,
            "evidence_source_production_eligible": True,
            "independently_verified": True,
            "isolation_id": "12345678-1234-4234-8234-123456789abd",
            "selected_executable_path": selected["path"],
            "selected_executable_sha256": selected["sha256"],
            "selected_executable_length_bytes": selected["length_bytes"],
            "packet_path": str(packet_path),
            "packet_sha256": hashlib.sha256(packet).hexdigest(),
            "packet_length_bytes": len(packet),
            "workspace_path": str(cwd),
            "writable_directory_path": str(additional_directory),
            "reviewed_read_only_roots": (str(cwd),),
            "writable_temp_scopes": (str(additional_directory),),
            "tool_subprocess_network_denied": True,
            "codex_control_plane_network_separately_scoped": True,
            "codex_control_plane_network_scope": "codex_service_only",
            "writable_directory_exclusive": True,
            "process_creation_controlled": True,
            "launcher_process_start_limit": 1,
            "tool_subprocess_start_limit": 1,
            "credential_access_denied": True,
            "user_profile_access_denied": True,
            "observed_at": (current - timedelta(seconds=1)).isoformat().replace(
                "+00:00", "Z"
            ),
            "expires_at": (current + timedelta(seconds=120)).isoformat().replace(
                "+00:00", "Z"
            ),
            "attestation_algorithm": "hmac-sha256",
            "attestation_key_id": "synthetic-test-key-v1",
        }
        receipt = ExternalIsolationReceipt(
            **unsigned,
            attestation_hmac_sha256="0" * 64,
            digest="",
        )
        unsigned_receipt = asdict(receipt)
        unsigned_receipt.pop("digest")
        return replace(receipt, digest=canonical_digest(unsigned_receipt))

    @staticmethod
    def mutate_isolation_receipt(
        receipt: ExternalIsolationReceipt,
        **changes: object,
    ) -> ExternalIsolationReceipt:
        mutated = replace(receipt, **changes, digest="")
        unsigned = asdict(mutated)
        unsigned.pop("digest")
        return replace(mutated, digest=canonical_digest(unsigned))

    @staticmethod
    def environment_for_packet(
        packet: bytes,
        source: dict[str, str] | None = None,
    ) -> ChildEnvironment:
        return _build_child_environment_for_test(
            source or {},
            bindings={
                "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH": r"C:\Temp\packet.json",
                "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256": hashlib.sha256(packet).hexdigest(),
                "MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES": str(len(packet)),
                "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_PATH": r"C:\Temp\child.ps1",
                "MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256": "b" * 64,
                "MYTHIC_EDGE_ROLE_POOL_ATTEMPT_SERIES_ID": "12345678-1234-4234-8234-123456789abc",
                "MYTHIC_EDGE_ROLE_POOL_SEQUENCE_INDEX": "1",
            },
        )

    def ready_preflight(self, root: Path) -> dict[str, object]:
        old, new = make_candidates(root)
        runner = FakeRunner(
            {
                f"{old.name}:{old.parent.name}": "codex-cli 0.130.0-alpha.5",
                f"{new.name}:{new.parent.name}": "codex-cli 0.144.2",
            },
            {
                f"{old.name}:{old.parent.name}": [],
                f"{new.name}:{new.parent.name}": [PREFERRED_MODEL],
            },
        )
        return resolve_launcher_preflight(root, runner=runner, observed_at=OBSERVED)

    def test_public_production_api_has_no_process_or_clock_injection_seam(self) -> None:
        parameters = inspect.signature(launch_once).parameters
        self.assertNotIn("popen_factory", parameters)
        self.assertNotIn("clock", parameters)
        with self.assertRaises(TypeError):
            build_child_environment(  # type: ignore[call-arg]
                {"PATH": r"C:\attacker-controlled"},
                packet_path=Path(r"C:\Temp\packet.json"),
                packet_bytes=b"packet",
                child_script_path=Path(r"C:\Temp\child.ps1"),
                child_script_bytes=b"script",
                attempt_series_id="12345678-1234-4234-8234-123456789abc",
                sequence_index=1,
            )

    def test_production_verifier_is_unprovisioned_opaque_and_has_no_signer(self) -> None:
        self.assertFalse(hasattr(ProductionVerificationContext, "__dataclass_fields__"))
        self.assertFalse(hasattr(launcher_contract, "_authenticate_payload_for_test"))
        self.assertFalse(
            hasattr(launcher_contract, "_authenticate_external_isolation_receipt_for_test")
        )
        with self.assertRaisesRegex(RuntimeError, "not provisioned"):
            ProductionVerificationContext(
                key_id="caller-key",
                expected_provider="caller-provider",
                expected_evidence_source="caller-source",
                expected_verifier_identity="caller-verifier",
                verification_key=b"a" * 32,
            )
        opaque = object.__new__(ProductionVerificationContext)
        self.assertFalse(hasattr(opaque, "__dict__"))
        self.assertFalse(opaque.verify("domain", {"value": 1}, "0" * 64))
        with self.assertRaises(TypeError):
            asdict(opaque)
        with self.assertRaises(TypeError):
            shallow_copy(opaque)
        with self.assertRaises(TypeError):
            deepcopy(opaque)
        with self.assertRaises(TypeError):
            pickle.dumps(opaque)

    def test_public_builder_derives_complete_bindings_from_exact_inputs(self) -> None:
        packet = b'{"packet":"exact"}'
        child_script = b"Write-Output '{}'"
        with patch.dict(
            os.environ,
            {"PATH": r"C:\Windows\System32", "TEMP": r"C:\Temp"},
            clear=True,
        ):
            environment = build_child_environment(
                packet_path=Path(r"C:\Temp\packet.json"),
                packet_bytes=packet,
                child_script_path=Path(r"C:\Temp\child.ps1"),
                child_script_bytes=child_script,
                attempt_series_id="12345678-1234-4234-8234-123456789abc",
                sequence_index=1,
            )
            self.assertEqual(
                validate_child_environment(
                    environment,
                    require_ambient_provenance=True,
                ),
                [],
            )
        values = environment.as_dict()
        self.assertEqual(environment.source_provenance, AMBIENT_ENVIRONMENT_PROVENANCE)
        self.assertEqual(
            values["MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256"],
            hashlib.sha256(packet).hexdigest(),
        )
        self.assertEqual(
            values["MYTHIC_EDGE_ROLE_POOL_PACKET_LENGTH_BYTES"],
            str(len(packet)),
        )
        self.assertEqual(
            values["MYTHIC_EDGE_ROLE_POOL_CHILD_SCRIPT_SHA256"],
            hashlib.sha256(child_script).hexdigest(),
        )

    def test_production_launch_rejects_missing_bindings_before_guard_or_popen(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            with patch.dict(os.environ, {"PATH": r"C:\Windows\System32"}, clear=True):
                environment = _build_child_environment_from_source(
                    os.environ,
                    bindings={},
                    source_provenance=AMBIENT_ENVIRONMENT_PROVENANCE,
                )
                guard = SingleStartGuard()
                with patch("codex_launcher_contract.subprocess.Popen") as popen:
                    with self.assertRaisesRegex(ValueError, "binding set is incomplete"):
                        launch_once(
                            preflight,
                            args,
                            b"packet",
                            cwd=Path("C:/workspace"),
                            additional_directory=Path("C:/temporary"),
                            output_schema_path=Path("C:/temporary/result.schema.json"),
                            environment=environment,
                            attempt_guard=guard,
                        )
            self.assertFalse(guard.consumed)
            popen.assert_not_called()

    def test_production_launch_requires_external_os_isolation_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            packet = b"packet"
            packet_path = root / "packet.json"
            packet_path.write_bytes(packet)
            child_script_path = root / "child.ps1"
            child_script = b"Write-Output '{}'"
            child_script_path.write_bytes(child_script)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=root,
                output_schema_path=root / "result.schema.json",
            )
            guard = SingleStartGuard()
            with patch.dict(os.environ, {"PATH": r"C:\Windows\System32"}, clear=True):
                environment = build_child_environment(
                    packet_path=packet_path,
                    packet_bytes=packet,
                    child_script_path=child_script_path,
                    child_script_bytes=child_script,
                    attempt_series_id="12345678-1234-4234-8234-123456789abc",
                    sequence_index=1,
                )
                with patch("codex_launcher_contract.subprocess.Popen") as popen:
                    with self.assertRaisesRegex(ValueError, "OS isolation evidence"):
                        launch_once(
                            preflight,
                            args,
                            packet,
                            cwd=Path("C:/workspace"),
                            additional_directory=root,
                            output_schema_path=root / "result.schema.json",
                            environment=environment,
                            attempt_guard=guard,
                        )
            self.assertFalse(guard.consumed)
            popen.assert_not_called()

    def test_external_isolation_relabel_and_redigest_cannot_supply_trust_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            packet = b"packet"
            packet_path = root / "packet.json"
            packet_path.write_bytes(packet)
            receipt = self.isolation_receipt(
                preflight,
                packet,
                packet_path,
                Path("C:/workspace"),
                root,
            )
            forged = self.mutate_isolation_receipt(
                receipt,
                provider="forged-os-isolator",
            )
            errors = validate_external_isolation_receipt(
                forged,
                preflight=preflight,
                packet_bytes=packet,
                packet_path=packet_path,
                cwd=Path("C:/workspace"),
                additional_directory=root,
                verification_context=None,
            )
            self.assertTrue(
                any("out-of-band typed contract" in error for error in errors),
                errors,
            )
            with self.assertRaisesRegex(RuntimeError, "not provisioned"):
                ProductionVerificationContext(
                    key_id="caller-key",
                    expected_provider="caller-provider",
                    expected_evidence_source="caller-source",
                    expected_verifier_identity="caller-verifier",
                    verification_key=b"a" * 32,
                )

    def test_production_launch_rejects_test_only_os_source_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            environment = self.environment_for_packet(
                b"packet",
                {"PATH": r"C:\attacker-controlled"},
            )
            guard = SingleStartGuard()
            with patch.dict(os.environ, {"PATH": r"C:\Windows\System32"}, clear=True):
                with patch("codex_launcher_contract.subprocess.Popen") as popen:
                    with self.assertRaisesRegex(ValueError, "frozen validation contract"):
                        launch_once(
                            preflight,
                            args,
                            b"packet",
                            cwd=Path("C:/workspace"),
                            additional_directory=Path("C:/temporary"),
                            output_schema_path=Path("C:/temporary/result.schema.json"),
                            environment=environment,
                            attempt_guard=guard,
                        )
            self.assertFalse(guard.consumed)
            popen.assert_not_called()

    def test_production_launch_stays_blocked_without_pinned_verifier(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=root,
                output_schema_path=root / "result.schema.json",
            )
            packet = b'{"packet":"exact"}'
            packet_path = root / "packet.json"
            packet_path.write_bytes(packet)
            child_script_path = root / "child.ps1"
            child_script = b"Write-Output '{}'"
            child_script_path.write_bytes(child_script)
            with patch.dict(os.environ, {"PATH": r"C:\Windows\System32"}, clear=True):
                environment = build_child_environment(
                    packet_path=packet_path,
                    packet_bytes=packet,
                    child_script_path=child_script_path,
                    child_script_bytes=child_script,
                    attempt_series_id="12345678-1234-4234-8234-123456789abc",
                    sequence_index=1,
                )
                guard = SingleStartGuard()
                with patch("codex_launcher_contract.subprocess.Popen") as popen:
                    with self.assertRaisesRegex(ValueError, "OS isolation evidence"):
                        launch_once(
                            preflight,
                            args,
                            packet,
                            cwd=Path("C:/workspace"),
                            additional_directory=root,
                            output_schema_path=root / "result.schema.json",
                            environment=environment,
                            attempt_guard=guard,
                            external_isolation_receipt=self.isolation_receipt(
                                preflight,
                                packet,
                                packet_path,
                                Path("C:/workspace"),
                                root,
                            ),
                            verification_context=None,
                        )
            self.assertFalse(guard.consumed)
            popen.assert_not_called()

    def test_public_direct_launcher_refuses_process_creation_after_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            packet = b'{"packet":"exact"}'
            packet_path = root / "packet.json"
            packet_path.write_bytes(packet)
            child_script_path = root / "child.ps1"
            child_script = b"Write-Output '{}'"
            child_script_path.write_bytes(child_script)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=root,
                output_schema_path=root / "result.schema.json",
            )
            with patch.dict(os.environ, {"PATH": r"C:\Windows\System32"}, clear=True):
                environment = build_child_environment(
                    packet_path=packet_path,
                    packet_bytes=packet,
                    child_script_path=child_script_path,
                    child_script_bytes=child_script,
                    attempt_series_id="12345678-1234-4234-8234-123456789abc",
                    sequence_index=1,
                )
                with patch(
                    "codex_launcher_contract.validate_external_isolation_receipt",
                    return_value=[],
                ), patch("codex_launcher_contract.subprocess.Popen") as popen:
                    with self.assertRaisesRegex(RuntimeError, "direct Popen launcher is retired"):
                        launch_once(
                            preflight,
                            args,
                            packet,
                            cwd=Path("C:/workspace"),
                            additional_directory=root,
                            output_schema_path=root / "result.schema.json",
                            environment=environment,
                            attempt_guard=SingleStartGuard(),
                        )
            popen.assert_not_called()

    def test_production_launch_rejects_stale_or_mismatched_isolation_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            packet = b"packet"
            packet_path = root / "packet.json"
            packet_path.write_bytes(packet)
            child_script_path = root / "child.ps1"
            child_script = b"Write-Output '{}'"
            child_script_path.write_bytes(child_script)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=root,
                output_schema_path=root / "result.schema.json",
            )
            with patch.dict(os.environ, {"PATH": r"C:\Windows\System32"}, clear=True):
                environment = build_child_environment(
                    packet_path=packet_path,
                    packet_bytes=packet,
                    child_script_path=child_script_path,
                    child_script_bytes=child_script,
                    attempt_series_id="12345678-1234-4234-8234-123456789abc",
                    sequence_index=1,
                )
                fresh = self.isolation_receipt(
                    preflight,
                    packet,
                    packet_path,
                    Path("C:/workspace"),
                    root,
                )
                stale = self.isolation_receipt(
                    preflight,
                    packet,
                    packet_path,
                    Path("C:/workspace"),
                    root,
                    current_time=datetime.now(timezone.utc) - timedelta(minutes=10),
                )
                cases = {
                    "stale": stale,
                    "executable": self.mutate_isolation_receipt(
                        fresh,
                        selected_executable_sha256="0" * 64,
                    ),
                    "packet": self.mutate_isolation_receipt(
                        fresh,
                        packet_length_bytes=len(packet) + 1,
                    ),
                    "read_roots": self.mutate_isolation_receipt(
                        fresh,
                        reviewed_read_only_roots=("C:/different",),
                    ),
                    "network": self.mutate_isolation_receipt(
                        fresh,
                        tool_subprocess_network_denied=False,
                    ),
                    "independence": self.mutate_isolation_receipt(
                        fresh,
                        independently_verified=False,
                    ),
                    "provider": self.mutate_isolation_receipt(
                        fresh,
                        provider_production_eligible=False,
                    ),
                    "control_plane": self.mutate_isolation_receipt(
                        fresh,
                        codex_control_plane_network_scope="unrestricted",
                    ),
                    "process_creation": self.mutate_isolation_receipt(
                        fresh,
                        process_creation_controlled=False,
                    ),
                    "credentials": self.mutate_isolation_receipt(
                        fresh,
                        credential_access_denied=False,
                    ),
                    "user_profile": self.mutate_isolation_receipt(
                        fresh,
                        user_profile_access_denied=False,
                    ),
                }
                for case_name, receipt in cases.items():
                    guard = SingleStartGuard()
                    with self.subTest(case=case_name), patch(
                        "codex_launcher_contract.subprocess.Popen"
                    ) as popen:
                        with self.assertRaisesRegex(ValueError, "OS isolation evidence"):
                            launch_once(
                                preflight,
                                args,
                                packet,
                                cwd=Path("C:/workspace"),
                                additional_directory=root,
                                output_schema_path=root / "result.schema.json",
                                environment=environment,
                                attempt_guard=guard,
                                external_isolation_receipt=receipt,
                                verification_context=None,
                            )
                        self.assertFalse(guard.consumed)
                        popen.assert_not_called()

    def test_launch_starts_once_and_records_content_free_hash_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            process = FakeProcess()
            factory_calls = 0

            def factory(*factory_args, **factory_kwargs):
                nonlocal factory_calls
                factory_calls += 1
                self.assertFalse(factory_kwargs["shell"])
                return process

            packet = b'{"packet":"exact"}'
            guard = SingleStartGuard()
            environment = self.environment_for_packet(
                packet,
                {"PATH": r"C:\Windows\System32"},
            )
            outcome = _launch_once_for_test(
                preflight,
                args,
                packet,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=environment,
                attempt_guard=guard,
                popen_factory=factory,
                clock=lambda: OBSERVED,
            )
            receipt = outcome.receipt
            self.assertEqual(factory_calls, 1)
            self.assertEqual(process.communicate_calls, 1)
            self.assertEqual(receipt["process_start_count"], 1)
            self.assertFalse(receipt["relaunch_attempted"])
            self.assertEqual(receipt["launch_backend"], "internal_test_backend")
            self.assertFalse(receipt["production_eligible"])
            self.assertIsNone(receipt["external_isolation_receipt_digest"])
            self.assertEqual(receipt["payload_sha256"], hashlib.sha256(packet).hexdigest())
            self.assertEqual(receipt["stdout_length_bytes"], len(b"typed-jsonl"))
            self.assertNotIn("stdout", receipt)
            self.assertNotIn("stderr", receipt)
            self.assertEqual(outcome.stdout_bytes, b"typed-jsonl")
            self.assertEqual(validate_launch_receipt(receipt), [])

            direct_receipt = dict(receipt)
            direct_receipt["launch_backend"] = "subprocess_popen"
            direct_receipt["production_eligible"] = True
            direct_receipt = launcher_contract.with_self_digest(direct_receipt)
            self.assertTrue(
                any(
                    "direct Popen backend must be production ineligible" in error
                    for error in validate_launch_receipt(direct_receipt)
                )
            )

            broker_receipt = dict(receipt)
            broker_receipt["launch_backend"] = "windows_isolation_broker"
            broker_receipt["production_eligible"] = True
            broker_receipt = launcher_contract.with_self_digest(broker_receipt)
            self.assertIn(
                launcher_contract.BROKER_RECEIPT_CHAIN_UNAVAILABLE_ERROR,
                validate_launch_receipt(broker_receipt),
            )
            self.assertEqual(
                validate_launch_receipt_against_context(
                    receipt,
                    preflight=preflight,
                    cwd=Path("C:/workspace"),
                    additional_directory=Path("C:/temporary"),
                    output_schema_path=Path("C:/temporary/result.schema.json"),
                    packet_bytes=packet,
                    child_environment=environment,
                    stdout_bytes=outcome.stdout_bytes,
                    stderr_bytes=outcome.stderr_bytes,
                ),
                [],
            )

            blocked = _launch_once_for_test(
                preflight,
                args,
                packet,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=environment,
                attempt_guard=guard,
                popen_factory=factory,
                clock=lambda: OBSERVED,
            ).receipt
            self.assertEqual(factory_calls, 1)
            self.assertEqual(blocked["sanitized_error_code"], "process_start_already_attempted")
            self.assertEqual(validate_launch_receipt(blocked), [])

    def test_process_start_failure_never_claims_a_start_or_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            factory_calls = 0

            def factory(*factory_args, **factory_kwargs):
                nonlocal factory_calls
                factory_calls += 1
                raise OSError("synthetic start failure")

            guard = SingleStartGuard()
            outcome = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=guard,
                popen_factory=factory,
                clock=lambda: OBSERVED,
            )
            receipt = outcome.receipt
            self.assertEqual(factory_calls, 1)
            self.assertEqual(receipt["process_start_count"], 0)
            self.assertEqual(receipt["sanitized_error_code"], "process_start_failed")
            self.assertFalse(receipt["relaunch_attempted"])
            self.assertEqual(validate_launch_receipt(receipt), [])

            blocked = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=guard,
                popen_factory=factory,
                clock=lambda: OBSERVED,
            ).receipt
            self.assertEqual(factory_calls, 1)
            self.assertEqual(blocked["sanitized_error_code"], "process_start_already_attempted")

    def test_argument_tamper_blocks_before_process_start(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            args[args.index("read-only")] = "danger-full-access"
            factory_calls = 0

            def factory(*factory_args, **factory_kwargs):
                nonlocal factory_calls
                factory_calls += 1
                return FakeProcess()

            receipt = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=SingleStartGuard(),
                popen_factory=factory,
                clock=lambda: OBSERVED,
            ).receipt
            self.assertEqual(factory_calls, 0)
            self.assertEqual(receipt["process_start_count"], 0)
            self.assertEqual(receipt["sanitized_error_code"], "exact_argument_array_mismatch")
            self.assertEqual(validate_launch_receipt(receipt), [])

    def test_executable_drift_blocks_before_process_start(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            Path(preflight["selected_executable"]["path"]).write_bytes(b"changed-cli")
            factory_calls = 0

            def factory(*factory_args, **factory_kwargs):
                nonlocal factory_calls
                factory_calls += 1
                return FakeProcess()

            receipt = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=SingleStartGuard(),
                popen_factory=factory,
                clock=lambda: OBSERVED,
            ).receipt
            self.assertEqual(factory_calls, 0)
            self.assertEqual(receipt["process_start_count"], 0)
            self.assertEqual(receipt["sanitized_error_code"], "executable_binding_changed")
            self.assertEqual(validate_launch_receipt(receipt), [])

    def test_timeout_kills_same_process_without_a_second_start(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            process = TimeoutProcess()
            factory_calls = 0

            def factory(*factory_args, **factory_kwargs):
                nonlocal factory_calls
                factory_calls += 1
                return process

            outcome = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=SingleStartGuard(),
                timeout_seconds=1,
                popen_factory=factory,
                clock=lambda: OBSERVED,
            )
            self.assertEqual(factory_calls, 1)
            self.assertEqual(process.communicate_calls, 2)
            self.assertEqual(outcome.receipt["process_start_count"], 1)
            self.assertTrue(outcome.receipt["timed_out"])
            self.assertEqual(outcome.receipt["sanitized_error_code"], "child_timeout")
            self.assertEqual(outcome.stderr_bytes, b"timed-out")
            self.assertEqual(validate_launch_receipt(outcome.receipt), [])

    def test_raw_environment_is_rejected_before_guard_or_popen(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            guard = SingleStartGuard()
            calls = 0

            def factory(*factory_args, **factory_kwargs):
                nonlocal calls
                calls += 1
                return FakeProcess()

            with self.assertRaises(ValueError):
                _launch_once_for_test(
                    preflight,
                    args,
                    b"packet",
                    cwd=Path("C:/workspace"),
                    additional_directory=Path("C:/temporary"),
                    output_schema_path=Path("C:/temporary/result.schema.json"),
                    environment={},  # type: ignore[arg-type]
                    attempt_guard=guard,
                    popen_factory=factory,
                )
            forged_entries = (("GH_TOKEN", "secret"),)
            forged = ChildEnvironment(
                policy_id=CHILD_ENVIRONMENT_POLICY,
                source_provenance="internal_test_fixture",
                safe_os_source_digest=canonical_digest(
                    {
                        "source_provenance": "internal_test_fixture",
                        "safe_os_values": {},
                    }
                ),
                entries=forged_entries,
                digest=canonical_digest(
                    {
                        "policy_id": CHILD_ENVIRONMENT_POLICY,
                        "source_provenance": "internal_test_fixture",
                        "safe_os_source_digest": canonical_digest(
                            {
                                "source_provenance": "internal_test_fixture",
                                "safe_os_values": {},
                            }
                        ),
                        "values": dict(forged_entries),
                    }
                ),
                source_key_count=1,
                retained_source_key_count=0,
                dropped_source_key_count=1,
                sensitive_source_key_count=1,
                binding_key_count=0,
            )
            with self.assertRaises(ValueError):
                _launch_once_for_test(
                    preflight,
                    args,
                    b"packet",
                    cwd=Path("C:/workspace"),
                    additional_directory=Path("C:/temporary"),
                    output_schema_path=Path("C:/temporary/result.schema.json"),
                    environment=forged,
                    attempt_guard=guard,
                    popen_factory=factory,
                )
            self.assertFalse(guard.consumed)
            self.assertEqual(calls, 0)

    def test_post_start_io_failure_is_not_mislabeled_as_start_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            process = CommunicateErrorProcess()
            outcome = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=SingleStartGuard(),
                popen_factory=lambda *args, **kwargs: process,
                clock=lambda: OBSERVED,
            )
            self.assertEqual(outcome.receipt["process_start_count"], 1)
            self.assertEqual(outcome.receipt["sanitized_error_code"], "child_io_failed")
            self.assertEqual(validate_launch_receipt(outcome.receipt), [])

    def test_invalid_post_start_state_is_cleaned_up_without_relaunch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            process = InvalidStateProcess()
            outcome = _launch_once_for_test(
                preflight,
                args,
                b"packet",
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=self.environment_for_packet(b"packet"),
                attempt_guard=SingleStartGuard(),
                popen_factory=lambda *factory_args, **factory_kwargs: process,
                clock=lambda: OBSERVED,
            )
            self.assertTrue(process.killed)
            self.assertEqual(process.communicate_calls, 1)
            self.assertEqual(outcome.receipt["process_start_count"], 1)
            self.assertEqual(
                outcome.receipt["sanitized_error_code"],
                "child_process_state_invalid",
            )
            self.assertEqual(validate_launch_receipt(outcome.receipt), [])

    def test_context_validator_rejects_redigested_binding_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            preflight = self.ready_preflight(root)
            args = build_codex_exec_args(
                preflight,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
            )
            packet = b"packet"
            environment = self.environment_for_packet(
                packet,
                {"TEMP": r"C:\Temp"},
            )
            outcome = _launch_once_for_test(
                preflight,
                args,
                packet,
                cwd=Path("C:/workspace"),
                additional_directory=Path("C:/temporary"),
                output_schema_path=Path("C:/temporary/result.schema.json"),
                environment=environment,
                attempt_guard=SingleStartGuard(),
                popen_factory=lambda *factory_args, **factory_kwargs: FakeProcess(),
                clock=lambda: OBSERVED,
            )
            mutations = {
                "preflight_digest": "0" * 64,
                "payload_sha256": "1" * 64,
                "environment_digest": "2" * 64,
                "executable_sha256": "3" * 64,
                "exact_argument_array": args[:-1],
                "started_at": "not-a-timestamp",
                "single_start_guard_consume_attempted": False,
            }
            for field_name, value in mutations.items():
                tampered = deepcopy(outcome.receipt)
                tampered[field_name] = value
                unsigned = dict(tampered)
                unsigned.pop("digest")
                tampered["digest"] = canonical_digest(unsigned)
                with self.subTest(field=field_name):
                    self.assertTrue(
                        validate_launch_receipt_against_context(
                            tampered,
                            preflight=preflight,
                            cwd=Path("C:/workspace"),
                            additional_directory=Path("C:/temporary"),
                            output_schema_path=Path("C:/temporary/result.schema.json"),
                            packet_bytes=packet,
                            child_environment=environment,
                            stdout_bytes=outcome.stdout_bytes,
                            stderr_bytes=outcome.stderr_bytes,
                        )
                    )
            false_nonzero = deepcopy(outcome.receipt)
            false_nonzero.update(
                {
                    "status": "failed",
                    "first_failed_stage": "child_process",
                    "sanitized_error_code": "child_exit_nonzero",
                    "exit_code": 0,
                }
            )
            unsigned = dict(false_nonzero)
            unsigned.pop("digest")
            false_nonzero["digest"] = canonical_digest(unsigned)
            self.assertTrue(
                any(
                    "nonzero integer exit_code" in error
                    for error in validate_launch_receipt(false_nonzero)
                )
            )


def _broker_self_digest(value: dict[str, object]) -> dict[str, object]:
    result = dict(value)
    result.pop("digest", None)
    result["digest"] = canonical_digest(result)
    return result


def _broker_receipt_base(schema: str) -> dict[str, object]:
    return {
        "schema_version": schema,
        "attestation_domain": launcher_contract.BROKER_RECEIPT_DOMAINS[schema],
        "attestation_algorithm": "hmac-sha256",
        "attestation_key_id": "1" * 64,
        "verifier_identity": (
            "mythic_edge_role_pool_windows_isolation_verifier_service.v1"
        ),
        "evidence_source": "windows_kernel_appcontainer_job_acl_network_state.v1",
        "attestation": "2" * 64,
    }


def _broker_file(path: str, marker: str) -> dict[str, object]:
    return {"path": path, "sha256": marker * 64, "length_bytes": 10}


def _broker_policy(name: str) -> dict[str, object]:
    return {"policy_id": f"{name}.v1", "digest": "b" * 64}


def _synthetic_broker_chain() -> tuple[dict[str, object], bytes, bytes]:
    entries = {
        "MYTHIC_EDGE_ROLE_POOL_PACKET_PATH": "C:\\synthetic\\packet.json",
        "MYTHIC_EDGE_ROLE_POOL_PACKET_SHA256": "a" * 64,
    }
    request = _broker_self_digest(
        {
            "schema_version": launcher_contract.BROKER_LAUNCH_REQUEST_SCHEMA_VERSION,
            "launch_id": "launch:11111111111111111111111111111111",
            "authority_digest": "3" * 64,
            "attempt_series_id": "attempt:11111111111111111111111111111111",
            "sequence_index": 1,
            "idempotency_key": "idempotency:11111111111111111111111111111111",
            "current_request_digest": "f" * 64,
            "canary_exception_digest": "c" * 64,
            "expires_at": "2026-07-15T12:05:00.000Z",
            "broker_epoch": "broker-epoch:11111111111111111111111111111111",
            "verifier_epoch": "verifier-epoch:11111111111111111111111111111111",
            "launcher_identity": "codex:broker-single-start/v1",
            "broker_identity": "mythic_edge_role_pool_windows_isolation_broker.v1",
            "verifier_identity": (
                "mythic_edge_role_pool_windows_isolation_verifier_service.v1"
            ),
            "launcher_preflight_digest": "4" * 64,
            "executable": _broker_file("C:\\synthetic\\codex.exe", "5"),
            "cli_version": "codex-cli 1.0.0",
            "arguments": ["exec", "--ephemeral"],
            "arguments_digest": canonical_digest(["exec", "--ephemeral"]),
            "packet": _broker_file("C:\\synthetic\\packet.json", "a"),
            "packet_bytes_equal_stdin": True,
            "output_schema": _broker_file("C:\\synthetic\\schema.json", "6"),
            "child_script": _broker_file("C:\\synthetic\\child.py", "7"),
            "working_directory": "C:\\synthetic",
            "allowed_namespace_root": "C:\\synthetic",
            "read_only_roots": ["C:\\synthetic"],
            "writable_temp_root": "C:\\synthetic\\writable",
            "writable_cleanup_required": True,
            "denied_repository_policy": _broker_policy("denied-repository"),
            "appcontainer_sid": "S-1-15-2-1",
            "child_environment": {
                "keys": sorted(entries),
                "entries": entries,
                "digest": canonical_digest(entries),
                "credential_like_values_present": False,
                "user_profile_access": False,
            },
            "policies": {
                name: _broker_policy(name)
                for name in (
                    "token",
                    "appcontainer",
                    "job",
                    "handle",
                    "filesystem",
                    "network",
                    "process_count",
                    "timeout",
                    "control_plane",
                )
            },
            "root_workload_count": 1,
            "allowed_tool_descendant_count": 1,
            "nested_agent_allowed": False,
            "relaunch_allowed": False,
            "shell_mediation": False,
            "intended_use": "stage4_evidence_only",
        }
    )
    reservation = _broker_self_digest(
        _broker_receipt_base(launcher_contract.BROKER_RESERVATION_SCHEMA_VERSION)
        | {
            "launch_id": request["launch_id"],
            "launch_request_digest": request["digest"],
            "authority_digest": request["authority_digest"],
            "attempt_series_id": request["attempt_series_id"],
            "sequence_index": 1,
            "idempotency_key": request["idempotency_key"],
            "broker_epoch": request["broker_epoch"],
            "verifier_epoch": request["verifier_epoch"],
            "reservation_id": "reservation:11111111111111111111111111111111",
            "reservation_status": "reserved_not_started",
            "observed_at": "2026-07-15T12:00:00.000Z",
            "expires_at": "2026-07-15T12:05:00.000Z",
        }
    )
    boundary = _broker_self_digest(
        _broker_receipt_base(launcher_contract.BROKER_BOUNDARY_SCHEMA_VERSION)
        | {
            "launch_id": request["launch_id"],
            "launch_request_digest": request["digest"],
            "start_reservation_digest": reservation["digest"],
            "boundary_receipt_id": "boundary:11111111111111111111111111111111",
            "broker_identity": {
                "service_sid": "S-1-5-80-1234",
                "scm_process_id": 42,
                "pipe_server_process_id": 42,
                "process_creation_time_utc_ticks": 638881344000000000,
                "binary_path": "C:\\synthetic\\broker.exe",
                "binary_sha256": "8" * 64,
                "binary_length_bytes": 10,
                "signer_sha256": "9" * 64,
                "installation_id": "installation:11111111111111111111111111111111",
                "provider_id": (
                    "mythic_edge_role_pool_windows_isolation_broker.v1"
                ),
                "broker_epoch": request["broker_epoch"],
                "restricted_service_configuration": True,
            },
            "verifier_service_sid": "S-1-5-80-1",
            "verifier_installation_id": "installation:11111111111111111111111111111111",
            "verifier_epoch": request["verifier_epoch"],
            "process_identity": "101:638881344000000000",
            "bindings_digest": "6" * 64,
            "observed_boundary": {
                "executable_path": request["executable"]["path"],
                "executable_sha256": request["executable"]["sha256"],
                "executable_length_bytes": request["executable"]["length_bytes"],
                "primary_thread_suspended": True,
                "process_created_count": 1,
                "process_resumed_count": 0,
                "final_job_membership": True,
                "restricted_token": True,
                "appcontainer_token": True,
                "appcontainer_identity_exact": True,
                "network_capabilities_absent": True,
                "namespace_no_reparse": True,
                "namespace_acl_read_only": True,
                "writable_root_scoped": True,
                "writable_acl_scoped": True,
                "job_no_breakaway": True,
                "job_kill_on_close": True,
                "explicit_inherited_handle_set": True,
                "process_limit_enforced": True,
            },
            "observed_at": "2026-07-15T12:00:01.000Z",
            "expires_at": "2026-07-15T12:05:00.000Z",
        }
    )
    start = _broker_self_digest(
        _broker_receipt_base(launcher_contract.BROKER_START_SCHEMA_VERSION)
        | {
            "launch_id": request["launch_id"],
            "launch_request_digest": request["digest"],
            "start_reservation_digest": reservation["digest"],
            "boundary_ready_receipt_digest": boundary["digest"],
            "process_identity": boundary["process_identity"],
            "process_created_count": 1,
            "process_resumed_count": 1,
            "relaunch_attempted": False,
            "start_time": "2026-07-15T12:00:02.000Z",
            "post_resume_observation_digest": "7" * 64,
            "observed_at": "2026-07-15T12:00:02.000Z",
        }
    )
    stdout = b"synthetic"
    stderr = b""
    terminal = _broker_self_digest(
        _broker_receipt_base(launcher_contract.BROKER_TERMINAL_SCHEMA_VERSION)
        | {
            "launch_id": request["launch_id"],
            "launch_request_digest": request["digest"],
            "start_receipt_digest": start["digest"],
            "process_identity": boundary["process_identity"],
            "terminal_status": "completed",
            "terminal_reason": "process_exit",
            "completed_at": "2026-07-15T12:00:03.000Z",
            "exit_code": 0,
            "timed_out": False,
            "cancelled": False,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stdout_length_bytes": len(stdout),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stderr_length_bytes": len(stderr),
            "job_termination_result": "not_required_empty",
            "cleanup_result": "temporary_scope_removed",
            "process_created_count": 1,
            "process_resumed_count": 1,
            "relaunch_attempted": False,
            "final_process_count": 0,
            "remaining_tracked_process_count": 0,
            "remaining_temporary_file_count": 0,
            "observed_at": "2026-07-15T12:00:03.000Z",
        }
    )
    chain = {
        "schema_version": launcher_contract.BROKER_RECEIPT_CHAIN_SCHEMA_VERSION,
        "launch_request": request,
        "reservation_receipt": reservation,
        "boundary_ready_receipt": boundary,
        "start_receipt": start,
        "terminal_receipt": terminal,
        "abort_receipt": None,
    }
    return chain, stdout, stderr


class _SyntheticBrokerChain:
    def __init__(self) -> None:
        self.document, self.stdout_bytes, self.stderr_bytes = _synthetic_broker_chain()

    def as_document(self) -> dict[str, object]:
        return deepcopy(self.document)


class _SyntheticBrokerClient:
    def __init__(self) -> None:
        self.chain = _SyntheticBrokerChain()
        self.calls = 0

    def start_once(self, launch_request: dict[str, object]) -> _SyntheticBrokerChain:
        self.calls += 1
        self.chain.document["launch_request"] = deepcopy(launch_request)
        request_digest = launch_request["digest"]
        boundary = self.chain.document["boundary_ready_receipt"]
        assert isinstance(boundary, dict)
        observed_boundary = boundary["observed_boundary"]
        executable = launch_request["executable"]
        assert isinstance(observed_boundary, dict)
        assert isinstance(executable, dict)
        observed_boundary.update(
            {
                "executable_path": executable["path"],
                "executable_sha256": executable["sha256"],
                "executable_length_bytes": executable["length_bytes"],
            }
        )
        for key in (
            "reservation_receipt",
            "boundary_ready_receipt",
            "start_receipt",
            "terminal_receipt",
        ):
            receipt = self.chain.document[key]
            assert isinstance(receipt, dict)
            receipt["launch_request_digest"] = request_digest
            redigested = _broker_self_digest(
                {name: value for name, value in receipt.items() if name != "digest"}
            )
            receipt.clear()
            receipt.update(redigested)
        reservation = self.chain.document["reservation_receipt"]
        boundary = self.chain.document["boundary_ready_receipt"]
        start = self.chain.document["start_receipt"]
        terminal = self.chain.document["terminal_receipt"]
        boundary["start_reservation_digest"] = reservation["digest"]
        boundary.update(_broker_self_digest({k: v for k, v in boundary.items() if k != "digest"}))
        start["start_reservation_digest"] = reservation["digest"]
        start["boundary_ready_receipt_digest"] = boundary["digest"]
        start.update(_broker_self_digest({k: v for k, v in start.items() if k != "digest"}))
        terminal["start_receipt_digest"] = start["digest"]
        terminal.update(_broker_self_digest({k: v for k, v in terminal.items() if k != "digest"}))
        return self.chain

    def verify_current_chain(self, chain: object) -> bool:
        return chain is self.chain


class _SyntheticAbortingBrokerClient(_SyntheticBrokerClient):
    def start_once(self, launch_request: dict[str, object]) -> _SyntheticBrokerChain:
        chain = super().start_once(launch_request)
        reservation = chain.document["reservation_receipt"]
        assert isinstance(reservation, dict)
        chain.document["boundary_ready_receipt"] = None
        chain.document["start_receipt"] = None
        chain.document["terminal_receipt"] = None
        chain.document["abort_receipt"] = _broker_self_digest(
            _broker_receipt_base(launcher_contract.BROKER_ABORT_SCHEMA_VERSION)
            | {
                "launch_id": launch_request["launch_id"],
                "launch_request_digest": launch_request["digest"],
                "start_reservation_digest": reservation["digest"],
                "latest_receipt_digest": reservation["digest"],
                "process_identity": None,
                "abort_state": "definitive_not_started",
                "first_failed_stage": "boundary_construction",
                "sanitized_reason": "source_binding_invalid",
                "process_created_count": 0,
                "process_resumed_count": 0,
                "relaunch_attempted": False,
                "termination_observed": True,
                "zero_survivors_observed": True,
                "cleanup_result": "cleanup_completed",
                "observed_at": "2026-07-15T12:00:01.000Z",
            }
        )
        chain.stdout_bytes = b""
        chain.stderr_bytes = b""
        return chain


class BrokerLauncherContractTests(unittest.TestCase):
    def test_broker_launch_path_returns_strict_v3_receipt_without_popen(self) -> None:
        chain, _stdout, _stderr = _synthetic_broker_chain()
        request = chain["launch_request"]
        client = _SyntheticBrokerClient()
        with patch("codex_launcher_contract.subprocess.Popen") as popen:
            outcome = launcher_contract._broker_launch_once_for_test(
                request,
                broker_client=client,
            )
        popen.assert_not_called()
        self.assertEqual(client.calls, 1)
        self.assertEqual(
            outcome.receipt["schema_version"],
            launcher_contract.BROKER_LAUNCH_RECEIPT_SCHEMA_VERSION,
        )
        self.assertEqual(validate_launch_receipt(outcome.receipt), [])
        self.assertIsNotNone(outcome.broker_verification_context)

    def test_broker_chain_tampering_is_rejected(self) -> None:
        chain, _stdout, _stderr = _synthetic_broker_chain()
        chain["start_receipt"]["process_resumed_count"] = 2
        self.assertTrue(launcher_contract.validate_broker_receipt_chain(chain))

    def test_broker_chain_rejects_abbreviated_or_caller_selected_boundary(self) -> None:
        chain, _stdout, _stderr = _synthetic_broker_chain()
        del chain["launch_request"]["policies"]
        chain["launch_request"] = _broker_self_digest(chain["launch_request"])
        self.assertTrue(launcher_contract.validate_broker_receipt_chain(chain))

        chain, _stdout, _stderr = _synthetic_broker_chain()
        chain["boundary_ready_receipt"]["observed_boundary"][
            "network_capabilities_absent"
        ] = False
        chain["boundary_ready_receipt"] = _broker_self_digest(
            chain["boundary_ready_receipt"]
        )
        self.assertTrue(launcher_contract.validate_broker_receipt_chain(chain))

    def test_broker_abort_is_preserved_as_symbolic_failed_receipt(self) -> None:
        chain, _stdout, _stderr = _synthetic_broker_chain()
        outcome = launcher_contract._broker_launch_once_for_test(
            chain["launch_request"],
            broker_client=_SyntheticAbortingBrokerClient(),
        )
        self.assertEqual(outcome.receipt["status"], "failed")
        self.assertEqual(outcome.receipt["process_start_count"], 0)
        self.assertEqual(
            outcome.receipt["sanitized_error_code"], "source_binding_invalid"
        )
        self.assertEqual(validate_launch_receipt(outcome.receipt), [])

    def test_broker_context_is_not_caller_constructible_or_serializable(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "not caller-constructible"):
            launcher_contract.BrokerVerificationContext()
        chain, _stdout, _stderr = _synthetic_broker_chain()
        outcome = launcher_contract._broker_launch_once_for_test(
            chain["launch_request"],
            broker_client=_SyntheticBrokerClient(),
        )
        with self.assertRaisesRegex(TypeError, "cannot be serialized"):
            pickle.dumps(outcome.broker_verification_context)

    def test_public_direct_launcher_still_never_calls_popen(self) -> None:
        source = inspect.getsource(launch_once)
        self.assertNotIn("subprocess.Popen", source)
        self.assertNotIn("popen_factory", source)


if __name__ == "__main__":
    unittest.main()
