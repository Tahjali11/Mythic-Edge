import {
  SETUP_STATUS_OBJECT,
  SETUP_STATUS_SCHEMA_VERSION,
  type SetupStatusErrorCode,
  type SetupStatusResponse
} from "./types";

const SETUP_STATUS_PATH = "/api/app/setup-status";
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

export class SetupStatusApiError extends Error {
  code: SetupStatusErrorCode;

  constructor(code: SetupStatusErrorCode, message: string) {
    super(message);
    this.name = "SetupStatusApiError";
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

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isStringRecord(value: unknown): value is Record<string, string> {
  if (!isRecord(value)) {
    return false;
  }
  return Object.values(value).every((entry) => typeof entry === "string");
}
