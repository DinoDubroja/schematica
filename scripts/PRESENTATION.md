# Figure presentation

LaTeX is the editable source. SVG is the default display format in chat and on
GitHub. Keep `preview.png` as a convenient download. Captions stay with the
figure and as readable, attributed text in its record.

## Export

Compile `drawing.tex` to a one-page PDF in the ignored `build/` directory using
Tectonic or a suitable LaTeX installation. With Python and PyMuPDF available:

```text
python scripts/export_svg.py build/<example>/drawing.pdf styles/<collection>/examples/<category>/<example> --title "Figure title" --description "Accessible description of the drawing."
```

This writes `preview-light.svg` and `preview-dark.svg` from the same PDF, keeping
geometry and typography identical. Glyphs are vector paths, so viewing does not
require the drawing's fonts. Both backgrounds are transparent; only ink changes.
The helper handles monochrome figures and rejects raster content or additional
colors that need a deliberate mapping. By default it does not alter LaTeX or PNG files.

For preference examples, add `--stem good` (or `bad`) to name the SVG pair,
and `--png` to explicitly write its matching transparent PNG. Add `--page 1`
or `--page 2` when one source contains multiple example pages. For example:

```text
python scripts/export_svg.py build/power-supply-arrows/drawing.pdf preferences/symbols/power-supply-arrows --page 1 --stem good --png --title "Power supply arrow symbols" --description "Positive and negative supply connections use arrows."
```

Without these options, existing single-figure exports behave as before.

## GitHub

Use paired links with GitHub's theme fragments on **the link destinations**:

```html
<a href="preview-light.svg#gh-light-mode-only"><img src="preview-light.svg" alt="Description" width="660"></a>
<a href="preview-dark.svg#gh-dark-mode-only"><img src="preview-dark.svg" alt="Description" width="660"></a>
```

In a gallery, replace the link destinations with the example folder, retaining
the corresponding fragment. Keep ordinary SVG and PNG download links below.
GitHub's current theme-fragment selectors follow its selected site theme,
including automatic mode. A `picture` source using `prefers-color-scheme` alone
can follow the system preference when the user selected a different site theme.
Check the live site when changing this convention. Other Markdown viewers may
show both variants; the explicit download links remain usable.

## Chat

Embed the vector drawing in the chat's supported inline presentation surface,
using transparent backgrounds and `currentColor` for ink inherited from the
host's foreground. Preserve `fill="none"` on open paths and namespace SVG IDs
when combining figures. Do not silently replace it with a PNG. If a chat client
cannot display inline SVG, explain the limitation and provide the SVG file;
use a raster preview only as an identified fallback or at the user's request.

## Check before delivery

- Compare the exported geometry and captions with the compiled source.
- Inspect every changed figure in light and dark presentation: readable ink,
  transparent background, intact labels, and no missing or clipped content.
- On GitHub, check both explicit site themes and confirm one variant is visible,
  including a site theme that differs from the system preference.
- Check gallery/example navigation, SVG downloads, and retained PNGs.
- For a presentation-only change, verify source and PNG hashes remain unchanged.
- Review inline chat output in both themes before showing it to the user.
