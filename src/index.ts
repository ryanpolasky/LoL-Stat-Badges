import { renderBadge, type BadgeRank } from "./badge";
import { resolveRegion } from "./regions";
import { getSoloTier, RiotError } from "./riot";

export interface Env {
  RIOT_API_KEY: string;
}

const REPO_URL = "https://github.com/ryanpolasky/LoL-Stat-Badges";
const OK_CACHE = "public, max-age=3600, stale-while-revalidate=86400";
const ERROR_CACHE = "public, max-age=300";

const NAME_RE = /^[^\p{C}\p{So}]{1,16}$/u;
const TAG_RE = /^[\p{L}\p{N}]{1,5}$/u;

function svg(body: string, cacheControl: string): Response {
  return new Response(body, {
    headers: { "Content-Type": "image/svg+xml; charset=utf-8", "Cache-Control": cacheControl },
  });
}

async function badge(regionIn: string, name: string, tag: string, rankName: boolean, env: Env): Promise<Response> {
  const region = resolveRegion(regionIn);
  const fail = () => svg(renderBadge("error", "ERROR"), ERROR_CACHE);
  if (!region || !NAME_RE.test(name) || !TAG_RE.test(tag)) return fail();

  let rank: BadgeRank;
  try {
    rank = await getSoloTier(name, tag, region, env.RIOT_API_KEY);
  } catch (e) {
    console.error(e instanceof RiotError ? e.message : e);
    return fail();
  }
  return svg(renderBadge(rank, rankName ? rank.toUpperCase() : `${name}#${tag}`), OK_CACHE);
}

function root(method: string): Response {
  if (method === "HEAD") return Response.redirect(REPO_URL, 303);
  return new Response(
    `<html><head><meta http-equiv="refresh" content="3;url=${REPO_URL}"/></head><body><h1>Thanks for using my API! :)</h1><p>You will be redirected to the GitHub repository shortly...</p></body></html>`,
    { headers: { "Content-Type": "text/html; charset=utf-8" } },
  );
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405 });
    const url = new URL(request.url);
    const path = url.pathname.replace(/^\/lol(?=\/|$)/, "").replace(/\/+$/, "");
    if (path === "") return root(request.method);

    const parts = path.split("/").slice(1);
    if (parts.length !== 4 || parts[0] !== "badge") return new Response("Not found", { status: 404 });

    let region: string, name: string, tag: string;
    try {
      [region, name, tag] = parts.slice(1).map(decodeURIComponent);
    } catch {
      return svg(renderBadge("error", "ERROR"), ERROR_CACHE);
    }
    const rankName = ["true", "1", "yes", "on"].includes(url.searchParams.get("rank_name")?.toLowerCase() ?? "");

    const cacheKey = new Request(
      `${url.origin}/lol/badge/${encodeURIComponent(region.toLowerCase())}/${encodeURIComponent(name.toLowerCase())}/${encodeURIComponent(tag.toLowerCase())}?rank_name=${rankName}`,
    );
    const cached = await caches.default.match(cacheKey);
    if (cached) return cached;

    const res = await badge(region, name, tag, rankName, env);
    ctx.waitUntil(caches.default.put(cacheKey, res.clone()));
    return res;
  },
} satisfies ExportedHandler<Env>;
