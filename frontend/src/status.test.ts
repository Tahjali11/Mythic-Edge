import { describe, expect, it } from "vitest";

import { cockpitStatusFromRawStatus, isSafeDisplayValue, safeDisplayValue, statusTone } from "./status";

describe("status helpers", () => {
  it("maps backend status labels to UI tones", () => {
    expect(statusTone("ok")).toBe("ok");
    expect(statusTone("configured_missing")).toBe("missing");
    expect(statusTone("unavailable")).toBe("unavailable");
    expect(statusTone("ready")).toBe("ok");
    expect(statusTone("blocked_missing_log")).toBe("error");
    expect(statusTone("not_configured")).toBe("missing");
    expect(statusTone("not_initialized")).toBe("missing");
    expect(statusTone("stopped")).toBe("deferred");
    expect(statusTone("stale")).toBe("deferred");
    expect(statusTone("blocked")).toBe("error");
    expect(statusTone("invalid_json")).toBe("error");
    expect(statusTone("disabled")).toBe("deferred");
    expect(statusTone("surprise")).toBe("unknown");
  });

  it("allows symbolic display labels and rejects unsafe private-like values", () => {
    expect(isSafeDisplayValue("<app_data>\\db\\mythic_edge.sqlite3")).toBe(true);
    expect(isSafeDisplayValue("<configured_player_log>")).toBe(true);
    expect(isSafeDisplayValue("%LOCALAPPDATA%\\MythicEdgeDev")).toBe(true);
    expect(isSafeDisplayValue("Z:\\synthetic\\unsafe\\Player.log")).toBe(false);
    expect(isSafeDisplayValue("https://example.test/hook")).toBe(false);
  });

  it("returns a redacted placeholder for unsafe display values", () => {
    expect(safeDisplayValue("Z:\\synthetic\\unsafe\\Player.log")).toEqual({
      text: "<redacted_path>",
      redacted: true
    });
  });

  it("translates raw backend statuses into player-facing cockpit labels", () => {
    expect(cockpitStatusFromRawStatus("ok", "app")).toEqual({ label: "Connected", tone: "ok" });
    expect(cockpitStatusFromRawStatus("schema_current", "analytics")).toEqual({ label: "Ready", tone: "ok" });
    expect(cockpitStatusFromRawStatus("empty", "analytics")).toEqual({ label: "Empty history", tone: "empty" });
    expect(cockpitStatusFromRawStatus("not_configured", "player_log")).toEqual({
      label: "Setup needed",
      tone: "missing"
    });
    expect(cockpitStatusFromRawStatus("not_running", "live_capture")).toEqual({
      label: "Waiting for Arena activity",
      tone: "deferred"
    });
    expect(cockpitStatusFromRawStatus("deferred", "trust")).toEqual({ label: "Limited data", tone: "deferred" });
    expect(cockpitStatusFromRawStatus("not_checked", "trust")).toEqual({ label: "Needs review", tone: "unknown" });
    expect(cockpitStatusFromRawStatus("surprise", "trust")).toEqual({ label: "Needs review", tone: "unknown" });
  });
});
