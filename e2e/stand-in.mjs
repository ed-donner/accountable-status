// A stand-in for Accountable: a page and an API (which answers 401, like the real one), plus a
// control port the tests use to stop and start both. Only the tests talk to the control port.

import http from "node:http";

const pagePort = Number(process.env.STAND_IN_PAGE_PORT);
const apiPort = Number(process.env.STAND_IN_API_PORT);
const controlPort = Number(process.env.STAND_IN_CONTROL_PORT);

function makeServer(status, body) {
  return http.createServer((_req, res) => {
    res.writeHead(status, { "content-type": "text/plain" });
    res.end(body);
  });
}

const targets = [
  { port: pagePort, status: 200, body: "page", server: null },
  { port: apiPort, status: 401, body: "unauthorized", server: null },
];

function listen(target) {
  return new Promise((resolve, reject) => {
    const server = makeServer(target.status, target.body);
    server.once("error", reject);
    server.listen(target.port, "127.0.0.1", () => {
      target.server = server;
      resolve();
    });
  });
}

function close(target) {
  return new Promise((resolve) => {
    const server = target.server;
    if (!server) return resolve();
    target.server = null;
    server.closeAllConnections();
    server.close(() => resolve());
  });
}

const control = http.createServer(async (req, res) => {
  try {
    if (req.url === "/stop") await Promise.all(targets.map(close));
    else if (req.url === "/start") await Promise.all(targets.filter((t) => !t.server).map(listen));
    else if (req.url !== "/state") {
      res.writeHead(404).end("unknown");
      return;
    }
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ running: targets.every((t) => t.server) }));
  } catch (error) {
    console.error("Stand-in control failed", error);
    res.writeHead(500).end(String(error));
  }
});

await Promise.all(targets.map(listen));
control.listen(controlPort, "127.0.0.1");
for (const signal of ["SIGINT", "SIGTERM"]) process.on(signal, () => process.exit(0));
