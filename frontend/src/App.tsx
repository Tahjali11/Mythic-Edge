import { useEffect, useRef, useState, type FormEvent, type ReactNode, type RefObject } from "react";

import "./App.css";
import {
  AnalyticsHistoryApiError,
  fetchGameHistory,
  fetchMatchHistory,
  fetchMulliganHistory,
  fetchOpeningHandHistory,
  fetchSetupStatus,
  ManualImportApiError,
  SetupStatusApiError,
  submitManualJsonlImport,
  submitManualJsonlUpload
} from "./api";
import { safeDisplayValue, statusTone } from "./status";
import {
  ANALYTICS_HISTORY_SCHEMA_VERSION,
  EARLY_GAME_HISTORY_SCHEMA_VERSION,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  SETUP_STATUS_SCHEMA_VERSION,
  type AnalyticsHistoryStatus,
  type AnalyticsHistoryStatusObject,
  type GameHistoryResponse,
  type ManualImportJob,
  type ManualImportRequest,
  type ManualImportUploadRequest,
  type MatchHistoryResponse,
  type MatchHistoryRow,
  type MulliganHistoryResponse,
  type MulliganHistoryRow,
  type OpeningHandHistoryResponse,
  type OpeningHandHistoryRow,
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
  fetchMatches?: () => Promise<MatchHistoryResponse>;
  fetchGames?: () => Promise<GameHistoryResponse>;
  fetchOpeningHands?: () => Promise<OpeningHandHistoryResponse>;
  fetchMulligans?: () => Promise<MulliganHistoryResponse>;
  submitImport?: (request: ManualImportRequest) => Promise<ManualImportJob>;
  submitUpload?: (request: ManualImportUploadRequest) => Promise<ManualImportJob>;
};

type ImportState =
  | { state: "idle" }
  | { state: "submitting" }
  | { state: "result"; job: ManualImportJob }
  | { state: "error"; code: ManualImportApiError["code"]; message: string };

type HistoryState =
  | { state: "loading" }
  | { state: "ready"; matches: MatchHistoryResponse; games: GameHistoryResponse; unsafeCount: number }
  | { state: "error"; code: AnalyticsHistoryApiError["code"]; message: string };

type EarlyGameHistoryState =
  | { state: "loading" }
  | {
      state: "ready";
      openingHands: OpeningHandHistoryResponse;
      mulligans: MulliganHistoryResponse;
      unsafeCount: number;
    }
  | { state: "error"; code: AnalyticsHistoryApiError["code"]; message: string };

type Panel = {
  title: string;
  status: string;
  details: Array<{ label: string; value: unknown }>;
};

export function SetupStatusApp({
  fetchStatus = fetchSetupStatus,
  fetchMatches = fetchMatchHistory,
  fetchGames = fetchGameHistory,
  fetchOpeningHands = fetchOpeningHandHistory,
  fetchMulligans = fetchMulliganHistory,
  submitImport = submitManualJsonlImport,
  submitUpload = submitManualJsonlUpload
}: SetupStatusAppProps) {
  const [loadState, setLoadState] = useState<LoadState>({ state: "loading" });
  const [historyState, setHistoryState] = useState<HistoryState>({ state: "loading" });
  const [earlyGameState, setEarlyGameState] = useState<EarlyGameHistoryState>({ state: "loading" });
  const [sourcePath, setSourcePath] = useState("");
  const [sourcePathsText, setSourcePathsText] = useState("");
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [uploadIgnoredFileCount, setUploadIgnoredFileCount] = useState(0);
  const [uploadSelectionMessage, setUploadSelectionMessage] = useState("");
  const [sourceLabel, setSourceLabel] = useState("");
  const [importState, setImportState] = useState<ImportState>({ state: "idle" });
  const uploadFileInputRef = useRef<HTMLInputElement>(null);
  const uploadFolderInputRef = useRef<HTMLInputElement>(null);

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

  useEffect(() => {
    let active = true;

    loadHistory();

    return () => {
      active = false;
    };

    function loadHistory() {
      setHistoryState({ state: "loading" });
      Promise.all([fetchMatches(), fetchGames()])
        .then(([matches, games]) => {
          if (!active) {
            return;
          }
          setHistoryState({
            state: "ready",
            matches,
            games,
            unsafeCount: countUnsafeHistoryValues(matches, games)
          });
        })
        .catch((error: unknown) => {
          if (!active) {
            return;
          }
          if (error instanceof AnalyticsHistoryApiError) {
            setHistoryState({ state: "error", code: error.code, message: error.message });
            return;
          }
          setHistoryState({
            state: "error",
            code: "backend_unavailable",
            message: "Analytics history backend is unavailable."
          });
      });
    }
  }, [fetchGames, fetchMatches]);

  useEffect(() => {
    let active = true;

    loadEarlyGameHistory();

    return () => {
      active = false;
    };

    function loadEarlyGameHistory() {
      setEarlyGameState({ state: "loading" });
      Promise.all([fetchOpeningHands(), fetchMulligans()])
        .then(([openingHands, mulligans]) => {
          if (!active) {
            return;
          }
          setEarlyGameState({
            state: "ready",
            openingHands,
            mulligans,
            unsafeCount: countUnsafeEarlyGameHistoryValues(openingHands, mulligans)
          });
        })
        .catch((error: unknown) => {
          if (!active) {
            return;
          }
          if (error instanceof AnalyticsHistoryApiError) {
            setEarlyGameState({ state: "error", code: error.code, message: error.message });
            return;
          }
          setEarlyGameState({
            state: "error",
            code: "backend_unavailable",
            message: "Analytics history backend is unavailable."
          });
        });
    }
  }, [fetchMulligans, fetchOpeningHands]);

  function refreshHistory() {
    setHistoryState({ state: "loading" });
    Promise.all([fetchMatches(), fetchGames()])
      .then(([matches, games]) => {
        setHistoryState({
          state: "ready",
          matches,
          games,
          unsafeCount: countUnsafeHistoryValues(matches, games)
        });
      })
      .catch((error: unknown) => {
        if (error instanceof AnalyticsHistoryApiError) {
          setHistoryState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setHistoryState({
          state: "error",
          code: "backend_unavailable",
          message: "Analytics history backend is unavailable."
        });
      });
  }

  function refreshEarlyGameHistory() {
    setEarlyGameState({ state: "loading" });
    Promise.all([fetchOpeningHands(), fetchMulligans()])
      .then(([openingHands, mulligans]) => {
        setEarlyGameState({
          state: "ready",
          openingHands,
          mulligans,
          unsafeCount: countUnsafeEarlyGameHistoryValues(openingHands, mulligans)
        });
      })
      .catch((error: unknown) => {
        if (error instanceof AnalyticsHistoryApiError) {
          setEarlyGameState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setEarlyGameState({
          state: "error",
          code: "backend_unavailable",
          message: "Analytics history backend is unavailable."
        });
      });
  }

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
    setUploadIgnoredFileCount(0);
    setUploadSelectionMessage("");
  }

  function handleUploadFolderFilesChange(fileList: FileList | null) {
    const selectedFiles = Array.from(fileList ?? []);
    const jsonlFiles = selectedFiles.filter((file) => isJsonlFileName(file.name));
    setUploadFiles(jsonlFiles);
    setUploadIgnoredFileCount(selectedFiles.length - jsonlFiles.length);
    setUploadSelectionMessage(
      selectedFiles.length > 0 && jsonlFiles.length === 0 ? "No JSONL files found in the selected folder." : ""
    );
  }

  function clearUploadSelection() {
    setUploadFiles([]);
    setUploadIgnoredFileCount(0);
    setUploadSelectionMessage("");
    if (uploadFileInputRef.current) {
      uploadFileInputRef.current.value = "";
    }
    if (uploadFolderInputRef.current) {
      uploadFolderInputRef.current.value = "";
    }
  }

  function assignUploadFolderInputRef(node: HTMLInputElement | null) {
    uploadFolderInputRef.current = node;
    if (node) {
      node.setAttribute("webkitdirectory", "");
      node.setAttribute("directory", "");
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
        onUploadFolderFilesChange={handleUploadFolderFilesChange}
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
        uploadFolderInputRef={assignUploadFolderInputRef}
        uploadFiles={uploadFiles}
        uploadIgnoredFileCount={uploadIgnoredFileCount}
        uploadSelectionMessage={uploadSelectionMessage}
      />

      <AnalyticsHistorySection historyState={historyState} onRefresh={refreshHistory} />
      <EarlyGameHistorySection earlyGameState={earlyGameState} onRefresh={refreshEarlyGameHistory} />

      <section className="panelGrid futureGrid" aria-label="Deferred local app sections">
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
  onUploadFolderFilesChange,
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
  uploadFolderInputRef,
  uploadFiles,
  uploadIgnoredFileCount,
  uploadSelectionMessage
}: {
  importState: ImportState;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
  onUploadFolderFilesChange: (fileList: FileList | null) => void;
  onUploadFilesChange: (fileList: FileList | null) => void;
  onUploadSubmit: (event: FormEvent<HTMLFormElement>) => void;
  sourceLabel: string;
  sourcePath: string;
  sourcePathsText: string;
  setSourceLabel: (value: string) => void;
  setSourcePath: (value: string) => void;
  setSourcePathsText: (value: string) => void;
  uploadFileInputRef: RefObject<HTMLInputElement | null>;
  uploadFolderInputRef: (node: HTMLInputElement | null) => void;
  uploadFiles: File[];
  uploadIgnoredFileCount: number;
  uploadSelectionMessage: string;
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
        <label htmlFor="manual-import-upload-folder">Upload JSONL folder</label>
        <input
          accept=".jsonl"
          disabled={busy}
          id="manual-import-upload-folder"
          multiple
          onChange={(event) => onUploadFolderFilesChange(event.target.files)}
          ref={uploadFolderInputRef}
          type="file"
        />
        <button disabled={busy || uploadFiles.length === 0} type="submit">
          Upload JSONL Files
        </button>
        {uploadFiles.length > 0 ? (
          <p className="uploadSelection">{formatUploadSelection(uploadFiles)}</p>
        ) : null}
        {uploadIgnoredFileCount > 0 ? (
          <p className="uploadSelection">{formatIgnoredUploadFiles(uploadIgnoredFileCount)}</p>
        ) : null}
        {uploadSelectionMessage ? <p className="uploadSelection">{uploadSelectionMessage}</p> : null}
      </form>
      {importState.state === "submitting" ? <p className="jobMessage">Import running</p> : null}
      {importState.state === "error" ? <ManualImportErrorNotice importState={importState} /> : null}
      {importState.state === "result" ? <ManualImportJobSummary job={importState.job} /> : null}
    </section>
  );
}

function AnalyticsHistorySection({
  historyState,
  onRefresh
}: {
  historyState: HistoryState;
  onRefresh: () => void;
}) {
  const status = analyticsHistoryStatus(historyState);
  const tone = statusTone(status);
  return (
    <section className={`analyticsHistorySection tone-${tone}`} aria-labelledby="analytics-history-title">
      <div className="panelHeader analyticsHistoryHeader">
        <div>
          <h2 id="analytics-history-title">Analytics History</h2>
        </div>
        <div className="historyHeaderActions">
          <StatusPill label={status} tone={tone} />
          <button disabled={historyState.state === "loading"} onClick={onRefresh} type="button">
            Refresh History
          </button>
        </div>
      </div>
      {historyState.state === "loading" ? <p className="historyStateMessage">Loading history</p> : null}
      {historyState.state === "error" ? <AnalyticsHistoryErrorNotice historyState={historyState} /> : null}
      {historyState.state === "ready" ? (
        <>
          {historyState.unsafeCount > 0 ? (
            <p className="historyStateMessage">{historyState.unsafeCount} history value was redacted.</p>
          ) : null}
          <div className="historySummaryGrid" aria-label="Analytics history summary">
            <HistorySummaryPanel title="Matches" response={historyState.matches} />
            <HistorySummaryPanel title="Games" response={historyState.games} />
          </div>
          <MatchHistoryTable response={historyState.matches} />
          <GameHistoryTable response={historyState.games} />
        </>
      ) : null}
    </section>
  );
}

function EarlyGameHistorySection({
  earlyGameState,
  onRefresh
}: {
  earlyGameState: EarlyGameHistoryState;
  onRefresh: () => void;
}) {
  const status = earlyGameHistoryStatus(earlyGameState);
  const tone = statusTone(status);
  return (
    <section className={`analyticsHistorySection tone-${tone}`} aria-labelledby="early-game-history-title">
      <div className="panelHeader analyticsHistoryHeader">
        <div>
          <h2 id="early-game-history-title">Early Game History</h2>
        </div>
        <div className="historyHeaderActions">
          <StatusPill label={status} tone={tone} />
          <button disabled={earlyGameState.state === "loading"} onClick={onRefresh} type="button">
            Refresh Early Game
          </button>
        </div>
      </div>
      {earlyGameState.state === "loading" ? <p className="historyStateMessage">Loading early game history</p> : null}
      {earlyGameState.state === "error" ? <EarlyGameHistoryErrorNotice earlyGameState={earlyGameState} /> : null}
      {earlyGameState.state === "ready" ? (
        <>
          {earlyGameState.unsafeCount > 0 ? (
            <p className="historyStateMessage">{earlyGameState.unsafeCount} early game value was redacted.</p>
          ) : null}
          <div className="historySummaryGrid" aria-label="Early game history summary">
            <EarlyGameSummaryPanel title="Opening Hands" response={earlyGameState.openingHands} />
            <EarlyGameSummaryPanel title="Mulligans" response={earlyGameState.mulligans} />
          </div>
          <OpeningHandHistoryTable response={earlyGameState.openingHands} />
          <MulliganHistoryTable response={earlyGameState.mulligans} />
        </>
      ) : null}
    </section>
  );
}

function EarlyGameHistoryErrorNotice({
  earlyGameState
}: {
  earlyGameState: Extract<EarlyGameHistoryState, { state: "error" }>;
}) {
  return (
    <section className={`historyNotice tone-${errorTone(earlyGameState.code)}`} aria-label="Early game history error">
      <div className="panelHeader">
        <h3>{analyticsHistoryErrorTitle(earlyGameState.code)}</h3>
        <StatusPill label={errorTone(earlyGameState.code)} tone={errorTone(earlyGameState.code)} />
      </div>
      <p>
        {earlyGameState.code === "incompatible_response"
          ? `Expected schema: ${EARLY_GAME_HISTORY_SCHEMA_VERSION}`
          : earlyGameState.message}
      </p>
    </section>
  );
}

function AnalyticsHistoryErrorNotice({ historyState }: { historyState: Extract<HistoryState, { state: "error" }> }) {
  return (
    <section className={`historyNotice tone-${errorTone(historyState.code)}`} aria-label="Analytics history error">
      <div className="panelHeader">
        <h3>{analyticsHistoryErrorTitle(historyState.code)}</h3>
        <StatusPill label={errorTone(historyState.code)} tone={errorTone(historyState.code)} />
      </div>
      <p>
        {historyState.code === "incompatible_response"
          ? `Expected schema: ${ANALYTICS_HISTORY_SCHEMA_VERSION}`
          : historyState.message}
      </p>
    </section>
  );
}

function EarlyGameSummaryPanel({
  title,
  response
}: {
  title: string;
  response: OpeningHandHistoryResponse | MulliganHistoryResponse;
}) {
  return (
    <article className={`historySummaryPanel tone-${statusTone(response.status)}`}>
      <div className="panelHeader">
        <h3>{title}</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      <dl>
        <SummaryRow label="rows" value={response.summary.row_count} />
        <SummaryRow label="cards" value={response.summary.card_row_count} />
        <SummaryRow label="degraded" value={response.summary.degraded_row_count} />
        <SummaryRow label="unavailable" value={response.summary.unavailable_row_count} />
        <SummaryRow label="conflict" value={response.summary.conflict_row_count} />
        <SummaryRow label="schema" value={response.database.schema_status} />
      </dl>
    </article>
  );
}

function HistorySummaryPanel({
  title,
  response
}: {
  title: string;
  response: MatchHistoryResponse | GameHistoryResponse;
}) {
  return (
    <article className={`historySummaryPanel tone-${statusTone(response.status)}`}>
      <div className="panelHeader">
        <h3>{title}</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      <dl>
        <SummaryRow label="rows" value={response.summary.row_count} />
        <SummaryRow label="degraded" value={response.summary.degraded_row_count} />
        <SummaryRow label="unavailable" value={response.summary.unavailable_row_count} />
        <SummaryRow label="conflict" value={response.summary.conflict_row_count} />
        <SummaryRow label="schema" value={response.database.schema_status} />
      </dl>
    </article>
  );
}

function OpeningHandHistoryTable({ response }: { response: OpeningHandHistoryResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="opening-hand-history-title">
      <div className="panelHeader">
        <h3 id="opening-hand-history-title">Opening Hands</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("opening hand", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Result</th>
                <th scope="col">Hand</th>
                <th scope="col">Cards</th>
                <th scope="col">Queue</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.opening_hand_id}>
                  <SafeCell value={`${row.match_id} game ${row.game_number}`} />
                  <SafeCell value={row.local_result ?? row.match_result ?? matchWinLabel(row.match_win)} />
                  <SafeCell value={openingHandSizeSummary(row)} />
                  <SafeCell value={openingHandCardsSummary(row)} />
                  <SafeCell value={row.queue_name ?? row.format_name} />
                  <SafeCell
                    value={statusSummary(
                      row.opening_hand_status,
                      row.game_status,
                      row.game_result_status,
                      row.match_result_status,
                      row.context_status
                    )}
                  />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function MulliganHistoryTable({ response }: { response: MulliganHistoryResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="mulligan-history-title">
      <div className="panelHeader">
        <h3 id="mulligan-history-title">Mulligans</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("mulligan", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Count</th>
                <th scope="col">Decision</th>
                <th scope="col">Cards</th>
                <th scope="col">Result</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.mulligan_event_id}>
                  <SafeCell value={`${row.match_id} game ${row.game_number}`} />
                  <SafeCell value={row.mulligan_count ?? row.ordinal_or_count} />
                  <SafeCell value={row.decision_detail} />
                  <SafeCell value={mulliganCardsSummary(row)} />
                  <SafeCell value={row.local_result ?? row.match_result ?? matchWinLabel(row.match_win)} />
                  <SafeCell
                    value={statusSummary(
                      row.mulligan_status,
                      row.game_status,
                      row.game_result_status,
                      row.match_result_status,
                      row.context_status
                    )}
                  />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function MatchHistoryTable({ response }: { response: MatchHistoryResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="match-history-title">
      <div className="panelHeader">
        <h3 id="match-history-title">Match History</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("match", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Match</th>
                <th scope="col">Completed</th>
                <th scope="col">Result</th>
                <th scope="col">Games</th>
                <th scope="col">Queue</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.match_id}>
                  <SafeCell value={row.match_id} />
                  <SafeCell value={row.match_completed_at ?? row.match_started_at} />
                  <SafeCell value={row.match_result ?? matchWinLabel(row.match_win)} />
                  <SafeCell value={gamesSummary(row)} />
                  <SafeCell value={row.queue_name ?? row.format_name} />
                  <SafeCell value={statusSummary(row.match_status, row.result_status, row.context_status)} />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function GameHistoryTable({ response }: { response: GameHistoryResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="game-history-title">
      <div className="panelHeader">
        <h3 id="game-history-title">Game History</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("game", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Completed</th>
                <th scope="col">Result</th>
                <th scope="col">Play/Draw</th>
                <th scope="col">Turns</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.game_id}>
                  <SafeCell value={`${row.match_id} game ${row.game_number}`} />
                  <SafeCell value={row.game_completed_at ?? row.game_started_at} />
                  <SafeCell value={row.local_result} />
                  <SafeCell value={row.play_draw} />
                  <SafeCell value={row.turn_count} />
                  <SafeCell value={statusSummary(row.game_status, row.result_status, row.context_status)} />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function SafeCell({ value }: { value: unknown }) {
  const safe = safeDisplayValue(value ?? "unknown");
  return <td className={safe.redacted ? "redactedRow" : undefined}>{safe.text}</td>;
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

function countUnsafeHistoryValues(matches: MatchHistoryResponse, games: GameHistoryResponse): number {
  const values: unknown[] = [
    matches.database.display_path,
    games.database.display_path,
    ...matches.warnings,
    ...matches.errors,
    ...games.warnings,
    ...games.errors
  ];
  for (const row of matches.rows) {
    values.push(
      row.match_id,
      row.parser_match_key,
      row.match_started_at,
      row.match_completed_at,
      row.match_result,
      row.queue_name,
      row.format_name,
      row.event_id,
      statusSummary(row.match_status, row.result_status, row.context_status)
    );
  }
  for (const row of games.rows) {
    values.push(
      row.game_id,
      row.match_id,
      row.game_started_at,
      row.game_completed_at,
      row.local_result,
      row.pre_postboard_label,
      row.play_draw,
      row.queue_name,
      row.format_name,
      row.event_id,
      statusSummary(row.game_status, row.result_status, row.context_status)
    );
  }
  return values.filter((value) => safeDisplayValue(value ?? "unknown").redacted).length;
}

function countUnsafeEarlyGameHistoryValues(
  openingHands: OpeningHandHistoryResponse,
  mulligans: MulliganHistoryResponse
): number {
  const values: unknown[] = [
    openingHands.database.display_path,
    mulligans.database.display_path,
    ...openingHands.warnings,
    ...openingHands.errors,
    ...mulligans.warnings,
    ...mulligans.errors
  ];
  for (const row of openingHands.rows) {
    values.push(
      row.opening_hand_id,
      row.match_id,
      row.game_id,
      row.local_result,
      row.play_draw,
      row.pre_postboard_label,
      row.match_result,
      row.queue_name,
      row.format_name,
      row.event_id,
      openingHandCardsSummary(row),
      statusSummary(
        row.opening_hand_status,
        row.game_status,
        row.game_result_status,
        row.match_result_status,
        row.context_status
      )
    );
  }
  for (const row of mulligans.rows) {
    values.push(
      row.mulligan_event_id,
      row.match_id,
      row.game_id,
      row.ordinal_or_count,
      row.decision_detail,
      row.local_result,
      row.play_draw,
      row.pre_postboard_label,
      row.match_result,
      row.queue_name,
      row.format_name,
      row.event_id,
      mulliganCardsSummary(row),
      statusSummary(
        row.mulligan_status,
        row.game_status,
        row.game_result_status,
        row.match_result_status,
        row.context_status
      )
    );
  }
  return values.filter((value) => safeDisplayValue(value ?? "unknown").redacted).length;
}

function analyticsHistoryStatus(historyState: HistoryState): string {
  if (historyState.state === "loading") {
    return "loading";
  }
  if (historyState.state === "error") {
    return errorTone(historyState.code);
  }
  if (historyState.unsafeCount > 0) {
    return "degraded";
  }
  const statuses: AnalyticsHistoryStatus[] = [historyState.matches.status, historyState.games.status];
  const priorityStatuses: AnalyticsHistoryStatus[] = ["error", "unavailable", "degraded", "missing"];
  for (const status of priorityStatuses) {
    if (statuses.includes(status)) {
      return status;
    }
  }
  if (statuses.every((status) => status === "empty")) {
    return "empty";
  }
  return "ok";
}

function earlyGameHistoryStatus(earlyGameState: EarlyGameHistoryState): string {
  if (earlyGameState.state === "loading") {
    return "loading";
  }
  if (earlyGameState.state === "error") {
    return errorTone(earlyGameState.code);
  }
  if (earlyGameState.unsafeCount > 0) {
    return "degraded";
  }
  const statuses: AnalyticsHistoryStatus[] = [earlyGameState.openingHands.status, earlyGameState.mulligans.status];
  const priorityStatuses: AnalyticsHistoryStatus[] = ["error", "unavailable", "degraded", "missing"];
  for (const status of priorityStatuses) {
    if (statuses.includes(status)) {
      return status;
    }
  }
  if (statuses.every((status) => status === "empty")) {
    return "empty";
  }
  return "ok";
}

function historyEmptyLabel(kind: string, status: string): string {
  if (status === "missing") {
    return `No ${kind} history database`;
  }
  if (status === "degraded") {
    return `${kind} history schema not current`;
  }
  if (status === "error") {
    return `${kind} history unavailable`;
  }
  return `No ${kind} rows`;
}

function openingHandSizeSummary(row: OpeningHandHistoryRow): string {
  const handSize = row.hand_size ?? "unknown";
  const exactCount = row.exact_card_count ?? "unknown";
  return `${handSize} cards count ${exactCount}`;
}

function openingHandCardsSummary(row: OpeningHandHistoryRow): string {
  if (row.cards.length === 0) {
    return "no cards";
  }
  return row.cards.map((card) => {
    const identity = card.card_name ?? (card.grp_id === null ? "unknown" : `grp ${card.grp_id}`);
    const resolution = card.name_resolution_status ?? card.identity_hint_source ?? "unknown";
    return `${card.card_position}: ${identity} ${resolution} ${card.grp_id ?? "unknown"}`;
  }).join(" ");
}

function mulliganCardsSummary(row: MulliganHistoryRow): string {
  if (row.cards.length === 0) {
    return "no cards";
  }
  return row.cards.map((card) => {
    const identity = card.card_name ?? (card.grp_id === null ? "unknown" : `grp ${card.grp_id}`);
    const source = card.identity_hint_source ?? "unknown";
    return `${card.card_position}: ${card.card_action} ${identity} ${source} ${card.grp_id ?? "unknown"}`;
  }).join(" ");
}

function matchWinLabel(value: number | null): string {
  if (value === 1) {
    return "win";
  }
  if (value === 0) {
    return "loss";
  }
  return "unknown";
}

function gamesSummary(row: MatchHistoryRow): string {
  const won = row.games_won ?? "unknown";
  const lost = row.games_lost ?? "unknown";
  const total = row.total_games ?? "unknown";
  return `${won}-${lost} of ${total}`;
}

function statusSummary(...statuses: Array<AnalyticsHistoryStatusObject | null>): string {
  const included = statuses.filter((status): status is AnalyticsHistoryStatusObject => status !== null);
  if (included.length === 0) {
    return "not joined";
  }
  const priority = included.find(
    (status) =>
      status.drift_status === "conflict" ||
      status.value_source === "conflict" ||
      status.drift_status === "degraded" ||
      status.confidence === "low" ||
      status.confidence === "unknown" ||
      status.availability_status !== "available"
  );
  const status = priority ?? included[0];
  return `${status.value_source} ${status.confidence} ${status.finality} ${status.drift_status} ${status.availability_status}`;
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

function formatIgnoredUploadFiles(count: number): string {
  return count === 1 ? "1 non-JSONL file ignored" : `${count} non-JSONL files ignored`;
}

function isJsonlFileName(value: string): boolean {
  return value.trim().toLowerCase().endsWith(".jsonl");
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

function analyticsHistoryErrorTitle(code: AnalyticsHistoryApiError["code"]): string {
  if (code === "malformed_response") {
    return "Malformed history response";
  }
  if (code === "incompatible_response") {
    return "Incompatible history schema";
  }
  if (code === "unsafe_api_base_url") {
    return "Unsafe API base URL";
  }
  return "Analytics history unavailable";
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
