import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import worker from "../src/index";
import { textWidth } from "../src/badge";

class FakeCache {
  store = new Map<string, Response>();
  async match(req: Request) {
    return this.store.get(req.url)?.clone();
  }
  async put(req: Request, res: Response) {
    this.store.set(req.url, res.clone());
  }
}

const env = { RIOT_API_KEY: "test-key" };
let cache: FakeCache;
let fetchMock: ReturnType<typeof vi.fn>;
let pending: Promise<unknown>[];
const ctx = { waitUntil: (p: Promise<unknown>) => pending.push(p), passThroughOnException() {} } as unknown as ExecutionContext;

function riot(routes: Record<string, unknown | number>) {
  fetchMock.mockImplementation(async (url: string) => {
    const hit = Object.entries(routes).find(([k]) => url.includes(k));
    if (!hit) return new Response("nope", { status: 404 });
    const [, v] = hit;
    return typeof v === "number" ? new Response("err", { status: v }) : Response.json(v);
  });
}

async function get(path: string, method = "GET") {
  const res = await worker.fetch(new Request(`https://api.ryanpolasky.com${path}`, { method }), env, ctx);
  await Promise.all(pending);
  return res;
}

beforeEach(() => {
  cache = new FakeCache();
  pending = [];
  fetchMock = vi.fn();
  vi.stubGlobal("caches", { default: cache });
  vi.stubGlobal("fetch", fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

const EGGY = {
  "by-riot-id/Eggy/NEW": { puuid: "p-eggy" },
  "entries/by-puuid/p-eggy": [
    { queueType: "RANKED_FLEX_SR", tier: "GOLD" },
    { queueType: "RANKED_SOLO_5x5", tier: "PLATINUM" },
  ],
};

describe("badge", () => {
  it("renders the solo queue rank with the riot id", async () => {
    riot(EGGY);
    const res = await get("/lol/badge/NA1/Eggy/NEW");
    const body = await res.text();
    expect(res.status).toBe(200);
    expect(res.headers.get("Content-Type")).toContain("image/svg+xml");
    expect(res.headers.get("Cache-Control")).toContain("max-age=3600");
    expect(body).toContain(">Eggy#NEW</text>");
    expect(body).toContain('fill="#4da8b5"');
    expect(body).toMatch(/textLength="[\d.]+"/);
    expect(body).toContain("sans-serif");
    expect(fetchMock.mock.calls[0][0]).toBe("https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Eggy/NEW");
    expect(fetchMock.mock.calls[1][0]).toBe("https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/p-eggy");
    expect(fetchMock.mock.calls[0][1].headers["X-Riot-Token"]).toBe("test-key");
  });

  it("shows the tier name with rank_name=true", async () => {
    riot(EGGY);
    expect(await (await get("/lol/badge/NA1/Eggy/NEW?rank_name=true")).text()).toContain(">PLATINUM</text>");
  });

  it("falls back to unranked without a solo queue entry", async () => {
    riot({ "by-riot-id": { puuid: "p" }, "by-puuid/p": [{ queueType: "RANKED_FLEX_SR", tier: "GOLD" }] });
    const body = await (await get("/lol/badge/EUW/Someone/EUW")).text();
    expect(body).toContain('fill="#808080"');
    expect(fetchMock.mock.calls[0][0]).toContain("https://europe.api.riotgames.com/");
    expect(fetchMock.mock.calls[1][0]).toContain("https://euw1.api.riotgames.com/");
  });

  it("routes SEA accounts through the asia cluster", async () => {
    riot({ "by-riot-id": { puuid: "p" }, "by-puuid/p": [] });
    await get("/lol/badge/VN2/Someone/VN2");
    expect(fetchMock.mock.calls[0][0]).toContain("https://asia.api.riotgames.com/");
    expect(fetchMock.mock.calls[1][0]).toContain("https://vn2.api.riotgames.com/");
  });

  it("encodes names with spaces and non-latin characters", async () => {
    riot({ "by-riot-id": { puuid: "p" }, "by-puuid/p": [{ queueType: "RANKED_SOLO_5x5", tier: "CHALLENGER" }] });
    const body = await (await get("/lol/badge/KR/Hide%20on%20bush/KR1")).text();
    expect(fetchMock.mock.calls[0][0]).toContain("/by-riot-id/Hide%20on%20bush/KR1");
    expect(body).toContain(">Hide on bush#KR1</text>");
    await get(`/lol/badge/KR/${encodeURIComponent("페이커")}/KR1`);
    expect(fetchMock.mock.calls.at(-2)![0]).toContain(encodeURIComponent("페이커"));
  });

  it("escapes markup in names", async () => {
    riot({ "by-riot-id": { puuid: "p" }, "by-puuid/p": [] });
    const body = await (await get(`/lol/badge/NA/${encodeURIComponent("<b>&")}/NA1`)).text();
    expect(body).toContain("&#60;b&#62;&#38;#NA1");
    expect(body).not.toContain("<b>");
  });

  it.each([
    ["unknown player", "/lol/badge/NA1/nobody/ZZZ"],
    ["bad region", "/lol/badge/XX/Eggy/NEW"],
    ["name too long", "/lol/badge/NA1/waytoolongnameeeeeeeeee/NEW"],
    ["tag too long", "/lol/badge/NA1/Eggy/TOOLONG"],
    ["non-alnum tag", "/lol/badge/NA1/Eggy/a-b"],
    ["bad escape", "/lol/badge/NA1/%E0%A4%A/NEW"],
  ])("returns a red error badge (not a 500) for %s", async (_, path) => {
    riot({});
    const res = await get(path);
    const body = await res.text();
    expect(res.status).toBe(200);
    expect(body).toContain(">ERROR</text>");
    expect(body).toContain('fill="#cc0000"');
    expect(res.headers.get("Cache-Control")).toBe("public, max-age=300");
  });

  it("returns an error badge when riot rate limits", async () => {
    riot({ "by-riot-id": 429 });
    expect(await (await get("/lol/badge/NA1/Eggy/NEW")).text()).toContain(">ERROR</text>");
  });

  it("serves repeat views from cache, case-insensitively", async () => {
    riot(EGGY);
    await get("/lol/badge/NA1/Eggy/NEW");
    await get("/lol/badge/na1/eggy/new");
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("reuses the cached puuid across rank refreshes", async () => {
    riot(EGGY);
    await get("/lol/badge/NA1/Eggy/NEW");
    await get("/lol/badge/NA1/Eggy/NEW?rank_name=true");
    expect(fetchMock.mock.calls.filter(([u]) => u.includes("by-riot-id"))).toHaveLength(1);
  });

  it("keeps the embedded icon small", async () => {
    riot(EGGY);
    expect((await (await get("/lol/badge/NA1/Eggy/NEW")).text()).length).toBeLessThan(15_000);
  });
});

describe("width", () => {
  it("grows with text and counts CJK as full width", () => {
    expect(textWidth("Hide on bush#KR1")).toBeGreaterThan(textWidth("Eggy#NEW"));
    expect(textWidth("페이커")).toBeGreaterThan(textWidth("abc"));
    expect(textWidth("iii")).toBeLessThan(textWidth("WWW"));
  });
});

describe("routes", () => {
  it("serves the landing page", async () => {
    expect((await get("/lol")).status).toBe(200);
    expect((await get("/lol/")).status).toBe(200);
  });
  it("redirects HEAD on root", async () => {
    const res = await get("/lol", "HEAD");
    expect(res.status).toBe(303);
  });
  it("404s unknown paths", async () => {
    expect((await get("/lol/nope")).status).toBe(404);
  });
});
