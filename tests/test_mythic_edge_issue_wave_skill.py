from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = (
    REPO_ROOT
    / "docs"
    / "codex_skills"
    / "mythic-edge-issue-wave"
    / "scripts"
    / "issue_wave_state.py"
)
SPEC = importlib.util.spec_from_file_location("issue_wave_state", HELPER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
issue_wave = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = issue_wave
SPEC.loader.exec_module(issue_wave)

FIXED_NOW = datetime(2026, 8, 13, 12, 0, 0, tzinfo=UTC)
RUN_ID = "20260813T120000Z-1a2b3c4d"
REPOSITORIES = issue_wave.DEFAULT_ALLOWLIST[:3]


def _scope(seed: str) -> dict[str, list[str]]:
    return {
        "paths": [f"global:{seed}:path"],
        "interfaces": [f"global:{seed}:interface"],
        "truth_owners": [f"global:{seed}:truth"],
        "dependencies": [f"global:{seed}:dependency"],
        "shared_artifacts": [f"global:{seed}:artifact"],
        "submission_lanes": [f"global:{seed}:submission"],
    }


def _candidate(
    root: Path,
    repository: str,
    issue: int,
    *,
    lane_id: str,
    created_at: str,
    priority_source: str = "next_role",
    scope: dict[str, list[str]] | None = None,
    evidence: dict[str, object] | None = None,
) -> dict[str, object]:
    base_evidence: dict[str, object] = {
        "issue_open": True,
        "not_deferred": True,
        "prerequisites_complete": True,
        "prerequisite_relationship_unambiguous": True,
        "repository_authority_compatible": True,
        "checkout_identity_exact": True,
        "active_work_clear": True,
        "wip_compatible": True,
        "wip_exception_authorized": False,
        "scope_known": True,
        "anchor_relationship": None,
        "summary": f"Current public evidence admits {repository}#{issue}.",
    }
    if evidence:
        base_evidence.update(evidence)
    return {
        "lane_id": lane_id,
        "repository": repository,
        "issue": issue,
        "issue_created_at": created_at,
        "priority_source": priority_source,
        "target_root": str(root),
        "evidence": base_evidence,
        "scope": _scope(lane_id) if scope is None else scope,
    }


def _dispatch_invocation(options: str = "") -> dict[str, object]:
    suffix = f"; {options}" if options else ""
    return issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (A{suffix})")


def _fixture(
    tmp_path: Path,
    *,
    lane_count: int = 1,
    invocation: dict[str, object] | None = None,
) -> tuple[Path, dict[str, object], dict[str, object], dict[str, Path]]:
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True)
    target_root_parent = tmp_path / "targets"
    target_root_parent.mkdir()
    candidates: list[dict[str, object]] = []
    roots: dict[str, Path] = {}
    for index, repository in enumerate(REPOSITORIES[:lane_count], start=1):
        root = target_root_parent / f"repo-{index}"
        root.mkdir()
        roots[repository] = root
        candidates.append(
            _candidate(
                root,
                repository,
                100 + index,
                lane_id=f"lane-{index}",
                created_at=f"2026080{index}T120000Z",
            )
        )
    return (
        workspace,
        _dispatch_invocation() if invocation is None else invocation,
        {"schema_version": issue_wave.MANIFEST_SCHEMA, "candidates": candidates},
        roots,
    )


def _init(
    tmp_path: Path,
    *,
    lane_count: int = 1,
    invocation: dict[str, object] | None = None,
) -> tuple[Path, Path, dict[str, object]]:
    workspace, selected_invocation, manifest, roots = _fixture(
        tmp_path, lane_count=lane_count, invocation=invocation
    )
    run_directory, state = issue_wave.init_run(
        workspace,
        selected_invocation,
        manifest,
        target_roots=roots,
        run_id=RUN_ID,
        now=FIXED_NOW,
    )
    return workspace, run_directory, state


def _event(
    lane_id: str,
    from_state: str,
    to_state: str,
    *,
    role: str | None = None,
    updates: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": issue_wave.EVENT_REQUEST_SCHEMA,
        "lane_id": lane_id,
        "from_state": from_state,
        "to_state": to_state,
        "role": issue_wave._expected_event_role(from_state, to_state) if role is None else role,
        "reason": f"Public-safe reason for {to_state}.",
        "evidence_summary": f"Current evidence supports {to_state}.",
        "updates": {} if updates is None else updates,
    }


def _transition(
    workspace: Path,
    state: dict[str, object],
    request: dict[str, object],
) -> dict[str, object]:
    return issue_wave.transition_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        request_value=request,
        now=FIXED_NOW + timedelta(seconds=state["revision"] + 1),
    )


def _advance_one_lane_through_b(
    tmp_path: Path, workspace: Path, state: dict[str, object]
) -> dict[str, object]:
    worktree = tmp_path / "checkpoint-worktree"
    worktree.mkdir(parents=True, exist_ok=True)
    for request in (
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
        _event(
            "lane-1",
            "a_running",
            "a_complete",
            updates={"artifacts": ["docs/problem_representations/issue-101.md"]},
        ),
        _event("lane-1", "a_complete", "a_scope_verified"),
        _event("lane-1", "a_scope_verified", "b_running"),
        _event(
            "lane-1",
            "b_running",
            "b_complete",
            updates={"artifacts": ["docs/contracts/issue-101.md"]},
        ),
    ):
        state = _transition(workspace, state, request)
    return state


def _advance_one_lane_to_refined_a_scope(
    tmp_path: Path,
    workspace: Path,
    state: dict[str, object],
    refined_scope: dict[str, list[str]],
) -> dict[str, object]:
    worktree = tmp_path / "refined-scope-worktree"
    worktree.mkdir(parents=True, exist_ok=True)
    for request in (
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
        _event(
            "lane-1",
            "a_running",
            "a_complete",
            updates={
                "artifacts": ["docs/problem_representations/issue-101.md"],
                "scope": refined_scope,
            },
        ),
        _event("lane-1", "a_complete", "a_scope_verified"),
    ):
        state = _transition(workspace, state, request)
    return state


@pytest.mark.parametrize(
    ("command", "mode", "repositories", "anchor", "run_id", "permissions"),
    [
        ("$mythic-edge-issue-wave Inspect (A)", "Inspect", None, None, None, (False, False)),
        (
            "$mythic-edge-issue-wave Inspect (A; repos=tahjali11/mythic-edge,Tahjali11/Mythic-Edge-Analytics)",
            "Inspect",
            list(REPOSITORIES[:2]),
            None,
            None,
            (False, False),
        ),
        (
            "$mythic-edge-issue-wave Inspect (A; repos=Tahjali11/Mythic-Edge; anchor=tahjali11/mythic-edge#123)",
            "Inspect",
            [REPOSITORIES[0]],
            {"repository": REPOSITORIES[0], "issue": 123},
            None,
            (False, False),
        ),
        (
            f"$mythic-edge-issue-wave Inspect (A; run={RUN_ID})",
            "Inspect",
            None,
            None,
            RUN_ID,
            (False, False),
        ),
        ("$mythic-edge-issue-wave Dispatch (A)", "Dispatch", None, None, None, (False, False)),
        (
            "$mythic-edge-issue-wave Dispatch (A; repos=Tahjali11/Mythic-Edge; allow-main-draft)",
            "Dispatch",
            [REPOSITORIES[0]],
            None,
            None,
            (True, False),
        ),
        (
            "$mythic-edge-issue-wave Dispatch (A; anchor=Tahjali11/Mythic-Edge#123; allow-wip-exception)",
            "Dispatch",
            None,
            {"repository": REPOSITORIES[0], "issue": 123},
            None,
            (False, True),
        ),
        (
            f"$mythic-edge-issue-wave Dispatch (A; run={RUN_ID})",
            "Dispatch",
            None,
            None,
            RUN_ID,
            (False, False),
        ),
    ],
)
def test_parse_canonical_invocations(
    command: str,
    mode: str,
    repositories: list[str] | None,
    anchor: dict[str, object] | None,
    run_id: str | None,
    permissions: tuple[bool, bool],
) -> None:
    parsed = issue_wave.parse_invocation(command)

    assert parsed["schema_version"] == issue_wave.INVOCATION_SCHEMA
    assert parsed["mode"] == mode
    assert parsed["entry_role"] == "A"
    assert parsed["selectors"] == {
        "repositories": repositories,
        "anchor": anchor,
        "run_id": run_id,
    }
    assert (
        parsed["permissions"]["allow_main_draft"],
        parsed["permissions"]["allow_wip_exception"],
    ) == permissions


@pytest.mark.parametrize(
    "command",
    [
        "mythic-edge-issue-wave Inspect (A)",
        "$mythic-edge-issue-wave inspect (A)",
        "$mythic-edge-issue-wave Inspect (B)",
        "$mythic-edge-issue-wave Inspect (A;)",
        "$mythic-edge-issue-wave Inspect (A;; repos=Tahjali11/Mythic-Edge)",
        "$mythic-edge-issue-wave Inspect (A; unknown=value)",
        "$mythic-edge-issue-wave Inspect (A; repos=)",
        "$mythic-edge-issue-wave Inspect (A; repos=Tahjali11/Unknown)",
        "$mythic-edge-issue-wave Inspect (A; repos=Tahjali11/Mythic-Edge,tahjali11/mythic-edge)",
        "$mythic-edge-issue-wave Inspect (A; "
        "repos=Tahjali11/Mythic-Edge,Tahjali11/Mythic-Edge-Analytics,"
        "Tahjali11/Mythic-Edge-Corpus,Tahjali11/Mythic-Edge-Security)",
        "$mythic-edge-issue-wave Inspect (A; anchor=Tahjali11/Mythic-Edge#0)",
        "$mythic-edge-issue-wave Inspect (A; run=bad)",
        f"$mythic-edge-issue-wave Inspect (A; run={RUN_ID}; repos=Tahjali11/Mythic-Edge)",
        "$mythic-edge-issue-wave Inspect (A; allow-main-draft)",
        "$mythic-edge-issue-wave Dispatch (A; allow-main-draft; allow-main-draft)",
        "$mythic-edge-issue-wave Dispatch (A; repos=Tahjali11/Mythic-Edge; repos=Tahjali11/Mythic-Edge)",
    ],
)
def test_parse_rejects_malformed_or_unsupported_invocations(command: str) -> None:
    with pytest.raises(issue_wave.IssueWaveError) as error:
        issue_wave.parse_invocation(command)

    assert error.value.code == "invalid_invocation"
    assert command not in error.value.message


def test_manifest_normalizes_only_allowlisted_candidates_and_requires_deterministic_order(
    tmp_path: Path,
) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path, lane_count=3)
    state_root = workspace / ".codex" / "role-pool-runs"

    validated = issue_wave.validate_manifest(
        manifest,
        invocation,
        target_roots=roots,
        state_root=state_root,
    )

    assert [candidate["repository"] for candidate in validated["candidates"]] == list(REPOSITORIES)
    reversed_manifest = deepcopy(manifest)
    reversed_manifest["candidates"].reverse()
    with pytest.raises(issue_wave.IssueWaveError, match="deterministically ordered"):
        issue_wave.validate_manifest(
            reversed_manifest,
            invocation,
            target_roots=roots,
            state_root=state_root,
        )


@pytest.mark.parametrize(
    "field",
    [
        "issue_open",
        "not_deferred",
        "prerequisites_complete",
        "prerequisite_relationship_unambiguous",
        "repository_authority_compatible",
        "checkout_identity_exact",
        "active_work_clear",
        "scope_known",
    ],
)
def test_manifest_fails_closed_for_each_required_candidate_predicate(
    tmp_path: Path,
    field: str,
) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path)
    manifest["candidates"][0]["evidence"][field] = False

    with pytest.raises(issue_wave.IssueWaveError, match="eligibility evidence"):
        issue_wave.validate_manifest(
            manifest,
            invocation,
            target_roots=roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )


def test_manifest_requires_both_dispatch_permission_and_current_wip_exception(
    tmp_path: Path,
) -> None:
    invocation = _dispatch_invocation("allow-wip-exception")
    workspace, _, manifest, roots = _fixture(tmp_path, invocation=invocation)
    manifest["candidates"][0]["evidence"].update(
        {"wip_compatible": False, "wip_exception_authorized": True}
    )

    validated = issue_wave.validate_manifest(
        manifest,
        invocation,
        target_roots=roots,
        state_root=workspace / ".codex" / "role-pool-runs",
    )
    assert validated["candidates"][0]["evidence"]["wip_exception_authorized"] is True

    without_permission = _dispatch_invocation()
    with pytest.raises(issue_wave.IssueWaveError, match="WIP evidence"):
        issue_wave.validate_manifest(
            manifest,
            without_permission,
            target_roots=roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )


def test_anchor_requires_a_durable_relationship_and_repos_filter_is_exact(tmp_path: Path) -> None:
    invocation = _dispatch_invocation(
        "repos=Tahjali11/Mythic-Edge; anchor=Tahjali11/Mythic-Edge#855"
    )
    workspace, _, manifest, roots = _fixture(tmp_path, invocation=invocation)

    with pytest.raises(issue_wave.IssueWaveError, match="anchor relationship"):
        issue_wave.validate_manifest(
            manifest,
            invocation,
            target_roots=roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )

    manifest["candidates"][0]["evidence"]["anchor_relationship"] = "next_role"
    issue_wave.validate_manifest(
        manifest,
        invocation,
        target_roots=roots,
        state_root=workspace / ".codex" / "role-pool-runs",
    )
    manifest["candidates"][0]["repository"] = REPOSITORIES[1]
    manifest["candidates"][0]["target_root"] = str(roots[REPOSITORIES[0]])
    with pytest.raises(issue_wave.IssueWaveError, match="requested repositories"):
        issue_wave.validate_manifest(
            manifest,
            invocation,
            target_roots=roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )


def test_manifest_rejects_mechanical_scope_overlap_and_multiple_issues_in_one_repo(
    tmp_path: Path,
) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path, lane_count=2)
    manifest["candidates"][1]["scope"]["shared_artifacts"] = manifest["candidates"][0]["scope"][
        "shared_artifacts"
    ]
    with pytest.raises(issue_wave.IssueWaveError, match="mechanically overlap"):
        issue_wave.validate_manifest(
            manifest,
            invocation,
            target_roots=roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )

    manifest["candidates"][1]["scope"] = _scope("lane-2")
    manifest["candidates"][1]["repository"] = REPOSITORIES[0]
    manifest["candidates"][1]["target_root"] = str(roots[REPOSITORIES[0]])
    duplicate_roots = {REPOSITORIES[0]: roots[REPOSITORIES[0]]}
    with pytest.raises(issue_wave.IssueWaveError, match="one candidate per repository"):
        issue_wave.validate_manifest(
            manifest,
            invocation,
            target_roots=duplicate_roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )


def test_run_identifier_and_state_root_containment_fail_closed(tmp_path: Path) -> None:
    assert issue_wave.generate_run_id(now=FIXED_NOW, entropy=bytes.fromhex("1a2b3c4d")) == RUN_ID
    target = tmp_path / "target"
    target.mkdir()
    invocation = _dispatch_invocation()
    manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                target,
                REPOSITORIES[0],
                101,
                lane_id="lane-1",
                created_at="20260801T120000Z",
            )
        ],
    }

    with pytest.raises(issue_wave.IssueWaveError, match="overlaps"):
        issue_wave.init_run(
            target,
            invocation,
            manifest,
            target_roots={REPOSITORIES[0]: target},
            run_id=RUN_ID,
            now=FIXED_NOW,
        )
    assert not (target / ".codex").exists()


def test_init_is_exclusive_and_rejects_duplicate_active_lane(tmp_path: Path) -> None:
    workspace, _, _ = _init(tmp_path)
    _, invocation, manifest, roots = _fixture(tmp_path / "second")

    with pytest.raises(issue_wave.IssueWaveError, match="reserved") as error:
        issue_wave.init_run(
            workspace,
            invocation,
            manifest,
            target_roots=roots,
            run_id="20260813T120001Z-01020304",
            now=FIXED_NOW + timedelta(seconds=1),
        )
    assert error.value.code == "repository_reserved"


@pytest.mark.parametrize("relationship", ["duplicate", "nested"])
def test_manifest_rejects_duplicate_or_nested_target_roots(
    tmp_path: Path,
    relationship: str,
) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path, lane_count=2)
    first = roots[REPOSITORIES[0]]
    second = first
    if relationship == "nested":
        second = first / "nested-target"
        second.mkdir()
    roots[REPOSITORIES[1]] = second
    manifest["candidates"][1]["target_root"] = str(second)

    with pytest.raises(issue_wave.IssueWaveError, match="roots overlap"):
        issue_wave.validate_manifest(
            manifest,
            invocation,
            target_roots=roots,
            state_root=workspace / ".codex" / "role-pool-runs",
        )


@pytest.mark.parametrize(
    "relationship",
    [
        "duplicate",
        "nested",
        "ancestor",
        "other_checkout",
        "own_checkout",
        "checkout_ancestor",
        "state_root",
    ],
)
def test_new_worktree_rejects_every_cross_lane_or_state_path_overlap(
    tmp_path: Path,
    relationship: str,
) -> None:
    workspace, run_directory, state = _init(tmp_path, lane_count=2)
    worktree_root = tmp_path / "worktrees"
    first = worktree_root / "lane-1"
    first.mkdir(parents=True)
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(first)},
        ),
    )

    if relationship == "duplicate":
        unsafe = first
    elif relationship == "nested":
        unsafe = first / "nested"
        unsafe.mkdir()
    elif relationship == "ancestor":
        unsafe = worktree_root
    elif relationship == "other_checkout":
        unsafe = Path(state["lanes"][0]["checkout_location"]) / "nested-worktree"
        unsafe.mkdir()
    elif relationship == "own_checkout":
        unsafe = Path(state["lanes"][1]["checkout_location"])
    elif relationship == "checkout_ancestor":
        unsafe = Path(state["lanes"][1]["checkout_location"]).parent
    else:
        unsafe = run_directory.parent / "nested-worktree"
        unsafe.mkdir()

    with pytest.raises(issue_wave.IssueWaveError, match="paths overlap"):
        _transition(
            workspace,
            state,
            _event(
                "lane-2",
                "selected",
                "a_running",
                updates={"branch": "issue/102", "worktree_location": str(unsafe)},
            ),
        )
    _, loaded, _ = issue_wave.load_run(workspace, RUN_ID)
    assert loaded["revision"] == state["revision"]
    assert loaded["lanes"][1]["worktree_location"] is None


def test_load_replay_rejects_a_hash_valid_recorded_worktree_collision(tmp_path: Path) -> None:
    workspace, run_directory, state = _init(tmp_path, lane_count=2)
    worktree = tmp_path / "worktrees" / "lane-1"
    worktree.mkdir(parents=True)
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    event_without_digest = {
        "schema_version": issue_wave.EVENT_SCHEMA,
        "sequence": state["revision"] + 1,
        "timestamp_utc": "20260813T120002Z",
        "event_type": "transition",
        "segment": state["current_segment"],
        "lane_id": "lane-2",
        "from_state": "selected",
        "to_state": "a_running",
        "role": "A",
        "reason": "Synthetic replay collision.",
        "evidence_summary": "The supplied path collides with another lane.",
        "updates": {"branch": "issue/102", "worktree_location": str(worktree)},
        "previous_event_digest": state["last_event_digest"],
    }
    event = {
        **event_without_digest,
        "event_digest": hashlib.sha256(
            issue_wave._canonical_json(event_without_digest)
        ).hexdigest(),
    }
    with (run_directory / "events.jsonl").open("ab") as stream:
        stream.write(issue_wave._canonical_json(event) + b"\n")

    with pytest.raises(issue_wave.IssueWaveError) as error:
        issue_wave.load_run(workspace, RUN_ID)
    assert error.value.code == "state_integrity_error"


def test_load_rejects_recorded_target_checkout_collision(tmp_path: Path) -> None:
    workspace, run_directory, _ = _init(tmp_path, lane_count=2)
    run_path = run_directory / "run.json"
    saved = json.loads(run_path.read_text(encoding="utf-8"))
    duplicate = saved["candidates"][0]["target_root"]
    saved["candidates"][1]["target_root"] = duplicate
    saved["lanes"][1]["checkout_location"] = duplicate
    run_path.write_bytes(issue_wave._canonical_json(saved) + b"\n")

    with pytest.raises(issue_wave.IssueWaveError) as error:
        issue_wave.load_run(workspace, RUN_ID)
    assert error.value.code == "state_integrity_error"


def test_recorded_worktree_cannot_be_cleared_to_bypass_global_isolation(tmp_path: Path) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )

    with pytest.raises(issue_wave.IssueWaveError, match="immutable"):
        _transition(
            workspace,
            state,
            _event(
                "lane-1",
                "a_running",
                "a_complete",
                updates={
                    "artifacts": ["docs/problem_representations/lane-1.md"],
                    "worktree_location": None,
                },
            ),
        )


def test_concurrent_same_lane_initialization_admits_exactly_one_run(tmp_path: Path) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path)
    barrier = threading.Barrier(2)
    run_ids = (RUN_ID, "20260813T120001Z-01020304")

    def attempt(run_id: str) -> str:
        barrier.wait()
        try:
            issue_wave.init_run(
                workspace,
                invocation,
                manifest,
                target_roots=roots,
                run_id=run_id,
                now=FIXED_NOW,
            )
            return "success"
        except issue_wave.IssueWaveError as error:
            return error.code

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(attempt, run_ids))

    assert results.count("success") == 1
    assert set(results) <= {"success", "state_locked", "repository_reserved"}
    state_root = workspace / ".codex" / "role-pool-runs"
    published = [path for path in state_root.iterdir() if issue_wave.RUN_ID_RE.fullmatch(path.name)]
    assert len(published) == 1
    assert not (state_root / ".admission.lock").exists()


def test_disjoint_lane_initialization_remains_admissible(tmp_path: Path) -> None:
    workspace, invocation, first_manifest, first_roots = _fixture(tmp_path / "first")
    issue_wave.init_run(
        workspace,
        invocation,
        first_manifest,
        target_roots=first_roots,
        run_id=RUN_ID,
        now=FIXED_NOW,
    )
    second_root = tmp_path / "second-target"
    second_root.mkdir()
    second_manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                second_root,
                REPOSITORIES[1],
                202,
                lane_id="lane-2",
                created_at="20260802T120000Z",
            )
        ],
    }

    second_directory, _ = issue_wave.init_run(
        workspace,
        invocation,
        second_manifest,
        target_roots={REPOSITORIES[1]: second_root},
        run_id="20260813T120001Z-01020304",
        now=FIXED_NOW + timedelta(seconds=1),
    )
    assert second_directory.exists()


def test_stale_admission_lock_fails_closed_without_cleanup(tmp_path: Path) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path)
    lock = workspace / ".codex" / "role-pool-runs" / ".admission.lock"
    lock.mkdir(parents=True)
    lock.joinpath("owner").write_text("stale\n", encoding="utf-8")

    with pytest.raises(issue_wave.IssueWaveError) as error:
        issue_wave.init_run(
            workspace,
            invocation,
            manifest,
            target_roots=roots,
            run_id=RUN_ID,
            now=FIXED_NOW,
            admission_wait_seconds=0,
        )
    assert error.value.code == "state_locked"
    assert lock.joinpath("owner").read_text(encoding="utf-8") == "stale\n"


def test_failed_init_cleanup_preserves_unowned_staging_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace, invocation, manifest, roots = _fixture(tmp_path)
    state_root = workspace / ".codex" / "role-pool-runs"
    staging = state_root / f".{RUN_ID}.init-fixed"
    staging.mkdir(parents=True)
    sentinel = staging / "other-initializer.json"
    sentinel.write_text("preserve\n", encoding="utf-8")

    class FixedUuid:
        hex = "fixed"

    monkeypatch.setattr(issue_wave.uuid, "uuid4", lambda: FixedUuid())
    with pytest.raises(issue_wave.IssueWaveError) as error:
        issue_wave.init_run(
            workspace,
            invocation,
            manifest,
            target_roots=roots,
            run_id=RUN_ID,
            now=FIXED_NOW,
        )
    assert error.value.code == "state_integrity_error"
    assert sentinel.read_text(encoding="utf-8") == "preserve\n"
    assert not (state_root / ".admission.lock").exists()


def test_transition_table_contains_every_contracted_edge_and_no_shortcut() -> None:
    expected = set(issue_wave.FORWARD_TRANSITIONS)
    expected.add(("a_running", "a_ambiguous"))
    expected.add(("a_complete", "unsafe_or_conflicting_scope"))
    expected.update(
        (state, stop)
        for state in issue_wave.PRE_ROLE_BOUNDARIES
        for stop in {
            "incompatible_repository_authority",
            "checkout_unavailable_or_ambiguous",
            "unsafe_or_conflicting_scope",
        }
    )
    expected.update(
        (state, "backward_route_to_a_or_b")
        for state in {"b_running", "b_complete", "c_running", "c_complete", "e_running", "e_approved"}
    )
    expected.update(
        (state, "d_required")
        for state in {"c_running", "c_complete", "e_running", "e_approved", "f_running", "f_complete", "checks_running"}
    )
    expected.update((state, "unknown_agent_outcome") for state in issue_wave.RUNNING_STATES)
    expected.add(("checks_running", "checks_pending"))

    actual = {
        (from_state, to_state)
        for from_state in issue_wave.ALL_STATES
        for to_state in issue_wave.ALL_STATES
        if issue_wave._allowed_transition(from_state, to_state)
    }
    assert actual == expected
    assert ("selected", "c_running") not in actual
    assert issue_wave.allowed_next_states("unknown_agent_outcome") == []


def test_state_lock_expected_revision_unknown_keys_and_duplicate_json_fail_closed(
    tmp_path: Path,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    request = _event("lane-1", "selected", "a_running")

    with pytest.raises(issue_wave.IssueWaveError, match="expected revision"):
        issue_wave.transition_run(
            workspace,
            RUN_ID,
            expected_revision=1,
            request_value=request,
            now=FIXED_NOW + timedelta(seconds=1),
        )
    request["unknown"] = True
    with pytest.raises(issue_wave.IssueWaveError, match="shape"):
        _transition(workspace, state, request)
    request.pop("unknown")
    (run_directory / ".transition.lock").write_text("held\n", encoding="utf-8")
    with pytest.raises(issue_wave.IssueWaveError) as locked:
        _transition(workspace, state, request)
    assert locked.value.code == "state_locked"
    (run_directory / ".transition.lock").unlink()

    duplicate = b'{"schema_version":"x","schema_version":"y"}\n'
    (run_directory / "run.json").write_bytes(duplicate)
    with pytest.raises(issue_wave.IssueWaveError) as corrupt:
        issue_wave.load_run(workspace, RUN_ID)
    assert corrupt.value.code in {"invalid_json", "state_integrity_error"}


def test_atomic_projection_recovers_one_flushed_event_without_touching_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    worktree = tmp_path / "worktrees" / "lane-1"
    worktree.mkdir(parents=True)
    request = _event(
        "lane-1",
        "selected",
        "a_running",
        updates={"branch": "issue/101", "worktree_location": str(worktree)},
    )

    def fail_projection(path: Path, value: object) -> None:
        del path, value
        raise OSError("synthetic crash after event flush")

    monkeypatch.setattr(issue_wave, "_atomic_write_json", fail_projection)
    with pytest.raises(issue_wave.IssueWaveError) as crash:
        _transition(workspace, state, request)
    assert crash.value.code == "state_integrity_error"
    assert "after the event was recorded" in crash.value.message

    run_mtime = (run_directory / "run.json").stat().st_mtime_ns
    event_mtime = (run_directory / "events.jsonl").stat().st_mtime_ns
    _, recovered, was_recovered = issue_wave.load_run(workspace, RUN_ID)
    assert was_recovered is True
    assert recovered["revision"] == 1
    assert recovered["lanes"][0]["state"] == "a_running"
    assert (run_directory / "run.json").stat().st_mtime_ns == run_mtime
    assert (run_directory / "events.jsonl").stat().st_mtime_ns == event_mtime

    monkeypatch.undo()
    stopped = issue_wave.transition_run(
        workspace,
        RUN_ID,
        expected_revision=1,
        request_value=_event("lane-1", "a_running", "unknown_agent_outcome"),
        now=FIXED_NOW + timedelta(seconds=2),
    )
    assert stopped["lanes"][0]["state"] == "unknown_agent_outcome"
    assert issue_wave.allowed_next_states("unknown_agent_outcome") == []


def test_read_only_inspect_loads_when_recorded_worktree_is_now_missing(tmp_path: Path) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    shutil.rmtree(worktree)

    _, loaded, recovered = issue_wave.load_run(workspace, RUN_ID)

    assert recovered is False
    assert loaded["revision"] == state["revision"]
    assert loaded["lanes"][0]["state"] == "a_running"


def test_corrupt_tail_broken_hash_and_projection_more_than_one_behind_fail_closed(
    tmp_path: Path,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    events_path = run_directory / "events.jsonl"
    good_events = events_path.read_bytes()
    events_path.write_bytes(good_events + b"partial")
    with pytest.raises(issue_wave.IssueWaveError, match="invalid tail"):
        issue_wave.load_run(workspace, RUN_ID)

    events_path.write_bytes(good_events.replace(b'"previous_event_digest":"', b'"previous_event_digest":"f', 1))
    with pytest.raises(issue_wave.IssueWaveError):
        issue_wave.load_run(workspace, RUN_ID)

    events_path.write_bytes(good_events)
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "a_running",
            "a_complete",
            updates={"artifacts": ["docs/problem_representations/issue-101.md"]},
        ),
    )
    stale = deepcopy(state)
    stale["revision"] = 0
    stale["updated_at_utc"] = stale["created_at_utc"]
    stale["last_event_digest"] = issue_wave.ZERO_DIGEST
    stale["lanes"] = [issue_wave._initial_lane(stale["candidates"][0])]
    stale["run_complete"] = False
    (run_directory / "run.json").write_bytes(issue_wave._canonical_json(stale) + b"\n")
    with pytest.raises(issue_wave.IssueWaveError, match="disagree"):
        issue_wave.load_run(workspace, RUN_ID)


def test_resume_permissions_are_immutable_and_unknown_outcome_is_not_resumable(
    tmp_path: Path,
) -> None:
    invocation = _dispatch_invocation("allow-main-draft")
    workspace, run_directory, state = _init(tmp_path, invocation=invocation)
    inspect_resume = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Inspect (A; run={RUN_ID})")
    dispatch_resume = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (A; run={RUN_ID})")
    same_permission = issue_wave.parse_invocation(
        f"$mythic-edge-issue-wave Dispatch (A; run={RUN_ID}; allow-main-draft)"
    )
    issue_wave.validate_resume_invocation(inspect_resume, state)
    issue_wave.validate_resume_invocation(dispatch_resume, state)
    issue_wave.validate_resume_invocation(same_permission, state)
    _, _, unprivileged = _init(tmp_path / "unprivileged")
    escalated = issue_wave.parse_invocation(
        f"$mythic-edge-issue-wave Dispatch (A; run={RUN_ID}; allow-main-draft)"
    )
    with pytest.raises(issue_wave.IssueWaveError) as drift:
        issue_wave.validate_resume_invocation(escalated, unprivileged)
    assert drift.value.code == "permission_drift"

    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    state = _transition(
        workspace,
        state,
        _event("lane-1", "a_running", "unknown_agent_outcome"),
    )
    assert state["lanes"][0]["state"] == "unknown_agent_outcome"
    assert issue_wave.allowed_next_states("unknown_agent_outcome") == []
    assert not (run_directory / ".transition.lock").exists()


def test_public_output_redacts_paths_and_errors_do_not_echo_forbidden_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    workspace, _, state = _init(tmp_path)
    projection = issue_wave.inspect_projection(state, recovered_projection=False)
    encoded = json.dumps(projection)
    assert str(tmp_path) not in encoded
    assert projection["lanes"][0]["local_paths_redacted"] is True

    forbidden_input = "synthetic-input-that-must-not-echo"
    code = issue_wave.run(
        ["parse", f"$mythic-edge-issue-wave Inspect (A; {forbidden_input})"]
    )
    output = capsys.readouterr().err
    assert code != 0
    assert forbidden_input not in output
    assert "invalid_invocation" in output


def _synthetic_private_path_shapes() -> list[str]:
    separator = "\\"
    drive_path = "C:" + separator + separator.join(
        ["Users", "Example", "private.txt"]
    )
    unc_path = separator * 2 + separator.join(
        ["server", "share", "private.txt"]
    )
    unix_home = "/" + "/".join(["home", "example", "private.txt"])
    unix_user = "/" + "/".join(["Users", "Example", "private.txt"])
    unix_temp = "/" + "/".join(["tmp", "private.txt"])
    unix_var = "/" + "/".join(["var", "lib", "private.txt"])
    unix_etc = "/" + "/".join(["etc", "private.conf"])
    unix_opt = "/" + "/".join(["opt", "private", "artifact.txt"])
    forward_unc = "//server/share/private.txt"
    return [
        drive_path,
        f"before {drive_path}",
        f"({drive_path})",
        f"[local]({drive_path})",
        unix_home,
        f"[local]({unix_user})",
        f"({unix_temp})",
        f"see,{unix_var}",
        unc_path,
        f"[local]({unc_path})",
        unix_etc,
        f"before,{unix_opt}",
        f"[local]({unix_etc})",
        forward_unc,
        f"[local]({forward_unc})",
    ]


@pytest.mark.parametrize("unsafe", _synthetic_private_path_shapes())
def test_public_text_rejects_local_paths_at_every_text_boundary_without_echo(
    unsafe: str,
) -> None:
    with pytest.raises(issue_wave.IssueWaveError) as error:
        issue_wave._public_text(
            unsafe,
            code="invalid_public_text",
            label="public summary",
        )
    assert error.value.code == "invalid_public_text"
    assert "local absolute path" in error.value.message
    assert unsafe not in error.value.message


@pytest.mark.parametrize(
    "safe",
    [
        "docs/contracts/example.md",
        "repository-relative/path.txt",
        "https://github.com/example/repository/issues/1",
        "<private-path-redacted>",
        "Use the symbolic workspace root.",
    ],
)
def test_public_text_accepts_relative_symbolic_and_https_text(safe: str) -> None:
    assert issue_wave._public_text(
        safe,
        code="invalid_public_text",
        label="public summary",
    ) == safe


def test_public_path_rejection_applies_to_representative_public_fields(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    unsafe = _synthetic_private_path_shapes()[2]
    workspace, invocation, manifest, roots = _fixture(tmp_path)
    manifest["candidates"][0]["evidence"]["summary"] = unsafe
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_bytes(issue_wave._canonical_json(manifest))
    target_root = next(iter(roots.values()))

    code = issue_wave.run(
        [
            "init",
            "$mythic-edge-issue-wave Dispatch (A)",
            "--manifest",
            str(manifest_path),
            "--workspace-root",
            str(workspace),
            "--target-root",
            f"{REPOSITORIES[0]}={target_root}",
            "--run-id",
            RUN_ID,
        ]
    )
    error_output = capsys.readouterr().err
    assert code != 0
    assert unsafe not in error_output
    assert not (workspace / ".codex").exists()

    with pytest.raises(issue_wave.IssueWaveError, match="local absolute path"):
        issue_wave._public_string_list(
            [unsafe],
            code="invalid_transition",
            label="artifact references",
        )
    with pytest.raises(issue_wave.IssueWaveError, match="local absolute path"):
        issue_wave._validate_checks({"status": "running", "summary": unsafe})


def test_reviewed_package_binding_uses_exact_utf8_order_bytes_modes_and_deletion_identity() -> None:
    base_commit = "a" * 40
    package = {
        "schema_version": issue_wave.REVIEWED_PACKAGE_SCHEMA,
        "base_commit": base_commit,
        "entries": [
            _package_entry("a.txt", "added", b"alpha\n"),
            _package_entry("deleted.txt", "deleted", b"old bytes\n"),
            _package_entry("executable.sh", "modified", b"#!/bin/sh\n", mode="100755"),
            _package_entry("\u00e9.txt", "added", b"utf8\n"),
        ],
    }

    binding = issue_wave.bind_reviewed_package(package)
    expected_bytes = json.dumps(
        package,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    assert binding == {
        "schema_version": issue_wave.REVIEWED_PACKAGE_SCHEMA,
        "base_commit": base_commit,
        "paths": ["a.txt", "deleted.txt", "executable.sh", "\u00e9.txt"],
        "reviewed_package_sha256": hashlib.sha256(expected_bytes).hexdigest(),
    }
    assert b"\xc3\xa9.txt" in expected_bytes
    assert not expected_bytes.endswith(b"\n")


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("unknown_key", "shape"),
        ("empty", "nonempty"),
        ("duplicate_path", "unique"),
        ("unsorted", "ordered"),
        ("absolute_path", "path"),
        ("dot_segment", "path"),
        ("backslash", "path"),
        ("status", "status"),
        ("mode", "mode"),
        ("type", "type"),
        ("negative_length", "nonnegative"),
        ("digest", "digest"),
        ("base", "base"),
    ],
)
def test_reviewed_package_schema_rejects_noncanonical_or_unsupported_values(
    mutation: str,
    message: str,
) -> None:
    package = _single_file_package("a" * 40, "a.txt", b"alpha\n")
    if mutation == "unknown_key":
        package["unknown"] = True
    elif mutation == "empty":
        package["entries"] = []
    elif mutation == "duplicate_path":
        package["entries"].append(deepcopy(package["entries"][0]))
    elif mutation == "unsorted":
        package["entries"] = [
            _package_entry("z.txt", "added", b"z"),
            _package_entry("a.txt", "added", b"a"),
        ]
    elif mutation == "absolute_path":
        package["entries"][0]["path"] = "/a.txt"
    elif mutation == "dot_segment":
        package["entries"][0]["path"] = "a/../b.txt"
    elif mutation == "backslash":
        package["entries"][0]["path"] = "a\\b.txt"
    elif mutation == "status":
        package["entries"][0]["status"] = "renamed"
    elif mutation == "mode":
        package["entries"][0]["object"]["mode"] = "120000"
    elif mutation == "type":
        package["entries"][0]["object"]["type"] = "tree"
    elif mutation == "negative_length":
        package["entries"][0]["object"]["byte_length"] = -1
    elif mutation == "digest":
        package["entries"][0]["object"]["sha256"] = "A" * 64
    else:
        package["base_commit"] = "A" * 40

    with pytest.raises(issue_wave.IssueWaveError, match=message) as error:
        issue_wave.bind_reviewed_package(package)
    assert error.value.code == "invalid_reviewed_package"


def test_bind_package_cli_is_read_only_and_rejects_duplicate_json_keys(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    package_path = tmp_path / "package.json"
    package = _single_file_package("a" * 40, "a.txt", b"alpha\n")
    package_path.write_bytes(issue_wave._canonical_package_json(package))
    before = sorted(path.name for path in tmp_path.iterdir())

    assert issue_wave.run(["bind-package", "--manifest", str(package_path)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["reviewed_package_sha256"] == issue_wave.bind_reviewed_package(package)[
        "reviewed_package_sha256"
    ]
    assert sorted(path.name for path in tmp_path.iterdir()) == before

    package_path.write_text(
        '{"schema_version":"x","schema_version":"y"}', encoding="utf-8"
    )
    assert issue_wave.run(["bind-package", "--manifest", str(package_path)]) != 0
    assert "invalid_json" in capsys.readouterr().err


def test_e_and_f_package_identity_fields_are_role_scoped_and_immutable(tmp_path: Path) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, "issue/101")
    reviewed_digest = "b" * 64

    with pytest.raises(issue_wave.IssueWaveError, match="updates"):
        _transition(
            workspace,
            state,
            _event(
                "lane-1",
                "e_running",
                "e_approved",
                updates={
                    "reviewed_commit": "a" * 40,
                    "validation_summary": ["stale pre-F field"],
                },
            ),
        )

    state = _approve_e_package(workspace, state, "lane-1", "a" * 40, reviewed_digest)
    lane = state["lanes"][0]
    assert lane["review_base_commit"] == "a" * 40
    assert lane["reviewed_package_sha256"] == reviewed_digest
    assert lane["created_commit"] is None
    assert lane["submitted_package_sha256"] is None
    state = _transition(workspace, state, _event("lane-1", "e_approved", "f_running"))

    with pytest.raises(issue_wave.IssueWaveError, match="does not match"):
        _transition(
            workspace,
            state,
            _event(
                "lane-1",
                "f_running",
                "f_complete",
                updates={
                    "created_commit": "c" * 40,
                    "submitted_package_sha256": "d" * 64,
                    "branch": "issue/101",
                    "draft_pr": 901,
                },
            ),
        )

    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "f_running",
            "f_complete",
            updates={
                "created_commit": "c" * 40,
                "submitted_package_sha256": reviewed_digest,
                "branch": "issue/101",
                "draft_pr": 901,
            },
        ),
    )
    lane = state["lanes"][0]
    assert lane["created_commit"] == "c" * 40
    assert lane["submitted_package_sha256"] == reviewed_digest

    with pytest.raises(issue_wave.IssueWaveError, match="not allowed"):
        _transition(
            workspace,
            state,
            _event(
                "lane-1",
                "f_complete",
                "checks_running",
                updates={
                    "created_commit": "e" * 40,
                    "checks": {"status": "running", "summary": "checks running"},
                },
            ),
        )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("draft_pr", 901, "draft PR update is not allowed here"),
        (
            "checks",
            {"status": "running", "summary": "premature checks claim"},
            "check evidence update is not allowed here",
        ),
    ],
)
def test_e_approval_rejects_submission_and_check_claims(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, "issue/101")
    updates: dict[str, object] = {
        "review_base_commit": "a" * 40,
        "reviewed_package_sha256": "b" * 64,
        "validation_summary": ["independent E approval"],
        field: value,
    }

    with pytest.raises(issue_wave.IssueWaveError, match=message):
        _transition(
            workspace,
            state,
            _event("lane-1", "e_running", "e_approved", updates=updates),
        )


@pytest.mark.parametrize(
    ("branch_update", "draft_pr_update", "message"),
    [
        (None, 901, "must reassert the bound issue branch"),
        ("issue/other", 901, "does not match the bound issue branch"),
        ("issue/101", "missing", "newly recorded positive draft PR"),
        ("issue/101", None, "newly recorded positive draft PR"),
    ],
)
def test_f_completion_requires_new_matching_branch_and_pr_evidence(
    tmp_path: Path,
    branch_update: str | None,
    draft_pr_update: int | str | None,
    message: str,
) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, "issue/101")
    reviewed_digest = "b" * 64
    state = _approve_e_package(workspace, state, "lane-1", "a" * 40, reviewed_digest)
    state = _transition(workspace, state, _event("lane-1", "e_approved", "f_running"))
    updates: dict[str, object] = {
        "created_commit": "c" * 40,
        "submitted_package_sha256": reviewed_digest,
    }
    if branch_update is not None:
        updates["branch"] = branch_update
    if draft_pr_update != "missing":
        updates["draft_pr"] = draft_pr_update

    with pytest.raises(issue_wave.IssueWaveError, match=message):
        _transition(
            workspace,
            state,
            _event("lane-1", "f_running", "f_complete", updates=updates),
        )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("branch", "issue/101", "branch update is not allowed here"),
        ("draft_pr", 902, "draft PR update is not allowed here"),
    ],
)
def test_post_f_branch_and_pr_are_immutable(
    tmp_path: Path,
    field: str,
    value: object,
    message: str,
) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, "issue/101")
    reviewed_digest = "b" * 64
    state = _approve_e_package(workspace, state, "lane-1", "a" * 40, reviewed_digest)
    state = _transition(workspace, state, _event("lane-1", "e_approved", "f_running"))
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "f_running",
            "f_complete",
            updates={
                "created_commit": "c" * 40,
                "submitted_package_sha256": reviewed_digest,
                "branch": "issue/101",
                "draft_pr": 901,
            },
        ),
    )
    updates = {
        "checks": {"status": "running", "summary": "checks running"},
        field: value,
    }

    with pytest.raises(issue_wave.IssueWaveError, match=message):
        _transition(
            workspace,
            state,
            _event("lane-1", "f_complete", "checks_running", updates=updates),
        )


@pytest.mark.parametrize(
    ("from_state", "to_state", "required_status", "wrong_status"),
    [
        ("f_complete", "checks_running", "running", "passed"),
        ("checks_running", "g_consideration_ready", "passed", "failed"),
        ("checks_running", "d_required", "failed", "pending"),
        ("checks_running", "checks_pending", "pending", "running"),
    ],
)
def test_check_evidence_is_scoped_to_exact_check_transition(
    tmp_path: Path,
    from_state: str,
    to_state: str,
    required_status: str,
    wrong_status: str,
) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, "issue/101")
    reviewed_digest = "b" * 64
    state = _approve_e_package(workspace, state, "lane-1", "a" * 40, reviewed_digest)
    state = _transition(workspace, state, _event("lane-1", "e_approved", "f_running"))
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "f_running",
            "f_complete",
            updates={
                "created_commit": "c" * 40,
                "submitted_package_sha256": reviewed_digest,
                "branch": "issue/101",
                "draft_pr": 901,
            },
        ),
    )
    if from_state == "checks_running":
        state = _transition(
            workspace,
            state,
            _event(
                "lane-1",
                "f_complete",
                "checks_running",
                updates={
                    "checks": {"status": "running", "summary": "checks running"}
                },
            ),
        )

    with pytest.raises(issue_wave.IssueWaveError, match="does not match"):
        _transition(
            workspace,
            state,
            _event(
                "lane-1",
                from_state,
                to_state,
                updates={
                    "checks": {"status": wrong_status, "summary": "wrong check evidence"}
                },
            ),
        )

    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            from_state,
            to_state,
            updates={
                "checks": {"status": required_status, "summary": "exact check evidence"}
            },
        ),
    )
    assert state["lanes"][0]["state"] == to_state
    assert state["lanes"][0]["checks"]["status"] == required_status


def _git(*args: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _git_bytes(*args: str, cwd: Path) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def _git_returncode(*args: str, cwd: Path) -> int:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
    ).returncode


def _package_entry(
    path: str,
    status: str,
    payload: bytes,
    *,
    mode: str = "100644",
) -> dict[str, object]:
    return {
        "path": path,
        "status": status,
        "object": {
            "type": "blob",
            "mode": mode,
            "byte_length": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        },
    }


def _single_file_package(
    base_commit: str,
    path: str,
    payload: bytes,
    *,
    status: str = "added",
    mode: str = "100644",
) -> dict[str, object]:
    return {
        "schema_version": issue_wave.REVIEWED_PACKAGE_SCHEMA,
        "base_commit": base_commit,
        "entries": [_package_entry(path, status, payload, mode=mode)],
    }


def _worktree_added_package(worktree: Path, base_commit: str, path: str) -> dict[str, object]:
    return _single_file_package(base_commit, path, worktree.joinpath(path).read_bytes())


def _index_added_package(worktree: Path, base_commit: str, path: str) -> dict[str, object]:
    fields = _git("ls-files", "--stage", "--", path, cwd=worktree).split()
    assert len(fields) >= 4
    return _single_file_package(
        base_commit,
        path,
        _git_bytes("show", f":{path}", cwd=worktree),
        mode=fields[0],
    )


def _commit_added_package(
    worktree: Path,
    base_commit: str,
    commit: str,
    path: str,
) -> dict[str, object]:
    fields = _git("ls-tree", commit, "--", path, cwd=worktree).split()
    assert len(fields) >= 4
    return _single_file_package(
        base_commit,
        path,
        _git_bytes("show", f"{commit}:{path}", cwd=worktree),
        mode=fields[0],
    )


def _synthetic_git_fixture(
    tmp_path: Path,
    *,
    lane_count: int = 3,
) -> tuple[Path, dict[str, Path], dict[str, object]]:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    remotes = tmp_path / "remotes"
    remotes.mkdir()
    repositories: dict[str, Path] = {}
    candidates: list[dict[str, object]] = []
    for index, repository in enumerate(REPOSITORIES[:lane_count], start=1):
        remote = remotes / f"remote-{index}.git"
        _git("init", "--bare", str(remote))
        checkout = tmp_path / "checkouts" / f"repo-{index}"
        checkout.parent.mkdir(exist_ok=True)
        _git("init", "-b", "main", str(checkout))
        checkout.joinpath("seed.txt").write_text(f"seed {index}\n", encoding="utf-8")
        _git("add", "seed.txt", cwd=checkout)
        _git(
            "-c",
            "user.name=Synthetic Codex",
            "-c",
            "user.email=synthetic@example.invalid",
            "commit",
            "-m",
            "seed",
            cwd=checkout,
        )
        _git("remote", "add", "origin", str(remote), cwd=checkout)
        _git("push", "-u", "origin", "main", cwd=checkout)
        repositories[repository] = checkout
        candidates.append(
            _candidate(
                checkout,
                repository,
                200 + index,
                lane_id=f"lane-{index}",
                created_at=f"2026080{index}T120000Z",
            )
        )
    return workspace, repositories, {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": candidates,
    }


def _advance_to_e_running(
    workspace: Path,
    state: dict[str, object],
    lane_id: str,
    worktree: Path,
    branch: str,
) -> dict[str, object]:
    state = _transition(
        workspace,
        state,
        _event(
            lane_id,
            "selected",
            "a_running",
            updates={"worktree_location": str(worktree), "branch": branch},
        ),
    )
    state = _transition(
        workspace,
        state,
        _event(
            lane_id,
            "a_running",
            "a_complete",
            updates={"artifacts": [f"docs/problem_representations/{lane_id}.md"]},
        ),
    )
    state = _transition(workspace, state, _event(lane_id, "a_complete", "a_scope_verified"))
    state = _transition(workspace, state, _event(lane_id, "a_scope_verified", "b_running"))
    state = _transition(
        workspace,
        state,
        _event(
            lane_id,
            "b_running",
            "b_complete",
            updates={"artifacts": [f"docs/contracts/{lane_id}.md"]},
        ),
    )
    state = _transition(workspace, state, _event(lane_id, "b_complete", "c_running"))
    state = _transition(
        workspace,
        state,
        _event(
            lane_id,
            "c_running",
            "c_complete",
            updates={
                "artifacts": [f"docs/implementation_handoffs/{lane_id}.md"],
                "validation_summary": [f"focused tests passed for {lane_id}"],
            },
        ),
    )
    return _transition(workspace, state, _event(lane_id, "c_complete", "e_running"))


def _approve_e_package(
    workspace: Path,
    state: dict[str, object],
    lane_id: str,
    review_base_commit: str,
    reviewed_package_sha256: str,
) -> dict[str, object]:
    return _transition(
        workspace,
        state,
        _event(
            lane_id,
            "e_running",
            "e_approved",
            updates={
                "review_base_commit": review_base_commit,
                "reviewed_package_sha256": reviewed_package_sha256,
                "validation_summary": [f"independent E approved {lane_id}"],
            },
        ),
    )


def _complete_f_and_start_checks(
    workspace: Path,
    state: dict[str, object],
    lane_id: str,
    created_commit: str,
    submitted_package_sha256: str,
    branch: str,
    draft_pr: int,
) -> dict[str, object]:
    state = _transition(
        workspace,
        state,
        _event(
            lane_id,
            "f_running",
            "f_complete",
            updates={
                "created_commit": created_commit,
                "submitted_package_sha256": submitted_package_sha256,
                "branch": branch,
                "draft_pr": draft_pr,
            },
        ),
    )
    return _transition(
        workspace,
        state,
        _event(
            lane_id,
            "f_complete",
            "checks_running",
            updates={"checks": {"status": "running", "summary": "Mocked required checks are running."}},
        ),
    )


@pytest.mark.integration
@pytest.mark.parametrize(
    "drift_dimension",
    ["base", "path", "status", "mode", "type", "byte", "length", "hash", "package"],
)
def test_post_e_reviewed_package_drift_routes_to_d_without_commit_push_or_pr(
    tmp_path: Path,
    drift_dimension: str,
) -> None:
    workspace, repositories, manifest = _synthetic_git_fixture(tmp_path, lane_count=1)
    _, state = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        manifest,
        target_roots=repositories,
        run_id=RUN_ID,
        now=FIXED_NOW,
    )
    candidate = manifest["candidates"][0]
    checkout = repositories[candidate["repository"]]
    branch = f"issue/{candidate['issue']}"
    worktree = tmp_path / "worktrees" / "lane-1"
    worktree.parent.mkdir()
    _git("worktree", "add", "-b", branch, str(worktree), cwd=checkout)
    payload = b"reviewed bytes\n"
    worktree.joinpath("synthetic.txt").write_bytes(payload)
    review_base = _git("rev-parse", "HEAD", cwd=worktree)
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, branch)
    reviewed_package = _worktree_added_package(worktree, review_base, "synthetic.txt")
    reviewed_binding = issue_wave.bind_reviewed_package(reviewed_package)[
        "reviewed_package_sha256"
    ]
    state = _approve_e_package(
        workspace,
        state,
        "lane-1",
        review_base,
        reviewed_binding,
    )

    drifted = deepcopy(reviewed_package)
    entry = drifted["entries"][0]
    if drift_dimension == "base":
        drifted["base_commit"] = "f" * 40
    elif drift_dimension == "path":
        entry["path"] = "renamed.txt"
    elif drift_dimension == "status":
        entry["status"] = "modified"
    elif drift_dimension == "mode":
        entry["object"]["mode"] = "100755"
    elif drift_dimension == "type":
        entry["object"]["type"] = "tree"
    elif drift_dimension == "byte":
        changed = b"different reviewed bytes\n"
        entry["object"]["byte_length"] = len(changed)
        entry["object"]["sha256"] = hashlib.sha256(changed).hexdigest()
    elif drift_dimension == "length":
        entry["object"]["byte_length"] += 1
    elif drift_dimension == "hash":
        entry["object"]["sha256"] = "0" * 64
    else:
        drifted["entries"].append(_package_entry("z-extra.txt", "added", b"extra\n"))

    try:
        current_binding = issue_wave.bind_reviewed_package(drifted)[
            "reviewed_package_sha256"
        ]
    except issue_wave.IssueWaveError:
        current_binding = None
    assert current_binding != reviewed_binding
    state = _transition(
        workspace,
        state,
        _event("lane-1", "e_approved", "d_required"),
    )

    lane = state["lanes"][0]
    assert lane["state"] == "d_required"
    assert lane["created_commit"] is None
    assert lane["submitted_package_sha256"] is None
    assert lane["draft_pr"] is None
    assert _git("rev-parse", "HEAD", cwd=worktree) == review_base
    assert _git_returncode("diff", "--cached", "--quiet", cwd=worktree) == 0
    assert _git("ls-remote", "--heads", "origin", branch, cwd=worktree) == ""


@pytest.mark.integration
def test_synthetic_three_lane_dispatch_uses_local_remotes_and_mocked_pr_ci(
    tmp_path: Path,
) -> None:
    workspace, repositories, manifest = _synthetic_git_fixture(tmp_path)
    _, state = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        manifest,
        target_roots=repositories,
        run_id=RUN_ID,
        now=FIXED_NOW,
    )
    worktree_root = tmp_path / "worktrees"
    worktree_root.mkdir()
    reviews: dict[str, dict[str, object]] = {}
    for index, candidate in enumerate(manifest["candidates"], start=1):
        lane_id = candidate["lane_id"]
        checkout = repositories[candidate["repository"]]
        branch = f"issue/{candidate['issue']}"
        worktree = worktree_root / lane_id
        _git("worktree", "add", "-b", branch, str(worktree), cwd=checkout)
        worktree.joinpath("synthetic.txt").write_bytes(f"synthetic {lane_id}\n".encode("utf-8"))
        review_base = _git("rev-parse", "HEAD", cwd=worktree)
        state = _advance_to_e_running(workspace, state, lane_id, worktree, branch)
        reviewed_manifest = _worktree_added_package(
            worktree, review_base, "synthetic.txt"
        )
        binding = issue_wave.bind_reviewed_package(reviewed_manifest)
        assert _git("rev-parse", "HEAD", cwd=worktree) == review_base
        assert _git_returncode("diff", "--cached", "--quiet", cwd=worktree) == 0
        assert _git("ls-remote", "--heads", "origin", branch, cwd=worktree) == ""
        state = _approve_e_package(
            workspace,
            state,
            lane_id,
            review_base,
            binding["reviewed_package_sha256"],
        )
        reviews[lane_id] = {
            "worktree": worktree,
            "branch": branch,
            "base": review_base,
            "binding": binding["reviewed_package_sha256"],
        }

    for index, candidate in enumerate(manifest["candidates"], start=1):
        lane_id = candidate["lane_id"]
        review = reviews[lane_id]
        worktree = review["worktree"]
        branch = review["branch"]
        review_base = review["base"]
        reviewed_binding = review["binding"]
        assert isinstance(worktree, Path)
        assert isinstance(branch, str)
        assert isinstance(review_base, str)
        assert isinstance(reviewed_binding, str)

        current_binding = issue_wave.bind_reviewed_package(
            _worktree_added_package(worktree, review_base, "synthetic.txt")
        )["reviewed_package_sha256"]
        assert current_binding == reviewed_binding
        assert _git_returncode("diff", "--cached", "--quiet", cwd=worktree) == 0
        state = _transition(
            workspace,
            state,
            _event(lane_id, "e_approved", "f_running"),
        )
        _git("add", "--", "synthetic.txt", cwd=worktree)
        staged_binding = issue_wave.bind_reviewed_package(
            _index_added_package(worktree, review_base, "synthetic.txt")
        )["reviewed_package_sha256"]
        assert staged_binding == reviewed_binding
        _git(
            "-c",
            "user.name=Synthetic Codex",
            "-c",
            "user.email=synthetic@example.invalid",
            "commit",
            "-m",
            f"synthetic {lane_id}",
            cwd=worktree,
        )
        created_commit = _git("rev-parse", "HEAD", cwd=worktree)
        assert _git("rev-list", "--parents", "-n", "1", created_commit, cwd=worktree).split() == [
            created_commit,
            review_base,
        ]
        committed_binding = issue_wave.bind_reviewed_package(
            _commit_added_package(
                worktree,
                review_base,
                created_commit,
                "synthetic.txt",
            )
        )["reviewed_package_sha256"]
        assert committed_binding == reviewed_binding
        _git("push", "-u", "origin", branch, cwd=worktree)
        state = _complete_f_and_start_checks(
            workspace,
            state,
            lane_id,
            created_commit,
            committed_binding,
            branch,
            900 + index,
        )

    outcomes = {"lane-1": "passed", "lane-2": "failed", "lane-3": "pending"}
    destinations = {
        "passed": "g_consideration_ready",
        "failed": "d_required",
        "pending": "checks_pending",
    }
    for lane_id, outcome in outcomes.items():
        state = _transition(
            workspace,
            state,
            _event(
                lane_id,
                "checks_running",
                destinations[outcome],
                updates={
                    "checks": {
                        "status": outcome,
                        "summary": f"Mocked CI boundary returned {outcome}.",
                    }
                },
            ),
        )

    assert {lane["lane_id"]: lane["state"] for lane in state["lanes"]} == {
        "lane-1": "g_consideration_ready",
        "lane-2": "d_required",
        "lane-3": "checks_pending",
    }
    assert state["run_complete"] is True
    for repository, checkout in repositories.items():
        assert _git("ls-remote", "--heads", "origin", cwd=checkout)
        assert repository in REPOSITORIES


@pytest.mark.integration
@pytest.mark.parametrize("lane_count", [1, 2])
def test_synthetic_single_and_two_lane_dispatch_use_disposable_local_remotes(
    tmp_path: Path,
    lane_count: int,
) -> None:
    workspace, repositories, manifest = _synthetic_git_fixture(tmp_path, lane_count=lane_count)
    _, state = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        manifest,
        target_roots=repositories,
        run_id=RUN_ID,
        now=FIXED_NOW,
    )
    for index, lane in enumerate(state["lanes"], start=1):
        checkout = repositories[lane["repository"]]
        worktree = tmp_path / "worktrees" / lane["lane_id"]
        worktree.parent.mkdir(exist_ok=True)
        branch = f"issue/{lane['issue']}"
        _git("worktree", "add", "-b", branch, str(worktree), cwd=checkout)
        state = _transition(
            workspace,
            state,
            _event(
                lane["lane_id"],
                "selected",
                "a_running",
                updates={"branch": branch, "worktree_location": str(worktree)},
            ),
        )
        state = _transition(
            workspace,
            state,
            _event(lane["lane_id"], "a_running", "a_ambiguous"),
        )
        assert index <= lane_count

    assert len(state["lanes"]) == lane_count
    assert all(lane["state"] == "a_ambiguous" for lane in state["lanes"])
    assert state["run_complete"] is True


@pytest.mark.integration
def test_synthetic_post_a_overlap_stops_conflicts_without_backfill_and_continues_unaffected(
    tmp_path: Path,
) -> None:
    workspace, _, state = _init(tmp_path, lane_count=3)
    for index in range(1, 4):
        worktree = tmp_path / "worktrees" / f"lane-{index}"
        worktree.mkdir(parents=True)
        state = _transition(
            workspace,
            state,
            _event(
                f"lane-{index}",
                "selected",
                "a_running",
                updates={"branch": f"issue/{100 + index}", "worktree_location": str(worktree)},
            ),
        )

    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "a_running",
            "a_complete",
            updates={"artifacts": ["docs/problem_representations/lane-1.md"]},
        ),
    )
    overlapping = _scope("post-a-overlap")
    for lane_id in ("lane-2", "lane-3"):
        state = _transition(
            workspace,
            state,
            _event(
                lane_id,
                "a_running",
                "a_complete",
                updates={
                    "artifacts": [f"docs/problem_representations/{lane_id}.md"],
                    "scope": overlapping,
                },
            ),
        )
    state = _transition(
        workspace,
        state,
        _event("lane-2", "a_complete", "unsafe_or_conflicting_scope"),
    )
    state = _transition(
        workspace,
        state,
        _event("lane-3", "a_complete", "unsafe_or_conflicting_scope"),
    )
    state = _transition(
        workspace,
        state,
        _event("lane-1", "a_complete", "a_scope_verified"),
    )

    assert [lane["lane_id"] for lane in state["lanes"]] == ["lane-1", "lane-2", "lane-3"]
    assert [lane["state"] for lane in state["lanes"]] == [
        "a_scope_verified",
        "unsafe_or_conflicting_scope",
        "unsafe_or_conflicting_scope",
    ]
    assert state["run_complete"] is False


@pytest.mark.integration
def test_synthetic_e_finding_routes_to_d_required(tmp_path: Path) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _advance_to_e_running(workspace, state, "lane-1", worktree, "issue/101")
    state = _transition(workspace, state, _event("lane-1", "e_running", "d_required"))
    assert state["lanes"][0]["state"] == "d_required"
    assert state["lanes"][0]["stop_reason"] == "d_required"


def test_governance_packets_are_redacted_aggregated_once_and_have_task_fallback(
    tmp_path: Path,
) -> None:
    workspace, _, state = _init(tmp_path)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    packet = {
        "schema_version": issue_wave.GOVERNANCE_PACKET_SCHEMA,
        "run_id": RUN_ID,
        "lane_id": "lane-1",
        "repository": REPOSITORIES[0],
        "issue": 101,
        "role": "A",
        "trigger_category": "a_ambiguity",
        "evidence_summary": "Current public authority leaves the dependency edge unresolved.",
        "impact": "The lane cannot be framed safely.",
        "repeated_pattern_count": None,
        "unresolved_question": "Which durable dependency edge controls this issue?",
        "suggested_review_route": "mythic-edge-constitutional-lawyer",
    }
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "a_running",
            "a_ambiguous",
            updates={"governance_packets": [packet]},
        ),
    )
    available = issue_wave.aggregate_governance_packets(state, task_creation_available=True)
    fallback = issue_wave.aggregate_governance_packets(state, task_creation_available=False)
    assert available["packet_count"] == fallback["packet_count"] == 1
    assert available["action"] == "root_create_one_read_only_task"
    assert fallback["action"] == "return_pasteable_prompt"
    assert "$mythic-edge-constitutional-lawyer" in fallback["prompt"]

    unsafe = deepcopy(packet)
    unsafe["evidence_summary"] = f"See {tmp_path} for private evidence."
    with pytest.raises(issue_wave.IssueWaveError, match="local absolute path"):
        issue_wave._validate_governance_packet(
            unsafe,
            run_id=RUN_ID,
            lane=state["lanes"][0],
        )


@pytest.mark.parametrize(
    ("token", "start", "end"),
    [("A-A", "A", "A"), ("A-B", "A", "B"), ("A-C", "A", "C"), ("A-E", "A", "E"), ("A-F", "A", "F")],
)
def test_parse_new_dispatch_checkpoint_segments(token: str, start: str, end: str) -> None:
    parsed = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch ({token})")
    assert parsed["schema_version"] == "mythic_edge_issue_wave_invocation.v2"
    assert parsed["segment"] == {"start_role": start, "end_role": end, "explicit": True}


@pytest.mark.parametrize(
    "command",
    [
        "$mythic-edge-issue-wave Dispatch (B-B)",
        "$mythic-edge-issue-wave Dispatch (A-D)",
        f"$mythic-edge-issue-wave Dispatch (E-C; run={RUN_ID})",
        "$mythic-edge-issue-wave Dispatch (A-B; allow-main-draft)",
        f"$mythic-edge-issue-wave Dispatch (C-E; run={RUN_ID}; allow-wip-exception)",
    ],
)
def test_parse_rejects_misaligned_or_permission_incompatible_segments(command: str) -> None:
    with pytest.raises(issue_wave.IssueWaveError):
        issue_wave.parse_invocation(command)


def _complete_a_b_checkpoint(
    tmp_path: Path, workspace: Path, state: dict[str, object]
) -> dict[str, object]:
    worktree = tmp_path / "checkpoint-worktree"
    worktree.mkdir(parents=True, exist_ok=True)
    requests = (
        _event("lane-1", "selected", "a_running", updates={"branch": "issue/101", "worktree_location": str(worktree)}),
        _event(
            "lane-1",
            "a_running",
            "a_complete",
            updates={"artifacts": ["docs/problem_representations/issue-101.md"]},
        ),
        _event("lane-1", "a_complete", "a_scope_verified"),
        _event("lane-1", "a_scope_verified", "b_running"),
        _event("lane-1", "b_running", "b_complete", updates={"artifacts": ["docs/contracts/issue-101.md"]}),
    )
    for request in requests:
        state = _transition(workspace, state, request)
    return state


def _stable_revalidation_proof(state: dict[str, object]) -> dict[str, object]:
    lanes = []
    for lane in state["lanes"]:
        artifacts = [
            {
                "reference": reference,
                "expected_sha256": hashlib.sha256(reference.encode("utf-8")).hexdigest(),
                "observed_sha256": hashlib.sha256(reference.encode("utf-8")).hexdigest(),
            }
            for reference in lane["artifacts"]
        ]
        lanes.append(
            {
                "lane_id": lane["lane_id"],
                "repository": lane["repository"],
                "issue": lane["issue"],
                "repository_head": {"expected": "a" * 40, "observed": "a" * 40},
                "artifacts": artifacts,
            }
        )
    return {
        "repository_heads_stable": True,
        "artifacts_stable": True,
        "worktrees_safe": True,
        "no_active_operations": True,
        "lanes": lanes,
    }


def _projection_time(state: dict[str, object]) -> datetime:
    return datetime.strptime(state["updated_at_utc"], "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)


def _saved_run_bytes(run_directory: Path) -> tuple[bytes, bytes]:
    return (
        (run_directory / "run.json").read_bytes(),
        (run_directory / "events.jsonl").read_bytes(),
    )


def _complete_recovery_proof() -> dict[str, object]:
    return {
        "termination_method": "mechanically_verified",
        "former_task_stopped": True,
        "all_agents_stopped": True,
        "preserved_state_stable": True,
        "no_active_operations": True,
    }


@pytest.mark.parametrize(
    "scope_dimension",
    (
        "paths",
        "interfaces",
        "truth_owners",
        "dependencies",
        "shared_artifacts",
        "submission_lanes",
    ),
)
def test_cross_run_admission_uses_current_non_final_lane_scope_after_a(
    tmp_path: Path,
    scope_dimension: str,
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    first_root = tmp_path / "first-repository"
    second_root = tmp_path / "second-repository"
    first_root.mkdir()
    second_root.mkdir()

    initial_scope = _scope(f"historical-{scope_dimension}")
    refined_scope = _scope(f"current-{scope_dimension}")
    refined_token = f"global:post-a:{scope_dimension}"
    refined_scope[scope_dimension] = [refined_token]
    first_manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                first_root,
                REPOSITORIES[0],
                101,
                lane_id="lane-1",
                created_at="20260801T120000Z",
                scope=initial_scope,
            )
        ],
    }
    first_directory, state = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        first_manifest,
        target_roots={REPOSITORIES[0]: first_root},
        run_id=RUN_ID,
        now=FIXED_NOW,
    )
    candidate_history = deepcopy(state["candidates"][0]["scope"])
    state = _advance_one_lane_to_refined_a_scope(tmp_path, workspace, state, refined_scope)

    assert state["candidates"][0]["scope"] == candidate_history == initial_scope
    assert state["lanes"][0]["scope"] == refined_scope
    before = _saved_run_bytes(first_directory)
    before_revision = state["revision"]
    state_root_entries = sorted(path.name for path in first_directory.parent.iterdir())

    second_scope = _scope(f"incoming-{scope_dimension}")
    second_scope[scope_dimension] = [refined_token]
    second_run_id = "20260813T120010Z-0a0b0c0d"
    second_manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                second_root,
                REPOSITORIES[1],
                202,
                lane_id="lane-2",
                created_at="20260802T120000Z",
                scope=second_scope,
            )
        ],
    }
    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.init_run(
            workspace,
            _dispatch_invocation(),
            second_manifest,
            target_roots={REPOSITORIES[1]: second_root},
            run_id=second_run_id,
            now=FIXED_NOW + timedelta(seconds=10),
        )

    assert rejected.value.code == "unsafe_or_conflicting_scope"
    assert not (first_directory.parent / second_run_id).exists()
    assert sorted(path.name for path in first_directory.parent.iterdir()) == state_root_entries
    assert _saved_run_bytes(first_directory) == before
    _, unchanged, _ = issue_wave.load_run(workspace, RUN_ID)
    assert unchanged["revision"] == before_revision
    assert unchanged["candidates"][0]["scope"] == candidate_history
    assert unchanged["lanes"][0]["scope"] == refined_scope
    assert unchanged["reservation"]["repositories"] == [REPOSITORIES[0]]
    assert list(second_root.iterdir()) == []

    disjoint_manifest = deepcopy(second_manifest)
    disjoint_manifest["candidates"][0]["scope"] = _scope(
        f"disjoint-current-{scope_dimension}"
    )
    disjoint_directory, disjoint_state = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        disjoint_manifest,
        target_roots={REPOSITORIES[1]: second_root},
        run_id=second_run_id,
        now=FIXED_NOW + timedelta(seconds=11),
    )
    assert disjoint_directory.exists()
    assert disjoint_state["execution_status"] == "active"


def test_saved_run_reacquisition_uses_current_non_final_lane_scope(tmp_path: Path) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, first_directory, state = _init(tmp_path, invocation=invocation)
    initial_scope = deepcopy(state["candidates"][0]["scope"])
    refined_scope = _scope("resume-current")
    refined_scope["paths"] = ["global:resume-current:path"]
    state = _advance_one_lane_to_refined_a_scope(tmp_path, workspace, state, refined_scope)
    state = _transition(workspace, state, _event("lane-1", "a_scope_verified", "b_running"))
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "b_running",
            "b_complete",
            updates={"artifacts": ["docs/contracts/issue-101.md"]},
        ),
    )
    state = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=FIXED_NOW + timedelta(seconds=20),
    )
    assert state["candidates"][0]["scope"] == initial_scope
    assert state["lanes"][0]["scope"] == refined_scope

    second_root = tmp_path / "resume-conflict-repository"
    second_root.mkdir()
    second_scope = _scope("resume-conflict")
    second_scope["paths"] = list(refined_scope["paths"])
    second_run_id = "20260813T120021Z-0a0b0c0d"
    second_manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                second_root,
                REPOSITORIES[1],
                202,
                lane_id="lane-2",
                created_at="20260802T120000Z",
                scope=second_scope,
            )
        ],
    }
    second_directory, _ = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        second_manifest,
        target_roots={REPOSITORIES[1]: second_root},
        run_id=second_run_id,
        now=FIXED_NOW + timedelta(seconds=21),
    )
    first_before = _saved_run_bytes(first_directory)
    second_before = _saved_run_bytes(second_directory)
    resume = issue_wave.parse_invocation(
        f"$mythic-edge-issue-wave Dispatch (C-C; run={RUN_ID})"
    )

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.authorize_segment(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            invocation_value=resume,
            revalidation_proof=_stable_revalidation_proof(state),
            now=FIXED_NOW + timedelta(seconds=22),
        )

    assert rejected.value.code == "unsafe_or_conflicting_scope"
    assert _saved_run_bytes(first_directory) == first_before
    assert _saved_run_bytes(second_directory) == second_before


def test_final_lane_scope_is_excluded_without_releasing_other_admission_guards(
    tmp_path: Path,
) -> None:
    workspace, first_directory, state = _init(tmp_path)
    initial_scope = deepcopy(state["candidates"][0]["scope"])
    final_scope = _scope("final-current")
    final_scope["interfaces"] = ["global:final-current:interface"]
    worktree = tmp_path / "final-lane-worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "a_running",
            "a_ambiguous",
            updates={"scope": final_scope},
        ),
    )
    assert state["candidates"][0]["scope"] == initial_scope
    assert state["lanes"][0]["scope"] == final_scope
    assert state["lanes"][0]["state"] in issue_wave.FINAL_STATES

    second_root = tmp_path / "final-overlap-repository"
    second_root.mkdir()
    second_scope = _scope("final-overlap")
    second_scope["interfaces"] = list(final_scope["interfaces"])
    second_run_id = "20260813T120010Z-0a0b0c0d"
    second_manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                second_root,
                REPOSITORIES[1],
                202,
                lane_id="lane-2",
                created_at="20260802T120000Z",
                scope=second_scope,
            )
        ],
    }
    second_directory, _ = issue_wave.init_run(
        workspace,
        _dispatch_invocation(),
        second_manifest,
        target_roots={REPOSITORIES[1]: second_root},
        run_id=second_run_id,
        now=FIXED_NOW + timedelta(seconds=10),
    )
    assert first_directory.exists()
    assert second_directory.exists()

    third_root = tmp_path / "third-repository"
    third_root.mkdir()
    third_manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                third_root,
                REPOSITORIES[2],
                303,
                lane_id="lane-3",
                created_at="20260803T120000Z",
                scope=_scope("third-disjoint"),
            )
        ],
    }
    with pytest.raises(issue_wave.IssueWaveError) as capacity_blocked:
        issue_wave.init_run(
            workspace,
            _dispatch_invocation(),
            third_manifest,
            target_roots={REPOSITORIES[2]: third_root},
            run_id="20260813T120011Z-01020304",
            now=FIXED_NOW + timedelta(seconds=11),
        )
    assert capacity_blocked.value.code == "active_wave_limit"


@pytest.mark.parametrize("lane_count", [1, 2])
def test_expired_recovery_terminal_releases_all_final_runs_before_checkpoint(
    tmp_path: Path,
    lane_count: int,
) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-A)")
    workspace, run_directory, state = _init(
        tmp_path,
        lane_count=lane_count,
        invocation=invocation,
    )
    worktrees: list[Path] = []
    for index in range(1, lane_count + 1):
        lane_id = f"lane-{index}"
        worktree = tmp_path / f"all-final-worktree-{index}"
        worktree.mkdir()
        worktrees.append(worktree)
        state = _transition(
            workspace,
            state,
            _event(
                lane_id,
                "selected",
                "a_running",
                updates={
                    "branch": f"issue/{100 + index}",
                    "worktree_location": str(worktree),
                },
            ),
        )
        updates: dict[str, object] = {
            "artifacts": [f"docs/problem_representations/issue-{100 + index}.md"]
        }
        if lane_count == 2 and index == 1:
            lane = next(item for item in state["lanes"] if item["lane_id"] == lane_id)
            updates["governance_packets"] = [
                {
                    "schema_version": issue_wave.GOVERNANCE_PACKET_SCHEMA,
                    "run_id": RUN_ID,
                    "lane_id": lane_id,
                    "repository": lane["repository"],
                    "issue": lane["issue"],
                    "role": "A",
                    "trigger_category": "a_ambiguity",
                    "evidence_summary": "Current authority leaves one dependency edge unresolved.",
                    "impact": "The lane cannot be framed safely.",
                    "repeated_pattern_count": None,
                    "unresolved_question": "Which durable dependency edge controls this issue?",
                    "suggested_review_route": "mythic-edge-constitutional-lawyer",
                }
            ]
        state = _transition(
            workspace,
            state,
            _event(lane_id, "a_running", "a_ambiguous", updates=updates),
        )

    preserved_lanes = deepcopy(state["lanes"])
    before_revision = state["revision"]
    before_events = issue_wave._read_events(run_directory / "events.jsonl")
    expiry = issue_wave._timestamp_datetime(state["reservation"]["lease"]["expires_at_utc"])
    recovered = issue_wave.recover_expired_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        proof_value=_complete_recovery_proof(),
        now=expiry + timedelta(seconds=1),
    )
    events = issue_wave._read_events(run_directory / "events.jsonl")

    assert recovered["revision"] == before_revision + 1
    assert len(events) == len(before_events) + 1
    assert events[-1]["event_type"] == "terminal_release"
    assert events[-1]["previous_event_digest"] == before_events[-1]["event_digest"]
    assert recovered["execution_status"] == "terminal"
    assert recovered["next_resumable_role"] is None
    assert recovered["run_complete"] is True
    assert recovered["reservation"]["repositories"] == []
    assert recovered["reservation"]["lease"]["released_at_utc"] == events[-1][
        "timestamp_utc"
    ]
    assert recovered["reservation"]["recovery"] == {
        "termination_proof": "mechanically_verified",
        "preserved_state_stable": True,
        "no_active_operations": True,
    }
    for before_lane, after_lane, worktree in zip(
        preserved_lanes, recovered["lanes"], worktrees, strict=True
    ):
        assert after_lane["state"] == before_lane["state"] == "a_ambiguous"
        assert after_lane["worktree_location"] == before_lane["worktree_location"]
        assert after_lane["artifacts"] == before_lane["artifacts"]
        assert after_lane["governance_packets"] == before_lane["governance_packets"]
        assert worktree.exists()
    _, persisted, reconstructed = issue_wave.load_run(workspace, RUN_ID)
    assert reconstructed is False
    assert persisted == recovered

    governance = issue_wave.aggregate_governance_packets(
        recovered,
        task_creation_available=False,
    )
    assert governance["packet_count"] == (1 if lane_count == 2 else 0)
    assert governance["action"] == ("return_pasteable_prompt" if lane_count == 2 else "none")


def test_expired_recovery_keeps_checkpoint_then_unproven_stop_precedence(
    tmp_path: Path,
) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    checkpoint_root = tmp_path / "checkpoint-case"
    workspace, run_directory, state = _init(checkpoint_root, invocation=invocation)
    state = _complete_a_b_checkpoint(checkpoint_root, workspace, state)
    expiry = issue_wave._timestamp_datetime(state["reservation"]["lease"]["expires_at_utc"])
    checkpointed = issue_wave.recover_expired_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        proof_value=_complete_recovery_proof(),
        now=expiry + timedelta(seconds=1),
    )
    assert issue_wave._read_events(run_directory / "events.jsonl")[-1][
        "event_type"
    ] == "checkpoint_release"
    assert checkpointed["execution_status"] == "checkpointed"
    assert checkpointed["next_resumable_role"] == "C"
    assert checkpointed["run_complete"] is False

    unproven_root = tmp_path / "unproven-case"
    unproven_workspace, unproven_directory, unproven = _init(
        unproven_root,
        invocation=invocation,
    )
    unproven_expiry = issue_wave._timestamp_datetime(
        unproven["reservation"]["lease"]["expires_at_utc"]
    )
    stopped = issue_wave.recover_expired_run(
        unproven_workspace,
        RUN_ID,
        expected_revision=unproven["revision"],
        proof_value=_complete_recovery_proof(),
        now=unproven_expiry + timedelta(seconds=1),
    )
    assert issue_wave._read_events(unproven_directory / "events.jsonl")[-1][
        "event_type"
    ] == "interruption_stop"
    assert stopped["execution_status"] == "stopped"
    assert stopped["next_resumable_role"] is None
    assert stopped["run_complete"] is False


def test_lease_renewal_rejects_backward_time_without_mutation_and_accepts_equal_time(
    tmp_path: Path,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    current = _projection_time(state)
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.renew_lease(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            now=current - timedelta(seconds=1),
        )
    assert rejected.value.code == "invalid_time"
    assert _saved_run_bytes(run_directory) == before

    renewed = issue_wave.renew_lease(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=current,
    )
    assert renewed["updated_at_utc"] == state["updated_at_utc"]
    assert renewed["reservation"]["lease"]["last_renewed_at_utc"] == state["updated_at_utc"]


def test_checkpoint_release_rejects_backward_time_without_mutation_and_accepts_equal_time(
    tmp_path: Path,
) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, run_directory, state = _init(tmp_path, invocation=invocation)
    state = _complete_a_b_checkpoint(tmp_path, workspace, state)
    current = _projection_time(state)
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.release_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            now=current - timedelta(seconds=1),
        )
    assert rejected.value.code == "invalid_time"
    assert _saved_run_bytes(run_directory) == before

    released = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=current,
    )
    assert released["execution_status"] == "checkpointed"
    assert released["updated_at_utc"] == state["updated_at_utc"]


def test_terminal_release_rejects_backward_time_without_mutation_and_accepts_equal_time(
    tmp_path: Path,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    worktree = tmp_path / "terminal-worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    state = _transition(workspace, state, _event("lane-1", "a_running", "a_ambiguous"))
    current = _projection_time(state)
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.release_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            terminal=True,
            now=current - timedelta(seconds=1),
        )
    assert rejected.value.code == "invalid_time"
    assert _saved_run_bytes(run_directory) == before

    released = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        terminal=True,
        now=current,
    )
    assert released["execution_status"] == "terminal"
    assert released["updated_at_utc"] == state["updated_at_utc"]


def test_checkpoint_release_rejects_expiry_plus_one_without_mutation_and_accepts_expiry(
    tmp_path: Path,
) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, run_directory, state = _init(tmp_path, invocation=invocation)
    state = _complete_a_b_checkpoint(tmp_path, workspace, state)
    expiry = issue_wave._timestamp_datetime(state["reservation"]["lease"]["expires_at_utc"])
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.release_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            now=expiry + timedelta(seconds=1),
        )
    assert rejected.value.code == "recovery_proof_required"
    assert _saved_run_bytes(run_directory) == before

    released = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=expiry,
    )
    assert released["execution_status"] == "checkpointed"
    assert released["updated_at_utc"] == state["reservation"]["lease"]["expires_at_utc"]


def test_terminal_release_rejects_expiry_plus_one_without_mutation_and_accepts_expiry(
    tmp_path: Path,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    worktree = tmp_path / "terminal-expiry-worktree"
    worktree.mkdir()
    state = _transition(
        workspace,
        state,
        _event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
    )
    state = _transition(workspace, state, _event("lane-1", "a_running", "a_ambiguous"))
    expiry = issue_wave._timestamp_datetime(state["reservation"]["lease"]["expires_at_utc"])
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.release_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            terminal=True,
            now=expiry + timedelta(seconds=1),
        )
    assert rejected.value.code == "recovery_proof_required"
    assert _saved_run_bytes(run_directory) == before

    released = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        terminal=True,
        now=expiry,
    )
    assert released["execution_status"] == "terminal"
    assert released["updated_at_utc"] == state["reservation"]["lease"]["expires_at_utc"]


def test_segment_authorization_rejects_backward_time_without_mutation_and_accepts_equal_time(
    tmp_path: Path,
) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, run_directory, state = _init(tmp_path, invocation=invocation)
    state = _complete_a_b_checkpoint(tmp_path, workspace, state)
    state = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=_projection_time(state),
    )
    resume = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (C-C; run={RUN_ID})")
    current = _projection_time(state)
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.authorize_segment(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            invocation_value=resume,
            revalidation_proof=_stable_revalidation_proof(state),
            now=current - timedelta(seconds=1),
        )
    assert rejected.value.code == "invalid_time"
    assert _saved_run_bytes(run_directory) == before

    authorized = issue_wave.authorize_segment(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        invocation_value=resume,
        revalidation_proof=_stable_revalidation_proof(state),
        now=current,
    )
    assert authorized["execution_status"] == "active"
    assert authorized["updated_at_utc"] == state["updated_at_utc"]


def test_expired_recovery_rejects_backward_time_without_mutation(
    tmp_path: Path,
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    proof = {
        "termination_method": "mechanically_verified",
        "former_task_stopped": True,
        "all_agents_stopped": True,
        "preserved_state_stable": True,
        "no_active_operations": True,
    }
    current = _projection_time(state)
    before = _saved_run_bytes(run_directory)

    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.recover_expired_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            proof_value=proof,
            now=current - timedelta(seconds=1),
        )
    assert rejected.value.code == "invalid_time"
    assert _saved_run_bytes(run_directory) == before

    with pytest.raises(issue_wave.IssueWaveError) as not_expired:
        issue_wave.recover_expired_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            proof_value=proof,
            now=current,
        )
    assert not_expired.value.code == "recovery_proof_required"
    assert _saved_run_bytes(run_directory) == before


def test_checkpoint_release_and_exact_next_segment_authorization(tmp_path: Path) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, _, state = _init(tmp_path, invocation=invocation)
    state = _complete_a_b_checkpoint(tmp_path, workspace, state)
    state = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=FIXED_NOW + timedelta(seconds=20),
    )
    assert state["execution_status"] == "checkpointed"
    assert state["next_resumable_role"] == "C"
    assert state["reservation"]["repositories"] == []
    assert (tmp_path / "checkpoint-worktree").exists()
    checkpoint_output = issue_wave.inspect_projection(state, recovered_projection=False)
    assert checkpoint_output["lanes"][0]["manual_next_role_prompt"].startswith(
        "Use $mythic-edge-workflow as Codex C"
    )
    assert checkpoint_output["lanes"][0]["next_segment_command"] == (
        f"$mythic-edge-issue-wave Dispatch (C-F; run={RUN_ID})"
    )

    resume = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (C-E; run={RUN_ID})")
    resumed = issue_wave.authorize_segment(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        invocation_value=resume,
        revalidation_proof=_stable_revalidation_proof(state),
        now=FIXED_NOW + timedelta(seconds=21),
    )
    assert resumed["execution_status"] == "active"
    assert resumed["current_segment"] == {"start_role": "C", "end_role": "E", "explicit": True}
    assert resumed["segment_history"][-1]["authorized_revision"] == resumed["revision"]
    assert resumed["segment_history"][-1]["revalidation_proof_sha256"] == hashlib.sha256(
        issue_wave._canonical_json(_stable_revalidation_proof(state))
    ).hexdigest()


def test_misaligned_resume_and_manual_drift_never_authorize(tmp_path: Path) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, _, state = _init(tmp_path, invocation=invocation)
    state = _complete_a_b_checkpoint(tmp_path, workspace, state)
    state = issue_wave.release_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=FIXED_NOW + timedelta(seconds=20),
    )
    bad = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (E-E; run={RUN_ID})")
    with pytest.raises(issue_wave.IssueWaveError) as misaligned:
        issue_wave.authorize_segment(
            workspace, RUN_ID, expected_revision=state["revision"], invocation_value=bad,
            revalidation_proof=_stable_revalidation_proof(state), now=FIXED_NOW + timedelta(seconds=21)
        )
    assert misaligned.value.code == "misaligned_segment"

    good = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (C-C; run={RUN_ID})")
    drift_proof = _stable_revalidation_proof(state)
    drift_proof["repository_heads_stable"] = False
    with pytest.raises(issue_wave.IssueWaveError) as drift:
        issue_wave.authorize_segment(
            workspace, RUN_ID, expected_revision=state["revision"], invocation_value=good,
            revalidation_proof=drift_proof, now=FIXED_NOW + timedelta(seconds=21)
        )
    assert drift.value.code == "manual_drift_detected"
    _, unchanged, _ = issue_wave.load_run(workspace, RUN_ID)
    assert unchanged["revision"] == state["revision"]


def test_lease_renewal_and_unknown_outcome_recovery(tmp_path: Path) -> None:
    workspace, _, state = _init(tmp_path)
    assert state["reservation"]["lease"]["expires_at_utc"] == "20260813T120500Z"
    state = issue_wave.renew_lease(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        now=FIXED_NOW + timedelta(seconds=60),
    )
    assert state["reservation"]["lease"]["expires_at_utc"] == "20260813T120600Z"
    with pytest.raises(issue_wave.IssueWaveError) as overdue:
        issue_wave.renew_lease(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            now=FIXED_NOW + timedelta(seconds=121),
        )
    assert overdue.value.code == "lease_renewal_overdue"

    worktree = tmp_path / "in-flight-worktree"
    worktree.mkdir()
    state = issue_wave.transition_run(
        workspace,
        RUN_ID,
        expected_revision=state["revision"],
        request_value=_event(
            "lane-1",
            "selected",
            "a_running",
            updates={"branch": "issue/101", "worktree_location": str(worktree)},
        ),
        now=FIXED_NOW + timedelta(seconds=60),
    )
    proof = {
        "termination_method": "mechanically_verified",
        "former_task_stopped": True,
        "all_agents_stopped": True,
        "preserved_state_stable": True,
        "no_active_operations": True,
    }
    recovered = issue_wave.recover_expired_run(
        workspace, RUN_ID, expected_revision=state["revision"], proof_value=proof,
        now=FIXED_NOW + timedelta(seconds=361)
    )
    assert recovered["execution_status"] == "stopped"
    assert recovered["lanes"][0]["state"] == "unknown_agent_outcome"
    assert recovered["next_resumable_role"] is None
    assert worktree.exists()


@pytest.mark.parametrize(
    ("elapsed", "expected_code"),
    [(60, None), (61, "lease_renewal_overdue"), (300, "lease_renewal_overdue"), (301, "recovery_proof_required")],
)
def test_every_transition_requires_a_current_timely_renewed_lease(
    tmp_path: Path, elapsed: int, expected_code: str | None
) -> None:
    workspace, run_directory, state = _init(tmp_path)
    worktree = tmp_path / f"lease-{elapsed}-worktree"
    worktree.mkdir()
    before = ((run_directory / "run.json").read_bytes(), (run_directory / "events.jsonl").read_bytes())
    request = _event(
        "lane-1",
        "selected",
        "a_running",
        updates={"branch": "issue/101", "worktree_location": str(worktree)},
    )

    if expected_code is None:
        updated = issue_wave.transition_run(
            workspace,
            RUN_ID,
            expected_revision=state["revision"],
            request_value=request,
            now=FIXED_NOW + timedelta(seconds=elapsed),
        )
        assert updated["lanes"][0]["state"] == "a_running"
    else:
        with pytest.raises(issue_wave.IssueWaveError) as rejected:
            issue_wave.transition_run(
                workspace,
                RUN_ID,
                expected_revision=state["revision"],
                request_value=request,
                now=FIXED_NOW + timedelta(seconds=elapsed),
            )
        assert rejected.value.code == expected_code
        assert ((run_directory / "run.json").read_bytes(), (run_directory / "events.jsonl").read_bytes()) == before


@pytest.mark.parametrize("nested_direction", ["second_inside_first", "first_inside_second"])
def test_cross_run_worktree_nesting_is_rejected_without_mutation(
    tmp_path: Path, nested_direction: str
) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    states = []
    run_ids = [RUN_ID, "20260813T120001Z-01020304"]
    for index, repository in enumerate(REPOSITORIES[:2]):
        root = tmp_path / f"checkout-{index}"
        root.mkdir()
        manifest = {
            "schema_version": issue_wave.MANIFEST_SCHEMA,
            "candidates": [
                _candidate(
                    root,
                    repository,
                    101 + index,
                    lane_id=f"lane-{index + 1}",
                    created_at=f"2026080{index + 1}T120000Z",
                )
            ],
        }
        _, state = issue_wave.init_run(
            workspace,
            _dispatch_invocation(),
            manifest,
            target_roots={repository: root},
            run_id=run_ids[index],
            now=FIXED_NOW,
        )
        states.append(state)

    outer = tmp_path / "shared-worktrees"
    inner = outer / "nested"
    inner.mkdir(parents=True)
    first_path, second_path = (outer, inner) if nested_direction == "second_inside_first" else (inner, outer)
    states[0] = issue_wave.transition_run(
        workspace,
        run_ids[0],
        expected_revision=states[0]["revision"],
        request_value=_event(
            "lane-1", "selected", "a_running",
            updates={"branch": "issue/101", "worktree_location": str(first_path)},
        ),
        now=FIXED_NOW + timedelta(seconds=1),
    )
    second_directory = workspace / ".codex" / "role-pool-runs" / run_ids[1]
    before = ((second_directory / "run.json").read_bytes(), (second_directory / "events.jsonl").read_bytes())
    with pytest.raises(issue_wave.IssueWaveError) as rejected:
        issue_wave.transition_run(
            workspace,
            run_ids[1],
            expected_revision=states[1]["revision"],
            request_value=_event(
                "lane-2", "selected", "a_running",
                updates={"branch": "issue/102", "worktree_location": str(second_path)},
            ),
            now=FIXED_NOW + timedelta(seconds=2),
        )
    assert rejected.value.code == "unsafe_or_conflicting_scope"
    assert ((second_directory / "run.json").read_bytes(), (second_directory / "events.jsonl").read_bytes()) == before


def test_resume_proof_rejects_missing_lane_changed_head_and_changed_artifact(tmp_path: Path) -> None:
    invocation = issue_wave.parse_invocation("$mythic-edge-issue-wave Dispatch (A-B)")
    workspace, _, state = _init(tmp_path, invocation=invocation)
    state = _complete_a_b_checkpoint(tmp_path, workspace, state)
    state = issue_wave.release_run(
        workspace, RUN_ID, expected_revision=state["revision"], now=FIXED_NOW + timedelta(seconds=20)
    )
    resume = issue_wave.parse_invocation(f"$mythic-edge-issue-wave Dispatch (C-C; run={RUN_ID})")
    proof = _stable_revalidation_proof(state)
    mutations = [
        lambda value: value["lanes"].clear(),
        lambda value: value["lanes"][0]["repository_head"].update(observed="b" * 40),
        lambda value: value["lanes"][0]["artifacts"][0].update(observed_sha256="b" * 64),
    ]
    for mutate in mutations:
        candidate = deepcopy(proof)
        mutate(candidate)
        with pytest.raises(issue_wave.IssueWaveError):
            issue_wave.authorize_segment(
                workspace,
                RUN_ID,
                expected_revision=state["revision"],
                invocation_value=resume,
                revalidation_proof=candidate,
                now=FIXED_NOW + timedelta(seconds=21),
            )


@pytest.mark.parametrize("status", ["active", "stopped", "terminal"])
def test_inspect_withholds_resume_output_unless_checkpoint_is_safe(tmp_path: Path, status: str) -> None:
    workspace, _, state = _init(tmp_path)
    if status != "active":
        state["execution_status"] = status
    projection = issue_wave.inspect_projection(state, recovered_projection=False)
    assert all(lane["manual_next_role_prompt"] is None for lane in projection["lanes"])
    assert all(lane["next_segment_command"] is None for lane in projection["lanes"])


def test_expired_lease_blocks_admission_without_mutation(tmp_path: Path) -> None:
    workspace, run_directory, _ = _init(tmp_path)
    before = ((run_directory / "run.json").read_bytes(), (run_directory / "events.jsonl").read_bytes())
    second_root = tmp_path / "second-repository"
    second_root.mkdir()
    manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [_candidate(second_root, REPOSITORIES[1], 202, lane_id="lane-2", created_at="20260802T120000Z")],
    }
    with pytest.raises(issue_wave.IssueWaveError) as blocked:
        issue_wave.init_run(
            workspace, _dispatch_invocation(), manifest, target_roots={REPOSITORIES[1]: second_root},
            run_id="20260813T120600Z-01020304", now=FIXED_NOW + timedelta(seconds=301)
        )
    assert blocked.value.code == "recovery_proof_required"
    assert ((run_directory / "run.json").read_bytes(), (run_directory / "events.jsonl").read_bytes()) == before


def test_two_simultaneous_disjoint_waves_succeed_and_third_is_rejected(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    barrier = threading.Barrier(2)

    def attempt(index: int) -> str:
        candidates = []
        roots = {}
        for lane_offset in range(3):
            repository_index = index * 3 + lane_offset
            repository = issue_wave.DEFAULT_ALLOWLIST[repository_index]
            root = tmp_path / f"wave-{index}-repo-{lane_offset}"
            root.mkdir()
            roots[repository] = root
            candidates.append(
                _candidate(
                    root,
                    repository,
                    300 + repository_index,
                    lane_id=f"wave-{index}-lane-{lane_offset}",
                    created_at=f"2026080{repository_index + 1}T120000Z",
                )
            )
        manifest = {
            "schema_version": issue_wave.MANIFEST_SCHEMA,
            "candidates": candidates,
        }
        barrier.wait()
        issue_wave.init_run(
            workspace, _dispatch_invocation(), manifest, target_roots=roots,
            run_id=f"20260813T12000{index}Z-0102030{index}", now=FIXED_NOW
        )
        return "success"

    with ThreadPoolExecutor(max_workers=2) as executor:
        assert list(executor.map(attempt, (0, 1))) == ["success", "success"]

    root = tmp_path / "repo-7"
    root.mkdir()
    manifest = {
        "schema_version": issue_wave.MANIFEST_SCHEMA,
        "candidates": [
            _candidate(
                root,
                issue_wave.DEFAULT_ALLOWLIST[6],
                307,
                lane_id="lane-7",
                created_at="20260807T120000Z",
            )
        ],
    }
    with pytest.raises(issue_wave.IssueWaveError) as third:
        issue_wave.init_run(
            workspace,
            _dispatch_invocation(),
            manifest,
            target_roots={issue_wave.DEFAULT_ALLOWLIST[6]: root},
            run_id="20260813T120003Z-01020303", now=FIXED_NOW + timedelta(seconds=3)
        )
    assert third.value.code == "active_wave_limit"


def test_repo_owned_skill_metadata_disables_implicit_invocation() -> None:
    metadata = (
        REPO_ROOT
        / "docs"
        / "codex_skills"
        / "mythic-edge-issue-wave"
        / "agents"
        / "openai.yaml"
    ).read_text(encoding="utf-8")
    assert 'display_name: "Mythic Edge Role Pool"' in metadata
    assert 'default_prompt: "Use $mythic-edge-issue-wave' in metadata
    assert "allow_implicit_invocation: false" in metadata


def test_helper_imports_only_deterministic_local_standard_library_modules() -> None:
    tree = ast.parse(HELPER_PATH.read_text(encoding="utf-8"))
    imported = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    assert imported <= {
        "__future__",
        "argparse",
        "contextlib",
        "copy",
        "datetime",
        "hashlib",
        "json",
        "os",
        "pathlib",
        "re",
        "secrets",
        "sys",
        "time",
        "typing",
        "uuid",
    }
    source = HELPER_PATH.read_text(encoding="utf-8")
    for forbidden in ("subprocess", "socket", "urllib", "requests", "github", "git "):
        assert forbidden not in source.casefold()


def test_legacy_role_pool_tracked_tree_matches_contract_baseline() -> None:
    tree = _git("rev-parse", "HEAD:docs/codex_skills/mythic-edge-role-pool", cwd=REPO_ROOT)
    files = _git(
        "ls-tree",
        "-r",
        "--name-only",
        "HEAD",
        "--",
        "docs/codex_skills/mythic-edge-role-pool",
        cwd=REPO_ROOT,
    ).splitlines()
    assert tree == "950768b80b760a0e0dfe3040df023de20eadaf81"
    assert len(files) == 38
    assert not any(
        path.startswith("docs/codex_skills/mythic-edge-role-pool/")
        for path in _git("diff", "--name-only", cwd=REPO_ROOT).splitlines()
    )
