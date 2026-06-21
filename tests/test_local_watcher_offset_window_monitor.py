from __future__ import annotations

import json

import pytest

from mythic_edge_parser.app import local_watcher_offset_window_monitor as monitor


def _synthetic_selection() -> dict:
    return monitor.describe_source_selection(
        source_label="synthetic_player_log",
        source_class="synthetic_player_log",
    )


def _synthetic_metadata(tmp_path, *, size: int = 4, generation: str = "generation_a") -> dict:
    path = tmp_path / f"{generation}.log"
    path.write_text("x" * size, encoding="utf-8")
    return monitor.capture_synthetic_file_metadata(
        source_label="synthetic_player_log",
        path=path,
        source_generation=generation,
    )


def test_source_selection_is_symbolic_and_false_flagged() -> None:
    source = _synthetic_selection()

    assert source["object"] == monitor.LOCAL_WATCHER_SOURCE_OBJECT
    assert source["selection_status"] == "source_selection_ready"
    assert source["contents_read"] is False
    assert source["raw_path_included"] is False
    assert source["raw_hash_included"] is False
    assert monitor.validate_source_selection(source) == []


def test_non_synthetic_source_without_approval_is_blocked_before_metadata_collection() -> None:
    source = monitor.describe_source_selection(
        source_label="operator_source",
        source_class="player_log",
        privacy_class="private_local",
        selection_mode="operator_selected_local",
    )
    window = monitor.start_offset_window(
        source_selection=source,
        start_metadata=None,
        window_id="private_window",
    )

    assert source["selection_mode"] == "blocked_missing_approval"
    assert source["selection_status"] == "window_blocked_missing_approval"
    assert source["contents_read"] is False
    assert window["window_mode"] == "blocked"
    assert window["window_status"] == "window_blocked_missing_approval"
    assert window["synthetic_start_offset"] is None
    assert window["synthetic_start_size_bytes"] is None
    assert monitor.validate_source_selection(source) == []
    assert monitor.validate_offset_window(window) == []


def test_path_like_source_label_is_rejected_without_echoing_value() -> None:
    forbidden_label = "/" + "Users" + "/example/private/" + "Player" + ".log"

    with pytest.raises(monitor.OffsetWindowMonitorError) as exc_info:
        monitor.describe_source_selection(
            source_label=forbidden_label,
            source_class="player_log",
        )

    assert exc_info.value.status == "blocked_forbidden_artifact"
    assert forbidden_label not in exc_info.value.reason


def test_capture_synthetic_file_metadata_omits_path_and_contents(tmp_path) -> None:
    source_text = "synthetic public line"
    source_path = tmp_path / "synthetic.log"
    source_path.write_text(source_text, encoding="utf-8")

    metadata = monitor.capture_synthetic_file_metadata(
        source_label="synthetic_player_log",
        path=source_path,
        source_generation="generation_a",
    )
    encoded = json.dumps(metadata, sort_keys=True)

    assert metadata["exists"] is True
    assert metadata["size_bytes"] == len(source_text)
    assert metadata["path_included"] is False
    assert metadata["contents_read"] is False
    assert str(source_path) not in encoded
    assert source_text not in encoded


def test_transition_classification_for_metadata_only_source_changes() -> None:
    base = {
        "exists": True,
        "source_generation": "generation_a",
        "synthetic_file_token": "token_a",
        "size_bytes": 10,
    }

    assert monitor.classify_source_transition(base, {**base, "size_bytes": 12}) == {
        "source_transition_status": "file_appended",
        "source_generation_status": "same_source_generation",
        "error_status": "no_error",
    }
    assert monitor.classify_source_transition(base, {**base, "size_bytes": 8}) == {
        "source_transition_status": "file_size_decreased",
        "source_generation_status": "truncated_generation",
        "error_status": "no_error",
    }
    assert monitor.classify_source_transition(
        base,
        {**base, "synthetic_file_token": "token_b"},
    )["source_transition_status"] == "file_recreated"
    assert monitor.classify_source_transition(
        base,
        {**base, "source_generation": "generation_b"},
    )["source_generation_status"] == "rotated_generation"
    assert monitor.classify_source_transition(base, {**base, "archived": True})[
        "source_generation_status"
    ] == "archived_generation"
    assert monitor.classify_source_transition(base, None)["error_status"] == "source_disappeared"


def test_start_and_finish_windows_for_read_from_start_and_tail_from_now(tmp_path) -> None:
    source = _synthetic_selection()
    metadata = _synthetic_metadata(tmp_path, size=4)
    appended = _synthetic_metadata(tmp_path, size=6)

    read_window = monitor.start_offset_window(
        source_selection=source,
        start_metadata=metadata,
        window_id="read_window",
        window_mode="read_from_start",
    )
    finished_read = monitor.finish_offset_window(window=read_window, end_metadata=appended)

    assert read_window["synthetic_start_offset"] == 0
    assert finished_read["synthetic_end_offset"] == 6
    assert finished_read["offset_range_status"] == "offset_range_valid"
    assert finished_read["review_required"] is False
    assert monitor.validate_offset_window(finished_read) == []

    tail_window = monitor.start_offset_window(
        source_selection=source,
        start_metadata=appended,
        window_id="tail_window",
        window_mode="tail_from_now",
    )
    finished_tail = monitor.finish_offset_window(window=tail_window, end_metadata=appended)

    assert tail_window["synthetic_start_offset"] == 6
    assert finished_tail["offset_range_status"] == "offset_range_empty"
    assert finished_tail["review_required"] is False
    assert monitor.validate_offset_window(finished_tail) == []


def test_cross_generation_and_reversed_offsets_require_review(tmp_path) -> None:
    source = _synthetic_selection()
    start_metadata = _synthetic_metadata(tmp_path, size=10)
    smaller_metadata = _synthetic_metadata(tmp_path, size=5)
    rotated_metadata = _synthetic_metadata(tmp_path, size=12, generation="generation_b")
    window = monitor.start_offset_window(
        source_selection=source,
        start_metadata=start_metadata,
        window_id="review_window",
        window_mode="tail_from_now",
    )

    reversed_window = monitor.finish_offset_window(
        window=window,
        end_metadata=smaller_metadata,
        transition={
            "source_transition_status": "file_unchanged",
            "source_generation_status": "same_source_generation",
            "error_status": "no_error",
        },
    )
    crossed_window = monitor.finish_offset_window(window=window, end_metadata=rotated_metadata)

    assert reversed_window["offset_range_status"] == "offset_range_reversed"
    assert reversed_window["window_status"] == "window_manual_review_required"
    assert reversed_window["review_required"] is True
    assert crossed_window["offset_range_status"] == "offset_range_crosses_generation"
    assert crossed_window["window_status"] == "window_manual_review_required"
    assert crossed_window["review_required"] is True


def test_update_buffer_pressure_statuses_are_deterministic() -> None:
    assert monitor.summarize_update_buffer(
        buffer_capacity=10,
        queued_update_count=2,
    )["backpressure_status"] == "buffer_ok"
    assert monitor.summarize_update_buffer(
        buffer_capacity=10,
        queued_update_count=8,
    )["backpressure_status"] == "buffer_near_limit"
    assert monitor.summarize_update_buffer(
        buffer_capacity=10,
        queued_update_count=11,
    )["backpressure_status"] == "buffer_over_limit_degraded"
    assert monitor.summarize_update_buffer(
        buffer_capacity=10,
        queued_update_count=1,
        dropped_update_count=1,
    )["backpressure_status"] == "buffer_dropped_updates"
    assert monitor.summarize_update_buffer(
        buffer_capacity=0,
        queued_update_count=0,
    )["backpressure_status"] == "buffer_unknown"


def test_report_validator_rejects_true_readiness_flags_and_content_claims(tmp_path) -> None:
    source = _synthetic_selection()
    metadata = _synthetic_metadata(tmp_path)
    window = monitor.start_offset_window(
        source_selection=source,
        start_metadata=metadata,
        window_id="readiness_window",
    )
    report = monitor.build_offset_window_monitor_report(
        source_selection=source,
        windows=[window],
    )

    assert monitor.validate_offset_window_monitor_report(report) == []

    report["parser_behavior_ready"] = True
    report["windows"][0]["contents_read"] = True

    errors = monitor.validate_offset_window_monitor_report(report)

    assert "report:parser_behavior_ready_must_remain_false" in errors
    assert "report:windows[0]:window:contents_read_must_remain_false" in errors


def test_validator_rejects_embedded_private_markers_without_echoing_values(tmp_path) -> None:
    source = _synthetic_selection()
    metadata = _synthetic_metadata(tmp_path)
    window = monitor.start_offset_window(
        source_selection=source,
        start_metadata=metadata,
        window_id="privacy_window",
    )
    report = monitor.build_offset_window_monitor_report(
        source_selection=source,
        windows=[window],
    )
    unix_path = "/" + "Users" + "/example/private/session"
    file_uri = "file://" + "/" + "Users" + "/example/private/session"
    report["source_selection"]["approval_issue"] = f"review {unix_path}"
    report["windows"][0]["source_generation"] = f"review {file_uri}"

    errors = monitor.validate_offset_window_monitor_report(report)
    encoded_errors = json.dumps(errors, sort_keys=True)

    assert "privacy:absolute_path:report.source_selection.approval_issue" in errors
    assert "privacy:absolute_path:report.windows[0].source_generation" in errors
    assert unix_path not in encoded_errors
    assert file_uri not in encoded_errors
