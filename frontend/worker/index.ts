export interface SitesPreviewAssets {
  fetch(request: Request): Promise<Response>;
}

export interface SitesPreviewEnv {
  ASSETS: SitesPreviewAssets;
}

export interface SitesPreviewWorker {
  fetch(request: Request, env: SitesPreviewEnv): Promise<Response>;
}

type UnavailableReason = "local_backend_required" | "preview_assets_unavailable";

const UNAVAILABLE_HEADERS = {
  "Cache-Control": "no-store",
  "Content-Type": "application/json; charset=utf-8",
  "X-Content-Type-Options": "nosniff"
} as const;

function isApiPath(pathname: string): boolean {
  return pathname === "/api" || pathname.startsWith("/api/");
}

function unavailableResponse(reason: UnavailableReason, method: string): Response {
  const body = JSON.stringify({
    schema_version: "sites_preview_api_unavailable.v1",
    object: "mythic_edge_sites_preview_api_unavailable",
    status: "unavailable",
    reason
  });

  return new Response(method === "HEAD" ? null : body, {
    status: 503,
    headers: UNAVAILABLE_HEADERS
  });
}

const worker: SitesPreviewWorker = {
  async fetch(request, env) {
    if (isApiPath(new URL(request.url).pathname)) {
      return unavailableResponse("local_backend_required", request.method);
    }

    const assets = env?.ASSETS;
    if (!assets || typeof assets.fetch !== "function") {
      return unavailableResponse("preview_assets_unavailable", request.method);
    }

    try {
      return await assets.fetch(request);
    } catch {
      return unavailableResponse("preview_assets_unavailable", request.method);
    }
  }
};

export default worker;
