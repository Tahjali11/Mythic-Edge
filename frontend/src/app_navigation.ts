export type AppRoute = "dashboard" | "coach" | "analytics" | "review" | "privacy" | "feedback" | "import" | "diagnostics";

export type RailItem = {
  route: AppRoute;
  label: string;
};

export const APP_ROUTES: readonly AppRoute[] = [
  "dashboard",
  "coach",
  "analytics",
  "review",
  "privacy",
  "feedback",
  "import",
  "diagnostics"
];

export const RAIL_ITEMS: readonly RailItem[] = [
  { route: "dashboard", label: "Dashboard" },
  { route: "coach", label: "Coach" },
  { route: "analytics", label: "Analytics" },
  { route: "review", label: "Review" },
  { route: "feedback", label: "Feedback" },
  { route: "import", label: "Import" },
  { route: "diagnostics", label: "Diagnostics" },
  { route: "privacy", label: "Privacy" }
];

export const LEFT_RAIL_COPY = {
  asideAriaLabel: "Local app sections",
  kicker: "Mythic Edge",
  title: "Local App",
  navigationAriaLabel: "Primary sections",
  footerAriaLabel: "Local app footer",
  footerLabel: "Settings",
  footerValue: "Not configured"
} as const;

export function appRouteHref(route: AppRoute): `#${AppRoute}` {
  return `#${route}`;
}

export function readAppRouteFromHash(hash = window.location.hash): AppRoute {
  const rawRoute = hash.replace(/^#\/?/, "").trim().toLowerCase();
  return isAppRoute(rawRoute) ? rawRoute : "dashboard";
}

export function isAppRoute(value: string): value is AppRoute {
  return APP_ROUTES.includes(value as AppRoute);
}
