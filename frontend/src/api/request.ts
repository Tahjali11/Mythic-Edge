import { SetupStatusApiError } from "./errors";

const REQUEST_GUARD_PATH = "/api/app/request-guard";
const REQUEST_GUARD_OBJECT = "mythic_edge_local_request_guard";
const REQUEST_GUARD_SCHEMA_VERSION = 1;
const REQUEST_GUARD_HEADER_NAME = "X-Mythic-Edge-Local-Request-Guard";

type LocalRequestGuard = {
  baseUrl: string;
  headerName: typeof REQUEST_GUARD_HEADER_NAME;
  guardValue: string;
};

let cachedLocalRequestGuard: LocalRequestGuard | null = null;
let pendingLocalRequestGuard: Promise<LocalRequestGuard> | null = null;

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

export function resetLocalRequestGuardForTests(): void {
  cachedLocalRequestGuard = null;
  pendingLocalRequestGuard = null;
}

export async function guardedFetch(
  baseUrl: string,
  path: string,
  init: RequestInit & { headers: Record<string, string> },
  fetchImpl: typeof fetch
): Promise<Response> {
  const guard = await fetchLocalRequestGuard(baseUrl, fetchImpl);
  return fetchImpl(`${baseUrl}${path}`, {
    ...init,
    headers: { ...init.headers, [guard.headerName]: guard.guardValue }
  });
}

async function fetchLocalRequestGuard(baseUrl: string, fetchImpl: typeof fetch): Promise<LocalRequestGuard> {
  if (cachedLocalRequestGuard?.baseUrl === baseUrl) {
    return cachedLocalRequestGuard;
  }
  pendingLocalRequestGuard ??= fetchAndValidateLocalRequestGuard(baseUrl, fetchImpl);
  try {
    cachedLocalRequestGuard = await pendingLocalRequestGuard;
    return cachedLocalRequestGuard;
  } finally {
    pendingLocalRequestGuard = null;
  }
}

async function fetchAndValidateLocalRequestGuard(baseUrl: string, fetchImpl: typeof fetch): Promise<LocalRequestGuard> {
  const response = await fetchImpl(`${baseUrl}${REQUEST_GUARD_PATH}`, {
    headers: { Accept: "application/json" }
  });
  if (!response.ok) {
    throw new Error("Local request guard is unavailable.");
  }
  const payload = await response.json();
  if (
    !isRecord(payload) ||
    payload.object !== REQUEST_GUARD_OBJECT ||
    payload.schema_version !== REQUEST_GUARD_SCHEMA_VERSION ||
    payload.status !== "available" ||
    payload.header_name !== REQUEST_GUARD_HEADER_NAME ||
    typeof payload["token"] !== "string" ||
    payload["token"].trim() === "" ||
    payload.expires_on_backend_restart !== true ||
    !Array.isArray(payload.warnings) ||
    !Array.isArray(payload.errors)
  ) {
    throw new Error("Local request guard returned malformed JSON.");
  }
  return { baseUrl, headerName: REQUEST_GUARD_HEADER_NAME, guardValue: payload["token"] };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
