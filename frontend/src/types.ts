export const SETUP_STATUS_OBJECT = "mythic_edge_local_app_setup_status";
export const SETUP_STATUS_SCHEMA_VERSION = "analytics_app_backend_setup_status.v1";
export const MANUAL_IMPORT_JOB_OBJECT = "mythic_edge_local_app_manual_jsonl_import_job";
export const MANUAL_IMPORT_JOB_SCHEMA_VERSION = "analytics_manual_jsonl_import_ui_job_status.v1";

export type SetupStatusTone =
  | "ok"
  | "degraded"
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

export type SetupStatusResponse = {
  object: typeof SETUP_STATUS_OBJECT;
  schema_version: typeof SETUP_STATUS_SCHEMA_VERSION;
  status: string;
  paths: SectionStatus;
  config: SectionStatus;
  player_log: SectionStatus;
  analytics_database: SectionStatus;
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

export type ManualImportStatus = "queued" | "running" | "succeeded" | "degraded" | "failed" | "rejected";

export type ManualImportSource = {
  source_kind: "saved_event_replay";
  source_artifact_label: string;
  source_display_label: string;
  source_file_extension: string;
  path_echoed: false;
};

export type ManualImportAdapter = {
  status: string;
  files_processed: number;
  records_seen: number;
  events_processed: number;
  events_skipped: number;
  unsupported_kind_counts: Record<string, number>;
  warnings: string[];
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

export type ManualImportRequest = {
  source_path: string;
  source_artifact_label?: string;
};

export type ManualImportErrorCode =
  | "backend_unavailable"
  | "malformed_response"
  | "incompatible_response"
  | "unsafe_api_base_url";
