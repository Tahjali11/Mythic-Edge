import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";
import test from "node:test";

const frontendRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = resolve(frontendRoot, "..");
const distRoot = resolve(frontendRoot, "dist");
const sourceMetadataPath = resolve(frontendRoot, ".openai", "hosting.json");
const builtMetadataPath = resolve(distRoot, ".openai", "hosting.json");
const serverEntryPath = resolve(distRoot, "server", "index.js");
const clientEntryPath = resolve(distRoot, "client", "index.html");

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

async function listFiles(root) {
  const files = [];

  async function visit(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = resolve(directory, entry.name);
      if (entry.isDirectory()) {
        await visit(path);
      } else if (entry.isFile()) {
        files.push(path);
      }
    }
  }

  await visit(root);
  return files;
}

function collectObjectKeys(value, keys = new Set()) {
  if (Array.isArray(value)) {
    for (const item of value) {
      collectObjectKeys(item, keys);
    }
    return keys;
  }
  if (value && typeof value === "object") {
    for (const [key, child] of Object.entries(value)) {
      keys.add(key.toLowerCase());
      collectObjectKeys(child, keys);
    }
  }
  return keys;
}

function assertDeepEmpty(value, label) {
  if (Array.isArray(value)) {
    assert.equal(value.length, 0, `${label} must not configure bindings`);
    return;
  }
  if (value && typeof value === "object") {
    for (const child of Object.values(value)) {
      assertDeepEmpty(child, label);
    }
    return;
  }
  assert.equal(value, undefined, `${label} must not configure a value`);
}

test("source and built hosting metadata are exact and byte-identical", async () => {
  const sourceBytes = await readFile(sourceMetadataPath);
  const builtBytes = await readFile(builtMetadataPath);
  const sourceValue = JSON.parse(sourceBytes.toString("utf8"));

  assert.deepEqual(Object.keys(sourceValue).sort(), ["d1", "r2"]);
  assert.equal(sourceValue.d1, null);
  assert.equal(sourceValue.r2, null);
  assert.deepEqual(builtBytes, sourceBytes);
  assert.equal(sha256(builtBytes), sha256(sourceBytes));
  await assert.rejects(access(resolve(distRoot, ".openai", "drizzle")));
});

test("Sites build emits the required client, asset, and server entries", async () => {
  await access(clientEntryPath);
  await access(serverEntryPath);

  const assetFiles = await listFiles(resolve(distRoot, "client", "assets"));
  assert.ok(assetFiles.length > 0, "client assets must not be empty");
});

test("built Worker preserves the exact API-unavailable boundary", async () => {
  const workerModule = await import(`${pathToFileURL(serverEntryPath).href}?shape-test=1`);
  const assets = {
    async fetch() {
      throw new Error("assets_must_not_run_for_api_paths");
    }
  };
  const response = await workerModule.default.fetch(
    new Request("https://preview.invalid/api/analytics/matches?private=marker"),
    { ASSETS: assets }
  );

  assert.equal(response.status, 503);
  assert.equal(response.headers.get("content-type"), "application/json; charset=utf-8");
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.equal(response.headers.get("x-content-type-options"), "nosniff");
  assert.equal(response.headers.has("access-control-allow-origin"), false);
  assert.equal(
    await response.text(),
    '{"schema_version":"sites_preview_api_unavailable.v1","object":"mythic_edge_sites_preview_api_unavailable","status":"unavailable","reason":"local_backend_required"}'
  );
});

test("generated Worker metadata contains no remote resource or deployment bindings", async () => {
  const files = await listFiles(distRoot);
  const wranglerFiles = files.filter((path) => /^wrangler(?:\..+)?\.json$/u.test(path.split(/[\\/]/u).at(-1)));
  assert.ok(wranglerFiles.length > 0, "generated Wrangler metadata is required");

  const forbiddenKeys = new Set([
    "account_id",
    "deployment_id",
    "project_id",
    "remote_bindings",
    "route",
    "routes",
    "tunnel"
  ]);
  const emptyResourceKeys = new Set([
    "d1_databases",
    "dispatch_namespaces",
    "durable_objects",
    "kv_namespaces",
    "queues",
    "r2_buckets",
    "services",
    "vars"
  ]);

  for (const path of wranglerFiles) {
    const value = JSON.parse(await readFile(path, "utf8"));
    const keys = collectObjectKeys(value);
    for (const forbidden of forbiddenKeys) {
      assert.equal(keys.has(forbidden), false, `generated metadata contains forbidden key: ${forbidden}`);
    }
    for (const resourceKey of emptyResourceKeys) {
      if (Object.hasOwn(value, resourceKey)) {
        assertDeepEmpty(value[resourceKey], resourceKey);
      }
    }
    assert.deepEqual(value.assets, {
      binding: "ASSETS",
      not_found_handling: "single-page-application",
      run_worker_first: ["/api", "/api/*"],
      directory: "../client"
    });
    assert.deepEqual(value.observability, { enabled: false });
  }
});

test("generated build output remains ignored", () => {
  for (const path of [clientEntryPath, serverEntryPath, builtMetadataPath]) {
    const result = spawnSync("git", ["check-ignore", "-q", relative(repositoryRoot, path)], {
      cwd: repositoryRoot,
      shell: false
    });
    assert.equal(result.status, 0, "generated output must be ignored");
  }
});
