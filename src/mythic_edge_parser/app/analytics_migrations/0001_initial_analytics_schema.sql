-- Mythic Edge local analytics SQLite schema v1.
-- Schema definitions are source-controlled SQL. Generated databases live under
-- data/analytics/ and must remain local-only.
-- Derived views are not materialized; core provenance columns are not_applicable
-- on views and remain on their source fact tables.

PRAGMA foreign_keys = ON;

CREATE TABLE schema_migrations (
    migration_id TEXT PRIMARY KEY,
    migration_filename TEXT NOT NULL UNIQUE,
    checksum_sha256 TEXT NOT NULL,
    applied_at TEXT NOT NULL,
    schema_version_after TEXT NOT NULL
);

CREATE TABLE parser_schema_versions (
    parser_schema_version_id TEXT PRIMARY KEY,
    parser_code_version TEXT,
    source_surfaces TEXT NOT NULL,
    field_evidence_schema_version TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO parser_schema_versions (
    parser_schema_version_id,
    parser_code_version,
    source_surfaces,
    field_evidence_schema_version,
    created_at
) VALUES (
    'analytics_local_sqlite_schema.v1',
    '',
    'MatchLogRow,GameLogRow,gameplay_action_entry,opponent_card_observation,field_evidence',
    '',
    'migration:0001_initial_analytics_schema'
);

CREATE TABLE ingest_runs (
    ingest_run_id TEXT PRIMARY KEY,
    source_kind TEXT NOT NULL CHECK (
        source_kind IN ('live_parser', 'saved_event_replay', 'sanitized_golden_replay')
    ),
    source_artifact_label TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('started', 'completed', 'failed', 'aborted')),
    parser_commit TEXT,
    parser_version TEXT,
    schema_version TEXT NOT NULL,
    row_counts_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (schema_version) REFERENCES parser_schema_versions(parser_schema_version_id)
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    session_label TEXT,
    started_at TEXT,
    ended_at TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE matches (
    match_id TEXT PRIMARY KEY,
    session_id TEXT,
    parser_match_key TEXT,
    match_started_at TEXT,
    match_completed_at TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE games (
    game_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL CHECK (game_number > 0),
    game_started_at TEXT,
    game_completed_at TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (match_id, game_number),
    CHECK (game_id = match_id || ':g' || game_number),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE game_players (
    game_player_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    team_id INTEGER,
    seat_id INTEGER,
    player_relation TEXT NOT NULL CHECK (player_relation IN ('local', 'opponent', 'unknown')),
    player_name_label TEXT,
    is_local INTEGER CHECK (is_local IN (0, 1)),
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE deck_labels (
    deck_label_id TEXT PRIMARY KEY,
    match_id TEXT,
    session_id TEXT,
    label_type TEXT NOT NULL,
    label_value TEXT NOT NULL,
    label_source TEXT NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    is_current INTEGER NOT NULL CHECK (is_current IN (0, 1)),
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE match_results (
    match_result_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL UNIQUE,
    match_result TEXT,
    winner_team_id INTEGER,
    games_won INTEGER,
    games_lost INTEGER,
    total_games INTEGER,
    match_win INTEGER CHECK (match_win IN (0, 1)),
    game_win_rate REAL,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE game_results (
    game_result_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL UNIQUE,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    winner_team_id INTEGER,
    local_result TEXT,
    pre_postboard_label TEXT CHECK (
        pre_postboard_label IS NULL OR pre_postboard_label IN ('game1', 'preboard', 'postboard', 'unknown')
    ),
    play_draw TEXT CHECK (play_draw IS NULL OR play_draw IN ('play', 'draw', 'unknown')),
    turn_count INTEGER,
    game_started_at TEXT,
    game_completed_at TEXT,
    game_duration_seconds REAL,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE match_context (
    match_context_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL UNIQUE,
    queue_name TEXT,
    format_name TEXT,
    event_id TEXT,
    match_win_condition TEXT,
    event_type TEXT,
    event_scope TEXT,
    event_source TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE rank_snapshots (
    rank_snapshot_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL,
    game_id TEXT,
    rank_context TEXT,
    rank_source TEXT,
    constructed_rank TEXT,
    constructed_tier TEXT,
    limited_rank TEXT,
    limited_tier TEXT,
    season_ordinal INTEGER,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE opening_hands (
    opening_hand_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL UNIQUE,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    hand_size INTEGER,
    exact_card_count INTEGER,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (opening_hand_id = game_id || ':opening_hand'),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE opening_hand_cards (
    opening_hand_card_id TEXT PRIMARY KEY,
    opening_hand_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    card_position INTEGER NOT NULL,
    grp_id INTEGER,
    card_name TEXT,
    identity_hint_source TEXT,
    name_resolution_status TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (opening_hand_id, card_position),
    CHECK (opening_hand_card_id = opening_hand_id || ':slot' || card_position),
    FOREIGN KEY (opening_hand_id) REFERENCES opening_hands(opening_hand_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE mulligan_events (
    mulligan_event_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    ordinal_or_count TEXT NOT NULL,
    mulligan_count INTEGER,
    decision_detail TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (mulligan_event_id = game_id || ':mulligan:' || ordinal_or_count),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE mulligan_bottomed_or_discarded_cards (
    mulligan_card_id TEXT PRIMARY KEY,
    mulligan_event_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    card_position INTEGER NOT NULL,
    card_action TEXT NOT NULL CHECK (card_action IN ('bottomed', 'discarded', 'unknown')),
    grp_id INTEGER,
    card_name TEXT,
    identity_hint_source TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (mulligan_event_id) REFERENCES mulligan_events(mulligan_event_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE sideboarding_states (
    sideboarding_state_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    sideboarding_entered INTEGER CHECK (sideboarding_entered IN (0, 1)),
    submit_deck_seen INTEGER CHECK (submit_deck_seen IN (0, 1)),
    exact_sideboard_delta_available INTEGER NOT NULL CHECK (exact_sideboard_delta_available IN (0, 1)),
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE submitted_deck_snapshots (
    submitted_deck_snapshot_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL UNIQUE,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    deck_name_label TEXT,
    submitted_at TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (submitted_deck_snapshot_id = game_id || ':submitted_deck'),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE submitted_deck_cards (
    submitted_deck_card_id TEXT PRIMARY KEY,
    submitted_deck_snapshot_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    section TEXT NOT NULL CHECK (section IN ('main', 'sideboard', 'companion', 'unknown')),
    grp_id INTEGER,
    card_key TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    card_name TEXT,
    identity_hint_source TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (submitted_deck_snapshot_id) REFERENCES submitted_deck_snapshots(submitted_deck_snapshot_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE turns (
    turn_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    turn_number INTEGER NOT NULL CHECK (turn_number >= 0),
    active_player_relation TEXT CHECK (
        active_player_relation IS NULL OR active_player_relation IN ('local', 'opponent', 'unknown')
    ),
    started_at TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (game_id, turn_number),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE gameplay_actions (
    gameplay_action_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    timestamp TEXT,
    game_state_id INTEGER,
    turn_number INTEGER,
    action_type TEXT NOT NULL,
    actor_relation TEXT NOT NULL CHECK (actor_relation IN ('local', 'opponent', 'unknown', '')),
    from_zone_type TEXT,
    to_zone_type TEXT,
    source_status TEXT,
    annotation_context_label TEXT,
    raw_action_type_labels TEXT,
    annotation_type_labels TEXT,
    visible_in_log INTEGER CHECK (visible_in_log IN (0, 1)),
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE gameplay_action_cards (
    gameplay_action_card_id TEXT PRIMARY KEY,
    gameplay_action_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    card_ordinal INTEGER NOT NULL,
    instance_id INTEGER,
    grp_id INTEGER,
    observed_grp_id INTEGER,
    overlay_grp_id INTEGER,
    object_source_grp_id INTEGER,
    identity_hint_source TEXT,
    card_name TEXT,
    display_name TEXT,
    name_resolution_status TEXT,
    enrichment_status TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (gameplay_action_id, card_ordinal),
    FOREIGN KEY (gameplay_action_id) REFERENCES gameplay_actions(gameplay_action_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE card_movements (
    card_movement_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    gameplay_action_id TEXT,
    turn_number INTEGER,
    grp_id INTEGER,
    instance_id INTEGER,
    from_zone_type TEXT,
    to_zone_type TEXT,
    movement_type TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (gameplay_action_id) REFERENCES gameplay_actions(gameplay_action_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE life_totals (
    life_total_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    turn_number INTEGER,
    player_relation TEXT NOT NULL CHECK (player_relation IN ('local', 'opponent', 'unknown')),
    life_total INTEGER,
    source_status TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE public_zone_observations (
    public_zone_observation_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    turn_number INTEGER,
    zone_type TEXT NOT NULL,
    player_relation TEXT NOT NULL CHECK (player_relation IN ('local', 'opponent', 'unknown')),
    grp_id INTEGER,
    instance_id INTEGER,
    visibility TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE opponent_card_observations (
    opponent_card_observation_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    gameplay_action_id TEXT,
    timestamp TEXT,
    game_state_id INTEGER,
    turn_number INTEGER,
    actor_relation TEXT NOT NULL CHECK (actor_relation = 'opponent'),
    actor_seat_id INTEGER,
    local_seat_id INTEGER,
    instance_id INTEGER,
    grp_id INTEGER,
    observed_grp_id INTEGER,
    overlay_grp_id INTEGER,
    object_source_grp_id INTEGER,
    parent_id INTEGER,
    identity_hint_source TEXT,
    card_name TEXT,
    display_name TEXT,
    resolution_status TEXT,
    name_resolution_source TEXT,
    action_type TEXT,
    cast_mode TEXT,
    source_evidence TEXT,
    evidence_status TEXT,
    visibility TEXT,
    from_zone_type TEXT,
    to_zone_type TEXT,
    degradation_flags TEXT,
    review_required INTEGER NOT NULL CHECK (review_required IN (0, 1)),
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (gameplay_action_id) REFERENCES gameplay_actions(gameplay_action_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE opponent_card_observation_cards (
    opponent_card_observation_card_id TEXT PRIMARY KEY,
    opponent_card_observation_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    card_ordinal INTEGER NOT NULL,
    grp_id INTEGER,
    observed_grp_id INTEGER,
    overlay_grp_id INTEGER,
    object_source_grp_id INTEGER,
    identity_hint_source TEXT,
    card_name TEXT,
    resolution_status TEXT,
    visibility TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (opponent_card_observation_id, card_ordinal),
    FOREIGN KEY (opponent_card_observation_id) REFERENCES opponent_card_observations(opponent_card_observation_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE matchup_labels (
    matchup_label_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL,
    label_value TEXT NOT NULL,
    label_source TEXT NOT NULL,
    author_label TEXT,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    is_current INTEGER NOT NULL CHECK (is_current IN (0, 1)),
    value_source TEXT NOT NULL CHECK (value_source = 'human_annotation'),
    confidence TEXT NOT NULL CHECK (confidence = 'human'),
    finality TEXT NOT NULL CHECK (finality IN ('annotation_current', 'annotation_historical')),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE archetype_labels (
    archetype_label_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL,
    label_value TEXT NOT NULL,
    label_source TEXT NOT NULL,
    author_label TEXT,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    is_current INTEGER NOT NULL CHECK (is_current IN (0, 1)),
    value_source TEXT NOT NULL CHECK (value_source = 'human_annotation'),
    confidence TEXT NOT NULL CHECK (confidence = 'human'),
    finality TEXT NOT NULL CHECK (finality IN ('annotation_current', 'annotation_historical')),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE game_notes (
    game_note_id TEXT PRIMARY KEY,
    game_id TEXT NOT NULL,
    match_id TEXT NOT NULL,
    note_text TEXT NOT NULL,
    note_source TEXT NOT NULL,
    author_label TEXT,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    is_current INTEGER NOT NULL CHECK (is_current IN (0, 1)),
    value_source TEXT NOT NULL CHECK (value_source = 'human_annotation'),
    confidence TEXT NOT NULL CHECK (confidence = 'human'),
    finality TEXT NOT NULL CHECK (finality IN ('annotation_current', 'annotation_historical')),
    drift_status TEXT NOT NULL CHECK (
        drift_status IN ('none', 'not_checked', 'degraded', 'conflict', 'missing_expected_evidence', 'redacted')
    ),
    parser_schema_version TEXT NOT NULL,
    ingest_run_id TEXT NOT NULL,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    availability_status TEXT NOT NULL CHECK (
        availability_status IN (
            'available',
            'expected_unavailable',
            'not_applicable',
            'not_observed',
            'withheld_private',
            'not_yet_supported'
        )
    ),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (parser_schema_version) REFERENCES parser_schema_versions(parser_schema_version_id),
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE TABLE fact_provenance (
    fact_provenance_id TEXT PRIMARY KEY,
    fact_table TEXT NOT NULL,
    fact_id TEXT NOT NULL,
    fact_field TEXT NOT NULL,
    ledger_entry_id TEXT,
    source_parser_surface TEXT NOT NULL,
    source_fact_key TEXT NOT NULL,
    source_event_kind TEXT,
    source_event_type TEXT,
    source_payload_paths TEXT NOT NULL,
    source_event_timestamp TEXT,
    value_source TEXT NOT NULL CHECK (
        value_source IN ('observed', 'derived', 'inferred', 'unknown', 'conflict', 'legacy_enriched', 'human_annotation')
    ),
    confidence TEXT NOT NULL CHECK (confidence IN ('high', 'medium', 'low', 'unknown', 'human')),
    finality TEXT NOT NULL CHECK (
        finality IN ('live', 'provisional', 'final', 'reconciled', 'annotation_current', 'annotation_historical')
    ),
    drift_flags TEXT NOT NULL,
    invariant_status TEXT,
    degraded_reason TEXT,
    review_required INTEGER NOT NULL CHECK (review_required IN (0, 1)),
    ingest_run_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (ingest_run_id) REFERENCES ingest_runs(ingest_run_id)
);

CREATE INDEX idx_ingest_runs_status ON ingest_runs(status);
CREATE INDEX idx_matches_ingest_run ON matches(ingest_run_id);
CREATE INDEX idx_games_match_id ON games(match_id);
CREATE INDEX idx_games_ingest_run ON games(ingest_run_id);
CREATE INDEX idx_game_players_game_id ON game_players(game_id);
CREATE INDEX idx_match_results_match_id ON match_results(match_id);
CREATE INDEX idx_game_results_match_id ON game_results(match_id);
CREATE INDEX idx_game_results_game_id ON game_results(game_id);
CREATE INDEX idx_match_context_match_id ON match_context(match_id);
CREATE INDEX idx_rank_snapshots_match_id ON rank_snapshots(match_id);
CREATE INDEX idx_opening_hands_game_id ON opening_hands(game_id);
CREATE INDEX idx_opening_hand_cards_opening_hand_id ON opening_hand_cards(opening_hand_id);
CREATE INDEX idx_mulligan_events_game_id ON mulligan_events(game_id);
CREATE INDEX idx_sideboarding_states_game_id ON sideboarding_states(game_id);
CREATE INDEX idx_submitted_deck_cards_snapshot_id ON submitted_deck_cards(submitted_deck_snapshot_id);
CREATE INDEX idx_turns_game_id ON turns(game_id);
CREATE INDEX idx_gameplay_actions_match_game ON gameplay_actions(match_id, game_number);
CREATE INDEX idx_gameplay_actions_game_id ON gameplay_actions(game_id);
CREATE INDEX idx_gameplay_action_cards_action_id ON gameplay_action_cards(gameplay_action_id);
CREATE INDEX idx_card_movements_game_id ON card_movements(game_id);
CREATE INDEX idx_life_totals_game_id ON life_totals(game_id);
CREATE INDEX idx_public_zone_observations_game_id ON public_zone_observations(game_id);
CREATE INDEX idx_opponent_card_observations_match_game ON opponent_card_observations(match_id, game_number);
CREATE INDEX idx_opponent_card_observation_cards_observation_id
    ON opponent_card_observation_cards(opponent_card_observation_id);
CREATE INDEX idx_matchup_labels_match_id ON matchup_labels(match_id);
CREATE INDEX idx_archetype_labels_match_id ON archetype_labels(match_id);
CREATE INDEX idx_game_notes_game_id ON game_notes(game_id);
CREATE INDEX idx_fact_provenance_fact ON fact_provenance(fact_table, fact_id, fact_field);
CREATE INDEX idx_fact_provenance_ingest_run ON fact_provenance(ingest_run_id);

CREATE VIEW v_opening_hand_cards AS
SELECT
    oh.match_id,
    oh.game_id,
    oh.game_number,
    oh.hand_size,
    ohc.card_position,
    ohc.grp_id,
    ohc.card_name,
    ohc.identity_hint_source,
    ohc.name_resolution_status,
    ohc.value_source,
    ohc.confidence,
    ohc.finality,
    ohc.availability_status
FROM opening_hands AS oh
JOIN opening_hand_cards AS ohc
    ON oh.opening_hand_id = ohc.opening_hand_id;

CREATE VIEW v_opening_lines AS
SELECT
    match_id,
    game_id,
    game_number,
    turn_number,
    action_type,
    actor_relation,
    from_zone_type,
    to_zone_type,
    value_source,
    confidence,
    availability_status
FROM gameplay_actions
WHERE turn_number IS NOT NULL
  AND turn_number <= 3;

CREATE VIEW v_mulligan_outcomes AS
SELECT
    me.match_id,
    me.game_id,
    me.game_number,
    me.mulligan_count,
    gr.local_result,
    gr.play_draw,
    me.value_source,
    me.confidence,
    me.availability_status
FROM mulligan_events AS me
LEFT JOIN game_results AS gr
    ON me.game_id = gr.game_id;

CREATE VIEW v_game1_vs_postboard AS
SELECT
    match_id,
    game_id,
    game_number,
    pre_postboard_label,
    local_result,
    play_draw,
    turn_count,
    value_source,
    confidence,
    availability_status
FROM game_results;

CREATE VIEW v_play_draw_splits AS
SELECT
    COALESCE(play_draw, 'unknown') AS play_draw,
    COUNT(*) AS game_count,
    SUM(CASE WHEN local_result = 'win' THEN 1 ELSE 0 END) AS wins,
    AVG(CASE WHEN local_result = 'win' THEN 1.0 ELSE 0.0 END) AS win_rate
FROM game_results
GROUP BY COALESCE(play_draw, 'unknown');

CREATE VIEW v_sample_size_warnings AS
SELECT
    play_draw,
    game_count,
    CASE
        WHEN game_count < 10 THEN 'small_sample'
        ELSE 'ok'
    END AS sample_size_warning
FROM v_play_draw_splits;

CREATE VIEW v_matchup_label_performance AS
SELECT
    ml.label_value AS matchup_label,
    COUNT(DISTINCT mr.match_id) AS match_count,
    SUM(CASE WHEN mr.match_win = 1 THEN 1 ELSE 0 END) AS match_wins,
    AVG(CASE WHEN mr.match_win = 1 THEN 1.0 ELSE 0.0 END) AS match_win_rate
FROM matchup_labels AS ml
LEFT JOIN match_results AS mr
    ON ml.match_id = mr.match_id
WHERE ml.is_current = 1
GROUP BY ml.label_value;
