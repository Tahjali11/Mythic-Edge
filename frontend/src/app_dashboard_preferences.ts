import type { AnalyticsDashboardModule, AnalyticsDashboardModuleView } from "./types";

export const DASHBOARD_MODULE_VIEW_PREFERENCES_KEY = "mythic_edge.analytics.dashboard.module_view_preferences.v1";

const DASHBOARD_MODULE_IDS = new Set<string>([
  "play_draw_win_rate",
  "game1_postboard",
  "mulligan_opening_hand_outcomes"
]);
const DASHBOARD_MODULE_VIEWS = new Set<string>(["bar", "table"]);

export function readDashboardModuleViewPreferences(): Record<string, AnalyticsDashboardModuleView> {
  if (typeof window === "undefined") {
    return {};
  }
  try {
    const raw = window.localStorage.getItem(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY);
    if (!raw) {
      return {};
    }
    const parsed: unknown = JSON.parse(raw);
    if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
      return {};
    }
    const preferences: Record<string, AnalyticsDashboardModuleView> = {};
    for (const [moduleId, view] of Object.entries(parsed)) {
      if (DASHBOARD_MODULE_IDS.has(moduleId) && typeof view === "string" && DASHBOARD_MODULE_VIEWS.has(view)) {
        preferences[moduleId] = view as AnalyticsDashboardModuleView;
      }
    }
    return preferences;
  } catch {
    return {};
  }
}

export function writeDashboardModuleViewPreferences(preferences: Record<string, AnalyticsDashboardModuleView>) {
  if (typeof window === "undefined") {
    return;
  }
  try {
    const safePreferences: Record<string, AnalyticsDashboardModuleView> = {};
    for (const [moduleId, view] of Object.entries(preferences)) {
      if (DASHBOARD_MODULE_IDS.has(moduleId) && DASHBOARD_MODULE_VIEWS.has(view)) {
        safePreferences[moduleId] = view;
      }
    }
    window.localStorage.setItem(DASHBOARD_MODULE_VIEW_PREFERENCES_KEY, JSON.stringify(safePreferences));
  } catch {
    // Browser storage is a preference surface only; rendering should continue without it.
  }
}

export function selectedDashboardModuleView(
  module: Pick<AnalyticsDashboardModule, "allowed_views" | "default_view" | "module_id">,
  preferences: Record<string, AnalyticsDashboardModuleView>
): AnalyticsDashboardModuleView {
  const preferred = preferences[module.module_id];
  if (preferred && module.allowed_views.includes(preferred)) {
    return preferred;
  }
  return module.allowed_views.includes(module.default_view) ? module.default_view : module.allowed_views[0] ?? "table";
}
