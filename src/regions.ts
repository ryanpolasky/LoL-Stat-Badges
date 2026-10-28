type Cluster = "americas" | "asia" | "europe";

const PLATFORMS: Record<string, [platform: string, cluster: Cluster]> = {
  NA: ["na1", "americas"],
  NA1: ["na1", "americas"],
  BR: ["br1", "americas"],
  BR1: ["br1", "americas"],
  LAN: ["la1", "americas"],
  LA1: ["la1", "americas"],
  LAS: ["la2", "americas"],
  LA2: ["la2", "americas"],
  OC: ["oc1", "americas"],
  OCE: ["oc1", "americas"],
  OC1: ["oc1", "americas"],
  KR: ["kr", "asia"],
  JP: ["jp1", "asia"],
  JP1: ["jp1", "asia"],
  PH: ["ph2", "asia"],
  PH2: ["ph2", "asia"],
  SG: ["sg2", "asia"],
  SG2: ["sg2", "asia"],
  TH: ["th2", "asia"],
  TH2: ["th2", "asia"],
  TW: ["tw2", "asia"],
  TW2: ["tw2", "asia"],
  VN: ["vn2", "asia"],
  VN2: ["vn2", "asia"],
  EUW: ["euw1", "europe"],
  EUW1: ["euw1", "europe"],
  EUN: ["eun1", "europe"],
  EUNE: ["eun1", "europe"],
  EUN1: ["eun1", "europe"],
  TR: ["tr1", "europe"],
  TR1: ["tr1", "europe"],
  RU: ["ru", "europe"],
  RU1: ["ru", "europe"],
  ME: ["me1", "europe"],
  ME1: ["me1", "europe"],
};

export interface Region {
  platform: string;
  cluster: Cluster;
}

export function resolveRegion(input: string): Region | null {
  const hit = PLATFORMS[input.toUpperCase()];
  return hit ? { platform: hit[0], cluster: hit[1] } : null;
}
