import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  AnalyticsHistoryApiError,
  LiveStatusApiError,
  ManualImportApiError,
  MatchJournalApiError,
  SetupStatusApiError
} from "./api";
import { SetupStatusApp } from "./App";
import {
  ACTION_REVIEW_SCHEMA_VERSION,
  ANALYTICS_HISTORY_SCHEMA_VERSION,
  EARLY_GAME_HISTORY_SCHEMA_VERSION,
  GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT,
  GAME_HISTORY_OBJECT,
  GAMEPLAY_ACTION_REVIEW_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
  LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
  LIVE_PLAYER_LOG_STATUS_OBJECT,
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
  type GameHistoryResponse,
  type GameplayActionReviewResponse,
  type LegacyJsonlImportQuality,
  type LivePlayerLogStatusResponse,
  type LiveWatcherDiagnosticsResponse,
  type LiveWatcherProcessStatusResponse,
  type LiveWatcherStatusResponse,
  type ManualImportJob,
  type ManualImportSourceArtifact,
  type MatchJournalResponse,
  type MatchHistoryResponse,
  type MulliganHistoryResponse,
  type OpeningHandHistoryResponse,
  type OpponentCardObservationReviewResponse,
  type PlayDrawSplitReviewResponse,
  type SetupStatusResponse
} from "./types";

afterEach(() => {
  cleanup();
  window.sessionStorage.clear();
});

describe("SetupStatusApp", () => {
  it("renders safe setup-status panels from a degraded backend payload", async () => {
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} />);

    expect(screen.getByText("Checking local app setup")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Setup Status" })).toBeInTheDocument();

    expect(screen.getByText("Backend Reachability")).toBeInTheDocument();
    expect(screen.getByText("<app_data>")).toBeInTheDocument();
    expect(screen.getAllByText("<configured_player_log>").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("Live Player.log")).toBeInTheDocument();
    expect(screen.getByText("Live Watcher")).toBeInTheDocument();
    expect(screen.getByText("Live Watcher Process")).toBeInTheDocument();
    expect(screen.getByText("readiness_only")).toBeInTheDocument();
    expect(screen.getByText("safeguards_only")).toBeInTheDocument();
    expect(screen.getByText("not_capturing")).toBeInTheDocument();
    expect(screen.getByText("not_running")).toBeInTheDocument();
    expect(screen.getByText("<app_data>\\db\\mythic_edge.sqlite3")).toBeInTheDocument();
    expect(screen.getByText("<app_data>\\db\\match_journal.sqlite3")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Import JSONL" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();
  });

  it("renders live watcher diagnostics as a read-only safe summary", async () => {
    render(
      <SetupStatusApp
        fetchLiveDiagnostics={() => Promise.resolve(buildLiveWatcherDiagnosticsPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Live Diagnostics" })).toBeInTheDocument();
    expect(screen.getByText("Read-only watcher quality summary")).toBeInTheDocument();
    expect(screen.getByText("player_log_stale")).toBeInTheDocument();
    expect(screen.getByText("metadata_only")).toBeInTheDocument();
    expect(screen.getByText("raw log")).toBeInTheDocument();
    expect(screen.getAllByText("excluded").length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText("Z:\\private\\Player.log")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|clear|repair|start|stop|restart/i })).not.toBeInTheDocument();
  });

  it("renders live diagnostics API errors without raw backend details", async () => {
    render(
      <SetupStatusApp
        fetchLiveDiagnostics={() =>
          Promise.reject(
            new LiveStatusApiError("malformed_response", "Live watcher diagnostics has an unsupported shape.")
          )
        }
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Live Diagnostics" })).toBeInTheDocument();
    expect(screen.getByText("Live watcher diagnostics has an unsupported shape.")).toBeInTheDocument();
    expect(screen.queryByText("Traceback")).not.toBeInTheDocument();
    expect(screen.queryByText("Player.log body")).not.toBeInTheDocument();
  });

  it("redacts unsafe live Player.log display strings from setup-status summaries", async () => {
    const rawPath = "Z:\\synthetic\\unsafe\\Player.log";
    const livePlayerLog = {
      ...buildLivePlayerLogStatusPayload(),
      player_log: {
        ...buildLivePlayerLogStatusPayload().player_log,
        display_path: rawPath
      }
    };
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload({ live_player_log: livePlayerLog }))} />);

    expect(await screen.findByText("Unsafe display value redacted")).toBeInTheDocument();
    expect(screen.getAllByText("<redacted_path>").length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText(rawPath)).not.toBeInTheDocument();
    expect(screen.queryByText(/currently capturing/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /start|stop/i })).not.toBeInTheDocument();
  });

  it("renders read-only match and game history with a refresh control", async () => {
    const fetchMatches = vi.fn(async () => buildMatchHistoryPayload());
    const fetchGames = vi.fn(async () => buildGameHistoryPayload());
    const fetchOpeningHands = vi.fn(async () => buildOpeningHandHistoryPayload());
    const fetchMulligans = vi.fn(async () => buildMulliganHistoryPayload());
    render(
      <SetupStatusApp
        fetchGames={fetchGames}
        fetchMatches={fetchMatches}
        fetchMulligans={fetchMulligans}
        fetchOpeningHands={fetchOpeningHands}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Analytics History" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Match History" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Game History" })).toBeInTheDocument();
    expect(screen.getAllByText("match:history:1").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("match:history:1 game 1").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("2-1 of 3")).toBeInTheDocument();
    expect(screen.getAllByText("observed high final none available").length).toBeGreaterThanOrEqual(2);
    expect(screen.queryByText("Analytics Views")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Refresh History" }));

    await waitFor(() => {
      expect(fetchMatches).toHaveBeenCalledTimes(2);
      expect(fetchGames).toHaveBeenCalledTimes(2);
    });
  });

  it("renders Match Journal cockpit context and bundle without pilot-error or destructive controls", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchJournal={() => Promise.resolve(buildMatchJournalPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Match Journal Cockpit" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Read-only Context" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Journal Bundle" })).toBeInTheDocument();
    expect(screen.getAllByText("match:history:1").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("match:history:1:g1").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText("Display-only field")).toBeInTheDocument();
    expect(screen.getByLabelText("Display-only value")).toBeInTheDocument();
    expect(screen.queryByText(/pilot.error|best line|hidden card|player mistake|coaching|line tracer/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();
  });

  it("submits and reloads a no-context unattached smoke note without parser identity", async () => {
    const fetchJournal = vi.fn(async () => buildMatchJournalPayload());
    const submitJournalUnattachedNote = vi.fn(async (_request: unknown) =>
      buildMatchJournalPayload({
        result: {
          service_result: {
            action: "record_unattached_note",
            status: "completed",
            primary_record_type: "note",
            primary_record_id: "journal_note:smoke:1",
            record_counts: { note: 1 }
          }
        }
      })
    );
    const fetchJournalUnattachedNote = vi.fn(async () =>
      buildMatchJournalPayload({
        result: {
          note: {
            journal_note_id: "journal_note:smoke:1",
            note_scope: "unattached",
            attachment_status: "unattached",
            author_label: "codex_smoke_test",
            source_surface: "local_tool",
            privacy_label: "sanitized_fixture",
            smoke_marker_present: true
          }
        }
      })
    );
    const emptyMatches = { ...buildMatchHistoryPayload(), status: "empty" as const, rows: [] };
    const emptyGames = { ...buildGameHistoryPayload(), status: "empty" as const, rows: [] };
    const props = {
      fetchGames: () => Promise.resolve(emptyGames),
      fetchJournal,
      fetchJournalUnattachedNote,
      fetchMatches: () => Promise.resolve(emptyMatches),
      fetchStatus: () => Promise.resolve(buildPayload()),
      submitJournalUnattachedNote
    };

    render(<SetupStatusApp {...props} />);

    expect(await screen.findByRole("heading", { name: "Match Journal Cockpit" })).toBeInTheDocument();
    expect(fetchJournal).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: "Save Journal Note" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Save Opponent Labels" })).toBeDisabled();
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Save Unattached Smoke Note" })).toBeEnabled();
    });

    fireEvent.click(screen.getByRole("button", { name: "Save Unattached Smoke Note" }));

    await waitFor(() => {
      expect(submitJournalUnattachedNote).toHaveBeenCalledTimes(1);
    });
    const request = submitJournalUnattachedNote.mock.calls[0]?.[0] as Record<string, unknown>;
    expect(request).toMatchObject({
      note_scope: "unattached",
      author_label: "codex_smoke_test",
      source_surface: "local_tool",
      privacy_label: "sanitized_fixture",
      note_format: "plain_text",
      priority_label: "normal"
    });
    expect(request).not.toHaveProperty("context");
    expect(String(request.note_text)).toMatch(/^MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW/);

    await waitFor(() => {
      expect(fetchJournalUnattachedNote).toHaveBeenCalledWith({
        journal_note_id: "journal_note:smoke:1",
        note_scope: "unattached"
      });
    });
    expect(await screen.findByRole("heading", { name: "Unattached Smoke Note" })).toBeInTheDocument();
    expect(screen.getAllByText("journal_note:smoke:1").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("unattached").length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText(/MYTHIC_EDGE_SMOKE_TEST|C:\\|script\.google\.com/i)).not.toBeInTheDocument();

    cleanup();
    render(<SetupStatusApp {...props} />);

    await waitFor(() => {
      expect(fetchJournalUnattachedNote).toHaveBeenCalledTimes(2);
    });
    expect(fetchJournalUnattachedNote).toHaveBeenLastCalledWith({
      journal_note_id: "journal_note:smoke:1",
      note_scope: "unattached"
    });
  });

  it("disables Match Journal forms when the backend facade is unavailable", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchJournal={() =>
          Promise.resolve(buildMatchJournalPayload({ status: "unavailable", result: {}, errors: ["service_unavailable"] }))
        }
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByText("Match Journal unavailable")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Save Journal Note" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Save Opponent Labels" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Save Review Flag" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Save Experiment Label" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Propose Display Correction" })).toBeDisabled();
  });

  it("submits allowed Match Journal cockpit updates with parser-owned context only", async () => {
    const submitJournalNote = vi.fn(async () => buildMatchJournalPayload({ result: { service_result: { action: "note" } } }));
    const submitJournalOpponentLabels = vi.fn(async () =>
      buildMatchJournalPayload({ result: { service_result: { action: "opponent" } } })
    );
    const submitJournalReviewFlag = vi.fn(async () =>
      buildMatchJournalPayload({ result: { service_result: { action: "flag" } } })
    );
    const submitJournalExperimentLabel = vi.fn(async () =>
      buildMatchJournalPayload({ result: { service_result: { action: "experiment" } } })
    );
    const submitJournalDisplayCorrection = vi.fn(async () =>
      buildMatchJournalPayload({ result: { service_result: { action: "display" } } })
    );
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchJournal={() => Promise.resolve(buildMatchJournalPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
        submitJournalDisplayCorrection={submitJournalDisplayCorrection}
        submitJournalExperimentLabel={submitJournalExperimentLabel}
        submitJournalNote={submitJournalNote}
        submitJournalOpponentLabels={submitJournalOpponentLabels}
        submitJournalReviewFlag={submitJournalReviewFlag}
      />
    );

    await screen.findByRole("heading", { name: "Match Journal Cockpit" });
    fireEvent.change(screen.getByLabelText("Journal note"), { target: { value: "Synthetic journal note." } });
    fireEvent.click(screen.getByRole("button", { name: "Save Journal Note" }));
    await waitFor(() => {
      expect(submitJournalNote).toHaveBeenCalledWith({
        context: {
          parser_match_id: "match:history:1",
          parser_game_id: "match:history:1:g1",
          game_number: 1
        },
        note_scope: "game",
        note_text: "Synthetic journal note."
      });
    });

    fireEvent.change(screen.getByLabelText("Opponent manual label"), {
      target: { value: "Manual Synthetic Archetype" }
    });
    fireEvent.click(screen.getByRole("button", { name: "Save Opponent Labels" }));
    await waitFor(() => {
      expect(submitJournalOpponentLabels).toHaveBeenCalledWith({
        context: {
          parser_match_id: "match:history:1",
          parser_game_id: "match:history:1:g1",
          game_number: 1
        },
        archetype: "Manual Synthetic Archetype"
      });
    });

    fireEvent.click(screen.getByRole("button", { name: "Save Review Flag" }));
    await waitFor(() => {
      expect(submitJournalReviewFlag).toHaveBeenCalledWith(
        expect.objectContaining({
          context: {
            parser_match_id: "match:history:1",
            parser_game_id: "match:history:1:g1",
            game_number: 1
          },
          flag_type: "needs_review"
        })
      );
    });
    fireEvent.change(screen.getByLabelText("Experiment label"), { target: { value: "ladder-test" } });
    fireEvent.click(screen.getByRole("button", { name: "Save Experiment Label" }));
    await waitFor(() => {
      expect(submitJournalExperimentLabel).toHaveBeenCalledWith(
        expect.objectContaining({
          context: {
            parser_match_id: "match:history:1",
            parser_game_id: "match:history:1:g1",
            game_number: 1
          },
          experiment_label: "ladder-test"
        })
      );
    });
    fireEvent.change(screen.getByLabelText("Display-only field"), { target: { value: "review_summary" } });
    fireEvent.change(screen.getByLabelText("Display-only value"), {
      target: { value: "Synthetic display label." }
    });
    fireEvent.click(screen.getByRole("button", { name: "Propose Display Correction" }));

    await waitFor(() => {
      expect(submitJournalDisplayCorrection).toHaveBeenCalledWith(
        expect.objectContaining({
          context: {
            parser_match_id: "match:history:1",
            parser_game_id: "match:history:1:g1",
            game_number: 1
          },
          effect_scope: "journal_display_only",
          target_surface: "journal_display"
        })
      );
    });
  });

  it("preserves Match Journal form input when sanitized failed submit envelopes resolve", async () => {
    const unavailableJournal = () =>
      buildMatchJournalPayload({ status: "unavailable", result: {}, errors: ["service_unavailable"] });
    const submitJournalNote = vi.fn(async () => unavailableJournal());
    const submitJournalOpponentLabels = vi.fn(async () => unavailableJournal());
    const submitJournalExperimentLabel = vi.fn(async () => unavailableJournal());
    const submitJournalDisplayCorrection = vi.fn(async () => unavailableJournal());
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchJournal={() => Promise.resolve(buildMatchJournalPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
        submitJournalDisplayCorrection={submitJournalDisplayCorrection}
        submitJournalExperimentLabel={submitJournalExperimentLabel}
        submitJournalNote={submitJournalNote}
        submitJournalOpponentLabels={submitJournalOpponentLabels}
      />
    );

    await screen.findByRole("heading", { name: "Match Journal Cockpit" });
    async function enabledFormControl(label: string) {
      const control = screen.getByLabelText(label);
      await waitFor(() => {
        expect(control).toBeEnabled();
      });
      return control;
    }

    async function enabledButton(name: string) {
      const button = screen.getByRole("button", { name });
      await waitFor(() => {
        expect(button).toBeEnabled();
      });
      return button;
    }

    const note = await enabledFormControl("Journal note");
    fireEvent.change(note, { target: { value: "Retry this journal note." } });
    fireEvent.click(await enabledButton("Save Journal Note"));
    await waitFor(() => {
      expect(submitJournalNote).toHaveBeenCalled();
    });
    expect(note).toHaveValue("Retry this journal note.");

    const opponent = await enabledFormControl("Opponent manual label");
    const tier = await enabledFormControl("Opponent tier label");
    fireEvent.change(opponent, { target: { value: "Retry Archetype" } });
    fireEvent.change(tier, { target: { value: "Retry Tier" } });
    fireEvent.click(await enabledButton("Save Opponent Labels"));
    await waitFor(() => {
      expect(submitJournalOpponentLabels).toHaveBeenCalled();
    });
    expect(opponent).toHaveValue("Retry Archetype");
    expect(tier).toHaveValue("Retry Tier");

    const experiment = await enabledFormControl("Experiment label");
    fireEvent.change(experiment, { target: { value: "retry-experiment" } });
    fireEvent.click(await enabledButton("Save Experiment Label"));
    await waitFor(() => {
      expect(submitJournalExperimentLabel).toHaveBeenCalled();
    });
    expect(experiment).toHaveValue("retry-experiment");

    const correctionField = await enabledFormControl("Display-only field");
    const correctionValue = await enabledFormControl("Display-only value");
    fireEvent.change(correctionField, { target: { value: "review_summary" } });
    fireEvent.change(correctionValue, { target: { value: "Retry display label." } });
    fireEvent.click(await enabledButton("Propose Display Correction"));
    await waitFor(() => {
      expect(submitJournalDisplayCorrection).toHaveBeenCalled();
    });
    expect(correctionField).toHaveValue("review_summary");
    expect(correctionValue).toHaveValue("Retry display label.");
    expect(screen.getByRole("heading", { name: "Journal Update Not Saved" })).toBeInTheDocument();
    expect(screen.getByText("service_unavailable")).toBeInTheDocument();
  });

  it("renders Match Journal API errors without raw backend details", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchJournal={() =>
          Promise.reject(new MatchJournalApiError("malformed_response", "Malformed Match Journal response"))
        }
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed Match Journal response" })).toBeInTheDocument();
    expect(screen.queryByText(/stack|error:|select \*|C:\\/i)).not.toBeInTheDocument();
  });

  it("renders read-only opening hand and mulligan history with a refresh control", async () => {
    const fetchOpeningHands = vi.fn(async () => buildOpeningHandHistoryPayload());
    const fetchMulligans = vi.fn(async () => buildMulliganHistoryPayload());
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={fetchMulligans}
        fetchOpeningHands={fetchOpeningHands}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Early Game History" })).toBeInTheDocument();
    expect(screen.getAllByRole("heading", { name: "Opening Hands" }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByRole("heading", { name: "Mulligans" }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("7 cards count 1")).toBeInTheDocument();
    expect(screen.getByText("1: Forest resolved 1001")).toBeInTheDocument();
    expect(screen.getByText("mulliganed_to_six")).toBeInTheDocument();
    expect(screen.getByText("1: bottomed Island direct_grp_id 1002")).toBeInTheDocument();
    expect(screen.queryByText(/best keep|mistake|advice|line tracer|hidden card/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Refresh Early Game" }));

    await waitFor(() => {
      expect(fetchOpeningHands).toHaveBeenCalledTimes(2);
      expect(fetchMulligans).toHaveBeenCalledTimes(2);
    });
  });

  it("renders read-only gameplay action and opponent observation review with a refresh control", async () => {
    const fetchGameplayActions = vi.fn(async () => buildGameplayActionReviewPayload());
    const fetchOpponentObservations = vi.fn(async () => buildOpponentObservationReviewPayload());
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchGameplayActions={fetchGameplayActions}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.resolve(buildOpeningHandHistoryPayload())}
        fetchOpponentObservations={fetchOpponentObservations}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Action Review" })).toBeInTheDocument();
    expect(screen.getAllByRole("heading", { name: "Gameplay Actions" }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByRole("heading", { name: "Opponent Observations" }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("opponent cast hand to stack observed")).toBeInTheDocument();
    expect(screen.getByText("1: Forest direct_grp_id 1001")).toBeInTheDocument();
    expect(screen.getByText("Island public visible missing_expected_evidence review required")).toBeInTheDocument();
    expect(screen.getByText("turn 2 opponent cast hand to stack")).toBeInTheDocument();
    expect(screen.queryByText(/best line|mistake|advice|line tracer|hidden card|archetype/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Refresh Actions" }));

    await waitFor(() => {
      expect(fetchGameplayActions).toHaveBeenCalledTimes(2);
      expect(fetchOpponentObservations).toHaveBeenCalledTimes(2);
    });
  });

  it("renders read-only play-draw and game1-postboard split review with a refresh control", async () => {
    const fetchPlayDrawSplits = vi.fn(async () => buildPlayDrawSplitReviewPayload());
    const fetchGame1PostboardSplits = vi.fn(async () => buildGame1PostboardSplitReviewPayload());
    render(
      <SetupStatusApp
        fetchGame1PostboardSplits={fetchGame1PostboardSplits}
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchGameplayActions={() => Promise.resolve(buildGameplayActionReviewPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.resolve(buildOpeningHandHistoryPayload())}
        fetchOpponentObservations={() => Promise.resolve(buildOpponentObservationReviewPayload())}
        fetchPlayDrawSplits={fetchPlayDrawSplits}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Split Review" })).toBeInTheDocument();
    expect(screen.getAllByRole("heading", { name: "Play/Draw Splits" }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByRole("heading", { name: "Game 1/Postboard Rows" })).toBeInTheDocument();
    expect(await screen.findByText("60 percent")).toBeInTheDocument();
    expect(screen.getByText("small_sample")).toBeInTheDocument();
    expect(screen.getAllByText("match:history:1 game 1").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("900 seconds")).toBeInTheDocument();
    expect(screen.queryByText(/best line|mistake|advice|line tracer|hidden card|archetype|causation/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reset|delete|wipe|cancel|retry|start|stop|git|sheets|ai/i })).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: "Refresh Splits" }));

    await waitFor(() => {
      expect(fetchPlayDrawSplits).toHaveBeenCalledTimes(2);
      expect(fetchGame1PostboardSplits).toHaveBeenCalledTimes(2);
    });
  });

  it("renders empty and degraded history states safely", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve({ ...buildGameHistoryPayload(), status: "degraded", rows: [] })}
        fetchMatches={() => Promise.resolve({ ...buildMatchHistoryPayload(), status: "empty", rows: [] })}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Analytics History" })).toBeInTheDocument();
    expect(screen.getByText("No match rows")).toBeInTheDocument();
    expect(screen.getByText("game history schema not current")).toBeInTheDocument();
  });

  it("renders empty and degraded early-game states safely", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve({ ...buildMulliganHistoryPayload(), status: "degraded", rows: [] })}
        fetchOpeningHands={() => Promise.resolve({ ...buildOpeningHandHistoryPayload(), status: "empty", rows: [] })}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Early Game History" })).toBeInTheDocument();
    expect(screen.getByText("No opening hand rows")).toBeInTheDocument();
    expect(screen.getByText("mulligan history schema not current")).toBeInTheDocument();
  });

  it("renders empty and degraded action review states safely", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchGameplayActions={() => Promise.resolve({ ...buildGameplayActionReviewPayload(), status: "empty", rows: [] })}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.resolve(buildOpeningHandHistoryPayload())}
        fetchOpponentObservations={() =>
          Promise.resolve({ ...buildOpponentObservationReviewPayload(), status: "degraded", rows: [] })
        }
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Action Review" })).toBeInTheDocument();
    expect(screen.getByText("No gameplay action rows")).toBeInTheDocument();
    expect(screen.getByText("opponent observation history schema not current")).toBeInTheDocument();
  });

  it("renders empty and degraded split review states safely", async () => {
    render(
      <SetupStatusApp
        fetchGame1PostboardSplits={() =>
          Promise.resolve({ ...buildGame1PostboardSplitReviewPayload(), status: "degraded", rows: [] })
        }
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchGameplayActions={() => Promise.resolve(buildGameplayActionReviewPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.resolve(buildOpeningHandHistoryPayload())}
        fetchOpponentObservations={() => Promise.resolve(buildOpponentObservationReviewPayload())}
        fetchPlayDrawSplits={() => Promise.resolve({ ...buildPlayDrawSplitReviewPayload(), status: "empty", rows: [] })}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Split Review" })).toBeInTheDocument();
    expect(screen.getByText("No play/draw split rows")).toBeInTheDocument();
    expect(screen.getByText("game 1/postboard split history schema not current")).toBeInTheDocument();
  });

  it("renders malformed history responses without raw backend details", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchMatches={() => Promise.reject(new AnalyticsHistoryApiError("malformed_response", "Malformed history"))}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed history response" })).toBeInTheDocument();
    expect(screen.queryByText(/stack|error:|select \*/i)).not.toBeInTheDocument();
  });

  it("renders malformed early-game history responses without raw backend details", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.reject(new AnalyticsHistoryApiError("malformed_response", "Malformed history"))}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed history response" })).toBeInTheDocument();
    expect(screen.queryByText(`Expected schema: ${EARLY_GAME_HISTORY_SCHEMA_VERSION}`)).not.toBeInTheDocument();
    expect(screen.queryByText(/stack|error:|select \*/i)).not.toBeInTheDocument();
  });

  it("renders malformed action review responses without raw backend details", async () => {
    render(
      <SetupStatusApp
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchGameplayActions={() => Promise.reject(new AnalyticsHistoryApiError("malformed_response", "Malformed history"))}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.resolve(buildOpeningHandHistoryPayload())}
        fetchOpponentObservations={() => Promise.resolve(buildOpponentObservationReviewPayload())}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed history response" })).toBeInTheDocument();
    expect(screen.queryByText(`Expected schema: ${ACTION_REVIEW_SCHEMA_VERSION}`)).not.toBeInTheDocument();
    expect(screen.queryByText(/stack|error:|select \*/i)).not.toBeInTheDocument();
  });

  it("renders malformed split review responses without raw backend details", async () => {
    render(
      <SetupStatusApp
        fetchGame1PostboardSplits={() => Promise.resolve(buildGame1PostboardSplitReviewPayload())}
        fetchGames={() => Promise.resolve(buildGameHistoryPayload())}
        fetchGameplayActions={() => Promise.resolve(buildGameplayActionReviewPayload())}
        fetchMatches={() => Promise.resolve(buildMatchHistoryPayload())}
        fetchMulligans={() => Promise.resolve(buildMulliganHistoryPayload())}
        fetchOpeningHands={() => Promise.resolve(buildOpeningHandHistoryPayload())}
        fetchOpponentObservations={() => Promise.resolve(buildOpponentObservationReviewPayload())}
        fetchPlayDrawSplits={() => Promise.reject(new AnalyticsHistoryApiError("malformed_response", "Malformed history"))}
        fetchStatus={() => Promise.resolve(buildPayload())}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed history response" })).toBeInTheDocument();
    expect(screen.queryByText(`Expected schema: ${SPLIT_REVIEW_SCHEMA_VERSION}`)).not.toBeInTheDocument();
    expect(screen.queryByText(/error:|select \*/i)).not.toBeInTheDocument();
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

  it("uploads folder-selected JSONL files as a flat filtered batch without displaying folder paths", async () => {
    const jsonlFile = withRelativePath(
      new File(['{"kind":"MatchState"}\n'], "a_events.JSONL", { type: "application/jsonl" }),
      "private-day-folder/nested/a_events.JSONL"
    );
    const ignoredFile = withRelativePath(
      new File(["not-jsonl"], "notes.txt", { type: "text/plain" }),
      "private-day-folder/nested/notes.txt"
    );
    const submitUpload = vi.fn(async () => buildUploadedManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitUpload={submitUpload} />);

    const folderInput = (await screen.findByLabelText("Upload JSONL folder")) as HTMLInputElement;
    expect(folderInput).toHaveAttribute("webkitdirectory");

    fireEvent.change(folderInput, { target: { files: [ignoredFile, jsonlFile] } });
    fireEvent.change(screen.getByLabelText("Source label"), { target: { value: "safe_folder_upload" } });

    expect(screen.getByText("1 files selected a_events.JSONL")).toBeInTheDocument();
    expect(screen.getByText("1 non-JSONL file ignored")).toBeInTheDocument();
    expect(screen.queryByText(/private-day-folder|nested|notes\.txt/i)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Upload JSONL Files" }));

    await waitFor(() => {
      expect(submitUpload).toHaveBeenCalledWith({
        files: [jsonlFile],
        source_artifact_label: "safe_folder_upload"
      });
    });
    expect(await screen.findByRole("heading", { name: "Import Job" })).toBeInTheDocument();
    expect(screen.getByText("uploaded_file_batch")).toBeInTheDocument();
    expect(screen.queryByText(/private-day-folder|nested|notes\.txt/i)).not.toBeInTheDocument();
  });

  it("does not start folder upload when selection contains no JSONL files", async () => {
    const ignoredFile = withRelativePath(
      new File(["not-jsonl"], "notes.txt", { type: "text/plain" }),
      "private-day-folder/notes.txt"
    );
    const submitUpload = vi.fn(async () => buildUploadedManualImportJob());
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} submitUpload={submitUpload} />);

    fireEvent.change(await screen.findByLabelText("Upload JSONL folder"), { target: { files: [ignoredFile] } });

    expect(screen.getByText("1 non-JSONL file ignored")).toBeInTheDocument();
    expect(screen.getByText("No JSONL files found in the selected folder.")).toBeInTheDocument();
    expect(screen.queryByText(/private-day-folder|notes\.txt/i)).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Upload JSONL Files" })).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "Upload JSONL Files" }));
    expect(submitUpload).not.toHaveBeenCalled();
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

function withRelativePath(file: File, relativePath: string): File {
  Object.defineProperty(file, "webkitRelativePath", {
    configurable: true,
    value: relativePath
  });
  return file;
}

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
    live_player_log: buildLivePlayerLogStatusPayload(),
    live_watcher: buildLiveWatcherStatusPayload(),
    live_watcher_process: buildLiveWatcherProcessStatusPayload(),
    analytics_database: {
      status: "missing",
      database: { display_path: "<app_data>\\db\\mythic_edge.sqlite3", schema_status: "missing" }
    },
    match_journal: {
      status: "not_initialized",
      database: { display_path: "<app_data>\\db\\match_journal.sqlite3", schema_status: "not_initialized" },
      write_controls: { status: "enabled_on_first_write" }
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
      match_journal_write_controls: "enabled_on_first_write",
      manual_import: "enabled",
      live_watcher: "disabled"
    },
    ...overrides
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
