/* One origin and millimetre coordinate system for Library and Review previews. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.SchematicaPreview = factory();
})(typeof window !== "undefined" ? window : this, function () {
  "use strict";
  const MM_PER_SVG_UNIT = 25.4 / 72;
  function artworkTransform(config) {
    const [x, y] = config.origin_svg;
    return `scale(${MM_PER_SVG_UNIT}) translate(${-x},${-y})`;
  }
  function pinPosition([x, y]) { return [x, -y]; }
  function imageBounds(config) {
    const [cx, cy] = config.visual_center_from_origin_mm;
    return [cx - config.width_mm / 2, cy - config.height_mm / 2, config.width_mm, config.height_mm];
  }
  function fitViewport(config, width, height) {
    // Match Review's existing fit, but make the whole canvas an SVG viewport.
    const scale = Math.min(12, width * .85 / config.width_mm, height * .78 / config.height_mm);
    const [cx, cy] = config.visual_center_from_origin_mm;
    return [cx - width / scale / 2, cy - height / scale / 2, width / scale, height / scale];
  }
  function gridLines([x, y, width, height]) {
    const lines = [];
    for (let n = Math.ceil(x); n <= x + width; n++) lines.push(`M${n},${y}v${height}`);
    for (let n = Math.ceil(y); n <= y + height; n++) lines.push(`M${x},${n}h${width}`);
    return lines;
  }
  return { MM_PER_SVG_UNIT, artworkTransform, pinPosition, imageBounds, fitViewport, gridLines };
});
