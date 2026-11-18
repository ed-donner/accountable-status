import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { formatClock, formatResponseTime } from "../format";
import type { ResponsePoint } from "../types";

export interface ChartPoint {
  time: number;
  ms: number;
}

/** Down checks have no response time, so they are left out of the chart. */
export function toChartPoints(points: ResponsePoint[]): ChartPoint[] {
  const result: ChartPoint[] = [];
  for (const p of points) {
    if (p.ms === null) continue;
    result.push({ time: new Date(p.t).getTime(), ms: p.ms });
  }
  return result;
}

interface TipProps {
  active?: boolean;
  payload?: { payload: ChartPoint }[];
}

function ChartTip({ active, payload }: TipProps) {
  if (!active || !payload?.length) return null;
  const point = payload[0].payload;
  return (
    <div className="chart-tip" data-testid="chart-tooltip">
      <span>{formatClock(point.time)}</span>
      <span className="mono">{formatResponseTime(point.ms)}</span>
    </div>
  );
}

export function ResponseChart({ points }: { points: ResponsePoint[] }) {
  const data = toChartPoints(points);
  if (data.length === 0) {
    return (
      <p className="muted" data-testid="chart-empty">
        No response times in the last 24 hours.
      </p>
    );
  }
  return (
    <div className="chart" data-testid="response-chart" role="img" aria-label="Response time over the last 24 hours">
      <ResponsiveContainer width="100%" height={220} initialDimension={{ width: 800, height: 220 }}>
        <LineChart data={data} margin={{ top: 8, right: 28, bottom: 0, left: 0 }}>
          <CartesianGrid vertical={false} stroke="var(--grid)" />
          <XAxis
            dataKey="time"
            type="number"
            scale="time"
            domain={["dataMin", "dataMax"]}
            tickFormatter={formatClock}
            tickCount={7}
            stroke="var(--muted)"
            tickLine={false}
            axisLine={false}
            minTickGap={32}
          />
          <YAxis
            tickFormatter={(v: number) => `${v} ms`}
            stroke="var(--muted)"
            tickLine={false}
            axisLine={false}
            width={64}
          />
          <Tooltip content={<ChartTip />} cursor={{ stroke: "var(--muted)", strokeWidth: 1 }} isAnimationActive={false} />
          <Line
            type="monotone"
            dataKey="ms"
            stroke="var(--line)"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, stroke: "var(--panel)", strokeWidth: 2 }}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
