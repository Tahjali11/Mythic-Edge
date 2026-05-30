export const SETUP_STATUS_OBJECT = "mythic_edge_local_app_setup_status";
export const SETUP_STATUS_SCHEMA_VERSION = "analytics_app_backend_setup_status.v1";

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
