import { act, render, screen, within } from "@testing-library/react";

import { App } from "./App";
import { IncidentList } from "./components/IncidentList";
import { toChartPoints } from "./components/ResponseChart";
import { ServiceCard } from "./components/ServiceCard";
import { makeResponse, makeService } from "./testData";

describe("ServiceCard", () => {
  it("renders 90 bars with their colors, including grey for no data", () => {
    render(<ServiceCard service={makeService()} />);
    const bars = screen.getAllByTestId("uptime-bar");
    expect(bars).toHaveLength(90);
    expect(bars[0]).toHaveAttribute("data-color", "grey");
    expect(bars[1]).toHaveAttribute("data-color", "amber");
    expect(bars[2]).toHaveAttribute("data-color", "red");
    expect(bars[3]).toHaveAttribute("data-color", "green");
    expect(screen.getByTestId("service-state")).toHaveTextContent("Up");
  });
});

describe("IncidentList", () => {
  it("marks an open incident and shows a message when there are none", () => {
    const { rerender } = render(
      <IncidentList
        incidents={[
          { id: 2, opened_at: "2026-06-15T10:00:00Z", closed_at: null, open: true, duration_seconds: 600 },
          { id: 1, opened_at: "2026-06-10T10:00:00Z", closed_at: "2026-06-10T10:42:00Z", open: false, duration_seconds: 2520 },
        ]}
      />,
    );
    const items = screen.getAllByTestId("incident");
    expect(items).toHaveLength(2);
    expect(within(items[0]).getByTestId("incident-open")).toBeInTheDocument();
    expect(within(items[1]).queryByTestId("incident-open")).toBeNull();
    expect(within(items[0]).getByTestId("incident-duration")).toHaveTextContent("10 min");
    expect(within(items[1]).getByTestId("incident-duration")).toHaveTextContent("42 min");

    rerender(<IncidentList incidents={[]} />);
    expect(screen.getByTestId("incidents-empty")).toHaveTextContent("No incidents");
  });
});

describe("ResponseChart data", () => {
  it("leaves down checks out", () => {
    const points = toChartPoints(makeService().response_times);
    expect(points.map((p) => p.ms)).toEqual([120, 1500]);
  });
});

describe("App", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("asks for data again after 30 seconds", async () => {
    const load = vi.fn().mockResolvedValue(makeResponse());
    render(<App load={load} />);
    await act(async () => {});
    expect(load).toHaveBeenCalledTimes(1);
    expect(screen.getByTestId("service-name")).toHaveTextContent("Accountable");
    await act(async () => {
      await vi.advanceTimersByTimeAsync(29_000);
    });
    expect(load).toHaveBeenCalledTimes(1);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1_000);
    });
    expect(load).toHaveBeenCalledTimes(2);
  });

  it("keeps the last data and shows a notice when a refresh fails", async () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const load = vi.fn().mockResolvedValueOnce(makeResponse()).mockRejectedValue(new Error("down"));
    render(<App load={load} />);
    await act(async () => {});
    await act(async () => {
      await vi.advanceTimersByTimeAsync(30_000);
    });
    expect(screen.getByTestId("load-error")).toHaveTextContent("last data");
    expect(screen.getByTestId("service-name")).toBeInTheDocument();
  });
});
