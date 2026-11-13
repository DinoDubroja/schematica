/* Browser-local review state. This file never sends writes to a server. */
(() => {
  "use strict";
  const key = "schematica-approvals-v1";
  const identity = symbol => ({ id: symbol.id, revision: symbol.revision,
    fingerprint: symbol.verification.fingerprint });
  const matches = (entry, symbol) => !!entry && entry.id === symbol.id &&
    entry.revision === symbol.revision && entry.fingerprint === symbol.verification.fingerprint;
  const official = symbol => symbol.verification.status === "verified";
  function reconcile(entries, symbols) {
    const valid = {};
    for (const symbol of symbols) {
      if (!official(symbol) && matches(entries?.[symbol.id], symbol)) valid[symbol.id] = identity(symbol);
    }
    return valid;
  }
  function create(symbols, storage) {
    let pending = {}, history = [], storageAvailable = true, discarded = 0;
    try {
      const saved = JSON.parse(storage.getItem(key) || "null");
      if (saved?.schema_version === 1) {
        pending = reconcile(saved.pending, symbols);
        discarded = Math.max(0, Object.keys(saved.pending || {}).length - Object.keys(pending).length);
        history = Array.isArray(saved.history) ? saved.history.slice(-100).map(value => reconcile(value, symbols)) : [];
      }
    } catch (_) { storageAvailable = false; }
    function persist() {
      try { storage.setItem(key, JSON.stringify({ schema_version: 1, pending, history })); }
      catch (_) { storageAvailable = false; }
    }
    persist();
    return {
      has: symbol => matches(pending[symbol.id], symbol),
      count: () => Object.keys(pending).length,
      canUndo: () => history.length > 0,
      storageAvailable: () => storageAvailable,
      discarded: () => discarded,
      select(symbol, selected) {
        if (official(symbol) || matches(pending[symbol.id], symbol) === selected) return false;
        history.push(structuredClone(pending)); history = history.slice(-100);
        if (selected) pending[symbol.id] = identity(symbol); else delete pending[symbol.id];
        persist(); return true;
      },
      undo() {
        if (!history.length) return false;
        pending = reconcile(history.pop(), symbols); persist(); return true;
      },
      payload() { return { schema_version: 1, library: "schematica", approvals: Object.values(pending) }; }
    };
  }
  const api = { key, identity, matches, official, reconcile, create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else window.SchematicaReview = api;
})();
