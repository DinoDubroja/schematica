"use strict";
const $ = selector => document.querySelector(selector);
const el = (tag, text, className) => { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; };
const svgEl = (tag, attrs) => { const node = document.createElementNS("http://www.w3.org/2000/svg", tag); for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value); return node; };
const Review = window.SchematicaReview;
const Configurations = window.SchematicaConfigurations;
const Host = window.SchematicaHost;
let agentResult = null;
const state = { data: null, symbol: null, size: "medium", stroke: "medium", view: "all", options: {}, render: 0, matrix: 0 };
const cache = new Map();
let review, svgSerial = 0;
function notify(message) { $("#notice").textContent = message; $("#notice").hidden = !message; }
function titleCase(value) { return value[0].toUpperCase() + value.slice(1).replaceAll("-", " "); }
function activeSymbol() { return state.data.symbols.find(s => s.id === state.symbol); }
function configFor(symbol) { return Configurations.find(symbol, state.size, state.stroke, symbol.id === state.symbol ? state.options : {}); }
function status(symbol) { return Review.official(symbol) ? "Verified" : review.has(symbol) ? "Pending" : "Unverified"; }
function symbolLink(symbol) { const url = new URL(location.href); url.hash = `symbol=${encodeURIComponent(symbol.id)}`; return url.href; }
function linkedSymbol() { return new URLSearchParams(location.hash.slice(1)).get("symbol"); }
function initTheme() {
  const button = $("#theme-toggle");
  function update() { const label = `Switch to ${document.documentElement.dataset.theme === "dark" ? "light" : "dark"} mode`; button.setAttribute("aria-label", label); button.title = label; }
  button.addEventListener("click", () => {
    const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("schematica-theme", theme); } catch (_) { /* The control still works. */ }
    update();
  }); update();
}
function filteredSymbols() {
  const words = $("#search").value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return state.data.symbols.filter(symbol =>
    (!agentResult || agentResult.match_ids.includes(symbol.id)) &&
    (state.view === "all" || !Review.official(symbol)) &&
    ($("#family-filter").value === "all" || symbol.family === $("#family-filter").value) &&
    ($("#batch-filter").value === "all" || symbol.batch === $("#batch-filter").value) &&
    words.every(word => [symbol.name, symbol.description, ...symbol.keywords, ...symbol.types].join(" ").toLowerCase().includes(word)));
}
function selectCard(id, updateUrl = true, scroll = true) {
  if (!state.data.symbols.some(symbol => symbol.id === id)) return;
  if (state.symbol !== id) state.options = Configurations.defaults(state.data.symbols.find(s => s.id === id));
  state.symbol = id;
  if (updateUrl) history.replaceState(null, "", symbolLink(activeSymbol()));
  document.querySelectorAll(".card[data-symbol]").forEach(card => {
    card.classList.toggle("active", card.dataset.symbol === id);
    card.querySelector("button").setAttribute("aria-pressed", card.dataset.symbol === id);
  });
  renderCards(); renderInspector();
  if (scroll && matchMedia("(max-width: 720px)").matches) $(".inspector").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth", block: "start" });
}
function renderCards() {
  const focus = document.activeElement?.dataset.approval, cardFocus = document.activeElement?.dataset.symbol;
  const symbols = filteredSymbols(), cards = $("#cards"); cards.replaceChildren();
  for (const symbol of symbols) {
    const card = el("article", undefined, "card" + (symbol.id === state.symbol ? " active" : "")); card.dataset.symbol = symbol.id;
    const button = el("button", undefined, "card-main"); button.dataset.symbol = symbol.id; button.setAttribute("aria-pressed", symbol.id === state.symbol);
    const config = configFor(symbol), thumb = el("span", undefined, "thumbnail"), img = el("img");
    Host.thumbnail(img, config); img.alt = ""; img.loading = "lazy"; img.style.width = `${config.width_mm / 34 * 100}%`; thumb.append(img);
    button.append(thumb, el("span", symbol.name, "card-name"));
    const label = el("label", undefined, "card-review"), checkbox = el("input"); checkbox.type = "checkbox"; checkbox.dataset.approval = symbol.id;
    checkbox.checked = Review.official(symbol) || review.has(symbol); checkbox.disabled = Review.official(symbol); checkbox.setAttribute("aria-label", `Verify ${symbol.name}`);
    label.append(checkbox, el("span", status(symbol))); card.append(button, label); cards.append(card);
  }
  $("#empty").hidden = symbols.length > 0; cards.setAttribute("aria-busy", "false"); cards.setAttribute("aria-labelledby", state.view === "all" ? "all-tab" : "unverified-tab");
  $("#review-count").textContent = Host.active ? `${symbols.length} symbols` : `${symbols.filter(s => !Review.official(s) && !review.has(s)).length} remaining`;
  const count = review.count(); $("#copy-approvals").textContent = count ? `Copy approvals (${count})` : "Copy approvals"; $("#copy-approvals").disabled = !count;
  if (focus) cards.querySelector(`input[data-approval="${CSS.escape(focus)}"]`)?.focus({ preventScroll: true });
  else if (cardFocus) cards.querySelector(`button[data-symbol="${CSS.escape(cardFocus)}"]`)?.focus({ preventScroll: true });
}
async function readArtwork(config) {
  const key = config.asset || config.key;
  if (!cache.has(key)) cache.set(key, Host.artwork(config).catch(error => { cache.delete(key); throw error; }));
  const source = new DOMParser().parseFromString(await cache.get(key), "image/svg+xml");
  if (source.querySelector("parsererror")) throw new Error("Preview unavailable. Reload to try again.");
  // Variations and the main preview can contain the same configuration: isolate IDs.
  const prefix = `preview-${++svgSerial}-`, ids = new Map();
  source.querySelectorAll("[id]").forEach(node => ids.set(node.id, prefix + node.id));
  source.querySelectorAll("*").forEach(node => {
    for (const attr of [...node.attributes]) {
      let value = attr.value;
      if (attr.name === "id") value = ids.get(value);
      else { value = value.replace(/url\(#([^)]*)\)/g, (_, id) => `url(#${ids.get(id) || id})`); if (attr.localName === "href" && value.startsWith("#")) value = "#" + (ids.get(value.slice(1)) || value.slice(1)); }
      if (attr.namespaceURI) node.setAttributeNS(attr.namespaceURI, attr.name, value); else node.setAttribute(attr.name, value);
    }
  }); return source;
}
async function previewSvg(symbol, config, inspection) {
  const source = await readArtwork(config);
  // The common physical viewport preserves size differences in the comparison.
  const root = svgEl("svg", { viewBox: inspection ? "-18 -12 36 24" : "-12 -12 24 24", role: "img", "aria-label": `${symbol.name}, ${config.size} size, ${config.stroke} stroke${config.options?.orientation ? `, ${config.options.orientation}` : ""}` });
  if (inspection) {
    const grid = svgEl("g", { class: "inspection-grid grid-lines", fill: "none", "stroke-width": ".025" });
    for (let x = -18; x <= 18; x++) grid.append(svgEl("path", { d: `M${x},-12v24` }));
    for (let y = -12; y <= 12; y++) grid.append(svgEl("path", { d: `M-18,${y}h36` }));
    grid.append(svgEl("path", { class: "grid-axes", d: "M-18,0h36M0,-12v24", "stroke-width": ".045" })); root.append(grid);
  }
  const [ox, oy] = config.origin_svg;
  const wrapper = svgEl("g", { class: "symbol-artwork", transform: `scale(${25.4 / 72}) translate(${-ox},${-oy})` });
  for (const child of source.documentElement.children) if (child.localName === "g" || child.localName === "defs") wrapper.append(document.importNode(child, true));
  root.append(wrapper);
  if (inspection) {
    const pins = svgEl("g", { class: "inspection-grid pin-markers" });
    for (const [id, [x, y]] of Object.entries(config.pins_mm)) {
      const circle = svgEl("circle", { cx: x, cy: -y, r: .20 }), title = svgEl("title", {}); title.textContent = symbol.pins.find(pin => pin.id === id)?.name || id; circle.append(title); pins.append(circle);
    } root.append(pins);
  } return root;
}
async function renderPreview(symbol, config) {
  const token = ++state.render, canvas = $("#canvas"); canvas.setAttribute("aria-busy", "true"); canvas.replaceChildren();
  try { const svg = await previewSvg(symbol, config, true); if (token === state.render) canvas.replaceChildren(svg); }
  catch (error) { if (token === state.render) canvas.replaceChildren(el("p", error.message, "error")); }
  finally { if (token === state.render) canvas.setAttribute("aria-busy", "false"); }
}
function setDownload(link, path) { link.href = path; link.download = path.split("/").pop(); link.removeAttribute("aria-disabled"); }
function updateApprovalControls() {
  const symbol = activeSymbol(), official = Review.official(symbol), pending = review.has(symbol);
  $("#approve-design").checked = official || pending; $("#approve-design").disabled = official; $("#approve-design").setAttribute("aria-label", `Approve ${symbol.name}, all supported variations`);
  $("#approval-label").textContent = status(symbol); $("#pending-note").hidden = !pending;
  $("#verify-next").disabled = official; $("#undo-approval").disabled = !review.canUndo();
}
function renderInspector() {
  const symbol = activeSymbol(); if (!symbol) return;
  const config = configFor(symbol); $("#symbol-name").textContent = symbol.name;
  renderOptions(symbol);
  for (const kind of ["size", "stroke"]) document.querySelectorAll(`button[data-${kind}]`).forEach(button => { const selected = button.dataset[kind] === state[kind]; button.classList.toggle("active", selected); button.setAttribute("aria-pressed", selected); });
  $("#description").textContent = symbol.description; $("#keywords").replaceChildren(...symbol.keywords.map(keyword => el("li", keyword)));
  const link = $("#download-svg"); link.removeAttribute("href"); link.setAttribute("aria-disabled", "true");
  Host.imageUrl(config).then(url => { if (activeSymbol()?.id === symbol.id && configFor(activeSymbol()).key === config.key) { setDownload(link, url); link.download = config.key + ".svg"; } }).catch(error => notify(error.message));
  $("#draft-note").hidden = !symbol.draft_id;
  updateApprovalControls(); renderPreview(symbol, config);
}
function changeApproval(symbol, selected) { review.select(symbol, selected); renderCards(); updateApprovalControls(); if (!review.storageAvailable()) notify("Browser storage is unavailable. Copy approvals before leaving this page."); }
async function copyText(text, title) {
  try { await navigator.clipboard.writeText(text); notify(`${title} copied.`); }
  catch (_) { $("#copy-title").textContent = title; $("#copy-text").value = text; $("#copy-dialog").showModal(); $("#copy-text").focus(); $("#copy-text").select(); }
}
function renderOptions(symbol) {
  const container = $("#symbol-options"), focus = document.activeElement;
  const focusedKey = focus?.dataset.option, focusedValue = focus?.dataset.value;
  container.replaceChildren();
  for (const [key, spec] of Object.entries(symbol.options || {})) {
    const field = el("fieldset"), legend = el("legend", spec.name), choices = el("div", undefined, "segmented option-choices");
    for (const value of spec.values) {
      const button = el("button", value.name); button.dataset.option = key; button.dataset.value = value.id;
      const selected = state.options[key] === value.id; button.classList.toggle("active", selected); button.setAttribute("aria-pressed", selected);
      choices.append(button);
    }
    field.append(legend, choices); container.append(field);
  }
  container.hidden = !container.children.length;
  if (focusedKey) container.querySelector(`button[data-option="${CSS.escape(focusedKey)}"][data-value="${CSS.escape(focusedValue)}"]`)?.focus({ preventScroll: true });
}
async function showConfigurations() {
  const symbol = activeSymbol(), token = ++state.matrix, rows = $("#variation-rows");
  $("#variation-symbol").textContent = symbol.name; rows.replaceChildren(); rows.setAttribute("aria-busy", "true");
  const jobs = [];
  for (const specification of Configurations.rows(symbol, state.data.presets)) {
    const row = el("section", undefined, "variation-row"), heading = el("h3", specification.name);
    const examples = el("div", undefined, "variation-examples");
    for (const example of specification.examples) {
      const cell = el("figure", undefined, "variation-example"), art = el("div", undefined, "variation-art");
      const caption = el("figcaption", example.name); if (example.detail) caption.append(el("span", example.detail));
      cell.append(art, caption); examples.append(cell);
      jobs.push(previewSvg(symbol, example.config, false).then(svg => { if (token === state.matrix) art.append(svg); })
        .catch(error => { if (token === state.matrix) art.append(el("p", error.message, "error")); }));
    }
    row.append(heading, examples); rows.append(row);
  }
  $("#configuration-dialog").showModal(); await Promise.all(jobs);
  if (token === state.matrix) rows.setAttribute("aria-busy", "false");
}
async function init() {
  try {
    const loaded = await Host.load(); state.data = loaded.catalog;
    review = Review.create(state.data.symbols, { getItem: key => localStorage.getItem(key), setItem: (key, value) => localStorage.setItem(key, value) });
    state.size = state.data.presets.default_size; state.stroke = state.data.presets.default_stroke;
    state.symbol = state.data.symbols.some(s => s.id === linkedSymbol()) ? linkedSymbol() : state.data.symbols[0].id;
    state.options = Configurations.defaults(activeSymbol());
    for (const kind of ["family", "batch"]) for (const value of [...new Set(state.data.symbols.map(s => s[kind]))]) {
      const option = el("option", value === "starter" ? "Starter library" : value === "resistors-01" ? "Resistors · Batch 01" : titleCase(value)); option.value = value; $(`#${kind}-filter`).append(option);
    }
    document.querySelectorAll("[disabled]").forEach(control => control.disabled = false);
    if (Host.active) {
      document.body.classList.add("agent-viewer");
      $("#use-symbol").hidden = false; $("#agent-filters").hidden = false;
      $("#open-exports").hidden = true;
      $("#copy-approvals").hidden = true;
      document.querySelectorAll(".review-tools > :not(#show-configurations),.pending-note").forEach(node => node.hidden = true);
      if (loaded.result) applyAgentResult(loaded.result);
      Host.subscribe(async result => {
        try { const data = await Host.load(); state.data = data.catalog; applyAgentResult(result); } catch (error) { notify(error.message); }
      });
      Host.startUpdates();
    }
    renderCards(); renderInspector(); $(".inspector").setAttribute("aria-busy", "false");
    if (review.discarded()) notify("Outdated or officially published selections were cleared.");
    if (!review.storageAvailable()) notify("Browser storage is unavailable. Copy approvals before leaving this page.");
  } catch (_) { $("#load-error").textContent = "Library unavailable. Reload to try again."; $("#load-error").hidden = false; $("#cards").setAttribute("aria-busy", "false"); $(".inspector").setAttribute("aria-busy", "false"); return; }
  $("#search").addEventListener("input", () => { renderCards(); if (Host.active) syncVisibleSelection(); });
  $("#search").addEventListener("keydown", async event => {
    if (Host.active && event.key === "Enter") { try { const query = event.target.value; event.target.value = ""; await Host.search(query); } catch (error) { notify(error.message); } }
  });
  $("#browse-all").addEventListener("click", async () => { try { $("#search").value = ""; $("#family-filter").value = "all"; $("#batch-filter").value = "all"; await Host.search("Browse all"); } catch (error) { notify(error.message); } });
  $("#use-symbol").addEventListener("click", async () => {
    const button = $("#use-symbol"); button.disabled = true;
    try { const response = await Host.select(activeSymbol(), configFor(activeSymbol())); notify(response.contextDelivered ? "Symbol selection is ready for the agent." : "Selection saved. Ask the agent to retrieve it from this viewer."); }
    catch (error) { notify(error.message); } finally { button.disabled = false; }
  });
  for (const kind of ["family", "batch"]) $(`#${kind}-filter`).addEventListener("change", () => { renderCards(); if (Host.active) syncVisibleSelection(); });
  $("#cards").addEventListener("click", event => { const button = event.target.closest("button[data-symbol]"); if (button) selectCard(button.dataset.symbol); });
  $("#cards").addEventListener("change", event => { if (event.target.dataset.approval) changeApproval(state.data.symbols.find(s => s.id === event.target.dataset.approval), event.target.checked); });
  const tabs = [...document.querySelectorAll("[data-view]")];
  function setView(button) { state.view = button.dataset.view; tabs.forEach(other => { other.classList.toggle("active", other === button); other.setAttribute("aria-selected", other === button); other.tabIndex = other === button ? 0 : -1; }); renderCards(); if (Host.active) syncVisibleSelection(); }
  tabs.forEach(button => {
    button.addEventListener("click", () => setView(button));
    button.addEventListener("keydown", event => { if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) { event.preventDefault(); const next = event.key === "Home" ? tabs[0] : event.key === "End" ? tabs.at(-1) : tabs[(tabs.indexOf(button) + 1) % tabs.length]; setView(next); next.focus(); } });
  });
  for (const kind of ["size", "stroke"]) document.querySelectorAll(`button[data-${kind}]`).forEach(button => button.addEventListener("click", () => { state[kind] = button.dataset[kind]; renderCards(); renderInspector(); }));
  $("#symbol-options").addEventListener("click", event => {
    const button = event.target.closest("button[data-option]"); if (!button) return;
    state.options[button.dataset.option] = button.dataset.value; renderCards(); renderInspector();
  });
  $("#grid-toggle").addEventListener("change", () => $("#canvas").classList.toggle("hide-grid", !$("#grid-toggle").checked));
  $("#approve-design").addEventListener("change", event => changeApproval(activeSymbol(), event.target.checked));
  $("#verify-next").addEventListener("click", () => {
    const current = activeSymbol(), visible = filteredSymbols(), index = visible.indexOf(current); changeApproval(current, true);
    const ordered = [...visible.slice(index + 1), ...visible.slice(0, index + 1)], next = ordered.find(symbol => !Review.official(symbol) && !review.has(symbol));
    if (next) selectCard(next.id); else notify("Review selections complete for this filter. Copy approvals to publish.");
  });
  $("#undo-approval").addEventListener("click", () => { review.undo(); renderCards(); updateApprovalControls(); notify("Pending selection undone."); });
  $("#copy-approvals").addEventListener("click", () => copyText(JSON.stringify(review.payload(), null, 2), "Approvals"));
  $("#copy-reference").addEventListener("click", () => { const symbol = activeSymbol(); copyText(`${symbol.name}\nID: ${symbol.id}\nRevision: ${symbol.revision}\n${symbolLink(symbol)}`, "Symbol reference"); });
  $("#select-copy-text").addEventListener("click", () => { $("#copy-text").focus(); $("#copy-text").select(); });
  $("#show-configurations").addEventListener("click", showConfigurations);
  document.querySelectorAll("[data-close]").forEach(button => button.addEventListener("click", () => document.getElementById(button.dataset.close).close()));
  window.addEventListener("hashchange", () => { if (linkedSymbol()) selectCard(linkedSymbol(), false, false); });
  $("#open-exports").addEventListener("click", () => {
    const options = Configurations.applicable(activeSymbol(), state.options);
    const labels = Object.entries(options).map(([key, value]) => activeSymbol().options[key].values.find(v => v.id === value).name);
    $("#export-summary").textContent = [state.data.symbols.length + " symbols", titleCase(state.size), titleCase(state.stroke), ...labels].join(" · ");
    setDownload($("#download-library"), `./${state.data.exports[Configurations.exportKey(state.size, state.stroke, options, state.data.export_defaults)]}`);
    $("#export-dialog").showModal();
  });
  $("#close-dialog").addEventListener("click", () => $("#export-dialog").close()); $("#download-library").addEventListener("click", () => $("#export-dialog").close());
  document.addEventListener("keydown", event => { if (event.key === "/" && !event.ctrlKey && !event.metaKey && !event.altKey && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) && !document.querySelector("dialog[open]")) { event.preventDefault(); $("#search").focus(); } });
}
function syncVisibleSelection() {
  const visible = filteredSymbols(); $(".inspector").hidden = visible.length === 0;
  if (visible.length && !visible.some(s => s.id === state.symbol)) selectCard(visible[0].id, false, false);
}
function applyAgentResult(result) {
  agentResult = result;
  if (result.selection) {
    state.symbol = result.selection.id;
    state.size = result.selection.configuration.size;
    state.stroke = result.selection.configuration.stroke;
    state.options = result.selection.configuration.options;
  }
  $("#active-filters").textContent = Object.entries(result.filters).map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(", ") : value}`).join(" · ") || "All symbols · dev library";
  if (result.filters.size) state.size = result.filters.size;
  if (result.filters.stroke) state.stroke = result.filters.stroke;
  renderCards(); syncVisibleSelection(); renderInspector();
}
initTheme();
init();
