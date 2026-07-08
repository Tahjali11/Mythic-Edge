import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  CoachBoundaryPanel,
  DashboardRouteCards,
  DashboardTrustPrivacySignal,
  PrivacyDetailsPanel,
  TrustPrivacyLayer,
  type StaticPanelInsight
} from "./app_static_panels";

const TRUST_ITEMS: StaticPanelInsight[] = [
  {
    title: "Freshness",
    status: "ok",
    tone: "ok",
    detail: "All public-safe views are fresh."
  },
  {
    title: "Data Quality",
    status: "degraded",
    tone: "degraded",
    detail: "One public-safe view is stale."
  },
  {
    title: "Privacy",
    status: "unknown",
    tone: "unknown",
    detail: "Unsafe display values stay redacted."
  }
];

afterEach(() => {
  cleanup();
});

describe("app static display panels", () => {
  it("preserves the coach boundary panel copy and status", () => {
    render(<CoachBoundaryPanel />);

    const section = screen.getByRole("region", { name: "Review Context Only" });
    expect(section).toHaveClass("coachBoundary");
    expect(within(section).getByText("Coach")).toHaveClass("eyebrow");
    expect(within(section).getByLabelText("status Not connected")).toHaveClass(
      "statusPill",
      "tone-deferred"
    );
    expect(
      within(section).getByText(
        "This shell can organize local review context, but it does not run model suggestions, line ranking, or error scoring."
      )
    ).toBeInTheDocument();
  });

  it("preserves full trust and privacy layer status cards", () => {
    render(<TrustPrivacyLayer items={TRUST_ITEMS} />);

    const section = screen.getByRole("region", { name: "Trust and Freshness" });
    expect(section).toHaveClass("trustLayer");
    expect(within(section).getByText("Trust and privacy")).toHaveClass("eyebrow");
    for (const item of TRUST_ITEMS) {
      const article = within(section).getByRole("heading", { name: item.title }).closest("article");
      expect(article).toHaveClass("trustItem", `tone-${item.tone}`);
      expect(within(article as HTMLElement).getByLabelText(`status ${item.status}`)).toHaveClass(
        "statusPill",
        `tone-${item.tone}`
      );
      expect(within(section).getByText(item.detail)).toBeInTheDocument();
    }
  });

  it("preserves compact dashboard trust and privacy signals", () => {
    render(<DashboardTrustPrivacySignal items={TRUST_ITEMS} />);

    const section = screen.getByRole("region", { name: "Trust and Freshness" });
    expect(section).toHaveClass("dashboardTrustSignal");
    expect(
      within(section).getByText("Compact safe-display signals only. Full details stay in Privacy and technical diagnostics.")
    ).toBeInTheDocument();
    const grid = within(section).getByLabelText("Compact trust and privacy statuses");
    for (const item of TRUST_ITEMS) {
      expect(within(grid).getByText(item.title)).toBeInTheDocument();
      expect(within(grid).getByLabelText(`status ${item.status}`)).toHaveClass(
        "statusPill",
        `tone-${item.tone}`
      );
    }
  });

  it("preserves dashboard route card labels, details, and hash hrefs", () => {
    render(<DashboardRouteCards />);

    const section = screen.getByRole("region", { name: "Go Deeper" });
    expect(section).toHaveClass("routeCardSection");
    expect(_routeCard("Analytics")).toHaveAttribute("href", "#analytics");
    expect(_routeCard("Review")).toHaveAttribute("href", "#review");
    expect(_routeCard("Feedback")).toHaveAttribute("href", "#feedback");
    expect(_routeCard("Import")).toHaveAttribute("href", "#import");
    expect(_routeCard("Diagnostics")).toHaveAttribute("href", "#diagnostics");
    expect(
      within(section).getByText("Open deeper read-only match, game, split, mulligan, and observation views.")
    ).toBeInTheDocument();
    expect(
      within(section).getByText("Open Match Journal context and human annotation tools without changing parser truth.")
    ).toBeInTheDocument();
    expect(
      within(section).getByText("Prepare a sanitized copy-first report. External issue submission remains deferred.")
    ).toBeInTheDocument();
    expect(
      within(section).getByText("Open manual JSONL import workflows without putting file forms on the dashboard.")
    ).toBeInTheDocument();
    expect(
      within(section).getByText("Inspect technical setup and live diagnostics only when you need the owner view.")
    ).toBeInTheDocument();
  });

  it("preserves privacy details panel headings and local-only boundary copy", () => {
    render(<PrivacyDetailsPanel />);

    const section = screen.getByRole("region", { name: "Local-Only Boundaries" });
    expect(section).toHaveClass("privacyDetails");
    expect(within(section).getByText("Privacy details")).toHaveClass("eyebrow");
    expect(within(section).getByRole("heading", { name: "Raw logs stay out of the UI" })).toBeInTheDocument();
    expect(within(section).getByRole("heading", { name: "Generated data stays local" })).toBeInTheDocument();
    expect(within(section).getByRole("heading", { name: "External systems are deferred" })).toBeInTheDocument();
    expect(
      within(section).getByText(
        "Player.log content, raw JSONL payloads, private paths, hashes, and local artifact contents are not displayed."
      )
    ).toBeInTheDocument();
    expect(
      within(section).getByText(
        "SQLite files and runtime app data are local support artifacts, not parser truth and not committed frontend state."
      )
    ).toBeInTheDocument();
    expect(
      within(section).getByText(
        "GitHub submission, Sheets transport, OpenAI runtime calls, and AI coaching stay inactive unless separately contracted."
      )
    ).toBeInTheDocument();
  });
});

function _routeCard(name: string) {
  return screen.getByRole("link", { name: new RegExp(`^${name}`) });
}
