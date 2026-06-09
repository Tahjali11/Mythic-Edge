import { describe, expect, it, vi } from "vitest";

import {
  fetchAnalyticsDashboardModules,
  fetchAnalyticsRefreshState,
  fetchGameplayActionReview,
  AnalyticsHistoryApiError,
  fetchGame1PostboardSplitReview,
  fetchLivePlayerLogStatus,
  fetchLiveWatcherDiagnosticsStatus,
  fetchLiveWatcherProcessStatus,
  fetchLiveWatcherStatus,
  fetchLiveCaptureStatus,
  fetchManualImportJob,
  fetchGameHistory,
  fetchMatchHistory,
  fetchMatchJournal,
  fetchMulliganHistory,
  fetchOpponentCardObservationReview,
  fetchOpeningHandHistory,
  fetchPlayDrawSplitReview,
  fetchSetupStatus,
  getApiBaseUrl,
  LiveStatusApiError,
  MatchJournalApiError,
  ManualImportApiError,
  previewErrorReport,
  SetupStatusApiError,
  submitErrorReport,
  submitMatchJournalDisplayCorrection,
  submitMatchJournalExperimentLabel,
  submitMatchJournalNote,
  submitMatchJournalOpponentLabels,
  submitMatchJournalReviewFlag,
  submitManualJsonlImport,
  submitManualJsonlUpload
} from "./api";
import {
  ACTION_REVIEW_SCHEMA_VERSION,
  ANALYTICS_DASHBOARD_MODULES_OBJECT,
  ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION,
  ANALYTICS_HISTORY_SCHEMA_VERSION,
  ANALYTICS_REFRESH_STATE_OBJECT,
  ANALYTICS_REFRESH_STATE_SCHEMA_VERSION,
  EARLY_GAME_HISTORY_SCHEMA_VERSION,
  ERROR_REPORT_PREVIEW_SCHEMA,
  ERROR_REPORT_SUBMISSION_OBJECT,
  ERROR_REPORT_SUBMISSION_SCHEMA,
  GAME_HISTORY_OBJECT,
  GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT,
  GAMEPLAY_ACTION_REVIEW_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
  LIVE_PLAYER_LOG_STATUS_OBJECT,
  LIVE_CAPTURE_SCHEMA_VERSION,
  LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
  LIVE_CAPTURE_STATUS_OBJECT,
  LIVE_STATUS_SCHEMA_VERSION,
  LIVE_WATCHER_DIAGNOSTICS_OBJECT,
  LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION,
  LIVE_WATCHER_PROCESS_OBJECT,
  LIVE_WATCHER_PROCESS_SCHEMA_VERSION,
  LIVE_WATCHER_STATUS_OBJECT,
  MANUAL_IMPORT_JOB_OBJECT,
  MANUAL_IMPORT_JOB_SCHEMA_VERSION,
  MATCH_JOURNAL_OBJECT,
  MATCH_JOURNAL_SCHEMA_VERSION,
  MATCH_HISTORY_OBJECT,
  MULLIGAN_HISTORY_OBJECT,
  OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT,
  OPENING_HAND_HISTORY_OBJECT,
  PLAY_DRAW_SPLIT_REVIEW_OBJECT,
  SETUP_STATUS_OBJECT,
  SETUP_STATUS_SCHEMA_VERSION,
  SPLIT_REVIEW_SCHEMA_VERSION,
  type Game1PostboardSplitReviewResponse,
  type AnalyticsDashboardModulesResponse,
  type AnalyticsRefreshStateResponse,
  type ErrorReportPreviewResponse,
  type ErrorReportSubmissionResponse,
  type GameHistoryResponse,
  type GameplayActionReviewResponse,
  type LegacyJsonlImportQuality,
  type LivePlayerLogStatusResponse,
  type LiveCaptureStatusResponse,
  type LiveWatcherDiagnosticsResponse,
  type LiveWatcherProcessStatusResponse,
  type LiveWatcherStatusResponse,
  type ManualImportJob,
  type MatchJournalResponse,
  type MulliganHistoryResponse,
  type OpeningHandHistoryResponse,
  type MatchHistoryResponse,
  type OpponentCardObservationReviewResponse,
  type PlayDrawSplitReviewResponse,
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

  it("fetches and validates live capture heartbeat and progress diagnostics", async () => {
    const payload = buildLiveCaptureStatusPayload({
      status: "capturing",
      heartbeat: {
        schema_version: LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
        status: "progress",
        heartbeat_updated_at: "2026-06-08T12:00:00Z",
        capture_duration_seconds: 15,
        heartbeat_age_seconds: 1,
        stale_after_seconds: 30
      },
      progress: {
        schema_version: LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
        log_poll_count: 5,
        log_chunks_seen: 0,
        structured_entry_count: 2,
        parser_event_count: 2,
        parser_event_kinds_seen: ["game_state"],
        match_ids_seen_count: 1,
        current_match_detected: true,
        current_match_game_wins: null,
        current_match_game_losses: null,
        last_completed_match_result: null,
        last_completed_match_game_wins: null,
        last_completed_match_game_losses: null,
        completed_game_rows_seen: 0,
        sqlite_write_attempt_count: 0,
        sqlite_rows_written: 0,
        last_no_write_reason: "no_completed_game_rows",
        last_event_seen_at: "2026-06-08T12:00:00Z",
        last_sqlite_write_at: null
      },
      parser_status_blurb: {
        code: "waiting_for_completed_facts",
        text: "Capturing; waiting for completed match facts.",
        tone: "waiting"
      }
    });
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(fetchLiveCaptureStatus(fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/live/capture/status", {
      headers: { Accept: "application/json" }
    });
  });

  it("submits sanitized error reports through the local backend route", async () => {
    const payload = buildErrorReportSubmissionPayload();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(
      submitErrorReport(
        {
          summary: "Dashboard status did not refresh",
          report_type: "bug",
          expected_behavior: "The dashboard should show current safe labels.",
          actual_behavior: "The dashboard kept old labels after reload.",
          reproduction_steps: "Open the app.",
          affected_area: "local_app_ui",
          severity: "degraded"
        },
        fetchImpl
      )
    ).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/feedback/error-report/submit", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: expect.stringContaining('"report_type":"bug"')
    });
  });

  it("accepts ready error-report previews when external submission is enabled", async () => {
    const payload = buildErrorReportPreviewPayload({ external_submission_enabled: true });
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(
      previewErrorReport(
        {
          summary: "Dashboard status did not refresh",
          report_type: "bug",
          expected_behavior: "The dashboard should show current safe labels.",
          actual_behavior: "The dashboard kept old labels after reload.",
          reproduction_steps: "Open the app.",
          affected_area: "local_app_ui",
          severity: "degraded"
        },
        fetchImpl
      )
    ).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/feedback/error-report/preview", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: expect.stringContaining('"report_type":"bug"')
    });
  });

  it("fetches and validates live Player.log and watcher status responses", async () => {
    const playerLogPayload = buildLivePlayerLogStatusPayload();
    const watcherPayload = buildLiveWatcherStatusPayload();
    const processPayload = buildLiveWatcherProcessStatusPayload();
    const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/api/live/player-log/status")) {
        return jsonResponse(playerLogPayload);
      }
      if (String(input).endsWith("/api/live/watcher/process")) {
        return jsonResponse(processPayload);
      }
      return jsonResponse(watcherPayload);
    }) as unknown as typeof fetch;

    await expect(fetchLivePlayerLogStatus(fetchImpl)).resolves.toEqual(playerLogPayload);
    await expect(fetchLiveWatcherStatus(fetchImpl)).resolves.toEqual(watcherPayload);
    await expect(fetchLiveWatcherProcessStatus(fetchImpl)).resolves.toEqual(processPayload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/live/player-log/status", {
      headers: { Accept: "application/json" }
    });
    expect(fetchImpl).toHaveBeenCalledWith("/api/live/watcher/status", {
      headers: { Accept: "application/json" }
    });
    expect(fetchImpl).toHaveBeenCalledWith("/api/live/watcher/process", {
      headers: { Accept: "application/json" }
    });
  });

  it("fetches and validates live watcher diagnostics responses", async () => {
    const payload = buildLiveWatcherDiagnosticsPayload();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(fetchLiveWatcherDiagnosticsStatus(fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/live/watcher/diagnostics", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed live status responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildLivePlayerLogStatusPayload(), schema_version: "future.live.schema" })
    ) as unknown as typeof fetch;
    await expect(fetchLivePlayerLogStatus(wrongSchemaFetch)).rejects.toBeInstanceOf(LiveStatusApiError);
    await expect(fetchLivePlayerLogStatus(wrongSchemaFetch)).rejects.toMatchObject({ code: "incompatible_response" });

    const rawPathFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveWatcherStatusPayload(),
        watcher: {
          ...buildLiveWatcherStatusPayload().watcher,
          running: true
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveWatcherStatus(rawPathFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const processControlFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveWatcherProcessStatusPayload(),
        process_control: {
          ...buildLiveWatcherProcessStatusPayload().process_control,
          start_allowed: true
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveWatcherProcessStatus(processControlFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const processPreconditionMapFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveWatcherProcessStatusPayload(),
        preconditions: {
          player_log_ready: { status: "pass", reason: null }
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveWatcherProcessStatus(processPreconditionMapFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const processPreconditionMissingFieldFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveWatcherProcessStatusPayload(),
        preconditions: buildLiveWatcherProcessStatusPayload().preconditions.map((entry, index) =>
          index === 0 ? { key: entry.key, status: entry.status } : entry
        )
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveWatcherProcessStatus(processPreconditionMissingFieldFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const unsafeDiagnosticsFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveWatcherDiagnosticsPayload(),
        capabilities: {
          ...buildLiveWatcherDiagnosticsPayload().capabilities,
          starts_watcher: true
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveWatcherDiagnosticsStatus(unsafeDiagnosticsFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const wrongDiagnosticsSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildLiveWatcherDiagnosticsPayload(), schema_version: "future.diagnostics" })
    ) as unknown as typeof fetch;
    await expect(fetchLiveWatcherDiagnosticsStatus(wrongDiagnosticsSchemaFetch)).rejects.toMatchObject({
      code: "incompatible_response"
    });

    const unsafeBlurbText = String.raw`C:\operator\AppData\Local\MythicEdge\Player.log`;
    const unsafeLiveCaptureBlurbFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveCaptureStatusPayload(),
        parser_status_blurb: {
          code: "waiting_for_events",
          text: unsafeBlurbText,
          tone: "waiting"
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveCaptureStatus(unsafeLiveCaptureBlurbFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });
    try {
      await fetchLiveCaptureStatus(unsafeLiveCaptureBlurbFetch);
    } catch (error) {
      expect(String(error)).not.toContain(unsafeBlurbText);
    }

    const unsafeHeartbeatFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveCaptureStatusPayload(),
        heartbeat: {
          ...buildLiveCaptureStatusPayload().heartbeat,
          heartbeat_updated_at: unsafeBlurbText
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveCaptureStatus(unsafeHeartbeatFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const unsafeProgressFetch = vi.fn(async () =>
      jsonResponse({
        ...buildLiveCaptureStatusPayload(),
        progress: {
          ...buildLiveCaptureStatusPayload().progress,
          parser_event_kinds_seen: ["game_state", unsafeBlurbText]
        }
      })
    ) as unknown as typeof fetch;
    await expect(fetchLiveCaptureStatus(unsafeProgressFetch)).rejects.toMatchObject({
      code: "malformed_response"
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

  it("fetches and validates the Match Journal cockpit bundle through the local app facade", async () => {
    const payload = buildMatchJournalPayload();
    const fetchImpl = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) => jsonResponse(payload));

    await expect(
      fetchMatchJournal(
        { parser_match_id: "match:history:1", parser_game_id: "match:history:1:g1", game_number: 1 },
        fetchImpl as unknown as typeof fetch
      )
    ).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith(
      "/api/journal?parser_match_id=match%3Ahistory%3A1&parser_game_id=match%3Ahistory%3A1%3Ag1&game_number=1",
      {
        headers: { Accept: "application/json" }
      }
    );
    expect(String(fetchImpl.mock.calls[0][0])).toContain("/api/journal?");
    expect(String(fetchImpl.mock.calls[0][0])).not.toMatch(/^\/journal/);
  });

  it("serializes contract-safe Match Journal context fields through the local app facade", async () => {
    const payload = buildMatchJournalPayload();
    const fetchImpl = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) => jsonResponse(payload));

    await expect(
      fetchMatchJournal(
        {
          journal_match_id: "journal:match:1",
          journal_game_id: "journal:game:1",
          attachment_status: "attached"
        },
        fetchImpl as unknown as typeof fetch
      )
    ).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith(
      "/api/journal?journal_match_id=journal%3Amatch%3A1&journal_game_id=journal%3Agame%3A1&attachment_status=attached",
      {
        headers: { Accept: "application/json" }
      }
    );
  });

  it("posts Match Journal cockpit mutations only to /api/journal routes", async () => {
    const payload = buildMatchJournalPayload({ result: { service_result: { action: "completed" } } });
    const fetchImpl = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) => jsonResponse(payload));
    const context = { parser_match_id: "match:history:1", parser_game_id: "match:history:1:g1", game_number: 1 };

    await submitMatchJournalNote(
      { context, note_scope: "game", note_text: "Synthetic note." },
      fetchImpl as unknown as typeof fetch
    );
    await submitMatchJournalOpponentLabels(
      { context, archetype: "Manual Synthetic Archetype" },
      fetchImpl as unknown as typeof fetch
    );
    await submitMatchJournalReviewFlag(
      { context, flag_type: "suspected_parser_gap" },
      fetchImpl as unknown as typeof fetch
    );
    await submitMatchJournalExperimentLabel(
      { context, experiment_label: "ladder-test" },
      fetchImpl as unknown as typeof fetch
    );
    await submitMatchJournalDisplayCorrection(
      {
        context,
        target_surface: "journal_display",
        target_field: "review_summary",
        proposed_value_label: "Synthetic display label."
      },
      fetchImpl as unknown as typeof fetch
    );

    expect(fetchImpl.mock.calls.map((call) => String(call[0]))).toEqual([
      "/api/journal/notes",
      "/api/journal/opponent-labels",
      "/api/journal/review-flags",
      "/api/journal/experiment-label",
      "/api/journal/display-corrections"
    ]);
    for (const [path] of fetchImpl.mock.calls) {
      expect(String(path)).not.toMatch(/^\/journal/);
    }
  });

  it("returns safe Match Journal unavailable envelopes and rejects malformed journal payloads", async () => {
    const unavailable = buildMatchJournalPayload({ status: "unavailable", errors: ["service_unavailable"] });
    const unavailableFetch = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) =>
      jsonResponse(unavailable, { status: 503 })
    );
    await expect(
      fetchMatchJournal({ parser_match_id: "match:history:1" }, unavailableFetch as unknown as typeof fetch)
    ).resolves.toEqual(unavailable);

    const malformedFetch = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) =>
      jsonResponse({ ...unavailable, schema_version: "future.schema" })
    );
    await expect(
      fetchMatchJournal({ parser_match_id: "match:history:1" }, malformedFetch as unknown as typeof fetch)
    ).rejects.toBeInstanceOf(MatchJournalApiError);
    await expect(
      fetchMatchJournal({ parser_match_id: "match:history:1" }, malformedFetch as unknown as typeof fetch)
    ).rejects.toMatchObject({ code: "incompatible_response" });
  });

  it("fetches and validates match and game history responses", async () => {
    const matchPayload = buildMatchHistoryPayload();
    const gamePayload = buildGameHistoryPayload();
    const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/api/analytics/matches")) {
        return jsonResponse(matchPayload);
      }
      return jsonResponse(gamePayload);
    }) as unknown as typeof fetch;

    await expect(fetchMatchHistory(fetchImpl)).resolves.toEqual(matchPayload);
    await expect(fetchGameHistory(fetchImpl)).resolves.toEqual(gamePayload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/matches", {
      headers: { Accept: "application/json" }
    });
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/games", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects incompatible or malformed history responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildMatchHistoryPayload(), schema_version: "future.schema" })
    ) as unknown as typeof fetch;
    await expect(fetchMatchHistory(wrongSchemaFetch)).rejects.toMatchObject({ code: "incompatible_response" });

    const wrongObjectFetch = vi.fn(async () =>
      jsonResponse({ ...buildGameHistoryPayload(), object: MATCH_HISTORY_OBJECT })
    ) as unknown as typeof fetch;
    await expect(fetchGameHistory(wrongObjectFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const malformedRowsFetch = vi.fn(async () =>
      jsonResponse({ ...buildMatchHistoryPayload(), rows: [{ match_id: "match:1" }] })
    ) as unknown as typeof fetch;
    await expect(fetchMatchHistory(malformedRowsFetch)).rejects.toMatchObject({ code: "malformed_response" });
  });

  it("rejects unsupported or private-marker history status labels safely", async () => {
    const privateStatus = "C:\\secret\\Player.log";
    const privateStatusFetch = vi.fn(async () =>
      jsonResponse({ ...buildMatchHistoryPayload(), status: privateStatus })
    ) as unknown as typeof fetch;
    await expect(fetchMatchHistory(privateStatusFetch)).rejects.toMatchObject({ code: "malformed_response" });

    try {
      await fetchMatchHistory(privateStatusFetch);
    } catch (error) {
      expect(String(error)).not.toContain(privateStatus);
      expect(String(error)).not.toContain("Player.log");
    }

    const unsupportedStatusFetch = vi.fn(async () =>
      jsonResponse({ ...buildGameHistoryPayload(), status: "stale_unknown_status" })
    ) as unknown as typeof fetch;
    await expect(fetchGameHistory(unsupportedStatusFetch)).rejects.toMatchObject({ code: "malformed_response" });
  });

  it("maps history request failures to history API errors", async () => {
    const fetchImpl = vi.fn(async () => {
      throw new Error("synthetic network failure");
    }) as unknown as typeof fetch;

    await expect(fetchMatchHistory(fetchImpl)).rejects.toBeInstanceOf(AnalyticsHistoryApiError);
    await expect(fetchMatchHistory(fetchImpl)).rejects.toMatchObject({ code: "backend_unavailable" });
  });

  it("fetches and validates opening hand and mulligan history responses", async () => {
    const openingPayload = buildOpeningHandHistoryPayload();
    const mulliganPayload = buildMulliganHistoryPayload();
    const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/api/analytics/opening-hands")) {
        return jsonResponse(openingPayload);
      }
      return jsonResponse(mulliganPayload);
    }) as unknown as typeof fetch;

    await expect(fetchOpeningHandHistory(fetchImpl)).resolves.toEqual(openingPayload);
    await expect(fetchMulliganHistory(fetchImpl)).resolves.toEqual(mulliganPayload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/opening-hands", {
      headers: { Accept: "application/json" }
    });
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/mulligans", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed early-game history responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildOpeningHandHistoryPayload(), schema_version: ANALYTICS_HISTORY_SCHEMA_VERSION })
    ) as unknown as typeof fetch;
    await expect(fetchOpeningHandHistory(wrongSchemaFetch)).rejects.toMatchObject({ code: "incompatible_response" });

    const wrongObjectFetch = vi.fn(async () =>
      jsonResponse({ ...buildMulliganHistoryPayload(), object: OPENING_HAND_HISTORY_OBJECT })
    ) as unknown as typeof fetch;
    await expect(fetchMulliganHistory(wrongObjectFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const malformedRowsFetch = vi.fn(async () =>
      jsonResponse({ ...buildOpeningHandHistoryPayload(), rows: [{ opening_hand_id: "opening:1" }] })
    ) as unknown as typeof fetch;
    await expect(fetchOpeningHandHistory(malformedRowsFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const unsupportedCardActionFetch = vi.fn(async () =>
      jsonResponse({
        ...buildMulliganHistoryPayload(),
        rows: [
          {
            ...buildMulliganHistoryPayload().rows[0],
            cards: [{ ...buildMulliganHistoryPayload().rows[0].cards[0], card_action: "coaching_label" }]
          }
        ]
      })
    ) as unknown as typeof fetch;
    await expect(fetchMulliganHistory(unsupportedCardActionFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });
  });

  it("fetches and validates gameplay action and opponent observation review responses", async () => {
    const actionPayload = buildGameplayActionReviewPayload();
    const observationPayload = buildOpponentObservationReviewPayload();
    const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/api/analytics/gameplay-actions")) {
        return jsonResponse(actionPayload);
      }
      return jsonResponse(observationPayload);
    }) as unknown as typeof fetch;

    await expect(fetchGameplayActionReview(fetchImpl)).resolves.toEqual(actionPayload);
    await expect(fetchOpponentCardObservationReview(fetchImpl)).resolves.toEqual(observationPayload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/gameplay-actions", {
      headers: { Accept: "application/json" }
    });
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/opponent-card-observations", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed action review responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildGameplayActionReviewPayload(), schema_version: EARLY_GAME_HISTORY_SCHEMA_VERSION })
    ) as unknown as typeof fetch;
    await expect(fetchGameplayActionReview(wrongSchemaFetch)).rejects.toMatchObject({
      code: "incompatible_response"
    });

    const wrongObjectFetch = vi.fn(async () =>
      jsonResponse({ ...buildOpponentObservationReviewPayload(), object: GAMEPLAY_ACTION_REVIEW_OBJECT })
    ) as unknown as typeof fetch;
    await expect(fetchOpponentCardObservationReview(wrongObjectFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const malformedRowsFetch = vi.fn(async () =>
      jsonResponse({ ...buildGameplayActionReviewPayload(), rows: [{ gameplay_action_id: "action:1" }] })
    ) as unknown as typeof fetch;
    await expect(fetchGameplayActionReview(malformedRowsFetch)).rejects.toMatchObject({ code: "malformed_response" });

    const malformedFlagsFetch = vi.fn(async () =>
      jsonResponse({
        ...buildOpponentObservationReviewPayload(),
        rows: [
          {
            ...buildOpponentObservationReviewPayload().rows[0],
            degradation_flags: "missing_expected_evidence"
          }
        ]
      })
    ) as unknown as typeof fetch;
    await expect(fetchOpponentCardObservationReview(malformedFlagsFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });
  });

  it("fetches and validates play-draw and game1-postboard split review responses", async () => {
    const playDrawPayload = buildPlayDrawSplitReviewPayload();
    const postboardPayload = buildGame1PostboardSplitReviewPayload();
    const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/api/analytics/play-draw-splits")) {
        return jsonResponse(playDrawPayload);
      }
      return jsonResponse(postboardPayload);
    }) as unknown as typeof fetch;

    await expect(fetchPlayDrawSplitReview(fetchImpl)).resolves.toEqual(playDrawPayload);
    await expect(fetchGame1PostboardSplitReview(fetchImpl)).resolves.toEqual(postboardPayload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/play-draw-splits", {
      headers: { Accept: "application/json" }
    });
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/game1-postboard-splits", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed split review responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildPlayDrawSplitReviewPayload(), schema_version: ACTION_REVIEW_SCHEMA_VERSION })
    ) as unknown as typeof fetch;
    await expect(fetchPlayDrawSplitReview(wrongSchemaFetch)).rejects.toMatchObject({
      code: "incompatible_response"
    });

    const wrongObjectFetch = vi.fn(async () =>
      jsonResponse({ ...buildGame1PostboardSplitReviewPayload(), object: PLAY_DRAW_SPLIT_REVIEW_OBJECT })
    ) as unknown as typeof fetch;
    await expect(fetchGame1PostboardSplitReview(wrongObjectFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const malformedSummaryFetch = vi.fn(async () =>
      jsonResponse({ ...buildPlayDrawSplitReviewPayload(), summary: { row_count: 1 } })
    ) as unknown as typeof fetch;
    await expect(fetchPlayDrawSplitReview(malformedSummaryFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const malformedRowsFetch = vi.fn(async () =>
      jsonResponse({ ...buildGame1PostboardSplitReviewPayload(), rows: [{ game_result_id: "result:1" }] })
    ) as unknown as typeof fetch;
    await expect(fetchGame1PostboardSplitReview(malformedRowsFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });
  });

  it("fetches and validates dynamic dashboard module responses", async () => {
    const payload = buildAnalyticsDashboardModulesPayload();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(fetchAnalyticsDashboardModules(fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/dashboard/modules", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed dashboard module responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildAnalyticsDashboardModulesPayload(), schema_version: SPLIT_REVIEW_SCHEMA_VERSION })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsDashboardModules(wrongSchemaFetch)).rejects.toMatchObject({
      code: "incompatible_response"
    });

    const unsafeBuilderFetch = vi.fn(async () =>
      jsonResponse({
        ...buildAnalyticsDashboardModulesPayload(),
        custom_explorer: { ...buildAnalyticsDashboardModulesPayload().custom_explorer, builder_ui_enabled: true }
      })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsDashboardModules(unsafeBuilderFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const malformedRowsFetch = vi.fn(async () =>
      jsonResponse({
        ...buildAnalyticsDashboardModulesPayload(),
        modules: [{ ...buildAnalyticsDashboardModulesPayload().modules[0], rows: [{ row_id: "row:1" }] }]
      })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsDashboardModules(malformedRowsFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });
  });

  it("fetches and validates analytics refresh-state responses", async () => {
    const payload = buildAnalyticsRefreshStatePayload();
    const fetchImpl = vi.fn(async () => jsonResponse(payload)) as unknown as typeof fetch;

    await expect(fetchAnalyticsRefreshState(fetchImpl)).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith("/api/analytics/refresh-state", {
      headers: { Accept: "application/json" }
    });
  });

  it("rejects malformed analytics refresh-state responses safely", async () => {
    const wrongSchemaFetch = vi.fn(async () =>
      jsonResponse({ ...buildAnalyticsRefreshStatePayload(), schema_version: ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsRefreshState(wrongSchemaFetch)).rejects.toMatchObject({
      code: "incompatible_response"
    });

    const wrongObjectFetch = vi.fn(async () =>
      jsonResponse({ ...buildAnalyticsRefreshStatePayload(), object: ANALYTICS_DASHBOARD_MODULES_OBJECT })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsRefreshState(wrongObjectFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const malformedCountsFetch = vi.fn(async () =>
      jsonResponse({
        ...buildAnalyticsRefreshStatePayload(),
        row_counts: { ...buildAnalyticsRefreshStatePayload().row_counts, match_results: -1 }
      })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsRefreshState(malformedCountsFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });

    const unsafeTimestampFetch = vi.fn(async () =>
      jsonResponse({
        ...buildAnalyticsRefreshStatePayload(),
        latest_completed_match_seen_at: String.raw`C:\operator\AppData\Local\MythicEdge\Player.log`
      })
    ) as unknown as typeof fetch;
    await expect(fetchAnalyticsRefreshState(unsafeTimestampFetch)).rejects.toMatchObject({
      code: "malformed_response"
    });
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

  it("submits browser upload import requests as multipart form data", async () => {
    const payload = buildManualImportJob();
    const firstFile = new File(['{"kind":"MatchState"}\n'], "a_events.jsonl", { type: "application/jsonl" });
    const secondFile = new File(['{"kind":"GameResult"}\n'], "b_events.jsonl", { type: "application/jsonl" });
    const fetchImpl = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      expect(init?.method).toBe("POST");
      expect(init?.headers).toEqual({ Accept: "application/json" });
      expect(init?.body).toBeInstanceOf(FormData);

      const formData = init?.body as FormData;
      const files = formData.getAll("files");
      expect(files).toHaveLength(2);
      expect(files[0]).toBe(firstFile);
      expect(files[1]).toBe(secondFile);
      expect(formData.get("source_artifact_label")).toBe("safe_upload_label");

      return jsonResponse(payload);
    }) as unknown as typeof fetch;

    await expect(
      submitManualJsonlUpload(
        {
          files: [firstFile, secondFile],
          source_artifact_label: " safe_upload_label "
        },
        fetchImpl
      )
    ).resolves.toEqual(payload);
    expect(fetchImpl).toHaveBeenCalledWith(
      "/api/imports/jsonl/upload",
      expect.objectContaining({
        method: "POST",
        headers: { Accept: "application/json" },
        body: expect.any(FormData)
      })
    );
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

function jsonResponse(payload: unknown, init: ResponseInit = {}): Response {
  return new Response(JSON.stringify(payload), {
    status: init.status ?? 200,
    statusText: init.statusText,
    headers: { "Content-Type": "application/json", ...init.headers }
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
    match_journal: { status: "not_initialized" },
    migrations: { status: "ok" },
    runtime: { status: "ok" },
    capabilities: { setup_status: "enabled", match_journal_write_controls: "enabled_on_first_write" }
  };
}

function buildErrorReportPreviewPayload(
  overrides: Partial<ErrorReportPreviewResponse> = {}
): ErrorReportPreviewResponse {
  return {
    schema: ERROR_REPORT_PREVIEW_SCHEMA,
    status: "preview_ready",
    issue_title: "[error-report] [bug] [local_app_ui] Dashboard status did not refresh",
    issue_body_markdown: "# [error-report] [bug] [local_app_ui] Dashboard status did not refresh",
    included_diagnostic_categories: ["backend_health", "privacy_boundary"],
    excluded_private_data: ["raw Player.log contents or raw log lines"],
    redaction_summary: ["No user-entered private path redactions were needed."],
    warnings: [],
    next_recommended_role: "Codex A or Codex B after reviewing the sanitized report",
    external_submission_enabled: false,
    ...overrides
  };
}

function buildErrorReportSubmissionPayload(): ErrorReportSubmissionResponse {
  return {
    object: ERROR_REPORT_SUBMISSION_OBJECT,
    schema_version: ERROR_REPORT_SUBMISSION_SCHEMA,
    status: "submitted",
    external_submission_enabled: true,
    submitted: true,
    issue_url: "https://github.com/Tahjali11/Mythic-Edge/issues/999",
    issue_number: 999,
    issue_title: "[error-report] [bug] [local_app_ui] Dashboard status did not refresh",
    issue_body_markdown: "# [error-report] [bug] [local_app_ui] Dashboard status did not refresh",
    labels: ["bug", "layer:dashboard", "workflow:problem"],
    fallback_available: true,
    warnings: [],
    errors: []
  };
}

function buildLivePlayerLogStatusPayload(): LivePlayerLogStatusResponse {
  return {
    object: LIVE_PLAYER_LOG_STATUS_OBJECT,
    schema_version: LIVE_STATUS_SCHEMA_VERSION,
    status: "ok",
    player_log: {
      status: "configured_exists",
      source: "configured",
      display_path: "<configured_player_log>",
      path_kind: "file",
      metadata_access: "accessible",
      exists: true,
      contents_read: false,
      tailing_started: false,
      size_bytes: 42,
      last_modified_at: "2026-06-02T00:00:00Z",
      last_modified_age_seconds: 1,
      activity_hint: "recent"
    },
    diagnostics: ["readability_not_probed", "rotation_detection_deferred", "truncation_detection_deferred"],
    warnings: [],
    errors: []
  };
}

function buildLiveWatcherStatusPayload(): LiveWatcherStatusResponse {
  return {
    object: LIVE_WATCHER_STATUS_OBJECT,
    schema_version: LIVE_STATUS_SCHEMA_VERSION,
    status: "ready",
    watcher: {
      status: "ready",
      mode: "readiness_only",
      running: false,
      start_allowed: false,
      stop_allowed: false,
      parser_runner_started: false,
      tailing_started: false,
      sqlite_live_writes_enabled: false,
      reason: null
    },
    player_log: {
      status: "configured_exists",
      source: "configured",
      display_path: "<configured_player_log>",
      path_kind: "file",
      metadata_access: "accessible",
      exists: true,
      contents_read: false,
      tailing_started: false,
      size_bytes: 42,
      last_modified_at: "2026-06-02T00:00:00Z",
      last_modified_age_seconds: 1,
      activity_hint: "recent"
    },
    warnings: [],
    errors: []
  };
}

function buildLiveWatcherProcessStatusPayload(): LiveWatcherProcessStatusResponse {
  return {
    object: LIVE_WATCHER_PROCESS_OBJECT,
    schema_version: LIVE_WATCHER_PROCESS_SCHEMA_VERSION,
    status: "not_initialized",
    process_control: {
      mode: "safeguards_only",
      implementation_status: "not_implemented",
      start_allowed: false,
      stop_allowed: false,
      start_route_enabled: false,
      stop_route_enabled: false,
      ui_controls_allowed: false,
      automatic_start_enabled: false,
      parser_runner_started: false,
      tailing_started: false,
      sqlite_live_writes_enabled: false,
      external_transport_allowed: false,
      reason: "watcher_state_missing"
    },
    watcher: {
      status: "not_initialized",
      running: false,
      pid_verified: false,
      single_instance_guard: "not_initialized",
      supervisor_boundary: "local_app_supervisor_deferred"
    },
    player_log: {
      object: LIVE_PLAYER_LOG_STATUS_OBJECT,
      status: "configured_exists",
      source: "configured",
      display_path: "<configured_player_log>",
      path_kind: "file",
      metadata_access: "accessible",
      exists: true,
      contents_read: false,
      tailing_started: false
    },
    preconditions: [
      { key: "player_log_ready", status: "pass", reason: null },
      { key: "app_data_root_available", status: "pass", reason: null },
      { key: "state_directory_available", status: "deferred", reason: "state_directory_not_created_by_get" },
      { key: "single_instance_guard_available", status: "deferred", reason: "single_instance_guard_deferred" },
      { key: "supervisor_target_defined", status: "deferred", reason: "supervisor_target_deferred" },
      { key: "external_transport_disabled", status: "pass", reason: null },
      { key: "live_sqlite_ingest_contract_present", status: "pass", reason: null },
      { key: "frontend_controls_authorized", status: "deferred", reason: "frontend_controls_not_authorized" }
    ],
    state: {
      source: "none",
      exists: false,
      status: "not_initialized",
      stale: false,
      pid_present: false,
      pid_verified: false,
      supervisor_token_present: false,
      display_path: "<app_data>\\jobs\\live_watcher_state.json",
      raw_path_exposed: false
    },
    warnings: [],
    errors: []
  };
}

function buildLiveCaptureStatusPayload(overrides: Partial<LiveCaptureStatusResponse> = {}): LiveCaptureStatusResponse {
  return {
    object: LIVE_CAPTURE_STATUS_OBJECT,
    schema_version: LIVE_CAPTURE_SCHEMA_VERSION,
    status: "ready_to_start",
    mode: "explicit_operator_control",
    capture: {
      running: false,
      start_allowed: true,
      stop_allowed: false,
      parser_runner_started: false,
      tailing_started: false,
      sqlite_live_writes_enabled: false,
      external_transport_allowed: false,
      raw_player_log_storage_enabled: false,
      supervisor_kind: "local_app_capture_supervisor",
      source_kind: "live_parser",
      reason: null
    },
    preconditions: [
      { key: "player_log_ready", status: "pass", reason: null },
      { key: "app_data_root_available", status: "pass", reason: null },
      { key: "state_directory_available", status: "pass", reason: null },
      { key: "single_instance_guard_available", status: "pass", reason: null },
      { key: "supervisor_target_defined", status: "pass", reason: null },
      { key: "external_transport_disabled", status: "pass", reason: null },
      { key: "live_sqlite_ingest_contract_present", status: "pass", reason: null },
      { key: "analytics_database_available", status: "pass", reason: null },
      { key: "frontend_controls_authorized", status: "pass", reason: null }
    ],
    state: {
      source: "none",
      exists: false,
      status: "not_initialized",
      stale: false,
      pid_present: false,
      pid_verified: false,
      supervisor_token_present: false,
      display_path: "<app_data>\\jobs\\live_capture_state.json",
      raw_path_exposed: false,
      started_at: null,
      updated_at: null
    },
    last_result: null,
    heartbeat: {
      schema_version: LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
      status: "not_started",
      heartbeat_updated_at: null,
      capture_duration_seconds: 0,
      heartbeat_age_seconds: null,
      stale_after_seconds: 30
    },
    progress: {
      schema_version: LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
      log_poll_count: 0,
      log_chunks_seen: 0,
      structured_entry_count: 0,
      parser_event_count: 0,
      parser_event_kinds_seen: [],
      match_ids_seen_count: 0,
      current_match_detected: false,
      current_match_game_wins: null,
      current_match_game_losses: null,
      last_completed_match_result: null,
      last_completed_match_game_wins: null,
      last_completed_match_game_losses: null,
      completed_game_rows_seen: 0,
      sqlite_write_attempt_count: 0,
      sqlite_rows_written: 0,
      last_no_write_reason: "not_started",
      last_event_seen_at: null,
      last_sqlite_write_at: null
    },
    parser_status_blurb: {
      code: "ready_to_start",
      text: "Ready to start capture.",
      tone: "neutral"
    },
    warnings: [],
    errors: [],
    ...overrides
  };
}

function buildLiveWatcherDiagnosticsPayload(): LiveWatcherDiagnosticsResponse {
  return {
    object: LIVE_WATCHER_DIAGNOSTICS_OBJECT,
    schema_version: LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION,
    status: "degraded",
    mode: "read_only_composition",
    summary: {
      info_count: 4,
      warning_count: 1,
      degraded_count: 0,
      error_count: 0,
      blocked_count: 0,
      unknown_count: 0
    },
    diagnostics: [
      {
        category: "player_log_metadata",
        key: "readability_not_probed",
        severity: "info",
        status: "readability_not_probed",
        evidence_availability: "deferred",
        source: "player_log_status",
        message: "Readability was not checked because diagnostics do not read Player.log contents.",
        count: null,
        review_required: false
      },
      {
        category: "player_log_metadata",
        key: "player_log_stale",
        severity: "warning",
        status: "player_log_stale",
        evidence_availability: "metadata_only",
        source: "player_log_status",
        message: "Player.log metadata indicates stale activity.",
        count: null,
        review_required: true
      }
    ],
    sources: {
      player_log_status: {
        supplied: true,
        status: "degraded",
        schema_version: LIVE_STATUS_SCHEMA_VERSION,
        evidence_availability: "metadata_only",
        limitations: ["contents_not_read"]
      },
      tailer_event_bridge: {
        supplied: false,
        status: "deferred",
        schema_version: null,
        evidence_availability: "deferred",
        limitations: ["tailer_not_called"]
      }
    },
    privacy: {
      raw_player_log_content_included: false,
      raw_player_log_path_included: false,
      raw_hashes_included: false,
      raw_sql_included: false,
      stack_traces_included: false,
      secrets_or_environment_values_included: false
    },
    capabilities: {
      read_only: true,
      starts_watcher: false,
      stops_watcher: false,
      tails_player_log: false,
      writes_sqlite: false,
      writes_diagnostics_files: false,
      external_transport_allowed: false
    },
    warnings: ["player_log_stale"],
    errors: []
  };
}

function buildMatchJournalPayload(overrides: Partial<MatchJournalResponse> = {}): MatchJournalResponse {
  return {
    object: MATCH_JOURNAL_OBJECT,
    schema_version: MATCH_JOURNAL_SCHEMA_VERSION,
    status: "ok",
    result: {
      bundle: {
        match: { parser_match_id: "match:history:1" },
        games: [{ parser_game_id: "match:history:1:g1" }],
        notes: [{ journal_note_id: "note:1" }],
        labels: [{ journal_label_id: "label:1" }],
        review_flags: [{ journal_review_flag_id: "flag:1" }],
        field_overrides: [{ journal_field_override_id: "override:1", effect_scope: "journal_display_only" }],
        warnings: []
      }
    },
    warnings: [],
    errors: [],
    ...overrides
  };
}

function buildHistoryStatus() {
  return {
    value_source: "observed",
    confidence: "high",
    finality: "final",
    drift_status: "none",
    availability_status: "available",
    source_parser_surface: "synthetic_history_test",
    source_fact_key: "synthetic_fact",
    ingest_run_id: "ingest:history:test"
  };
}

function buildMatchHistoryPayload(): MatchHistoryResponse {
  return {
    object: MATCH_HISTORY_OBJECT,
    schema_version: ANALYTICS_HISTORY_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 1
    },
    summary: {
      row_count: 1,
      degraded_row_count: 0,
      unavailable_row_count: 0,
      conflict_row_count: 0
    },
    rows: [
      {
        match_id: "match:history:1",
        parser_match_key: "match:history:1",
        match_started_at: "2026-05-30T00:00:00Z",
        match_completed_at: "2026-05-30T00:30:00Z",
        match_result: "W",
        match_win: 1,
        games_won: 2,
        games_lost: 1,
        total_games: 3,
        game_win_rate: 0.667,
        queue_name: "Ranked",
        format_name: "Standard",
        event_id: "PremierDraft",
        match_status: buildHistoryStatus(),
        result_status: buildHistoryStatus(),
        context_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildGameHistoryPayload(): GameHistoryResponse {
  return {
    object: GAME_HISTORY_OBJECT,
    schema_version: ANALYTICS_HISTORY_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 1
    },
    summary: {
      row_count: 1,
      degraded_row_count: 0,
      unavailable_row_count: 0,
      conflict_row_count: 0
    },
    rows: [
      {
        game_id: "match:history:1:g1",
        match_id: "match:history:1",
        game_number: 1,
        game_started_at: "2026-05-30T00:00:00Z",
        game_completed_at: "2026-05-30T00:10:00Z",
        local_result: "win",
        winner_team_id: 1,
        pre_postboard_label: "game1",
        play_draw: "play",
        turn_count: 8,
        game_duration_seconds: 900,
        queue_name: "Ranked",
        format_name: "Standard",
        event_id: "PremierDraft",
        game_status: buildHistoryStatus(),
        result_status: buildHistoryStatus(),
        context_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildOpeningHandHistoryPayload(): OpeningHandHistoryResponse {
  return {
    object: OPENING_HAND_HISTORY_OBJECT,
    schema_version: EARLY_GAME_HISTORY_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 1
    },
    summary: {
      row_count: 1,
      card_row_count: 1,
      degraded_row_count: 0,
      unavailable_row_count: 0,
      conflict_row_count: 0
    },
    rows: [
      {
        opening_hand_id: "match:history:1:g1:opening_hand",
        match_id: "match:history:1",
        game_id: "match:history:1:g1",
        game_number: 1,
        hand_size: 7,
        exact_card_count: 1,
        local_result: "win",
        play_draw: "play",
        pre_postboard_label: "game1",
        match_result: "W",
        match_win: 1,
        queue_name: "Ranked",
        format_name: "Standard",
        event_id: "PremierDraft",
        cards: [
          {
            opening_hand_card_id: "match:history:1:g1:opening_hand:slot1",
            card_position: 1,
            grp_id: 1001,
            card_name: "Forest",
            identity_hint_source: "direct_grp_id",
            name_resolution_status: "resolved",
            card_status: buildHistoryStatus()
          }
        ],
        opening_hand_status: buildHistoryStatus(),
        game_status: buildHistoryStatus(),
        game_result_status: buildHistoryStatus(),
        match_result_status: buildHistoryStatus(),
        context_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildMulliganHistoryPayload(): MulliganHistoryResponse {
  return {
    object: MULLIGAN_HISTORY_OBJECT,
    schema_version: EARLY_GAME_HISTORY_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 1
    },
    summary: {
      row_count: 1,
      card_row_count: 1,
      degraded_row_count: 0,
      unavailable_row_count: 0,
      conflict_row_count: 0
    },
    rows: [
      {
        mulligan_event_id: "match:history:1:g1:mulligan:1",
        match_id: "match:history:1",
        game_id: "match:history:1:g1",
        game_number: 1,
        ordinal_or_count: "1",
        mulligan_count: 1,
        decision_detail: "mulliganed_to_six",
        local_result: "win",
        play_draw: "play",
        pre_postboard_label: "game1",
        match_result: "W",
        match_win: 1,
        queue_name: "Ranked",
        format_name: "Standard",
        event_id: "PremierDraft",
        cards: [
          {
            mulligan_card_id: "match:history:1:g1:mulligan:1:card1",
            card_position: 1,
            card_action: "bottomed",
            grp_id: 1002,
            card_name: "Island",
            identity_hint_source: "direct_grp_id",
            card_status: buildHistoryStatus()
          }
        ],
        mulligan_status: buildHistoryStatus(),
        game_status: buildHistoryStatus(),
        game_result_status: buildHistoryStatus(),
        match_result_status: buildHistoryStatus(),
        context_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildGameplayActionReviewPayload(): GameplayActionReviewResponse {
  return {
    object: GAMEPLAY_ACTION_REVIEW_OBJECT,
    schema_version: ACTION_REVIEW_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 1
    },
    summary: {
      row_count: 1,
      card_row_count: 1,
      degraded_row_count: 0,
      unavailable_row_count: 0,
      conflict_row_count: 0,
      review_required_row_count: 0
    },
    rows: [
      {
        gameplay_action_id: "match:history:1:g1:action:cast",
        match_id: "match:history:1",
        game_id: "match:history:1:g1",
        game_number: 1,
        timestamp: "2026-05-30T00:05:00Z",
        game_state_id: 123,
        turn_number: 2,
        action_type: "cast",
        actor_relation: "opponent",
        from_zone_type: "hand",
        to_zone_type: "stack",
        source_status: "observed",
        annotation_context_label: "gameplay_action",
        raw_action_type_labels: "cast",
        annotation_type_labels: "spell",
        visible_in_log: true,
        card_count: 1,
        grp_ids: [1001],
        local_result: "win",
        play_draw: "play",
        pre_postboard_label: "game1",
        match_result: "W",
        match_win: 1,
        queue_name: "Ranked",
        format_name: "Standard",
        event_id: "PremierDraft",
        cards: [
          {
            gameplay_action_card_id: "match:history:1:g1:action:cast:card1",
            card_ordinal: 1,
            instance_id: 10001,
            grp_id: 1001,
            observed_grp_id: 1001,
            overlay_grp_id: null,
            object_source_grp_id: 1001,
            identity_hint_source: "direct_grp_id",
            card_name: "Forest",
            display_name: "Forest",
            name_resolution_status: "resolved",
            enrichment_status: "not_needed",
            card_status: buildHistoryStatus()
          }
        ],
        gameplay_action_status: buildHistoryStatus(),
        game_status: buildHistoryStatus(),
        game_result_status: buildHistoryStatus(),
        match_result_status: buildHistoryStatus(),
        context_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildOpponentObservationReviewPayload(): OpponentCardObservationReviewResponse {
  return {
    object: OPPONENT_CARD_OBSERVATION_REVIEW_OBJECT,
    schema_version: ACTION_REVIEW_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 1
    },
    summary: {
      row_count: 1,
      card_row_count: 1,
      degraded_row_count: 1,
      unavailable_row_count: 0,
      conflict_row_count: 0,
      review_required_row_count: 1
    },
    rows: [
      {
        opponent_card_observation_id: "match:history:1:g1:observation:2",
        gameplay_action_id: "match:history:1:g1:action:cast",
        match_id: "match:history:1",
        game_id: "match:history:1:g1",
        game_number: 1,
        timestamp: "2026-05-30T00:05:01Z",
        game_state_id: 124,
        turn_number: 2,
        actor_relation: "opponent",
        actor_seat_id: 2,
        local_seat_id: 1,
        instance_id: 20001,
        grp_id: 2001,
        observed_grp_id: 2001,
        overlay_grp_id: null,
        object_source_grp_id: 2001,
        parent_id: null,
        identity_hint_source: "visible_object",
        card_name: "Island",
        display_name: "Island",
        resolution_status: "resolved",
        name_resolution_source: "local_catalog",
        action_type: "cast",
        cast_mode: "normal",
        source_evidence: "gameplay_action",
        evidence_status: "visible",
        visibility: "public",
        from_zone_type: "hand",
        to_zone_type: "stack",
        degradation_flags: ["missing_expected_evidence"],
        review_required: true,
        linked_gameplay_action: {
          gameplay_action_id: "match:history:1:g1:action:cast",
          turn_number: 2,
          action_type: "cast",
          actor_relation: "opponent",
          from_zone_type: "hand",
          to_zone_type: "stack",
          visible_in_log: true
        },
        local_result: "win",
        play_draw: "play",
        pre_postboard_label: "game1",
        match_result: "W",
        match_win: 1,
        queue_name: "Ranked",
        format_name: "Standard",
        event_id: "PremierDraft",
        cards: [
          {
            opponent_card_observation_card_id: "match:history:1:g1:observation:2:card1",
            card_ordinal: 1,
            grp_id: 2001,
            observed_grp_id: 2001,
            overlay_grp_id: null,
            object_source_grp_id: 2001,
            identity_hint_source: "visible_object",
            card_name: "Island",
            resolution_status: "resolved",
            visibility: "public",
            card_status: buildHistoryStatus()
          }
        ],
        opponent_card_observation_status: buildHistoryStatus(),
        linked_gameplay_action_status: buildHistoryStatus(),
        game_status: buildHistoryStatus(),
        game_result_status: buildHistoryStatus(),
        match_result_status: buildHistoryStatus(),
        context_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildPlayDrawSplitReviewPayload(): PlayDrawSplitReviewResponse {
  return {
    object: PLAY_DRAW_SPLIT_REVIEW_OBJECT,
    schema_version: SPLIT_REVIEW_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 2
    },
    summary: {
      row_count: 2,
      total_game_count: 12,
      known_result_count: 11,
      wins: 7,
      losses: 4,
      unknown_result_count: 1,
      unavailable_result_count: 1,
      degraded_result_count: 1,
      small_sample_group_count: 1
    },
    rows: [
      {
        play_draw: "play",
        game_count: 10,
        known_result_count: 10,
        wins: 6,
        losses: 4,
        unknown_result_count: 0,
        unavailable_result_count: 0,
        degraded_result_count: 0,
        win_rate: 0.6,
        sample_size_warning: "ok"
      },
      {
        play_draw: "draw",
        game_count: 2,
        known_result_count: 1,
        wins: 1,
        losses: 0,
        unknown_result_count: 1,
        unavailable_result_count: 1,
        degraded_result_count: 1,
        win_rate: 1,
        sample_size_warning: "small_sample"
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildGame1PostboardSplitReviewPayload(): Game1PostboardSplitReviewResponse {
  return {
    object: GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT,
    schema_version: SPLIT_REVIEW_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    pagination: {
      limit: 50,
      offset: 0,
      returned: 2
    },
    summary: {
      row_count: 2,
      game1_row_count: 1,
      postboard_row_count: 1,
      known_result_count: 2,
      unknown_result_count: 0,
      degraded_row_count: 0,
      unavailable_row_count: 0,
      conflict_row_count: 0
    },
    rows: [
      {
        game_result_id: "match:history:1:g1:game_result",
        match_id: "match:history:1",
        game_id: "match:history:1:g1",
        game_number: 1,
        pre_postboard_label: "game1",
        local_result: "win",
        play_draw: "play",
        turn_count: 8,
        game_duration_seconds: 900,
        game_result_status: buildHistoryStatus()
      },
      {
        game_result_id: "match:history:1:g2:game_result",
        match_id: "match:history:1",
        game_id: "match:history:1:g2",
        game_number: 2,
        pre_postboard_label: "postboard",
        local_result: "loss",
        play_draw: "draw",
        turn_count: null,
        game_duration_seconds: null,
        game_result_status: buildHistoryStatus()
      }
    ],
    warnings: [],
    errors: []
  };
}

function buildAnalyticsDashboardModulesPayload(): AnalyticsDashboardModulesResponse {
  const sourceMetadata = {
    source_tables_or_views: ["v_play_draw_splits", "v_sample_size_warnings"],
    source_contracts: ["docs/contracts/analytics_dynamic_decision_support_dashboard.md"],
    source_type: "fixed_sql_view",
    parser_truth_boundary: "Parser/state owns match and game facts.",
    analytics_truth_boundary: "Dashboard modules are fixed read-only projections."
  };
  const winRateMetric = {
    metric_id: "win_rate",
    label: "Win rate",
    value: 60,
    value_kind: "percentage" as const,
    unit: "percent",
    display: "60 percent",
    calculation_note: "Calculated over known win/loss game rows only.",
    source: "analytics_derived"
  };
  return {
    object: ANALYTICS_DASHBOARD_MODULES_OBJECT,
    schema_version: ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION,
    status: "ok",
    database: {
      display_path: "<app_data>\\db\\mythic_edge.sqlite3",
      exists: true,
      schema_status: "schema_current",
      status: "ok"
    },
    modules: [
      {
        module_id: "play_draw_win_rate",
        title: "Win Rate By Play/Draw",
        decision_question: "Am I performing differently on the play versus on the draw?",
        status: "ok",
        tone: "limited",
        default_view: "bar",
        allowed_views: ["bar", "table"],
        metric: winRateMetric,
        dimensions: [
          {
            dimension_id: "play_draw",
            label: "Play/draw",
            source: "v_play_draw_splits",
            value_source: "analytics_derived",
            allowed_values: ["play", "draw", "unknown"]
          }
        ],
        rows: [
          {
            row_id: "play_draw:play",
            label: "Play",
            dimension_values: { play_draw: "play" },
            metrics: [
              { metric_id: "game_count", label: "Games", value: 10, value_kind: "count", unit: "games", display: "10 games" },
              {
                metric_id: "known_result_count",
                label: "Known results",
                value: 10,
                value_kind: "count",
                unit: "games",
                display: "10 known games"
              },
              { metric_id: "wins", label: "Wins", value: 6, value_kind: "count", unit: "games", display: "6 wins" },
              { metric_id: "losses", label: "Losses", value: 4, value_kind: "count", unit: "games", display: "4 losses" },
              { metric_id: "win_rate", label: "Win rate", value: 60, value_kind: "percentage", unit: "percent", display: "60 percent" },
              {
                metric_id: "unknown_or_degraded_count",
                label: "Unknown or degraded",
                value: 0,
                value_kind: "count",
                unit: "games",
                display: "0 games"
              }
            ],
            status: "ok",
            tone: "ok",
            sample_size: { status: "ok", known_result_count: 10, total_count: 10 },
            warnings: [],
            source_metadata: sourceMetadata
          },
          {
            row_id: "play_draw:draw",
            label: "Draw",
            dimension_values: { play_draw: "draw" },
            metrics: [
              { metric_id: "game_count", label: "Games", value: 2, value_kind: "count", unit: "games", display: "2 games" },
              {
                metric_id: "known_result_count",
                label: "Known results",
                value: 1,
                value_kind: "count",
                unit: "games",
                display: "1 known games"
              },
              { metric_id: "wins", label: "Wins", value: 1, value_kind: "count", unit: "games", display: "1 wins" },
              { metric_id: "losses", label: "Losses", value: 0, value_kind: "count", unit: "games", display: "0 losses" },
              { metric_id: "win_rate", label: "Win rate", value: 100, value_kind: "percentage", unit: "percent", display: "100 percent" },
              {
                metric_id: "unknown_or_degraded_count",
                label: "Unknown or degraded",
                value: 1,
                value_kind: "count",
                unit: "games",
                display: "1 games"
              }
            ],
            status: "degraded",
            tone: "limited",
            sample_size: { status: "small_sample", known_result_count: 1, total_count: 2 },
            warnings: ["small_sample"],
            source_metadata: sourceMetadata
          }
        ],
        summary: {
          row_count: 2,
          known_result_count: 11,
          wins: 7,
          losses: 4,
          unknown_or_degraded_count: 1,
          win_rate_percent: 63.6,
          display: "7-4 over 11 known games"
        },
        warnings: ["small_sample"],
        errors: [],
        data_quality: {
          status: "ok",
          sample_size_status: "small_sample",
          known_result_count: 11,
          unknown_or_degraded_count: 1,
          review_required_count: 0,
          confidence: "medium",
          finality: "analytics_projection",
          notes: ["Limited sample; descriptive review only."]
        },
        source_metadata: sourceMetadata,
        schema_version: ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION
      },
      {
        module_id: "game1_postboard",
        title: "Game 1 / Postboard",
        decision_question: "Are my game 1 and postboard games showing different observed results?",
        status: "empty",
        tone: "empty",
        default_view: "bar",
        allowed_views: ["bar", "table"],
        metric: { ...winRateMetric, value: null, value_kind: "null", display: "No known results" },
        dimensions: [
          {
            dimension_id: "game1_postboard",
            label: "Game 1/postboard",
            source: "v_game1_vs_postboard",
            value_source: "analytics_derived",
            allowed_values: ["game1", "postboard", "unknown"]
          }
        ],
        rows: [],
        summary: { row_count: 0, known_result_count: 0, wins: 0, losses: 0, unknown_or_degraded_count: 0, display: "No known win/loss rows" },
        warnings: [],
        errors: [],
        data_quality: {
          status: "empty",
          sample_size_status: "empty",
          known_result_count: 0,
          unknown_or_degraded_count: 0,
          review_required_count: 0,
          confidence: "unknown",
          finality: "unknown",
          notes: []
        },
        source_metadata: { ...sourceMetadata, source_tables_or_views: ["v_game1_vs_postboard"], source_type: "fixed_backend_aggregation" },
        schema_version: ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION
      },
      {
        module_id: "mulligan_opening_hand_outcomes",
        title: "Mulligan / Opening Hand Outcomes",
        decision_question: "Are my keep and mulligan patterns associated with observed outcomes?",
        status: "empty",
        tone: "empty",
        default_view: "table",
        allowed_views: ["bar", "table"],
        metric: { ...winRateMetric, value: null, value_kind: "null", display: "No known results" },
        dimensions: [
          { dimension_id: "opening_hand_size", label: "Opening hand size", source: "opening_hands", value_source: "parser_normalized" },
          { dimension_id: "mulligan_bucket", label: "Mulligan bucket", source: "mulligan_events", value_source: "parser_normalized" }
        ],
        rows: [],
        summary: { row_count: 0, known_result_count: 0, wins: 0, losses: 0, unknown_or_degraded_count: 0, display: "No known win/loss rows" },
        warnings: [],
        errors: [],
        data_quality: {
          status: "empty",
          sample_size_status: "empty",
          known_result_count: 0,
          unknown_or_degraded_count: 0,
          review_required_count: 0,
          confidence: "unknown",
          finality: "unknown",
          notes: []
        },
        source_metadata: {
          ...sourceMetadata,
          source_tables_or_views: ["opening_hands", "mulligan_events", "game_results"],
          source_type: "fixed_backend_aggregation"
        },
        schema_version: ANALYTICS_DASHBOARD_MODULES_SCHEMA_VERSION
      }
    ],
    custom_explorer: {
      status: "deferred",
      builder_ui_enabled: false,
      query_execution_enabled: false,
      dimensions: [
        {
          dimension_id: "journal_matchup_label",
          label: "Journal matchup label",
          source: "future_match_journal_projection",
          value_source: "journal_annotation",
          annotation_boundary: "Journal annotation"
        }
      ],
      metrics: ["games_played", "wins", "losses", "win_rate"],
      warnings: ["custom_explorer_builder_deferred"],
      errors: []
    },
    warnings: [],
    errors: []
  };
}

function buildAnalyticsRefreshStatePayload(): AnalyticsRefreshStateResponse {
  return {
    object: ANALYTICS_REFRESH_STATE_OBJECT,
    schema_version: ANALYTICS_REFRESH_STATE_SCHEMA_VERSION,
    status: "ok",
    analytics_revision: "analytics-refresh-v1:synthetic",
    latest_completed_match_result_available: true,
    latest_completed_match_seen_at: "2026-06-08T00:10:00Z",
    latest_completed_ingest_finished_at: "2026-06-08T00:10:01Z",
    row_counts: {
      ingest_runs: 1,
      matches: 1,
      games: 3,
      match_results: 1,
      game_results: 3
    },
    warnings: [],
    errors: []
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
