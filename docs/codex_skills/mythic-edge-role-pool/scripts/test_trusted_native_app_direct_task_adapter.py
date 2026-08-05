from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime, timezone
from typing import Mapping

import trusted_native_app_direct_task_adapter as direct

NOW = datetime(2026, 8, 4, 12, 0, 0, tzinfo=timezone.utc)
LATER = datetime(2026, 8, 4, 12, 5, 0, tzinfo=timezone.utc)
PROJECT_ID = "synthetic-project-private"
THREAD_ID = "thread.synthetic.1"
CLIENT_ID = "client.synthetic.1"


def _clock(*values: datetime):
    remaining = list(values)

    def read() -> datetime:
        return remaining.pop(0) if remaining else values[-1]

    return read


def _monotonic_clock(*values: float):
    remaining = list(values)

    def read() -> float:
        return remaining.pop(0) if remaining else values[-1]

    return read


def _lane(
    role: str = "E",
    *,
    base_ref: str = "refs/heads/main",
    stop_conditions: list[str] | None = None,
) -> dict[str, object]:
    return direct.with_self_digest(
        {
            "lane_id": "lane.synthetic.1",
            "repository_id": 1235264383,
            "canonical_name": "tahjali11/mythic-edge",
            "issue_url": "https://github.com/Tahjali11/Mythic-Edge/issues/813",
            "role": role,
            "operation_id": "inspect",
            "base_ref": base_ref,
            "base_sha": "b" * 40,
            "predecessor_packet_sha256": None,
            "command_ids": [],
            "read_scope": ["docs"],
            "mutation_scope": [],
            "protected_surfaces": ["native_task_launch"],
            "validation_command_ids": [],
            "expected_artifact_paths": [],
            "stop_conditions": stop_conditions or ["Stop on authority drift."],
            "lane_packet_sha256": "",
        },
        "lane_packet_sha256",
    )


def _request(role: str = "E", *, lane: Mapping[str, object] | None = None):
    selected = dict(lane or _lane(role))
    return direct.with_self_digest(
        {
            "schema_version": "trusted_owner_native_task_request.v1",
            "request_sha256": "1" * 64,
            "claim_observation_sha256": "2" * 64,
            "lane_packet_sha256": selected["lane_packet_sha256"],
            "repository_id": selected["repository_id"],
            "issue_url": selected["issue_url"],
            "role": role,
            "base_sha": selected["base_sha"],
            "worktree_observation_sha256": "7" * 64,
            "context_mode": "isolated_packet_only",
            "fork_turns": "none",
            "issued_at_utc": "2026-08-04T11:59:00Z",
            "task_request_sha256": "",
        },
        "task_request_sha256",
    )


def _registry(role: str = "E") -> dict[str, object]:
    return {
        "repository_id": 1235264383,
        "eligible_roles": [role],
        "permitted_operations": ["inspect"],
        "permitted_read_scope": ["docs"],
        "maximum_mutation_scope": [],
        "repository_code_execution_policy": "forbidden",
        "approved_commands": [],
    }


def _handoff(role: str = "E") -> dict[str, object]:
    return direct.with_self_digest(
        {
            "status": "complete",
            "next_role": "F" if role == "E" else "E",
            "source_artifact_paths": ["docs/contracts/example.md"],
            "finding_ids": [],
            "stop_reason": None,
            "handoff_sha256": "",
        },
        "handoff_sha256",
    )


def _effects(**changes: int) -> dict[str, int]:
    result = {field: 0 for field in direct.EFFECT_COUNT_FIELDS}
    result.update(changes)
    return result


def _operation_id(role: str = "E") -> str:
    lane = _lane(role)
    request = _request(role, lane=lane)
    return direct.build_operation_binding(
        task_request=request,
        lane_packet=lane,
        project_id=PROJECT_ID,
    )[2]


def _readback(
    status: object = "completed",
    *,
    role: str = "E",
    thread_id: str = THREAD_ID,
    project_id: str = PROJECT_ID,
    repository_id: int = 1235264383,
    worktree_sha256: str = "7" * 64,
    branch_ref: str = "refs/heads/main",
    base_sha: str = "b" * 40,
    operation_id: str | None = None,
    handoffs: list[object] | None = None,
    post_sha256: str | None = "7" * 64,
    effect_counts: Mapping[str, int] | None = None,
) -> dict[str, object]:
    terminal = direct.normalize_task_status(status) in direct.TERMINAL_STATUSES
    return {
        "threadId": thread_id,
        "projectId": project_id,
        "repositoryId": repository_id,
        "worktreeObservationSha256": worktree_sha256,
        "branchRef": branch_ref,
        "baseSha": base_sha,
        "operationId": operation_id or _operation_id(role),
        "status": status,
        "handoffs": (
            handoffs
            if handoffs is not None
            else ([_handoff(role)] if terminal and status == "completed" else [])
        ),
        "postWorktreeObservationSha256": post_sha256,
        "effectCounts": dict(effect_counts or _effects()),
    }


class FakeClient:
    synthetic_only = True

    def __init__(
        self,
        *,
        create_response: object = None,
        list_response: object = None,
        read_responses: list[object] | None = None,
    ) -> None:
        self.create_response = (
            {"threadId": THREAD_ID} if create_response is None else create_response
        )
        self.list_response = {"threads": []} if list_response is None else list_response
        self.read_responses = list(read_responses or [_readback()])
        self.create_calls: list[dict[str, object]] = []
        self.list_call_count = 0
        self.read_calls: list[str] = []
        self.follow_up_message_count = 0
        self.replacement_task_count = 0
        self.real_operation_call_count = 0

    def create_thread(self, *, target: Mapping[str, object], prompt: str) -> object:
        self.create_calls.append({"target": copy.deepcopy(target), "prompt": prompt})
        if isinstance(self.create_response, Exception):
            raise self.create_response
        return copy.deepcopy(self.create_response)

    def list_threads(self) -> object:
        self.list_call_count += 1
        return copy.deepcopy(self.list_response)

    def read_thread(self, thread_id: str) -> object:
        self.read_calls.append(thread_id)
        if not self.read_responses:
            raise RuntimeError("synthetic exhausted response")
        result = self.read_responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return copy.deepcopy(result)


def _list_entry(
    *,
    thread_id: str = THREAD_ID,
    client_id: str | None = CLIENT_ID,
    project_id: str = PROJECT_ID,
    operation_id: str | None = None,
) -> dict[str, object]:
    return {
        "threadId": thread_id,
        "clientThreadId": client_id,
        "projectId": project_id,
        "operationId": operation_id or _operation_id(),
    }


def _adapter(
    client: FakeClient,
    *,
    role: str = "E",
    lane: Mapping[str, object] | None = None,
    request: Mapping[str, object] | None = None,
    first_r2: bool = True,
    monotonic_clock: object = None,
) -> direct.TrustedNativeAppDirectTaskAdapter:
    selected_lane = dict(lane or _lane(role))
    selected_request = dict(request or _request(role, lane=selected_lane))
    adapter_kwargs: dict[str, object] = {}
    if monotonic_clock is not None:
        adapter_kwargs["monotonic_clock"] = monotonic_clock
    return direct.TrustedNativeAppDirectTaskAdapter(
        task_request=selected_request,
        lane_packet=selected_lane,
        registry_entry=_registry(role),
        project_id=PROJECT_ID,
        client=client,
        clock=_clock(NOW, LATER, LATER),
        first_r2=first_r2,
        **adapter_kwargs,
    )


class ContractBytesTests(unittest.TestCase):
    def test_known_answer_vectors_are_exact(self) -> None:
        self.assertEqual(
            direct.validate_fixed_contract_bytes(),
            {
                "terminal_byte_count": 391,
                "terminal_sha256": direct.TERMINAL_READBACK_KAT_SHA256,
                "platform_preimage_byte_count": 1489,
                "platform_self_sha256": direct.PLATFORM_RECEIPT_KAT_SELF_SHA256,
                "platform_artifact_byte_count": 1582,
                "platform_artifact_sha256": (
                    direct.PLATFORM_RECEIPT_KAT_ARTIFACT_SHA256
                ),
            },
        )

    def test_canonical_parser_rejects_duplicate_order_and_framing(self) -> None:
        terminal = direct._terminal_readback_kat()
        encoded = direct.canonical_json_bytes(terminal)
        self.assertEqual(
            direct.parse_canonical_json_line(
                encoded,
                fields=direct.TERMINAL_READBACK_FIELDS,
            ),
            terminal,
        )
        duplicate = encoded.replace(b"{", b'{"schema_version":"duplicate",', 1)
        reordered = {"app_task_operation_id": terminal["app_task_operation_id"]}
        reordered.update(terminal)
        for invalid in (
            duplicate,
            direct.canonical_json_bytes(reordered),
            encoded.rstrip(b"\n"),
            encoded + b"\n",
            encoded.replace(b"\n", b"\r\n"),
            b"\xef\xbb\xbf" + encoded,
        ):
            with self.subTest(invalid=invalid[:20]):
                with self.assertRaises(direct.AppNativeDirectAdapterError):
                    direct.parse_canonical_json_line(
                        invalid,
                        fields=direct.TERMINAL_READBACK_FIELDS,
                    )

    def test_terminal_readback_rejects_every_binding_class(self) -> None:
        terminal = direct._terminal_readback_kat()
        expected = {
            "app_task_operation_id": terminal["app_task_operation_id"],
            "task_identity_digest": terminal["task_identity_sha256"],
            "task_target_readback_sha256": terminal[
                "task_target_readback_sha256"
            ],
        }
        self.assertEqual(
            direct.validate_terminal_readback(terminal, **expected),
            [],
        )
        mutations = {
            "schema_version": "wrong",
            "app_task_operation_id": "wrong",
            "task_identity_sha256": "wrong",
            "terminal_status": "running",
            "task_target_readback_sha256": "wrong",
            "read_at_utc": "2026-08-04T12:05:00.1Z",
        }
        for field, value in mutations.items():
            changed = dict(terminal)
            changed[field] = value
            with self.subTest(field=field):
                self.assertTrue(
                    direct.validate_terminal_readback(changed, **expected)
                )


class AdmissionAndConstructionTests(unittest.TestCase):
    def test_general_contract_accepts_only_b_and_e(self) -> None:
        for role in ("B", "E"):
            lane = _lane(role)
            self.assertEqual(
                direct.validate_direct_request_boundary(
                    task_request=_request(role, lane=lane),
                    lane_packet=lane,
                    registry_entry=_registry(role),
                ),
                [],
            )
        for role in "ACDFGH":
            lane = _lane("E")
            request = _request("E", lane=lane)
            request["role"] = role
            request = direct.with_self_digest(request, "task_request_sha256")
            self.assertTrue(
                direct.validate_direct_request_boundary(
                    task_request=request,
                    lane_packet=lane,
                    registry_entry=_registry("E"),
                )
            )

    def test_first_r2_policy_accepts_e_and_rejects_b(self) -> None:
        for role, expected in (("E", []), ("B", ["first_r2_role_not_admitted"])):
            lane = _lane(role)
            self.assertEqual(
                direct.validate_first_r2_request(
                    task_request=_request(role, lane=lane),
                    lane_packet=lane,
                    registry_entry=_registry(role),
                ),
                expected,
            )

    def test_effect_arrays_registry_and_scope_fail_closed(self) -> None:
        lane = _lane()
        request = _request(lane=lane)
        for field in (
            "command_ids",
            "validation_command_ids",
            "mutation_scope",
            "expected_artifact_paths",
        ):
            changed = dict(lane)
            changed[field] = ["forbidden"]
            changed = direct.with_self_digest(changed, "lane_packet_sha256")
            rebound = dict(request)
            rebound["lane_packet_sha256"] = changed["lane_packet_sha256"]
            rebound = direct.with_self_digest(rebound, "task_request_sha256")
            self.assertTrue(
                direct.validate_direct_request_boundary(
                    task_request=rebound,
                    lane_packet=changed,
                    registry_entry=_registry(),
                )
            )
        invalid_registry = _registry()
        invalid_registry["repository_code_execution_policy"] = "allowlisted"
        self.assertTrue(
            direct.validate_direct_request_boundary(
                task_request=request,
                lane_packet=lane,
                registry_entry=invalid_registry,
            )
        )

    def test_target_prompt_and_operation_binding_are_exact(self) -> None:
        lane = _lane()
        request = _request(lane=lane)
        binding, digest, operation_id = direct.build_operation_binding(
            task_request=request,
            lane_packet=lane,
            project_id=PROJECT_ID,
        )
        self.assertEqual(tuple(binding), direct.OPERATION_BINDING_FIELDS)
        self.assertEqual(operation_id, f"app_native_{digest[:32]}")
        target = direct.build_create_target(
            project_id=PROJECT_ID,
            base_ref=str(lane["base_ref"]),
        )
        self.assertEqual(
            target,
            {
                "type": "project",
                "projectId": PROJECT_ID,
                "environment": {
                    "type": "worktree",
                    "startingState": {
                        "type": "branch",
                        "branchName": "refs/heads/main",
                    },
                },
            },
        )
        prompt = direct.build_canonical_prompt(
            task_request=request,
            lane_packet=lane,
            predecessor_packet=None,
            app_task_operation_id=operation_id,
        )
        self.assertEqual(prompt.count("mythic_edge_operation_id:"), 1)
        self.assertIn("predecessor_packet: null\n", prompt)
        self.assertNotIn(PROJECT_ID, prompt)
        self.assertNotIn("model", target)
        self.assertNotIn("thinking", target)
        self.assertTrue(prompt.endswith("\n"))

    def test_deadline_default_exact_override_and_malformed_rejection(self) -> None:
        self.assertEqual(direct.observation_deadline_seconds(_lane()), 5400)
        selected = _lane(
            stop_conditions=["app_native_observation_deadline_seconds:120"]
        )
        self.assertEqual(direct.observation_deadline_seconds(selected), 120)
        for values in (
            ["app_native_observation_deadline_seconds:0"],
            ["app_native_observation_deadline_seconds:not-an-int"],
            [
                "app_native_observation_deadline_seconds:120",
                "app_native_observation_deadline_seconds:121",
            ],
        ):
            with self.assertRaises(direct.AppNativeDirectAdapterError):
                direct.observation_deadline_seconds(_lane(stop_conditions=values))


class LifecycleTests(unittest.TestCase):
    def test_direct_stable_id_completed_receipt_and_no_echo(self) -> None:
        client = FakeClient()
        adapter = _adapter(client)
        request = _request(lane=_lane())
        receipt = adapter.create_once(request)
        self.assertEqual(adapter.call_guard_state, "entered_once")
        self.assertEqual(len(client.create_calls), 1)
        self.assertEqual(client.read_calls, [THREAD_ID])
        self.assertEqual(receipt["task_id"], THREAD_ID)
        self.assertEqual(
            adapter.last_result["status"],
            "synthetic_app_native_receipt_accepted_non_live",
        )
        serialized = json.dumps(adapter.last_result, sort_keys=True)
        self.assertNotIn(PROJECT_ID, serialized)
        self.assertNotIn(CLIENT_ID, serialized)
        self.assertEqual(client.follow_up_message_count, 0)
        self.assertEqual(client.replacement_task_count, 0)
        self.assertEqual(client.real_operation_call_count, 0)

    def test_client_identity_resolves_exactly_once(self) -> None:
        client = FakeClient(
            create_response={"clientThreadId": CLIENT_ID},
            list_response={"threads": [_list_entry()]},
        )
        adapter = _adapter(client)
        adapter.create_once(_request(lane=_lane()))
        platform = adapter.last_result["platform_receipt"]
        self.assertEqual(
            platform["returned_identifier_kind"],
            "client_thread_id_resolved",
        )
        self.assertEqual(client.list_call_count, 1)

    def test_client_identity_pending_and_multiple_match_are_unknown(self) -> None:
        for threads in ([], [_list_entry(), _list_entry(thread_id="thread.synthetic.2")]):
            client = FakeClient(
                create_response={"clientThreadId": CLIENT_ID},
                list_response={"threads": threads},
            )
            adapter = _adapter(client)
            with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
                adapter.create_once(_request(lane=_lane()))
            self.assertEqual(
                caught.exception.profile_projection,
                "unknown_outcome_reconciliation_required",
            )
            self.assertEqual(adapter.last_result["create_call_count"], 1)

    def test_ambiguous_submission_zero_one_and_multiple_matches(self) -> None:
        for count, accepted in ((0, False), (1, True), (2, False)):
            threads = [
                _list_entry(
                    thread_id=f"thread.synthetic.{index + 1}",
                    client_id=None,
                )
                for index in range(count)
            ]
            client = FakeClient(
                create_response=direct.AmbiguousCreateOutcome("ambiguous"),
                list_response={"threads": threads},
                read_responses=[
                    _readback(thread_id="thread.synthetic.1")
                ],
            )
            adapter = _adapter(client)
            if accepted:
                adapter.create_once(_request(lane=_lane()))
                self.assertEqual(
                    adapter.last_result["platform_receipt"][
                        "returned_identifier_kind"
                    ],
                    "ambiguous_submission_reconciled",
                )
            else:
                with self.assertRaises(direct.AppNativeDirectAdapterError):
                    adapter.create_once(_request(lane=_lane()))
            self.assertEqual(len(client.create_calls), 1)

    def test_known_rejection_and_unknown_outcome_are_nonretryable(self) -> None:
        for response in (
            direct.KnownCreateRejection("known"),
            {"unexpected": "shape"},
        ):
            client = FakeClient(create_response=response)
            adapter = _adapter(client)
            with self.assertRaises(direct.AppNativeDirectAdapterError):
                adapter.create_once(_request(lane=_lane()))
            with self.assertRaisesRegex(
                direct.AppNativeDirectAdapterError,
                "app_native_adapter_already_used",
            ):
                adapter.create_once(_request(lane=_lane()))
            self.assertEqual(len(client.create_calls), 1)

    def test_preflight_rejection_never_enters_create_and_is_nonretryable(self) -> None:
        lane = _lane("B")
        request = _request("B", lane=lane)
        client = FakeClient(read_responses=[_readback(role="B")])
        adapter = _adapter(
            client,
            role="B",
            lane=lane,
            request=request,
            first_r2=True,
        )
        with self.assertRaises(direct.AppNativeDirectAdapterError):
            adapter.create_once(request)
        self.assertEqual(adapter.call_guard_state, "not_entered")
        self.assertEqual(client.create_calls, [])
        with self.assertRaises(direct.AppNativeDirectAdapterError):
            adapter.create_once(request)

    def test_wrong_target_binding_matrix_fails_after_one_create(self) -> None:
        mutations = {
            "thread_id": {"thread_id": "thread.synthetic.2"},
            "project": {"project_id": "other-project"},
            "repository": {"repository_id": 2},
            "worktree": {"worktree_sha256": "0" * 64},
            "branch": {"branch_ref": "refs/heads/other"},
            "base": {"base_sha": "c" * 40},
            "operation": {"operation_id": "app_native_wrong"},
        }
        for name, change in mutations.items():
            with self.subTest(name=name):
                client = FakeClient(read_responses=[_readback(**change)])
                adapter = _adapter(client)
                with self.assertRaises(direct.AppNativeDirectAdapterError):
                    adapter.create_once(_request(lane=_lane()))
                self.assertEqual(len(client.create_calls), 1)
                self.assertEqual(adapter.last_result["task_receipt"], None)

    def test_running_then_terminal_uses_one_final_deadline_read(self) -> None:
        client = FakeClient(read_responses=[_readback("running"), _readback()])
        adapter = _adapter(
            client,
            monotonic_clock=_monotonic_clock(100.0, 5500.0),
        )
        adapter.create_once(_request(lane=_lane()))
        self.assertEqual(client.read_calls, [THREAD_ID, THREAD_ID])
        platform = adapter.last_result["platform_receipt"]
        self.assertEqual(platform["terminal_status"], "completed")
        self.assertEqual(platform["reconciliation_status"], "not_required")
        self.assertEqual(platform["observation_deadline_seconds"], 5400)

    def test_nonterminal_deadline_outcomes_retain_same_task_without_retry(self) -> None:
        outcomes = (
            _readback("running"),
            _readback(["running", "completed"], handoffs=[]),
            _readback("unrecognized", handoffs=[]),
            RuntimeError("synthetic unavailable"),
        )
        for final in outcomes:
            client = FakeClient(read_responses=[_readback("running"), final])
            adapter = _adapter(
                client,
                monotonic_clock=_monotonic_clock(100.0, 5500.0),
            )
            with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
                adapter.create_once(_request(lane=_lane()))
            self.assertEqual(
                caught.exception.profile_projection,
                "unknown_outcome_reconciliation_required",
            )
            platform = adapter.last_result["platform_receipt"]
            self.assertIsNotNone(platform)
            self.assertEqual(platform["reconciliation_status"], "required_same_task")
            self.assertIsNone(platform["terminal_readback_sha256"])
            self.assertEqual(len(client.create_calls), 1)

    def test_later_same_task_reconciliation_never_creates_again(self) -> None:
        client = FakeClient(
            read_responses=[
                _readback("running"),
                _readback("running"),
                _readback(),
            ]
        )
        adapter = _adapter(
            client,
            monotonic_clock=_monotonic_clock(100.0, 5500.0, 5500.0),
        )
        with self.assertRaises(direct.AppNativeDirectAdapterError):
            adapter.create_once(_request(lane=_lane()))
        reconciled = adapter.reconcile_same_task()
        self.assertEqual(
            reconciled["platform_receipt"]["reconciliation_status"],
            "resolved_same_task_terminal",
        )
        self.assertEqual(len(client.create_calls), 1)

    def test_running_before_deadline_waits_for_same_task_reconciliation(self) -> None:
        events: list[str] = []
        moments = iter((100.0, 5499.0, 5500.0))

        def monotonic_clock() -> float:
            events.append("monotonic")
            return next(moments)

        class OrderedFakeClient(FakeClient):
            def create_thread(
                self,
                *,
                target: Mapping[str, object],
                prompt: str,
            ) -> object:
                events.append("create_thread")
                return super().create_thread(target=target, prompt=prompt)

            def read_thread(self, thread_id: str) -> object:
                events.append("read_thread")
                return super().read_thread(thread_id)

        client = OrderedFakeClient(
            read_responses=[_readback("running"), _readback()]
        )
        adapter = _adapter(
            client,
            monotonic_clock=monotonic_clock,
        )

        with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
            adapter.create_once(_request(lane=_lane()))

        self.assertEqual(caught.exception.code, "observation_deadline_not_elapsed")
        self.assertIsNone(caught.exception.profile_projection)
        self.assertEqual(client.read_calls, [THREAD_ID])
        self.assertIsNone(adapter.last_result)
        self.assertEqual(
            events,
            ["monotonic", "create_thread", "read_thread", "monotonic"],
        )

        reconciled = adapter.reconcile_same_task()
        self.assertEqual(
            reconciled["status"],
            "synthetic_app_native_receipt_accepted_non_live",
        )
        self.assertEqual(client.read_calls, [THREAD_ID, THREAD_ID])
        self.assertEqual(len(client.create_calls), 1)
        self.assertEqual(
            events,
            [
                "monotonic",
                "create_thread",
                "read_thread",
                "monotonic",
                "monotonic",
                "read_thread",
            ],
        )

    def test_completed_without_post_worktree_evidence_is_unknown(self) -> None:
        client = FakeClient(read_responses=[_readback(post_sha256=None)])
        adapter = _adapter(client)

        with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
            adapter.create_once(_request(lane=_lane()))

        self.assertEqual(
            caught.exception.code,
            "post_worktree_observation_required",
        )
        self.assertEqual(
            caught.exception.profile_projection,
            "unknown_outcome_reconciliation_required",
        )
        self.assertEqual(
            adapter.last_result["status"],
            "unknown_outcome_reconciliation_required",
        )
        self.assertIsNone(adapter.last_result["platform_receipt"])
        self.assertIsNone(adapter.last_result["task_receipt"])

    def test_completed_with_changed_post_worktree_evidence_is_unknown(self) -> None:
        client = FakeClient(read_responses=[_readback(post_sha256="9" * 64)])
        adapter = _adapter(client)

        with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
            adapter.create_once(_request(lane=_lane()))

        self.assertEqual(
            caught.exception.code,
            "post_worktree_observation_mismatch",
        )
        self.assertEqual(
            caught.exception.profile_projection,
            "unknown_outcome_reconciliation_required",
        )
        self.assertEqual(
            adapter.last_result["status"],
            "unknown_outcome_reconciliation_required",
        )
        self.assertIsNone(adapter.last_result["platform_receipt"])
        self.assertIsNone(adapter.last_result["task_receipt"])

    def test_mixed_recognized_and_unknown_status_requires_same_task(self) -> None:
        mixed_status = ["completed", "newPlatformStatus"]
        self.assertEqual(direct.normalize_task_status(mixed_status), "unknown")
        client = FakeClient(
            read_responses=[
                _readback(status=mixed_status, handoffs=[]),
                _readback(status=mixed_status, handoffs=[]),
            ]
        )
        adapter = _adapter(
            client,
            monotonic_clock=_monotonic_clock(100.0, 5500.0),
        )

        with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
            adapter.create_once(_request(lane=_lane()))

        self.assertEqual(
            caught.exception.profile_projection,
            "unknown_outcome_reconciliation_required",
        )
        self.assertEqual(
            adapter.last_result["status"],
            "unknown_outcome_reconciliation_required",
        )
        self.assertEqual(
            adapter.last_result["platform_receipt"]["terminal_status"],
            "unknown",
        )
        self.assertEqual(
            adapter.last_result["platform_receipt"]["reconciliation_status"],
            "required_same_task",
        )
        self.assertEqual(len(client.create_calls), 1)
        self.assertEqual(client.read_calls, [THREAD_ID, THREAD_ID])

    def test_completed_requires_exactly_one_unwrapped_valid_handoff(self) -> None:
        invalid_handoffs = (
            [],
            [_handoff(), _handoff()],
            ["prose"],
            [{"wrapped": _handoff()}],
            [{**_handoff(), "unexpected": False}],
        )
        for handoffs in invalid_handoffs:
            client = FakeClient(read_responses=[_readback(handoffs=list(handoffs))])
            adapter = _adapter(client)
            with self.assertRaises(direct.AppNativeDirectAdapterError):
                adapter.create_once(_request(lane=_lane()))
            self.assertEqual(adapter.last_result["status"], "failed_lane_known")

    def test_failed_and_interrupted_are_known_terminal_non_success(self) -> None:
        for status in ("failed", "interrupted"):
            client = FakeClient(read_responses=[_readback(status)])
            adapter = _adapter(client)
            with self.assertRaises(direct.AppNativeDirectAdapterError) as caught:
                adapter.create_once(_request(lane=_lane()))
            self.assertEqual(caught.exception.profile_projection, "failed_lane_known")
            platform = adapter.last_result["platform_receipt"]
            self.assertEqual(platform["terminal_status"], status)
            self.assertIsNotNone(platform["terminal_readback_sha256"])
            self.assertIsNone(platform["typed_handoff_sha256"])

    def test_every_unexpected_effect_is_visible_and_never_repaired(self) -> None:
        for field in direct.EFFECT_COUNT_FIELDS:
            changed = _effects(**{field: 1})
            client = FakeClient(read_responses=[_readback(effect_counts=changed)])
            adapter = _adapter(client)
            with self.assertRaises(direct.AppNativeDirectAdapterError):
                adapter.create_once(_request(lane=_lane()))
            self.assertEqual(adapter.last_result["status"], "failed_lane_known")
            self.assertFalse(hasattr(client, "cleanup"))
            self.assertFalse(hasattr(client, "repair"))


class ReceiptTests(unittest.TestCase):
    def test_receipt_order_digest_outer_binding_and_private_rejection(self) -> None:
        client = FakeClient()
        adapter = _adapter(client)
        receipt = adapter.create_once(_request(lane=_lane()))
        platform = adapter.last_result["platform_receipt"]
        self.assertEqual(tuple(platform), direct.PLATFORM_RECEIPT_FIELDS)
        self.assertEqual(tuple(receipt), direct.TASK_RECEIPT_FIELDS)
        terminal = direct._terminal_readback_kat()
        kat = direct._platform_receipt_kat()
        self.assertEqual(
            direct.validate_platform_receipt(kat, terminal_readback=terminal),
            [],
        )
        self.assertEqual(
            direct.validate_task_receipt(
                receipt,
                task_request=_request(lane=_lane()),
                platform_receipt=platform,
            ),
            [],
        )
        serialized = direct.canonical_json_bytes(platform)
        self.assertNotIn(PROJECT_ID.encode(), serialized)
        self.assertNotIn(CLIENT_ID.encode(), serialized)

    def test_receipt_rejects_field_order_nullability_digest_and_extra(self) -> None:
        terminal = direct._terminal_readback_kat()
        original = direct._platform_receipt_kat()
        variants: list[dict[str, object]] = []
        reordered = {"app_task_operation_id": original["app_task_operation_id"]}
        reordered.update(original)
        variants.append(reordered)
        for field, value in (
            ("create_call_count", 2),
            ("terminal_status", "running"),
            ("terminal_readback_sha256", None),
            ("typed_handoff_sha256", None),
            ("platform_receipt_sha256", "0" * 64),
        ):
            changed = dict(original)
            changed[field] = value
            variants.append(changed)
        extra = dict(original)
        extra["unexpected"] = False
        variants.append(extra)
        for value in variants:
            self.assertTrue(
                direct.validate_platform_receipt(
                    value,
                    terminal_readback=terminal,
                )
            )

    def test_completed_receipt_requires_post_worktree_digest(self) -> None:
        terminal = direct._terminal_readback_kat()
        changed = dict(direct._platform_receipt_kat())
        changed["post_worktree_observation_sha256"] = None
        changed = direct.seal_platform_receipt(
            {
                field: changed[field]
                for field in direct.PLATFORM_RECEIPT_FIELDS[:-1]
            }
        )

        errors = direct.validate_platform_receipt(
            changed,
            terminal_readback=terminal,
        )

        self.assertIn("post_worktree_observation_sha256_required", errors)

    def test_real_operation_and_alternate_fallback_are_closed(self) -> None:
        with self.assertRaisesRegex(
            direct.AppNativeDirectAdapterError,
            "real_task_operation_not_authorized",
        ):
            direct.real_app_task_create_once()
        forbidden_names = {
            "subprocess",
            "shell",
            "app_server",
            "broker",
            "codex_exec",
            "send_message",
            "cancel",
            "interrupt",
        }
        self.assertTrue(forbidden_names.isdisjoint(vars(direct)))

    def test_complete_suite_uses_zero_real_task_operations(self) -> None:
        clients = [
            FakeClient(),
            FakeClient(
                create_response={"clientThreadId": CLIENT_ID},
                list_response={"threads": [_list_entry()]},
            ),
        ]
        for client in clients:
            _adapter(client).create_once(_request(lane=_lane()))
        self.assertEqual(sum(item.real_operation_call_count for item in clients), 0)
        self.assertEqual(sum(len(item.create_calls) for item in clients), 2)


if __name__ == "__main__":
    unittest.main()
