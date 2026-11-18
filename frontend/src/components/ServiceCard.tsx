import { formatDateTime, formatUptime } from "../format";
import type { ServiceState, ServiceStatus } from "../types";
import { IncidentList } from "./IncidentList";
import { ResponseChart } from "./ResponseChart";
import { UptimeBars } from "./UptimeBars";

const STATE_TEXT: Record<ServiceState, string> = {
  up: "Up",
  down: "Down",
  unknown: "No checks yet",
};

export function ServiceCard({ service }: { service: ServiceStatus }) {
  return (
    <article className="panel" data-testid="service-card" aria-labelledby={`svc-${service.id}`}>
      <div className="card-head">
        <div>
          <h2 id={`svc-${service.id}`} data-testid="service-name">{service.name}</h2>
          <p className="muted small">
            {service.last_checked_at ? `Last checked ${formatDateTime(service.last_checked_at)}` : "Not checked yet"}
          </p>
        </div>
        <span className={`pill pill-${service.state}`} data-testid="service-state">
          <span className="dot" />
          {STATE_TEXT[service.state]}
        </span>
      </div>

      <section>
        <div className="section-head">
          <h3>Last 90 days</h3>
          <p className="muted small">
            <span className="mono" data-testid="uptime-90d">{formatUptime(service.uptime_90d)}</span> uptime
          </p>
        </div>
        <UptimeBars days={service.days} />
      </section>

      <section>
        <div className="section-head">
          <h3>Response time, last 24 hours</h3>
        </div>
        <ResponseChart points={service.response_times} />
      </section>

      <section>
        <div className="section-head">
          <h3>Incidents</h3>
        </div>
        <IncidentList incidents={service.incidents} />
      </section>
    </article>
  );
}
