import { useCallback, useEffect, useRef, useState } from "react";

import { REFRESH_MS, fetchStatus } from "./api";
import { ServiceCard } from "./components/ServiceCard";
import type { StatusResponse } from "./types";

interface AppProps {
  /** Overridable so tests can use their own fetcher. */
  load?: (signal?: AbortSignal) => Promise<StatusResponse>;
  refreshMs?: number;
}

export function App({ load = fetchStatus, refreshMs = REFRESH_MS }: AppProps) {
  const [data, setData] = useState<StatusResponse | null>(null);
  const [failed, setFailed] = useState(false);
  const loadRef = useRef(load);
  loadRef.current = load;

  const refresh = useCallback(async (signal?: AbortSignal) => {
    try {
      const next = await loadRef.current(signal);
      setData(next);
      setFailed(false);
    } catch (error) {
      if (signal?.aborted) return;
      console.error("Could not load the status", error);
      setFailed(true);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    void refresh(controller.signal);
    const timer = setInterval(() => void refresh(controller.signal), refreshMs);
    return () => {
      controller.abort();
      clearInterval(timer);
    };
  }, [refresh, refreshMs]);

  return (
    <main className="page" data-testid="status-page">
      <header className="page-header">
        <h1>Accountable Status</h1>
        <p className="tagline">Checked every minute</p>
      </header>
      {failed && (
        <p className="notice" role="alert" data-testid="load-error">
          {data
            ? "The status service did not answer. Showing the last data received."
            : "The status service did not answer. Trying again shortly."}
        </p>
      )}
      {!data && !failed && (
        <p className="muted" data-testid="loading">
          Loading status
        </p>
      )}
      {data?.services.map((service) => <ServiceCard key={service.id} service={service} />)}
    </main>
  );
}
