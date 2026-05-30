import { useEffect, useRef, useState, type FormEvent, type ReactNode, type RefObject } from "react";

import "./App.css";
import {
  fetchSetupStatus,
  ManualImportApiError,
  SetupStatusApiError,
  submitManualJsonlImport,
  submitManualJsonlUpload
} from "./api";
import { safeDisplayValue, statusTone } from "./status";
import {
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  SETUP_STATUS_SCHEMA_VERSION,
  type ManualImportJob,
  type ManualImportRequest,
  type ManualImportUploadRequest,
  type LegacyJsonlImportQuality,
  type LegacyJsonlRoutingHint,
  type ManualImportSourceArtifact,
  type SectionStatus,
  type SetupStatusResponse
} from "./types";

type LoadState =
  | { state: "loading" }
  | { state: "ready"; payload: SetupStatusResponse; unsafeCount: number }
  | { state: "error"; code: SetupStatusApiError["code"]; message: string };

type SetupStatusAppProps = {
  fetchStatus?: () => Promise<SetupStatusResponse>;
  submitImport?: (request: ManualImportRequest) => Promise<ManualImportJob>;
  submitUpload?: (request: ManualImportUploadRequest) => Promise<ManualImportJob>;
};

type ImportState =
  | { state: "idle" }
  | { state: "submitting" }
  | { state: "result"; job: ManualImportJob }
  | { state: "error"; code: ManualImportApiError["code"]; message: string };

type Panel = {
  title: string;
  status: string;
  details: Array<{ label: string; value: unknown }>;
};

export function SetupStatusApp({
  fetchStatus = fetchSetupStatus,
  submitImport = submitManualJsonlImport,
  submitUpload = submitManualJsonlUpload
}: SetupStatusAppProps) {
  const [loadState, setLoadState] = useState<LoadState>({ state: "loading" });
  const [sourcePath, setSourcePath] = useState("");
  const [sourcePathsText, setSourcePathsText] = useState("");
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [sourceLabel, setSourceLabel] = useState("");
  const [importState, setImportState] = useState<ImportState>({ state: "idle" });
  const uploadFileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let active = true;
    setLoadState({ state: "loading" });

    fetchStatus()
      .then((payload) => {
        if (!active) {
          return;
        }
        const unsafeCount = countUnsafeValues(payload);
        setLoadState({ state: "ready", payload, unsafeCount });
      })
      .catch((error: unknown) => {
        if (!active) {
          return;
        }
        if (error instanceof SetupStatusApiError) {
          setLoadState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setLoadState({
          state: "error",
          code: "backend_unavailable",
          message: "Backend setup status is unavailable."
        });
      });

    return () => {
      active = false;
    };
  }, [fetchStatus]);

  async function handleManualImport(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedPath = sourcePath.trim();
    const trimmedBatchPaths = sourcePathsText
      .split(/\r?\n/)
      .map((path) => path.trim())
      .filter(Boolean);
    const hasSinglePath = Boolean(trimmedPath);
    const hasBatchPaths = trimmedBatchPaths.length > 0;
    if (importState.state === "submitting" || hasSinglePath === hasBatchPaths) {
      return;
    }

    const request: ManualImportRequest = hasBatchPaths ? { source_paths: trimmedBatchPaths } : { source_path: trimmedPath };
    const trimmedLabel = sourceLabel.trim();
    if (trimmedLabel) {
      request.source_artifact_label = trimmedLabel;
    }

    setImportState({ state: "submitting" });
    try {
      const job = await submitImport(request);
      setSourcePath("");
      setSourcePathsText("");
      setSourceLabel("");
      setImportState({ state: "result", job });
    } catch (error: unknown) {
      setSourcePath("");
      setSourcePathsText("");
      setSourceLabel("");
      if (error instanceof ManualImportApiError) {
        setImportState({ state: "error", code: error.code, message: error.message });
        return;
      }
      setImportState({
        state: "error",
        code: "backend_unavailable",
        message: "Manual import backend is unavailable."
      });
    }
  }

  async function handleBrowserUpload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (importState.state === "submitting" || uploadFiles.length === 0) {
      return;
    }

    const request: ManualImportUploadRequest = { files: uploadFiles };
    const trimmedLabel = sourceLabel.trim();
    if (trimmedLabel) {
      request.source_artifact_label = trimmedLabel;
    }

    setImportState({ state: "submitting" });
    try {
      const job = await submitUpload(request);
      clearUploadSelection();
      setSourceLabel("");
      setImportState({ state: "result", job });
    } catch (error: unknown) {
      clearUploadSelection();
      setSourceLabel("");
      if (error instanceof ManualImportApiError) {
        setImportState({ state: "error", code: error.code, message: error.message });
        return;
      }
      setImportState({
        state: "error",
        code: "backend_unavailable",
        message: "Manual import backend is unavailable."
      });
    }
  }

  function handleUploadFilesChange(fileList: FileList | null) {
    setUploadFiles(Array.from(fileList ?? []));
  }

  function clearUploadSelection() {
    setUploadFiles([]);
    if (uploadFileInputRef.current) {
      uploadFileInputRef.current.value = "";
    }
  }

  if (loadState.state === "loading") {
    return (
      <Shell>
        <StatusNotice title="Checking local app setup" status="unknown" />
      </Shell>
    );
  }

  if (loadState.state === "error") {
    return (
      <Shell>
        <StatusNotice title={errorTitle(loadState.code)} status={errorTone(loadState.code)}>
          {loadState.code === "incompatible_response" ? (
            <span>Expected schema: {SETUP_STATUS_SCHEMA_VERSION}</span>
          ) : (
            <span>{loadState.message}</span>
          )}
        </StatusNotice>
      </Shell>
    );
  }

  const panels = buildPanels(loadState.payload);
  const overallTone = loadState.unsafeCount > 0 ? "degraded" : statusTone(loadState.payload.status);

  return (
    <Shell>
      <section className="summaryBand" aria-labelledby="overall-status">
        <div>
          <p className="eyebrow">Mythic Edge Local App</p>
          <h1 id="overall-status">Setup Status</h1>
        </div>
        <StatusPill label={loadState.unsafeCount > 0 ? "degraded" : loadState.payload.status} tone={overallTone} />
      </section>

      {loadState.unsafeCount > 0 ? (
        <StatusNotice title="Unsafe display value redacted" status="degraded">
          <span>{loadState.unsafeCount} value was replaced with &lt;redacted_path&gt;.</span>
        </StatusNotice>
      ) : null}

      <section className="panelGrid" aria-label="Setup status sections">
        <StatusPanel
          title="Backend Reachability"
          status="ok"
          details={[{ label: "aggregate endpoint", value: "/api/app/setup-status" }]}
        />
        {panels.map((panel) => (
          <StatusPanel key={panel.title} {...panel} />
        ))}
      </section>

      <ManualImportPanel
        importState={importState}
        onSubmit={handleManualImport}
        onUploadFilesChange={handleUploadFilesChange}
        onUploadSubmit={handleBrowserUpload}
        sourceLabel={sourceLabel}
        sourcePath={sourcePath}
        sourcePathsText={sourcePathsText}
        setSourceLabel={setSourceLabel}
        setSourcePath={setSourcePath}
        setSourcePathsText={setSourcePathsText}
        uploadFileInputRef={uploadFileInputRef}
        uploadFiles={uploadFiles}
      />

      <section className="panelGrid futureGrid" aria-label="Deferred local app sections">
        <StatusPanel title="Analytics Views" status="deferred" details={[{ label: "state", value: "deferred" }]} />
        <StatusPanel title="Live Watcher" status="deferred" details={[{ label: "state", value: "deferred" }]} />
      </section>
    </Shell>
  );
}

export default SetupStatusApp;

function Shell({ children }: { children: ReactNode }) {
  return (
    <main className="appShell">
      <div className="content">{children}</div>
    </main>
  );
}

function StatusNotice({ title, status, children }: { title: string; status: string; children?: ReactNode }) {
  return (
    <section className={`notice tone-${statusTone(status)}`} aria-labelledby="status-notice">
      <div>
        <h1 id="status-notice">{title}</h1>
        {children ? <p>{children}</p> : null}
      </div>
      <StatusPill label={status} tone={statusTone(status)} />
    </section>
  );
}

function StatusPanel({ title, status, details }: Panel) {
  const tone = statusTone(status);
  return (
    <article className={`statusPanel tone-${tone}`}>
      <div className="panelHeader">
        <h2>{title}</h2>
        <StatusPill label={status} tone={tone} />
      </div>
      <dl>
        {details.map((detail) => {
          const safe = safeDisplayValue(detail.value);
          return (
            <div className={safe.redacted ? "redactedRow" : undefined} key={`${detail.label}-${String(detail.value)}`}>
              <dt>{detail.label}</dt>
              <dd>{safe.text}</dd>
            </div>
          );
        })}
      </dl>
    </article>
  );
}

function ManualImportPanel({
  importState,
  onUploadFilesChange,
  onUploadSubmit,
  onSubmit,
  sourceLabel,
  sourcePath,
  sourcePathsText,
  setSourceLabel,
  setSourcePath,
  setSourcePathsText,
  uploadFileInputRef,
  uploadFiles
}: {
  importState: ImportState;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onUploadFilesChange: (fileList: FileList | null) => void;
  onUploadSubmit: (event: FormEvent<HTMLFormElement>) => void;
  sourceLabel: string;
  sourcePath: string;
  sourcePathsText: string;
  setSourceLabel: (value: string) => void;
  setSourcePath: (value: string) => void;
  setSourcePathsText: (value: string) => void;
  uploadFileInputRef: RefObject<HTMLInputElement | null>;
  uploadFiles: File[];
}) {
  const busy = importState.state === "submitting";
  const status = manualImportStatus(importState);
  const tone = statusTone(status);
  const hasSinglePath = Boolean(sourcePath.trim());
  const hasBatchPaths = sourcePathsText
    .split(/\r?\n/)
    .some((path) => path.trim());
  const hasExactlyOneSourceMode = hasSinglePath !== hasBatchPaths;
  return (
    <section className={`manualImportPanel tone-${tone}`} aria-labelledby="manual-import-title">
      <div className="panelHeader">
        <h2 id="manual-import-title">Manual Import</h2>
        <StatusPill label={status} tone={tone} />
      </div>
      <form className="manualImportForm" onSubmit={onSubmit}>
        <label htmlFor="manual-import-path">JSONL path</label>
        <input
          autoComplete="off"
          disabled={busy}
          id="manual-import-path"
          onChange={(event) => setSourcePath(event.target.value)}
          value={sourcePath}
        />
        <label htmlFor="manual-import-batch-paths">Batch JSONL paths</label>
        <textarea
          disabled={busy}
          id="manual-import-batch-paths"
          onChange={(event) => setSourcePathsText(event.target.value)}
          rows={4}
          value={sourcePathsText}
        />
        <label htmlFor="manual-import-label">Source label</label>
        <input
          autoComplete="off"
          disabled={busy}
          id="manual-import-label"
          onChange={(event) => setSourceLabel(event.target.value)}
          value={sourceLabel}
        />
        <button disabled={busy || !hasExactlyOneSourceMode} type="submit">
          Import JSONL
        </button>
      </form>
      <form className="manualImportForm uploadImportForm" onSubmit={onUploadSubmit}>
        <label htmlFor="manual-import-upload-files">Upload JSONL files</label>
        <input
          accept=".jsonl"
          disabled={busy}
          id="manual-import-upload-files"
          multiple
          onChange={(event) => onUploadFilesChange(event.target.files)}
          ref={uploadFileInputRef}
          type="file"
        />
        <button disabled={busy || uploadFiles.length === 0} type="submit">
          Upload JSONL Files
        </button>
        {uploadFiles.length > 0 ? (
          <p className="uploadSelection">{formatUploadSelection(uploadFiles)}</p>
        ) : null}
      </form>
      {importState.state === "submitting" ? <p className="jobMessage">Import running</p> : null}
      {importState.state === "error" ? <ManualImportErrorNotice importState={importState} /> : null}
      {importState.state === "result" ? <ManualImportJobSummary job={importState.job} /> : null}
    </section>
  );
}

function ManualImportErrorNotice({ importState }: { importState: Extract<ImportState, { state: "error" }> }) {
  return (
    <section className={`jobResult tone-${errorTone(importState.code)}`} aria-label="Manual import error">
      <div className="panelHeader">
        <h2>{manualImportErrorTitle(importState.code)}</h2>
        <StatusPill label={errorTone(importState.code)} tone={errorTone(importState.code)} />
      </div>
      <p>{importState.code === "incompatible_response" ? `Expected schema: ${MANUAL_IMPORT_JOB_SCHEMA_VERSION}` : importState.message}</p>
    </section>
  );
}

function ManualImportJobSummary({ job }: { job: ManualImportJob }) {
  const sourceArtifacts = job.adapter.source_artifacts ?? job.source.source_artifacts ?? [];
  return (
    <section className={`jobResult tone-${statusTone(job.status)}`} aria-label="Manual import job summary">
      <div className="panelHeader">
        <h2>Import Job</h2>
        <StatusPill label={job.status} tone={statusTone(job.status)} />
      </div>
      <dl>
        <SummaryRow label="source" value={job.source.source_display_label} />
        <SummaryRow label="source mode" value={job.source.source_mode ?? job.adapter.source_mode ?? "single_file"} />
        <SummaryRow label="files selected" value={job.source.files_selected ?? job.adapter.files_selected ?? 1} />
        <SummaryRow label="adapter events" value={job.adapter.events_processed} />
        <SummaryRow label="adapter skipped" value={job.adapter.events_skipped} />
        <SummaryRow label="matches" value={job.ingest.row_counts.matches ?? 0} />
        <SummaryRow label="games" value={job.ingest.row_counts.games ?? 0} />
        <SummaryRow label="database" value={job.database.status} />
        <SummaryRow label="warnings" value={formatLabels(job.warnings)} />
        <SummaryRow label="errors" value={formatLabels(job.errors)} />
      </dl>
      {job.adapter.quality ? <ManualImportQualitySummary quality={job.adapter.quality} /> : null}
      {sourceArtifacts.length > 0 ? <ManualImportSourceArtifactsSummary artifacts={sourceArtifacts} /> : null}
    </section>
  );
}

function ManualImportSourceArtifactsSummary({ artifacts }: { artifacts: ManualImportSourceArtifact[] }) {
  return (
    <section className="sourceArtifactsBreakdown" aria-label="Import source artifact summary">
      <h3>Source Files</h3>
      <dl>
        {artifacts.map((artifact) => (
          <SummaryRow
            key={`${artifact.batch_index}-${artifact.source_artifact_label}`}
            label={`file ${artifact.batch_index + 1}`}
            value={formatSourceArtifact(artifact)}
          />
        ))}
      </dl>
    </section>
  );
}

function ManualImportQualitySummary({ quality }: { quality: LegacyJsonlImportQuality }) {
  return (
    <section className="qualityBreakdown" aria-label="Import quality breakdown">
      <h3>Quality Breakdown</h3>
      <dl>
        <SummaryRow label="quality status" value={quality.quality_status} />
        <SummaryRow label="processed kinds" value={formatNumberRecord(quality.processed_kind_counts)} />
        <SummaryRow label="skipped reasons" value={formatNumberRecord(quality.skipped_reason_counts)} />
        <SummaryRow label="unsupported kinds" value={formatNumberRecord(quality.unsupported_kind_counts)} />
        <SummaryRow label="output gaps" value={formatNumberRecord(quality.output_gap_counts)} />
        <SummaryRow label="adapter warning codes" value={formatLabels(quality.adapter_warning_codes)} />
        <SummaryRow label="ingest warning codes" value={formatLabels(quality.ingest_warning_codes)} />
        <SummaryRow label="routing hints" value={formatRoutingHints(quality.routing_hints)} />
      </dl>
    </section>
  );
}

function SummaryRow({ label, value }: { label: string; value: unknown }) {
  const safe = safeDisplayValue(String(value));
  return (
    <div className={safe.redacted ? "redactedRow" : undefined}>
      <dt>{label}</dt>
      <dd>{safe.text}</dd>
    </div>
  );
}

function StatusPill({ label, tone }: { label: string; tone: string }) {
  return (
    <span className={`statusPill tone-${tone}`} aria-label={`status ${label}`}>
      <span aria-hidden="true" />
      {label}
    </span>
  );
}

function buildPanels(payload: SetupStatusResponse): Panel[] {
  return [
    {
      title: "App Data",
      status: statusFromSection(payload.paths),
      details: [
        { label: "root", value: nestedValue(payload.paths, ["app_data_root", "display_path"]) },
        { label: "policy", value: payload.paths.redaction_policy }
      ]
    },
    {
      title: "Local Config",
      status: statusFromSection(payload.config),
      details: [
        { label: "file", value: nestedValue(payload.config, ["config_file", "display_path"]) },
        { label: "state", value: nestedValue(payload.config, ["config_file", "status"]) }
      ]
    },
    {
      title: "Player Log",
      status: statusFromSection(payload.player_log),
      details: [
        { label: "path", value: nestedValue(payload.player_log, ["player_log", "display_path"]) },
        { label: "state", value: nestedValue(payload.player_log, ["player_log", "status"]) }
      ]
    },
    {
      title: "Analytics Database",
      status: statusFromSection(payload.analytics_database),
      details: [
        { label: "path", value: nestedValue(payload.analytics_database, ["database", "display_path"]) },
        { label: "schema", value: nestedValue(payload.analytics_database, ["database", "schema_status"]) }
      ]
    },
    {
      title: "Migrations",
      status: statusFromSection(payload.migrations),
      details: [
        { label: "loader", value: payload.migrations.migration_status },
        { label: "available", value: migrationCount(payload.migrations) }
      ]
    },
    {
      title: "Runtime",
      status: statusFromSection(payload.runtime),
      details: [
        { label: "backend", value: nestedValue(payload.runtime, ["backend", "status"]) },
        { label: "parser runner", value: nestedValue(payload.runtime, ["parser_runner", "status"]) },
        { label: "live watcher", value: nestedValue(payload.runtime, ["live_watcher", "status"]) }
      ]
    }
  ];
}

function statusFromSection(section: SectionStatus): string {
  return typeof section.status === "string" ? section.status : "unknown";
}

function nestedValue(root: SectionStatus, path: string[]): unknown {
  let current: unknown = root;
  for (const key of path) {
    if (!isRecord(current)) {
      return "unknown";
    }
    current = current[key];
  }
  return current ?? "unknown";
}

function migrationCount(section: SectionStatus): string {
  const migrations = section.migrations;
  if (!Array.isArray(migrations)) {
    return "0";
  }
  return String(migrations.length);
}

function countUnsafeValues(payload: SetupStatusResponse): number {
  return buildPanels(payload).reduce((count, panel) => {
    return count + panel.details.filter((detail) => safeDisplayValue(detail.value).redacted).length;
  }, 0);
}

function manualImportStatus(importState: ImportState): string {
  if (importState.state === "submitting") {
    return "running";
  }
  if (importState.state === "result") {
    return importState.job.status;
  }
  if (importState.state === "error") {
    return errorTone(importState.code);
  }
  return "enabled";
}

function formatLabels(values: string[]): string {
  if (values.length === 0) {
    return "none";
  }
  return values.join(" ");
}

function formatNumberRecord(values: Record<string, number>): string {
  const entries = Object.entries(values).filter(([, count]) => count !== 0);
  if (entries.length === 0) {
    return "none";
  }
  return entries.map(([label, count]) => `${label} ${count}`).join(" ");
}

function formatRoutingHints(hints: LegacyJsonlRoutingHint[]): string {
  if (hints.length === 0) {
    return "none";
  }
  return hints.map((hint) => `${hint.code} ${hint.category} ${hint.severity} ${hint.count}`).join(" ");
}

function formatSourceArtifact(artifact: ManualImportSourceArtifact): string {
  const warnings = formatLabels(artifact.adapter_warning_codes);
  return `${artifact.source_display_label} ${artifact.status} events ${artifact.events_processed} skipped ${artifact.events_skipped} warnings ${warnings}`;
}

function formatUploadSelection(files: File[]): string {
  const labels = files.map((file) => safeUploadFileName(file.name)).join(" ");
  return `${files.length} files selected ${labels}`;
}

function safeUploadFileName(value: string): string {
  const basename = value.split(/[\\/]+/).pop()?.trim() ?? "";
  const markerText = basename.toLowerCase();
  const privateMarkers = [
    "player.log",
    "script.google.com",
    "hooks.",
    "webhook",
    "api_key",
    "apikey",
    "access_token",
    "bearer ",
    "secret",
    "password",
    "token"
  ];
  if (
    /^[A-Za-z0-9_. -]{1,80}\.jsonl$/i.test(basename) &&
    !privateMarkers.some((marker) => markerText.includes(marker))
  ) {
    return basename;
  }
  return "<selected_jsonl>";
}

function manualImportErrorTitle(code: ManualImportApiError["code"]): string {
  if (code === "malformed_response") {
    return "Malformed import response";
  }
  if (code === "incompatible_response") {
    return "Incompatible import schema";
  }
  if (code === "unsafe_api_base_url") {
    return "Unsafe API base URL";
  }
  return "Backend unavailable";
}

function errorTitle(code: SetupStatusApiError["code"]): string {
  if (code === "malformed_response") {
    return "Malformed setup response";
  }
  if (code === "incompatible_response") {
    return "Incompatible setup schema";
  }
  if (code === "unsafe_api_base_url") {
    return "Unsafe API base URL";
  }
  return "Backend unavailable";
}

function errorTone(code: SetupStatusApiError["code"]): string {
  return code === "unsafe_api_base_url" || code === "incompatible_response" ? "error" : "unavailable";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
