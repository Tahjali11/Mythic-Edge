export const SETUP_STATUS_OBJECT = "mythic_edge_local_app_setup_status";
export const SETUP_STATUS_SCHEMA_VERSION = "analytics_app_backend_setup_status.v1";
export const LIVE_STATUS_SCHEMA_VERSION = "live_app_player_log_path_watcher_status.v1";
export const LIVE_PLAYER_LOG_STATUS_OBJECT = "mythic_edge_local_app_live_player_log_status";
export const LIVE_WATCHER_STATUS_OBJECT = "mythic_edge_local_app_live_watcher_status";
export const LIVE_WATCHER_PROCESS_SCHEMA_VERSION = "live_app_player_log_watcher_process_control_safeguards.v1";
export const LIVE_WATCHER_PROCESS_OBJECT = "mythic_edge_local_app_live_watcher_process_status";
export const MANUAL_IMPORT_JOB_OBJECT = "mythic_edge_local_app_manual_jsonl_import_job";
export const MANUAL_IMPORT_JOB_SCHEMA_VERSION = "analytics_manual_jsonl_import_ui_job_status.v1";
export const LEGACY_JSONL_IMPORT_QUALITY_OBJECT = "mythic_edge_legacy_jsonl_import_quality";
export const LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION = "analytics_legacy_jsonl_import_quality_breakdown.v1";
export const ANALYTICS_HISTORY_SCHEMA_VERSION = "analytics_app_match_game_history_views.v1";
export const MATCH_HISTORY_OBJECT = "mythic_edge_local_app_match_history";
export const GAME_HISTORY_OBJECT = "mythic_edge_local_app_game_history";
export const EARLY_GAME_HISTORY_SCHEMA_VERSION = "analytics_app_opening_hand_mulligan_views.v1";
export const OPENING_HAND_HISTORY_OBJECT = "mythic_edge_local_app_opening_hand_history";
export const MULLIGAN_HISTORY_OBJECT = "mythic_edge_local_app_mulligan_history";
export const ACTION_REVIEW_SCHEMA_VERSION = "analytics_app_gameplay_action_opponent_observation_views.v1";
export const GAMEPLAY_ACTION_REVIEW_OBJECT = "mythic_edge_local_app_gameplay_action_review";
export const OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT = "mythic_edge_local_app_opponent_card_observation_review";
export const SPLIT_REVIEW_SCHEMA_VERSION = "analytics_app_play_draw_postboard_split_views.v1";
export const PLAY_DRAW_SPLIT_REVIEW_OBJECT = "mythic_edge_local_app_play_draw_split_review";
export const GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT = "mythic_edge_local_app_game1_postboard_split_review";
export const MATCH_JOURNAL_OBJECT = "mythic_edge_local_app_match_journal";
export const MATCH_JOURNAL_SCHEMA_VERSION = "match_journal_cockpit_ui.v1";

export type SetupStatusTone =
  | "ok"
  | "degraded"
  | "empty"
  | "missing"
  | "unavailable"
  | "error"
  | "deferred"
  | "unknown";

export type SectionStatus = {
  object?: string;
  schema_version?: string;
  status?: string;
  [key: string]: unknown;
};

export type CapabilityStatus = Record<string, string>;

export type LivePlayerLogSummary = {
  status: string;
  source: "configured" | "detected_default" | "none" | "unavailable" | string;
  display_path: string;
  path_kind: "file" | "missing" | "directory" | "unknown" | "unavailable" | string;
  metadata_access: "accessible" | "denied" | "not_checked" | "unavailable" | string;
  exists: boolean;
  contents_read: false;
  tailing_started: false;
  size_bytes?: number | null;
  last_modified_at?: string | null;
  last_modified_age_seconds?: number | null;
  activity_hint?: "recent" | "stale" | "unknown" | "not_applicable" | string;
};

export type LivePlayerLogStatusResponse = {
  object: typeof LIVE_PLAYER_LOG_STATUS_OBJECT;
  schema_version: typeof LIVE_STATUS_SCHEMA_VERSION;
  status: string;
  player_log: LivePlayerLogSummary;
  diagnostics: string[];
  warnings: string[];
  errors: string[];
  [key: string]: unknown;
};

export type LiveWatcherSummary = {
  status: string;
  mode: "readiness_only" | string;
  running: false;
  start_allowed: false;
  stop_allowed: false;
  parser_runner_started: false;
  tailing_started: false;
  sqlite_live_writes_enabled: false;
  reason: string | null;
};

export type LiveWatcherStatusResponse = {
  object: typeof LIVE_WATCHER_STATUS_OBJECT;
  schema_version: typeof LIVE_STATUS_SCHEMA_VERSION;
  status: string;
  watcher: LiveWatcherSummary;
  player_log: LivePlayerLogSummary;
  warnings: string[];
  errors: string[];
  [key: string]: unknown;
};

export type LiveWatcherProcessControl = {
  mode: "safeguards_only";
  implementation_status: "not_implemented" | "state_only" | "deferred" | string;
  start_allowed: false;
  stop_allowed: false;
  start_route_enabled: false;
  stop_route_enabled: false;
  ui_controls_allowed: false;
  automatic_start_enabled: false;
  parser_runner_started: false;
  tailing_started: false;
  sqlite_live_writes_enabled: false;
  external_transport_allowed: false;
  reason: string | null;
};

export type LiveWatcherProcessSummary = {
  status: string;
  running: false;
  pid_verified: false;
  single_instance_guard: string;
  supervisor_boundary: string;
};

export type LiveWatcherProcessState = {
  source: string;
  exists: boolean;
  status: string;
  stale: boolean;
  pid_present: boolean;
  pid_verified: false;
  supervisor_token_present: boolean;
  display_path: string | null;
  raw_path_exposed: false;
};

export type LiveWatcherProcessPrecondition = {
  key: string;
  status: string;
  reason: string | null;
};

export type LiveWatcherProcessStatusResponse = {
  object: typeof LIVE_WATCHER_PROCESS_OBJECT;
  schema_version: typeof LIVE_WATCHER_PROCESS_SCHEMA_VERSION;
  status: string;
  process_control: LiveWatcherProcessControl;
  watcher: LiveWatcherProcessSummary;
  player_log: SectionStatus;
  preconditions: LiveWatcherProcessPrecondition[];
  state: LiveWatcherProcessState;
  warnings: string[];
  errors: string[];
  [key: string]: unknown;
};

export type SetupStatusResponse = {
  object: typeof SETUP_STATUS_OBJECT;
  schema_version: typeof SETUP_STATUS_SCHEMA_VERSION;
  status: string;
  paths: SectionStatus;
  config: SectionStatus;
  player_log: SectionStatus;
  live_player_log?: LivePlayerLogStatusResponse;
  live_watcher?: LiveWatcherStatusResponse;
  live_watcher_process?: LiveWatcherProcessStatusResponse;
  analytics_database: SectionStatus;
  match_journal: SectionStatus;
  migrations: SectionStatus;
  runtime: SectionStatus;
  capabilities: CapabilityStatus;
  [key: string]: unknown;
};

export type SetupStatusErrorCode =
  | "backend_unavailable"
  | "malformed_response"
  | "incompatible_response"
  | "unsafe_api_base_url";
export type LiveStatusErrorCode = SetupStatusErrorCode;

export type ManualImportStatus = "queued" | "running" | "succeeded" | "degraded" | "failed" | "rejected";

export type ManualImportSource = {
  source_kind: "saved_event_replay";
  source_artifact_label: string;
  source_display_label: string;
  source_file_extension: string;
  path_echoed: false;
  source_mode?: "single_file" | "explicit_file_batch" | "uploaded_file_batch" | "adapter_directory_selection" | string;
  files_selected?: number;
  files_accepted?: number;
  files_rejected?: number;
  source_group_label?: string;
  source_artifacts?: ManualImportSourceArtifact[];
};

export type LegacyJsonlImportQualityStatus = "complete" | "degraded" | "failed";

export type LegacyJsonlRoutingHint = {
  code: string;
  category: string;
  severity: string;
  count: number;
};

export type LegacyJsonlImportQuality = {
  object: typeof LEGACY_JSONL_IMPORT_QUALITY_OBJECT;
  schema_version: typeof LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION;
  quality_status: LegacyJsonlImportQualityStatus;
  records_seen: number;
  events_processed: number;
  events_skipped: number;
  processed_kind_counts: Record<string, number>;
  unsupported_kind_counts: Record<string, number>;
  skipped_reason_counts: Record<string, number>;
  blank_line_count: number;
  duplicate_raw_hash_count: number;
  unsupported_kind_skip_count: number;
  output_gap_counts: Record<string, number>;
  adapter_warning_counts: Record<string, number>;
  adapter_warning_codes: string[];
  ingest_warning_codes: string[];
  routing_hints: LegacyJsonlRoutingHint[];
  privacy: {
    has_private_path_echo: false;
    raw_payload_exposed: false;
    raw_hash_exposed: false;
  };
};

export type ManualImportSourceArtifact = {
  batch_index: number;
  source_artifact_label: string;
  source_display_label: string;
  status: "processed" | "processed_with_skips" | "rejected" | "failed" | string;
  records_seen: number;
  events_processed: number;
  events_skipped: number;
  processed_kind_counts: Record<string, number>;
  unsupported_kind_counts: Record<string, number>;
  skipped_reason_counts: Record<string, number>;
  adapter_warning_codes: string[];
};

export type ManualImportAdapter = {
  status: string;
  files_processed: number;
  records_seen: number;
  events_processed: number;
  events_skipped: number;
  unsupported_kind_counts: Record<string, number>;
  warnings: string[];
  quality?: LegacyJsonlImportQuality;
  source_mode?: "single_file" | "explicit_file_batch" | "uploaded_file_batch" | "adapter_directory_selection" | string;
  files_selected?: number;
  files_accepted?: number;
  files_rejected?: number;
  source_artifacts?: ManualImportSourceArtifact[];
};

export type ManualImportIngest = {
  status: string;
  ingest_run_id: string;
  source_kind: string;
  source_artifact_label: string;
  row_counts: Record<string, number>;
  warnings: string[];
  skipped: Record<string, number>;
};

export type ManualImportDatabase = {
  status: string;
  display_path: string;
  created: boolean;
};

export type ManualImportJob = {
  object: typeof MANUAL_IMPORT_JOB_OBJECT;
  schema_version: typeof MANUAL_IMPORT_JOB_SCHEMA_VERSION;
  job_id: string;
  status: ManualImportStatus;
  phase: string;
  created_at: string;
  started_at: string;
  finished_at: string;
  source: ManualImportSource;
  adapter: ManualImportAdapter;
  ingest: ManualImportIngest;
  database: ManualImportDatabase;
  warnings: string[];
  errors: string[];
  [key: string]: unknown;
};

export type ManualImportSingleFileRequest = {
  source_path: string;
  source_paths?: never;
  source_artifact_label?: string;
};

export type ManualImportBatchRequest = {
  source_paths: string[];
  source_path?: never;
  source_artifact_label?: string;
};

export type ManualImportRequest = ManualImportSingleFileRequest | ManualImportBatchRequest;

export type ManualImportUploadRequest = {
  files: File[];
  source_artifact_label?: string;
};

export type ManualImportErrorCode =
  | "backend_unavailable"
  | "malformed_response"
  | "incompatible_response"
  | "unsafe_api_base_url";

export type AnalyticsHistoryErrorCode =
  | "backend_unavailable"
  | "malformed_response"
  | "incompatible_response"
  | "unsafe_api_base_url";

export type MatchJournalApiErrorCode =
  | "backend_unavailable"
  | "malformed_response"
  | "incompatible_response"
  | "unsafe_api_base_url";

export type MatchJournalStatus = "ok" | "degraded" | "empty" | "missing" | "unavailable" | "error";

export type MatchJournalContext = {
  journal_match_id?: string;
  journal_game_id?: string;
  parser_match_id?: string;
  parser_game_id?: string;
  game_number?: number;
  attachment_status?: string;
};

export type MatchJournalResponse = {
  object: typeof MATCH_JOURNAL_OBJECT;
  schema_version: typeof MATCH_JOURNAL_SCHEMA_VERSION;
  status: MatchJournalStatus;
  result: Record<string, unknown>;
  warnings: string[];
  errors: string[];
};

export type MatchJournalAttachedNoteRequest = {
  context: MatchJournalContext;
  note_scope: "match" | "game" | "sideboarding";
  note_text: string;
};

export type MatchJournalUnattachedNoteRequest = {
  note_scope: "unattached";
  note_text: string;
  author_label?: string;
  source_surface?: string;
  privacy_label?: string;
  note_format?: string;
  priority_label?: string;
};

export type MatchJournalNoteRequest = MatchJournalAttachedNoteRequest | MatchJournalUnattachedNoteRequest;

export type MatchJournalUnattachedNoteReadbackRequest = {
  journal_note_id: string;
  note_scope: "unattached";
};

export type MatchJournalOpponentLabelsRequest = {
  context: MatchJournalContext;
  archetype?: string;
  tier?: string;
};

export type MatchJournalReviewFlagRequest = {
  context: MatchJournalContext;
  flag_type: string;
  flag_status?: string;
  reason?: string;
  priority_label?: string;
};

export type MatchJournalExperimentLabelRequest = {
  context: MatchJournalContext;
  experiment_label: string;
};

export type MatchJournalDisplayCorrectionRequest = {
  context: MatchJournalContext;
  target_surface: "journal_display";
  target_field: string;
  proposed_value_label: string;
  original_value_label?: string;
  override_reason?: string;
  override_status?: string;
  effect_scope?: "journal_display_only";
};

export type AnalyticsHistoryStatus = "ok" | "empty" | "missing" | "unavailable" | "degraded" | "error";

export type AnalyticsHistoryStatusObject = {
  value_source: string;
  confidence: string;
  finality: string;
  drift_status: string;
  availability_status: string;
  source_parser_surface: string;
  source_fact_key: string;
  ingest_run_id: string;
};

export type AnalyticsHistoryDatabase = {
  display_path: string;
  exists: boolean;
  schema_status: string;
  status: string;
};

export type AnalyticsHistoryPagination = {
  limit: number;
  offset: number;
  returned: number;
};

export type AnalyticsHistorySummary = {
  row_count: number;
  degraded_row_count: number;
  unavailable_row_count: number;
  conflict_row_count: number;
};

export type EarlyGameHistorySummary = AnalyticsHistorySummary & {
  card_row_count: number;
};

export type ActionReviewSummary = EarlyGameHistorySummary & {
  review_required_row_count: number;
};

export type PlayDrawSplitSummary = {
  row_count: number;
  total_game_count: number;
  known_result_count: number;
  wins: number;
  losses: number;
  unknown_result_count: number;
  unavailable_result_count: number;
  degraded_result_count: number;
  small_sample_group_count: number;
};

export type Game1PostboardSplitSummary = {
  row_count: number;
  game1_row_count: number;
  postboard_row_count: number;
  known_result_count: number;
  unknown_result_count: number;
  degraded_row_count: number;
  unavailable_row_count: number;
  conflict_row_count: number;
};

export type MatchHistoryRow = {
  match_id: string;
  parser_match_key: string | null;
  match_started_at: string | null;
  match_completed_at: string | null;
  match_result: string | null;
  match_win: number | null;
  games_won: number | null;
  games_lost: number | null;
  total_games: number | null;
  game_win_rate: number | null;
  queue_name: string | null;
  format_name: string | null;
  event_id: string | null;
  match_status: AnalyticsHistoryStatusObject;
  result_status: AnalyticsHistoryStatusObject | null;
  context_status: AnalyticsHistoryStatusObject | null;
};

export type GameHistoryRow = {
  game_id: string;
  match_id: string;
  game_number: number;
  game_started_at: string | null;
  game_completed_at: string | null;
  local_result: string | null;
  winner_team_id: number | null;
  pre_postboard_label: string | null;
  play_draw: string | null;
  turn_count: number | null;
  game_duration_seconds: number | null;
  queue_name: string | null;
  format_name: string | null;
  event_id: string | null;
  game_status: AnalyticsHistoryStatusObject;
  result_status: AnalyticsHistoryStatusObject | null;
  context_status: AnalyticsHistoryStatusObject | null;
};

export type MatchHistoryResponse = {
  object: typeof MATCH_HISTORY_OBJECT;
  schema_version: typeof ANALYTICS_HISTORY_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: AnalyticsHistorySummary;
  rows: MatchHistoryRow[];
  warnings: string[];
  errors: string[];
};

export type GameHistoryResponse = {
  object: typeof GAME_HISTORY_OBJECT;
  schema_version: typeof ANALYTICS_HISTORY_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: AnalyticsHistorySummary;
  rows: GameHistoryRow[];
  warnings: string[];
  errors: string[];
};

export type OpeningHandCardRow = {
  opening_hand_card_id: string;
  card_position: number;
  grp_id: number | null;
  card_name: string | null;
  identity_hint_source: string | null;
  name_resolution_status: string | null;
  card_status: AnalyticsHistoryStatusObject;
};

export type OpeningHandHistoryRow = {
  opening_hand_id: string;
  match_id: string;
  game_id: string;
  game_number: number;
  hand_size: number | null;
  exact_card_count: number | null;
  local_result: string | null;
  play_draw: string | null;
  pre_postboard_label: string | null;
  match_result: string | null;
  match_win: number | null;
  queue_name: string | null;
  format_name: string | null;
  event_id: string | null;
  cards: OpeningHandCardRow[];
  opening_hand_status: AnalyticsHistoryStatusObject;
  game_status: AnalyticsHistoryStatusObject | null;
  game_result_status: AnalyticsHistoryStatusObject | null;
  match_result_status: AnalyticsHistoryStatusObject | null;
  context_status: AnalyticsHistoryStatusObject | null;
};

export type MulliganCardRow = {
  mulligan_card_id: string;
  card_position: number;
  card_action: "bottomed" | "discarded" | "unknown";
  grp_id: number | null;
  card_name: string | null;
  identity_hint_source: string | null;
  card_status: AnalyticsHistoryStatusObject;
};

export type MulliganHistoryRow = {
  mulligan_event_id: string;
  match_id: string;
  game_id: string;
  game_number: number;
  ordinal_or_count: string;
  mulligan_count: number | null;
  decision_detail: string | null;
  local_result: string | null;
  play_draw: string | null;
  pre_postboard_label: string | null;
  match_result: string | null;
  match_win: number | null;
  queue_name: string | null;
  format_name: string | null;
  event_id: string | null;
  cards: MulliganCardRow[];
  mulligan_status: AnalyticsHistoryStatusObject;
  game_status: AnalyticsHistoryStatusObject | null;
  game_result_status: AnalyticsHistoryStatusObject | null;
  match_result_status: AnalyticsHistoryStatusObject | null;
  context_status: AnalyticsHistoryStatusObject | null;
};

export type OpeningHandHistoryResponse = {
  object: typeof OPENING_HAND_HISTORY_OBJECT;
  schema_version: typeof EARLY_GAME_HISTORY_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: EarlyGameHistorySummary;
  rows: OpeningHandHistoryRow[];
  warnings: string[];
  errors: string[];
};

export type MulliganHistoryResponse = {
  object: typeof MULLIGAN_HISTORY_OBJECT;
  schema_version: typeof EARLY_GAME_HISTORY_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: EarlyGameHistorySummary;
  rows: MulliganHistoryRow[];
  warnings: string[];
  errors: string[];
};

export type GameplayActionCardRow = {
  gameplay_action_card_id: string;
  card_ordinal: number;
  instance_id: number | null;
  grp_id: number | null;
  observed_grp_id: number | null;
  overlay_grp_id: number | null;
  object_source_grp_id: number | null;
  identity_hint_source: string | null;
  card_name: string | null;
  display_name: string | null;
  name_resolution_status: string | null;
  enrichment_status: string | null;
  card_status: AnalyticsHistoryStatusObject;
};

export type GameplayActionReviewRow = {
  gameplay_action_id: string;
  match_id: string;
  game_id: string;
  game_number: number;
  timestamp: string | null;
  game_state_id: number | null;
  turn_number: number | null;
  action_type: string;
  actor_relation: string;
  from_zone_type: string | null;
  to_zone_type: string | null;
  source_status: string | null;
  annotation_context_label: string | null;
  raw_action_type_labels: string | null;
  annotation_type_labels: string | null;
  visible_in_log: boolean | null;
  card_count: number;
  grp_ids: number[];
  local_result: string | null;
  play_draw: string | null;
  pre_postboard_label: string | null;
  match_result: string | null;
  match_win: number | null;
  queue_name: string | null;
  format_name: string | null;
  event_id: string | null;
  cards: GameplayActionCardRow[];
  gameplay_action_status: AnalyticsHistoryStatusObject;
  game_status: AnalyticsHistoryStatusObject | null;
  game_result_status: AnalyticsHistoryStatusObject | null;
  match_result_status: AnalyticsHistoryStatusObject | null;
  context_status: AnalyticsHistoryStatusObject | null;
};

export type LinkedGameplayAction = {
  gameplay_action_id: string;
  turn_number: number | null;
  action_type: string;
  actor_relation: string;
  from_zone_type: string | null;
  to_zone_type: string | null;
  visible_in_log: boolean | null;
};

export type OpponentCardObservationCardRow = {
  opponent_card_observation_card_id: string;
  card_ordinal: number;
  grp_id: number | null;
  observed_grp_id: number | null;
  overlay_grp_id: number | null;
  object_source_grp_id: number | null;
  identity_hint_source: string | null;
  card_name: string | null;
  resolution_status: string | null;
  visibility: string | null;
  card_status: AnalyticsHistoryStatusObject;
};

export type OpponentCardObservationReviewRow = {
  opponent_card_observation_id: string;
  gameplay_action_id: string | null;
  match_id: string;
  game_id: string;
  game_number: number;
  timestamp: string | null;
  game_state_id: number | null;
  turn_number: number | null;
  actor_relation: string;
  actor_seat_id: number | null;
  local_seat_id: number | null;
  instance_id: number | null;
  grp_id: number | null;
  observed_grp_id: number | null;
  overlay_grp_id: number | null;
  object_source_grp_id: number | null;
  parent_id: number | null;
  identity_hint_source: string | null;
  card_name: string | null;
  display_name: string | null;
  resolution_status: string | null;
  name_resolution_source: string | null;
  action_type: string | null;
  cast_mode: string | null;
  source_evidence: string | null;
  evidence_status: string | null;
  visibility: string | null;
  from_zone_type: string | null;
  to_zone_type: string | null;
  degradation_flags: string[];
  review_required: boolean;
  linked_gameplay_action: LinkedGameplayAction | null;
  local_result: string | null;
  play_draw: string | null;
  pre_postboard_label: string | null;
  match_result: string | null;
  match_win: number | null;
  queue_name: string | null;
  format_name: string | null;
  event_id: string | null;
  cards: OpponentCardObservationCardRow[];
  opponent_card_observation_status: AnalyticsHistoryStatusObject;
  linked_gameplay_action_status: AnalyticsHistoryStatusObject | null;
  game_status: AnalyticsHistoryStatusObject | null;
  game_result_status: AnalyticsHistoryStatusObject | null;
  match_result_status: AnalyticsHistoryStatusObject | null;
  context_status: AnalyticsHistoryStatusObject | null;
};

export type GameplayActionReviewResponse = {
  object: typeof GAMEPLAY_ACTION_REVIEW_OBJECT;
  schema_version: typeof ACTION_REVIEW_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: ActionReviewSummary;
  rows: GameplayActionReviewRow[];
  warnings: string[];
  errors: string[];
};

export type OpponentCardObservationReviewResponse = {
  object: typeof OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT;
  schema_version: typeof ACTION_REVIEW_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: ActionReviewSummary;
  rows: OpponentCardObservationReviewRow[];
  warnings: string[];
  errors: string[];
};

export type PlayDrawSplitRow = {
  play_draw: string;
  game_count: number;
  known_result_count: number;
  wins: number;
  losses: number;
  unknown_result_count: number;
  unavailable_result_count: number;
  degraded_result_count: number;
  win_rate: number | null;
  sample_size_warning: string | null;
};

export type Game1PostboardSplitRow = {
  game_result_id: string;
  match_id: string;
  game_id: string;
  game_number: number;
  pre_postboard_label: string | null;
  local_result: string | null;
  play_draw: string | null;
  turn_count: number | null;
  game_duration_seconds: number | null;
  game_result_status: AnalyticsHistoryStatusObject;
};

export type PlayDrawSplitReviewResponse = {
  object: typeof PLAY_DRAW_SPLIT_REVIEW_OBJECT;
  schema_version: typeof SPLIT_REVIEW_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: PlayDrawSplitSummary;
  rows: PlayDrawSplitRow[];
  warnings: string[];
  errors: string[];
};

export type Game1PostboardSplitReviewResponse = {
  object: typeof GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT;
  schema_version: typeof SPLIT_REVIEW_SCHEMA_VERSION;
  status: AnalyticsHistoryStatus;
  database: AnalyticsHistoryDatabase;
  pagination: AnalyticsHistoryPagination;
  summary: Game1PostboardSplitSummary;
  rows: Game1PostboardSplitRow[];
  warnings: string[];
  errors: string[];
};
