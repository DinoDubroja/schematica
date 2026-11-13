"use strict";
const $ = selector => document.querySelector(selector);
const ns = "http://www.w3.org/2000/svg";
const state = { data: null, symbol: "resistor-eu", size: "medium", stroke: "medium", filter: "all", render: 0 };
const cache = new Map();
function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function svgEl(tag, attrs) {
  const node = document.createElementNS(ns, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  return node;
}
function initTheme() {
  const button = $("#theme-toggle");
  function update() {
    const label = `Switch to ${document.documentElement.dataset.theme === "dark" ? "light" : "dark"} mode`;
    button.setAttribute("aria-label", label);
    button.title = label;
  }
  button.addEventListener("click", () => {
    const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("schematica-theme", theme); } catch (_) { /* Switching still works without storage. */ }
    update();
  });
  update();
}
function activeSymbol() { return state.data.symbols.find(s => s.id === state.symbol); }
function configFor(symbol) { return symbol.configurations.find(c => c.size === state.size && c.stroke === state.stroke); }
function titleCase(value) { return value[0].toUpperCase() + value.slice(1); }
function selectCard(id) {
  // Update in place so keyboard focus stays on the chosen card.
  state.symbol = id;
  document.querySelectorAll(".card[data-symbol]").forEach(card => {
    const active = card.dataset.symbol === id;
    card.classList.toggle("active", active);
    card.setAttribute("aria-pressed", active);
  });
  renderInspector();
  if (matchMedia("(max-width: 720px)").matches) {
    $(".inspector").scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth", block: "start" });
  }
}
function renderCards() {
  const words = $("#search").value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  const symbols = state.data.symbols.filter(s =>
    (state.filter === "all" || s.types.includes(state.filter)) &&
    words.every(word => [s.name, s.description, ...s.keywords, ...s.types].join(" ").toLowerCase().includes(word)));
  const cards = $("#cards");
  cards.replaceChildren();
  for (const symbol of symbols) {
    const card = el("button", undefined, "card" + (symbol.id === state.symbol ? " active" : ""));
    card.dataset.symbol = symbol.id;
    card.setAttribute("aria-pressed", symbol.id === state.symbol);
    const config = configFor(symbol);
    const thumb = el("span", undefined, "thumbnail"), img = el("img");
    img.src = `./library/${config.svg}`;
    img.alt = "";
    img.style.width = `${config.width_mm / 34 * 100}%`;
    thumb.append(img);
    card.append(thumb, el("span", symbol.name, "card-name"));
    cards.append(card);
  }
  $("#empty").hidden = symbols.length > 0;
  cards.setAttribute("aria-busy", "false");
}
async function renderPreview(symbol, config) {
  const token = ++state.render;
  $("#canvas").setAttribute("aria-busy", "true");
  // Do not leave a previous configuration visible while its replacement loads.
  $("#canvas").replaceChildren();
  if (!cache.has(config.key)) cache.set(config.key, fetch(`./library/${config.svg}`).then(response => {
    if (!response.ok) throw new Error("Preview unavailable. Reload to try again.");
    return response.text();
  }).catch(error => { cache.delete(config.key); throw error; }));
  try {
    const source = new DOMParser().parseFromString(await cache.get(config.key), "image/svg+xml");
    if (token !== state.render) return;
    if (source.querySelector("parsererror")) throw new Error("Preview unavailable. Reload to try again.");
    const root = svgEl("svg", { viewBox: "-18 -12 36 24", role: "img", "aria-label": `${config.name}, ${config.size} size, ${config.stroke} stroke` });
    const grid = svgEl("g", { class: "inspection-grid grid-lines", fill: "none", "stroke-width": ".025" });
    for (let x = -18; x <= 18; x++) grid.append(svgEl("path", { d: `M${x},-12v24` }));
    for (let y = -12; y <= 12; y++) grid.append(svgEl("path", { d: `M-18,${y}h36` }));
    grid.append(svgEl("path", { class: "grid-axes", d: "M-18,0h36M0,-12v24", "stroke-width": ".045" }));
    root.append(grid);
    const [ox, oy] = config.origin_svg;
    const wrapper = svgEl("g", { class: "symbol-artwork", transform: `scale(${25.4 / 72}) translate(${-ox},${-oy})` });
    for (const child of source.documentElement.children) {
      if (child.localName === "g" || child.localName === "defs") wrapper.append(document.importNode(child, true));
    }
    root.append(wrapper);
    const pins = svgEl("g", { class: "inspection-grid pin-markers" });
    for (const [id, [x, y]] of Object.entries(config.pins_mm)) {
      const circle = svgEl("circle", { cx: x, cy: -y, r: .20 });
      const title = svgEl("title", {});
      title.textContent = symbol.pins.find(pin => pin.id === id)?.name || id;
      circle.append(title);
      pins.append(circle);
    }
    root.append(pins);
    $("#canvas").replaceChildren(root);
    updateGrid();
  } catch (error) {
    if (token === state.render) $("#canvas").replaceChildren(el("p", error.message, "error"));
  } finally {
    if (token === state.render) $("#canvas").setAttribute("aria-busy", "false");
  }
}
function updateGrid() {
  $("#canvas").classList.toggle("hide-grid", !$("#grid-toggle").checked);
}
function setDownload(link, path) {
  link.href = path;
  link.download = path.split("/").pop();
  link.removeAttribute("aria-disabled");
}
function renderInspector() {
  const symbol = activeSymbol(), config = configFor(symbol);
  $("#symbol-name").textContent = symbol.name;
  for (const kind of ["size", "stroke"]) document.querySelectorAll(`button[data-${kind}]`).forEach(button => {
    const selected = button.dataset[kind] === state[kind];
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", selected);
  });
  $("#description").textContent = symbol.description;
  $("#keywords").replaceChildren(...symbol.keywords.map(keyword => el("li", keyword)));
  setDownload($("#download-svg"), `./library/${config.svg}`);
  renderPreview(symbol, config);
}
async function init() {
  try {
    const response = await fetch("./library/catalog.json");
    if (!response.ok) throw new Error("Library unavailable. Reload to try again.");
    state.data = await response.json();
    state.size = state.data.presets.default_size;
    state.stroke = state.data.presets.default_stroke;
    state.symbol = state.data.symbols[0].id;
    renderCards();
    renderInspector();
  } catch (_) {
    $("#load-error").textContent = "Library unavailable. Reload to try again.";
    $("#load-error").hidden = false;
    $("#cards").setAttribute("aria-busy", "false");
    $(".inspector").setAttribute("aria-busy", "false");
    return;
  }
  document.querySelectorAll("[disabled]").forEach(control => control.disabled = false);
  $(".inspector").setAttribute("aria-busy", "false");
  $("#search").addEventListener("input", renderCards);
  $("#cards").addEventListener("click", event => {
    const card = event.target.closest("[data-symbol]");
    if (card) selectCard(card.dataset.symbol);
  });
  document.querySelectorAll("[data-filter]").forEach(button => button.addEventListener("click", () => {
    state.filter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach(other => {
      other.classList.toggle("active", other === button);
      other.setAttribute("aria-pressed", other === button);
    });
    renderCards();
  }));
  for (const kind of ["size", "stroke"]) document.querySelectorAll(`button[data-${kind}]`).forEach(button => button.addEventListener("click", () => {
    state[kind] = button.dataset[kind];
    renderCards();
    renderInspector();
  }));
  $("#grid-toggle").addEventListener("change", updateGrid);
  $("#open-exports").addEventListener("click", () => {
    $("#export-summary").textContent = `6 symbols · ${titleCase(state.size)} · ${titleCase(state.stroke)}`;
    setDownload($("#download-library"), `./${state.data.exports[`${state.size}-${state.stroke}`]}`);
    $("#export-dialog").showModal();
  });
  $("#close-dialog").addEventListener("click", () => $("#export-dialog").close());
  $("#download-library").addEventListener("click", () => $("#export-dialog").close());
  document.addEventListener("keydown", event => {
    if (event.key === "/" && !event.ctrlKey && !event.metaKey && !event.altKey && !/INPUT|TEXTAREA/.test(document.activeElement.tagName) && !$("#export-dialog").open) {
      event.preventDefault();
      $("#search").focus();
    }
  });
}
initTheme();
init();
