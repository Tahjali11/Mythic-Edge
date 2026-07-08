import { appRouteHref, type AppRoute } from "./app_navigation";
import type { SetupStatusTone } from "./types";

export type StaticPanelInsight = {
  title: string;
  status: string;
  tone: SetupStatusTone;
  detail: string;
};

type RouteCard = {
  route: AppRoute;
  title: string;
  detail: string;
};

const DASHBOARD_ROUTE_CARDS: readonly RouteCard[] = [
  {
    route: "analytics",
    title: "Analytics",
    detail: "Open deeper read-only match, game, split, mulligan, and observation views."
  },
  {
    route: "review",
    title: "Review",
    detail: "Open Match Journal context and human annotation tools without changing parser truth."
  },
  {
    route: "feedback",
    title: "Feedback",
    detail: "Prepare a sanitized copy-first report. External issue submission remains deferred."
  },
  {
    route: "import",
    title: "Import",
    detail: "Open manual JSONL import workflows without putting file forms on the dashboard."
  },
  {
    route: "diagnostics",
    title: "Diagnostics",
    detail: "Inspect technical setup and live diagnostics only when you need the owner view."
  }
] as const;

export function CoachBoundaryPanel() {
  return (
    <section className="coachBoundary" id="coach" aria-labelledby="coach-boundary-title">
      <div className="panelHeader">
        <div>
          <p className="eyebrow">Coach</p>
          <h2 id="coach-boundary-title">Review Context Only</h2>
        </div>
        <StaticPanelStatusPill label="Not connected" tone="deferred" />
      </div>
      <p>
        This shell can organize local review context, but it does not run model suggestions, line ranking, or error scoring.
      </p>
    </section>
  );
}

export function TrustPrivacyLayer({ items }: { items: StaticPanelInsight[] }) {
  return (
    <section className="trustLayer" id="privacy" aria-labelledby="trust-layer-title">
      <div className="sectionHeading">
        <p className="eyebrow">Trust and privacy</p>
        <h2 id="trust-layer-title">Trust and Freshness</h2>
      </div>
      <div className="trustGrid">
        {items.map((item) => (
          <article className={`trustItem tone-${item.tone}`} key={item.title}>
            <div className="panelHeader">
              <h3>{item.title}</h3>
              <StaticPanelStatusPill label={item.status} tone={item.tone} />
            </div>
            <p>{item.detail}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

export function DashboardTrustPrivacySignal({ items }: { items: StaticPanelInsight[] }) {
  return (
    <section className="dashboardTrustSignal" aria-labelledby="dashboard-trust-title">
      <div>
        <p className="eyebrow">Trust and privacy</p>
        <h2 id="dashboard-trust-title">Trust and Freshness</h2>
        <p>Compact safe-display signals only. Full details stay in Privacy and technical diagnostics.</p>
      </div>
      <div className="dashboardTrustSignalGrid" aria-label="Compact trust and privacy statuses">
        {items.map((item) => (
          <div className="dashboardTrustSignalItem" key={item.title}>
            <span>{item.title}</span>
            <StaticPanelStatusPill label={item.status} tone={item.tone} />
          </div>
        ))}
      </div>
    </section>
  );
}

export function DashboardRouteCards() {
  return (
    <section className="routeCardSection" aria-labelledby="route-card-title">
      <div className="sectionHeading">
        <p className="eyebrow">Modes</p>
        <h2 id="route-card-title">Go Deeper</h2>
      </div>
      <div className="routeCardGrid">
        {DASHBOARD_ROUTE_CARDS.map((card) => (
          <a className="routeCard" href={appRouteHref(card.route)} key={card.route}>
            <span>{card.title}</span>
            <p>{card.detail}</p>
          </a>
        ))}
      </div>
    </section>
  );
}

export function PrivacyDetailsPanel() {
  return (
    <section className="privacyDetails" aria-labelledby="privacy-details-title">
      <div className="sectionHeading">
        <p className="eyebrow">Privacy details</p>
        <h2 id="privacy-details-title">Local-Only Boundaries</h2>
      </div>
      <div className="trustGrid">
        <article className="trustItem">
          <h3>Raw logs stay out of the UI</h3>
          <p>Player.log content, raw JSONL payloads, private paths, hashes, and local artifact contents are not displayed.</p>
        </article>
        <article className="trustItem">
          <h3>Generated data stays local</h3>
          <p>SQLite files and runtime app data are local support artifacts, not parser truth and not committed frontend state.</p>
        </article>
        <article className="trustItem">
          <h3>External systems are deferred</h3>
          <p>GitHub submission, Sheets transport, OpenAI runtime calls, and AI coaching stay inactive unless separately contracted.</p>
        </article>
      </div>
    </section>
  );
}

function StaticPanelStatusPill({ label, tone }: { label: string; tone: string }) {
  return (
    <span className={`statusPill tone-${tone}`} aria-label={`status ${label}`}>
      <span aria-hidden="true" />
      {label}
    </span>
  );
}
