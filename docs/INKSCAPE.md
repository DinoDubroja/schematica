# Inkscape quick start

## Use one symbol

1. In Schematica, choose a symbol, size and stroke. Click the download icon beside
   its name.
2. Open the SVG in Inkscape, or use **File → Import** in your drawing. Keep its
   original scale; use the selected preset rather than resizing to change stroke.
3. Open **Object → Layers and Objects** (`Ctrl+Shift+L`). Expand the symbol group
   to select a named body, lead, plate or sign. Save as Inkscape SVG.

Expect black artwork on a transparent background, with no blue markers or grid.
Dark mode affects the browser preview only. File dimensions are in millimetres;
the export canvas includes a 1 mm margin around the artwork.

## Use the Symbols panel

1. Choose size and stroke, then **Export library → Download SVG**. The file contains
   all six symbols at those settings, regardless of the search/filter.
2. Open the downloaded file in Inkscape. Open **Object → Symbols** (`Ctrl+Shift+Y`)
   and select **Current document**. Expect six thumbnails.
3. Click a thumbnail to copy it. Create or switch to your drawing, click its canvas
   and paste (`Ctrl+V`). Do not press Ctrl+C on an empty canvas: that can replace the
   symbol clipboard. Dragging a thumbnail onto the current document also works.
4. To edit the internal parts, select the placed symbol and use
   **Edit → Clone → Unlink Clone** (`Shift+Alt+D`). Expand it in Layers and Objects.
5. Save and reopen. The artwork and named parts should remain intact.

For a reusable installed set, open **Edit → Preferences → System** and locate the
user configuration folder. Copy the library SVG into its `symbols` subfolder
(create that subfolder if needed), restart Inkscape, then choose the library in
Symbols. Use this displayed location instead of assuming a Windows profile path.
[Inkscape's Symbols guide](https://wiki.inkscape.org/wiki/SymbolsDialog).

## Set a 1 mm grid

1. In your drawing, open **File → Document Properties** (`Ctrl+Shift+D`), then **Grids**.
2. Add a **Rectangular grid**. Set grid units to **mm**, X/Y spacing to **1**, and
   X/Y origin to **0**. Set a major grid line every **5** lines if useful.
3. Show the grid from **View → Page Grid**. Enable snapping, grids and cusp nodes
   in the snapping controls. Avoid bounding-box snapping for electrical terminals:
   stroke edges do not coincide with the path endpoints.
4. Unlink a placed symbol if needed. Align one lead endpoint to a grid intersection
   using node snapping; keep the symbol's scale unchanged. Its other endpoints
   should then lie on the grid. Draw connections from endpoint to endpoint.

A pasted symbol can initially land between grid points. The viewer's blue points
are preview aids, not exported objects or automatic electrical connections.
Inkscape 1.3 uses a grid dropdown and **New**; 1.4 uses grid-type buttons.
[Grid controls in Inkscape 1.4](https://wiki.inkscape.org/wiki/Release_notes/1.4#Grids).

Quick scale check: the **Small / Thick coil** has a 14 mm distance between terminal
centres and a **14.30 × 1.80 mm** visual bounding box including stroke. Choose visual
bounding boxes in Inkscape's selector preferences before comparing that measurement.
