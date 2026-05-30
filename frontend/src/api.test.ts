import { describe, expect, it, vi } from "vitest";

import {
  fetchManualImportJob,
  fetchSetupStatus,
  getApiBaseUrl,
  ManualImportApiError,
  SetupStatusApiError,
  submitManualJsonlImport
} from "./api";
import {
  LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
  MANUAL_IMPORT_JOB_OBJECT,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  SETUP_STATUS_OBJECT,
  SETUP_STATUS_SCHEMA_VERSION,
  type LegacyJsonlImportQuality,
  type ManualImportJob,
  type SetupStatusResponse
} from "./types";

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

  it("submits manual JSONL import requests without exposing raw payloads in errors", async () => {
    const payload = buildManualImportJob();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(
      submitManualJsonlImport({ source_path: "Z:\\synthetic\\events_v1.jsonl" }, fetchImpl)
    ).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/imports/jsonl", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({ source_path: "Z:\\synthetic\\events_v1.jsonl" })
    });
  });

  it("submits explicit batch import requests with source_paths", async () => {
    const payload = buildManualImportJob();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;
    const sourcePaths = ["Z:\\synthetic\\a_events.jsonl", "Z:\\synthetic\\b_events.jsonl"];

    await expect(submitManualJsonlImport({ source_paths: sourcePaths }, fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/imports/jsonl", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({ source_paths: sourcePaths })
    });
  });

  it("fetches manual import job status by opaque id", async () => {
    const payload = buildManualImportJob();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(fetchManualImportJob("job/with space", fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/imports/jobs/job%2Fwith%20space", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed manual import job responses safely", async () => {
    const missingFieldsFetch = vi.fn(async () =>
      jsonResponse({ object: MANUAL_IMPORT_JOB_OBJECT })
    ) as unknown as typeof fetch;
    await expect(
      submitManualJsonlImport({ source_path: "Z:\\synthetic\\events_v1.jsonl" }, missingFieldsFetch)
    ).rejects.toMatchObject({ code: "malformed_response" });

    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildManualImportJob(), schema_version: "future.schema" })
    ) as unknown as typeof fetch;
    await expect(
      submitManualJsonlImport({ source_path: "Z:\\synthetic\\events_v1.jsonl" }, wrongSchemaFetch)
    ).rejects.toMatchObject({ code: "incompatible_response" });

    const missingQualityFetch = vi.fn(async () =>
      jsonResponse({
        ...buildManualImportJob(),
        adapter: { ...buildManualImportJob().adapter, quality: undefined }
      })
    ) as unknown as typeof fetch;
    await expect(
      submitManualJsonlImport({ source_path: "Z:\\synthetic\\events_v1.jsonl" }, missingQualityFetch)
    ).rejects.toMatchObject({ code: "malformed_response" });

    const wrongQualitySchemaFetch = vi.fn(async () =>
      jsonResponse({
        ...buildManualImportJob(),
        adapter: {
          ...buildManualImportJob().adapter,
          quality: { ...buildImportQuality(), schema_version: "future.quality" }
        }
      })
    ) as unknown as typeof fetch;
    await expect(
      submitManualJsonlImport({ source_path: "Z:\\synthetic\\events_v1.jsonl" }, wrongQualitySchemaFetch)
    ).rejects.toMatchObject({ code: "incompatible_response" });
  });

  it("maps manual import backend and unsafe API base failures", async () => {
    const failedFetch = vi.fn(async () => {
      throw new Error("synthetic network failure");
    }) as unknown as typeof fetch;

    await expect(
      submitManualJsonlImport({ source_path: "Z:\\synthetic\\events_v1.jsonl" }, failedFetch)
    ).rejects.toBeInstanceOf(ManualImportApiError);
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

function buildManualImportJob(): ManualImportJob {
  return {
    object: MANUAL_IMPORT_JOB_OBJECT,
    schema_version: MANUAL_IMPORT_JOB_SCHEMA_VERSION,
    job_id: "job-123",
    status: "succeeded",
    phase: "completed",
    created_at: "2026-05-29T18:00:00+00:00",
    started_at: "2026-05-29T18:00:00+00:00",
    finished_at: "2026-05-29T18:00:01+00:00",
    source: {
      source_kind: "saved_event_replay",
      source_artifact_label: "safe_source_label",
      source_display_label: "events_v1.jsonl",
      source_file_extension: ".jsonl",
      path_echoed: false,
      source_mode: "single_file",
      files_selected: 1,
      files_accepted: 1,
      files_rejected: 0,
      source_group_label: "safe_source_label",
      source_artifacts: []
    },
    adapter: {
      status: "succeeded",
      files_processed: 1,
      records_seen: 3,
      events_processed: 3,
      events_skipped: 0,
      unsupported_kind_counts: {},
      warnings: [],
      source_mode: "single_file",
      files_selected: 1,
      files_accepted: 1,
      files_rejected: 0,
      source_artifacts: [],
      quality: buildImportQuality()
    },
    ingest: {
      status: "succeeded",
      ingest_run_id: "ingest-123",
      source_kind: "saved_event_replay",
      source_artifact_label: "safe_source_label",
      row_counts: { matches: 1, games: 1 },
      warnings: [],
      skipped: {}
    },
    database: {
      status: "ok",
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      created: true
    },
    warnings: [],
    errors: []
  };
}

function buildImportQuality(): LegacyJsonlImportQuality {
  return {
    object: LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
    schema_version: LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
    quality_status: "complete" as const,
    records_seen: 3,
    events_processed: 3,
    events_skipped: 0,
    processed_kind_counts: { GameResult: 1, GameState: 1, MatchState: 1 },
    unsupported_kind_counts: {},
    skipped_reason_counts: {
      blank_line: 0,
      duplicate_raw_hash: 0,
      unsupported_kind: 0
    },
    blank_line_count: 0,
    duplicate_raw_hash_count: 0,
    unsupported_kind_skip_count: 0,
    output_gap_counts: {
      incomplete_match_summary: 0,
      incomplete_game_summary: 0,
      incomplete_summary_unclassified: 0
    },
    adapter_warning_counts: {},
    adapter_warning_codes: [],
    ingest_warning_codes: [],
    routing_hints: [],
    privacy: {
      has_private_path_echo: false as const,
      raw_payload_exposed: false as const,
      raw_hash_exposed: false as const
    }
  };
}
