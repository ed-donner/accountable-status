import { useState } from "react";

import { formatDay, formatUptime } from "../format";
import type { DayStatus } from "../types";

const LABEL: Record<DayStatus["color"], string> = {
  green: "Operational",
  amber: "Some downtime",
  red: "Significant downtime",
  grey: "No data",
};

export function UptimeBars({ days }: { days: DayStatus[] }) {
  const [active, setActive] = useState<number | null>(null);
  const shown = active === null ? null : days[active];

  return (
    <div className="bars-wrap">
      <ol className="bars" data-testid="uptime-bars" onMouseLeave={() => setActive(null)}>
        {days.map((day, index) => (
          <li
            key={day.date}
            className={`bar bar-${day.color}`}
            data-testid="uptime-bar"
            data-color={day.color}
            data-date={day.date}
            tabIndex={0}
            aria-label={`${formatDay(day.date)}: ${formatUptime(day.uptime)}, ${LABEL[day.color]}`}
            onMouseEnter={() => setActive(index)}
            onFocus={() => setActive(index)}
            onBlur={() => setActive(null)}
          />
        ))}
      </ol>
      <div className="bars-tip" aria-live="polite" data-testid="uptime-tooltip">
        {shown ? (
          <>
            <span>{formatDay(shown.date)}</span>
            <span className="mono">{formatUptime(shown.uptime)}</span>
          </>
        ) : (
          <span className="muted">Hover over a day to see its uptime</span>
        )}
      </div>
      <div className="bars-axis">
        <span>90 days ago</span>
        <span>Today</span>
      </div>
      <ul className="key" data-testid="uptime-key">
        <li><span className="swatch bar-green" />99.9% or more</li>
        <li><span className="swatch bar-amber" />99% to 99.9%</li>
        <li><span className="swatch bar-red" />Below 99%</li>
        <li><span className="swatch bar-grey" />No data</li>
      </ul>
    </div>
  );
}
