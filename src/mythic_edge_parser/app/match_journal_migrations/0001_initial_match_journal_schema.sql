CREATE TABLE journal_schema_migrations (
    migration_id TEXT PRIMARY KEY,
    migration_filename TEXT NOT NULL,
    checksum_sha256 TEXT NOT NULL,
    applied_at TEXT NOT NULL,
    schema_version_after TEXT NOT NULL
);

CREATE TABLE journal_schema_versions (
    schema_version_id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL
);

INSERT INTO journal_schema_versions (
    schema_version_id,
    description,
    created_at
) VALUES (
    'match_journal_local_sqlite_schema.v1',
    'Match Journal local SQLite schema v1',
    '2026-05-29T00:00:00+00:00'
);

CREATE TABLE journal_matches (
    journal_match_id TEXT PRIMARY KEY,
    parser_match_id TEXT,
    attachment_status TEXT NOT NULL DEFAULT 'unattached'
        CHECK (attachment_status IN ('attached', 'unattached', 'pending', 'ambiguous', 'detached')),
    title TEXT,
    experiment_id TEXT,
    review_status TEXT NOT NULL DEFAULT 'not_reviewed'
        CHECK (review_status IN ('not_reviewed', 'needs_review', 'reviewing', 'reviewed', 'archived')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    author_label TEXT NOT NULL,
    source_surface TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_surface IN ('manual', 'imported_review', 'local_tool', 'test_fixture')),
    privacy_label TEXT NOT NULL DEFAULT 'local_private'
        CHECK (privacy_label IN ('local_private', 'sanitized_fixture', 'shareable_summary')),
    CHECK (attachment_status != 'attached' OR parser_match_id IS NOT NULL)
);

CREATE TABLE journal_games (
    journal_game_id TEXT PRIMARY KEY,
    journal_match_id TEXT REFERENCES journal_matches(journal_match_id) ON DELETE SET NULL,
    parser_match_id TEXT,
    parser_game_id TEXT,
    game_number INTEGER CHECK (game_number IS NULL OR game_number > 0),
    attachment_status TEXT NOT NULL DEFAULT 'unattached'
        CHECK (attachment_status IN ('attached', 'unattached', 'pending', 'ambiguous', 'detached')),
    review_status TEXT NOT NULL DEFAULT 'not_reviewed'
        CHECK (review_status IN ('not_reviewed', 'needs_review', 'reviewing', 'reviewed', 'archived')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    author_label TEXT NOT NULL,
    source_surface TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_surface IN ('manual', 'imported_review', 'local_tool', 'test_fixture')),
    privacy_label TEXT NOT NULL DEFAULT 'local_private'
        CHECK (privacy_label IN ('local_private', 'sanitized_fixture', 'shareable_summary')),
    CHECK (attachment_status != 'attached' OR parser_game_id IS NOT NULL)
);

CREATE TABLE journal_notes (
    journal_note_id TEXT PRIMARY KEY,
    journal_match_id TEXT REFERENCES journal_matches(journal_match_id) ON DELETE SET NULL,
    journal_game_id TEXT REFERENCES journal_games(journal_game_id) ON DELETE SET NULL,
    parser_match_id TEXT,
    parser_game_id TEXT,
    note_scope TEXT NOT NULL
        CHECK (note_scope IN ('match', 'game', 'sideboarding', 'turn', 'action', 'general', 'unattached')),
    note_text TEXT NOT NULL,
    note_format TEXT NOT NULL DEFAULT 'plain_text'
        CHECK (note_format IN ('plain_text', 'markdown')),
    author_label TEXT NOT NULL,
    source_surface TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_surface IN ('manual', 'imported_review', 'local_tool', 'test_fixture')),
    privacy_label TEXT NOT NULL DEFAULT 'local_private'
        CHECK (privacy_label IN ('local_private', 'sanitized_fixture', 'shareable_summary')),
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0, 1)),
    supersedes_note_id TEXT REFERENCES journal_notes(journal_note_id) ON DELETE SET NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE journal_reference_values (
    reference_id TEXT PRIMARY KEY,
    reference_type TEXT NOT NULL
        CHECK (
            reference_type IN (
                'review_status',
                'pilot_error_reason',
                'opponent_archetype_tier',
                'sideboarding_label',
                'experiment_id',
                'custom_label'
            )
        ),
    label TEXT NOT NULL,
    description TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE journal_labels (
    journal_label_id TEXT PRIMARY KEY,
    journal_match_id TEXT REFERENCES journal_matches(journal_match_id) ON DELETE SET NULL,
    journal_game_id TEXT REFERENCES journal_games(journal_game_id) ON DELETE SET NULL,
    parser_match_id TEXT,
    parser_game_id TEXT,
    label_scope TEXT NOT NULL
        CHECK (label_scope IN ('match', 'game', 'sideboarding', 'review', 'experiment', 'opponent', 'unattached')),
    label_type TEXT NOT NULL
        CHECK (
            label_type IN (
                'matchup_label',
                'opponent_archetype',
                'opponent_archetype_tier',
                'experiment_id',
                'pilot_error',
                'pilot_error_reason',
                'review_status',
                'sideboarding_label',
                'custom'
            )
        ),
    label_value TEXT NOT NULL,
    reference_id TEXT REFERENCES journal_reference_values(reference_id) ON DELETE SET NULL,
    author_label TEXT NOT NULL,
    source_surface TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_surface IN ('manual', 'imported_review', 'local_tool', 'test_fixture')),
    privacy_label TEXT NOT NULL DEFAULT 'local_private'
        CHECK (privacy_label IN ('local_private', 'sanitized_fixture', 'shareable_summary')),
    is_current INTEGER NOT NULL DEFAULT 1 CHECK (is_current IN (0, 1)),
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (label_type != 'pilot_error' OR label_value IN ('yes', 'no', 'unknown', 'not_reviewed'))
);

CREATE TABLE journal_review_flags (
    journal_review_flag_id TEXT PRIMARY KEY,
    journal_match_id TEXT REFERENCES journal_matches(journal_match_id) ON DELETE SET NULL,
    journal_game_id TEXT REFERENCES journal_games(journal_game_id) ON DELETE SET NULL,
    parser_match_id TEXT,
    parser_game_id TEXT,
    flag_type TEXT NOT NULL
        CHECK (
            flag_type IN (
                'needs_review',
                'interesting_match',
                'suspected_parser_gap',
                'sideboarding_review',
                'pilot_error_review',
                'custom'
            )
        ),
    flag_status TEXT NOT NULL DEFAULT 'open'
        CHECK (flag_status IN ('open', 'in_progress', 'resolved', 'dismissed', 'archived')),
    priority_label TEXT NOT NULL DEFAULT 'normal',
    reason TEXT,
    author_label TEXT NOT NULL,
    source_surface TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_surface IN ('manual', 'imported_review', 'local_tool', 'test_fixture')),
    privacy_label TEXT NOT NULL DEFAULT 'local_private'
        CHECK (privacy_label IN ('local_private', 'sanitized_fixture', 'shareable_summary')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE journal_field_overrides (
    journal_field_override_id TEXT PRIMARY KEY,
    journal_match_id TEXT REFERENCES journal_matches(journal_match_id) ON DELETE SET NULL,
    journal_game_id TEXT REFERENCES journal_games(journal_game_id) ON DELETE SET NULL,
    parser_match_id TEXT,
    parser_game_id TEXT,
    target_surface TEXT NOT NULL
        CHECK (
            target_surface IN (
                'match_log_row',
                'game_log_row',
                'action_log_row',
                'analytics_view',
                'journal_display'
            )
        ),
    target_field TEXT NOT NULL,
    original_value_label TEXT,
    proposed_value_label TEXT NOT NULL,
    override_reason TEXT,
    override_status TEXT NOT NULL DEFAULT 'proposed'
        CHECK (
            override_status IN (
                'proposed',
                'accepted_for_journal_display',
                'rejected',
                'superseded',
                'archived'
            )
        ),
    effect_scope TEXT NOT NULL DEFAULT 'journal_display_only'
        CHECK (effect_scope = 'journal_display_only'),
    author_label TEXT NOT NULL,
    source_surface TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_surface IN ('manual', 'imported_review', 'local_tool', 'test_fixture')),
    privacy_label TEXT NOT NULL DEFAULT 'local_private'
        CHECK (privacy_label IN ('local_private', 'sanitized_fixture', 'shareable_summary')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_journal_matches_parser_match_id ON journal_matches(parser_match_id);
CREATE INDEX idx_journal_matches_review_status ON journal_matches(review_status);
CREATE INDEX idx_journal_games_journal_match_id ON journal_games(journal_match_id);
CREATE INDEX idx_journal_games_parser_game_id ON journal_games(parser_game_id);
CREATE INDEX idx_journal_notes_journal_match_id ON journal_notes(journal_match_id);
CREATE INDEX idx_journal_notes_journal_game_id ON journal_notes(journal_game_id);
CREATE INDEX idx_journal_notes_current_scope ON journal_notes(is_current, note_scope);
CREATE INDEX idx_journal_labels_match_type ON journal_labels(journal_match_id, label_type, is_current);
CREATE INDEX idx_journal_review_flags_status ON journal_review_flags(flag_status, flag_type);
CREATE INDEX idx_journal_field_overrides_target ON journal_field_overrides(target_surface, target_field);
