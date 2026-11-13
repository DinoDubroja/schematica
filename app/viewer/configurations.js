/* Shared selection rules for the viewer and its option-comparison tests. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.SchematicaConfigurations = factory();
})(typeof window !== "undefined" ? window : this, function () {
  "use strict";
  function defaults(symbol) {
    return Object.fromEntries(Object.entries(symbol.options || {}).map(([key, spec]) => [key, spec.default]));
  }
  function applicable(symbol, selections = {}) {
    const result = defaults(symbol);
    for (const [key, spec] of Object.entries(symbol.options || {})) {
      if (spec.values.some(value => value.id === selections[key])) result[key] = selections[key];
    }
    return result;
  }
  function find(symbol, size, stroke, selections = {}) {
    const options = applicable(symbol, selections);
    return symbol.configurations.find(config => config.size === size && config.stroke === stroke &&
      Object.keys(options).every(key => config.options?.[key] === options[key]));
  }
  function rows(symbol, presets) {
    const size = presets.default_size, stroke = presets.default_stroke, options = defaults(symbol);
    const rows = [
      { name: "Stroke", examples: symbol.presets.strokes.map(id => ({ name: presets.strokes[id].name,
        detail: `${presets.strokes[id].width_mm.toFixed(2)} mm`, config: find(symbol, size, id, options) })) },
      { name: "Size", examples: symbol.presets.sizes.map(id => ({ name: presets.sizes[id].name,
        detail: `${presets.sizes[id].factor.toFixed(2)}×`, config: find(symbol, id, stroke, options) })) }
    ];
    for (const [key, spec] of Object.entries(symbol.options || {})) rows.push({ name: spec.name,
      examples: spec.values.map(value => ({ name: value.name, config: find(symbol, size, stroke, { ...options, [key]: value.id }) })) });
    return rows;
  }
  function exportKey(size, stroke, selections, exportDefaults) {
    return `${size}-${stroke}` + Object.entries(selections).sort(([a], [b]) => a.localeCompare(b))
      .filter(([key, value]) => value !== exportDefaults[key]).map(([key, value]) => `-${key}-${value}`).join("");
  }
  return { defaults, applicable, find, rows, exportKey };
});
