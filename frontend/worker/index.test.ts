// @vitest-environment node

import { describe, expect, it, vi } from "vitest";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import {
  copySitesHostingMetadata,
  validateSitesHostingMetadata
} from "../build/sites-vite-plugin";
import worker, { type SitesPreviewEnv } from "./index";

const API_UNAVAILABLE_BODY = JSON.stringify({
  schema_version: "sites_preview_api_unavailable.v1",
  object: "mythic_edge_sites_preview_api_unavailable",
  status: "unavailable",
  reason: "local_backend_required"
});

function makeEnv(fetchImpl = vi.fn(async () => new Response("asset"))): SitesPreviewEnv {
  return {
    ASSETS: {
      fetch: fetchImpl
    }
  };
}

describe("Sites preview Worker routing", () => {
  it.each([
    ["GET", "/api"],
    ["GET", "/api/analytics/matches"],
    ["POST", "/api/imports/jsonl"],
    ["OPTIONS", "/api/live/capture/start"]
  ])("returns the exact unavailable contract for %s %s", async (method, path) => {
    const assetsFetch = vi.fn(async () => new Response("asset"));
    const response = await worker.fetch(
      new Request(`https://preview.invalid${path}`, { method }),
      makeEnv(assetsFetch)
    );

    expect(response.status).toBe(503);
    expect(response.headers.get("content-type")).toBe("application/json; charset=utf-8");
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(response.headers.get("x-content-type-options")).toBe("nosniff");
    expect(response.headers.has("access-control-allow-origin")).toBe(false);
    expect(await response.text()).toBe(API_UNAVAILABLE_BODY);
    expect(assetsFetch).not.toHaveBeenCalled();
  });

  it("returns the API status and headers without a body for HEAD", async () => {
    const assetsFetch = vi.fn(async () => new Response("asset"));
    const response = await worker.fetch(
      new Request("https://preview.invalid/api/status", { method: "HEAD" }),
      makeEnv(assetsFetch)
    );

    expect(response.status).toBe(503);
    expect(response.headers.get("content-type")).toBe("application/json; charset=utf-8");
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(response.headers.get("x-content-type-options")).toBe("nosniff");
    expect(await response.text()).toBe("");
    expect(assetsFetch).not.toHaveBeenCalled();
  });

  it("delegates non-API requests to the assets binding with the original request", async () => {
    const assetResponse = new Response("spa", { status: 200 });
    const assetsFetch = vi.fn(async () => assetResponse);
    const request = new Request("https://preview.invalid/apiary?view=navigation");

    const response = await worker.fetch(request, makeEnv(assetsFetch));

    expect(response).toBe(assetResponse);
    expect(assetsFetch).toHaveBeenCalledOnce();
    expect(assetsFetch).toHaveBeenCalledWith(request);
  });

  it("delegates static asset requests to the assets binding with the original request", async () => {
    const assetResponse = new Response("asset", { status: 200 });
    const assetsFetch = vi.fn(async () => assetResponse);
    const request = new Request("https://preview.invalid/assets/app.js");

    const response = await worker.fetch(request, makeEnv(assetsFetch));

    expect(response).toBe(assetResponse);
    expect(assetsFetch).toHaveBeenCalledOnce();
    expect(assetsFetch).toHaveBeenCalledWith(request);
  });

  it("sanitizes an absent assets binding", async () => {
    const response = await worker.fetch(
      new Request("https://preview.invalid/dashboard?private=query"),
      {} as SitesPreviewEnv
    );
    const body = await response.text();

    expect(response.status).toBe(503);
    expect(JSON.parse(body)).toEqual({
      schema_version: "sites_preview_api_unavailable.v1",
      object: "mythic_edge_sites_preview_api_unavailable",
      status: "unavailable",
      reason: "preview_assets_unavailable"
    });
    expect(body).not.toContain("dashboard");
    expect(body).not.toContain("private");
  });

  it("sanitizes assets binding failures without exception echo", async () => {
    const privateMarker = "private-local-marker";
    const assetsFetch = vi.fn(async () => {
      throw new Error(privateMarker);
    });

    const response = await worker.fetch(
      new Request("https://preview.invalid/settings", {
        headers: { "x-private-marker": privateMarker }
      }),
      makeEnv(assetsFetch)
    );
    const body = await response.text();

    expect(response.status).toBe(503);
    expect(body).toContain('"reason":"preview_assets_unavailable"');
    expect(body).not.toContain(privateMarker);
  });

  it("is deterministic and does not echo API input", async () => {
    const privateMarker = "private-request-marker";
    const requestFactory = () =>
      new Request(`https://preview.invalid/api/report?value=${privateMarker}`, {
        method: "POST",
        headers: { "x-private-marker": privateMarker },
        body: privateMarker
      });
    const env = makeEnv();

    const first = await worker.fetch(requestFactory(), env);
    const second = await worker.fetch(requestFactory(), env);
    const firstBody = await first.text();
    const secondBody = await second.text();

    expect(firstBody).toBe(API_UNAVAILABLE_BODY);
    expect(secondBody).toBe(firstBody);
    expect(firstBody).not.toContain(privateMarker);
  });
});

describe("Sites hosting metadata", () => {
  const validMetadata = new TextEncoder().encode('{\n  "d1": null,\n  "r2": null\n}\n');

  it("accepts only the exact null resource-key shape", () => {
    expect(() => validateSitesHostingMetadata(validMetadata)).not.toThrow();

    for (const invalid of [
      "not-json",
      "{}",
      '{"d1":null,"r2":null,"project_id":"forbidden"}',
      '{"d1":"binding","r2":null}',
      '{"d1":null,"r2":{}}'
    ]) {
      expect(() => validateSitesHostingMetadata(new TextEncoder().encode(invalid))).toThrowError(
        "sites_hosting_metadata_invalid"
      );
    }
  });

  it("copies source bytes exactly and replaces only generated metadata", async () => {
    const frontendRoot = await mkdtemp(join(tmpdir(), "mythic-edge-sites-metadata-"));

    try {
      await mkdir(join(frontendRoot, ".openai"), { recursive: true });
      await mkdir(join(frontendRoot, "dist", ".openai"), { recursive: true });
      await writeFile(join(frontendRoot, ".openai", "hosting.json"), validMetadata);
      await writeFile(join(frontendRoot, "dist", ".openai", "stale.json"), "stale");

      await copySitesHostingMetadata(frontendRoot);

      expect(await readFile(join(frontendRoot, "dist", ".openai", "hosting.json"))).toEqual(
        Buffer.from(validMetadata)
      );
      await expect(readFile(join(frontendRoot, "dist", ".openai", "stale.json"))).rejects.toThrow();
    } finally {
      await rm(frontendRoot, { force: true, recursive: true });
    }
  });

  it("fails closed when source metadata is missing", async () => {
    const frontendRoot = await mkdtemp(join(tmpdir(), "mythic-edge-sites-metadata-"));

    try {
      await expect(copySitesHostingMetadata(frontendRoot)).rejects.toThrowError(
        "sites_hosting_metadata_missing"
      );
    } finally {
      await rm(frontendRoot, { force: true, recursive: true });
    }
  });
});
