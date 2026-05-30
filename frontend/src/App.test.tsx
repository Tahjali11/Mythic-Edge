import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ManualImportApiError, SetupStatusApiError } from "./api";
import { SetupStatusApp } from "./App";
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

afterEach(() => {
  cleanup();
});

describe("SetupStatusApp", () => {
  it("renders safe setup-status panels from a degraded backend payload", async () => {
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} />);

    expect(screen.getByText("Checking local app setup")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Setup Status" })).toBeInTheDocument();

    expect(screen.getByText("Backend Reachability")).toBeInTheDocument();
    expect(screen.getByText("<app_data>")).toBeInTheDocument();
    expect(screen.getByText("<configured_player_log>")).toBeInTheDocument();
    expect(screen.getByText("<app_data>\\db\\mythic_edge.sqlite3")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Import JSONL" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();
  });

  it("renders a backend-unavailable state without stack traces", async () => {
    render(
      <SetupStatusApp
        fetchStatus={() => Promise.reject(new SetupStatusApiError("backend_unavailable", "Backend unavailable"))}
      />
    );

    expect(await screen.findByRole("heading", { name: "Backend unavailable" })).toBeInTheDocument();
    expect(screen.queryByText(/synthetic network failure|stack|error:/i)).not.toBeInTheDocument();
  });

  it("renders malformed and incompatible response states safely", async () => {
    const { rerender } = render(
      <SetupStatusApp
        fetchStatus={() => Promise.reject(new SetupStatusApiError("malformed_response", "Malformed setup response"))}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed setup response" })).toBeInTheDocument();

    rerender(
      <SetupStatusApp
        fetchStatus={() =>
          Promise.reject(
            new SetupStatusApiError(
              "incompatible_response",
              `Expected setup status schema ${SETUP_STATUS_SCHEMA_VERSION}.`
            )
          )
        }
      />
    );

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Incompatible setup schema" })).toBeInTheDocument();
    });
    expect(screen.getByText(`Expected schema: ${SETUP_STATUS_SCHEMA_VERSION}`)).toBeInTheDocument();
  });

  it("redacts unsafe path-like values from backend display fields", async () => {
    const payload = buildPayload({
      paths: {
        status: "degraded",
        app_data_root: { display_path: "Z:\\synthetic\\unsafe\\Player.log" },
        redaction_policy: "symbolic_app_data_paths_only"
      }
    });

    render(<SetupStatusApp fetchStatus={() => Promise.resolve(payload)} />);

    await screen.findByText("Unsafe display value redacted");
    expect(screen.getAllByText("<redacted_path>").length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText("Z:\\synthetic\\unsafe\\Player.log")).not.toBeInTheDocument();
    expect(screen.getByText("Unsafe display value redacted")).toBeInTheDocument();
  });

  it("submits manual import and renders sanitized job summary without retaining the raw path", async () => {
    const rawPath = "Z:\\synthetic\\events_v1.jsonl";
    const submitImport = vi.fn(async () => buildManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    const pathInput = await screen.findByLabelText("JSONL path");
    fireEvent.change(pathInput, { target: { value: rawPath } });
    fireEvent.change(screen.getByLabelText("Source label"), { target: { value: "safe_source_label" } });
    fireEvent.click(screen.getByRole("button", { name: "Import JSONL" }));

    await waitFor(() => {
      expect(submitImport).toHaveBeenCalledWith({
        source_path: rawPath,
        source_artifact_label: "safe_source_label"
      });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Quality Breakdown" })).toBeInTheDocument();
    expect(screen.getByText("events_v1.jsonl")).toBeInTheDocument();
    expect(screen.getByText("duplicate_raw_hash 1 unsupported_kind 1")).toBeInTheDocument();
    expect(screen.getByText("unsupported_event_kinds parser_or_adapter_backlog warning 1")).toBeInTheDocument();
    expect(screen.getByText("unsupported_event_kinds")).toBeInTheDocument();
    expect(pathInput).toHaveValue("");
    expect(screen.queryByDisplayValue(rawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(rawPath)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|git|sheets|ai/i })).not.toBeInTheDocument();
  });

  it("renders manual import API errors safely and clears the submitted path", async () => {
    const rawPath = "Z:\\synthetic\\events_v1.jsonl";
    const submitImport = vi.fn(async () => {
      throw new ManualImportApiError("malformed_response", "Malformed import response");
    });
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    const pathInput = await screen.findByLabelText("JSONL path");
    fireEvent.change(pathInput, { target: { value: rawPath } });
    fireEvent.click(screen.getByRole("button", { name: "Import JSONL" }));

    expect(await screen.findByRole("heading", { name: "Malformed import response" })).toBeInTheDocument();
    expect(pathInput).toHaveValue("");
    expect(screen.queryByText(/stack|error:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(rawPath)).not.toBeInTheDocument();
  });
});

function buildPayload(overrides: Partial<SetupStatusResponse> = {}): SetupStatusResponse {
  return {
    object: SETUP_STATUS_OBJECT,
    schema_version: SETUP_STATUS_SCHEMA_VERSION,
    status: "degraded",
    paths: {
      status: "degraded",
      app_data_root: { display_path: "<app_data>" },
      redaction_policy: "symbolic_app_data_paths_only"
    },
    config: {
      status: "missing",
      config_file: { display_path: "<app_data>\\config\\app_config.json", status: "missing" }
    },
    player_log: {
      status: "missing",
      player_log: { display_path: "<configured_player_log>", status: "configured_missing" }
    },
    analytics_database: {
      status: "missing",
      database: { display_path: "<app_data>\\db\\mythic_edge.sqlite3", schema_status: "missing" }
    },
    migrations: {
      status: "ok",
      migration_status: "available",
      migrations: [{ migration_id: "001_initial", checksum_present: true }]
    },
    runtime: {
      status: "ok",
      backend: { status: "running" },
      parser_runner: { status: "deferred" },
      live_watcher: { status: "deferred" },
      manual_import: { status: "enabled" }
    },
    capabilities: {
      setup_status: "enabled",
      manual_import: "enabled",
      live_watcher: "disabled"
    },
    ...overrides
  };
}

function buildManualImportJob(): ManualImportJob {
  return {
    object: MANUAL_IMPORT_JOB_OBJECT,
    schema_version: MANUAL_IMPORT_JOB_SCHEMA_VERSION,
    job_id: "job-123",
    status: "degraded",
    phase: "completed",
    created_at: "2026-05-29T18:00:00+00:00",
    started_at: "2026-05-29T18:00:00+00:00",
    finished_at: "2026-05-29T18:00:01+00:00",
    source: {
      source_kind: "saved_event_replay",
      source_artifact_label: "safe_source_label",
      source_display_label: "events_v1.jsonl",
      source_file_extension: ".jsonl",
      path_echoed: false
    },
    adapter: {
      status: "degraded",
      files_processed: 1,
      records_seen: 6,
      events_processed: 3,
      events_skipped: 2,
      unsupported_kind_counts: { ConnectionError: 1 },
      warnings: [],
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
    warnings: ["unsupported_event_kinds"],
    errors: []
  };
}

function buildImportQuality(): LegacyJsonlImportQuality {
  return {
    object: LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
    schema_version: LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
    quality_status: "degraded" as const,
    records_seen: 6,
    events_processed: 3,
    events_skipped: 2,
    processed_kind_counts: { GameResult: 1, GameState: 1, MatchState: 1 },
    unsupported_kind_counts: { ConnectionError: 1 },
    skipped_reason_counts: {
      blank_line: 0,
      duplicate_raw_hash: 1,
      unsupported_kind: 1
    },
    blank_line_count: 0,
    duplicate_raw_hash_count: 1,
    unsupported_kind_skip_count: 1,
    output_gap_counts: {
      incomplete_match_summary: 0,
      incomplete_game_summary: 0,
      incomplete_summary_unclassified: 0
    },
    adapter_warning_counts: {
      events_skipped: 1,
      unsupported_event_kinds: 1
    },
    adapter_warning_codes: ["events_skipped", "unsupported_event_kinds"],
    ingest_warning_codes: [],
    routing_hints: [
      {
        code: "unsupported_event_kinds",
        category: "parser_or_adapter_backlog",
        severity: "warning",
        count: 1
      }
    ],
    privacy: {
      has_private_path_echo: false as const,
      raw_payload_exposed: false as const,
      raw_hash_exposed: false as const
    }
  };
}
