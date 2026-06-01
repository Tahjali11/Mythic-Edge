import {
  ANALYTICS_HISTORY_SCHEMA_VERSION,
  GAME_HISTORY_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
  MANUAL_IMPORT_JOB_OBJECT,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  MATCH_HISTORY_OBJECT,
  SETUP_STATUS_OBJECT,
  SETUP_STATUS_SCHEMA_VERSION,
  type AnalyticsHistoryErrorCode,
  type AnalyticsHistoryStatus,
  type GameHistoryResponse,
  type ManualImportErrorCode,
  type ManualImportJob,
  type ManualImportRequest,
  type ManualImportUploadRequest,
  type MatchHistoryResponse,
  type SetupStatusErrorCode,
  type SetupStatusResponse
} from "./types";

const SETUP_STATUS_PATH = "/api/app/setup-status";
const MATCH_HISTORY_PATH = "/api/analytics/matches";
const GAME_HISTORY_PATH = "/api/analytics/games";
const MANUAL_IMPORT_PATH = "/api/imports/jsonl";
const MANUAL_IMPORT_UPLOAD_PATH = "/api/imports/jsonl/upload";
const MANUAL_IMPORT_JOB_PATH = "/api/imports/jobs";
const REQUIRED_SETUP_STATUS_FIELDS = [
  "object",
  "schema_version",
  "status",
  "paths",
  "config",
  "player_log",
  "analytics_database",
  "migrations",
  "runtime",
  "capabilities"
] as const;
const REQUIRED_MANUAL_IMPORT_JOB_FIELDS = [
  "object",
  "schema_version",
  "job_id",
  "status",
  "phase",
  "created_at",
  "started_at",
  "finished_at",
  "source",
  "adapter",
  "ingest",
  "database",
  "warnings",
  "errors"
] as const;
const REQUIRED_ANALYTICS_HISTORY_FIELDS = [
  "object",
  "schema_version",
  "status",
  "database",
  "pagination",
  "summary",
  "rows",
  "warnings",
  "errors"
] as const;

export class SetupStatusApiError extends Error {
  code: SetupStatusErrorCode;

  constructor(code: SetupStatusErrorCode, message: string) {
    super(message);
    this.name = "SetupStatusApiError";
    this.code = code;
  }
}

export class ManualImportApiError extends Error {
  code: ManualImportErrorCode;

  constructor(code: ManualImportErrorCode, message: string) {
    super(message);
    this.name = "ManualImportApiError";
    this.code = code;
  }
}

export class AnalyticsHistoryApiError extends Error {
  code: AnalyticsHistoryErrorCode;

  constructor(code: AnalyticsHistoryErrorCode, message: string) {
    super(message);
    this.name = "AnalyticsHistoryApiError";
    this.code = code;
  }
}

export function getApiBaseUrl(value: string | undefined = import.meta.env.VITE_MYTHIC_EDGE_API_BASE_URL): string {
  const trimmed = (value ?? "").trim().replace(/\/+$/, "");
  if (!trimmed) {
    return "";
  }

  let parsed: URL;
  try {
    parsed = new URL(trimmed);
  } catch {
    throw new SetupStatusApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }

  const isLoopback = parsed.protocol === "http:" && (parsed.hostname === "127.0.0.1" || parsed.hostname === "localhost");
  const port = Number(parsed.port);
  const hasValidPort = Number.isInteger(port) && port >= 1 && port <= 65535;
  const hasOnlyOrigin = parsed.pathname === "/" && parsed.search === "" && parsed.hash === "";
  if (!isLoopback || !hasValidPort || !hasOnlyOrigin) {
    throw new SetupStatusApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }

  return parsed.origin;
}

export async function fetchSetupStatus(fetchImpl: typeof fetch = fetch): Promise<SetupStatusResponse> {
  const baseUrl = getApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${SETUP_STATUS_PATH}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new SetupStatusApiError("backend_unavailable", "Backend setup status is unavailable.");
  }

  if (!response.ok) {
    throw new SetupStatusApiError("backend_unavailable", "Backend setup status is unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new SetupStatusApiError("malformed_response", "Backend setup status returned malformed JSON.");
  }

  return validateSetupStatusResponse(payload);
}

export async function fetchMatchHistory(fetchImpl: typeof fetch = fetch): Promise<MatchHistoryResponse> {
  return fetchAnalyticsHistory(
    MATCH_HISTORY_PATH,
    MATCH_HISTORY_OBJECT,
    validateMatchHistoryRows,
    fetchImpl
  ) as Promise<MatchHistoryResponse>;
}

export async function fetchGameHistory(fetchImpl: typeof fetch = fetch): Promise<GameHistoryResponse> {
  return fetchAnalyticsHistory(
    GAME_HISTORY_PATH,
    GAME_HISTORY_OBJECT,
    validateGameHistoryRows,
    fetchImpl
  ) as Promise<GameHistoryResponse>;
}

export async function submitManualJsonlImport(
  request: ManualImportRequest,
  fetchImpl: typeof fetch = fetch
): Promise<ManualImportJob> {
  const baseUrl = getManualImportApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${MANUAL_IMPORT_PATH}`, {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(request)
    });
  } catch {
    throw new ManualImportApiError("backend_unavailable", "Manual import backend is unavailable.");
  }

  if (!response.ok) {
    throw new ManualImportApiError("backend_unavailable", "Manual import backend is unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new ManualImportApiError("malformed_response", "Manual import returned malformed JSON.");
  }

  return validateManualImportJob(payload);
}

export async function submitManualJsonlUpload(
  request: ManualImportUploadRequest,
  fetchImpl: typeof fetch = fetch
): Promise<ManualImportJob> {
  const baseUrl = getManualImportApiBaseUrl();
  const formData = new FormData();
  for (const file of request.files) {
    formData.append("files", file);
  }
  if (request.source_artifact_label?.trim()) {
    formData.append("source_artifact_label", request.source_artifact_label.trim());
  }

  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${MANUAL_IMPORT_UPLOAD_PATH}`, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: formData
    });
  } catch {
    throw new ManualImportApiError("backend_unavailable", "Manual import backend is unavailable.");
  }

  if (!response.ok) {
    throw new ManualImportApiError("backend_unavailable", "Manual import backend is unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new ManualImportApiError("malformed_response", "Manual import returned malformed JSON.");
  }

  return validateManualImportJob(payload);
}

export async function fetchManualImportJob(jobId: string, fetchImpl: typeof fetch = fetch): Promise<ManualImportJob> {
  const baseUrl = getManualImportApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${MANUAL_IMPORT_JOB_PATH}/${encodeURIComponent(jobId)}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new ManualImportApiError("backend_unavailable", "Manual import job status is unavailable.");
  }

  if (!response.ok) {
    throw new ManualImportApiError("backend_unavailable", "Manual import job status is unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new ManualImportApiError("malformed_response", "Manual import job status returned malformed JSON.");
  }

  return validateManualImportJob(payload);
}

function validateSetupStatusResponse(payload: unknown): SetupStatusResponse {
  if (!isRecord(payload)) {
    throw new SetupStatusApiError("malformed_response", "Backend setup status must be a JSON object.");
  }

  for (const field of REQUIRED_SETUP_STATUS_FIELDS) {
    if (!(field in payload)) {
      throw new SetupStatusApiError("malformed_response", "Backend setup status is missing required fields.");
    }
  }

  if (payload.schema_version !== SETUP_STATUS_SCHEMA_VERSION) {
    throw new SetupStatusApiError(
      "incompatible_response",
      `Expected setup status schema ${SETUP_STATUS_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== SETUP_STATUS_OBJECT) {
    throw new SetupStatusApiError("malformed_response", "Backend setup status object is unsupported.");
  }

  if (
    typeof payload.status !== "string" ||
    !isRecord(payload.paths) ||
    !isRecord(payload.config) ||
    !isRecord(payload.player_log) ||
    !isRecord(payload.analytics_database) ||
    !isRecord(payload.migrations) ||
    !isRecord(payload.runtime) ||
    !isStringRecord(payload.capabilities)
  ) {
    throw new SetupStatusApiError("malformed_response", "Backend setup status has an unsupported shape.");
  }

  return payload as SetupStatusResponse;
}

async function fetchAnalyticsHistory(
  path: string,
  objectName: string,
  validateRows: (rows: unknown) => void,
  fetchImpl: typeof fetch
): Promise<MatchHistoryResponse | GameHistoryResponse> {
  const baseUrl = getAnalyticsHistoryApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${path}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new AnalyticsHistoryApiError("backend_unavailable", "Analytics history backend is unavailable.");
  }

  if (!response.ok) {
    throw new AnalyticsHistoryApiError("backend_unavailable", "Analytics history backend is unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history returned malformed JSON.");
  }

  return validateAnalyticsHistoryResponse(payload, objectName, validateRows);
}

function getAnalyticsHistoryApiBaseUrl(): string {
  try {
    return getApiBaseUrl();
  } catch {
    throw new AnalyticsHistoryApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }
}

function validateAnalyticsHistoryResponse(
  payload: unknown,
  objectName: string,
  validateRows: (rows: unknown) => void
): MatchHistoryResponse | GameHistoryResponse {
  if (!isRecord(payload)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history must be a JSON object.");
  }

  for (const field of REQUIRED_ANALYTICS_HISTORY_FIELDS) {
    if (!(field in payload)) {
      throw new AnalyticsHistoryApiError("malformed_response", "Analytics history is missing required fields.");
    }
  }

  if (payload.schema_version !== ANALYTICS_HISTORY_SCHEMA_VERSION) {
    throw new AnalyticsHistoryApiError(
      "incompatible_response",
      `Expected analytics history schema ${ANALYTICS_HISTORY_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== objectName) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history object is unsupported.");
  }

  if (
    !isAnalyticsHistoryStatus(payload.status) ||
    !isHistoryDatabase(payload.database) ||
    !isHistoryPagination(payload.pagination) ||
    !isHistorySummary(payload.summary) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history has an unsupported shape.");
  }

  validateRows(payload.rows);

  return payload as MatchHistoryResponse | GameHistoryResponse;
}

function isAnalyticsHistoryStatus(value: unknown): value is AnalyticsHistoryStatus {
  return (
    value === "ok" ||
    value === "empty" ||
    value === "missing" ||
    value === "unavailable" ||
    value === "degraded" ||
    value === "error"
  );
}

function validateMatchHistoryRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Match history rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.match_id !== "string" ||
      !isStringOrNull(row.parser_match_key) ||
      !isStringOrNull(row.match_started_at) ||
      !isStringOrNull(row.match_completed_at) ||
      !isStringOrNull(row.match_result) ||
      !isNumberOrNull(row.match_win) ||
      !isNumberOrNull(row.games_won) ||
      !isNumberOrNull(row.games_lost) ||
      !isNumberOrNull(row.total_games) ||
      !isNumberOrNull(row.game_win_rate) ||
      !isStringOrNull(row.queue_name) ||
      !isStringOrNull(row.format_name) ||
      !isStringOrNull(row.event_id) ||
      !isHistoryStatus(row.match_status) ||
      !isHistoryStatusOrNull(row.result_status) ||
      !isHistoryStatusOrNull(row.context_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Match history row has an unsupported shape.");
    }
  }
}

function validateGameHistoryRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Game history rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.game_id !== "string" ||
      typeof row.match_id !== "string" ||
      typeof row.game_number !== "number" ||
      !isStringOrNull(row.game_started_at) ||
      !isStringOrNull(row.game_completed_at) ||
      !isStringOrNull(row.local_result) ||
      !isNumberOrNull(row.winner_team_id) ||
      !isStringOrNull(row.pre_postboard_label) ||
      !isStringOrNull(row.play_draw) ||
      !isNumberOrNull(row.turn_count) ||
      !isNumberOrNull(row.game_duration_seconds) ||
      !isStringOrNull(row.queue_name) ||
      !isStringOrNull(row.format_name) ||
      !isStringOrNull(row.event_id) ||
      !isHistoryStatus(row.game_status) ||
      !isHistoryStatusOrNull(row.result_status) ||
      !isHistoryStatusOrNull(row.context_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Game history row has an unsupported shape.");
    }
  }
}

function getManualImportApiBaseUrl(): string {
  try {
    return getApiBaseUrl();
  } catch {
    throw new ManualImportApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }
}

function validateManualImportJob(payload: unknown): ManualImportJob {
  if (!isRecord(payload)) {
    throw new ManualImportApiError("malformed_response", "Manual import job must be a JSON object.");
  }

  for (const field of REQUIRED_MANUAL_IMPORT_JOB_FIELDS) {
    if (!(field in payload)) {
      throw new ManualImportApiError("malformed_response", "Manual import job is missing required fields.");
    }
  }

  if (payload.schema_version !== MANUAL_IMPORT_JOB_SCHEMA_VERSION) {
    throw new ManualImportApiError(
      "incompatible_response",
      `Expected manual import schema ${MANUAL_IMPORT_JOB_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== MANUAL_IMPORT_JOB_OBJECT) {
    throw new ManualImportApiError("malformed_response", "Manual import job object is unsupported.");
  }

  if (
    typeof payload.job_id !== "string" ||
    typeof payload.status !== "string" ||
    typeof payload.phase !== "string" ||
    typeof payload.created_at !== "string" ||
    typeof payload.started_at !== "string" ||
    typeof payload.finished_at !== "string" ||
    !isRecord(payload.source) ||
    !isRecord(payload.adapter) ||
    !isRecord(payload.ingest) ||
    !isRecord(payload.database) ||
    !Array.isArray(payload.warnings) ||
    !Array.isArray(payload.errors)
  ) {
    throw new ManualImportApiError("malformed_response", "Manual import job has an unsupported shape.");
  }

  validateManualImportAdapter(payload.adapter);

  return payload as ManualImportJob;
}

function validateManualImportAdapter(adapter: Record<string, unknown>): void {
  if (
    typeof adapter.status !== "string" ||
    typeof adapter.files_processed !== "number" ||
    typeof adapter.records_seen !== "number" ||
    typeof adapter.events_processed !== "number" ||
    typeof adapter.events_skipped !== "number" ||
    !isNumberRecord(adapter.unsupported_kind_counts) ||
    !isStringArray(adapter.warnings)
  ) {
    throw new ManualImportApiError("malformed_response", "Manual import adapter has an unsupported shape.");
  }

  const needsQuality = adapter.status === "succeeded" || adapter.status === "degraded" || adapter.status === "failed";
  if (needsQuality && !("quality" in adapter)) {
    throw new ManualImportApiError("malformed_response", "Manual import adapter is missing quality details.");
  }
  if ("quality" in adapter) {
    validateManualImportQuality(adapter.quality);
  }
  if ("source_artifacts" in adapter && !isSourceArtifacts(adapter.source_artifacts)) {
    throw new ManualImportApiError("malformed_response", "Manual import adapter has unsupported source artifacts.");
  }
}

function validateManualImportQuality(value: unknown): void {
  if (!isRecord(value)) {
    throw new ManualImportApiError("malformed_response", "Manual import quality must be a JSON object.");
  }

  if (value.schema_version !== LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION) {
    throw new ManualImportApiError(
      "incompatible_response",
      `Expected import quality schema ${LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION}.`
    );
  }

  if (value.object !== LEGACY_JSONL_IMPORT_QUALITY_OBJECT) {
    throw new ManualImportApiError("malformed_response", "Manual import quality object is unsupported.");
  }

  if (
    !isQualityStatus(value.quality_status) ||
    typeof value.records_seen !== "number" ||
    typeof value.events_processed !== "number" ||
    typeof value.events_skipped !== "number" ||
    !isNumberRecord(value.processed_kind_counts) ||
    !isNumberRecord(value.unsupported_kind_counts) ||
    !isNumberRecord(value.skipped_reason_counts) ||
    typeof value.blank_line_count !== "number" ||
    typeof value.duplicate_raw_hash_count !== "number" ||
    typeof value.unsupported_kind_skip_count !== "number" ||
    !isNumberRecord(value.output_gap_counts) ||
    !isNumberRecord(value.adapter_warning_counts) ||
    !isStringArray(value.adapter_warning_codes) ||
    !isStringArray(value.ingest_warning_codes) ||
    !isRoutingHints(value.routing_hints) ||
    !isPrivacySummary(value.privacy)
  ) {
    throw new ManualImportApiError("malformed_response", "Manual import quality has an unsupported shape.");
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isStringRecord(value: unknown): value is Record<string, string> {
  if (!isRecord(value)) {
    return false;
  }
  return Object.values(value).every((entry) => typeof entry === "string");
}

function isNumberRecord(value: unknown): value is Record<string, number> {
  if (!isRecord(value)) {
    return false;
  }
  return Object.values(value).every((entry) => typeof entry === "number");
}

function isStringOrNull(value: unknown): value is string | null {
  return typeof value === "string" || value === null;
}

function isNumberOrNull(value: unknown): value is number | null {
  return typeof value === "number" || value === null;
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((entry) => typeof entry === "string");
}

function isHistoryDatabase(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.display_path === "string" &&
    typeof value.exists === "boolean" &&
    typeof value.schema_status === "string" &&
    typeof value.status === "string"
  );
}

function isHistoryPagination(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.limit === "number" &&
    typeof value.offset === "number" &&
    typeof value.returned === "number"
  );
}

function isHistorySummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.row_count === "number" &&
    typeof value.degraded_row_count === "number" &&
    typeof value.unavailable_row_count === "number" &&
    typeof value.conflict_row_count === "number"
  );
}

function isHistoryStatus(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.value_source === "string" &&
    typeof value.confidence === "string" &&
    typeof value.finality === "string" &&
    typeof value.drift_status === "string" &&
    typeof value.availability_status === "string" &&
    typeof value.source_parser_surface === "string" &&
    typeof value.source_fact_key === "string" &&
    typeof value.ingest_run_id === "string"
  );
}

function isHistoryStatusOrNull(value: unknown): boolean {
  return value === null || isHistoryStatus(value);
}

function isQualityStatus(value: unknown): value is "complete" | "degraded" | "failed" {
  return value === "complete" || value === "degraded" || value === "failed";
}

function isRoutingHints(value: unknown): value is Array<Record<string, unknown>> {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.code === "string" &&
        typeof entry.category === "string" &&
        typeof entry.severity === "string" &&
        typeof entry.count === "number"
    )
  );
}

function isSourceArtifacts(value: unknown): value is Array<Record<string, unknown>> {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.batch_index === "number" &&
        typeof entry.source_artifact_label === "string" &&
        typeof entry.source_display_label === "string" &&
        typeof entry.status === "string" &&
        typeof entry.records_seen === "number" &&
        typeof entry.events_processed === "number" &&
        typeof entry.events_skipped === "number" &&
        isNumberRecord(entry.processed_kind_counts) &&
        isNumberRecord(entry.unsupported_kind_counts) &&
        isNumberRecord(entry.skipped_reason_counts) &&
        isStringArray(entry.adapter_warning_codes)
    )
  );
}

function isPrivacySummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    value.has_private_path_echo === false &&
    value.raw_payload_exposed === false &&
    value.raw_hash_exposed === false
  );
}
