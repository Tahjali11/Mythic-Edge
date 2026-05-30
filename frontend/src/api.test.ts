import { describe, expect, it, vi } from "vitest";

import { fetchSetupStatus, getApiBaseUrl, SetupStatusApiError } from "./api";
import { SETUP_STATUS_OBJECT, SETUP_STATUS_SCHEMA_VERSION, type SetupStatusResponse } from "./types";

describe("api helpers", () => {
  it("accepts empty and loopback API base URLs only", () => {
    expect(getApiBaseUrl("")).toBe("");
    expect(getApiBaseUrl("http://127.0.0.1:8000")).toBe("http://127.0.0.1:8000");
    expect(getApiBaseUrl("http://localhost:5173/")).toBe("http://localhost:5173");

    for (const value of ["https://127.0.0.1:8000", "http://0.0.0.0:8000", "http://example.test:8000"]) {
      expect(() => getApiBaseUrl(value)).toThrow(SetupStatusApiError);
    }
  });

  it("fetches and validates the aggregate setup status response", async () => {
    const payload = buildSetupStatusPayload();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(fetchSetupStatus(fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/app/setup-status", {
      headers: { Accept: "application/json" }
    });
  });

  it("classifies missing required schema fields as malformed responses", async () => {
    const missingSchemaFetch = vi.fn(async () =>
      jsonResponse({ object: SETUP_STATUS_OBJECT })
    ) as unknown as typeof fetch;
    await expect(fetchSetupStatus(missingSchemaFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const missingObjectFetch = vi.fn(async () =>
      jsonResponse({ schema_version: SETUP_STATUS_SCHEMA_VERSION })
    ) as unknown as typeof fetch;
    await expect(fetchSetupStatus(missingObjectFetch)).rejects.toMatchObject({ code: "malformed_response" });
  });

  it("rejects malformed or incompatible responses without returning raw payloads", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildSetupStatusPayload(), schema_version: "future.schema" })
    ) as unknown as typeof fetch;
    await expect(fetchSetupStatus(wrongSchemaFetch)).rejects.toMatchObject({ code: "incompatible_response" });

    const nonObjectFetch = vi.fn(async () => jsonResponse(["not", "object"])) as unknown as typeof fetch;
    await expect(fetchSetupStatus(nonObjectFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const wrongObjectFetch = vi.fn(async () =>
      jsonResponse({ ...buildSetupStatusPayload(), object: "future_setup_status" })
    ) as unknown as typeof fetch;
    await expect(fetchSetupStatus(wrongObjectFetch)).rejects.toMatchObject({ code: "malformed_response" });
  });

  it("maps failed requests to backend unavailable", async () => {
    const fetchImpl = vi.fn(async () => {
      throw new Error("synthetic network failure");
    }) as unknown as typeof fetch;

    await expect(fetchSetupStatus(fetchImpl)).rejects.toMatchObject({ code: "backend_unavailable" });
  });
});

function jsonResponse(payload: unknown): Response {
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}

function buildSetupStatusPayload(): SetupStatusResponse {
  return {
    object: SETUP_STATUS_OBJECT,
    schema_version: SETUP_STATUS_SCHEMA_VERSION,
    status: "degraded",
    paths: { status: "degraded" },
    config: { status: "missing" },
    player_log: { status: "missing" },
    analytics_database: { status: "missing" },
    migrations: { status: "ok" },
    runtime: { status: "ok" },
    capabilities: { setup_status: "enabled" }
  };
}
