import { useEffect, useRef, useState } from "react";

import type { AnalyticsRefreshStateResponse, SetupStatusTone } from "./types";

export type AnalyticsAutoRefreshState =
  | { state: "checking"; checkedAt: string | null }
  | { state: "up_to_date"; checkedAt: string | null }
  | { state: "updated"; checkedAt: string }
  | { state: "paused"; checkedAt: string | null }
  | { state: "degraded"; checkedAt: string | null; message: string };

export type AutoRefreshActiveCheck = () => boolean;

export const ANALYTICS_AUTO_REFRESH_INTERVAL_MS = 25_000;

export function useAnalyticsAutoRefreshState({
  analyticsViewLoading,
  fetchAnalyticsRefreshState,
  refreshAnalyticsViews
}: {
  analyticsViewLoading: boolean;
  fetchAnalyticsRefreshState: () => Promise<AnalyticsRefreshStateResponse>;
  refreshAnalyticsViews: (isAutoRefreshActive: AutoRefreshActiveCheck) => Promise<void>;
}): AnalyticsAutoRefreshState {
  const [analyticsAutoRefreshState, setAnalyticsAutoRefreshState] = useState<AnalyticsAutoRefreshState>({
    state: "checking",
    checkedAt: null
  });
  const analyticsRefreshRevisionRef = useRef<string | null>(null);
  const analyticsAutoRefreshInFlightRef = useRef(false);
  const analyticsViewLoadingRef = useRef(analyticsViewLoading);
  analyticsViewLoadingRef.current = analyticsViewLoading;

  useEffect(() => {
    let active = true;

    async function checkAnalyticsRefreshState() {
      if (!active || analyticsAutoRefreshInFlightRef.current) {
        return;
      }
      if (document.visibilityState === "hidden") {
        setAnalyticsAutoRefreshState((current) => ({ state: "paused", checkedAt: current.checkedAt }));
        return;
      }

      analyticsAutoRefreshInFlightRef.current = true;
      setAnalyticsAutoRefreshState((current) => ({ state: "checking", checkedAt: current.checkedAt }));
      try {
        const payload = await fetchAnalyticsRefreshState();
        if (!active) {
          return;
        }

        const checkedAt = formatAutoRefreshCheckedAt(new Date());
        const nextRevision = payload.analytics_revision;
        const previousRevision = analyticsRefreshRevisionRef.current;
        const safeToRefresh = payload.status === "ok" || payload.status === "empty";

        if (!safeToRefresh) {
          if (nextRevision !== null) {
            analyticsRefreshRevisionRef.current = nextRevision;
          }
          setAnalyticsAutoRefreshState({
            state: "degraded",
            checkedAt,
            message: "Auto-refresh is degraded; manual refresh remains available."
          });
          return;
        }

        if (nextRevision !== null && previousRevision !== null && nextRevision !== previousRevision) {
          if (analyticsViewLoadingRef.current) {
            setAnalyticsAutoRefreshState({ state: "checking", checkedAt });
            return;
          }
          analyticsRefreshRevisionRef.current = nextRevision;
          await refreshAnalyticsViews(() => active);
          if (!active) {
            return;
          }
          setAnalyticsAutoRefreshState({ state: "updated", checkedAt });
          return;
        }

        if (nextRevision !== null) {
          analyticsRefreshRevisionRef.current = nextRevision;
        }
        setAnalyticsAutoRefreshState({ state: "up_to_date", checkedAt });
      } catch {
        if (!active) {
          return;
        }
        setAnalyticsAutoRefreshState((current) => ({
          state: "degraded",
          checkedAt: current.checkedAt,
          message: "Auto-refresh check is unavailable; manual refresh remains available."
        }));
      } finally {
        analyticsAutoRefreshInFlightRef.current = false;
      }
    }

    function handleVisibilityChange() {
      if (document.visibilityState === "visible") {
        void checkAnalyticsRefreshState();
        return;
      }
      setAnalyticsAutoRefreshState((current) => ({ state: "paused", checkedAt: current.checkedAt }));
    }

    void checkAnalyticsRefreshState();
    const intervalId = window.setInterval(() => {
      void checkAnalyticsRefreshState();
    }, ANALYTICS_AUTO_REFRESH_INTERVAL_MS);
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      active = false;
      window.clearInterval(intervalId);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [fetchAnalyticsRefreshState, refreshAnalyticsViews]);

  return analyticsAutoRefreshState;
}

export function analyticsAutoRefreshNoticeContent(state: AnalyticsAutoRefreshState): {
  title: string;
  detail: string;
  tone: SetupStatusTone;
} {
  if (state.state === "updated") {
    return {
      title: "Analytics auto-refresh",
      detail: `Analytics updated ${state.checkedAt}.`,
      tone: "ok"
    };
  }
  if (state.state === "paused") {
    return {
      title: "Analytics auto-refresh",
      detail: "Auto-refresh is paused while this tab is hidden.",
      tone: "deferred"
    };
  }
  if (state.state === "degraded") {
    return {
      title: "Analytics auto-refresh",
      detail: state.message,
      tone: "degraded"
    };
  }
  if (state.state === "checking") {
    return {
      title: "Analytics auto-refresh",
      detail: state.checkedAt === null ? "Checking for safe analytics updates." : "Checking for safe analytics updates.",
      tone: "unknown"
    };
  }
  return {
    title: "Analytics auto-refresh",
    detail: state.checkedAt === null ? "Waiting for analytics refresh state." : `Analytics checked ${state.checkedAt}.`,
    tone: "ok"
  };
}

export function formatAutoRefreshCheckedAt(date: Date): string {
  return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

export function AnalyticsAutoRefreshNotice({ state }: { state: AnalyticsAutoRefreshState }) {
  const content = analyticsAutoRefreshNoticeContent(state);
  return (
    <section className={`autoRefreshNotice tone-${content.tone}`} aria-live="polite" aria-label="Analytics auto-refresh">
      <span>{content.title}</span>
      <p>{content.detail}</p>
    </section>
  );
}
