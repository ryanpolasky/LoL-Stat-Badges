import type { Region } from "./regions";

export type Tier =
  | "iron"
  | "bronze"
  | "silver"
  | "gold"
  | "platinum"
  | "emerald"
  | "diamond"
  | "master"
  | "grandmaster"
  | "challenger"
  | "unranked";

export class RiotError extends Error {
  constructor(readonly status: number, message: string) {
    super(message);
  }
}

const PUUID_TTL = 30 * 24 * 3600;

async function riotGet<T>(url: string, apiKey: string): Promise<T> {
  const res = await fetch(url, { headers: { "X-Riot-Token": apiKey } });
  if (!res.ok) throw new RiotError(res.status, `Riot ${res.status} for ${new URL(url).pathname}`);
  return res.json() as Promise<T>;
}

async function getPuuid(name: string, tag: string, region: Region, apiKey: string): Promise<string> {
  const key = new Request(
    `https://puuid.lol-stat-badges.internal/${region.cluster}/${encodeURIComponent(name.toLowerCase())}/${encodeURIComponent(tag.toLowerCase())}`,
  );
  const cached = await caches.default.match(key);
  if (cached) return cached.text();

  const url = `https://${region.cluster}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/${encodeURIComponent(name)}/${encodeURIComponent(tag)}`;
  const { puuid } = await riotGet<{ puuid?: string }>(url, apiKey);
  if (!puuid) throw new RiotError(404, "No PUUID in account response");
  await caches.default.put(key, new Response(puuid, { headers: { "Cache-Control": `max-age=${PUUID_TTL}` } }));
  return puuid;
}

export async function getSoloTier(name: string, tag: string, region: Region, apiKey: string): Promise<Tier> {
  const puuid = await getPuuid(name, tag, region, apiKey);
  const url = `https://${region.platform}.api.riotgames.com/lol/league/v4/entries/by-puuid/${encodeURIComponent(puuid)}`;
  const entries = await riotGet<{ queueType: string; tier: string }[]>(url, apiKey);
  const solo = entries.find((e) => e.queueType === "RANKED_SOLO_5x5");
  return solo ? (solo.tier.toLowerCase() as Tier) : "unranked";
}
