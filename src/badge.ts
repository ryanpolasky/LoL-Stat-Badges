import { ICONS, VERDANA_WIDTHS } from "./generated";
import type { Tier } from "./riot";

export type BadgeRank = Tier | "error";

export const COLORS: Record<BadgeRank, string> = {
  iron: "#3c2f2a",
  bronze: "#ae6f5b",
  silver: "#7c8892",
  gold: "#ae8a5a",
  platinum: "#4da8b5",
  emerald: "#33b86f",
  diamond: "#218dc6",
  master: "#ba48e1",
  grandmaster: "#e3653d",
  challenger: "#43AFEC",
  error: "#cc0000",
  unranked: "#808080",
};

const FONT_SIZE = 11;
const BOLD_SCALE = 1.12;
const LETTER_SPACING = 1;
const TEXT_X = 38;
const RIGHT_PAD = 19;

export function textWidth(text: string): number {
  let width = 0;
  let count = 0;
  for (const ch of text) {
    const cp = ch.codePointAt(0)!;
    const em = VERDANA_WIDTHS[cp];
    width += em !== undefined ? em * BOLD_SCALE : cp >= 0x2e80 ? 1 : 0.62;
    count++;
  }
  return width * FONT_SIZE + Math.max(0, count - 1) * LETTER_SPACING;
}

function escapeXml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
}

export function renderBadge(rank: BadgeRank, text: string): string {
  const textLength = Math.round(textWidth(text) * 10) / 10;
  const width = Math.ceil(TEXT_X + textLength + RIGHT_PAD);
  const label = escapeXml(text);
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="28" role="img" aria-label="${label}">` +
    `<title>${label}</title>` +
    `<rect width="${width}" height="28" fill="${COLORS[rank]}"/>` +
    `<image href="data:image/png;base64,${ICONS[rank]}" x="5" y="0" width="28" height="28"/>` +
    `<text x="${TEXT_X}" y="15.5" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="${FONT_SIZE}" font-weight="bold" fill="#fff" dominant-baseline="middle" textLength="${textLength}" lengthAdjust="spacing">${label}</text>` +
    `</svg>`
  );
}
