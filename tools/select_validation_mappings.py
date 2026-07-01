"""Focused validation mapping data for the advisory selector."""

PROTECTED_CATEGORY_GROUPS = {
    "parser_surface",
    "parser_state_or_model_surface",
    "extractor_surface",
    "runtime_app_surface",
    "workbook_schema_or_export_surface",
    "webhook_or_output_surface",
    "apps_script_surface",
}

FOCUSED_TEST_MAPPINGS: tuple[tuple[str, str], ...] = (
    ("tools/select_validation.py", "python3 -m pytest -q tests/test_select_validation.py"),
    ("tests/test_select_validation.py", "python3 -m pytest -q tests/test_select_validation.py"),
    ("docs/local_artifacts_manifest.json", "python3 -m pytest -q tests/test_check_local_environment.py"),
    ("tools/check_local_environment.py", "python3 -m pytest -q tests/test_check_local_environment.py"),
    ("tests/test_check_local_environment.py", "python3 -m pytest -q tests/test_check_local_environment.py"),
    ("tools/generate_hardening_report.py", "python3 -m pytest -q tests/test_hardening_report_generator.py"),
    ("tests/test_hardening_report_generator.py", "python3 -m pytest -q tests/test_hardening_report_generator.py"),
    ("tools/run_hardening_orchestrator.py", "python3 -m pytest -q tests/test_hardening_orchestrator.py"),
    ("tests/test_hardening_orchestrator.py", "python3 -m pytest -q tests/test_hardening_orchestrator.py"),
    ("tools/check_secret_patterns.py", "python3 -m pytest -q tests/test_check_secret_patterns.py"),
    ("tests/test_check_secret_patterns.py", "python3 -m pytest -q tests/test_check_secret_patterns.py"),
    ("tools/check_coverage_floor.py", "python3 -m pytest -q tests/test_check_coverage_floor.py"),
    ("tests/test_check_coverage_floor.py", "python3 -m pytest -q tests/test_check_coverage_floor.py"),
    ("tools/check_protected_surfaces.py", "python3 -m pytest -q tests/test_check_protected_surfaces.py"),
    ("tests/test_check_protected_surfaces.py", "python3 -m pytest -q tests/test_check_protected_surfaces.py"),
    ("tools/check_surface_authorization.py", "python3 -m pytest -q tests/test_check_surface_authorization.py"),
    ("tests/test_check_surface_authorization.py", "python3 -m pytest -q tests/test_check_surface_authorization.py"),
    ("tools/dev_app/dev_app_launcher.py", "python3 -m pytest -q tests/test_analytics_dev_app_launcher.py"),
    ("tools/dev_app/start_mythic_edge_dev_app.ps1", "python3 -m pytest -q tests/test_analytics_dev_app_launcher.py"),
    ("tests/test_analytics_dev_app_launcher.py", "python3 -m pytest -q tests/test_analytics_dev_app_launcher.py"),
    (
        "src/mythic_edge_parser/parsers/gre/connect_resp.py",
        "python3 -m pytest -q tests/test_gre_connect_resp_parser.py",
    ),
    ("src/mythic_edge_parser/parsers/gre/game_result.py", "python3 -m pytest -q tests/test_gre_game_result_parser.py"),
    ("src/mythic_edge_parser/parsers/gre/game_state.py", "python3 -m pytest -q tests/test_gre_game_state_parser.py"),
    ("src/mythic_edge_parser/parsers/gre/turn_info.py", "python3 -m pytest -q tests/test_gre_turn_info_parser.py"),
    (
        "src/mythic_edge_parser/parsers/match_state.py",
        "python3 -m pytest -q tests/test_match_state_parser.py tests/test_match_summary_from_match_state.py",
    ),
    ("src/mythic_edge_parser/parsers/api_common.py", "python3 -m pytest -q tests/test_api_common.py"),
    ("src/mythic_edge_parser/parsers/client_actions.py", "python3 -m pytest -q tests/test_client_actions_parser.py"),
    ("src/mythic_edge_parser/app/event_identity.py", "python3 -m pytest -q tests/test_event_identity.py"),
    ("src/mythic_edge_parser/app/state.py", "python3 -m pytest -q tests/test_state.py"),
    ("src/mythic_edge_parser/app/models.py", "python3 -m pytest -q tests/test_app_models.py tests/test_events.py"),
    ("src/mythic_edge_parser/app/extractors.py", "python3 -m pytest -q tests/test_app_extractors.py"),
    ("src/mythic_edge_parser/app/runner.py", "python3 -m pytest -q tests/test_runner.py"),
    ("src/mythic_edge_parser/app/outputs.py", "python3 -m pytest -q tests/test_app_outputs.py"),
    (
        "src/mythic_edge_parser/app/sheet_schema.py",
        "python3 -m pytest -q tests/test_sheet_schema.py tests/test_event_schema_snapshots.py",
    ),
    (
        "src/mythic_edge_parser/app/sheet_exports.py",
        "python3 -m pytest -q tests/test_sheet_exports.py tests/test_event_schema_snapshots.py",
    ),
    (
        "src/mythic_edge_parser/app/transforms.py",
        "python3 -m pytest -q tests/test_transforms.py tests/test_event_schema_snapshots.py",
    ),
    ("src/mythic_edge_parser/app/runtime_surfaces.py", "python3 -m pytest -q tests/test_runtime_surfaces.py"),
    ("src/mythic_edge_parser/app/diagnostics.py", "python3 -m pytest -q tests/test_diagnostics.py"),
    ("src/mythic_edge_parser/app/log_drift_sensor.py", "python3 -m pytest -q tests/test_log_drift_sensor.py"),
    ("src/mythic_edge_parser/app/status_api.py", "python3 -m pytest -q tests/test_status_api.py"),
    (
        "src/mythic_edge_parser/app/analytics_migration_loader.py",
        "python3 -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py",
    ),
    (
        "src/mythic_edge_parser/app/analytics_migrations/__init__.py",
        "python3 -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py",
    ),
    ("src/mythic_edge_parser/app/analytics_sidecar.py", "python3 -m pytest -q tests/test_analytics_sidecar.py"),
    (
        "src/mythic_edge_parser/app/analytics_ingest.py",
        "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py "
        "tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py "
        "tests/test_analytics_field_evidence_ingest.py",
    ),
    (
        "src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py",
        "python3 -m pytest -q tests/test_analytics_legacy_jsonl_artifact_adapter.py "
        "tests/test_analytics_manual_jsonl_import.py tests/test_analytics_browser_jsonl_upload.py",
    ),
    (
        "src/mythic_edge_parser/local_app/config.py",
        "python3 -m pytest -q tests/test_analytics_local_app_config.py",
    ),
    (
        "src/mythic_edge_parser/local_app/paths.py",
        "python3 -m pytest -q tests/test_analytics_local_app_config.py",
    ),
    (
        "src/mythic_edge_parser/local_app/setup_status.py",
        "python3 -m pytest -q tests/test_analytics_local_app_config.py tests/test_analytics_local_app_backend.py",
    ),
    (
        "src/mythic_edge_parser/local_app/backend.py",
        "python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_manual_jsonl_import.py "
        "tests/test_analytics_app_match_game_history_views.py tests/test_analytics_app_opening_hand_mulligan_views.py "
        "tests/test_analytics_app_play_draw_postboard_split_views.py "
        "tests/test_analytics_app_gameplay_action_opponent_observation_views.py",
    ),
    (
        "src/mythic_edge_parser/local_app/import_jobs.py",
        "python3 -m pytest -q tests/test_analytics_manual_jsonl_import.py tests/test_analytics_browser_jsonl_upload.py",
    ),
    (
        "src/mythic_edge_parser/local_app/analytics_history.py",
        "python3 -m pytest -q tests/test_analytics_app_match_game_history_views.py "
        "tests/test_analytics_app_opening_hand_mulligan_views.py "
        "tests/test_analytics_app_play_draw_postboard_split_views.py "
        "tests/test_analytics_app_gameplay_action_opponent_observation_views.py",
    ),
    (
        "src/mythic_edge_parser/stream.py",
        "python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py",
    ),
)
