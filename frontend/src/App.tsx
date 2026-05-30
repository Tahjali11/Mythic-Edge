import { useEffect, useState, type ReactNode } from "react";

import "./App.css";
import { fetchSetupStatus, SetupStatusApiError } from "./api";
import { safeDisplayValue, statusTone } from "./status";
import { SETUP_STATUS_SCHEMA_VERSION, type SectionStatus, type SetupStatusResponse } from "./types";

type LoadState =
  | { state: "loading" }
  | { state: "ready"; payload: SetupStatusResponse; unsafeCount: number }
  | { state: "error"; code: SetupStatusApiError["code"]; message: string };

type SetupStatusAppProps = {
  fetchStatus?: () => Promise<SetupStatusResponse>;
};

type Panel = {
  title: string;
  status: string;
  details: Array<{ label: string; value: unknown }>;
};

export function SetupStatusApp({ fetchStatus = fetchSetupStatus }: SetupStatusAppProps) {
  const [loadState, setLoadState] = useState<LoadState>({ state: "loading" });

  useEffect(() => {
    let active = true;
    setLoadState({ state: "loading" });

    fetchStatus()
      .then((payload) => {
        if (!active) {
          return;
        }
        const unsafeCount = countUnsafeValues(payload);
        setLoadState({ state: "ready", payload, unsafeCount });
      })
      .catch((error: unknown) => {
        if (!active) {
          return;
        }
        if (error instanceof SetupStatusApiError) {
          setLoadState({ state: "error", code: error.code, message: error.message });
          return;
        }
        setLoadState({
          state: "error",
          code: "backend_unavailable",
          message: "Backend setup status is unavailable."
        });
      });

    return () => {
      active = false;
    };
  }, [fetchStatus]);

  if (loadState.state === "loading") {
    return (
      <Shell>
        <StatusNotice title="Checking local app setup" status="unknown" />
      </Shell>
    );
  }

  if (loadState.state === "error") {
    return (
      <Shell>
        <StatusNotice title={errorTitle(loadState.code)} status={errorTone(loadState.code)}>
          {loadState.code === "incompatible_response" ? (
            <span>Expected schema: {SETUP_STATUS_SCHEMA_VERSION}</span>
          ) : (
            <span>{loadState.message}</span>
          )}
        </StatusNotice>
      </Shell>
    );
  }

  const panels = buildPanels(loadState.payload);
  const overallTone = loadState.unsafeCount > 0 ? "degraded" : statusTone(loadState.payload.status);

  return (
    <Shell>
      <section className="summaryBand" aria-labelledby="overall-status">
        <div>
          <p className="eyebrow">Mythic Edge Local App</p>
          <h1 id="overall-status">Setup Status</h1>
        </div>
        <StatusPill label={loadState.unsafeCount > 0 ? "degraded" : loadState.payload.status} tone={overallTone} />
      </section>

      {loadState.unsafeCount > 0 ? (
        <StatusNotice title="Unsafe display value redacted" status="degraded">
          <span>{loadState.unsafeCount} value was replaced with &lt;redacted_path&gt;.</span>
        </StatusNotice>
      ) : null}

      <section className="panelGrid" aria-label="Setup status sections">
        <StatusPanel
          title="Backend Reachability"
          status="ok"
          details={[{ label: "aggregate endpoint", value: "/api/app/setup-status" }]}
        />
        {panels.map((panel) => (
          <StatusPanel key={panel.title} {...panel} />
        ))}
      </section>

      <section className="panelGrid futureGrid" aria-label="Deferred local app sections">
        <StatusPanel title="Manual Import" status="deferred" details={[{ label: "state", value: "deferred" }]} />
        <StatusPanel title="Analytics Views" status="deferred" details={[{ label: "state", value: "deferred" }]} />
        <StatusPanel title="Live Watcher" status="deferred" details={[{ label: "state", value: "deferred" }]} />
      </section>
    </Shell>
  );
}

export default SetupStatusApp;

function Shell({ children }: { children: ReactNode }) {
  return (
    <main className="appShell">
      <div className="content">{children}</div>
    </main>
  );
}

function StatusNotice({ title, status, children }: { title: string; status: string; children?: ReactNode }) {
  return (
    <section className={`notice tone-${statusTone(status)}`} aria-labelledby="status-notice">
      <div>
        <h1 id="status-notice">{title}</h1>
        {children ? <p>{children}</p> : null}
      </div>
      <StatusPill label={status} tone={statusTone(status)} />
    </section>
  );
}

function StatusPanel({ title, status, details }: Panel) {
  const tone = statusTone(status);
  return (
    <article className={`statusPanel tone-${tone}`}>
      <div className="panelHeader">
        <h2>{title}</h2>
        <StatusPill label={status} tone={tone} />
      </div>
      <dl>
        {details.map((detail) => {
          const safe = safeDisplayValue(detail.value);
          return (
            <div className={safe.redacted ? "redactedRow" : undefined} key={`${detail.label}-${String(detail.value)}`}>
              <dt>{detail.label}</dt>
              <dd>{safe.text}</dd>
            </div>
          );
        })}
      </dl>
    </article>
  );
}

function StatusPill({ label, tone }: { label: string; tone: string }) {
  return (
    <span className={`statusPill tone-${tone}`} aria-label={`status ${label}`}>
      <span aria-hidden="true" />
      {label}
    </span>
  );
}

function buildPanels(payload: SetupStatusResponse): Panel[] {
  return [
    {
      title: "App Data",
      status: statusFromSection(payload.paths),
      details: [
        { label: "root", value: nestedValue(payload.paths, ["app_data_root", "display_path"]) },
        { label: "policy", value: payload.paths.redaction_policy }
      ]
    },
    {
      title: "Local Config",
      status: statusFromSection(payload.config),
      details: [
        { label: "file", value: nestedValue(payload.config, ["config_file", "display_path"]) },
        { label: "state", value: nestedValue(payload.config, ["config_file", "status"]) }
      ]
    },
    {
      title: "Player Log",
      status: statusFromSection(payload.player_log),
      details: [
        { label: "path", value: nestedValue(payload.player_log, ["player_log", "display_path"]) },
        { label: "state", value: nestedValue(payload.player_log, ["player_log", "status"]) }
      ]
    },
    {
      title: "Analytics Database",
      status: statusFromSection(payload.analytics_database),
      details: [
        { label: "path", value: nestedValue(payload.analytics_database, ["database", "display_path"]) },
        { label: "schema", value: nestedValue(payload.analytics_database, ["database", "schema_status"]) }
      ]
    },
    {
      title: "Migrations",
      status: statusFromSection(payload.migrations),
      details: [
        { label: "loader", value: payload.migrations.migration_status },
        { label: "available", value: migrationCount(payload.migrations) }
      ]
    },
    {
      title: "Runtime",
      status: statusFromSection(payload.runtime),
      details: [
        { label: "backend", value: nestedValue(payload.runtime, ["backend", "status"]) },
        { label: "parser runner", value: nestedValue(payload.runtime, ["parser_runner", "status"]) },
        { label: "live watcher", value: nestedValue(payload.runtime, ["live_watcher", "status"]) }
      ]
    }
  ];
}

function statusFromSection(section: SectionStatus): string {
  return typeof section.status === "string" ? section.status : "unknown";
}

function nestedValue(root: SectionStatus, path: string[]): unknown {
  let current: unknown = root;
  for (const key of path) {
    if (!isRecord(current)) {
      return "unknown";
    }
    current = current[key];
  }
  return current ?? "unknown";
}

function migrationCount(section: SectionStatus): string {
  const migrations = section.migrations;
  if (!Array.isArray(migrations)) {
    return "0";
  }
  return String(migrations.length);
}

function countUnsafeValues(payload: SetupStatusResponse): number {
  return buildPanels(payload).reduce((count, panel) => {
    return count + panel.details.filter((detail) => safeDisplayValue(detail.value).redacted).length;
  }, 0);
}

function errorTitle(code: SetupStatusApiError["code"]): string {
  if (code === "malformed_response") {
    return "Malformed setup response";
  }
  if (code === "incompatible_response") {
    return "Incompatible setup schema";
  }
  if (code === "unsafe_api_base_url") {
    return "Unsafe API base URL";
  }
  return "Backend unavailable";
}

function errorTone(code: SetupStatusApiError["code"]): string {
  return code === "unsafe_api_base_url" || code === "incompatible_response" ? "error" : "unavailable";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
