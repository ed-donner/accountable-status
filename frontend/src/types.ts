export type BarColor = "green" | "amber" | "red" | "grey";
export type ServiceState = "up" | "down" | "unknown";

export interface DayStatus {
  date: string; // local day, YYYY-MM-DD
  uptime: number | null; // percent; null when there were no checks
  color: BarColor;
  checks: number;
}

export interface ResponsePoint {
  t: string; // ISO time
  ms: number | null; // null for a down check
}

export interface Incident {
  id: number;
  opened_at: string;
  closed_at: string | null;
  open: boolean;
  duration_seconds: number;
}

export interface ServiceStatus {
  id: string;
  name: string;
  state: ServiceState;
  last_checked_at: string | null;
  uptime_90d: number | null;
  days: DayStatus[];
  response_times: ResponsePoint[];
  incidents: Incident[];
}

export interface StatusResponse {
  generated_at: string;
  services: ServiceStatus[];
}
