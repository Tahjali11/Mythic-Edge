from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime, timezone
from typing import Iterable, Mapping

import trusted_native_app_server_adapter as app_server

SHA = "a" * 64
NOW = datetime(2026, 7, 29, 12, 0, 0, tzinfo=timezone.utc)


def _lane(role: str = "B") -> dict[str, object]:
    return app_server.with_self_digest(
        {
            "lane_id": "lane.1",
            "repository_id": 1,
            "canonical_name": "tahjali11/mythic-edge",
            "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/758",
            "role": role,
            "operation_id": "inspect",
            "base_ref": "refs/heads/main",
            "base_sha": "b" * 40,
            "predecessor_packet_sha256": None,
            "command_ids": [],
            "read_scope": ["docs"],
            "mutation_scope": [],
            "protected_surfaces": ["native_task_launch"],
            "validation_command_ids": [],
            "expected_artifact_paths": [],
            "stop_conditions": ["Stop on authority drift."],
            "lane_packet_sha256": "",
        },
        "lane_packet_sha256",
    )


def _task_request(
    role: str = "B",
    *,
    lane: Mapping[str, object] | None = None,
) -> dict[str, object]:
    selected_lane = dict(lane or _lane(role))
    return app_server.with_self_digest(
        {
            "schema_version": "trusted_owner_native_task_request.v1",
            "request_sha256": "1" * 64,
            "claim_observation_sha256": "2" * 64,
            "lane_packet_sha256": selected_lane["lane_packet_sha256"],
            "repository_id": 1,
            "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/758",
            "role": role,
            "base_sha": "b" * 40,
            "worktree_observation_sha256": "4" * 64,
            "context_mode": "isolated_packet_only",
            "fork_turns": "none",
            "issued_at_utc": "2026-07-29T12:00:00Z",
            "task_request_sha256": "",
        },
        "task_request_sha256",
    )


def _instruction_packet(
    task_request: Mapping[str, object],
    lane: Mapping[str, object],
) -> dict[str, object]:
    return app_server.seal_instruction_packet(
        {
            "schema_version": app_server.INSTRUCTION_PACKET_SCHEMA,
            "task_request_sha256": task_request["task_request_sha256"],
            "lane_packet_sha256": lane["lane_packet_sha256"],
            "role": task_request["role"],
            "operation_id": lane["operation_id"],
            "issue_url": task_request["issue_url"],
            "predecessor_packet_sha256": lane["predecessor_packet_sha256"],
            "role_contract_path": (
                app_server.ROLE_CONTRACT_PATHS[str(task_request["role"])]
            ),
            "role_contract_sha256": "6" * 64,
            "role_pool_skill_sha256": "c" * 64,
            "output_schema_sha256": app_server.ROLE_OUTPUT_SCHEMA_SHA256,
            "lane_packet_json": app_server.canonical_json_bytes(
                lane,
                final_lf=True,
            ).decode("utf-8"),
            "predecessor_packet_json": None,
            "instruction_packet_sha256": "",
        }
    )


def _execution_binding(
    role: str = "B",
    *,
    task_request: Mapping[str, object] | None = None,
    instruction_packet: Mapping[str, object] | None = None,
) -> dict[str, object]:
    request = dict(task_request or _task_request(role))
    lane = _lane(role)
    packet = dict(instruction_packet or _instruction_packet(request, lane))
    return app_server.seal_execution_binding(
        {
            "schema_version": app_server.EXECUTION_BINDING_SCHEMA,
            "profile_contract_sha256": app_server.PROFILE_CONTRACT_SHA256,
            "companion_contract_sha256": app_server.COMPANION_CONTRACT_SHA256,
            "task_request_sha256": request["task_request_sha256"],
            "request_sha256": request["request_sha256"],
            "claim_observation_sha256": request["claim_observation_sha256"],
            "lane_packet_sha256": request["lane_packet_sha256"],
            "worktree_observation_sha256": request["worktree_observation_sha256"],
            "registry_sha256": "6" * 64,
            "release_state_record_sha256": "7" * 64,
            "skill_tree_sha256": "8" * 64,
            "repository_id": 1,
            "issue_url": request["issue_url"],
            "role": role,
            "operation_id": "inspect",
            "predecessor_packet_sha256": None,
            "cwd_identity_sha256": "9" * 64,
            "model_request_mode": "platform_default_then_bind_thread_response",
            "requested_model": None,
            "requested_effort": None,
            "sandbox_binding_sha256": "a" * 64,
            "approval_policy": "untrusted",
            "role_instruction_sha256": app_server.DEVELOPER_INSTRUCTION_SHA256,
            "instruction_packet_sha256": packet["instruction_packet_sha256"],
            "role_pool_skill_sha256": "c" * 64,
            "output_schema_sha256": app_server.ROLE_OUTPUT_SCHEMA_SHA256,
            "installation_receipt_sha256": "d" * 64,
            "executable_sha256": app_server.PINNED_EXECUTABLE_SHA256,
            "protocol_schema_sha256": app_server.PINNED_PROTOCOL_SCHEMA_SHA256,
            "runtime_config_manifest_sha256": "e" * 64,
            "environment_binding_sha256": "f" * 64,
            "turn_timeout_seconds": 120,
        }
    )


def _registry_entry() -> dict[str, object]:
    return {
        "repository_id": 1,
        "repository_code_execution_policy": "forbidden",
        "maximum_mutation_scope": [],
        "approved_commands": [],
    }


def _private_context() -> app_server.SyntheticPrivateContext:
    return app_server.SyntheticPrivateContext(
        cwd="C:\\synthetic\\worktree",
        codex_home="C:\\synthetic\\codex-home",
        skill_path="C:\\synthetic\\skills\\mythic-edge-role-pool\\SKILL.md",
        agents_path="C:\\synthetic\\worktree\\AGENTS.md",
        agents_sha256="0" * 64,
    )


def _role_output(
    *,
    result: str = "completed",
    status: str = "complete",
) -> dict[str, object]:
    return {
        "schema_version": app_server.ROLE_OUTPUT_SCHEMA_VERSION,
        "result": result,
        "files_changed": [],
        "validation": [],
        "handoff": {
            "status": status,
            "next_role": "E",
            "source_artifact_paths": ["docs/contracts/example.md"],
            "finding_ids": [],
            "stop_reason": None,
        },
    }


class ScriptedTransport:
    synthetic_only = True
    process_start_count = 0

    def __init__(
        self,
        *,
        events: Iterable[object] | None = None,
        cleanup_status: str = "complete",
    ) -> None:
        self.cleanup_status = cleanup_status
        self.requests: list[dict[str, object]] = []
        self.notifications: list[dict[str, object]] = []
        self.responses: list[dict[str, object]] = []
        self._events = list(events) if events is not None else None
        self.thread_id = "thread.synthetic.1"
        self.turn_id = "turn.synthetic.1"

    def request(self, message: Mapping[str, object]) -> object:
        copied = copy.deepcopy(dict(message))
        self.requests.append(copied)
        request_id = copied["id"]
        method = copied["method"]
        if method == "initialize":
            return {
                "id": request_id,
                "result": {
                    "platformFamily": "windows",
                    "platformOs": "windows",
                    "userAgent": "codex-cli/0.146.0",
                    "codexHome": _private_context().codex_home,
                },
            }
        if method == "thread/start":
            return {
                "id": request_id,
                "result": {
                    "thread": {
                        "id": self.thread_id,
                        "ephemeral": True,
                        "turns": [],
                        "parentThreadId": None,
                        "forkedFromThreadId": None,
                        "cwd": _private_context().cwd,
                        "approvalPolicy": "untrusted",
                        "approvalsReviewer": "user",
                        "sandbox": "read-only",
                        "model": "gpt-synthetic",
                        "reasoningEffort": "high",
                        "instructionSources": [_private_context().agents_path],
                    }
                },
            }
        if method == "turn/start":
            return {
                "id": request_id,
                "result": {
                    "turn": {
                        "id": self.turn_id,
                        "status": "inProgress",
                    }
                },
            }
        raise AssertionError(f"unexpected method: {method}")

    def notify(self, message: Mapping[str, object]) -> None:
        self.notifications.append(copy.deepcopy(dict(message)))

    def messages(self) -> Iterable[object]:
        if self._events is None:
            return iter(
                [
                    {
                        "method": "thread/started",
                        "params": {"threadId": self.thread_id},
                    },
                    {
                        "method": "turn/started",
                        "params": {
                            "threadId": self.thread_id,
                            "turnId": self.turn_id,
                        },
                    },
                    {
                        "method": "item/started",
                        "params": {
                            "threadId": self.thread_id,
                            "turnId": self.turn_id,
                            "item": {"type": "plan"},
                        },
                    },
                    {
                        "method": "turn/completed",
                        "params": {
                            "threadId": self.thread_id,
                            "turnId": self.turn_id,
                            "status": "completed",
                            "output": _role_output(),
                        },
                    },
                ]
            )
        return iter(self._events)

    def respond(self, message: Mapping[str, object]) -> None:
        self.responses.append(copy.deepcopy(dict(message)))


class TimeoutTransport(ScriptedTransport):
    def messages(self) -> Iterable[object]:
        raise app_server.FakeTransportTimeout("synthetic_timeout")


class ProcessExitTransport(ScriptedTransport):
    def messages(self) -> Iterable[object]:
        raise app_server.FakeTransportProcessExit("synthetic_process_exit")


def _run(
    transport: ScriptedTransport | None = None,
    *,
    task_request: Mapping[str, object] | None = None,
    lane: Mapping[str, object] | None = None,
    registry_entry: Mapping[str, object] | None = None,
    instruction_packet: str | None = None,
    binding: Mapping[str, object] | None = None,
) -> dict[str, object]:
    selected_lane = dict(lane or _lane())
    selected_request = dict(
        task_request or _task_request(str(selected_lane["role"]), lane=selected_lane)
    )
    packet = _instruction_packet(selected_request, selected_lane)
    packet_text = instruction_packet or app_server.canonical_json_bytes(
        packet,
        final_lf=True,
    ).decode("utf-8")
    return app_server.run_inert_app_server_once(
        task_request=selected_request,
        execution_binding=binding
        or _execution_binding(
            str(selected_request["role"]),
            task_request=selected_request,
            instruction_packet=packet,
        ),
        registry_entry=registry_entry or _registry_entry(),
        private_context=_private_context(),
        instruction_packet=packet_text,
        transport=transport or ScriptedTransport(),
        clock=lambda: NOW,
    )


class ContractBindingTests(unittest.TestCase):
    def test_fixed_contract_bytes_match_reviewed_digests(self) -> None:
        self.assertEqual(
            app_server.validate_fixed_contract_bytes(),
            {
                "developer_instruction_sha256": (app_server.DEVELOPER_INSTRUCTION_SHA256),
                "role_output_schema_sha256": app_server.ROLE_OUTPUT_SCHEMA_SHA256,
                "inspect_config_sha256": app_server.INSPECT_ONLY_CONFIG_SHA256,
            },
        )

    def test_lifecycle_registry_is_exact_and_closed(self) -> None:
        self.assertEqual(
            app_server.validate_lifecycle_registry(),
            {
                "tuple_count": 39,
                "overlap_count": 0,
                "uncovered_count": 0,
                "unreachable_row_count": 0,
                "sha256": app_server.LIFECYCLE_REGISTRY_SHA256,
            },
        )

    def test_every_lifecycle_row_selects_itself(self) -> None:
        for row in app_server.LIFECYCLE_ROWS:
            with self.subTest(ordinal=row[0]):
                selected = app_server.select_lifecycle_case(
                    row[1],
                    row[2],
                    row[3],
                )
                self.assertEqual(selected["ordinal"], row[0])
                self.assertEqual(selected["lifecycle_case"], row[4])
                self.assertEqual(selected["profile_projection"], row[5])

    def test_unknown_selector_fails_closed_by_consumption_state(self) -> None:
        self.assertEqual(
            app_server.select_lifecycle_case("bad", "bad", "not_consumed")["lifecycle_case"],
            "AS-BLK-001",
        )
        self.assertEqual(
            app_server.select_lifecycle_case("bad", "bad", "consumed")["lifecycle_case"],
            "AS-UNK-001",
        )

    def test_request_ids_are_deterministic_and_distinct(self) -> None:
        first = app_server.request_ids("a" * 64)
        second = app_server.request_ids("a" * 64)
        self.assertEqual(first, second)
        self.assertEqual(len(set(first.values())), 5)
        self.assertEqual(first["initialize"], f"rp-init-{'a' * 32}")

    def test_wire_decoder_rejects_duplicate_keys_and_bad_framing(self) -> None:
        cases = (
            b'{"a":1,"a":2}\n',
            b"\xef\xbb\xbf{}\n",
            b"{}\r\n",
            b"{}",
            b"{}\n{}\n",
        )
        for raw in cases:
            with self.subTest(raw=raw):
                with self.assertRaises(app_server.AppServerAdapterError):
                    app_server.decode_json_line(raw)

    def test_wire_decoder_accepts_one_utf8_json_line(self) -> None:
        self.assertEqual(
            app_server.decode_json_line(b'{"id":"one","value":1}\n'),
            {"id": "one", "value": 1},
        )

    def test_execution_binding_rejects_contract_or_digest_drift(self) -> None:
        binding = _execution_binding()
        self.assertEqual(app_server.validate_execution_binding(binding), [])
        for field in (
            "profile_contract_sha256",
            "companion_contract_sha256",
            "protocol_schema_sha256",
            "execution_binding_sha256",
        ):
            changed = copy.deepcopy(binding)
            changed[field] = SHA
            self.assertTrue(
                app_server.validate_execution_binding(changed),
                msg=field,
            )


class InspectOnlyBoundaryTests(unittest.TestCase):
    def test_only_b_and_e_empty_inspect_lanes_are_accepted(self) -> None:
        for role in ("B", "E"):
            with self.subTest(role=role):
                self.assertEqual(
                    app_server.validate_inspect_only_effect_boundary(
                        _task_request(role),
                        _lane(role),
                        _registry_entry(),
                        turn_timeout_seconds=120,
                    ),
                    [],
                )

    def test_role_operation_and_policy_widening_are_rejected(self) -> None:
        task_request = _task_request("A")
        lane = _lane("A")
        lane["operation_id"] = "implement"
        registry = _registry_entry()
        registry["repository_code_execution_policy"] = "reviewed_command_set_only"
        errors = app_server.validate_inspect_only_effect_boundary(
            task_request,
            lane,
            registry,
            turn_timeout_seconds=121,
        )
        self.assertIn("role_not_inspect_only", errors)
        self.assertIn("operation_not_inspect", errors)
        self.assertIn("repository_code_execution_policy_invalid", errors)
        self.assertIn("turn_timeout_invalid", errors)

    def test_every_effect_array_must_be_empty(self) -> None:
        for field in (
            "command_ids",
            "validation_command_ids",
            "mutation_scope",
            "expected_artifact_paths",
        ):
            lane = _lane()
            lane[field] = ["forbidden"]
            errors = app_server.validate_inspect_only_effect_boundary(
                _task_request(),
                lane,
                _registry_entry(),
                turn_timeout_seconds=120,
            )
            self.assertIn(f"{field}_not_empty", errors)
        for field in ("maximum_mutation_scope", "approved_commands"):
            registry = _registry_entry()
            registry[field] = ["forbidden"]
            errors = app_server.validate_inspect_only_effect_boundary(
                _task_request(),
                _lane(),
                registry,
                turn_timeout_seconds=120,
            )
            self.assertIn(f"{field}_not_empty", errors)

    def test_run_rejects_widened_effect_boundary_before_transport(self) -> None:
        lane = _lane()
        lane["mutation_scope"] = ["src"]
        lane = app_server.with_self_digest(lane, "lane_packet_sha256")
        request = _task_request(lane=lane)
        transport = ScriptedTransport()
        result = _run(
            transport,
            task_request=request,
            lane=lane,
        )
        self.assertEqual(result["lifecycle_case"], "AS-BLK-001")
        self.assertEqual(transport.requests, [])

        registry = _registry_entry()
        registry["repository_code_execution_policy"] = (
            "reviewed_command_set_only"
        )
        transport = ScriptedTransport()
        result = _run(transport, registry_entry=registry)
        self.assertEqual(result["lifecycle_case"], "AS-BLK-001")
        self.assertEqual(transport.requests, [])

    def test_run_rejects_cross_binding_and_noncanonical_instruction(self) -> None:
        binding = _execution_binding()
        changed_binding = copy.deepcopy(binding)
        changed_binding["request_sha256"] = "f" * 64
        changed_binding = app_server.seal_execution_binding(changed_binding)
        transport = ScriptedTransport()
        result = _run(transport, binding=changed_binding)
        self.assertEqual(result["lifecycle_case"], "AS-BLK-001")
        self.assertEqual(transport.requests, [])

        transport = ScriptedTransport()
        result = _run(
            transport,
            instruction_packet='{"schema_version":"synthetic_instruction.v1"}',
        )
        self.assertEqual(result["lifecycle_case"], "AS-BLK-001")
        self.assertEqual(transport.requests, [])

    def test_role_output_requires_zero_effects_and_sorted_handoff(self) -> None:
        output = _role_output()
        self.assertEqual(app_server.validate_role_output(output), [])
        output["files_changed"] = [
            {
                "path": "forbidden",
                "change_kind": "added",
                "before_sha256": None,
                "after_sha256": SHA,
            }
        ]
        self.assertIn(
            "role_output_files_changed_not_empty",
            app_server.validate_role_output(output),
        )

    def test_role_output_rejects_private_value_echo(self) -> None:
        output = _role_output(result="blocked", status="blocked")
        output["handoff"]["stop_reason"] = _private_context().cwd
        self.assertIn(
            "role_output_private_value_echo",
            app_server.validate_role_output(
                output,
                private_values=(_private_context().cwd,),
            ),
        )


class AdapterLifecycleTests(unittest.TestCase):
    def test_happy_path_is_one_synthetic_lifecycle_with_public_safe_receipts(
        self,
    ) -> None:
        transport = ScriptedTransport()
        result = _run(transport)
        self.assertEqual(
            result["status"],
            "synthetic_app_server_receipt_accepted_non_live",
        )
        self.assertEqual(result["lifecycle_case"], "AS-ACC-001")
        self.assertEqual(result["actual_process_start_count"], 0)
        self.assertEqual(result["automatic_retry_count"], 0)
        self.assertEqual(result["fallback_attempt_count"], 0)
        self.assertEqual(result["durable_write_count"], 0)
        self.assertIs(result["synthetic_only"], True)
        self.assertIs(result["live_ready"], False)
        self.assertEqual(
            [request["method"] for request in transport.requests],
            ["initialize", "thread/start", "turn/start"],
        )
        self.assertEqual(
            transport.notifications,
            [{"method": "initialized", "params": {}}],
        )
        platform = result["platform_receipt"]
        self.assertEqual(app_server.validate_platform_receipt(platform), [])
        task = result["task_receipt"]
        self.assertTrue(task["task_id"].startswith("app_server_"))
        self.assertTrue(task["platform_receipt_ref"].startswith("role_pool:app_server:"))
        public_projection = json.dumps(result, sort_keys=True)
        for private_value in (
            _private_context().cwd,
            _private_context().codex_home,
            _private_context().skill_path,
            _private_context().agents_path,
        ):
            self.assertNotIn(private_value, public_projection)

    def test_adapter_is_single_use_and_does_not_retry(self) -> None:
        transport = ScriptedTransport()
        lane = _lane()
        request = _task_request(lane=lane)
        packet = _instruction_packet(request, lane)
        adapter = app_server.TrustedNativeAppServerAdapter(
            execution_binding=_execution_binding(
                task_request=request,
                instruction_packet=packet,
            ),
            registry_entry=_registry_entry(),
            private_context=_private_context(),
            instruction_packet=app_server.canonical_json_bytes(
                packet,
                final_lf=True,
            ).decode("utf-8"),
            transport=transport,
            clock=lambda: NOW,
        )
        receipt = adapter.create_once(request)
        self.assertEqual(receipt["schema_version"], "trusted_owner_native_task_receipt.v1")
        with self.assertRaisesRegex(
            app_server.AppServerAdapterError,
            "app_server_adapter_already_used",
        ):
            adapter.create_once(request)
        self.assertEqual(len(transport.requests), 3)

    def test_invalid_accepted_input_does_not_consume_adapter(self) -> None:
        transport = ScriptedTransport()
        lane = _lane()
        request = _task_request(lane=lane)
        packet = _instruction_packet(request, lane)
        adapter = app_server.TrustedNativeAppServerAdapter(
            execution_binding=_execution_binding(
                task_request=request,
                instruction_packet=packet,
            ),
            registry_entry=_registry_entry(),
            private_context=_private_context(),
            instruction_packet=app_server.canonical_json_bytes(
                packet,
                final_lf=True,
            ).decode("utf-8"),
            transport=transport,
            clock=lambda: NOW,
        )
        changed_request = copy.deepcopy(request)
        changed_request["request_sha256"] = "f" * 64
        changed_request = app_server.with_self_digest(
            changed_request,
            "task_request_sha256",
        )

        with self.assertRaisesRegex(
            app_server.AppServerAdapterError,
            "AS-BLK-001",
        ):
            adapter.create_once(changed_request)
        self.assertEqual(transport.requests, [])

        receipt = adapter.create_once(request)
        self.assertEqual(
            receipt["schema_version"],
            "trusted_owner_native_task_receipt.v1",
        )
        self.assertEqual(len(transport.requests), 3)

    def test_non_synthetic_transport_is_rejected_before_requests(self) -> None:
        transport = ScriptedTransport()
        transport.synthetic_only = False
        result = _run(transport)
        self.assertEqual(result["lifecycle_case"], "AS-BLK-001")
        self.assertEqual(transport.requests, [])

    def test_wrong_initialize_response_id_fails_known(self) -> None:
        class WrongIdTransport(ScriptedTransport):
            def request(self, message: Mapping[str, object]) -> object:
                response = super().request(message)
                if message["method"] == "initialize":
                    response["id"] = "wrong"
                return response

        result = _run(WrongIdTransport())
        self.assertEqual(result["lifecycle_case"], "AS-KNOWN-FAIL-001")
        self.assertEqual(result["automatic_retry_count"], 0)

    def test_missing_extra_or_wrong_instruction_source_fails_before_turn(
        self,
    ) -> None:
        for sources in (
            [],
            [_private_context().agents_path, "C:\\synthetic\\extra\\AGENTS.md"],
            ["C:\\other\\AGENTS.md"],
        ):

            class SourceTransport(ScriptedTransport):
                def __init__(self, source_values: list[str]) -> None:
                    super().__init__()
                    self.source_values = source_values

                def request(self, message: Mapping[str, object]) -> object:
                    response = super().request(message)
                    if message["method"] == "thread/start":
                        response["result"]["thread"]["instructionSources"] = self.source_values
                    return response

            with self.subTest(sources=sources):
                transport = SourceTransport(sources)
                result = _run(transport)
                self.assertEqual(result["lifecycle_case"], "AS-KNOWN-FAIL-001")
                self.assertEqual(
                    [row["method"] for row in transport.requests],
                    ["initialize", "thread/start"],
                )

    def test_model_and_effort_are_bound_from_thread_response_into_turn(self) -> None:
        transport = ScriptedTransport()
        result = _run(transport)
        self.assertEqual(result["lifecycle_case"], "AS-ACC-001")
        turn_params = transport.requests[2]["params"]
        self.assertEqual(turn_params["model"], "gpt-synthetic")
        self.assertEqual(turn_params["effort"], "high")
        self.assertIsNone(transport.requests[1]["params"]["model"])

    def test_command_approval_is_declined_and_policy_breach_is_terminal(
        self,
    ) -> None:
        transport = ScriptedTransport(
            events=[
                {
                    "id": "server-request-1",
                    "method": "item/commandExecution/requestApproval",
                    "params": {
                        "threadId": "thread.synthetic.1",
                        "turnId": "turn.synthetic.1",
                    },
                }
            ]
        )
        result = _run(transport)
        self.assertEqual(result["lifecycle_case"], "AS-POL-001")
        self.assertEqual(
            transport.responses,
            [{"id": "server-request-1", "result": {"decision": "decline"}}],
        )
        self.assertEqual(result["automatic_retry_count"], 0)
        self.assertEqual(result["fallback_attempt_count"], 0)

    def test_file_change_command_and_diff_items_are_policy_breaches(self) -> None:
        for item_type in ("fileChange", "commandExecution", "patch", "diff"):
            transport = ScriptedTransport(
                events=[
                    {
                        "method": "item/started",
                        "params": {
                            "threadId": "thread.synthetic.1",
                            "turnId": "turn.synthetic.1",
                            "item": {"type": item_type},
                        },
                    }
                ]
            )
            with self.subTest(item_type=item_type):
                self.assertEqual(_run(transport)["lifecycle_case"], "AS-POL-001")

    def test_unknown_notification_and_second_terminal_are_rejected(self) -> None:
        unknown = ScriptedTransport(
            events=[
                {
                    "method": "thread/resumed",
                    "params": {
                        "threadId": "thread.synthetic.1",
                        "turnId": "turn.synthetic.1",
                    },
                }
            ]
        )
        self.assertEqual(_run(unknown)["lifecycle_case"], "AS-POL-001")

        terminal = {
            "method": "turn/completed",
            "params": {
                "threadId": "thread.synthetic.1",
                "turnId": "turn.synthetic.1",
                "status": "completed",
                "output": _role_output(),
            },
        }
        duplicated = ScriptedTransport(events=[terminal, copy.deepcopy(terminal)])
        self.assertEqual(_run(duplicated)["lifecycle_case"], "AS-POL-001")

    def test_invalid_role_output_is_known_failure(self) -> None:
        output = _role_output()
        output["validation"] = [
            {
                "command_id": "forbidden",
                "status": "passed",
                "exit_code": 0,
                "evidence_sha256": SHA,
            }
        ]
        transport = ScriptedTransport(
            events=[
                {
                    "method": "turn/completed",
                    "params": {
                        "threadId": "thread.synthetic.1",
                        "turnId": "turn.synthetic.1",
                        "status": "completed",
                        "output": output,
                    },
                }
            ]
        )
        self.assertEqual(_run(transport)["lifecycle_case"], "AS-OUT-001")

    def test_absent_terminal_remains_unknown(self) -> None:
        result = _run(ScriptedTransport(events=[]))
        self.assertEqual(result["lifecycle_case"], "AS-UNK-001")
        self.assertEqual(
            result["profile_projection"],
            "unknown_outcome_reconciliation_required",
        )

    def test_timeout_and_process_exit_have_distinct_terminal_cases(self) -> None:
        timeout = _run(TimeoutTransport())
        self.assertEqual(timeout["lifecycle_case"], "AS-TMO-UNK-001")
        self.assertEqual(timeout["automatic_retry_count"], 0)
        process_exit = _run(ProcessExitTransport())
        self.assertEqual(process_exit["lifecycle_case"], "AS-EXIT-001")

    def test_cleanup_failure_and_unknown_never_become_success(self) -> None:
        failed = _run(ScriptedTransport(cleanup_status="known_incomplete"))
        self.assertEqual(failed["lifecycle_case"], "AS-CLN-FAIL-001")
        unknown = _run(ScriptedTransport(cleanup_status="unknown"))
        self.assertEqual(unknown["lifecycle_case"], "AS-CLN-UNK-001")

    def test_oversized_or_duplicate_wire_message_fails_closed(self) -> None:
        oversized = b"{" + (b" " * app_server.MAX_JSON_LINE_BYTES) + b"}\n"
        result = _run(ScriptedTransport(events=[oversized]))
        self.assertEqual(result["lifecycle_case"], "AS-KNOWN-FAIL-001")
        duplicate = b'{"method":"turn/started","method":"turn/completed","params":{}}\n'
        result = _run(ScriptedTransport(events=[duplicate]))
        self.assertEqual(result["lifecycle_case"], "AS-KNOWN-FAIL-001")

    def test_real_process_entrypoint_is_explicitly_inert(self) -> None:
        with self.assertRaisesRegex(
            app_server.AppServerAdapterError,
            "real_process_start_not_authorized",
        ):
            app_server.start_pinned_app_server_once({}, {})


if __name__ == "__main__":
    unittest.main()
