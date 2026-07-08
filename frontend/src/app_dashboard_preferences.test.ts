import { afterEach, describe, expect, it, vi } from "vitest";

import {
  DASHBOARD_MODULE_VIEW_PREFERENCES_KEY,
  readDashboardModuleViewPreferences,
  selectedDashboardModuleView,
  writeDashboardModuleViewPreferences
} from "./app_dashboard_preferences";
import type { AnalyticsDashboardModule, AnalyticsDashboardModuleView } from "./types";

afterEach(() => {
  vi.restoreAllMocks();
  window.localStorage.clear();
});

describe("app dashboard module preferences", () => {
  it("preserves the dashboard module preference storage key", () => {
    expect(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY).toBe(
      "mythic_edge.analytics.dashboard.module_view_preferences.v1"
    );
  });

  it("reads only supported module ids and supported view values", () => {
    window.localStorage.setItem(
      DASHBOARD_MODULE_VIEW_PREFERENCES_KEY,
      JSON.stringify({
        play_draw_win_rate: "bar",
        game1_postboard: "table",
        mulligan_opening_hand_outcomes: "grid",
        unknown_module: "table",
        "C:\\secret\\Player.log": "bar"
      })
    );

    expect(readDashboardModuleViewPreferences()).toEqual({
      play_draw_win_rate: "bar",
      game1_postboard: "table"
    });
  });

  it("falls back to empty preferences for missing, malformed, and non-object storage", () => {
    expect(readDashboardModuleViewPreferences()).toEqual({});

    window.localStorage.setItem(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY, "{");
    expect(readDashboardModuleViewPreferences()).toEqual({});

    window.localStorage.setItem(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY, JSON.stringify(["bar"]));
    expect(readDashboardModuleViewPreferences()).toEqual({});

    window.localStorage.setItem(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY, JSON.stringify(null));
    expect(readDashboardModuleViewPreferences()).toEqual({});
  });

  it("writes only supported module ids and supported view values", () => {
    writeDashboardModuleViewPreferences({
      play_draw_win_rate: "table",
      game1_postboard: "bar",
      mulligan_opening_hand_outcomes: "grid" as AnalyticsDashboardModuleView,
      unknown_module: "table"
    });

    expect(JSON.parse(window.localStorage.getItem(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY) ?? "{}")).toEqual({
      play_draw_win_rate: "table",
      game1_postboard: "bar"
    });
  });

  it("does not throw when browser storage access fails", () => {
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("storage unavailable");
    });
    expect(readDashboardModuleViewPreferences()).toEqual({});

    vi.restoreAllMocks();
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("storage unavailable");
    });
    expect(() => writeDashboardModuleViewPreferences({ play_draw_win_rate: "table" })).not.toThrow();
  });

  it("selects preferred, default, first allowed, then table fallback views without changing vocabulary", () => {
    expect(
      selectedDashboardModuleView(moduleForViewSelection({ allowed_views: ["bar", "table"], default_view: "bar" }), {
        play_draw_win_rate: "table"
      })
    ).toBe("table");

    expect(
      selectedDashboardModuleView(moduleForViewSelection({ allowed_views: ["bar", "table"], default_view: "bar" }), {})
    ).toBe("bar");

    expect(
      selectedDashboardModuleView(
        moduleForViewSelection({ allowed_views: ["table"], default_view: "bar" }),
        { play_draw_win_rate: "bar" }
      )
    ).toBe("table");

    expect(
      selectedDashboardModuleView(moduleForViewSelection({ allowed_views: [], default_view: "bar" }), {
        play_draw_win_rate: "bar"
      })
    ).toBe("table");
  });
});

function moduleForViewSelection({
  allowed_views,
  default_view
}: {
  allowed_views: AnalyticsDashboardModuleView[];
  default_view: AnalyticsDashboardModuleView;
}): Pick<AnalyticsDashboardModule, "allowed_views" | "default_view" | "module_id"> {
  return {
    allowed_views,
    default_view,
    module_id: "play_draw_win_rate"
  };
}
