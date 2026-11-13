// Applied before the stylesheet so a saved dark theme never flashes white.
(() => {
  let theme = "dark";
  try { theme = localStorage.getItem("schematica-theme") || theme; } catch (_) {}
  document.documentElement.dataset.theme = theme === "light" ? "light" : "dark";
})();
