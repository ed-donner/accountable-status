import type { DayStatus, ServiceStatus, StatusResponse } from "./types";

export function makeDays(count = 90): DayStatus[] {
  return Array.from({ length: count }, (_, i) => {
    const date = new Date(2026, 5, 1 + i);
    const iso = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
    if (i === 0) return { date: iso, uptime: null, color: "grey", checks: 0 };
    if (i === 1) return { date: iso, uptime: 99.5, color: "amber", checks: 1440 };
    if (i === 2) return { date: iso, uptime: 90, color: "red", checks: 1440 };
    return { date: iso, uptime: 100, color: "green", checks: 1440 };
  });
}

export function makeService(overrides: Partial<ServiceStatus> = {}): ServiceStatus {
  return {
    id: "accountable",
    name: "Accountable",
    state: "up",
    last_checked_at: "2026-06-15T12:00:00Z",
    uptime_90d: 99.8,
    days: makeDays(),
    response_times: [
      { t: "2026-06-15T10:00:00Z", ms: 120 },
      { t: "2026-06-15T10:01:00Z", ms: null },
      { t: "2026-06-15T10:02:00Z", ms: 1500 },
    ],
    incidents: [],
    ...overrides,
  };
}

export function makeResponse(service: ServiceStatus = makeService()): StatusResponse {
  return { generated_at: "2026-06-15T12:00:00Z", services: [service] };
}
