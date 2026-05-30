import {
  MANUAL_IMPORT_JOB_OBJECT,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  SETUP_STATUS_OBJECT,
  SETUP_STATUS_SCHEMA_VERSION,
  type ManualImportErrorCode,
  type ManualImportJob,
  type ManualImportRequest,
  type SetupStatusErrorCode,
  type SetupStatusResponse
} from "./types";

const SETUP_STATUS_PATH = "/api/app/setup-status";
const MANUAL_IMPORT_PATH = "/api/imports/jsonl";
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

  return payload as ManualImportJob;
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
