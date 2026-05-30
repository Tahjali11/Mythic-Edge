import type { SetupStatusTone } from "./types";

const SAFE_SYMBOLIC_VALUE_RE = /^<[A-Za-z0-9_.\\-]+>(?:\\[A-Za-z0-9_.-]+)*$/;
const SIMPLE_SAFE_VALUE_RE = /^[A-Za-z0-9_.:()\\ -]+$/;
const ABSOLUTE_WINDOWS_PATH_RE = /^[A-Za-z]:\\/;
const ABSOLUTE_HOME_PATH_RE = /^\/(?:Users|home|tmp|var|private)\//;
const URL_RE = /^[a-z][a-z0-9+.-]*:\/\//i;
const SECRET_MARKER_RE = /(api[_-]?key|secret|token|oauth|webhook)/i;

export function statusTone(status: string): SetupStatusTone {
  const normalized = status.toLowerCase();
  if (normalized === "ok" || normalized.endsWith("_exists") || normalized === "present") {
    return "ok";
  }
  if (normalized === "degraded") {
    return "degraded";
  }
  if (normalized === "missing" || normalized.endsWith("_missing")) {
    return "missing";
  }
  if (normalized === "unavailable") {
    return "unavailable";
  }
  if (normalized === "error" || normalized.startsWith("invalid_") || normalized === "unreadable") {
    return "error";
  }
  if (normalized === "deferred" || normalized === "disabled" || normalized === "separate_reference_surface") {
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
