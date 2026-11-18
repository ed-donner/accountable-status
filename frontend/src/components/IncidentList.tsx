import { formatDateTime, formatDuration } from "../format";
import type { Incident } from "../types";

export function IncidentList({ incidents }: { incidents: Incident[] }) {
  if (incidents.length === 0) {
    return (
      <p className="muted" data-testid="incidents-empty">
        No incidents in the last 90 days.
      </p>
    );
  }
  return (
    <ul className="incidents" data-testid="incident-list">
      {incidents.map((incident) => (
        <li
          key={incident.id}
          className="incident"
          data-testid="incident"
          data-open={incident.open ? "true" : "false"}
        >
          <div className="incident-state">
            {incident.open ? (
              <span className="pill pill-down" data-testid="incident-open">Open</span>
            ) : (
              <span className="pill pill-closed">Closed</span>
            )}
          </div>
          <div className="incident-times">
            <span>Started {formatDateTime(incident.opened_at)}</span>
            <span className="muted">
              {incident.closed_at ? `Ended ${formatDateTime(incident.closed_at)}` : "Still open"}
            </span>
          </div>
          <div className="incident-duration mono" data-testid="incident-duration">
            {formatDuration(incident.duration_seconds)}
          </div>
        </li>
      ))}
    </ul>
  );
}
