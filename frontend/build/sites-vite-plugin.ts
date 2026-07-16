import { createHash } from "node:crypto";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

import type { Plugin } from "vite";

const SOURCE_METADATA_PARTS = [".openai", "hosting.json"] as const;
const GENERATED_METADATA_PARTS = ["dist", ".openai"] as const;

function symbolicError(code: string): Error {
  return new Error(code);
}

export function validateSitesHostingMetadata(bytes: Uint8Array): void {
  let value: unknown;

  try {
    value = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  } catch {
    throw symbolicError("sites_hosting_metadata_invalid");
  }

  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw symbolicError("sites_hosting_metadata_invalid");
  }

  const record = value as Record<string, unknown>;
  const keys = Object.keys(record).sort();
  if (
    keys.length !== 2 ||
    keys[0] !== "d1" ||
    keys[1] !== "r2" ||
    record.d1 !== null ||
    record.r2 !== null
  ) {
    throw symbolicError("sites_hosting_metadata_invalid");
  }
}

function sha256(bytes: Uint8Array): string {
  return createHash("sha256").update(bytes).digest("hex");
}

export async function copySitesHostingMetadata(frontendRoot: string): Promise<void> {
  const sourcePath = resolve(frontendRoot, ...SOURCE_METADATA_PARTS);
  const generatedDirectory = resolve(frontendRoot, ...GENERATED_METADATA_PARTS);
  const generatedPath = resolve(generatedDirectory, "hosting.json");
  let sourceBytes: Uint8Array;

  try {
    sourceBytes = await readFile(sourcePath);
  } catch {
    throw symbolicError("sites_hosting_metadata_missing");
  }

  validateSitesHostingMetadata(sourceBytes);

  try {
    await rm(generatedDirectory, { force: true, recursive: true });
    await mkdir(generatedDirectory, { recursive: true });
    await writeFile(generatedPath, sourceBytes);
    const generatedBytes = await readFile(generatedPath);
    if (sha256(sourceBytes) !== sha256(generatedBytes)) {
      throw symbolicError("sites_hosting_metadata_digest_mismatch");
    }
  } catch (error) {
    if (error instanceof Error && error.message === "sites_hosting_metadata_digest_mismatch") {
      throw error;
    }
    throw symbolicError("sites_hosting_metadata_copy_failed");
  }
}

export function sitesHostingMetadataPlugin(frontendRoot: string): Plugin {
  return {
    name: "mythic-edge-sites-hosting-metadata",
    enforce: "post",
    async closeBundle() {
      await copySitesHostingMetadata(frontendRoot);
    }
  };
}
