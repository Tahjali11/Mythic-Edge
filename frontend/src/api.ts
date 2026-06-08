import {
  ACTION_REVIEW_SCHEMA_VERSION,
  ANALYTICS_DASHBOARD_MODULES_OBJECT,
  ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION,
  ANALYTICS_HISTORY_SCHEMA_VERSION,
  EARLY_GAME_HISTORY_SCHEMA_VERSION,
  ERROR_REPORT_PREVIEW_SCHEMA,
  GAME_HISTORY_OBJECT,
  GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT,
  GAMEPLAY_ACTION_REVIEW_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
  LIVE_PLAYER_LOG_STATUS_OBJECT,
  LIVE_CAPTURE_SCHEMA_VERSION,
  LIVE_CAPTURE_START_RESULT_OBJECT,
  LIVE_CAPTURE_STATUS_OBJECT,
  LIVE_CAPTURE_STOP_RESULT_OBJECT,
  LIVE_STATUS_SCHEMA_VERSION,
  LIVE_WATCHER_DIAGNOSTICS_OBJECT,
  LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION,
  LIVE_WATCHER_PROCESS_OBJECT,
  LIVE_WATCHER_PROCESS_SCHEMA_VERSION,
  LIVE_WATCHER_STATUS_OBJECT,
  MANUAL_IMPORT_JOB_OBJECT,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  MATCH_JOURNAL_OBJECT,
  MATCH_JOURNAL_SCHEMA_VERSION,
  MATCH_HISTORY_OBJECT,
  MULLIGAN_HISTORY_OBJECT,
  OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT,
  OPENING_HAND_HISTORY_OBJECT,
  PLAY_DRAW_SPLIT_REVIEW_OBJECT,
  SETUP_STATUS_OBJECT,
  SETUP_STATUS_SCHEMA_VERSION,
  SPLIT_REVIEW_SCHEMA_VERSION,
  type AnalyticsHistoryErrorCode,
  type AnalyticsHistoryStatus,
  type AnalyticsDashboardModulesResponse,
  type ErrorReportApiErrorCode,
  type ErrorReportPreviewRequest,
  type ErrorReportPreviewResponse,
  type Game1PostboardSplitReviewResponse,
  type GameHistoryResponse,
  type GameplayActionReviewResponse,
  type LivePlayerLogStatusResponse,
  type LiveCaptureStartResult,
  type LiveCaptureStatusResponse,
  type LiveCaptureStopResult,
  type LiveStatusErrorCode,
  type LiveWatcherDiagnosticsResponse,
  type LiveWatcherProcessStatusResponse,
  type LiveWatcherStatusResponse,
  type ManualImportErrorCode,
  type ManualImportJob,
  type ManualImportRequest,
  type ManualImportUploadRequest,
  type MatchJournalApiErrorCode,
  type MatchJournalContext,
  type MatchJournalDisplayCorrectionRequest,
  type MatchJournalExperimentLabelRequest,
  type MatchJournalNoteRequest,
  type MatchJournalOpponentLabelsRequest,
  type MatchJournalResponse,
  type MatchJournalReviewFlagRequest,
  type MatchJournalStatus,
  type MatchJournalUnattachedNoteReadbackRequest,
  type MatchHistoryResponse,
  type MulliganHistoryResponse,
  type OpeningHandHistoryResponse,
  type OpponentCardObservationReviewResponse,
  type PlayDrawSplitReviewResponse,
  type SetupStatusErrorCode,
  type SetupStatusResponse
} from "./types";

const SETUP_STATUS_PATH = "/api/app/setup-status";
const LIVE_PLAYER_LOG_STATUS_PATH = "/api/live/player-log/status";
const LIVE_WATCHER_STATUS_PATH = "/api/live/watcher/status";
const LIVE_WATCHER_PROCESS_STATUS_PATH = "/api/live/watcher/process";
const LIVE_WATCHER_DIAGNOSTICS_STATUS_PATH = "/api/live/watcher/diagnostics";
const LIVE_CAPTURE_STATUS_PATH = "/api/live/capture/status";
const LIVE_CAPTURE_START_PATH = "/api/live/capture/start";
const LIVE_CAPTURE_STOP_PATH = "/api/live/capture/stop";
const MATCH_HISTORY_PATH = "/api/analytics/matches";
const GAME_HISTORY_PATH = "/api/analytics/games";
const OPENING_HAND_HISTORY_PATH = "/api/analytics/opening-hands";
const MULLIGAN_HISTORY_PATH = "/api/analytics/mulligans";
const GAMEPLAY_ACTION_REVIEW_PATH = "/api/analytics/gameplay-actions";
const OPPONENT_CARD_OBSERVATION_REVIEW_PATH = "/api/analytics/opponent-card-observations";
const PLAY_DRAW_SPLIT_REVIEW_PATH = "/api/analytics/play-draw-splits";
const GAME1_POSTBOARD_SPLIT_REVIEW_PATH = "/api/analytics/game1-postboard-splits";
const ANALYTICS_DASHBOARD_MODULES_PATH = "/api/analytics/dashboard/modules";
const MANUAL_IMPORT_PATH = "/api/imports/jsonl";
const MANUAL_IMPORT_UPLOAD_PATH = "/api/imports/jsonl/upload";
const MANUAL_IMPORT_JOB_PATH = "/api/imports/jobs";
const MATCH_JOURNAL_PATH = "/api/journal";
const MATCH_JOURNAL_NOTES_PATH = "/api/journal/notes";
const MATCH_JOURNAL_OPPONENT_LABELS_PATH = "/api/journal/opponent-labels";
const MATCH_JOURNAL_REVIEW_FLAGS_PATH = "/api/journal/review-flags";
const MATCH_JOURNAL_EXPERIMENT_LABEL_PATH = "/api/journal/experiment-label";
const MATCH_JOURNAL_DISPLAY_CORRECTIONS_PATH = "/api/journal/display-corrections";
const ERROR_REPORT_PREVIEW_PATH = "/api/feedback/error-report/preview";
const REQUIRED_SETUP_STATUS_FIELDS = [
  "object",
  "schema_version",
  "status",
  "paths",
  "config",
  "player_log",
  "analytics_database",
  "match_journal",
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
const REQUIRED_ANALYTICS_DASHBOARD_MODULES_FIELDS = [
  "object",
  "schema_version",
  "status",
  "database",
  "modules",
  "custom_explorer",
  "warnings",
  "errors"
] as const;
const REQUIRED_MATCH_JOURNAL_FIELDS = ["object", "schema_version", "status", "result", "warnings", "errors"] as const;
const REQUIRED_ERROR_REPORT_PREVIEW_FIELDS = [
  "schema",
  "status",
  "issue_title",
  "issue_body_markdown",
  "included_diagnostic_categories",
  "excluded_private_data",
  "redaction_summary",
  "warnings",
  "next_recommended_role",
  "external_submission_enabled"
] as const;
const LIVE_WATCHER_PROCESS_PRECONDITION_KEYS = [
  "player_log_ready",
  "app_data_root_available",
  "state_directory_available",
  "single_instance_guard_available",
  "supervisor_target_defined",
  "external_transport_disabled",
  "live_sqlite_ingest_contract_present",
  "frontend_controls_authorized"
] as const;

export class SetupStatusApiError extends Error {
  code: SetupStatusErrorCode;

  constructor(code: SetupStatusErrorCode, message: string) {
    super(message);
    this.name = "SetupStatusApiError";
    this.code = code;
  }
}

export class LiveStatusApiError extends Error {
  code: LiveStatusErrorCode;

  constructor(code: LiveStatusErrorCode, message: string) {
    super(message);
    this.name = "LiveStatusApiError";
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

export class MatchJournalApiError extends Error {
  code: MatchJournalApiErrorCode;

  constructor(code: MatchJournalApiErrorCode, message: string) {
    super(message);
    this.name = "MatchJournalApiError";
    this.code = code;
  }
}

export class ErrorReportApiError extends Error {
  code: ErrorReportApiErrorCode;

  constructor(code: ErrorReportApiErrorCode, message: string) {
    super(message);
    this.name = "ErrorReportApiError";
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

export async function previewErrorReport(
  request: ErrorReportPreviewRequest,
  fetchImpl: typeof fetch = fetch
): Promise<ErrorReportPreviewResponse> {
  const baseUrl = getErrorReportApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${ERROR_REPORT_PREVIEW_PATH}`, {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(request)
    });
  } catch {
    throw new ErrorReportApiError("backend_unavailable", "Error report preview is unavailable.");
  }

  if (!response.ok) {
    throw new ErrorReportApiError("backend_unavailable", "Error report preview is unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new ErrorReportApiError("malformed_response", "Error report preview returned malformed JSON.");
  }

  return validateErrorReportPreviewResponse(payload);
}

export async function fetchLivePlayerLogStatus(fetchImpl: typeof fetch = fetch): Promise<LivePlayerLogStatusResponse> {
  const payload = await fetchLiveStatusPayload(LIVE_PLAYER_LOG_STATUS_PATH, "Live Player.log status", fetchImpl);
  return validateLivePlayerLogStatusResponse(payload);
}

export async function fetchLiveWatcherStatus(fetchImpl: typeof fetch = fetch): Promise<LiveWatcherStatusResponse> {
  const payload = await fetchLiveStatusPayload(LIVE_WATCHER_STATUS_PATH, "Live watcher status", fetchImpl);
  return validateLiveWatcherStatusResponse(payload);
}

export async function fetchLiveWatcherProcessStatus(
  fetchImpl: typeof fetch = fetch
): Promise<LiveWatcherProcessStatusResponse> {
  const payload = await fetchLiveStatusPayload(
    LIVE_WATCHER_PROCESS_STATUS_PATH,
    "Live watcher process status",
    fetchImpl
  );
  return validateLiveWatcherProcessStatusResponse(payload);
}

export async function fetchLiveWatcherDiagnosticsStatus(
  fetchImpl: typeof fetch = fetch
): Promise<LiveWatcherDiagnosticsResponse> {
  const payload = await fetchLiveStatusPayload(
    LIVE_WATCHER_DIAGNOSTICS_STATUS_PATH,
    "Live watcher diagnostics",
    fetchImpl
  );
  return validateLiveWatcherDiagnosticsResponse(payload);
}

export async function fetchLiveCaptureStatus(fetchImpl: typeof fetch = fetch): Promise<LiveCaptureStatusResponse> {
  const payload = await fetchLiveStatusPayload(LIVE_CAPTURE_STATUS_PATH, "Live capture status", fetchImpl);
  return validateLiveCaptureStatusResponse(payload);
}

export async function startLiveCapture(fetchImpl: typeof fetch = fetch): Promise<LiveCaptureStartResult> {
  const payload = await postLiveCaptureControl(LIVE_CAPTURE_START_PATH, "Start capture", fetchImpl);
  return validateLiveCaptureStartResult(payload);
}

export async function stopLiveCapture(fetchImpl: typeof fetch = fetch): Promise<LiveCaptureStopResult> {
  const payload = await postLiveCaptureControl(LIVE_CAPTURE_STOP_PATH, "Stop capture", fetchImpl);
  return validateLiveCaptureStopResult(payload);
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

export async function fetchOpeningHandHistory(fetchImpl: typeof fetch = fetch): Promise<OpeningHandHistoryResponse> {
  return fetchEarlyGameHistory(
    OPENING_HAND_HISTORY_PATH,
    OPENING_HAND_HISTORY_OBJECT,
    validateOpeningHandHistoryRows,
    fetchImpl
  ) as Promise<OpeningHandHistoryResponse>;
}

export async function fetchMulliganHistory(fetchImpl: typeof fetch = fetch): Promise<MulliganHistoryResponse> {
  return fetchEarlyGameHistory(
    MULLIGAN_HISTORY_PATH,
    MULLIGAN_HISTORY_OBJECT,
    validateMulliganHistoryRows,
    fetchImpl
  ) as Promise<MulliganHistoryResponse>;
}

export async function fetchGameplayActionReview(fetchImpl: typeof fetch = fetch): Promise<GameplayActionReviewResponse> {
  return fetchActionReviewHistory(
    GAMEPLAY_ACTION_REVIEW_PATH,
    GAMEPLAY_ACTION_REVIEW_OBJECT,
    validateGameplayActionReviewRows,
    fetchImpl
  ) as Promise<GameplayActionReviewResponse>;
}

export async function fetchOpponentCardObservationReview(
  fetchImpl: typeof fetch = fetch
): Promise<OpponentCardObservationReviewResponse> {
  return fetchActionReviewHistory(
    OPPONENT_CARD_OBSERVATION_REVIEW_PATH,
    OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT,
    validateOpponentCardObservationReviewRows,
    fetchImpl
  ) as Promise<OpponentCardObservationReviewResponse>;
}

export async function fetchPlayDrawSplitReview(fetchImpl: typeof fetch = fetch): Promise<PlayDrawSplitReviewResponse> {
  return fetchSplitReviewHistory(
    PLAY_DRAW_SPLIT_REVIEW_PATH,
    PLAY_DRAW_SPLIT_REVIEW_OBJECT,
    isPlayDrawSplitSummary,
    validatePlayDrawSplitRows,
    fetchImpl
  ) as Promise<PlayDrawSplitReviewResponse>;
}

export async function fetchGame1PostboardSplitReview(
  fetchImpl: typeof fetch = fetch
): Promise<Game1PostboardSplitReviewResponse> {
  return fetchSplitReviewHistory(
    GAME1_POSTBOARD_SPLIT_REVIEW_PATH,
    GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT,
    isGame1PostboardSplitSummary,
    validateGame1PostboardSplitRows,
    fetchImpl
  ) as Promise<Game1PostboardSplitReviewResponse>;
}

export async function fetchAnalyticsDashboardModules(
  fetchImpl: typeof fetch = fetch
): Promise<AnalyticsDashboardModulesResponse> {
  const baseUrl = getAnalyticsHistoryApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${ANALYTICS_DASHBOARD_MODULES_PATH}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new AnalyticsHistoryApiError("backend_unavailable", "Analytics dashboard modules are unavailable.");
  }

  if (!response.ok) {
    throw new AnalyticsHistoryApiError("backend_unavailable", "Analytics dashboard modules are unavailable.");
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics dashboard modules returned malformed JSON.");
  }

  return validateAnalyticsDashboardModulesResponse(payload);
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

export async function fetchMatchJournal(
  context: MatchJournalContext,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  const baseUrl = getMatchJournalApiBaseUrl();
  const params = new URLSearchParams();
  if (context.journal_match_id) {
    params.set("journal_match_id", context.journal_match_id);
  }
  if (context.journal_game_id) {
    params.set("journal_game_id", context.journal_game_id);
  }
  if (context.parser_match_id) {
    params.set("parser_match_id", context.parser_match_id);
  }
  if (context.parser_game_id) {
    params.set("parser_game_id", context.parser_game_id);
  }
  if (typeof context.game_number === "number") {
    params.set("game_number", String(context.game_number));
  }
  if (context.attachment_status) {
    params.set("attachment_status", context.attachment_status);
  }

  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${MATCH_JOURNAL_PATH}?${params.toString()}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new MatchJournalApiError("backend_unavailable", "Match Journal backend is unavailable.");
  }

  return parseMatchJournalResponse(response);
}

export async function submitMatchJournalNote(
  request: MatchJournalNoteRequest,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  return postMatchJournal(MATCH_JOURNAL_NOTES_PATH, request, fetchImpl);
}

export async function fetchMatchJournalUnattachedNote(
  request: MatchJournalUnattachedNoteReadbackRequest,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  const baseUrl = getMatchJournalApiBaseUrl();
  const params = new URLSearchParams();
  params.set("journal_note_id", request.journal_note_id);
  params.set("note_scope", request.note_scope);

  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${MATCH_JOURNAL_NOTES_PATH}?${params.toString()}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new MatchJournalApiError("backend_unavailable", "Match Journal backend is unavailable.");
  }

  return parseMatchJournalResponse(response);
}

export async function submitMatchJournalOpponentLabels(
  request: MatchJournalOpponentLabelsRequest,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  return postMatchJournal(MATCH_JOURNAL_OPPONENT_LABELS_PATH, request, fetchImpl);
}

export async function submitMatchJournalReviewFlag(
  request: MatchJournalReviewFlagRequest,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  return postMatchJournal(MATCH_JOURNAL_REVIEW_FLAGS_PATH, request, fetchImpl);
}

export async function submitMatchJournalExperimentLabel(
  request: MatchJournalExperimentLabelRequest,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  return postMatchJournal(MATCH_JOURNAL_EXPERIMENT_LABEL_PATH, request, fetchImpl);
}

export async function submitMatchJournalDisplayCorrection(
  request: MatchJournalDisplayCorrectionRequest,
  fetchImpl: typeof fetch = fetch
): Promise<MatchJournalResponse> {
  return postMatchJournal(MATCH_JOURNAL_DISPLAY_CORRECTIONS_PATH, request, fetchImpl);
}

async function postMatchJournal(
  path: string,
  request: object,
  fetchImpl: typeof fetch
): Promise<MatchJournalResponse> {
  const baseUrl = getMatchJournalApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${path}`, {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify(request)
    });
  } catch {
    throw new MatchJournalApiError("backend_unavailable", "Match Journal backend is unavailable.");
  }

  return parseMatchJournalResponse(response);
}

async function parseMatchJournalResponse(response: Response): Promise<MatchJournalResponse> {
  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    throw new MatchJournalApiError("malformed_response", "Match Journal returned malformed JSON.");
  }

  const journal = validateMatchJournalResponse(payload);
  if (!response.ok && journal.errors.length === 0) {
    throw new MatchJournalApiError("malformed_response", "Match Journal error response is missing an error code.");
  }
  return journal;
}

async function fetchLiveStatusPayload(
  path: string,
  label: string,
  fetchImpl: typeof fetch
): Promise<unknown> {
  const baseUrl = getLiveStatusApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${path}`, {
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new LiveStatusApiError("backend_unavailable", `${label} is unavailable.`);
  }

  if (!response.ok) {
    throw new LiveStatusApiError("backend_unavailable", `${label} is unavailable.`);
  }

  try {
    return await response.json();
  } catch {
    throw new LiveStatusApiError("malformed_response", `${label} returned malformed JSON.`);
  }
}

async function postLiveCaptureControl(
  path: string,
  label: string,
  fetchImpl: typeof fetch,
): Promise<unknown> {
  const baseUrl = getApiBaseUrl();
  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}${path}`, {
      method: "POST",
      headers: { Accept: "application/json" }
    });
  } catch {
    throw new LiveStatusApiError("backend_unavailable", `${label} is unavailable.`);
  }

  if (!response.ok) {
    throw new LiveStatusApiError("backend_unavailable", `${label} is unavailable.`);
  }

  try {
    return await response.json();
  } catch {
    throw new LiveStatusApiError("malformed_response", `${label} returned malformed JSON.`);
  }
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
    !isRecord(payload.match_journal) ||
    !isRecord(payload.migrations) ||
    !isRecord(payload.runtime) ||
    !isStringRecord(payload.capabilities)
  ) {
    throw new SetupStatusApiError("malformed_response", "Backend setup status has an unsupported shape.");
  }

  return payload as SetupStatusResponse;
}

function validateLivePlayerLogStatusResponse(payload: unknown): LivePlayerLogStatusResponse {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Live Player.log status must be a JSON object.");
  }
  if (payload.schema_version !== LIVE_STATUS_SCHEMA_VERSION) {
    throw new LiveStatusApiError(
      "incompatible_response",
      `Expected live status schema ${LIVE_STATUS_SCHEMA_VERSION}.`
    );
  }
  if (payload.object !== LIVE_PLAYER_LOG_STATUS_OBJECT) {
    throw new LiveStatusApiError("malformed_response", "Live Player.log status object is unsupported.");
  }
  if (
    typeof payload.status !== "string" ||
    !isLivePlayerLogSummary(payload.player_log) ||
    !isStringArray(payload.diagnostics) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Live Player.log status has an unsupported shape.");
  }
  return payload as LivePlayerLogStatusResponse;
}

function validateLiveWatcherStatusResponse(payload: unknown): LiveWatcherStatusResponse {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Live watcher status must be a JSON object.");
  }
  if (payload.schema_version !== LIVE_STATUS_SCHEMA_VERSION) {
    throw new LiveStatusApiError(
      "incompatible_response",
      `Expected live status schema ${LIVE_STATUS_SCHEMA_VERSION}.`
    );
  }
  if (payload.object !== LIVE_WATCHER_STATUS_OBJECT) {
    throw new LiveStatusApiError("malformed_response", "Live watcher status object is unsupported.");
  }
  if (
    typeof payload.status !== "string" ||
    !isLiveWatcherSummary(payload.watcher) ||
    !isLivePlayerLogSummary(payload.player_log) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Live watcher status has an unsupported shape.");
  }
  return payload as LiveWatcherStatusResponse;
}

function validateLiveWatcherProcessStatusResponse(payload: unknown): LiveWatcherProcessStatusResponse {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Live watcher process status must be a JSON object.");
  }
  if (payload.schema_version !== LIVE_WATCHER_PROCESS_SCHEMA_VERSION) {
    throw new LiveStatusApiError(
      "incompatible_response",
      `Expected live watcher process schema ${LIVE_WATCHER_PROCESS_SCHEMA_VERSION}.`
    );
  }
  if (payload.object !== LIVE_WATCHER_PROCESS_OBJECT) {
    throw new LiveStatusApiError("malformed_response", "Live watcher process status object is unsupported.");
  }
  if (
    typeof payload.status !== "string" ||
    !isLiveWatcherProcessControl(payload.process_control) ||
    !isLiveWatcherProcessSummary(payload.watcher) ||
    !isRecord(payload.player_log) ||
    !isPreconditions(payload.preconditions) ||
    !isLiveWatcherProcessState(payload.state) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Live watcher process status has an unsupported shape.");
  }
  return payload as LiveWatcherProcessStatusResponse;
}

function validateLiveWatcherDiagnosticsResponse(payload: unknown): LiveWatcherDiagnosticsResponse {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Live watcher diagnostics must be a JSON object.");
  }
  if (payload.schema_version !== LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION) {
    throw new LiveStatusApiError(
      "incompatible_response",
      `Expected live watcher diagnostics schema ${LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION}.`
    );
  }
  if (payload.object !== LIVE_WATCHER_DIAGNOSTICS_OBJECT) {
    throw new LiveStatusApiError("malformed_response", "Live watcher diagnostics object is unsupported.");
  }
  if (
    typeof payload.status !== "string" ||
    payload.mode !== "read_only_composition" ||
    !isLiveWatcherDiagnosticsSummary(payload.summary) ||
    !isLiveWatcherDiagnosticsEntries(payload.diagnostics) ||
    !isRecord(payload.sources) ||
    !isLiveWatcherDiagnosticsPrivacy(payload.privacy) ||
    !isLiveWatcherDiagnosticsCapabilities(payload.capabilities) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Live watcher diagnostics has an unsupported shape.");
  }
  return payload as LiveWatcherDiagnosticsResponse;
}

function validateLiveCaptureStatusResponse(payload: unknown): LiveCaptureStatusResponse {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Live capture status must be a JSON object.");
  }
  if (payload.schema_version !== LIVE_CAPTURE_SCHEMA_VERSION) {
    throw new LiveStatusApiError(
      "incompatible_response",
      `Expected live capture schema ${LIVE_CAPTURE_SCHEMA_VERSION}.`
    );
  }
  if (payload.object !== LIVE_CAPTURE_STATUS_OBJECT) {
    throw new LiveStatusApiError("malformed_response", "Live capture status object is unsupported.");
  }
  if (
    typeof payload.status !== "string" ||
    payload.mode !== "explicit_operator_control" ||
    !isLiveCaptureSummary(payload.capture) ||
    !isLiveCapturePreconditions(payload.preconditions) ||
    !isLiveCaptureState(payload.state) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Live capture status has an unsupported shape.");
  }
  return payload as LiveCaptureStatusResponse;
}

function validateLiveCaptureStartResult(payload: unknown): LiveCaptureStartResult {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Start capture result must be a JSON object.");
  }
  if (
    payload.object !== LIVE_CAPTURE_START_RESULT_OBJECT ||
    payload.schema_version !== LIVE_CAPTURE_SCHEMA_VERSION ||
    typeof payload.status !== "string" ||
    typeof payload.accepted !== "boolean" ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Start capture result has an unsupported shape.");
  }
  const captureStatus = validateLiveCaptureStatusResponse(payload.capture_status);
  return { ...(payload as Omit<LiveCaptureStartResult, "capture_status">), capture_status: captureStatus };
}

function validateLiveCaptureStopResult(payload: unknown): LiveCaptureStopResult {
  if (!isRecord(payload)) {
    throw new LiveStatusApiError("malformed_response", "Stop capture result must be a JSON object.");
  }
  if (
    payload.object !== LIVE_CAPTURE_STOP_RESULT_OBJECT ||
    payload.schema_version !== LIVE_CAPTURE_SCHEMA_VERSION ||
    typeof payload.status !== "string" ||
    typeof payload.accepted !== "boolean" ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new LiveStatusApiError("malformed_response", "Stop capture result has an unsupported shape.");
  }
  const captureStatus = validateLiveCaptureStatusResponse(payload.capture_status);
  return { ...(payload as Omit<LiveCaptureStopResult, "capture_status">), capture_status: captureStatus };
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

async function fetchEarlyGameHistory(
  path: string,
  objectName: string,
  validateRows: (rows: unknown) => void,
  fetchImpl: typeof fetch
): Promise<OpeningHandHistoryResponse | MulliganHistoryResponse> {
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

  return validateEarlyGameHistoryResponse(payload, objectName, validateRows);
}

async function fetchActionReviewHistory(
  path: string,
  objectName: string,
  validateRows: (rows: unknown) => void,
  fetchImpl: typeof fetch
): Promise<GameplayActionReviewResponse | OpponentCardObservationReviewResponse> {
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

  return validateActionReviewHistoryResponse(payload, objectName, validateRows);
}

async function fetchSplitReviewHistory(
  path: string,
  objectName: string,
  validateSummary: (value: unknown) => boolean,
  validateRows: (rows: unknown) => void,
  fetchImpl: typeof fetch
): Promise<PlayDrawSplitReviewResponse | Game1PostboardSplitReviewResponse> {
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

  return validateSplitReviewHistoryResponse(payload, objectName, validateSummary, validateRows);
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

function validateEarlyGameHistoryResponse(
  payload: unknown,
  objectName: string,
  validateRows: (rows: unknown) => void
): OpeningHandHistoryResponse | MulliganHistoryResponse {
  if (!isRecord(payload)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history must be a JSON object.");
  }

  for (const field of REQUIRED_ANALYTICS_HISTORY_FIELDS) {
    if (!(field in payload)) {
      throw new AnalyticsHistoryApiError("malformed_response", "Analytics history is missing required fields.");
    }
  }

  if (payload.schema_version !== EARLY_GAME_HISTORY_SCHEMA_VERSION) {
    throw new AnalyticsHistoryApiError(
      "incompatible_response",
      `Expected analytics history schema ${EARLY_GAME_HISTORY_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== objectName) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history object is unsupported.");
  }

  if (
    !isAnalyticsHistoryStatus(payload.status) ||
    !isHistoryDatabase(payload.database) ||
    !isHistoryPagination(payload.pagination) ||
    !isEarlyGameHistorySummary(payload.summary) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history has an unsupported shape.");
  }

  validateRows(payload.rows);

  return payload as OpeningHandHistoryResponse | MulliganHistoryResponse;
}

function validateActionReviewHistoryResponse(
  payload: unknown,
  objectName: string,
  validateRows: (rows: unknown) => void
): GameplayActionReviewResponse | OpponentCardObservationReviewResponse {
  if (!isRecord(payload)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history must be a JSON object.");
  }

  for (const field of REQUIRED_ANALYTICS_HISTORY_FIELDS) {
    if (!(field in payload)) {
      throw new AnalyticsHistoryApiError("malformed_response", "Analytics history is missing required fields.");
    }
  }

  if (payload.schema_version !== ACTION_REVIEW_SCHEMA_VERSION) {
    throw new AnalyticsHistoryApiError(
      "incompatible_response",
      `Expected analytics history schema ${ACTION_REVIEW_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== objectName) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history object is unsupported.");
  }

  if (
    !isAnalyticsHistoryStatus(payload.status) ||
    !isHistoryDatabase(payload.database) ||
    !isHistoryPagination(payload.pagination) ||
    !isActionReviewSummary(payload.summary) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history has an unsupported shape.");
  }

  validateRows(payload.rows);

  return payload as GameplayActionReviewResponse | OpponentCardObservationReviewResponse;
}

function validateSplitReviewHistoryResponse(
  payload: unknown,
  objectName: string,
  validateSummary: (value: unknown) => boolean,
  validateRows: (rows: unknown) => void
): PlayDrawSplitReviewResponse | Game1PostboardSplitReviewResponse {
  if (!isRecord(payload)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history must be a JSON object.");
  }

  for (const field of REQUIRED_ANALYTICS_HISTORY_FIELDS) {
    if (!(field in payload)) {
      throw new AnalyticsHistoryApiError("malformed_response", "Analytics history is missing required fields.");
    }
  }

  if (payload.schema_version !== SPLIT_REVIEW_SCHEMA_VERSION) {
    throw new AnalyticsHistoryApiError(
      "incompatible_response",
      `Expected analytics history schema ${SPLIT_REVIEW_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== objectName) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history object is unsupported.");
  }

  if (
    !isAnalyticsHistoryStatus(payload.status) ||
    !isHistoryDatabase(payload.database) ||
    !isHistoryPagination(payload.pagination) ||
    !validateSummary(payload.summary) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics history has an unsupported shape.");
  }

  validateRows(payload.rows);

  return payload as PlayDrawSplitReviewResponse | Game1PostboardSplitReviewResponse;
}

function validateAnalyticsDashboardModulesResponse(payload: unknown): AnalyticsDashboardModulesResponse {
  if (!isRecord(payload)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics dashboard modules must be a JSON object.");
  }

  for (const field of REQUIRED_ANALYTICS_DASHBOARD_MODULES_FIELDS) {
    if (!(field in payload)) {
      throw new AnalyticsHistoryApiError("malformed_response", "Analytics dashboard modules are missing required fields.");
    }
  }

  if (payload.schema_version !== ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION) {
    throw new AnalyticsHistoryApiError(
      "incompatible_response",
      `Expected analytics dashboard schema ${ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== ANALYTICS_DASHBOARD_MODULES_OBJECT) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics dashboard modules object is unsupported.");
  }

  if (
    !isAnalyticsHistoryStatus(payload.status) ||
    !isHistoryDatabase(payload.database) ||
    !isAnalyticsDashboardModules(payload.modules) ||
    !isAnalyticsDashboardCustomExplorer(payload.custom_explorer) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new AnalyticsHistoryApiError("malformed_response", "Analytics dashboard modules have an unsupported shape.");
  }

  return payload as AnalyticsDashboardModulesResponse;
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

function validateOpeningHandHistoryRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Opening hand history rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.opening_hand_id !== "string" ||
      typeof row.match_id !== "string" ||
      typeof row.game_id !== "string" ||
      typeof row.game_number !== "number" ||
      !isNumberOrNull(row.hand_size) ||
      !isNumberOrNull(row.exact_card_count) ||
      !isStringOrNull(row.local_result) ||
      !isStringOrNull(row.play_draw) ||
      !isStringOrNull(row.pre_postboard_label) ||
      !isStringOrNull(row.match_result) ||
      !isNumberOrNull(row.match_win) ||
      !isStringOrNull(row.queue_name) ||
      !isStringOrNull(row.format_name) ||
      !isStringOrNull(row.event_id) ||
      !isOpeningHandCards(row.cards) ||
      !isHistoryStatus(row.opening_hand_status) ||
      !isHistoryStatusOrNull(row.game_status) ||
      !isHistoryStatusOrNull(row.game_result_status) ||
      !isHistoryStatusOrNull(row.match_result_status) ||
      !isHistoryStatusOrNull(row.context_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Opening hand history row has an unsupported shape.");
    }
  }
}

function validateMulliganHistoryRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Mulligan history rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.mulligan_event_id !== "string" ||
      typeof row.match_id !== "string" ||
      typeof row.game_id !== "string" ||
      typeof row.game_number !== "number" ||
      typeof row.ordinal_or_count !== "string" ||
      !isNumberOrNull(row.mulligan_count) ||
      !isStringOrNull(row.decision_detail) ||
      !isStringOrNull(row.local_result) ||
      !isStringOrNull(row.play_draw) ||
      !isStringOrNull(row.pre_postboard_label) ||
      !isStringOrNull(row.match_result) ||
      !isNumberOrNull(row.match_win) ||
      !isStringOrNull(row.queue_name) ||
      !isStringOrNull(row.format_name) ||
      !isStringOrNull(row.event_id) ||
      !isMulliganCards(row.cards) ||
      !isHistoryStatus(row.mulligan_status) ||
      !isHistoryStatusOrNull(row.game_status) ||
      !isHistoryStatusOrNull(row.game_result_status) ||
      !isHistoryStatusOrNull(row.match_result_status) ||
      !isHistoryStatusOrNull(row.context_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Mulligan history row has an unsupported shape.");
    }
  }
}

function validateGameplayActionReviewRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Gameplay action rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.gameplay_action_id !== "string" ||
      typeof row.match_id !== "string" ||
      typeof row.game_id !== "string" ||
      typeof row.game_number !== "number" ||
      !isStringOrNull(row.timestamp) ||
      !isNumberOrNull(row.game_state_id) ||
      !isNumberOrNull(row.turn_number) ||
      typeof row.action_type !== "string" ||
      typeof row.actor_relation !== "string" ||
      !isStringOrNull(row.from_zone_type) ||
      !isStringOrNull(row.to_zone_type) ||
      !isStringOrNull(row.source_status) ||
      !isStringOrNull(row.annotation_context_label) ||
      !isStringOrNull(row.raw_action_type_labels) ||
      !isStringOrNull(row.annotation_type_labels) ||
      !isBooleanOrNull(row.visible_in_log) ||
      typeof row.card_count !== "number" ||
      !isNumberArray(row.grp_ids) ||
      !isStringOrNull(row.local_result) ||
      !isStringOrNull(row.play_draw) ||
      !isStringOrNull(row.pre_postboard_label) ||
      !isStringOrNull(row.match_result) ||
      !isNumberOrNull(row.match_win) ||
      !isStringOrNull(row.queue_name) ||
      !isStringOrNull(row.format_name) ||
      !isStringOrNull(row.event_id) ||
      !isGameplayActionCards(row.cards) ||
      !isHistoryStatus(row.gameplay_action_status) ||
      !isHistoryStatusOrNull(row.game_status) ||
      !isHistoryStatusOrNull(row.game_result_status) ||
      !isHistoryStatusOrNull(row.match_result_status) ||
      !isHistoryStatusOrNull(row.context_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Gameplay action row has an unsupported shape.");
    }
  }
}

function validateOpponentCardObservationReviewRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Opponent observation rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.opponent_card_observation_id !== "string" ||
      !isStringOrNull(row.gameplay_action_id) ||
      typeof row.match_id !== "string" ||
      typeof row.game_id !== "string" ||
      typeof row.game_number !== "number" ||
      !isStringOrNull(row.timestamp) ||
      !isNumberOrNull(row.game_state_id) ||
      !isNumberOrNull(row.turn_number) ||
      typeof row.actor_relation !== "string" ||
      !isNumberOrNull(row.actor_seat_id) ||
      !isNumberOrNull(row.local_seat_id) ||
      !isNumberOrNull(row.instance_id) ||
      !isNumberOrNull(row.grp_id) ||
      !isNumberOrNull(row.observed_grp_id) ||
      !isNumberOrNull(row.overlay_grp_id) ||
      !isNumberOrNull(row.object_source_grp_id) ||
      !isNumberOrNull(row.parent_id) ||
      !isStringOrNull(row.identity_hint_source) ||
      !isStringOrNull(row.card_name) ||
      !isStringOrNull(row.display_name) ||
      !isStringOrNull(row.resolution_status) ||
      !isStringOrNull(row.name_resolution_source) ||
      !isStringOrNull(row.action_type) ||
      !isStringOrNull(row.cast_mode) ||
      !isStringOrNull(row.source_evidence) ||
      !isStringOrNull(row.evidence_status) ||
      !isStringOrNull(row.visibility) ||
      !isStringOrNull(row.from_zone_type) ||
      !isStringOrNull(row.to_zone_type) ||
      !isStringArray(row.degradation_flags) ||
      typeof row.review_required !== "boolean" ||
      !isLinkedGameplayActionOrNull(row.linked_gameplay_action) ||
      !isStringOrNull(row.local_result) ||
      !isStringOrNull(row.play_draw) ||
      !isStringOrNull(row.pre_postboard_label) ||
      !isStringOrNull(row.match_result) ||
      !isNumberOrNull(row.match_win) ||
      !isStringOrNull(row.queue_name) ||
      !isStringOrNull(row.format_name) ||
      !isStringOrNull(row.event_id) ||
      !isOpponentObservationCards(row.cards) ||
      !isHistoryStatus(row.opponent_card_observation_status) ||
      !isHistoryStatusOrNull(row.linked_gameplay_action_status) ||
      !isHistoryStatusOrNull(row.game_status) ||
      !isHistoryStatusOrNull(row.game_result_status) ||
      !isHistoryStatusOrNull(row.match_result_status) ||
      !isHistoryStatusOrNull(row.context_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Opponent observation row has an unsupported shape.");
    }
  }
}

function validatePlayDrawSplitRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Play/draw split rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.play_draw !== "string" ||
      typeof row.game_count !== "number" ||
      typeof row.known_result_count !== "number" ||
      typeof row.wins !== "number" ||
      typeof row.losses !== "number" ||
      typeof row.unknown_result_count !== "number" ||
      typeof row.unavailable_result_count !== "number" ||
      typeof row.degraded_result_count !== "number" ||
      !isNumberOrNull(row.win_rate) ||
      !isStringOrNull(row.sample_size_warning)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Play/draw split row has an unsupported shape.");
    }
  }
}

function validateGame1PostboardSplitRows(rows: unknown): void {
  if (!Array.isArray(rows)) {
    throw new AnalyticsHistoryApiError("malformed_response", "Game 1/postboard split rows must be an array.");
  }
  for (const row of rows) {
    if (
      !isRecord(row) ||
      typeof row.game_result_id !== "string" ||
      typeof row.match_id !== "string" ||
      typeof row.game_id !== "string" ||
      typeof row.game_number !== "number" ||
      !isStringOrNull(row.pre_postboard_label) ||
      !isStringOrNull(row.local_result) ||
      !isStringOrNull(row.play_draw) ||
      !isNumberOrNull(row.turn_count) ||
      !isNumberOrNull(row.game_duration_seconds) ||
      !isHistoryStatus(row.game_result_status)
    ) {
      throw new AnalyticsHistoryApiError("malformed_response", "Game 1/postboard split row has an unsupported shape.");
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

function getLiveStatusApiBaseUrl(): string {
  try {
    return getApiBaseUrl();
  } catch {
    throw new LiveStatusApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }
}

function getMatchJournalApiBaseUrl(): string {
  try {
    return getApiBaseUrl();
  } catch {
    throw new MatchJournalApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }
}

function getErrorReportApiBaseUrl(): string {
  try {
    return getApiBaseUrl();
  } catch {
    throw new ErrorReportApiError("unsafe_api_base_url", "API base URL must be a local loopback HTTP origin.");
  }
}

function validateErrorReportPreviewResponse(payload: unknown): ErrorReportPreviewResponse {
  if (!isRecord(payload)) {
    throw new ErrorReportApiError("malformed_response", "Error report preview must be a JSON object.");
  }

  for (const field of REQUIRED_ERROR_REPORT_PREVIEW_FIELDS) {
    if (!(field in payload)) {
      throw new ErrorReportApiError("malformed_response", "Error report preview is missing required fields.");
    }
  }

  if (payload.schema !== ERROR_REPORT_PREVIEW_SCHEMA) {
    throw new ErrorReportApiError(
      "incompatible_response",
      `Expected error report preview schema ${ERROR_REPORT_PREVIEW_SCHEMA}.`
    );
  }

  if (!isErrorReportPreviewStatus(payload.status)) {
    throw new ErrorReportApiError("malformed_response", "Error report preview status is unsupported.");
  }

  if (
    typeof payload.issue_title !== "string" ||
    typeof payload.issue_body_markdown !== "string" ||
    !isStringArray(payload.included_diagnostic_categories) ||
    !isStringArray(payload.excluded_private_data) ||
    !isStringArray(payload.redaction_summary) ||
    !isStringArray(payload.warnings) ||
    typeof payload.next_recommended_role !== "string" ||
    payload.external_submission_enabled !== false
  ) {
    throw new ErrorReportApiError("malformed_response", "Error report preview has an unsupported shape.");
  }

  return payload as ErrorReportPreviewResponse;
}

function isErrorReportPreviewStatus(value: unknown): boolean {
  return value === "preview_ready" || value === "invalid_request" || value === "blocked_privacy_guard";
}

function validateMatchJournalResponse(payload: unknown): MatchJournalResponse {
  if (!isRecord(payload)) {
    throw new MatchJournalApiError("malformed_response", "Match Journal response must be a JSON object.");
  }

  for (const field of REQUIRED_MATCH_JOURNAL_FIELDS) {
    if (!(field in payload)) {
      throw new MatchJournalApiError("malformed_response", "Match Journal response is missing required fields.");
    }
  }

  if (payload.schema_version !== MATCH_JOURNAL_SCHEMA_VERSION) {
    throw new MatchJournalApiError(
      "incompatible_response",
      `Expected Match Journal schema ${MATCH_JOURNAL_SCHEMA_VERSION}.`
    );
  }

  if (payload.object !== MATCH_JOURNAL_OBJECT) {
    throw new MatchJournalApiError("malformed_response", "Match Journal object is unsupported.");
  }

  if (
    !isMatchJournalStatus(payload.status) ||
    !isRecord(payload.result) ||
    !isStringArray(payload.warnings) ||
    !isStringArray(payload.errors)
  ) {
    throw new MatchJournalApiError("malformed_response", "Match Journal response has an unsupported shape.");
  }

  return payload as MatchJournalResponse;
}

function isMatchJournalStatus(value: unknown): value is MatchJournalStatus {
  return (
    value === "ok" ||
    value === "degraded" ||
    value === "empty" ||
    value === "missing" ||
    value === "unavailable" ||
    value === "error"
  );
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

function isBooleanOrNull(value: unknown): value is boolean | null {
  return typeof value === "boolean" || value === null;
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((entry) => typeof entry === "string");
}

function isLivePlayerLogSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.status === "string" &&
    typeof value.source === "string" &&
    typeof value.display_path === "string" &&
    typeof value.path_kind === "string" &&
    typeof value.metadata_access === "string" &&
    typeof value.exists === "boolean" &&
    value.contents_read === false &&
    value.tailing_started === false &&
    isNumberOrNull(value.size_bytes) &&
    isStringOrNull(value.last_modified_at) &&
    isNumberOrNull(value.last_modified_age_seconds) &&
    typeof value.activity_hint === "string"
  );
}

function isLiveWatcherSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.status === "string" &&
    value.mode === "readiness_only" &&
    value.running === false &&
    value.start_allowed === false &&
    value.stop_allowed === false &&
    value.parser_runner_started === false &&
    value.tailing_started === false &&
    value.sqlite_live_writes_enabled === false &&
    isStringOrNull(value.reason)
  );
}

function isLiveWatcherProcessControl(value: unknown): boolean {
  return (
    isRecord(value) &&
    value.mode === "safeguards_only" &&
    typeof value.implementation_status === "string" &&
    value.start_allowed === false &&
    value.stop_allowed === false &&
    value.start_route_enabled === false &&
    value.stop_route_enabled === false &&
    value.ui_controls_allowed === false &&
    value.automatic_start_enabled === false &&
    typeof value.parser_runner_started === "boolean" &&
    typeof value.tailing_started === "boolean" &&
    typeof value.sqlite_live_writes_enabled === "boolean" &&
    value.external_transport_allowed === false &&
    isStringOrNull(value.reason)
  );
}

function isLiveWatcherProcessSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.status === "string" &&
    typeof value.running === "boolean" &&
    typeof value.pid_verified === "boolean" &&
    typeof value.single_instance_guard === "string" &&
    typeof value.supervisor_boundary === "string"
  );
}

function isLiveWatcherProcessState(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.source === "string" &&
    typeof value.exists === "boolean" &&
    typeof value.status === "string" &&
    typeof value.stale === "boolean" &&
    typeof value.pid_present === "boolean" &&
    value.pid_verified === false &&
    typeof value.supervisor_token_present === "boolean" &&
    isStringOrNull(value.display_path) &&
    value.raw_path_exposed === false
  );
}

function isLiveCaptureSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.running === "boolean" &&
    typeof value.start_allowed === "boolean" &&
    typeof value.stop_allowed === "boolean" &&
    typeof value.parser_runner_started === "boolean" &&
    typeof value.tailing_started === "boolean" &&
    typeof value.sqlite_live_writes_enabled === "boolean" &&
    value.external_transport_allowed === false &&
    value.raw_player_log_storage_enabled === false &&
    typeof value.supervisor_kind === "string" &&
    typeof value.source_kind === "string" &&
    isStringOrNull(value.reason)
  );
}

function isLiveCapturePreconditions(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.key === "string" &&
        typeof entry.status === "string" &&
        isStringOrNull(entry.reason)
    )
  );
}

function isLiveCaptureState(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.source === "string" &&
    typeof value.exists === "boolean" &&
    typeof value.status === "string" &&
    typeof value.stale === "boolean" &&
    typeof value.pid_present === "boolean" &&
    value.pid_verified === false &&
    typeof value.supervisor_token_present === "boolean" &&
    isStringOrNull(value.display_path) &&
    value.raw_path_exposed === false &&
    (!("started_at" in value) || isStringOrNull(value.started_at)) &&
    (!("updated_at" in value) || isStringOrNull(value.updated_at))
  );
}

function isPreconditions(value: unknown): boolean {
  if (!Array.isArray(value)) {
    return false;
  }
  const keys = value.map((entry) => (isRecord(entry) ? entry.key : null));
  return (
    keys.length === LIVE_WATCHER_PROCESS_PRECONDITION_KEYS.length &&
    LIVE_WATCHER_PROCESS_PRECONDITION_KEYS.every((key, index) => keys[index] === key) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.key === "string" &&
        typeof entry.status === "string" &&
        isStringOrNull(entry.reason)
    )
  );
}

function isLiveWatcherDiagnosticsSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.info_count === "number" &&
    typeof value.warning_count === "number" &&
    typeof value.degraded_count === "number" &&
    typeof value.error_count === "number" &&
    typeof value.blocked_count === "number" &&
    typeof value.unknown_count === "number"
  );
}

function isLiveWatcherDiagnosticsEntries(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.category === "string" &&
        typeof entry.key === "string" &&
        typeof entry.severity === "string" &&
        typeof entry.status === "string" &&
        typeof entry.evidence_availability === "string" &&
        typeof entry.source === "string" &&
        typeof entry.message === "string" &&
        isNumberOrNull(entry.count) &&
        typeof entry.review_required === "boolean"
    )
  );
}

function isLiveWatcherDiagnosticsPrivacy(value: unknown): boolean {
  return (
    isRecord(value) &&
    value.raw_player_log_content_included === false &&
    value.raw_player_log_path_included === false &&
    value.raw_hashes_included === false &&
    value.raw_sql_included === false &&
    value.stack_traces_included === false &&
    value.secrets_or_environment_values_included === false
  );
}

function isLiveWatcherDiagnosticsCapabilities(value: unknown): boolean {
  return (
    isRecord(value) &&
    value.read_only === true &&
    value.starts_watcher === false &&
    value.stops_watcher === false &&
    value.tails_player_log === false &&
    value.writes_sqlite === false &&
    value.writes_diagnostics_files === false &&
    value.external_transport_allowed === false
  );
}

function isNumberArray(value: unknown): value is number[] {
  return Array.isArray(value) && value.every((entry) => typeof entry === "number");
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

function isEarlyGameHistorySummary(value: unknown): boolean {
  return isHistorySummary(value) && isRecord(value) && typeof value.card_row_count === "number";
}

function isActionReviewSummary(value: unknown): boolean {
  return (
    isEarlyGameHistorySummary(value) &&
    isRecord(value) &&
    typeof value.review_required_row_count === "number"
  );
}

function isPlayDrawSplitSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.row_count === "number" &&
    typeof value.total_game_count === "number" &&
    typeof value.known_result_count === "number" &&
    typeof value.wins === "number" &&
    typeof value.losses === "number" &&
    typeof value.unknown_result_count === "number" &&
    typeof value.unavailable_result_count === "number" &&
    typeof value.degraded_result_count === "number" &&
    typeof value.small_sample_group_count === "number"
  );
}

function isGame1PostboardSplitSummary(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.row_count === "number" &&
    typeof value.game1_row_count === "number" &&
    typeof value.postboard_row_count === "number" &&
    typeof value.known_result_count === "number" &&
    typeof value.unknown_result_count === "number" &&
    typeof value.degraded_row_count === "number" &&
    typeof value.unavailable_row_count === "number" &&
    typeof value.conflict_row_count === "number"
  );
}

function isAnalyticsDashboardModules(value: unknown): boolean {
  return Array.isArray(value) && value.every((module) => isAnalyticsDashboardModule(module));
}

function isAnalyticsDashboardModule(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.module_id === "string" &&
    typeof value.title === "string" &&
    typeof value.decision_question === "string" &&
    isAnalyticsDashboardModuleStatus(value.status) &&
    isAnalyticsDashboardModuleTone(value.tone) &&
    isAnalyticsDashboardView(value.default_view) &&
    Array.isArray(value.allowed_views) &&
    value.allowed_views.every((entry) => isAnalyticsDashboardView(entry)) &&
    value.allowed_views.includes(value.default_view) &&
    isAnalyticsDashboardMetric(value.metric, { moduleMetric: true }) &&
    isAnalyticsDashboardDimensions(value.dimensions) &&
    isAnalyticsDashboardRows(value.rows) &&
    isRecord(value.summary) &&
    isStringArray(value.warnings) &&
    isStringArray(value.errors) &&
    isAnalyticsDashboardDataQuality(value.data_quality) &&
    isAnalyticsDashboardSourceMetadata(value.source_metadata) &&
    value.schema_version === ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION
  );
}

function isAnalyticsDashboardModuleStatus(value: unknown): boolean {
  return (
    value === "ok" ||
    value === "empty" ||
    value === "missing" ||
    value === "unavailable" ||
    value === "degraded" ||
    value === "error" ||
    value === "deferred"
  );
}

function isAnalyticsDashboardModuleTone(value: unknown): boolean {
  return (
    value === "ok" ||
    value === "empty" ||
    value === "limited" ||
    value === "degraded" ||
    value === "blocked" ||
    value === "deferred"
  );
}

function isAnalyticsDashboardView(value: unknown): boolean {
  return value === "bar" || value === "table";
}

function isAnalyticsDashboardMetric(value: unknown, options: { moduleMetric: boolean }): boolean {
  return (
    isRecord(value) &&
    typeof value.metric_id === "string" &&
    typeof value.label === "string" &&
    (typeof value.value === "number" || typeof value.value === "string" || value.value === null) &&
    isAnalyticsDashboardMetricKind(value.value_kind) &&
    typeof value.unit === "string" &&
    typeof value.display === "string" &&
    (!options.moduleMetric || typeof value.calculation_note === "string") &&
    (!options.moduleMetric || typeof value.source === "string")
  );
}

function isAnalyticsDashboardMetricKind(value: unknown): boolean {
  return value === "count" || value === "ratio" || value === "percentage" || value === "text" || value === "null";
}

function isAnalyticsDashboardDimensions(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.dimension_id === "string" &&
        typeof entry.label === "string" &&
        typeof entry.source === "string" &&
        isAnalyticsDashboardValueSource(entry.value_source) &&
        (!("allowed_values" in entry) || isStringArray(entry.allowed_values)) &&
        (!("annotation_boundary" in entry) || entry.annotation_boundary === "Journal annotation")
    )
  );
}

function isAnalyticsDashboardValueSource(value: unknown): boolean {
  return (
    value === "parser_normalized" ||
    value === "analytics_derived" ||
    value === "journal_annotation" ||
    value === "display_only"
  );
}

function isAnalyticsDashboardRows(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.row_id === "string" &&
        typeof entry.label === "string" &&
        isRecord(entry.dimension_values) &&
        Array.isArray(entry.metrics) &&
        entry.metrics.every((metric) => isAnalyticsDashboardMetric(metric, { moduleMetric: false })) &&
        isAnalyticsDashboardModuleStatus(entry.status) &&
        isAnalyticsDashboardModuleTone(entry.tone) &&
        isAnalyticsDashboardSampleSize(entry.sample_size) &&
        isStringArray(entry.warnings) &&
        isAnalyticsDashboardSourceMetadata(entry.source_metadata)
    )
  );
}

function isAnalyticsDashboardSampleSize(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.status === "string" &&
    typeof value.known_result_count === "number" &&
    typeof value.total_count === "number"
  );
}

function isAnalyticsDashboardDataQuality(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.status === "string" &&
    typeof value.sample_size_status === "string" &&
    typeof value.known_result_count === "number" &&
    typeof value.unknown_or_degraded_count === "number" &&
    typeof value.review_required_count === "number" &&
    typeof value.confidence === "string" &&
    typeof value.finality === "string" &&
    isStringArray(value.notes)
  );
}

function isAnalyticsDashboardSourceMetadata(value: unknown): boolean {
  return (
    isRecord(value) &&
    isStringArray(value.source_tables_or_views) &&
    isStringArray(value.source_contracts) &&
    typeof value.source_type === "string" &&
    typeof value.parser_truth_boundary === "string" &&
    typeof value.analytics_truth_boundary === "string" &&
    (!("generated_at" in value) || typeof value.generated_at === "string")
  );
}

function isAnalyticsDashboardCustomExplorer(value: unknown): boolean {
  return (
    isRecord(value) &&
    typeof value.status === "string" &&
    value.builder_ui_enabled === false &&
    value.query_execution_enabled === false &&
    isAnalyticsDashboardDimensions(value.dimensions) &&
    isStringArray(value.metrics) &&
    isStringArray(value.warnings) &&
    isStringArray(value.errors)
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

function isOpeningHandCards(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.opening_hand_card_id === "string" &&
        typeof entry.card_position === "number" &&
        isNumberOrNull(entry.grp_id) &&
        isStringOrNull(entry.card_name) &&
        isStringOrNull(entry.identity_hint_source) &&
        isStringOrNull(entry.name_resolution_status) &&
        isHistoryStatus(entry.card_status)
    )
  );
}

function isMulliganCards(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.mulligan_card_id === "string" &&
        typeof entry.card_position === "number" &&
        isMulliganCardAction(entry.card_action) &&
        isNumberOrNull(entry.grp_id) &&
        isStringOrNull(entry.card_name) &&
        isStringOrNull(entry.identity_hint_source) &&
        isHistoryStatus(entry.card_status)
    )
  );
}

function isGameplayActionCards(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.gameplay_action_card_id === "string" &&
        typeof entry.card_ordinal === "number" &&
        isNumberOrNull(entry.instance_id) &&
        isNumberOrNull(entry.grp_id) &&
        isNumberOrNull(entry.observed_grp_id) &&
        isNumberOrNull(entry.overlay_grp_id) &&
        isNumberOrNull(entry.object_source_grp_id) &&
        isStringOrNull(entry.identity_hint_source) &&
        isStringOrNull(entry.card_name) &&
        isStringOrNull(entry.display_name) &&
        isStringOrNull(entry.name_resolution_status) &&
        isStringOrNull(entry.enrichment_status) &&
        isHistoryStatus(entry.card_status)
    )
  );
}

function isOpponentObservationCards(value: unknown): boolean {
  return (
    Array.isArray(value) &&
    value.every(
      (entry) =>
        isRecord(entry) &&
        typeof entry.opponent_card_observation_card_id === "string" &&
        typeof entry.card_ordinal === "number" &&
        isNumberOrNull(entry.grp_id) &&
        isNumberOrNull(entry.observed_grp_id) &&
        isNumberOrNull(entry.overlay_grp_id) &&
        isNumberOrNull(entry.object_source_grp_id) &&
        isStringOrNull(entry.identity_hint_source) &&
        isStringOrNull(entry.card_name) &&
        isStringOrNull(entry.resolution_status) &&
        isStringOrNull(entry.visibility) &&
        isHistoryStatus(entry.card_status)
    )
  );
}

function isLinkedGameplayActionOrNull(value: unknown): boolean {
  return (
    value === null ||
    (isRecord(value) &&
      typeof value.gameplay_action_id === "string" &&
      isNumberOrNull(value.turn_number) &&
      typeof value.action_type === "string" &&
      typeof value.actor_relation === "string" &&
      isStringOrNull(value.from_zone_type) &&
      isStringOrNull(value.to_zone_type) &&
      isBooleanOrNull(value.visible_in_log))
  );
}

function isMulliganCardAction(value: unknown): value is "bottomed" | "discarded" | "unknown" {
  return value === "bottomed" || value === "discarded" || value === "unknown";
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
