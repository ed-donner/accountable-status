import { barColor, formatDuration, formatResponseTime, formatUptime } from "./format";

describe("barColor", () => {
  it("uses the 99.9 and 99 thresholds unrounded, and grey for no data", () => {
    expect(barColor(99.95)).toBe("green");
    expect(barColor(99.9)).toBe("green");
    expect(barColor(99.8999)).toBe("amber");
    expect(barColor(99.5)).toBe("amber");
    expect(barColor(99)).toBe("amber");
    expect(barColor(98.9999)).toBe("red");
    expect(barColor(98)).toBe("red");
    expect(barColor(null)).toBe("grey");
  });
});

describe("formatting for reading", () => {
  it("formats durations", () => {
    expect(formatDuration(45)).toBe("45 s");
    expect(formatDuration(7 * 60)).toBe("7 min");
    expect(formatDuration(3 * 3600 + 5 * 60)).toBe("3 h 5 min");
    expect(formatDuration(2 * 3600)).toBe("2 h");
    expect(formatDuration(26 * 3600)).toBe("1 d 2 h");
    expect(formatDuration(-5)).toBe("0 s");
  });

  it("formats response times and uptime", () => {
    expect(formatResponseTime(87)).toBe("87 ms");
    expect(formatResponseTime(1234)).toBe("1,234 ms");
    expect(formatResponseTime(null)).toBe("No response");
    expect(formatUptime(100)).toBe("100%");
    expect(formatUptime(99.996)).toBe("99.99%");
    expect(formatUptime(99.5)).toBe("99.50%");
    expect(formatUptime(null)).toBe("No data");
  });
});
