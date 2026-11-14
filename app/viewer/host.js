"use strict";
// The same viewer runs as a static website, local integration preview or MCP App.
(function () {
  const embedded = !!window.SCHEMATICA_EMBEDDED, integration = !!window.SCHEMATICA_INTEGRATION;
  const pending = new Map(), listeners = new Set(), blobs = new Map();
  let serial = 0, sessionId, latest, initialResolve, connected = false, hostOrigin = "*", hostCapabilities = {};
  const thumbnails = new WeakMap();
  const observer = typeof IntersectionObserver === "undefined" ? null : new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      const config = thumbnails.get(entry.target); observer.unobserve(entry.target);
      Host.imageUrl(config).then(url => { if (entry.target.isConnected) entry.target.src = url; }).catch(() => { entry.target.alt = "Preview unavailable"; });
    }
  });
  const initial = new Promise(resolve => initialResolve = resolve);
  function notify(method, params) { window.parent.postMessage({ jsonrpc: "2.0", method, params }, hostOrigin); }
  function rpc(method, params) {
    return new Promise((resolve, reject) => {
      const id = ++serial;
      const timer = setTimeout(() => { pending.delete(id); reject(new Error("The host did not respond. Try again or use the viewer link.")); }, 20000);
      pending.set(id, { resolve, reject, timer });
      window.parent.postMessage({ jsonrpc: "2.0", id, method, params }, hostOrigin);
    });
  }
  async function tool(name, args = {}) {
    const value = await rpc("tools/call", { name, arguments: args });
    if (value.isError) throw new Error(value.content?.find(x => x.type === "text")?.text || "Tool failed");
    return value;
  }
  async function json(url, body) {
    const response = await fetch(url, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
    const value = await response.json(); if (!response.ok) throw new Error(value.error || "Request failed"); return value;
  }
  function received(value) {
    if (!value?.session_id) return;
    sessionId = value.session_id; latest = value; initialResolve(value);
    for (const listener of listeners) listener(value);
  }
  if (embedded) {
    window.addEventListener("message", event => {
      if (event.source !== window.parent || (hostOrigin !== "*" && event.origin !== hostOrigin)) return;
      const message = event.data;
      if (!message || message.jsonrpc !== "2.0") return;
      if (message.id && pending.has(message.id)) {
        if (hostOrigin === "*" && event.origin !== "null") hostOrigin = event.origin;
        const job = pending.get(message.id); pending.delete(message.id); clearTimeout(job.timer);
        message.error ? job.reject(new Error(message.error.message)) : job.resolve(message.result);
      } else if (message.method === "ui/notifications/tool-result") {
        received(message.params?.structuredContent);
      } else if (message.method === "ui/notifications/host-context-changed" && message.params?.theme) {
        document.documentElement.dataset.theme = message.params.theme;
      } else if (message.method === "ping" || message.method === "ui/resource-teardown") {
        window.parent.postMessage({ jsonrpc: "2.0", id: message.id, result: {} }, hostOrigin);
      }
    });
  }
  const Host = {
    active: embedded || integration, embedded,
    async load() {
      if (embedded) {
        if (!connected) {
          const init = await rpc("ui/initialize", { protocolVersion: "2026-01-26", appInfo: { name: "Schematica", version: "0.1.0" }, appCapabilities: { availableDisplayModes: ["inline", "fullscreen"] } });
          connected = true;
          hostCapabilities = init.hostCapabilities || {};
          if (init.hostContext?.theme) document.documentElement.dataset.theme = init.hostContext.theme;
          notify("ui/notifications/initialized", {});
          new ResizeObserver(() => notify("ui/notifications/size-changed", { height: document.body.scrollHeight })).observe(document.body);
        }
        await initial;
        return (await tool("viewer_data", { session_id: sessionId }))._meta;
      }
      if (integration) {
        const params = new URLSearchParams(location.search);
        sessionId = params.get("session");
        if (!sessionId) {
          const filters = params.has("symbol") ? { ids: [params.get("symbol")] } : {};
          const response = await json("/api/search", { filters }); received(response);
          if (params.has("symbol") && params.has("revision")) {
            await json("/api/select", { symbol_id: params.get("symbol"), revision: Number(params.get("revision")),
              size: params.get("size") || "medium", stroke: params.get("stroke") || "medium", options: JSON.parse(params.get("options") || "{}"),
              session_id: sessionId, ...(params.has("draft") ? { draft_id: params.get("draft") } : {}) });
          }
          const url = new URL(location.href); url.searchParams.set("session", sessionId); history.replaceState(null, "", url);
        }
        const data = await json(`/api/viewer?session=${encodeURIComponent(sessionId)}`); latest = data.result;
        return data;
      }
      return { catalog: await json("./library/catalog.json"), session: { filters: {} } };
    },
    async artwork(config) {
      if (embedded) return (await tool("get_artwork", { asset: config.asset }))._meta.svg;
      const response = await fetch(integration ? "/artwork/" + config.asset : "./library/" + config.svg);
      if (!response.ok) throw new Error("Preview unavailable. Reload to try again."); return response.text();
    },
    async imageUrl(config) {
      if (!embedded) return integration ? "/artwork/" + config.asset : "./library/" + config.svg;
      if (!blobs.has(config.asset)) blobs.set(config.asset, Host.artwork(config).then(svg => URL.createObjectURL(new Blob([svg], { type: "image/svg+xml" }))));
      return blobs.get(config.asset);
    },
    async download(config) {
      if (!embedded || hostCapabilities.downloadFile === undefined) {
        throw new Error("This chat cannot download files directly. Open the browser viewer link and export there.");
      }
      const svg = await Host.artwork(config);
      const response = await rpc("ui/download-file", { contents: [{ type: "resource", resource: {
        uri: "file:///" + encodeURIComponent(config.key + ".svg"), mimeType: "image/svg+xml", text: svg
      } }] });
      if (response.isError) throw new Error("Download was cancelled or refused by the chat host.");
    },
    thumbnail(img, config) {
      if (embedded && observer) { thumbnails.set(img, config); observer.observe(img); }
      else Host.imageUrl(config).then(url => { if (img.isConnected) img.src = url; }).catch(() => { img.alt = "Preview unavailable"; });
    },
    async search(query, filters) {
      const args = { query, session_id: sessionId, ...(filters ? { filters } : {}) };
      const response = embedded ? (await tool("search_symbols", args)).structuredContent : await json("/api/search", args);
      received(response); return response;
    },
    async select(symbol, config) {
      const args = { symbol_id: symbol.id, revision: symbol.revision, size: config.size, stroke: config.stroke,
        options: config.options || {}, session_id: sessionId, ...(symbol.draft_id ? { draft_id: symbol.draft_id } : {}) };
      const selection = embedded ? (await tool("use_symbol", args)).structuredContent : await json("/api/select", args);
      if (embedded) {
        try { await rpc("ui/update-model-context", { structuredContent: { schematica_selection: selection } }); }
        catch (_) { return { selection, contextDelivered: false }; }
      }
      return { selection, contextDelivered: true };
    },
    subscribe(listener) { listeners.add(listener); },
    startUpdates() {
      if (!integration) return;
      setInterval(async () => {
        if (document.hidden || !sessionId) return;
        try { const next = await json(`/api/session?session=${sessionId}`); if (next.sequence !== latest?.sequence) received(next); } catch (_) { /* Retain the current usable view. */ }
      }, 2000);
    }
  };
  window.SchematicaHost = Host;
})();
