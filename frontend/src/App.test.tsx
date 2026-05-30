import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SetupStatusApiError } from "./api";
import { SetupStatusApp } from "./App";
import { SETUP_STATUS_OBJECT, SETUP_STATUS_SCHEMA_VERSION, type SetupStatusResponse } from "./types";

describe("SetupStatusApp", () => {
  it("renders safe setup-status panels from a degraded backend payload", async () => {
    render(<SetupStatusApp fetchStatus={() => Promise.resolve(buildPayload())} />);

    expect(screen.getByText("Checking local app setup")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Setup Status" })).toBeInTheDocument();

    expect(screen.getByText("Backend Reachability")).toBeInTheDocument();
    expect(screen.getByText("<app_data>")).toBeInTheDocument();
    expect(screen.getByText("<configured_player_log>")).toBeInTheDocument();
    expect(screen.getByText("<app_data>\\db\\mythic_edge.sqlite3")).toBeInTheDocument();
    expect(screen.queryAllByRole("button")).toHaveLength(0);
    expect(screen.queryByLabelText(/reset|delete|import|start|stop/i)).not.toBeInTheDocument();
  });

  it("renders a backend-unavailable state without stack traces", async () => {
    render(
      <SetupStatusApp
        fetchStatus={() => Promise.reject(new SetupStatusApiError("backend_unavailable", "Backend unavailable"))}
      />
    );

    expect(await screen.findByRole("heading", { name: "Backend unavailable" })).toBeInTheDocument();
    expect(screen.queryByText(/synthetic network failure|stack|error:/i)).not.toBeInTheDocument();
  });

  it("renders malformed and incompatible response states safely", async () => {
    const { rerender } = render(
      <SetupStatusApp
        fetchStatus={() => Promise.reject(new SetupStatusApiError("malformed_response", "Malformed setup response"))}
      />
    );

    expect(await screen.findByRole("heading", { name: "Malformed setup response" })).toBeInTheDocument();

    rerender(
      <SetupStatusApp
        fetchStatus={() =>
          Promise.reject(
            new SetupStatusApiError(
              "incompatible_response",
              `Expected setup status schema ${SETUP_STATUS_SCHEMA_VERSION}.`
            )
          )
        }
      />
    );

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Incompatible setup schema" })).toBeInTheDocument();
    });
    expect(screen.getByText(`Expected schema: ${SETUP_STATUS_SCHEMA_VERSION}`)).toBeInTheDocument();
  });

  it("redacts unsafe path-like values from backend display fields", async () => {
    const payload = buildPayload({
      paths: {
        status: "degraded",
        app_data_root: { display_path: "Z:\\synthetic\\unsafe\\Player.log" },
        redaction_policy: "symbolic_app_data_paths_only"
      }
    });

    render(<SetupStatusApp fetchStatus={() => Promise.resolve(payload)} />);

    expect(await screen.findByText("<redacted_path>")).toBeInTheDocument();
    expect(screen.queryByText("Z:\\synthetic\\unsafe\\Player.log")).not.toBeInTheDocument();
    expect(screen.getByText("Unsafe display value redacted")).toBeInTheDocument();
  });
});

function buildPayload(overrides: Partial<SetupStatusResponse> = {}): SetupStatusResponse {
  return {
    object: SETUP_STATUS_OBJECT,
    schema_version: SETUP_STATUS_SCHEMA_VERSION,
    status: "degraded",
    paths: {
      status: "degraded",
      app_data_root: { display_path: "<app_data>" },
      redaction_policy: "symbolic_app_data_paths_only"
    },
    config: {
      status: "missing",
      config_file: { display_path: "<app_data>\\config\\app_config.json", status: "missing" }
    },
    player_log: {
      status: "missing",
      player_log: { display_path: "<configured_player_log>", status: "configured_missing" }
    },
    analytics_database: {
      status: "missing",
      database: { display_path: "<app_data>\\db\\mythic_edge.sqlite3", schema_status: "missing" }
    },
    migrations: {
      status: "ok",
      migration_status: "available",
      migrations: [{ migration_id: "001_initial", checksum_present: true }]
    },
    runtime: {
      status: "ok",
      backend: { status: "running" },
      parser_runner: { status: "deferred" },
      live_watcher: { status: "deferred" }
    },
    capabilities: {
      setup_status: "enabled",
      manual_import: "disabled",
      live_watcher: "disabled"
    },
    ...overrides
  };
}
