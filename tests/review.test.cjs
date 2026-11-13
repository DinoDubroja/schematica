const test = require('node:test');
const assert = require('node:assert/strict');
const Review = require('../app/viewer/review.js');
const design = (id, fingerprint = 'shape-1', status = 'unverified') =>
  ({id, revision: 1, verification: {fingerprint, status}});
const memory = () => { let value; return {getItem: () => value, setItem: (_, next) => {value = next}}; };

test('pending approvals persist, identify exact geometry, and can be undone after reload', () => {
  const symbols = [design('a'), design('b')], storage = memory();
  let state = Review.create(symbols, storage);
  state.select(symbols[0], true); state.select(symbols[1], true);
  state = Review.create(symbols, storage);
  assert.equal(state.count(), 2);
  assert.deepEqual(state.payload().approvals[0], {id:'a', revision:1, fingerprint:'shape-1'});
  state.undo(); assert.equal(state.count(), 1); assert.equal(state.has(symbols[0]), true);
  state.undo(); assert.equal(state.count(), 0);
});
test('stale revision/fingerprint and unknown designs cannot survive reload or Undo', () => {
  const a = design('a'), storage = memory(); let state = Review.create([a], storage);
  state.select(a, true); state.select(a, false);
  const changed = design('a', 'shape-2'); state = Review.create([changed], storage);
  state.undo(); assert.equal(state.count(), 0);
  state.select(changed, true);
  state = Review.create([{...changed, revision:2}], storage); assert.equal(state.count(), 0);
  state = Review.create([], storage); assert.equal(state.count(), 0);
});
test('official approvals clear pending entries and cannot be reversed locally', () => {
  const a = design('a'), storage = memory(); let state = Review.create([a], storage);
  state.select(a, true);
  const approved = design('a', 'shape-1', 'verified'); state = Review.create([approved], storage);
  assert.equal(state.count(), 0); assert.equal(state.select(approved, false), false);
  state.undo(); assert.equal(state.count(), 0); assert.equal(approved.verification.status, 'verified');
});
test('local state is isolated, and blocked storage still permits copying this session', () => {
  const a = design('a'), one = Review.create([a], memory()), two = Review.create([a], memory());
  one.select(a, true); assert.equal(two.count(), 0); assert.equal(a.verification.status, 'unverified');
  const blocked = Review.create([a], {getItem(){throw Error()},setItem(){throw Error()}});
  blocked.select(a, true); assert.equal(blocked.count(), 1); assert.equal(blocked.storageAvailable(), false);
});
