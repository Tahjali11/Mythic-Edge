import type { SetupStatusTone } from "./types";

const SAFE_SYMBOLIC_VALUE_RE = /^<[A-Za-z0-9_.\\-]+>(?:\\[A-Za-z0-9_.-]+)*$/;
const SIMPLE_SAFE_VALUE_RE = /^[A-Za-z0-9_.:()\\ -]+$/;
const ABSOLUTE_WINDOWS_PATH_RE = /^[A-Za-z]:\\/;
const ABSOLUTE_HOME_PATH_RE = /^\/(?:Users|home|tmp|var|private)\//;
const URL_RE = /^[a-z][a-z0-9+.-]*:\/\//i;
const SECRET_MARKER_RE = /(api[_-]?key|secret|token|oauth|webhook)/i;

export function statusTone(status: string): SetupStatusTone {
  const normalized = status.toLowerCase();
  if (
    normalized === "ok" ||
    normalized === "enabled" ||
    normalized === "succeeded" ||
    normalized === "completed" ||
    normalized === "ready" ||
    normalized === "running" ||
    normalized === "schema_current" ||
    normalized.endsWith("_exists") ||
    normalized === "present"
  ) {
    return "ok";
  }
  if (normalized === "degraded") {
    return "degraded";
  }
  if (normalized === "empty") {
    return "empty";
  }
  if (
    normalized === "missing" ||
    normalized.endsWith("_missing") ||
    normalized === "not_configured" ||
    normalized === "not_initialized"
  ) {
    return "missing";
  }
  if (normalized === "unavailable") {
    return "unavailable";
  }
  if (
    normalized === "error" ||
    normalized === "failed" ||
    normalized === "rejected" ||
    normalized.startsWith("invalid_") ||
    normalized === "blocked" ||
    normalized.startsWith("blocked_") ||
    normalized === "crashed" ||
    normalized === "orphaned" ||
    normalized === "unreadable"
  ) {
    return "error";
  }
  if (
    normalized === "deferred" ||
    normalized === "disabled" ||
    normalized === "stopped" ||
    normalized === "stale" ||
    normalized === "separate_reference_surface"
  ) {
    return "deferred";
  }
  return "unknown";
}

export function isSafeDisplayValue(value: unknown): value is string {
  if (typeof value !== "string") {
    return false;
  }

  const trimmed = value.trim();
  if (trimmed.length === 0 || trimmed.length > 160) {
    return false;
  }
  if (trimmed.includes("\n") || trimmed.includes("\r")) {
    return false;
  }
  if (URL_RE.test(trimmed) || SECRET_MARKER_RE.test(trimmed)) {
    return false;
  }
  if (ABSOLUTE_WINDOWS_PATH_RE.test(trimmed) || ABSOLUTE_HOME_PATH_RE.test(trimmed)) {
    return false;
  }
  if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
    return false;
  }
  if (trimmed.includes("Player.log") && !trimmed.startsWith("<")) {
    return false;
  }
  if (SAFE_SYMBOLIC_VALUE_RE.test(trimmed)) {
    return true;
  }
  if (trimmed === "%LOCALAPPDATA%\\MythicEdgeDev") {
    return true;
  }
  return SIMPLE_SAFE_VALUE_RE.test(trimmed);
}

export function safeDisplayValue(value: unknown, fallback = "<redacted_path>"): { text: string; redacted: boolean } {
  if (isSafeDisplayValue(value)) {
    return { text: value, redacted: false };
  }
  return { text: fallback, redacted: true };
}

export type CockpitStatus = {
  label: string;
  tone: SetupStatusTone;
};

export type CockpitStatusContext = "app" | "player_log" | "live_capture" | "analytics" | "journal" | "trust";

export function cockpitStatusFromRawStatus(status: unknown, context: CockpitStatusContext = "trust"): CockpitStatus {
  const normalized = typeof status === "string" ? status.trim().toLowerCase() : "unknown";
  const tone = statusTone(normalized);

  if (context === "app") {
    if (["ok", "enabled", "ready", "running", "present", "completed", "succeeded"].includes(normalized)) {
      return { label: "Connected", tone };
    }
  }

  if (context === "live_capture") {
    if (["capturing", "running"].includes(normalized)) {
      return { label: "Capturing", tone };
    }
    if (["stopped", "not_started", "not_running", "not_capturing"].includes(normalized)) {
      return { label: "Waiting for Arena activity", tone: "deferred" };
    }
  }

  if (["ok", "enabled", "ready", "present", "completed", "succeeded", "schema_current"].includes(normalized)) {
    return { label: "Ready", tone };
  }
  if (normalized === "empty") {
    return { label: "Empty history", tone };
  }
  if (normalized === "running") {
    return { label: "Capturing", tone };
  }
  if (
    normalized === "missing" ||
    normalized.endsWith("_missing") ||
    normalized === "not_configured" ||
    normalized === "not_initialized"
  ) {
    return { label: "Setup needed", tone };
  }
  if (["blocked", "failed", "error", "unreadable", "crashed", "rejected"].includes(normalized)) {
    return { label: "Blocked", tone };
  }
  if (["stale", "degraded"].includes(normalized)) {
    return { label: "Needs review", tone: normalized === "degraded" ? "degraded" : "deferred" };
  }
  if (
    ["deferred", "disabled", "state_only", "readiness_only", "safeguards_only", "separate_reference_surface"].includes(
      normalized
    )
  ) {
    return { label: "Limited data", tone: "deferred" };
  }
  if (["stopped", "not_started", "not_running", "not_capturing"].includes(normalized)) {
    return { label: "Stopped", tone: "deferred" };
  }
  if (["unavailable"].includes(normalized)) {
    return { label: "Unavailable", tone };
  }
  return { label: "Needs review", tone: "unknown" };
}
