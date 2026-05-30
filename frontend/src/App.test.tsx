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
  type ManualImportSourceArtifact,
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

  it("submits a batch import and renders sanitized per-file summaries", async () => {
    const firstRawPath = "Z:\\synthetic\\a_events.jsonl";
    const secondRawPath = "Z:\\synthetic\\b_events.jsonl";
    const submitImport = vi.fn(async () => buildBatchManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    const batchInput = await screen.findByLabelText("Batch JSONL paths");
    fireEvent.change(batchInput, { target: { value: `${firstRawPath}\n${secondRawPath}` } });
    fireEvent.change(screen.getByLabelText("Source label"), { target: { value: "safe_batch_label" } });
    fireEvent.click(screen.getByRole("button", { name: "Import JSONL" }));

    await waitFor(() => {
      expect(submitImport).toHaveBeenCalledWith({
        source_paths: [firstRawPath, secondRawPath],
        source_artifact_label: "safe_batch_label"
      });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getByText("explicit_file_batch")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Source Files" })).toBeInTheDocument();
    expect(screen.getByText("a_events.jsonl processed events 2 skipped 0 warnings none")).toBeInTheDocument();
    expect(screen.getByText("b_events.jsonl processed events 1 skipped 0 warnings none")).toBeInTheDocument();
    expect(batchInput).toHaveValue("");
    expect(screen.queryByDisplayValue(firstRawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(firstRawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(secondRawPath)).not.toBeInTheDocument();
  });

  it("uploads browser-selected JSONL files and renders sanitized upload summaries", async () => {
    const firstFile = new File(['{"kind":"MatchState"}\n'], "a_events.jsonl", { type: "application/jsonl" });
    const secondFile = new File(['{"kind":"GameResult"}\n'], "b_events.jsonl", { type: "application/jsonl" });
    const submitUpload = vi.fn(async () => buildUploadedManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitUpload={submitUpload} />);

    const uploadInput = (await screen.findByLabelText("Upload JSONL files")) as HTMLInputElement;
    fireEvent.change(uploadInput, { target: { files: [firstFile, secondFile] } });
    fireEvent.change(screen.getByLabelText("Source label"), { target: { value: "safe_upload_label" } });
    expect(screen.getByText("2 files selected a_events.jsonl b_events.jsonl")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Upload JSONL Files" }));

    await waitFor(() => {
      expect(submitUpload).toHaveBeenCalledWith({
        files: [firstFile, secondFile],
        source_artifact_label: "safe_upload_label"
      });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getByText("uploaded_file_batch")).toBeInTheDocument();
    expect(screen.getByText("a_events.jsonl processed events 2 skipped 0 warnings none")).toBeInTheDocument();
    expect(screen.getByText("b_events.jsonl processed events 1 skipped 0 warnings none")).toBeInTheDocument();
    expect(screen.queryByText("2 files selected a_events.jsonl b_events.jsonl")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|git|sheets|ai/i })).not.toBeInTheDocument();
  });

  it("renders upload API errors safely and clears selected files", async () => {
    const rawFileName = "secret_token_dump.jsonl";
    const selectedFile = new File(['{"raw":"private"}\n'], rawFileName, { type: "application/jsonl" });
    const submitUpload = vi.fn(async () => {
      throw new ManualImportApiError("malformed_response", "Malformed import response");
    });
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitUpload={submitUpload} />);

    fireEvent.change(await screen.findByLabelText("Upload JSONL files"), { target: { files: [selectedFile] } });
    expect(screen.getByText("1 files selected <selected_jsonl>")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Upload JSONL Files" }));

    expect(await screen.findByRole("heading", { name: "Malformed import response" })).toBeInTheDocument();
    expect(screen.queryByText("1 files selected <selected_jsonl>")).not.toBeInTheDocument();
    expect(screen.queryByText(/stack|error:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(rawFileName)).not.toBeInTheDocument();
  });

  it("redacts selected upload filenames with private-marker classes", async () => {
    const privateNames = [
      "api_key_dump.jsonl",
      "apikey_dump.jsonl",
      "access_token_dump.jsonl",
      "bearer credential.jsonl",
      "password_dump.jsonl",
      "hooks.example.jsonl",
      "script.google.com.jsonl"
    ];
    const selectedFiles = privateNames.map((name) => new File(['{"kind":"Rank"}\n'], name, { type: "application/jsonl" }));
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} />);

    fireEvent.change(await screen.findByLabelText("Upload JSONL files"), { target: { files: selectedFiles } });

    expect(
      screen.getByText(
        "7 files selected <selected_jsonl> <selected_jsonl> <selected_jsonl> <selected_jsonl> <selected_jsonl> <selected_jsonl> <selected_jsonl>"
      )
    ).toBeInTheDocument();
    for (const privateName of privateNames) {
      expect(screen.queryByText(privateName)).not.toBeInTheDocument();
    }
  });

  it("renders a rejected batch import state without retaining raw paths", async () => {
    const rawPath = "Z:\\synthetic\\invalid_events.jsonl";
    const submitImport = vi.fn(async () => buildBatchRejectedManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    const batchInput = await screen.findByLabelText("Batch JSONL paths");
    fireEvent.change(batchInput, { target: { value: rawPath } });
    fireEvent.click(screen.getByRole("button", { name: "Import JSONL" }));

    await waitFor(() => {
      expect(submitImport).toHaveBeenCalledWith({ source_paths: [rawPath] });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getAllByLabelText("status rejected").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("<selected_jsonl>")).toBeInTheDocument();
    expect(screen.getByText("source_path_invalid")).toBeInTheDocument();
    expect(batchInput).toHaveValue("");
    expect(screen.queryByDisplayValue(rawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(rawPath)).not.toBeInTheDocument();
  });

  it("renders a failed batch import state without raw payload, hash, or path details", async () => {
    const firstRawPath = "Z:\\synthetic\\a_events.jsonl";
    const secondRawPath = "Z:\\synthetic\\malformed_events.jsonl";
    const privateHash = "batch-private-raw-hash";
    const rawPayload = '{"kind": "GameState", "payload": ';
    const submitImport = vi.fn(async () => buildBatchFailedManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    const batchInput = await screen.findByLabelText("Batch JSONL paths");
    fireEvent.change(batchInput, { target: { value: `${firstRawPath}\n${secondRawPath}` } });
    fireEvent.click(screen.getByRole("button", { name: "Import JSONL" }));

    await waitFor(() => {
      expect(submitImport).toHaveBeenCalledWith({ source_paths: [firstRawPath, secondRawPath] });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getAllByLabelText("status failed").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("invalid_jsonl").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("invalid_jsonl source_artifact_problem action_needed 1")).toBeInTheDocument();
    expect(batchInput).toHaveValue("");
    expect(screen.queryByText(firstRawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(secondRawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(privateHash)).not.toBeInTheDocument();
    expect(screen.queryByText(rawPayload)).not.toBeInTheDocument();
  });

  it("renders a degraded batch import state with safe aggregate and per-file details", async () => {
    const firstRawPath = "Z:\\synthetic\\a_events.jsonl";
    const secondRawPath = "Z:\\synthetic\\degraded_events.jsonl";
    const submitImport = vi.fn(async () => buildBatchDegradedManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    const batchInput = await screen.findByLabelText("Batch JSONL paths");
    fireEvent.change(batchInput, { target: { value: `${firstRawPath}\n${secondRawPath}` } });
    fireEvent.click(screen.getByRole("button", { name: "Import JSONL" }));

    await waitFor(() => {
      expect(submitImport).toHaveBeenCalledWith({ source_paths: [firstRawPath, secondRawPath] });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getAllByLabelText("status degraded").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("explicit_file_batch")).toBeInTheDocument();
    expect(screen.getByText("duplicate_raw_hash 1 unsupported_kind 1")).toBeInTheDocument();
    expect(screen.getByText("degraded_events.jsonl processed_with_skips events 1 skipped 2 warnings events_skipped")).toBeInTheDocument();
    expect(batchInput).toHaveValue("");
    expect(screen.queryByText(firstRawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(secondRawPath)).not.toBeInTheDocument();
  });

  it("keeps manual import submission disabled when both single and batch paths are entered", async () => {
    const submitImport = vi.fn(async () => buildManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitImport={submitImport} />);

    fireEvent.change(await screen.findByLabelText("JSONL path"), { target: { value: "Z:\\synthetic\\events.jsonl" } });
    fireEvent.change(screen.getByLabelText("Batch JSONL paths"), { target: { value: "Z:\\synthetic\\a_events.jsonl" } });

    expect(screen.getByRole("button", { name: "Import JSONL" })).toBeDisabled();
    expect(submitImport).not.toHaveBeenCalled();
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
      path_echoed: false,
      source_mode: "single_file",
      files_selected: 1,
      files_accepted: 1,
      files_rejected: 0,
      source_group_label: "safe_source_label",
      source_artifacts: []
    },
    adapter: {
      status: "degraded",
      files_processed: 1,
      records_seen: 6,
      events_processed: 3,
      events_skipped: 2,
      unsupported_kind_counts: { ConnectionError: 1 },
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
    warnings: ["unsupported_event_kinds"],
    errors: []
  };
}

function buildBatchManualImportJob(): ManualImportJob {
  const job = buildManualImportJob();
  const sourceArtifacts: ManualImportSourceArtifact[] = [
    {
      batch_index: 0,
      source_artifact_label: "legacy_jsonl_file:0:abc123",
      source_display_label: "a_events.jsonl",
      status: "processed",
      records_seen: 2,
      events_processed: 2,
      events_skipped: 0,
      processed_kind_counts: { GameState: 1, MatchState: 1 },
      unsupported_kind_counts: {},
      skipped_reason_counts: {
        blank_line: 0,
        duplicate_raw_hash: 0,
        unsupported_kind: 0
      },
      adapter_warning_codes: []
    },
    {
      batch_index: 1,
      source_artifact_label: "legacy_jsonl_file:1:def456",
      source_display_label: "b_events.jsonl",
      status: "processed",
      records_seen: 1,
      events_processed: 1,
      events_skipped: 0,
      processed_kind_counts: { GameResult: 1 },
      unsupported_kind_counts: {},
      skipped_reason_counts: {
        blank_line: 0,
        duplicate_raw_hash: 0,
        unsupported_kind: 0
      },
      adapter_warning_codes: []
    }
  ];
  return {
    ...job,
    status: "succeeded",
    source: {
      ...job.source,
      source_artifact_label: "safe_batch_label",
      source_display_label: "2 selected JSONL files",
      source_mode: "explicit_file_batch",
      files_selected: 2,
      files_accepted: 2,
      files_rejected: 0,
      source_group_label: "safe_batch_label",
      source_artifacts: sourceArtifacts
    },
    adapter: {
      ...job.adapter,
      status: "succeeded",
      files_processed: 2,
      records_seen: 3,
      events_processed: 3,
      events_skipped: 0,
      unsupported_kind_counts: {},
      source_mode: "explicit_file_batch",
      files_selected: 2,
      files_accepted: 2,
      files_rejected: 0,
      source_artifacts: sourceArtifacts,
      quality: buildImportQuality()
    },
    warnings: []
  };
}

function buildUploadedManualImportJob(): ManualImportJob {
  const job = buildBatchManualImportJob();
  const sourceArtifacts = (job.source.source_artifacts ?? []).map((artifact) => ({
    ...artifact,
    source_artifact_label: artifact.source_artifact_label.replace("legacy_jsonl_file", "legacy_jsonl_uploaded_file")
  }));
  return {
    ...job,
    source: {
      ...job.source,
      source_artifact_label: "safe_upload_label",
      source_display_label: "2 uploaded JSONL files",
      source_mode: "uploaded_file_batch",
      source_group_label: "safe_upload_label",
      source_artifacts: sourceArtifacts
    },
    adapter: {
      ...job.adapter,
      source_mode: "uploaded_file_batch",
      source_artifacts: sourceArtifacts
    }
  };
}

function buildBatchRejectedManualImportJob(): ManualImportJob {
  const job = buildManualImportJob();
  return {
    ...job,
    status: "rejected",
    phase: "failed",
    source: {
      ...job.source,
      source_artifact_label: "",
      source_display_label: "<selected_jsonl>",
      source_file_extension: ".jsonl",
      source_mode: "explicit_file_batch",
      files_selected: 1,
      files_accepted: 0,
      files_rejected: 0,
      source_group_label: "",
      source_artifacts: []
    },
    adapter: {
      status: "not_started",
      files_processed: 0,
      records_seen: 0,
      events_processed: 0,
      events_skipped: 0,
      unsupported_kind_counts: {},
      warnings: [],
      source_mode: "",
      files_selected: 0,
      files_accepted: 0,
      files_rejected: 0,
      source_artifacts: []
    },
    ingest: {
      ...job.ingest,
      status: "not_started",
      ingest_run_id: "",
      row_counts: {}
    },
    database: {
      status: "not_started",
      display_path: "",
      created: false
    },
    warnings: [],
    errors: ["source_path_invalid"]
  };
}

function buildBatchFailedManualImportJob(): ManualImportJob {
  const job = buildBatchManualImportJob();
  return {
    ...job,
    status: "failed",
    phase: "failed",
    adapter: {
      ...job.adapter,
      status: "failed",
      files_processed: 0,
      records_seen: 0,
      events_processed: 0,
      events_skipped: 0,
      unsupported_kind_counts: {},
      warnings: [],
      source_artifacts: [],
      quality: {
        ...buildImportQuality(),
        quality_status: "failed",
        records_seen: 0,
        events_processed: 0,
        events_skipped: 0,
        processed_kind_counts: {},
        unsupported_kind_counts: {},
        skipped_reason_counts: {},
        blank_line_count: 0,
        duplicate_raw_hash_count: 0,
        unsupported_kind_skip_count: 0,
        adapter_warning_counts: { invalid_jsonl: 1 },
        adapter_warning_codes: ["invalid_jsonl"],
        routing_hints: [
          {
            code: "invalid_jsonl",
            category: "source_artifact_problem",
            severity: "action_needed",
            count: 1
          }
        ]
      }
    },
    ingest: {
      ...job.ingest,
      status: "not_started",
      ingest_run_id: "",
      row_counts: {}
    },
    database: {
      status: "not_started",
      display_path: "",
      created: false
    },
    warnings: [],
    errors: ["invalid_jsonl"]
  };
}

function buildBatchDegradedManualImportJob(): ManualImportJob {
  const job = buildBatchManualImportJob();
  const degradedSourceArtifacts: ManualImportSourceArtifact[] = [
    {
      batch_index: 0,
      source_artifact_label: "legacy_jsonl_file:0:abc123",
      source_display_label: "a_events.jsonl",
      status: "processed",
      records_seen: 2,
      events_processed: 2,
      events_skipped: 0,
      processed_kind_counts: { GameState: 1, MatchState: 1 },
      unsupported_kind_counts: {},
      skipped_reason_counts: {
        blank_line: 0,
        duplicate_raw_hash: 0,
        unsupported_kind: 0
      },
      adapter_warning_codes: []
    },
    {
      batch_index: 1,
      source_artifact_label: "legacy_jsonl_file:1:def456",
      source_display_label: "degraded_events.jsonl",
      status: "processed_with_skips",
      records_seen: 3,
      events_processed: 1,
      events_skipped: 2,
      processed_kind_counts: { GameResult: 1 },
      unsupported_kind_counts: { ConnectionError: 1 },
      skipped_reason_counts: {
        blank_line: 0,
        duplicate_raw_hash: 1,
        unsupported_kind: 1
      },
      adapter_warning_codes: ["events_skipped"]
    }
  ];
  return {
    ...job,
    status: "degraded",
    adapter: {
      ...job.adapter,
      status: "degraded",
      records_seen: 5,
      events_processed: 3,
      events_skipped: 2,
      unsupported_kind_counts: { ConnectionError: 1 },
      source_artifacts: degradedSourceArtifacts,
      quality: buildImportQuality()
    },
    source: {
      ...job.source,
      source_artifacts: degradedSourceArtifacts
    },
    warnings: ["unsupported_event_kinds", "events_skipped"]
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
