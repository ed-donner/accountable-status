import type { StatusResponse } from "./types";

export const REFRESH_MS = 30_000;

export async function fetchStatus(signal?: AbortSignal): Promise<StatusResponse> {
  const response = await fetch("/api/status", { signal });
  if (!response.ok) {
    throw new Error(`The status service answered ${response.status}`);
  }
  return (await response.json()) as StatusResponse;
}
