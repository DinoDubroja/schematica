# Figure presentation

[Chat behavior](../agents/BEHAVIOR.md#presenting-illustrations) defines the default:
show illustrations and visual comparisons directly in the conversation. Use the
[chat procedure](#chat) unless the user requests a different format or destination.

For generated/recreated drawings, LaTeX is the editable source and SVG is the
default vector display format. When saving an example or preference is authorized,
keep its source, transparent light/dark SVGs and a convenient PNG download together.
The export and GitHub sections below apply to that authorized save or an explicit
export request; a chat preview does not automatically create a permanent example.
Original reference images have their own supported path below. Captions stay with
saved figures and as readable, attributed text in their records.

## Original reference images

Save an authorized source image unchanged as `reference.png`, retaining its actual
format/extension if different. Preserve the supplied background and caption; do
not crop, invert, remove the background, or convert it just to enter the gallery.
An original PNG with its white background is valid on both site themes. It is a
complete reference image, not an SVG fallback or an unfinished recreation.

Use a linked image on its example page, with accessible alt text and a suitable
display width; the link opens the full-resolution original:

```html
<a href="reference.png"><img src="reference.png" alt="Three-op-amp instrumentation amplifier, Figure 5.77." width="840"></a>
```

In a category gallery, link the image to the example page instead. Preserve the
source attribution and readable caption there, with a download and navigation.
Do not feed the raster through `export_svg.py` or wrap it in a nominal SVG.
Optional theme variants are separate derived files, only when requested; retain
the original. A later recreation adds the vector assets below without replacing
the reference image. Do not require every reference to have a recreation.

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

### Choose the delivery

1. Honor an explicit output format or destination. Otherwise, deliver the visual
   in chat without requiring the user to ask for a preview or open a downloaded file.
2. Use the host's native inline visualization capability when available. Read its
   current rendering instructions and use its supported surface for embedded SVG,
   labels and any useful controls. Do not depend on a private plugin path or assume
   that every chat client supports the same renderer.
3. Keep temporary source, exports and presentation fragments in the task's allowed
   working area, outside accepted galleries. These support rendering the response;
   do not commit them or add permanent examples/preferences unless authorized.
4. During discussion, show the proposed result, accept corrections and update the
   in-chat preview. Preserve the distinction between liking the appearance and
   authorizing implementation. Continue an already authorized save within its scope
   without asking for the same permission again.

### Render the preview

- Reuse the selected drawing's vector geometry from its editable source. For
  LaTeX-based figures, compile and export as above into the working area. Keep the
  preview faithful to the source and the applicable schematic preferences.
- Embed SVG with a transparent background and `currentColor` for schematic ink
  inherited from the host's foreground. Preserve `fill="none"` on open paths and
  namespace SVG IDs when combining figures. Use the host's theme-aware colors for
  surrounding labels and meaningful highlights; do not hardcode a light background.
- Keep the surrounding presentation compact and unframed, with concise readable
  labels and little explanatory text. Use native text for comparison labels when
  possible, so they remain readable as the conversation width changes.
- For Good/Bad comparisons, use two equal columns: green Good on the left and red
  Bad on the right, with no checkmark/cross icons. Put accepted variants side by
  side inside the Good cell, label each beneath its drawing and mark the default.
  Match drawing scale across the comparison. Do not enlarge a single Bad drawing
  merely to fill its cell. Follow the same grouping in an authorized saved gallery;
  see [the gallery authoring contract](../agents/PROJECT_RULES.md#deterministic-gallery-generation).
- Use neutral labels for alternatives the user has not judged. Add controls only
  when they help explore a meaningful choice; a static comparison needs none.
- Adapt to the available conversation width without clipped labels or misleading
  scale changes. Keep the relationship between grouped alternatives and Good/Bad
  clear when a narrow display requires reflow.

If the host cannot render the native inline view, explain that specific limitation
and use the closest supported preview. Prefer an inline vector view where possible;
identify a raster fallback when necessary. Offer a file link only when needed or
requested, rather than silently replacing the default in-chat experience.

## Check before delivery

- For an imported reference, compare the saved bytes with the supplied original,
  inspect image identity/caption, and verify readable presentation on both backgrounds.
  If the original is inaccessible, retain a clearly labeled text record; do not
  add a broken image link or claim the import or visual review succeeded.
- For generated/recreated drawings, compare exported geometry and captions with the compiled source.
- Inspect every changed figure in light and dark presentation: readable ink,
  transparent background, intact labels, and no missing or clipped content.
- On GitHub, check both explicit site themes and confirm one variant is visible,
  including a site theme that differs from the system preference.
- Check gallery/example navigation, SVG downloads, and retained PNGs.
- For a presentation-only change, verify source and PNG hashes remain unchanged.
- Review inline chat output in both themes before showing it to the user. Check
  labels, comparison grouping, equal drawing scale and fit at the intended width;
  verify any controls actually update the relevant visual. Report a check as
  unverified if the host does not expose a way to perform it.
