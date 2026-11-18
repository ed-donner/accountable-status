import type { BarColor } from "./types";

export const GREEN_AT = 99.9;
export const AMBER_AT = 99.0;

/** Bar color for a day's uptime in percent. Compared unrounded; null means no checks. */
export function barColor(uptime: number | null): BarColor {
  if (uptime === null) return "grey";
  if (uptime >= GREEN_AT) return "green";
  if (uptime >= AMBER_AT) return "amber";
  return "red";
}

/** Uptime for reading: cut (not rounded) to two decimals so 99.996 never shows as 100%. */
export function formatUptime(uptime: number | null): string {
  if (uptime === null) return "No data";
  const cut = Math.floor(uptime * 100 + 1e-9) / 100;
  return `${cut.toFixed(Number.isInteger(cut) ? 0 : 2)}%`;
}

export function formatResponseTime(ms: number | null): string {
  if (ms === null) return "No response";
  return `${Math.round(ms).toLocaleString("en-US")} ms`;
}

/** 45 s, 7 min, 3 h 5 min, 1 d 2 h. */
export function formatDuration(totalSeconds: number): string {
  const seconds = Math.max(0, Math.round(totalSeconds));
  if (seconds < 60) return `${seconds} s`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) {
    const rest = minutes % 60;
    return rest ? `${hours} h ${rest} min` : `${hours} h`;
  }
  const days = Math.floor(hours / 24);
  const restHours = hours % 24;
  return restHours ? `${days} d ${restHours} h` : `${days} d`;
}

/** A YYYY-MM-DD local day, for example "Mon 15 Jun 2026". */
export function formatDay(day: string): string {
  const [y, m, d] = day.split("-").map(Number);
  return new Date(y, m - 1, d).toLocaleDateString("en-GB", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatClock(ms: number): string {
  return new Date(ms).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
}
