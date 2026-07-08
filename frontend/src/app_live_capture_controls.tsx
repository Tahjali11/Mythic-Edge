import type { ReactNode } from "react";

import type { LiveCaptureStatusResponse, SetupStatusTone } from "./types";
import type { LiveStatusApiError } from "./api";

export type LiveCaptureControlState =
  | { state: "loading" }
  | { state: "ready"; payload: LiveCaptureStatusResponse; message?: string }
  | { state: "submitting"; payload: LiveCaptureStatusResponse | null; action: "start" | "stop" }
  | { state: "error"; code: LiveStatusApiError["code"]; message: string; payload?: LiveCaptureStatusResponse | null };

type DashboardLiveCaptureAction =
  | { kind: "start"; label: "Start capture"; disabled: false }
  | { kind: "stop"; label: "Stop capture"; disabled: false }
  | { kind: "pending"; label: "Starting capture" | "Stopping capture"; disabled: true }
  | { kind: "blocked"; label: string; ariaLabel: string; disabled: true };

type LiveCaptureStatusPill = (props: { label: string; pulse?: boolean; tone: SetupStatusTone }) => ReactNode;

export function DashboardLiveCaptureControl({
  state,
  onStartCapture,
  onStopCapture
}: {
  state: LiveCaptureControlState;
  onStartCapture: () => void;
  onStopCapture: () => void;
}) {
  const action = dashboardLiveCaptureAction(state);
  return (
    <div className="dashboardCaptureControl" aria-label="Live capture lifecycle control">
      <div className="dashboardCaptureActionSlot">
        {action.kind === "start" ? (
          <button className="captureLifecycleButton" onClick={onStartCapture} type="button">
            {action.label}
          </button>
        ) : null}
        {action.kind === "stop" ? (
          <button className="captureLifecycleButton isStopping" onClick={onStopCapture} type="button">
            {action.label}
          </button>
        ) : null}
        {action.kind === "pending" ? (
          <button aria-label={action.label} className="captureLifecycleButton isPending" disabled type="button">
            {action.label === "Starting capture" ? "Starting" : "Stopping"}
          </button>
        ) : null}
        {action.kind === "blocked" ? (
          <button aria-label={action.ariaLabel} className="captureLifecycleButton isPending" disabled type="button">
            {action.label}
          </button>
        ) : null}
      </div>
      <a
        className="captureDiagnosticsLink"
        href="#diagnostics"
        aria-label="View live capture diagnostics"
        title="View live capture diagnostics"
      >
        <span aria-hidden="true">i</span>
      </a>
    </div>
  );
}

export function LiveCaptureControlPanel({
  state,
  onStartCapture,
  onStopCapture,
  StatusPillComponent
}: {
  state: LiveCaptureControlState;
  onStartCapture: () => void;
  onStopCapture: () => void;
  StatusPillComponent: LiveCaptureStatusPill;
}) {
  const payload = liveCaptureControlPayload(state);
  const statusLabel = payload ? liveCaptureStatusLabel(payload.status) : state.state === "loading" ? "Checking" : "Unavailable";
  const tone = payload ? liveCaptureTone(payload.status) : state.state === "error" ? "error" : "unknown";
  const startAllowed = liveCaptureStartAllowed(state);
  const stopAllowed = state.state !== "submitting" && Boolean(payload?.capture.stop_allowed);
  const message =
    state.state === "error"
      ? state.message
      : state.state === "submitting"
        ? state.action === "start"
          ? "Starting capture from the local app."
          : "Stopping the app-owned capture supervisor."
        : state.state === "ready" && state.message
          ? state.message
          : liveCaptureBlurbText(payload) ?? liveCaptureControlDetail(payload);
  return (
    <section className="captureControlPanel" aria-labelledby="live-capture-control-title">
      <div>
        <p className="eyebrow">Explicit local control</p>
        <h2 id="live-capture-control-title">Live Capture Control</h2>
        <p>{message}</p>
      </div>
      <div className="captureControlActions">
        <StatusPillComponent label={statusLabel} pulse={payload?.status === "capturing"} tone={tone} />
        {startAllowed ? (
          <button onClick={onStartCapture} type="button">
            Start capture
          </button>
        ) : null}
        {stopAllowed ? (
          <button onClick={onStopCapture} type="button">
            Stop capture
          </button>
        ) : null}
      </div>
    </section>
  );
}

export function liveCaptureStartAllowed(state: LiveCaptureControlState): boolean {
  const payload = liveCaptureControlPayload(state);
  return state.state !== "submitting" && Boolean(payload?.capture.start_allowed);
}

function dashboardLiveCaptureAction(state: LiveCaptureControlState): DashboardLiveCaptureAction {
  if (state.state === "submitting") {
    return {
      kind: "pending",
      label: state.action === "start" ? "Starting capture" : "Stopping capture",
      disabled: true
    };
  }
  if (state.state === "loading") {
    return { kind: "blocked", label: "Checking", ariaLabel: "Checking live capture status", disabled: true };
  }

  const payload = liveCaptureControlPayload(state);
  if (payload === null || state.state === "error") {
    return { kind: "blocked", label: "Unavailable", ariaLabel: "Live capture unavailable", disabled: true };
  }
  if (liveCaptureDashboardBlocked(payload)) {
    return dashboardLiveCaptureBlockedAction(payload);
  }
  if (payload.status === "capturing" && payload.capture.running && payload.capture.stop_allowed) {
    return { kind: "stop", label: "Stop capture", disabled: false };
  }
  if ((payload.status === "ready_to_start" || payload.status === "stopped") && !payload.capture.running && payload.capture.start_allowed) {
    return { kind: "start", label: "Start capture", disabled: false };
  }
  if (payload.status === "starting") {
    return { kind: "pending", label: "Starting capture", disabled: true };
  }
  if (payload.status === "stopping") {
    return { kind: "pending", label: "Stopping capture", disabled: true };
  }
  return dashboardLiveCaptureBlockedAction(payload);
}

function dashboardLiveCaptureBlockedAction(payload: LiveCaptureStatusResponse): DashboardLiveCaptureAction {
  if (payload.status === "unavailable") {
    return { kind: "blocked", label: "Unavailable", ariaLabel: "Live capture unavailable", disabled: true };
  }
  if (payload.status === "starting") {
    return { kind: "pending", label: "Starting capture", disabled: true };
  }
  if (payload.status === "stopping") {
    return { kind: "pending", label: "Stopping capture", disabled: true };
  }
  return { kind: "blocked", label: "Needs review", ariaLabel: "Live capture needs review", disabled: true };
}

function liveCaptureDashboardBlocked(payload: LiveCaptureStatusResponse): boolean {
  if (payload.status === "capturing" && !payload.capture.running) {
    return true;
  }
  if ((payload.status === "ready_to_start" || payload.status === "stopped") && payload.capture.running) {
    return true;
  }
  if (payload.state.stale) {
    return true;
  }
  return ["blocked", "failed", "crashed", "stale", "degraded", "unknown", "unavailable"].includes(payload.status);
}

export function liveCaptureDashboardStatus(payload: LiveCaptureStatusResponse): {
  label: string;
  tone: SetupStatusTone;
  liveActive: boolean;
} {
  if (!liveCaptureDashboardBlocked(payload)) {
    return {
      label: liveCaptureStatusLabel(payload.status),
      tone: liveCaptureTone(payload.status),
      liveActive: payload.status === "capturing" && payload.capture.running
    };
  }
  if (payload.status === "blocked") {
    return { label: "Blocked", tone: "error", liveActive: false };
  }
  if (payload.status === "failed" || payload.status === "crashed") {
    return { label: "Failed", tone: "error", liveActive: false };
  }
  if (payload.status === "unavailable") {
    return { label: "Unavailable", tone: "unavailable", liveActive: false };
  }
  return { label: "Needs review", tone: "unknown", liveActive: false };
}

export function liveCaptureDashboardDetail(payload: LiveCaptureStatusResponse): string {
  if (payload.status === "stale" || payload.state.stale || payload.capture.reason === "capture_state_stale") {
    return "Capture state is stale; open diagnostics.";
  }
  if (liveCaptureDashboardBlocked(payload)) {
    return liveCaptureControlDetail(payload);
  }
  return liveCaptureBlurbText(payload) ?? liveCaptureControlDetail(payload);
}

export function liveCaptureControlPayload(state: LiveCaptureControlState): LiveCaptureStatusResponse | null {
  if (state.state === "ready" || state.state === "submitting") {
    return state.payload;
  }
  if (state.state === "error") {
    return state.payload ?? null;
  }
  return null;
}

function liveCaptureStatusLabel(status: string): string {
  if (status === "ready_to_start") {
    return "Ready to start";
  }
  if (status === "capturing") {
    return "Capturing";
  }
  if (status === "starting") {
    return "Starting";
  }
  if (status === "stopping") {
    return "Stopping";
  }
  if (status === "stopped") {
    return "Stopped";
  }
  if (status === "blocked") {
    return "Blocked";
  }
  if (status === "failed" || status === "crashed") {
    return "Failed";
  }
  if (status === "stale") {
    return "Needs review";
  }
  if (status === "degraded") {
    return "Limited data";
  }
  if (status === "unavailable") {
    return "Unavailable";
  }
  return "Needs review";
}

function liveCaptureTone(status: string): SetupStatusTone {
  if (status === "capturing") {
    return "ok";
  }
  if (status === "ready_to_start" || status === "starting" || status === "stopping" || status === "stopped") {
    return "deferred";
  }
  if (status === "blocked" || status === "failed" || status === "crashed") {
    return "error";
  }
  if (status === "stale" || status === "degraded") {
    return "degraded";
  }
  if (status === "unavailable") {
    return "unavailable";
  }
  return "unknown";
}

function liveCaptureControlDetail(payload: LiveCaptureStatusResponse | null): string {
  if (payload === null) {
    return "Live capture control status is loading.";
  }
  if (payload.status === "capturing") {
    return "Parser, Player.log tailing, and SQLite writes are active for the app-owned supervisor.";
  }
  if (payload.status === "ready_to_start") {
    return "Player.log is configured, but live capture is not running. Start capture to add completed games to SQLite.";
  }
  if (payload.status === "starting") {
    return "Capture start was accepted; waiting for the app-owned supervisor to report active tailing.";
  }
  if (payload.status === "stopped") {
    return "Live capture is stopped. Start capture before testing a new game if you want it added to analytics.";
  }
  if (payload.status === "stopping") {
    return "The app-owned capture supervisor is stopping.";
  }
  if (payload.status === "blocked") {
    return "Live capture is blocked by a safe precondition; inspect diagnostics before starting.";
  }
  if (payload.status === "stale") {
    return "Capture state is stale or ownership is ambiguous; review before starting or stopping.";
  }
  if (payload.status === "failed" || payload.status === "crashed") {
    return "Live capture failed without exposing private log content.";
  }
  return "Live capture status is incomplete or unavailable; inspect setup and diagnostics.";
}

function liveCaptureBlurbText(payload: LiveCaptureStatusResponse | null): string | null {
  const text = payload?.parser_status_blurb?.text?.trim();
  return text || null;
}

export function liveCaptureControlMessage(status: string): string {
  if (status === "capturing") {
    return "Capture is active.";
  }
  if (status === "starting") {
    return "Capture start accepted.";
  }
  if (status === "already_running") {
    return "Capture was already running; no duplicate supervisor was started.";
  }
  if (status === "stopped") {
    return "Capture stopped.";
  }
  if (status === "not_running") {
    return "Capture was not running.";
  }
  if (status === "blocked") {
    return "Capture request was blocked by a safe precondition.";
  }
  if (status === "failed") {
    return "Capture request failed without exposing private log content.";
  }
  return "Capture status updated.";
}

const LIVE_CAPTURE_RECORDED_MATCH_DETAIL = "Most recent completed match was recorded.";

export function compactLiveCaptureDetail(label: string, detail?: string): string {
  const safeDetail = detail?.trim();
  if (safeDetail === LIVE_CAPTURE_RECORDED_MATCH_DETAIL) {
    return safeDetail;
  }
  if (label === "Capturing") {
    return "Capture active.";
  }
  if (label === "Ready to start" || label === "Stopped") {
    return "Capture is not running.";
  }
  if (label === "Blocked") {
    return "Capture blocked.";
  }
  if (label === "Setup needed") {
    return "Setup needed.";
  }
  if (label === "Needs review" && detail) {
    return detail;
  }
  if (label === "Unavailable") {
    return "Status unavailable.";
  }
  return `${label}.`;
}
