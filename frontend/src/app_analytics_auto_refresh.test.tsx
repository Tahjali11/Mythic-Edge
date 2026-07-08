import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  ANALYTICS_AUTO_REFRESH_INTERVAL_MS,
  AnalyticsAutoRefreshNotice,
  type AutoRefreshActiveCheck,
  useAnalyticsAutoRefreshState
} from "./app_analytics_auto_refresh";
import {
  ANALYTICS_REFRESH_STATE_OBJECT,
  ANALYTICS_REFRESH_STATE_SCHEMA_VERSION,
  type AnalyticsRefreshStateResponse
} from "./types";

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.restoreAllMocks();
});

describe("analytics auto-refresh helper", () => {
  it("checks immediately and preserves the 25-second interval for unchanged revisions", async () => {
    vi.useFakeTimers();
    const fetchAnalyticsRefreshState = vi
      .fn()
      .mockResolvedValueOnce(buildAnalyticsRefreshStatePayload({ analytics_revision: "analytics-refresh-v1:baseline" }))
      .mockResolvedValueOnce(buildAnalyticsRefreshStatePayload({ analytics_revision: "analytics-refresh-v1:baseline" }));
    const refreshAnalyticsViews = vi.fn(async () => undefined);

    render(
      <AutoRefreshHarness
        fetchAnalyticsRefreshState={fetchAnalyticsRefreshState}
        refreshAnalyticsViews={refreshAnalyticsViews}
      />
    );

    await flushAsyncUpdates();

    expect(screen.getByLabelText("Analytics auto-refresh")).toHaveTextContent("Analytics checked");
    expect(fetchAnalyticsRefreshState).toHaveBeenCalledTimes(1);
    expect(refreshAnalyticsViews).not.toHaveBeenCalled();

    await act(async () => {
      vi.advanceTimersByTime(ANALYTICS_AUTO_REFRESH_INTERVAL_MS);
    });
    await flushAsyncUpdates();

    expect(fetchAnalyticsRefreshState).toHaveBeenCalledTimes(2);
    expect(refreshAnalyticsViews).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Analytics auto-refresh")).toHaveTextContent("Analytics checked");
  });

  it("refreshes analytics views once after a changed safe revision", async () => {
    vi.useFakeTimers();
    const activeChecks: boolean[] = [];
    const fetchAnalyticsRefreshState = vi
      .fn()
      .mockResolvedValueOnce(buildAnalyticsRefreshStatePayload({ analytics_revision: "analytics-refresh-v1:baseline" }))
      .mockResolvedValueOnce(buildAnalyticsRefreshStatePayload({ analytics_revision: "analytics-refresh-v1:changed" }));
    const refreshAnalyticsViews = vi.fn(async (isAutoRefreshActive: AutoRefreshActiveCheck) => {
      activeChecks.push(isAutoRefreshActive());
    });

    render(
      <AutoRefreshHarness
        fetchAnalyticsRefreshState={fetchAnalyticsRefreshState}
        refreshAnalyticsViews={refreshAnalyticsViews}
      />
    );

    await flushAsyncUpdates();

    await act(async () => {
      vi.advanceTimersByTime(ANALYTICS_AUTO_REFRESH_INTERVAL_MS);
    });
    await flushAsyncUpdates();

    expect(fetchAnalyticsRefreshState).toHaveBeenCalledTimes(2);
    expect(refreshAnalyticsViews).toHaveBeenCalledTimes(1);
    expect(activeChecks).toEqual([true]);
    expect(screen.getByLabelText("Analytics auto-refresh")).toHaveTextContent("Analytics updated");
  });

  it("pauses while hidden and checks immediately when visible again", async () => {
    vi.useFakeTimers();
    const visibilityState = vi.spyOn(document, "visibilityState", "get");
    visibilityState.mockReturnValue("hidden");
    const fetchAnalyticsRefreshState = vi
      .fn()
      .mockResolvedValue(buildAnalyticsRefreshStatePayload({ analytics_revision: "analytics-refresh-v1:baseline" }));
    const refreshAnalyticsViews = vi.fn(async () => undefined);

    render(
      <AutoRefreshHarness
        fetchAnalyticsRefreshState={fetchAnalyticsRefreshState}
        refreshAnalyticsViews={refreshAnalyticsViews}
      />
    );

    await flushAsyncUpdates();

    expect(screen.getByLabelText("Analytics auto-refresh")).toHaveTextContent(
      "Auto-refresh is paused while this tab is hidden."
    );
    expect(fetchAnalyticsRefreshState).not.toHaveBeenCalled();

    visibilityState.mockReturnValue("visible");
    await act(async () => {
      document.dispatchEvent(new Event("visibilitychange"));
    });
    await flushAsyncUpdates();

    expect(fetchAnalyticsRefreshState).toHaveBeenCalledTimes(1);
    expect(refreshAnalyticsViews).not.toHaveBeenCalled();
    expect(screen.getByLabelText("Analytics auto-refresh")).toHaveTextContent("Analytics checked");
  });
});

function AutoRefreshHarness({
  analyticsViewLoading = false,
  fetchAnalyticsRefreshState,
  refreshAnalyticsViews
}: {
  analyticsViewLoading?: boolean;
  fetchAnalyticsRefreshState: () => Promise<AnalyticsRefreshStateResponse>;
  refreshAnalyticsViews: (isAutoRefreshActive: AutoRefreshActiveCheck) => Promise<void>;
}) {
  const state = useAnalyticsAutoRefreshState({
    analyticsViewLoading,
    fetchAnalyticsRefreshState,
    refreshAnalyticsViews
  });
  return <AnalyticsAutoRefreshNotice state={state} />;
}

async function flushAsyncUpdates() {
  await act(async () => {
    await Promise.resolve();
    await Promise.resolve();
    await Promise.resolve();
  });
}

function buildAnalyticsRefreshStatePayload(
  overrides: Partial<AnalyticsRefreshStateResponse> = {}
): AnalyticsRefreshStateResponse {
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
    errors: [],
    ...overrides
  };
}
