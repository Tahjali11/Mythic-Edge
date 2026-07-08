import { describe, expect, it } from "vitest";

import {
  appRouteHref,
  APP_ROUTES,
  isAppRoute,
  LEFT_RAIL_COPY,
  RAIL_ITEMS,
  readAppRouteFromHash
} from "./app_navigation";

describe("app navigation metadata", () => {
  it("preserves the route vocabulary and rail item order", () => {
    expect(APP_ROUTES).toEqual([
      "dashboard",
      "coach",
      "analytics",
      "review",
      "privacy",
      "feedback",
      "import",
      "diagnostics"
    ]);
    expect(RAIL_ITEMS).toEqual([
      { route: "dashboard", label: "Dashboard" },
      { route: "coach", label: "Coach" },
      { route: "analytics", label: "Analytics" },
      { route: "review", label: "Review" },
      { route: "feedback", label: "Feedback" },
      { route: "import", label: "Import" },
      { route: "diagnostics", label: "Diagnostics" },
      { route: "privacy", label: "Privacy" }
    ]);
  });

  it("preserves static rail copy and aria labels", () => {
    expect(LEFT_RAIL_COPY).toEqual({
      asideAriaLabel: "Local app sections",
      kicker: "Mythic Edge",
      title: "Local App",
      navigationAriaLabel: "Primary sections",
      footerAriaLabel: "Local app footer",
      footerLabel: "Settings",
      footerValue: "Not configured"
    });
  });

  it("normalizes supported hash routes without changing unknown-route fallback", () => {
    expect(readAppRouteFromHash("#analytics")).toBe("analytics");
    expect(readAppRouteFromHash("#/review")).toBe("review");
    expect(readAppRouteFromHash("#  IMPORT  ")).toBe("import");
    expect(readAppRouteFromHash("#unknown-section")).toBe("dashboard");
    expect(readAppRouteFromHash("")).toBe("dashboard");
  });

  it("keeps route membership and href generation symbolic", () => {
    expect(isAppRoute("diagnostics")).toBe(true);
    expect(isAppRoute("unknown-section")).toBe(false);
    expect(appRouteHref("diagnostics")).toBe("#diagnostics");
    expect(appRouteHref("dashboard")).toBe("#dashboard");
  });
});
