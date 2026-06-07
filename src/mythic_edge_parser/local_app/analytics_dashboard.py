from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from .paths import LocalAppPaths, display_app_path
from .setup_status import build_analytics_database_status

DASHBOARD_MODULES_OBJECT = "mythic_edge_local_app_analytics_dashboard_modules"
DASHBOARD_MODULES_SCHEMA_VERSION = "analytics_dynamic_decision_support_dashboard.v1"
DASHBOARD_CONTRACT = "docs/contracts/analytics_dynamic_decision_support_dashboard.md"

MODULE_IDS = (
    "play_draw_win_rate",
    "game1_postboard",
    "mulligan_opening_hand_outcomes",
)


def build_analytics_dashboard_modules(paths: LocalAppPaths) -> dict[str, object]:
    database_status = build_analytics_database_status(paths)
    database = _dashboard_database(database_status)
    status = str(database_status.get("status", "error"))
    schema_status = str(database["schema_status"])

    if status in {"missing", "unavailable"}:
        return _payload(
            status=status,
            database=database,
            modules=_empty_modules(status=status, tone="blocked" if status == "missing" else "degraded"),
            warnings=[],
            errors=[],
        )
    if status == "error":
        return _payload(
            status="error",
            database=database,
            modules=_empty_modules(status="error", tone="blocked", errors=_stable_errors(database_status)),
            warnings=[],
            errors=_stable_errors(database_status),
        )
    if schema_status != "schema_current":
        return _payload(
            status="degraded",
            database=database,
            modules=_empty_modules(
                status="degraded",
                tone="degraded",
                warnings=["analytics_schema_not_current"],
            ),
            warnings=["analytics_schema_not_current"],
            errors=[],
        )

    database_path = paths.analytics_database
    if database_path is None:
        return _payload(
            status="unavailable",
            database={**database, "status": "unavailable"},
            modules=_empty_modules(status="unavailable", tone="degraded", errors=["app_data_root_unavailable"]),
            warnings=[],
            errors=["app_data_root_unavailable"],
        )

    try:
        play_draw_rows = _query_rows(database_path, _PLAY_DRAW_DASHBOARD_QUERY)
        game1_postboard_rows = _query_rows(database_path, _GAME1_POSTBOARD_DASHBOARD_QUERY)
        mulligan_opening_hand_rows = _query_rows(database_path, _MULLIGAN_OPENING_HAND_DASHBOARD_QUERY)
    except (OSError, sqlite3.DatabaseError):
        return _payload(
            status="error",
            database={**database, "status": "error"},
            modules=_empty_modules(status="error", tone="blocked", errors=["analytics_dashboard_query_failed"]),
            warnings=[],
            errors=["analytics_dashboard_query_failed"],
        )

    modules = [
        _play_draw_module(play_draw_rows),
        _game1_postboard_module(game1_postboard_rows),
        _mulligan_opening_hand_module(mulligan_opening_hand_rows),
    ]
    if all(not module["rows"] for module in modules):
        top_status = "empty"
    elif any(module["status"] == "error" for module in modules):
        top_status = "error"
    elif any(module["status"] == "degraded" for module in modules):
        top_status = "degraded"
    else:
        top_status = "ok"

    warnings = sorted({warning for module in modules for warning in _string_list(module.get("warnings"))})
    errors = sorted({error for module in modules for error in _string_list(module.get("errors"))})
    return _payload(status=top_status, database=database, modules=modules, warnings=warnings, errors=errors)


def _query_rows(database_path: Path, query: str) -> list[sqlite3.Row]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return list(connection.execute(query).fetchall())
    finally:
        connection.close()


def _payload(
    *,
    status: str,
    database: dict[str, object],
    modules: list[dict[str, object]],
    warnings: list[str],
    errors: list[str],
) -> dict[str, object]:
    return {
        "object": DASHBOARD_MODULES_OBJECT,
        "schema_version": DASHBOARD_MODULES_SCHEMA_VERSION,
        "status": status,
        "database": database,
        "modules": modules,
        "custom_explorer": _custom_explorer(),
        "warnings": warnings,
        "errors": errors,
    }


def _dashboard_database(database_status: dict[str, object]) -> dict[str, object]:
    database = database_status.get("database")
    if not isinstance(database, dict):
        return {
            "display_path": display_app_path("db", "mythic_edge.sqlite3"),
            "exists": False,
            "schema_status": "unavailable",
            "status": "error",
        }
    return {
        "display_path": str(database.get("display_path", display_app_path("db", "mythic_edge.sqlite3"))),
        "exists": bool(database.get("exists", False)),
        "schema_status": str(database.get("schema_status", "unknown")),
        "status": str(database_status.get("status", "error")),
    }


def _empty_modules(
    *,
    status: str,
    tone: str,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> list[dict[str, object]]:
    return [
        _module(
            module_id="play_draw_win_rate",
            title="Win Rate By Play/Draw",
            decision_question="Am I performing differently on the play versus on the draw?",
            default_view="bar",
            metric=_module_metric(
                metric_id="win_rate",
                label="Win rate",
                value=None,
                value_kind="null",
                unit="percent",
                display="No known results",
                calculation_note="Calculated over known win/loss game rows only.",
            ),
            dimensions=[
                _dimension(
                    "play_draw",
                    "Play/draw",
                    source="v_play_draw_splits",
                    value_source="analytics_derived",
                    allowed_values=["play", "draw", "unknown"],
                )
            ],
            rows=[],
            summary=_summary(row_count=0, known_result_count=0, wins=0, losses=0, unknown_or_degraded_count=0),
            status=status,
            tone=tone,
            warnings=warnings or [],
            errors=errors or [],
            data_quality=_data_quality(status=status, sample_size_status="empty"),
            source_metadata=_source_metadata(
                ["v_play_draw_splits", "v_sample_size_warnings"],
                source_type="fixed_sql_view",
            ),
        ),
        _module(
            module_id="game1_postboard",
            title="Game 1 / Postboard",
            decision_question="Are my game 1 and postboard games showing different observed results?",
            default_view="bar",
            metric=_module_metric(
                metric_id="win_rate",
                label="Win rate",
                value=None,
                value_kind="null",
                unit="percent",
                display="No known results",
                calculation_note="Calculated over known win/loss game rows only.",
            ),
            dimensions=[
                _dimension(
                    "game1_postboard",
                    "Game 1/postboard",
                    source="v_game1_vs_postboard",
                    value_source="analytics_derived",
                    allowed_values=["game1", "postboard", "unknown"],
                )
            ],
            rows=[],
            summary=_summary(row_count=0, known_result_count=0, wins=0, losses=0, unknown_or_degraded_count=0),
            status=status,
            tone=tone,
            warnings=warnings or [],
            errors=errors or [],
            data_quality=_data_quality(status=status, sample_size_status="empty"),
            source_metadata=_source_metadata(["v_game1_vs_postboard"], source_type="fixed_backend_aggregation"),
        ),
        _module(
            module_id="mulligan_opening_hand_outcomes",
            title="Mulligan / Opening Hand Outcomes",
            decision_question="Are my keep and mulligan patterns associated with observed outcomes?",
            default_view="table",
            metric=_module_metric(
                metric_id="win_rate",
                label="Win rate",
                value=None,
                value_kind="null",
                unit="percent",
                display="No known results",
                calculation_note="Calculated over known win/loss game rows only.",
            ),
            dimensions=[
                _dimension(
                    "opening_hand_size",
                    "Opening hand size",
                    source="opening_hands",
                    value_source="parser_normalized",
                ),
                _dimension(
                    "mulligan_bucket",
                    "Mulligan bucket",
                    source="mulligan_events",
                    value_source="parser_normalized",
                ),
            ],
            rows=[],
            summary=_summary(row_count=0, known_result_count=0, wins=0, losses=0, unknown_or_degraded_count=0),
            status=status,
            tone=tone,
            warnings=warnings or [],
            errors=errors or [],
            data_quality=_data_quality(status=status, sample_size_status="empty"),
            source_metadata=_source_metadata(
                ["opening_hands", "mulligan_events", "game_results"],
                source_type="fixed_backend_aggregation",
            ),
        ),
    ]


def _play_draw_module(rows: list[sqlite3.Row]) -> dict[str, object]:
    module_rows = [_play_draw_module_row(row) for row in rows]
    return _result_module(
        module_id="play_draw_win_rate",
        title="Win Rate By Play/Draw",
        decision_question="Am I performing differently on the play versus on the draw?",
        default_view="bar",
        dimensions=[
            _dimension(
                "play_draw",
                "Play/draw",
                source="v_play_draw_splits",
                value_source="analytics_derived",
                allowed_values=["play", "draw", "unknown"],
            )
        ],
        rows=module_rows,
        source_metadata=_source_metadata(
            ["v_play_draw_splits", "v_sample_size_warnings"],
            source_type="fixed_sql_view",
        ),
    )


def _game1_postboard_module(rows: list[sqlite3.Row]) -> dict[str, object]:
    module_rows = [
        _result_group_module_row(row, dimension_id="game1_postboard", label_prefix="Game group") for row in rows
    ]
    return _result_module(
        module_id="game1_postboard",
        title="Game 1 / Postboard",
        decision_question="Are my game 1 and postboard games showing different observed results?",
        default_view="bar",
        dimensions=[
            _dimension(
                "game1_postboard",
                "Game 1/postboard",
                source="v_game1_vs_postboard",
                value_source="analytics_derived",
                allowed_values=["game1", "postboard", "unknown"],
            )
        ],
        rows=module_rows,
        source_metadata=_source_metadata(["v_game1_vs_postboard"], source_type="fixed_backend_aggregation"),
    )


def _mulligan_opening_hand_module(rows: list[sqlite3.Row]) -> dict[str, object]:
    module_rows = [_mulligan_opening_hand_row(row) for row in rows]
    return _result_module(
        module_id="mulligan_opening_hand_outcomes",
        title="Mulligan / Opening Hand Outcomes",
        decision_question="Are my keep and mulligan patterns associated with observed outcomes?",
        default_view="table",
        dimensions=[
            _dimension(
                "opening_hand_size",
                "Opening hand size",
                source="opening_hands",
                value_source="parser_normalized",
            ),
            _dimension(
                "mulligan_bucket",
                "Mulligan bucket",
                source="mulligan_events",
                value_source="parser_normalized",
            ),
        ],
        rows=module_rows,
        source_metadata=_source_metadata(
            ["opening_hands", "mulligan_events", "game_results"],
            source_type="fixed_backend_aggregation",
        ),
    )


def _result_module(
    *,
    module_id: str,
    title: str,
    decision_question: str,
    default_view: str,
    dimensions: list[dict[str, object]],
    rows: list[dict[str, object]],
    source_metadata: dict[str, object],
) -> dict[str, object]:
    summary = _result_summary(rows)
    sample_size_status = _sample_size_status(summary["known_result_count"], rows)
    status = "ok" if rows else "empty"
    tone = "ok"
    if not rows:
        tone = "empty"
    elif sample_size_status == "small_sample" or summary["unknown_or_degraded_count"] > 0:
        tone = "limited"
    metric = _module_metric(
        metric_id="win_rate",
        label="Win rate",
        value=summary["win_rate_percent"],
        value_kind="percentage" if summary["win_rate_percent"] is not None else "null",
        unit="percent",
        display=_percent_display(summary["win_rate_percent"]),
        calculation_note="Calculated over known win/loss game rows only.",
    )
    warnings = sorted({warning for row in rows for warning in _string_list(row.get("warnings"))})
    return _module(
        module_id=module_id,
        title=title,
        decision_question=decision_question,
        default_view=default_view,
        metric=metric,
        dimensions=dimensions,
        rows=rows,
        summary=summary,
        status=status,
        tone=tone,
        warnings=warnings,
        errors=[],
        data_quality=_data_quality(
            status=status,
            sample_size_status=sample_size_status,
            known_result_count=summary["known_result_count"],
            unknown_or_degraded_count=summary["unknown_or_degraded_count"],
            confidence="medium" if tone == "limited" else "high",
            finality="analytics_projection",
            notes=_quality_notes(sample_size_status, summary["unknown_or_degraded_count"]),
        ),
        source_metadata=source_metadata,
    )


def _module(
    *,
    module_id: str,
    title: str,
    decision_question: str,
    status: str,
    tone: str,
    default_view: str,
    metric: dict[str, object],
    dimensions: list[dict[str, object]],
    rows: list[dict[str, object]],
    summary: dict[str, object],
    warnings: list[str],
    errors: list[str],
    data_quality: dict[str, object],
    source_metadata: dict[str, object],
) -> dict[str, object]:
    return {
        "module_id": module_id,
        "title": title,
        "decision_question": decision_question,
        "status": status,
        "tone": tone,
        "default_view": default_view,
        "allowed_views": ["bar", "table"],
        "metric": metric,
        "dimensions": dimensions,
        "rows": rows,
        "summary": summary,
        "warnings": warnings,
        "errors": errors,
        "data_quality": data_quality,
        "source_metadata": source_metadata,
        "schema_version": DASHBOARD_MODULES_SCHEMA_VERSION,
    }


def _play_draw_module_row(row: sqlite3.Row) -> dict[str, object]:
    play_draw = _safe_group_value(row["play_draw"], fallback="unknown")
    return _result_row(
        row_id=f"play_draw:{_safe_id(play_draw)}",
        label=_label(play_draw),
        dimension_values={"play_draw": play_draw},
        game_count=_int_value(row["game_count"]),
        known_result_count=_int_value(row["known_result_count"]),
        wins=_int_value(row["wins"]),
        losses=_int_value(row["losses"]),
        unknown_result_count=_int_value(row["unknown_result_count"]),
        unavailable_result_count=_int_value(row["unavailable_result_count"]),
        degraded_result_count=_int_value(row["degraded_result_count"]),
        win_rate=_optional_ratio(row["win_rate"]),
        sample_size_warning=_safe_warning(row["sample_size_warning"]),
        source_metadata=_source_metadata(
            ["v_play_draw_splits", "v_sample_size_warnings"],
            source_type="fixed_sql_view",
        ),
    )


def _result_group_module_row(row: sqlite3.Row, *, dimension_id: str, label_prefix: str) -> dict[str, object]:
    group = _safe_group_value(row[dimension_id], fallback="unknown")
    return _result_row(
        row_id=f"{dimension_id}:{_safe_id(group)}",
        label=f"{label_prefix}: {_label(group)}",
        dimension_values={dimension_id: group},
        game_count=_int_value(row["game_count"]),
        known_result_count=_int_value(row["known_result_count"]),
        wins=_int_value(row["wins"]),
        losses=_int_value(row["losses"]),
        unknown_result_count=_int_value(row["unknown_result_count"]),
        unavailable_result_count=_int_value(row["unavailable_result_count"]),
        degraded_result_count=_int_value(row["degraded_result_count"]),
        win_rate=_optional_ratio(row["win_rate"]),
        sample_size_warning=_sample_warning_for_count(_int_value(row["known_result_count"])),
        source_metadata=_source_metadata(["v_game1_vs_postboard"], source_type="fixed_backend_aggregation"),
    )


def _mulligan_opening_hand_row(row: sqlite3.Row) -> dict[str, object]:
    opening_hand_size = _safe_group_value(row["opening_hand_size"], fallback="unknown")
    mulligan_bucket = _safe_group_value(row["mulligan_bucket"], fallback="unknown")
    return _result_row(
        row_id=f"mulligan_opening:{_safe_id(opening_hand_size)}:{_safe_id(mulligan_bucket)}",
        label=f"{_opening_hand_label(opening_hand_size)} / {_mulligan_label(mulligan_bucket)}",
        dimension_values={
            "opening_hand_size": opening_hand_size,
            "mulligan_bucket": mulligan_bucket,
        },
        game_count=_int_value(row["game_count"]),
        known_result_count=_int_value(row["known_result_count"]),
        wins=_int_value(row["wins"]),
        losses=_int_value(row["losses"]),
        unknown_result_count=_int_value(row["unknown_result_count"]),
        unavailable_result_count=_int_value(row["unavailable_result_count"]),
        degraded_result_count=_int_value(row["degraded_result_count"]),
        win_rate=_optional_ratio(row["win_rate"]),
        sample_size_warning=_sample_warning_for_count(_int_value(row["known_result_count"])),
        source_metadata=_source_metadata(
            ["opening_hands", "mulligan_events", "game_results"],
            source_type="fixed_backend_aggregation",
        ),
    )


def _result_row(
    *,
    row_id: str,
    label: str,
    dimension_values: dict[str, object],
    game_count: int,
    known_result_count: int,
    wins: int,
    losses: int,
    unknown_result_count: int,
    unavailable_result_count: int,
    degraded_result_count: int,
    win_rate: float | None,
    sample_size_warning: str | None,
    source_metadata: dict[str, object],
) -> dict[str, object]:
    win_rate_percent = _percent_value(win_rate)
    warnings = []
    if sample_size_warning == "small_sample":
        warnings.append("small_sample")
    if unknown_result_count + unavailable_result_count + degraded_result_count > 0:
        warnings.append("unknown_or_degraded_results_present")
    status = "degraded" if degraded_result_count > 0 else "ok"
    tone = "limited" if warnings else "ok"
    return {
        "row_id": row_id,
        "label": label,
        "dimension_values": dimension_values,
        "metrics": [
            _row_metric("game_count", "Games", game_count, "count", "games", f"{game_count} games"),
            _row_metric(
                "known_result_count",
                "Known results",
                known_result_count,
                "count",
                "games",
                f"{known_result_count} known games",
            ),
            _row_metric("wins", "Wins", wins, "count", "games", f"{wins} wins"),
            _row_metric("losses", "Losses", losses, "count", "games", f"{losses} losses"),
            _row_metric(
                "win_rate",
                "Win rate",
                win_rate_percent,
                "percentage" if win_rate_percent is not None else "null",
                "percent",
                _percent_display(win_rate_percent),
            ),
            _row_metric(
                "unknown_or_degraded_count",
                "Unknown or degraded",
                unknown_result_count + unavailable_result_count + degraded_result_count,
                "count",
                "games",
                f"{unknown_result_count + unavailable_result_count + degraded_result_count} games",
            ),
        ],
        "status": status,
        "tone": tone,
        "sample_size": {
            "status": sample_size_warning or _sample_warning_for_count(known_result_count),
            "known_result_count": known_result_count,
            "total_count": game_count,
        },
        "warnings": warnings,
        "source_metadata": source_metadata,
    }


def _module_metric(
    *,
    metric_id: str,
    label: str,
    value: object,
    value_kind: str,
    unit: str,
    display: str,
    calculation_note: str,
) -> dict[str, object]:
    return {
        "metric_id": metric_id,
        "label": label,
        "value": value,
        "value_kind": value_kind,
        "unit": unit,
        "display": display,
        "calculation_note": calculation_note,
        "source": "analytics_derived",
    }


def _row_metric(
    metric_id: str,
    label: str,
    value: object,
    value_kind: str,
    unit: str,
    display: str,
) -> dict[str, object]:
    return {
        "metric_id": metric_id,
        "label": label,
        "value": value,
        "value_kind": value_kind,
        "unit": unit,
        "display": display,
    }


def _dimension(
    dimension_id: str,
    label: str,
    *,
    source: str,
    value_source: str,
    allowed_values: list[str] | None = None,
    annotation_boundary: str | None = None,
) -> dict[str, object]:
    dimension: dict[str, object] = {
        "dimension_id": dimension_id,
        "label": label,
        "source": source,
        "value_source": value_source,
    }
    if allowed_values is not None:
        dimension["allowed_values"] = allowed_values
    if annotation_boundary is not None:
        dimension["annotation_boundary"] = annotation_boundary
    return dimension


def _source_metadata(source_tables_or_views: list[str], *, source_type: str) -> dict[str, object]:
    return {
        "source_tables_or_views": source_tables_or_views,
        "source_contracts": [DASHBOARD_CONTRACT],
        "source_type": source_type,
        "parser_truth_boundary": "Parser/state owns match, game, play/draw, mulligan, and opening-hand facts.",
        "analytics_truth_boundary": "Dashboard modules are fixed read-only projections of local analytics facts.",
    }


def _data_quality(
    *,
    status: str,
    sample_size_status: str,
    known_result_count: int = 0,
    unknown_or_degraded_count: int = 0,
    review_required_count: int = 0,
    confidence: str = "unknown",
    finality: str = "unknown",
    notes: list[str] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "sample_size_status": sample_size_status,
        "known_result_count": known_result_count,
        "unknown_or_degraded_count": unknown_or_degraded_count,
        "review_required_count": review_required_count,
        "confidence": confidence,
        "finality": finality,
        "notes": notes or [],
    }


def _result_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    known_result_count = sum(_metric_value(row, "known_result_count") for row in rows)
    wins = sum(_metric_value(row, "wins") for row in rows)
    losses = sum(_metric_value(row, "losses") for row in rows)
    unknown_or_degraded_count = sum(_metric_value(row, "unknown_or_degraded_count") for row in rows)
    win_rate_percent = None if known_result_count == 0 else round(wins / known_result_count * 100, 1)
    return _summary(
        row_count=len(rows),
        known_result_count=known_result_count,
        wins=wins,
        losses=losses,
        unknown_or_degraded_count=unknown_or_degraded_count,
        win_rate_percent=win_rate_percent,
    )


def _summary(
    *,
    row_count: int,
    known_result_count: int,
    wins: int,
    losses: int,
    unknown_or_degraded_count: int,
    win_rate_percent: float | None = None,
) -> dict[str, object]:
    return {
        "row_count": row_count,
        "known_result_count": known_result_count,
        "wins": wins,
        "losses": losses,
        "unknown_or_degraded_count": unknown_or_degraded_count,
        "win_rate_percent": win_rate_percent,
        "display": (
            f"{wins}-{losses} over {known_result_count} known games"
            if known_result_count
            else "No known win/loss rows"
        ),
    }


def _custom_explorer() -> dict[str, object]:
    return {
        "status": "deferred",
        "builder_ui_enabled": False,
        "query_execution_enabled": False,
        "dimensions": [
            _dimension(
                "date_time_bucket",
                "Date/time bucket",
                source="fixed_future_projection",
                value_source="display_only",
            ),
            _dimension(
                "play_draw",
                "Play/draw",
                source="v_play_draw_splits",
                value_source="analytics_derived",
                allowed_values=["play", "draw", "unknown"],
            ),
            _dimension(
                "game1_postboard",
                "Game 1/postboard",
                source="v_game1_vs_postboard",
                value_source="analytics_derived",
                allowed_values=["game1", "postboard", "unknown"],
            ),
            _dimension("match_result", "Match result", source="match_results", value_source="parser_normalized"),
            _dimension("game_result", "Game result", source="game_results", value_source="parser_normalized"),
            _dimension("mulligan_count", "Mulligan count", source="mulligan_events", value_source="parser_normalized"),
            _dimension(
                "opening_hand_size",
                "Opening hand size",
                source="opening_hands",
                value_source="parser_normalized",
            ),
            _dimension("queue", "Queue", source="match_context", value_source="parser_normalized"),
            _dimension("format", "Format", source="match_context", value_source="parser_normalized"),
            _dimension("event", "Event", source="match_context", value_source="parser_normalized"),
            _dimension("card_name", "Card name", source="future_card_projection", value_source="display_only"),
            _dimension("grp_id", "GRP ID", source="future_card_projection", value_source="display_only"),
            _dimension(
                "gameplay_action_type",
                "Gameplay action type",
                source="future_gameplay_action_module",
                value_source="display_only",
            ),
            _dimension(
                "opponent_observed_card",
                "Opponent observed card",
                source="future_opponent_observation_module",
                value_source="display_only",
            ),
            _dimension(
                "journal_matchup_label",
                "Journal matchup label",
                source="future_match_journal_projection",
                value_source="journal_annotation",
                annotation_boundary="Journal annotation",
            ),
            _dimension(
                "journal_archetype_label",
                "Journal archetype label",
                source="future_match_journal_projection",
                value_source="journal_annotation",
                annotation_boundary="Journal annotation",
            ),
        ],
        "metrics": [
            "games_played",
            "matches_played",
            "wins",
            "losses",
            "win_rate",
            "known_result_count",
            "unknown_degraded_count",
            "sample_size_warning_count",
            "review_required_count",
        ],
        "warnings": ["custom_explorer_builder_deferred"],
        "errors": [],
    }


def _sample_size_status(known_result_count: int, rows: list[dict[str, object]]) -> str:
    if not rows:
        return "empty"
    if known_result_count == 0:
        return "unknown"
    if any(
        isinstance(row.get("sample_size"), dict) and row["sample_size"].get("status") == "small_sample"
        for row in rows
    ):
        return "small_sample"
    return "ok"


def _quality_notes(sample_size_status: str, unknown_or_degraded_count: int) -> list[str]:
    notes = []
    if sample_size_status == "small_sample":
        notes.append("Limited sample; descriptive review only.")
    if unknown_or_degraded_count:
        notes.append("Unknown or degraded rows remain visible.")
    if not notes:
        notes.append("Descriptive local analytics projection.")
    return notes


def _metric_value(row: dict[str, object], metric_id: str) -> int:
    metrics = row.get("metrics")
    if not isinstance(metrics, list):
        return 0
    for metric in metrics:
        if isinstance(metric, dict) and metric.get("metric_id") == metric_id:
            value = metric.get("value")
            return _int_value(value)
    return 0


def _percent_value(ratio: float | None) -> float | None:
    if ratio is None:
        return None
    return round(ratio * 100, 1)


def _percent_display(value: object) -> str:
    if not isinstance(value, int | float):
        return "No known results"
    if float(value).is_integer():
        return f"{int(value)} percent"
    return f"{value:.1f} percent"


def _sample_warning_for_count(known_result_count: int) -> str:
    if known_result_count <= 0:
        return "empty"
    if known_result_count < 10:
        return "small_sample"
    return "ok"


def _safe_warning(value: object) -> str | None:
    if value in {"ok", "small_sample"}:
        return str(value)
    return None


def _safe_group_value(value: object, *, fallback: str) -> str:
    if value is None:
        return fallback
    text = str(value).strip().lower()
    if not text or not re.fullmatch(r"[a-z0-9_.:-]+", text):
        return fallback
    return text


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-z0-9_.:-]+", "_", value.lower()).strip("_") or "unknown"


def _label(value: str) -> str:
    if value == "game1":
        return "Game 1"
    return value.replace("_", " ").replace("-", " ").title()


def _opening_hand_label(value: str) -> str:
    if value == "unknown":
        return "Opening hand unknown"
    return f"{value} cards"


def _mulligan_label(value: str) -> str:
    if value == "kept_initial_hand":
        return "Kept initial hand"
    if value.startswith("mulligan_"):
        return f"Mulligan count {value.removeprefix('mulligan_')}"
    return "Mulligan unknown"


def _optional_ratio(value: object) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    return None


def _int_value(value: object) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int | float):
        return int(value)
    return 0


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, str)]


def _stable_errors(database_status: dict[str, object]) -> list[str]:
    errors = database_status.get("errors")
    if isinstance(errors, list) and all(isinstance(entry, str) for entry in errors):
        return errors
    return ["analytics_dashboard_database_unavailable"]


_PLAY_DRAW_DASHBOARD_QUERY = """
SELECT
    splits.play_draw,
    splits.game_count,
    splits.known_result_count,
    splits.wins,
    splits.losses,
    splits.unknown_result_count,
    splits.unavailable_result_count,
    splits.degraded_result_count,
    splits.win_rate,
    warnings.sample_size_warning
FROM v_play_draw_splits AS splits
LEFT JOIN v_sample_size_warnings AS warnings
    ON warnings.play_draw = splits.play_draw
ORDER BY
    CASE splits.play_draw
        WHEN 'play' THEN 0
        WHEN 'draw' THEN 1
        WHEN 'unknown' THEN 2
        ELSE 3
    END ASC,
    splits.play_draw ASC
"""

_GAME1_POSTBOARD_DASHBOARD_QUERY = """
WITH grouped AS (
    SELECT
        CASE
            WHEN pre_postboard_label IN ('game1', 'preboard') OR game_number = 1 THEN 'game1'
            WHEN pre_postboard_label = 'postboard' THEN 'postboard'
            ELSE 'unknown'
        END AS game1_postboard,
        local_result,
        availability_status,
        drift_status,
        value_source,
        confidence
    FROM v_game1_vs_postboard
)
SELECT
    game1_postboard,
    COUNT(*) AS game_count,
    SUM(CASE WHEN local_result IN ('win', 'loss') THEN 1 ELSE 0 END) AS known_result_count,
    SUM(CASE WHEN local_result = 'win' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN local_result = 'loss' THEN 1 ELSE 0 END) AS losses,
    SUM(CASE WHEN local_result IS NULL OR local_result NOT IN ('win', 'loss') THEN 1 ELSE 0 END)
        AS unknown_result_count,
    SUM(CASE WHEN availability_status != 'available' THEN 1 ELSE 0 END) AS unavailable_result_count,
    SUM(
        CASE
            WHEN drift_status IN ('degraded', 'conflict', 'missing_expected_evidence', 'redacted')
              OR value_source = 'conflict'
              OR confidence IN ('low', 'unknown')
            THEN 1
            ELSE 0
        END
    ) AS degraded_result_count,
    CASE
        WHEN SUM(CASE WHEN local_result IN ('win', 'loss') THEN 1 ELSE 0 END) = 0 THEN NULL
        ELSE
            SUM(CASE WHEN local_result = 'win' THEN 1.0 ELSE 0.0 END)
            / SUM(CASE WHEN local_result IN ('win', 'loss') THEN 1.0 ELSE 0.0 END)
    END AS win_rate
FROM grouped
GROUP BY game1_postboard
ORDER BY
    CASE game1_postboard
        WHEN 'game1' THEN 0
        WHEN 'postboard' THEN 1
        WHEN 'unknown' THEN 2
        ELSE 3
    END ASC,
    game1_postboard ASC
"""

_MULLIGAN_OPENING_HAND_DASHBOARD_QUERY = """
WITH mulligan_by_game AS (
    SELECT
        game_id,
        COUNT(*) AS mulligan_event_count,
        MAX(COALESCE(mulligan_count, -1)) AS max_mulligan_count,
        SUM(CASE WHEN availability_status != 'available' THEN 1 ELSE 0 END) AS mulligan_unavailable_count,
        SUM(
            CASE
                WHEN drift_status IN ('degraded', 'conflict', 'missing_expected_evidence', 'redacted')
                  OR value_source = 'conflict'
                  OR confidence IN ('low', 'unknown')
                THEN 1
                ELSE 0
            END
        ) AS mulligan_degraded_count
    FROM mulligan_events
    GROUP BY game_id
)
SELECT
    COALESCE(CAST(oh.hand_size AS TEXT), 'unknown') AS opening_hand_size,
    CASE
        WHEN mb.mulligan_event_count IS NULL THEN 'unknown'
        WHEN mb.max_mulligan_count <= 0 THEN 'kept_initial_hand'
        ELSE 'mulligan_' || mb.max_mulligan_count
    END AS mulligan_bucket,
    COUNT(*) AS game_count,
    SUM(CASE WHEN gr.local_result IN ('win', 'loss') THEN 1 ELSE 0 END) AS known_result_count,
    SUM(CASE WHEN gr.local_result = 'win' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN gr.local_result = 'loss' THEN 1 ELSE 0 END) AS losses,
    SUM(CASE WHEN gr.local_result IS NULL OR gr.local_result NOT IN ('win', 'loss') THEN 1 ELSE 0 END)
        AS unknown_result_count,
    SUM(
        CASE
            WHEN oh.availability_status != 'available'
              OR COALESCE(gr.availability_status, 'available') != 'available'
              OR COALESCE(mb.mulligan_unavailable_count, 0) > 0
            THEN 1
            ELSE 0
        END
    ) AS unavailable_result_count,
    SUM(
        CASE
            WHEN oh.drift_status IN ('degraded', 'conflict', 'missing_expected_evidence', 'redacted')
              OR oh.value_source = 'conflict'
              OR oh.confidence IN ('low', 'unknown')
              OR COALESCE(gr.drift_status, 'none') IN ('degraded', 'conflict', 'missing_expected_evidence', 'redacted')
              OR COALESCE(gr.value_source, 'observed') = 'conflict'
              OR COALESCE(gr.confidence, 'high') IN ('low', 'unknown')
              OR COALESCE(mb.mulligan_degraded_count, 0) > 0
            THEN 1
            ELSE 0
        END
    ) AS degraded_result_count,
    CASE
        WHEN SUM(CASE WHEN gr.local_result IN ('win', 'loss') THEN 1 ELSE 0 END) = 0 THEN NULL
        ELSE
            SUM(CASE WHEN gr.local_result = 'win' THEN 1.0 ELSE 0.0 END)
            / SUM(CASE WHEN gr.local_result IN ('win', 'loss') THEN 1.0 ELSE 0.0 END)
    END AS win_rate
FROM opening_hands AS oh
LEFT JOIN game_results AS gr
    ON gr.game_id = oh.game_id
LEFT JOIN mulligan_by_game AS mb
    ON mb.game_id = oh.game_id
GROUP BY opening_hand_size, mulligan_bucket
ORDER BY
    CASE opening_hand_size
        WHEN 'unknown' THEN 99
        ELSE CAST(opening_hand_size AS INTEGER)
    END DESC,
    mulligan_bucket ASC
"""
