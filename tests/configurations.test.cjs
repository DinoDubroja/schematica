const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const C = require('../app/viewer/configurations.js');
const library = process.env.SCHEMATICA_LIBRARY || path.join(__dirname, '../app/library');
const data = JSON.parse(fs.readFileSync(path.join(library, 'catalog.json')));

test('every supported selection resolves to its exact rendered configuration', () => {
  for (const symbol of data.symbols) for (const config of symbol.configurations) {
    assert.equal(C.find(symbol, config.size, config.stroke, config.options)?.key, config.key);
  }
});

test('comparison rows vary one dimension and hold all others at declared defaults', () => {
  for (const symbol of data.symbols) {
    const rows = C.rows(symbol, data.presets);
    assert.equal(rows.length, 2 + Object.keys(symbol.options || {}).length);
    for (const [index, row] of rows.entries()) for (const { config } of row.examples) {
      assert.ok(config);
      if (index !== 0) assert.equal(config.stroke, data.presets.default_stroke);
      if (index !== 1) assert.equal(config.size, data.presets.default_size);
      if (index < 2) assert.deepEqual(config.options || {}, C.defaults(symbol));
    }
    assert.deepEqual(rows.slice(0, 2).map(r => r.examples.length), [3, 3]);
  }
});

test('unsupported selections fall back to defaults and do not leak to other designs', () => {
  const adjustable = data.symbols.find(s => s.options);
  const fixed = data.symbols.find(s => s.id === 'resistor-eu');
  assert.deepEqual(C.applicable(adjustable, { orientation: 'unknown' }), C.defaults(adjustable));
  assert.deepEqual(C.applicable(fixed, { orientation: 'down-left' }), {});
  assert.equal(C.find(fixed, 'small', 'thick', { orientation: 'down-left' }).key, 'resistor-eu-small-thick');
});

test('library filenames preserve default names and distinguish selected orientations', () => {
  const defaults = { orientation: 'up-right' };
  assert.equal(C.exportKey('small', 'thick', {}, defaults), 'small-thick');
  assert.equal(C.exportKey('small', 'thick', defaults, defaults), 'small-thick');
  assert.equal(C.exportKey('small', 'thick', { orientation: 'down-left' }, defaults), 'small-thick-orientation-down-left');
});
