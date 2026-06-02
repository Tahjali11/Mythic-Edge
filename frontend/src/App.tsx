import { useEffect, useRef, useState, type FormEvent, type ReactNode, type RefObject } from "react";

import "./App.css";
import {
  AnalyticsHistoryApiError,
  fetchGame1PostboardSplitReview,
  fetchGameHistory,
  fetchGameplayActionReview,
  fetchMatchJournal,
  fetchMatchJournalUnattachedNote,
  fetchMatchHistory,
  fetchMulliganHistory,
  fetchOpponentCardObservationReview,
  fetchOpeningHandHistory,
  fetchPlayDrawSplitReview,
  fetchSetupStatus,
  ManualImportApiError,
  MatchJournalApiError,
  SetupStatusApiError,
  submitMatchJournalDisplayCorrection,
  submitMatchJournalExperimentLabel,
  submitMatchJournalNote,
  submitMatchJournalOpponentLabels,
  submitMatchJournalReviewFlag,
  submitManualJsonlImport,
  submitManualJsonlUpload
} from "./api";
import { safeDisplayValue, statusTone } from "./status";
import {
  ACTION_REVIEW_SCHEMA_VERSION,
  ANALYTICS_HISTORY_SCHEMA_VERSION,
  EARLY_GAME_HISTORY_SCHEMA_VERSION,
  LIVE_PLAYER_LOG_STATUS_OBJECT,
  LIVE_STATUS_SCHEMA_VERSION,
  LIVE_WATCHER_STATUS_OBJECT,
  SPLIT_REVIEW_SCHEMA_VERSION,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  SETUP_STATUS_SCHEMA_VERSION,
  type AnalyticsHistoryStatus,
  type AnalyticsHistoryStatusObject,
  type Game1PostboardSplitReviewResponse,
  type Game1PostboardSplitRow,
  type GameHistoryResponse,
  type GameHistoryRow,
  type GameplayActionReviewResponse,
  type GameplayActionReviewRow,
  type LivePlayerLogStatusResponse,
  type LiveWatcherStatusResponse,
  type ManualImportJob,
  type ManualImportRequest,
  type ManualImportUploadRequest,
  type MatchJournalContext,
  type MatchJournalDisplayCorrectionRequest,
  type MatchJournalExperimentLabelRequest,
  type MatchJournalAttachedNoteRequest,
  type MatchJournalNoteRequest,
  type MatchJournalOpponentLabelsRequest,
  type MatchJournalResponse,
  type MatchJournalReviewFlagRequest,
  type MatchJournalUnattachedNoteReadbackRequest,
  type MatchJournalUnattachedNoteRequest,
  type MatchHistoryResponse,
  type MatchHistoryRow,
  type MulliganHistoryResponse,
  type MulliganHistoryRow,
  type OpeningHandHistoryResponse,
  type OpeningHandHistoryRow,
  type OpponentCardObservationReviewResponse,
  type OpponentCardObservationReviewRow,
  type PlayDrawSplitReviewResponse,
  type PlayDrawSplitRow,
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
  fetchGameplayActions?: () => Promise<GameplayActionReviewResponse>;
  fetchOpponentObservations?: () => Promise<OpponentCardObservationReviewResponse>;
  fetchPlayDrawSplits?: () => Promise<PlayDrawSplitReviewResponse>;
  fetchGame1PostboardSplits?: () => Promise<Game1PostboardSplitReviewResponse>;
  fetchJournal?: (context: MatchJournalContext) => Promise<MatchJournalResponse>;
  fetchJournalUnattachedNote?: (request: MatchJournalUnattachedNoteReadbackRequest) => Promise<MatchJournalResponse>;
  submitJournalNote?: (request: MatchJournalNoteRequest) => Promise<MatchJournalResponse>;
  submitJournalUnattachedNote?: (request: MatchJournalUnattachedNoteRequest) => Promise<MatchJournalResponse>;
  submitJournalOpponentLabels?: (request: MatchJournalOpponentLabelsRequest) => Promise<MatchJournalResponse>;
  submitJournalReviewFlag?: (request: MatchJournalReviewFlagRequest) => Promise<MatchJournalResponse>;
  submitJournalExperimentLabel?: (request: MatchJournalExperimentLabelRequest) => Promise<MatchJournalResponse>;
  submitJournalDisplayCorrection?: (request: MatchJournalDisplayCorrectionRequest) => Promise<MatchJournalResponse>;
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

type ActionReviewState =
  | { state: "loading" }
  | {
      state: "ready";
      gameplayActions: GameplayActionReviewResponse;
      opponentObservations: OpponentCardObservationReviewResponse;
      unsafeCount: number;
    }
  | { state: "error"; code: AnalyticsHistoryApiError["code"]; message: string };

type SplitReviewState =
  | { state: "loading" }
  | {
      state: "ready";
      playDrawSplits: PlayDrawSplitReviewResponse;
      game1PostboardSplits: Game1PostboardSplitReviewResponse;
      unsafeCount: number;
    }
  | { state: "error"; code: AnalyticsHistoryApiError["code"]; message: string };

type MatchJournalState =
  | { state: "loading" }
  | { state: "ready"; payload: MatchJournalResponse; unsafeCount: number }
  | { state: "error"; code: MatchJournalApiError["code"]; message: string };

type MatchJournalSubmitState =
  | { state: "idle" }
  | { state: "submitting" }
  | { state: "result"; payload: MatchJournalResponse }
  | { state: "error"; code: MatchJournalApiError["code"]; message: string };

type MatchJournalSmokeReadbackState =
  | { state: "idle" }
  | { state: "loading"; journalNoteId: string }
  | { state: "ready"; journalNoteId: string; payload: MatchJournalResponse }
  | { state: "error"; journalNoteId?: string; code: MatchJournalApiError["code"]; message: string };

type MatchJournalContextSummary = {
  context: MatchJournalContext | null;
  match: MatchHistoryRow | null;
  game: GameHistoryRow | null;
};

type Panel = {
  title: string;
  status: string;
  details: Array<{ label: string; value: unknown }>;
};

const UNATTACHED_SMOKE_NOTE_PREFIX = "MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW";
const UNATTACHED_SMOKE_NOTE_STORAGE_KEY = "mythic_edge.match_journal.unattached_smoke_note_id";

export function SetupStatusApp({
  fetchStatus = fetchSetupStatus,
  fetchMatches = fetchMatchHistory,
  fetchGames = fetchGameHistory,
  fetchOpeningHands = fetchOpeningHandHistory,
  fetchMulligans = fetchMulliganHistory,
  fetchGameplayActions = fetchGameplayActionReview,
  fetchOpponentObservations = fetchOpponentCardObservationReview,
  fetchPlayDrawSplits = fetchPlayDrawSplitReview,
  fetchGame1PostboardSplits = fetchGame1PostboardSplitReview,
  fetchJournal = fetchMatchJournal,
  fetchJournalUnattachedNote = fetchMatchJournalUnattachedNote,
  submitJournalNote = submitMatchJournalNote,
  submitJournalUnattachedNote = submitMatchJournalNote,
  submitJournalOpponentLabels = submitMatchJournalOpponentLabels,
  submitJournalReviewFlag = submitMatchJournalReviewFlag,
  submitJournalExperimentLabel = submitMatchJournalExperimentLabel,
  submitJournalDisplayCorrection = submitMatchJournalDisplayCorrection,
  submitImport = submitManualJsonlImport,
  submitUpload = submitManualJsonlUpload
}: SetupStatusAppProps) {
  const [loadState, setLoadState] = useState<LoadState>({ state: "loading" });
  const [historyState, setHistoryState] = useState<HistoryState>({ state: "loading" });
  const [earlyGameState, setEarlyGameState] = useState<EarlyGameHistoryState>({ state: "loading" });
  const [actionReviewState, setActionReviewState] = useState<ActionReviewState>({ state: "loading" });
  const [splitReviewState, setSplitReviewState] = useState<SplitReviewState>({ state: "loading" });
  const [journalState, setJournalState] = useState<MatchJournalState>({ state: "loading" });
  const [journalSubmitState, setJournalSubmitState] = useState<MatchJournalSubmitState>({ state: "idle" });
  const [journalSmokeReadbackState, setJournalSmokeReadbackState] = useState<MatchJournalSmokeReadbackState>({
    state: "idle"
  });
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

  useEffect(() => {
    let active = true;

    loadActionReview();

    return () => {
      active = false;
    };

    function loadActionReview() {
      setActionReviewState({ state: "loading" });
      Promise.all([fetchGameplayActions(), fetchOpponentObservations()])
        .then(([gameplayActions, opponentObservations]) => {
          if (!active) {
            return;
          }
          setActionReviewState({
            state: "ready",
            gameplayActions,
            opponentObservations,
            unsafeCount: countUnsafeActionReviewValues(gameplayActions, opponentObservations)
          });
        })
        .catch((error: unknown) => {
          if (!active) {
            return;
          }
          if (error instanceof AnalyticsHistoryApiError) {
            setActionReviewState({ state: "error", code: error.code, message: error.message });
            return;
          }
          setActionReviewState({
            state: "error",
            code: "backend_unavailable",
            message: "Analytics history backend is unavailable."
          });
        });
    }
  }, [fetchGameplayActions, fetchOpponentObservations]);

  useEffect(() => {
    let active = true;

    loadSplitReview();

    return () => {
      active = false;
    };

    function loadSplitReview() {
      setSplitReviewState({ state: "loading" });
      Promise.all([fetchPlayDrawSplits(), fetchGame1PostboardSplits()])
        .then(([playDrawSplits, game1PostboardSplits]) => {
          if (!active) {
            return;
          }
          setSplitReviewState({
            state: "ready",
            playDrawSplits,
            game1PostboardSplits,
            unsafeCount: countUnsafeSplitReviewValues(playDrawSplits, game1PostboardSplits)
          });
        })
        .catch((error: unknown) => {
          if (!active) {
            return;
          }
          if (error instanceof AnalyticsHistoryApiError) {
            setSplitReviewState({ state: "error", code: error.code, message: error.message });
            return;
          }
          setSplitReviewState({
            state: "error",
            code: "backend_unavailable",
            message: "Analytics history backend is unavailable."
          });
        });
    }
  }, [fetchGame1PostboardSplits, fetchPlayDrawSplits]);

  useEffect(() => {
    let active = true;
    const contextSummary = buildMatchJournalContextSummary(historyState);

    if (historyState.state === "loading") {
      setJournalState({ state: "loading" });
      return () => {
        active = false;
      };
    }
    if (historyState.state === "error") {
      setJournalState({
        state: "error",
        code: "backend_unavailable",
        message: "Match Journal context is unavailable."
      });
      return () => {
        active = false;
      };
    }
    if (contextSummary.context === null) {
      setJournalState({
        state: "ready",
        payload: emptyMatchJournalPayload(),
        unsafeCount: 0
      });
      return () => {
        active = false;
      };
    }

    setJournalState({ state: "loading" });
    fetchJournal(contextSummary.context)
      .then((payload) => {
        if (!active) {
          return;
        }
        setJournalState({ state: "ready", payload, unsafeCount: countUnsafeJournalValues(payload) });
      })
      .catch((error: unknown) => {
        if (!active) {
          return;
        }
        if (error instanceof MatchJournalApiError) {
          setJournalState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setJournalState({
          state: "error",
          code: "backend_unavailable",
          message: "Match Journal backend is unavailable."
        });
      });

    return () => {
      active = false;
    };
  }, [fetchJournal, historyState]);

  useEffect(() => {
    let active = true;
    const contextSummary = buildMatchJournalContextSummary(historyState);

    if (historyState.state !== "ready" || contextSummary.context !== null) {
      setJournalSmokeReadbackState({ state: "idle" });
      return () => {
        active = false;
      };
    }

    const journalNoteId = readStoredUnattachedSmokeNoteId();
    if (journalNoteId === null) {
      setJournalSmokeReadbackState({ state: "idle" });
      return () => {
        active = false;
      };
    }

    setJournalSmokeReadbackState({ state: "loading", journalNoteId });
    fetchJournalUnattachedNote({ journal_note_id: journalNoteId, note_scope: "unattached" })
      .then((payload) => {
        if (!active) {
          return;
        }
        setJournalSmokeReadbackState({ state: "ready", journalNoteId, payload });
      })
      .catch((error: unknown) => {
        if (!active) {
          return;
        }
        if (error instanceof MatchJournalApiError) {
          setJournalSmokeReadbackState({ state: "error", journalNoteId, code: error.code, message: error.message });
          return;
        }
        setJournalSmokeReadbackState({
          state: "error",
          journalNoteId,
          code: "backend_unavailable",
          message: "Match Journal unattached note readback is unavailable."
        });
      });

    return () => {
      active = false;
    };
  }, [fetchJournalUnattachedNote, historyState]);

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

  function refreshActionReview() {
    setActionReviewState({ state: "loading" });
    Promise.all([fetchGameplayActions(), fetchOpponentObservations()])
      .then(([gameplayActions, opponentObservations]) => {
        setActionReviewState({
          state: "ready",
          gameplayActions,
          opponentObservations,
          unsafeCount: countUnsafeActionReviewValues(gameplayActions, opponentObservations)
        });
      })
      .catch((error: unknown) => {
        if (error instanceof AnalyticsHistoryApiError) {
          setActionReviewState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setActionReviewState({
          state: "error",
          code: "backend_unavailable",
          message: "Analytics history backend is unavailable."
        });
      });
  }

  function refreshSplitReview() {
    setSplitReviewState({ state: "loading" });
    Promise.all([fetchPlayDrawSplits(), fetchGame1PostboardSplits()])
      .then(([playDrawSplits, game1PostboardSplits]) => {
        setSplitReviewState({
          state: "ready",
          playDrawSplits,
          game1PostboardSplits,
          unsafeCount: countUnsafeSplitReviewValues(playDrawSplits, game1PostboardSplits)
        });
      })
      .catch((error: unknown) => {
        if (error instanceof AnalyticsHistoryApiError) {
          setSplitReviewState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setSplitReviewState({
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

  async function runJournalMutation(
    action: (context: MatchJournalContext) => Promise<MatchJournalResponse>
  ): Promise<boolean> {
    const context = buildMatchJournalContextSummary(historyState).context;
    if (context === null || journalSubmitState.state === "submitting") {
      return false;
    }

    setJournalSubmitState({ state: "submitting" });
    try {
      const payload = await action(context);
      setJournalSubmitState({ state: "result", payload });
      return isSuccessfulMatchJournalSubmit(payload);
    } catch (error: unknown) {
      if (error instanceof MatchJournalApiError) {
        setJournalSubmitState({ state: "error", code: error.code, message: error.message });
        return false;
      }
      setJournalSubmitState({
        state: "error",
        code: "backend_unavailable",
        message: "Match Journal backend is unavailable."
      });
      return false;
    }
  }

  function handleJournalNoteSubmit(request: Omit<MatchJournalAttachedNoteRequest, "context">): Promise<boolean> {
    return runJournalMutation((context) => submitJournalNote({ ...request, context }));
  }

  async function handleUnattachedSmokeNoteSubmit(): Promise<boolean> {
    if (journalSubmitState.state === "submitting" || buildMatchJournalContextSummary(historyState).context !== null) {
      return false;
    }
    if (journalState.state !== "ready" || journalState.payload.status === "unavailable" || journalState.payload.status === "error") {
      return false;
    }

    setJournalSubmitState({ state: "submitting" });
    const noteText = `${UNATTACHED_SMOKE_NOTE_PREFIX} ${new Date().toISOString()}`;
    try {
      const payload = await submitJournalUnattachedNote({
        note_scope: "unattached",
        note_text: noteText,
        author_label: "codex_smoke_test",
        source_surface: "local_tool",
        privacy_label: "sanitized_fixture",
        note_format: "plain_text",
        priority_label: "normal"
      });
      setJournalSubmitState({ state: "result", payload });
      const journalNoteId = journalPrimaryRecordId(payload);
      if (journalNoteId !== null) {
        storeUnattachedSmokeNoteId(journalNoteId);
        await readBackUnattachedSmokeNote(journalNoteId);
      } else if (isSuccessfulMatchJournalSubmit(payload)) {
        setJournalSmokeReadbackState({
          state: "error",
          code: "malformed_response",
          message: "Match Journal response is missing a journal note id."
        });
      }
      return isSuccessfulMatchJournalSubmit(payload);
    } catch (error: unknown) {
      if (error instanceof MatchJournalApiError) {
        setJournalSubmitState({ state: "error", code: error.code, message: error.message });
        return false;
      }
      setJournalSubmitState({
        state: "error",
        code: "backend_unavailable",
        message: "Match Journal backend is unavailable."
      });
      return false;
    }
  }

  async function readBackUnattachedSmokeNote(journalNoteId: string) {
    setJournalSmokeReadbackState({ state: "loading", journalNoteId });
    try {
      const payload = await fetchJournalUnattachedNote({ journal_note_id: journalNoteId, note_scope: "unattached" });
      setJournalSmokeReadbackState({ state: "ready", journalNoteId, payload });
    } catch (error: unknown) {
      if (error instanceof MatchJournalApiError) {
        setJournalSmokeReadbackState({ state: "error", journalNoteId, code: error.code, message: error.message });
        return;
      }
      setJournalSmokeReadbackState({
        state: "error",
        journalNoteId,
        code: "backend_unavailable",
        message: "Match Journal unattached note readback is unavailable."
      });
    }
  }

  function handleJournalOpponentLabelsSubmit(
    request: Omit<MatchJournalOpponentLabelsRequest, "context">
  ): Promise<boolean> {
    return runJournalMutation((context) => submitJournalOpponentLabels({ ...request, context }));
  }

  function handleJournalReviewFlagSubmit(request: Omit<MatchJournalReviewFlagRequest, "context">): Promise<boolean> {
    return runJournalMutation((context) => submitJournalReviewFlag({ ...request, context }));
  }

  function handleJournalExperimentLabelSubmit(
    request: Omit<MatchJournalExperimentLabelRequest, "context">
  ): Promise<boolean> {
    return runJournalMutation((context) => submitJournalExperimentLabel({ ...request, context }));
  }

  function handleJournalDisplayCorrectionSubmit(
    request: Omit<MatchJournalDisplayCorrectionRequest, "context">
  ): Promise<boolean> {
    return runJournalMutation((context) => submitJournalDisplayCorrection({ ...request, context }));
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
  const journalContextSummary = buildMatchJournalContextSummary(historyState);

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
      <MatchJournalCockpit
        contextSummary={journalContextSummary}
        journalState={journalState}
        onDisplayCorrectionSubmit={handleJournalDisplayCorrectionSubmit}
        onExperimentLabelSubmit={handleJournalExperimentLabelSubmit}
        onNoteSubmit={handleJournalNoteSubmit}
        onOpponentLabelsSubmit={handleJournalOpponentLabelsSubmit}
        onReviewFlagSubmit={handleJournalReviewFlagSubmit}
        onUnattachedSmokeNoteSubmit={handleUnattachedSmokeNoteSubmit}
        smokeReadbackState={journalSmokeReadbackState}
        submitState={journalSubmitState}
      />
      <EarlyGameHistorySection earlyGameState={earlyGameState} onRefresh={refreshEarlyGameHistory} />
      <ActionReviewSection actionReviewState={actionReviewState} onRefresh={refreshActionReview} />
      <SplitReviewSection splitReviewState={splitReviewState} onRefresh={refreshSplitReview} />
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

function MatchJournalCockpit({
  contextSummary,
  journalState,
  onDisplayCorrectionSubmit,
  onExperimentLabelSubmit,
  onNoteSubmit,
  onOpponentLabelsSubmit,
  onReviewFlagSubmit,
  onUnattachedSmokeNoteSubmit,
  smokeReadbackState,
  submitState
}: {
  contextSummary: MatchJournalContextSummary;
  journalState: MatchJournalState;
  onDisplayCorrectionSubmit: (request: Omit<MatchJournalDisplayCorrectionRequest, "context">) => Promise<boolean>;
  onExperimentLabelSubmit: (request: Omit<MatchJournalExperimentLabelRequest, "context">) => Promise<boolean>;
  onNoteSubmit: (request: Omit<MatchJournalAttachedNoteRequest, "context">) => Promise<boolean>;
  onOpponentLabelsSubmit: (request: Omit<MatchJournalOpponentLabelsRequest, "context">) => Promise<boolean>;
  onReviewFlagSubmit: (request: Omit<MatchJournalReviewFlagRequest, "context">) => Promise<boolean>;
  onUnattachedSmokeNoteSubmit: () => Promise<boolean>;
  smokeReadbackState: MatchJournalSmokeReadbackState;
  submitState: MatchJournalSubmitState;
}) {
  const [noteScope, setNoteScope] = useState<MatchJournalAttachedNoteRequest["note_scope"]>("game");
  const [noteText, setNoteText] = useState("");
  const [opponentLabel, setOpponentLabel] = useState("");
  const [opponentTier, setOpponentTier] = useState("");
  const [flagType, setFlagType] = useState("needs_review");
  const [experimentLabel, setExperimentLabel] = useState("");
  const [correctionField, setCorrectionField] = useState("");
  const [correctionValue, setCorrectionValue] = useState("");

  const status = matchJournalStatus(journalState);
  const tone = statusTone(status);
  const disabled = matchJournalWriteDisabled(journalState, contextSummary.context, submitState);
  const smokeDisabled = matchJournalSmokeWriteDisabled(journalState, contextSummary.context, submitState);

  async function handleNoteSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = noteText.trim();
    if (disabled || !trimmed) {
      return;
    }
    if (await onNoteSubmit({ note_scope: noteScope, note_text: trimmed })) {
      setNoteText("");
    }
  }

  async function handleUnattachedSmokeSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (smokeDisabled) {
      return;
    }
    await onUnattachedSmokeNoteSubmit();
  }

  async function handleOpponentLabelsSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const archetype = opponentLabel.trim();
    const tier = opponentTier.trim();
    if (disabled || (!archetype && !tier)) {
      return;
    }
    if (await onOpponentLabelsSubmit({
      ...(archetype ? { archetype } : {}),
      ...(tier ? { tier } : {})
    })) {
      setOpponentLabel("");
      setOpponentTier("");
    }
  }

  async function handleReviewFlagSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (disabled || !flagType.trim()) {
      return;
    }
    await onReviewFlagSubmit({ flag_type: flagType, priority_label: "normal" });
  }

  async function handleExperimentSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = experimentLabel.trim();
    if (disabled || !trimmed) {
      return;
    }
    if (await onExperimentLabelSubmit({ experiment_label: trimmed })) {
      setExperimentLabel("");
    }
  }

  async function handleDisplayCorrectionSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const targetField = correctionField.trim();
    const proposedValue = correctionValue.trim();
    if (disabled || !targetField || !proposedValue) {
      return;
    }
    if (await onDisplayCorrectionSubmit({
      target_surface: "journal_display",
      target_field: targetField,
      proposed_value_label: proposedValue,
      effect_scope: "journal_display_only"
    })) {
      setCorrectionField("");
      setCorrectionValue("");
    }
  }

  return (
    <section className={`matchJournalSection tone-${tone}`} aria-labelledby="match-journal-title">
      <div className="panelHeader analyticsHistoryHeader">
        <div>
          <h2 id="match-journal-title">Match Journal Cockpit</h2>
        </div>
        <StatusPill label={status} tone={tone} />
      </div>
      <div className="historySummaryGrid" aria-label="Match Journal cockpit summary">
        <MatchJournalContextPanel contextSummary={contextSummary} />
        <MatchJournalBundleSummary journalState={journalState} />
      </div>
      {journalState.state === "loading" ? <p className="historyStateMessage">Loading Match Journal</p> : null}
      {journalState.state === "error" ? <MatchJournalErrorNotice journalState={journalState} /> : null}
      {journalState.state === "ready" && journalState.unsafeCount > 0 ? (
        <p className="historyStateMessage">{journalState.unsafeCount} Match Journal value was redacted.</p>
      ) : null}
      {journalState.state === "ready" && journalState.payload.status === "unavailable" ? (
        <p className="historyStateMessage">Match Journal unavailable</p>
      ) : null}
      {contextSummary.context === null ? (
        <form
          aria-label="Unattached smoke note"
          className="manualImportForm journalForm"
          onSubmit={handleUnattachedSmokeSubmit}
        >
          <button disabled={smokeDisabled} type="submit">
            Save Unattached Smoke Note
          </button>
        </form>
      ) : null}
      <MatchJournalSmokeReadbackNotice smokeReadbackState={smokeReadbackState} />
      <div className="journalFormGrid" aria-label="Match Journal edit controls">
        <form className="manualImportForm journalForm" onSubmit={handleNoteSubmit}>
          <label htmlFor="journal-note-scope">Note scope</label>
          <select
            disabled={disabled}
            id="journal-note-scope"
            onChange={(event) => setNoteScope(event.target.value as MatchJournalAttachedNoteRequest["note_scope"])}
            value={noteScope}
          >
            <option value="match">Match</option>
            <option value="game">Game</option>
            <option value="sideboarding">Sideboarding</option>
          </select>
          <label htmlFor="journal-note-text">Journal note</label>
          <textarea
            disabled={disabled}
            id="journal-note-text"
            onChange={(event) => setNoteText(event.target.value)}
            rows={3}
            value={noteText}
          />
          <button disabled={disabled || !noteText.trim()} type="submit">
            Save Journal Note
          </button>
        </form>
        <form className="manualImportForm journalForm" onSubmit={handleOpponentLabelsSubmit}>
          <label htmlFor="journal-opponent-label">Opponent manual label</label>
          <input
            autoComplete="off"
            disabled={disabled}
            id="journal-opponent-label"
            onChange={(event) => setOpponentLabel(event.target.value)}
            value={opponentLabel}
          />
          <label htmlFor="journal-opponent-tier">Opponent tier label</label>
          <input
            autoComplete="off"
            disabled={disabled}
            id="journal-opponent-tier"
            onChange={(event) => setOpponentTier(event.target.value)}
            value={opponentTier}
          />
          <button disabled={disabled || (!opponentLabel.trim() && !opponentTier.trim())} type="submit">
            Save Opponent Labels
          </button>
        </form>
        <form className="manualImportForm journalForm" onSubmit={handleReviewFlagSubmit}>
          <label htmlFor="journal-review-flag">Review flag</label>
          <select
            disabled={disabled}
            id="journal-review-flag"
            onChange={(event) => setFlagType(event.target.value)}
            value={flagType}
          >
            <option value="needs_review">Needs review</option>
            <option value="interesting_match">Interesting match</option>
            <option value="suspected_parser_gap">Suspected parser gap</option>
            <option value="sideboarding_review">Sideboarding review</option>
          </select>
          <button disabled={disabled || !flagType.trim()} type="submit">
            Save Review Flag
          </button>
        </form>
        <form className="manualImportForm journalForm" onSubmit={handleExperimentSubmit}>
          <label htmlFor="journal-experiment-label">Experiment label</label>
          <input
            autoComplete="off"
            disabled={disabled}
            id="journal-experiment-label"
            onChange={(event) => setExperimentLabel(event.target.value)}
            value={experimentLabel}
          />
          <button disabled={disabled || !experimentLabel.trim()} type="submit">
            Save Experiment Label
          </button>
        </form>
        <form className="manualImportForm journalForm" onSubmit={handleDisplayCorrectionSubmit}>
          <label htmlFor="journal-correction-field">Display-only field</label>
          <input
            autoComplete="off"
            disabled={disabled}
            id="journal-correction-field"
            onChange={(event) => setCorrectionField(event.target.value)}
            value={correctionField}
          />
          <label htmlFor="journal-correction-value">Display-only value</label>
          <input
            autoComplete="off"
            disabled={disabled}
            id="journal-correction-value"
            onChange={(event) => setCorrectionValue(event.target.value)}
            value={correctionValue}
          />
          <button disabled={disabled || !correctionField.trim() || !correctionValue.trim()} type="submit">
            Propose Display Correction
          </button>
        </form>
      </div>
      <MatchJournalSubmitNotice submitState={submitState} />
    </section>
  );
}

function MatchJournalContextPanel({ contextSummary }: { contextSummary: MatchJournalContextSummary }) {
  const match = contextSummary.match;
  const game = contextSummary.game;
  return (
    <article className="historySummaryPanel tone-ok">
      <div className="panelHeader">
        <h3>Read-only Context</h3>
      </div>
      <dl>
        <SummaryRow label="match" value={match?.match_id ?? contextSummary.context?.parser_match_id ?? "unknown"} />
        <SummaryRow label="game" value={game?.game_id ?? contextSummary.context?.parser_game_id ?? "unknown"} />
        <SummaryRow label="game number" value={game?.game_number ?? contextSummary.context?.game_number ?? "unknown"} />
        <SummaryRow label="result" value={game?.local_result ?? match?.match_result ?? "unknown"} />
        <SummaryRow label="play/draw" value={game?.play_draw ?? "unknown"} />
        <SummaryRow label="queue" value={game?.queue_name ?? match?.queue_name ?? "unknown"} />
        <SummaryRow label="format" value={game?.format_name ?? match?.format_name ?? "unknown"} />
        <SummaryRow label="event" value={game?.event_id ?? match?.event_id ?? "unknown"} />
        <SummaryRow
          label="status"
          value={
            game
              ? statusSummary(game.game_status, game.result_status, game.context_status)
              : match
                ? statusSummary(match.match_status, match.result_status, match.context_status)
                : "unknown"
          }
        />
      </dl>
    </article>
  );
}

function MatchJournalBundleSummary({ journalState }: { journalState: MatchJournalState }) {
  if (journalState.state !== "ready") {
    return (
      <article className="historySummaryPanel tone-unknown">
        <div className="panelHeader">
          <h3>Journal Bundle</h3>
        </div>
        <p className="historyStateMessage">not loaded</p>
      </article>
    );
  }
  const bundle = journalBundle(journalState.payload);
  return (
    <article className={`historySummaryPanel tone-${statusTone(journalState.payload.status)}`}>
      <div className="panelHeader">
        <h3>Journal Bundle</h3>
        <StatusPill label={journalState.payload.status} tone={statusTone(journalState.payload.status)} />
      </div>
      <dl>
        <SummaryRow label="match" value={bundle ? "present" : "not loaded"} />
        <SummaryRow label="games" value={bundleArrayCount(bundle, "games")} />
        <SummaryRow label="notes" value={bundleArrayCount(bundle, "notes")} />
        <SummaryRow label="labels" value={bundleArrayCount(bundle, "labels")} />
        <SummaryRow label="review flags" value={bundleArrayCount(bundle, "review_flags")} />
        <SummaryRow label="display corrections" value={bundleArrayCount(bundle, "field_overrides")} />
        <SummaryRow label="warnings" value={formatLabels(journalState.payload.warnings)} />
        <SummaryRow label="errors" value={formatLabels(journalState.payload.errors)} />
      </dl>
    </article>
  );
}

function MatchJournalErrorNotice({ journalState }: { journalState: Extract<MatchJournalState, { state: "error" }> }) {
  return (
    <section className={`historyNotice tone-${errorTone(journalState.code)}`} aria-label="Match Journal error">
      <div className="panelHeader">
        <h3>{matchJournalErrorTitle(journalState.code)}</h3>
        <StatusPill label={errorTone(journalState.code)} tone={errorTone(journalState.code)} />
      </div>
      <p>{journalState.message}</p>
    </section>
  );
}

function MatchJournalSubmitNotice({ submitState }: { submitState: MatchJournalSubmitState }) {
  if (submitState.state === "idle") {
    return null;
  }
  if (submitState.state === "submitting") {
    return <p className="jobMessage">Saving journal update</p>;
  }
  if (submitState.state === "error") {
    return (
      <section className={`jobResult tone-${errorTone(submitState.code)}`} aria-label="Match Journal submit error">
        <div className="panelHeader">
          <h2>{matchJournalErrorTitle(submitState.code)}</h2>
          <StatusPill label={errorTone(submitState.code)} tone={errorTone(submitState.code)} />
        </div>
        <p>{submitState.message}</p>
      </section>
    );
  }
  return (
    <section className={`jobResult tone-${statusTone(submitState.payload.status)}`} aria-label="Match Journal submit result">
      <div className="panelHeader">
        <h2>{isSuccessfulMatchJournalSubmit(submitState.payload) ? "Journal Update Saved" : "Journal Update Not Saved"}</h2>
        <StatusPill label={submitState.payload.status} tone={statusTone(submitState.payload.status)} />
      </div>
      <dl>
        <SummaryRow label="warnings" value={formatLabels(submitState.payload.warnings)} />
        <SummaryRow label="errors" value={formatLabels(submitState.payload.errors)} />
      </dl>
    </section>
  );
}

function MatchJournalSmokeReadbackNotice({
  smokeReadbackState
}: {
  smokeReadbackState: MatchJournalSmokeReadbackState;
}) {
  if (smokeReadbackState.state === "idle") {
    return null;
  }
  if (smokeReadbackState.state === "loading") {
    return <p className="jobMessage">Reading unattached smoke note</p>;
  }
  if (smokeReadbackState.state === "error") {
    return (
      <section className={`jobResult tone-${errorTone(smokeReadbackState.code)}`} aria-label="Unattached smoke note readback error">
        <div className="panelHeader">
          <h2>{matchJournalErrorTitle(smokeReadbackState.code)}</h2>
          <StatusPill label={errorTone(smokeReadbackState.code)} tone={errorTone(smokeReadbackState.code)} />
        </div>
        <p>{smokeReadbackState.message}</p>
      </section>
    );
  }

  const note = journalReadbackNote(smokeReadbackState.payload);
  return (
    <section className="jobResult tone-ok" aria-label="Unattached smoke note readback">
      <div className="panelHeader">
        <h2>Unattached Smoke Note</h2>
        <StatusPill label={smokeReadbackState.payload.status} tone={statusTone(smokeReadbackState.payload.status)} />
      </div>
      <dl>
        <SummaryRow label="journal note" value={note?.journal_note_id ?? smokeReadbackState.journalNoteId} />
        <SummaryRow label="note scope" value={note?.note_scope ?? "unknown"} />
        <SummaryRow label="attachment" value={note?.attachment_status ?? "unknown"} />
        <SummaryRow label="author" value={note?.author_label ?? "unknown"} />
        <SummaryRow label="source" value={note?.source_surface ?? "unknown"} />
        <SummaryRow label="privacy" value={note?.privacy_label ?? "unknown"} />
        <SummaryRow label="smoke marker" value={note?.smoke_marker_present ?? false} />
      </dl>
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

function ActionReviewSection({
  actionReviewState,
  onRefresh
}: {
  actionReviewState: ActionReviewState;
  onRefresh: () => void;
}) {
  const status = actionReviewStatus(actionReviewState);
  const tone = statusTone(status);
  return (
    <section className={`analyticsHistorySection tone-${tone}`} aria-labelledby="action-review-title">
      <div className="panelHeader analyticsHistoryHeader">
        <div>
          <h2 id="action-review-title">Action Review</h2>
        </div>
        <div className="historyHeaderActions">
          <StatusPill label={status} tone={tone} />
          <button disabled={actionReviewState.state === "loading"} onClick={onRefresh} type="button">
            Refresh Actions
          </button>
        </div>
      </div>
      {actionReviewState.state === "loading" ? <p className="historyStateMessage">Loading action review</p> : null}
      {actionReviewState.state === "error" ? (
        <ActionReviewErrorNotice actionReviewState={actionReviewState} />
      ) : null}
      {actionReviewState.state === "ready" ? (
        <>
          {actionReviewState.unsafeCount > 0 ? (
            <p className="historyStateMessage">{actionReviewState.unsafeCount} action review value was redacted.</p>
          ) : null}
          <div className="historySummaryGrid" aria-label="Action review summary">
            <ActionReviewSummaryPanel title="Gameplay Actions" response={actionReviewState.gameplayActions} />
            <ActionReviewSummaryPanel title="Opponent Observations" response={actionReviewState.opponentObservations} />
          </div>
          <GameplayActionReviewTable response={actionReviewState.gameplayActions} />
          <OpponentObservationReviewTable response={actionReviewState.opponentObservations} />
        </>
      ) : null}
    </section>
  );
}

function ActionReviewErrorNotice({
  actionReviewState
}: {
  actionReviewState: Extract<ActionReviewState, { state: "error" }>;
}) {
  return (
    <section className={`historyNotice tone-${errorTone(actionReviewState.code)}`} aria-label="Action review error">
      <div className="panelHeader">
        <h3>{analyticsHistoryErrorTitle(actionReviewState.code)}</h3>
        <StatusPill label={errorTone(actionReviewState.code)} tone={errorTone(actionReviewState.code)} />
      </div>
      <p>
        {actionReviewState.code === "incompatible_response"
          ? `Expected schema: ${ACTION_REVIEW_SCHEMA_VERSION}`
          : actionReviewState.message}
      </p>
    </section>
  );
}

function SplitReviewSection({
  splitReviewState,
  onRefresh
}: {
  splitReviewState: SplitReviewState;
  onRefresh: () => void;
}) {
  const status = splitReviewStatus(splitReviewState);
  const tone = statusTone(status);
  return (
    <section className={`analyticsHistorySection tone-${tone}`} aria-labelledby="split-review-title">
      <div className="panelHeader analyticsHistoryHeader">
        <div>
          <h2 id="split-review-title">Split Review</h2>
        </div>
        <div className="historyHeaderActions">
          <StatusPill label={status} tone={tone} />
          <button disabled={splitReviewState.state === "loading"} onClick={onRefresh} type="button">
            Refresh Splits
          </button>
        </div>
      </div>
      {splitReviewState.state === "loading" ? <p className="historyStateMessage">Loading split review</p> : null}
      {splitReviewState.state === "error" ? <SplitReviewErrorNotice splitReviewState={splitReviewState} /> : null}
      {splitReviewState.state === "ready" ? (
        <>
          {splitReviewState.unsafeCount > 0 ? (
            <p className="historyStateMessage">{splitReviewState.unsafeCount} split review value was redacted.</p>
          ) : null}
          <div className="historySummaryGrid" aria-label="Split review summary">
            <PlayDrawSplitSummaryPanel response={splitReviewState.playDrawSplits} />
            <Game1PostboardSplitSummaryPanel response={splitReviewState.game1PostboardSplits} />
          </div>
          <PlayDrawSplitTable response={splitReviewState.playDrawSplits} />
          <Game1PostboardSplitTable response={splitReviewState.game1PostboardSplits} />
        </>
      ) : null}
    </section>
  );
}

function SplitReviewErrorNotice({
  splitReviewState
}: {
  splitReviewState: Extract<SplitReviewState, { state: "error" }>;
}) {
  return (
    <section className={`historyNotice tone-${errorTone(splitReviewState.code)}`} aria-label="Split review error">
      <div className="panelHeader">
        <h3>{analyticsHistoryErrorTitle(splitReviewState.code)}</h3>
        <StatusPill label={errorTone(splitReviewState.code)} tone={errorTone(splitReviewState.code)} />
      </div>
      <p>
        {splitReviewState.code === "incompatible_response"
          ? `Expected schema: ${SPLIT_REVIEW_SCHEMA_VERSION}`
          : splitReviewState.message}
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

function ActionReviewSummaryPanel({
  title,
  response
}: {
  title: string;
  response: GameplayActionReviewResponse | OpponentCardObservationReviewResponse;
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
        <SummaryRow label="review" value={response.summary.review_required_row_count} />
        <SummaryRow label="schema" value={response.database.schema_status} />
      </dl>
    </article>
  );
}

function PlayDrawSplitSummaryPanel({ response }: { response: PlayDrawSplitReviewResponse }) {
  return (
    <article className={`historySummaryPanel tone-${statusTone(response.status)}`}>
      <div className="panelHeader">
        <h3>Play/Draw Splits</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      <dl>
        <SummaryRow label="rows" value={response.summary.row_count} />
        <SummaryRow label="games" value={response.summary.total_game_count} />
        <SummaryRow label="known" value={response.summary.known_result_count} />
        <SummaryRow label="wins" value={response.summary.wins} />
        <SummaryRow label="losses" value={response.summary.losses} />
        <SummaryRow label="unknown" value={response.summary.unknown_result_count} />
        <SummaryRow label="unavailable" value={response.summary.unavailable_result_count} />
        <SummaryRow label="degraded" value={response.summary.degraded_result_count} />
        <SummaryRow label="small sample" value={response.summary.small_sample_group_count} />
        <SummaryRow label="schema" value={response.database.schema_status} />
      </dl>
    </article>
  );
}

function Game1PostboardSplitSummaryPanel({ response }: { response: Game1PostboardSplitReviewResponse }) {
  return (
    <article className={`historySummaryPanel tone-${statusTone(response.status)}`}>
      <div className="panelHeader">
        <h3>Game 1/Postboard</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      <dl>
        <SummaryRow label="rows" value={response.summary.row_count} />
        <SummaryRow label="game 1" value={response.summary.game1_row_count} />
        <SummaryRow label="postboard" value={response.summary.postboard_row_count} />
        <SummaryRow label="known" value={response.summary.known_result_count} />
        <SummaryRow label="unknown" value={response.summary.unknown_result_count} />
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

function GameplayActionReviewTable({ response }: { response: GameplayActionReviewResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="gameplay-action-review-title">
      <div className="panelHeader">
        <h3 id="gameplay-action-review-title">Gameplay Actions</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("gameplay action", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Turn</th>
                <th scope="col">Action</th>
                <th scope="col">Cards</th>
                <th scope="col">Result</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.gameplay_action_id}>
                  <SafeCell value={`${row.match_id} game ${row.game_number}`} />
                  <SafeCell value={row.turn_number ?? "unknown"} />
                  <SafeCell value={gameplayActionSummary(row)} />
                  <SafeCell value={gameplayActionCardsSummary(row)} />
                  <SafeCell value={row.local_result ?? row.match_result ?? matchWinLabel(row.match_win)} />
                  <SafeCell
                    value={statusSummary(
                      row.gameplay_action_status,
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

function OpponentObservationReviewTable({ response }: { response: OpponentCardObservationReviewResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="opponent-observation-review-title">
      <div className="panelHeader">
        <h3 id="opponent-observation-review-title">Opponent Observations</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("opponent observation", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Turn</th>
                <th scope="col">Observation</th>
                <th scope="col">Cards</th>
                <th scope="col">Link</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.opponent_card_observation_id}>
                  <SafeCell value={`${row.match_id} game ${row.game_number}`} />
                  <SafeCell value={row.turn_number ?? "unknown"} />
                  <SafeCell value={opponentObservationSummary(row)} />
                  <SafeCell value={opponentObservationCardsSummary(row)} />
                  <SafeCell value={linkedGameplayActionSummary(row)} />
                  <SafeCell
                    value={statusSummary(
                      row.opponent_card_observation_status,
                      row.linked_gameplay_action_status,
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

function PlayDrawSplitTable({ response }: { response: PlayDrawSplitReviewResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="play-draw-split-review-title">
      <div className="panelHeader">
        <h3 id="play-draw-split-review-title">Play/Draw Splits</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("play/draw split", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Split</th>
                <th scope="col">Games</th>
                <th scope="col">Known</th>
                <th scope="col">Wins</th>
                <th scope="col">Losses</th>
                <th scope="col">Unknown</th>
                <th scope="col">Unavailable</th>
                <th scope="col">Degraded</th>
                <th scope="col">Win Rate</th>
                <th scope="col">Sample</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.play_draw}>
                  <SafeCell value={row.play_draw} />
                  <SafeCell value={row.game_count} />
                  <SafeCell value={row.known_result_count} />
                  <SafeCell value={row.wins} />
                  <SafeCell value={row.losses} />
                  <SafeCell value={row.unknown_result_count} />
                  <SafeCell value={row.unavailable_result_count} />
                  <SafeCell value={row.degraded_result_count} />
                  <SafeCell value={winRateLabel(row.win_rate)} />
                  <SafeCell value={row.sample_size_warning ?? "none"} />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function Game1PostboardSplitTable({ response }: { response: Game1PostboardSplitReviewResponse }) {
  return (
    <section className="historyTableSection" aria-labelledby="game1-postboard-split-review-title">
      <div className="panelHeader">
        <h3 id="game1-postboard-split-review-title">Game 1/Postboard Rows</h3>
        <StatusPill label={response.status} tone={statusTone(response.status)} />
      </div>
      {response.rows.length === 0 ? (
        <p className="historyStateMessage">{historyEmptyLabel("game 1/postboard split", response.status)}</p>
      ) : (
        <div className="historyTableWrap">
          <table className="historyTable">
            <thead>
              <tr>
                <th scope="col">Game</th>
                <th scope="col">Split</th>
                <th scope="col">Result</th>
                <th scope="col">Play/Draw</th>
                <th scope="col">Turns</th>
                <th scope="col">Duration</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {response.rows.map((row) => (
                <tr key={row.game_result_id}>
                  <SafeCell value={`${row.match_id} game ${row.game_number}`} />
                  <SafeCell value={row.pre_postboard_label ?? "unknown"} />
                  <SafeCell value={row.local_result ?? "unknown"} />
                  <SafeCell value={row.play_draw ?? "unknown"} />
                  <SafeCell value={row.turn_count ?? "unknown"} />
                  <SafeCell value={durationLabel(row.game_duration_seconds)} />
                  <SafeCell value={statusSummary(row.game_result_status)} />
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
  const safe = safeDisplayValue(formatSafeCellValue(value));
  return <td className={safe.redacted ? "redactedRow" : undefined}>{safe.text}</td>;
}

function formatSafeCellValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "unknown";
  }
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return "unknown";
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

function buildMatchJournalContextSummary(historyState: HistoryState): MatchJournalContextSummary {
  if (historyState.state !== "ready") {
    return { context: null, match: null, game: null };
  }
  const game = historyState.games.rows[0] ?? null;
  const match = game
    ? historyState.matches.rows.find((row) => row.match_id === game.match_id) ?? historyState.matches.rows[0] ?? null
    : historyState.matches.rows[0] ?? null;
  if (game) {
    return {
      context: {
        parser_match_id: game.match_id,
        parser_game_id: game.game_id,
        game_number: game.game_number
      },
      match,
      game
    };
  }
  if (match) {
    return {
      context: {
        parser_match_id: match.match_id
      },
      match,
      game: null
    };
  }
  return { context: null, match: null, game: null };
}

function emptyMatchJournalPayload(): MatchJournalResponse {
  return {
    object: "mythic_edge_local_app_match_journal",
    schema_version: "match_journal_cockpit_ui.v1",
    status: "empty",
    result: {},
    warnings: [],
    errors: []
  };
}

function countUnsafeJournalValues(payload: MatchJournalResponse): number {
  const values: unknown[] = [...payload.warnings, ...payload.errors, payload.status];
  const bundle = journalBundle(payload);
  if (bundle) {
    values.push(
      bundleArrayCount(bundle, "games"),
      bundleArrayCount(bundle, "notes"),
      bundleArrayCount(bundle, "labels"),
      bundleArrayCount(bundle, "review_flags"),
      bundleArrayCount(bundle, "field_overrides")
    );
  }
  return values.filter((value) => safeDisplayValue(value ?? "unknown").redacted).length;
}

function matchJournalStatus(journalState: MatchJournalState): string {
  if (journalState.state === "loading") {
    return "loading";
  }
  if (journalState.state === "error") {
    return errorTone(journalState.code);
  }
  if (journalState.unsafeCount > 0) {
    return "degraded";
  }
  return journalState.payload.status;
}

function isSuccessfulMatchJournalSubmit(payload: MatchJournalResponse): boolean {
  return payload.status === "ok" && payload.errors.length === 0;
}

function matchJournalWriteDisabled(
  journalState: MatchJournalState,
  context: MatchJournalContext | null,
  submitState: MatchJournalSubmitState
): boolean {
  if (submitState.state === "submitting" || context === null || journalState.state !== "ready") {
    return true;
  }
  return journalState.payload.status === "unavailable" || journalState.payload.status === "error";
}

function matchJournalSmokeWriteDisabled(
  journalState: MatchJournalState,
  context: MatchJournalContext | null,
  submitState: MatchJournalSubmitState
): boolean {
  if (submitState.state === "submitting" || context !== null || journalState.state !== "ready") {
    return true;
  }
  return journalState.payload.status === "unavailable" || journalState.payload.status === "error";
}

function journalBundle(payload: MatchJournalResponse): Record<string, unknown> | null {
  const bundle = payload.result.bundle;
  return isRecord(bundle) ? bundle : null;
}

function journalReadbackNote(payload: MatchJournalResponse): Record<string, unknown> | null {
  const note = payload.result.note;
  return isRecord(note) ? note : null;
}

function journalPrimaryRecordId(payload: MatchJournalResponse): string | null {
  const serviceResult = payload.result.service_result;
  if (!isRecord(serviceResult) || typeof serviceResult.primary_record_id !== "string") {
    return null;
  }
  const journalNoteId = serviceResult.primary_record_id.trim();
  return isSafeJournalNoteId(journalNoteId) ? journalNoteId : null;
}

function readStoredUnattachedSmokeNoteId(): string | null {
  try {
    const journalNoteId = window.sessionStorage.getItem(UNATTACHED_SMOKE_NOTE_STORAGE_KEY);
    if (journalNoteId === null || !isSafeJournalNoteId(journalNoteId)) {
      return null;
    }
    return journalNoteId;
  } catch {
    return null;
  }
}

function storeUnattachedSmokeNoteId(journalNoteId: string) {
  if (!isSafeJournalNoteId(journalNoteId)) {
    return;
  }
  try {
    window.sessionStorage.setItem(UNATTACHED_SMOKE_NOTE_STORAGE_KEY, journalNoteId);
  } catch {
    return;
  }
}

function isSafeJournalNoteId(value: string): boolean {
  return value.length > 0 && value.length <= 160 && /^[A-Za-z0-9_.:-]+$/.test(value);
}

function bundleArrayCount(bundle: Record<string, unknown> | null, key: string): number {
  if (bundle === null) {
    return 0;
  }
  const value = bundle[key];
  return Array.isArray(value) ? value.length : 0;
}

function matchJournalErrorTitle(code: MatchJournalApiError["code"]): string {
  if (code === "malformed_response") {
    return "Malformed Match Journal response";
  }
  if (code === "incompatible_response") {
    return "Incompatible Match Journal schema";
  }
  if (code === "unsafe_api_base_url") {
    return "Unsafe API base URL";
  }
  return "Match Journal unavailable";
}

function buildPanels(payload: SetupStatusResponse): Panel[] {
  const livePlayerLogPanel = buildLivePlayerLogPanel(payload.live_player_log);
  const liveWatcherPanel = buildLiveWatcherPanel(payload.live_watcher);
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
    ...(livePlayerLogPanel ? [livePlayerLogPanel] : []),
    ...(liveWatcherPanel ? [liveWatcherPanel] : []),
    {
      title: "Analytics Database",
      status: statusFromSection(payload.analytics_database),
      details: [
        { label: "path", value: nestedValue(payload.analytics_database, ["database", "display_path"]) },
        { label: "schema", value: nestedValue(payload.analytics_database, ["database", "schema_status"]) }
      ]
    },
    {
      title: "Match Journal",
      status: statusFromSection(payload.match_journal),
      details: [
        { label: "path", value: nestedValue(payload.match_journal, ["database", "display_path"]) },
        { label: "writes", value: nestedValue(payload.match_journal, ["write_controls", "status"]) }
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

function buildLivePlayerLogPanel(payload: unknown): Panel | null {
  if (!isLivePlayerLogStatusResponse(payload)) {
    return null;
  }
  return {
    title: "Live Player.log",
    status: payload.player_log.status,
    details: [
      { label: "path", value: payload.player_log.display_path },
      { label: "source", value: payload.player_log.source },
      { label: "kind", value: payload.player_log.path_kind },
      { label: "metadata", value: payload.player_log.metadata_access },
      { label: "activity", value: payload.player_log.activity_hint ?? "unknown" },
      { label: "contents", value: payload.player_log.contents_read ? "read" : "not_read" },
      { label: "tailing", value: payload.player_log.tailing_started ? "started" : "not_started" }
    ]
  };
}

function buildLiveWatcherPanel(payload: unknown): Panel | null {
  if (!isLiveWatcherStatusResponse(payload)) {
    return null;
  }
  return {
    title: "Live Watcher",
    status: payload.watcher.status,
    details: [
      { label: "mode", value: payload.watcher.mode },
      { label: "readiness", value: payload.watcher.status },
      { label: "capture", value: payload.watcher.running ? "capturing" : "not_capturing" },
      { label: "start", value: payload.watcher.start_allowed ? "allowed" : "disabled" },
      { label: "stop", value: payload.watcher.stop_allowed ? "allowed" : "disabled" },
      { label: "tailing", value: payload.watcher.tailing_started ? "started" : "not_started" },
      { label: "reason", value: payload.watcher.reason ?? "none" }
    ]
  };
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

function countUnsafeActionReviewValues(
  gameplayActions: GameplayActionReviewResponse,
  opponentObservations: OpponentCardObservationReviewResponse
): number {
  const values: unknown[] = [
    gameplayActions.database.display_path,
    opponentObservations.database.display_path,
    ...gameplayActions.warnings,
    ...gameplayActions.errors,
    ...opponentObservations.warnings,
    ...opponentObservations.errors
  ];
  for (const row of gameplayActions.rows) {
    values.push(
      row.gameplay_action_id,
      row.match_id,
      row.game_id,
      row.timestamp,
      row.action_type,
      row.actor_relation,
      row.from_zone_type,
      row.to_zone_type,
      row.source_status,
      row.annotation_context_label,
      row.raw_action_type_labels,
      row.annotation_type_labels,
      gameplayActionCardsSummary(row),
      statusSummary(
        row.gameplay_action_status,
        row.game_status,
        row.game_result_status,
        row.match_result_status,
        row.context_status
      )
    );
  }
  for (const row of opponentObservations.rows) {
    values.push(
      row.opponent_card_observation_id,
      row.gameplay_action_id,
      row.match_id,
      row.game_id,
      row.timestamp,
      row.card_name,
      row.display_name,
      row.action_type,
      row.cast_mode,
      row.source_evidence,
      row.evidence_status,
      row.visibility,
      row.from_zone_type,
      row.to_zone_type,
      row.degradation_flags.join(" "),
      opponentObservationCardsSummary(row),
      linkedGameplayActionSummary(row),
      statusSummary(
        row.opponent_card_observation_status,
        row.linked_gameplay_action_status,
        row.game_status,
        row.game_result_status,
        row.match_result_status,
        row.context_status
      )
    );
  }
  return values.filter((value) => safeDisplayValue(value ?? "unknown").redacted).length;
}

function countUnsafeSplitReviewValues(
  playDrawSplits: PlayDrawSplitReviewResponse,
  game1PostboardSplits: Game1PostboardSplitReviewResponse
): number {
  const values: unknown[] = [
    playDrawSplits.database.display_path,
    game1PostboardSplits.database.display_path,
    ...playDrawSplits.warnings,
    ...playDrawSplits.errors,
    ...game1PostboardSplits.warnings,
    ...game1PostboardSplits.errors
  ];
  for (const row of playDrawSplits.rows) {
    values.push(row.play_draw, row.sample_size_warning);
  }
  for (const row of game1PostboardSplits.rows) {
    values.push(
      row.game_result_id,
      row.match_id,
      row.game_id,
      row.pre_postboard_label,
      row.local_result,
      row.play_draw,
      statusSummary(row.game_result_status)
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

function actionReviewStatus(actionReviewState: ActionReviewState): string {
  if (actionReviewState.state === "loading") {
    return "loading";
  }
  if (actionReviewState.state === "error") {
    return errorTone(actionReviewState.code);
  }
  if (actionReviewState.unsafeCount > 0) {
    return "degraded";
  }
  const statuses: AnalyticsHistoryStatus[] = [
    actionReviewState.gameplayActions.status,
    actionReviewState.opponentObservations.status
  ];
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

function splitReviewStatus(splitReviewState: SplitReviewState): string {
  if (splitReviewState.state === "loading") {
    return "loading";
  }
  if (splitReviewState.state === "error") {
    return errorTone(splitReviewState.code);
  }
  if (splitReviewState.unsafeCount > 0) {
    return "degraded";
  }
  const statuses: AnalyticsHistoryStatus[] = [
    splitReviewState.playDrawSplits.status,
    splitReviewState.game1PostboardSplits.status
  ];
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

function gameplayActionSummary(row: GameplayActionReviewRow): string {
  const actor = row.actor_relation || "unknown";
  const source = row.source_status ?? row.annotation_context_label ?? "unknown";
  const movement = `${row.from_zone_type ?? "unknown"} to ${row.to_zone_type ?? "unknown"}`;
  return `${actor} ${row.action_type} ${movement} ${source}`;
}

function gameplayActionCardsSummary(row: GameplayActionReviewRow): string {
  if (row.cards.length === 0) {
    return "no cards";
  }
  return row.cards.map((card) => {
    const identity = card.display_name ?? card.card_name ?? (card.grp_id === null ? "unknown" : `grp ${card.grp_id}`);
    const source = card.identity_hint_source ?? card.name_resolution_status ?? "unknown";
    return `${card.card_ordinal}: ${identity} ${source} ${card.grp_id ?? "unknown"}`;
  }).join(" ");
}

function opponentObservationSummary(row: OpponentCardObservationReviewRow): string {
  const identity = row.display_name ?? row.card_name ?? (row.grp_id === null ? "unknown" : `grp ${row.grp_id}`);
  const flags = degradationFlagsSummary(row);
  const review = row.review_required ? "review required" : "review clear";
  return `${identity} ${visibilityEvidenceSummary(row)} ${flags} ${review}`;
}

function opponentObservationCardsSummary(row: OpponentCardObservationReviewRow): string {
  if (row.cards.length === 0) {
    return "no cards";
  }
  return row.cards.map((card) => {
    const identity = card.card_name ?? (card.grp_id === null ? "unknown" : `grp ${card.grp_id}`);
    const source = card.identity_hint_source ?? card.resolution_status ?? "unknown";
    return `${card.card_ordinal}: ${identity} ${source} ${card.visibility ?? "unknown"} ${card.grp_id ?? "unknown"}`;
  }).join(" ");
}

function linkedGameplayActionSummary(row: OpponentCardObservationReviewRow): string {
  if (row.linked_gameplay_action === null) {
    return "not linked";
  }
  const action = row.linked_gameplay_action;
  const movement = `${action.from_zone_type ?? "unknown"} to ${action.to_zone_type ?? "unknown"}`;
  return `turn ${action.turn_number ?? "unknown"} ${action.actor_relation} ${action.action_type} ${movement}`;
}

function visibilityEvidenceSummary(row: OpponentCardObservationReviewRow): string {
  const visibility = row.visibility ?? "unknown visibility";
  const evidence = row.evidence_status ?? row.source_evidence ?? "unknown evidence";
  return `${visibility} ${evidence}`;
}

function degradationFlagsSummary(row: OpponentCardObservationReviewRow): string {
  if (row.degradation_flags.length === 0) {
    return "no flags";
  }
  return row.degradation_flags.join(" ");
}

function winRateLabel(value: number | null): string {
  if (value === null) {
    return "unknown";
  }
  return `${Math.round(value * 1000) / 10} percent`;
}

function durationLabel(value: number | null): string {
  if (value === null) {
    return "unknown";
  }
  return `${Math.round(value)} seconds`;
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

function isLivePlayerLogStatusResponse(value: unknown): value is LivePlayerLogStatusResponse {
  return (
    isRecord(value) &&
    value.object === LIVE_PLAYER_LOG_STATUS_OBJECT &&
    value.schema_version === LIVE_STATUS_SCHEMA_VERSION &&
    typeof value.status === "string" &&
    isRecord(value.player_log)
  );
}

function isLiveWatcherStatusResponse(value: unknown): value is LiveWatcherStatusResponse {
  return (
    isRecord(value) &&
    value.object === LIVE_WATCHER_STATUS_OBJECT &&
    value.schema_version === LIVE_STATUS_SCHEMA_VERSION &&
    typeof value.status === "string" &&
    isRecord(value.watcher) &&
    isRecord(value.player_log)
  );
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
