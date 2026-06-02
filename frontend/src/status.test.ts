import { describe, expect, it } from "vitest";

import { isSafeDisplayValue, safeDisplayValue, statusTone } from "./status";

describe("status helpers", () => {
  it("maps backend status labels to UI tones", () => {
    expect(statusTone("ok")).toBe("ok");
    expect(statusTone("configured_missing")).toBe("missing");
    expect(statusTone("unavailable")).toBe("unavailable");
    expect(statusTone("ready")).toBe("ok");
    expect(statusTone("blocked_missing_log")).toBe("error");
    expect(statusTone("not_configured")).toBe("missing");
    expect(statusTone("stopped")).toBe("deferred");
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
});
