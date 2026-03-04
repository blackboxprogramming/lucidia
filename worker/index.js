/**
 * Lucidia Cloudflare Worker — blackroad.io API edge layer
 *
 * Handles API requests at the edge for low-latency responses.
 * Long-running inference is offloaded via the /run endpoint which
 * dispatches to a Durable Object / Queue for async processing.
 *
 * Routes:
 *   GET  /          → health check
 *   GET  /status    → service status JSON
 *   POST /chat      → forward to Lucidia AI (sync, ≤30 s CPU)
 *   POST /run       → enqueue a long-running task (async via CF Queue)
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // CORS pre-flight
    if (request.method === "OPTIONS") {
      return corsResponse(new Response(null, { status: 204 }));
    }

    switch (url.pathname) {
      case "/":
        return corsResponse(
          new Response(
            JSON.stringify({
              service: "lucidia-worker",
              version: "1.0.0",
              status: "ok",
              verified: true,
            }),
            { status: 200, headers: { "Content-Type": "application/json" } }
          )
        );

      case "/status":
        return corsResponse(
          new Response(
            JSON.stringify({
              service: "lucidia-worker",
              status: "healthy",
              timestamp: new Date().toISOString(),
              region: request.cf?.colo ?? "unknown",
            }),
            { status: 200, headers: { "Content-Type": "application/json" } }
          )
        );

      case "/chat":
        if (request.method !== "POST") {
          return corsResponse(
            new Response(JSON.stringify({ error: "POST required" }), {
              status: 405,
              headers: { "Content-Type": "application/json" },
            })
          );
        }
        try {
          const body = await request.json();
          const message = body.message ?? "";
          // Stub response — replace with actual Lucidia AI call via env binding
          return corsResponse(
            new Response(
              JSON.stringify({
                reply: `Lucidia received: "${message}"`,
                source: "worker-edge",
              }),
              { status: 200, headers: { "Content-Type": "application/json" } }
            )
          );
        } catch {
          return corsResponse(
            new Response(JSON.stringify({ error: "Invalid JSON" }), {
              status: 400,
              headers: { "Content-Type": "application/json" },
            })
          );
        }

      case "/run":
        if (request.method !== "POST") {
          return corsResponse(
            new Response(JSON.stringify({ error: "POST required" }), {
              status: 405,
              headers: { "Content-Type": "application/json" },
            })
          );
        }
        try {
          const task = await request.json();
          // Enqueue for async long-running processing
          if (env.TASK_QUEUE) {
            await env.TASK_QUEUE.send(task);
            return corsResponse(
              new Response(
                JSON.stringify({ queued: true, task }),
                { status: 202, headers: { "Content-Type": "application/json" } }
              )
            );
          }
          return corsResponse(
            new Response(
              JSON.stringify({ queued: false, message: "Queue not configured" }),
              { status: 200, headers: { "Content-Type": "application/json" } }
            )
          );
        } catch {
          return corsResponse(
            new Response(JSON.stringify({ error: "Invalid JSON" }), {
              status: 400,
              headers: { "Content-Type": "application/json" },
            })
          );
        }

      default:
        return corsResponse(
          new Response(JSON.stringify({ error: "Not found" }), {
            status: 404,
            headers: { "Content-Type": "application/json" },
          })
        );
    }
  },
};

function corsResponse(response) {
  // Public edge API — CORS is intentionally open (*) for the demo worker.
  // Restrict to specific origins (e.g., "https://blackroad.io") once a
  // custom domain is configured in wrangler.toml and Cloudflare DNS.
  const headers = new Headers(response.headers);
  headers.set("Access-Control-Allow-Origin", "*");
  headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
