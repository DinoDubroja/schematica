# Review: hosted symbol library

13-11-2026 · Build **971b3b876b93** · **Web preview and completed source published.**

[Open the preview](https://schematica-preview.dinodubroja.workers.dev/)
· [Fixed review version](https://650191bd-schematica-preview.dinodubroja.workers.dev/)

This run published the accepted website unchanged through Cloudflare's static-file
upload. No account is needed to view it. Both links were checked in a Windows browser.

Repository handoff: the completed batch is published on [GitHub main](https://github.com/DinoDubroja/schematica).
Source commit `4b76d70` was checked through GitHub: all 853 repository files matched
the local commit, including 54 SVGs, 54 TeX bundles, the viewer and these guides.
The README now links [laptop setup and update steps](DEVELOPMENT.md#get-the-project-on-another-windows-device).
Saved measurement reports use portable, relative artifact paths. The viewer and
published artwork are unchanged. After obtaining the repository on the laptop,
expect `implementation/README.md`, these instructions and all 54 SVG/TeX bundles;
follow the local setup/build checks in DEVELOPMENT.md, then the checklist below.

## What changed

- Browsing comes first: symbol-and-name cards, search, filters and a clean preview.
  Removed slogans, counts, export selection, Add configuration and technical panels.
- Larger blue connection points; read-only Description and Keywords; working
  dark/light mode. Presets update the preview and all card thumbnails together.
- A discreet icon exports one SVG. Export library downloads all six symbols at
  the chosen size/stroke, even while search or filters are active. Each library
  title identifies its preset. No selection workflow.
- A portable static website replaces the runtime export service. Cloudflare
  configuration and a website ZIP support manual publication. README, developer and Inkscape
  instructions are separated and kept short. Future runs must update this review.

Accepted symbol geometry is unchanged. Descriptions/keywords were made readable;
all 54 SVG descriptions were refreshed through the existing renderer.

## Open and check it — about 10 minutes

Open the fixed review version above on **each Windows device**. No local setup is
needed. For local development, run `./launch.ps1` from `implementation` and open
http://127.0.0.1:8765/. Setup and port alternatives are in
[DEVELOPMENT.md](DEVELOPMENT.md#open-the-viewer-on-windows).

1. **Browse:** expect six cards containing only a drawing and name. Select an
   op-amp: its name and preview must change. There should be no export cart,
   Add configuration button, slogans, revision or configuration counts.
2. **Theme:** use the sun/moon button, reload, then switch back and reload again.
   Both choices should persist. Artwork, grid, blue points and controls must remain
   readable in both themes. Only the theme is saved; presets reset to Medium.
3. **Search:** type `elliptical` — expect only Coil inductor. Type `zzzz` — expect
   “No matching symbols.” Clear search; Passive shows four cards, Amplifiers two,
   All six. Description keywords are searchable.
4. **Presets:** choose Coil inductor, Small, Thick. Size changes geometry; stroke
   changes line weight without moving pins. Card thumbnails follow the same presets.
   Toggle Grid & pins off: both grid and blue points disappear, artwork remains.
   Expand Description: useful text and keywords, with no editable fields.
5. **Single export:** click the download icon beside the symbol name. Expect
   `inductor-coil-small-thick.svg`. Open in Inkscape: black vector artwork, no grid
   or blue points. Its visual bounding box is **14.30 × 1.80 mm**, including stroke;
   terminal centres are 14 mm apart. The page includes extra margins.
6. **Library export:** while still Small/Thick, search for `capacitor` and choose
   Export library. Expect “6 symbols · Small · Thick”, not a filtered subset.
   Download `schematica-small-thick.svg`. In Inkscape, Symbols → Current document
   must show **six** symbols. Paste a thumbnail into a new drawing, unlink it and
   inspect the named parts. Save/reopen. Follow [INKSCAPE.md](INKSCAPE.md) for exact
   menus, grid setup and the difference between stroke edges and terminal centres.
7. **Keyboard/layout:** Tab through controls; Enter activates a card or download;
   Escape closes the export dialog and returns focus to Export library. `/` focuses
   search when not typing. Narrow the window: cards and controls must fit without
   horizontal scrolling; selecting a card brings its preview into view.

Repeat these steps on both Windows devices using the same fixed preview URL.
[Build information](https://650191bd-schematica-preview.dinodubroja.workers.dev/build.json)
must show `971b3b876b93` on both. Report the device/browser, failed step, chosen
preset and what happened instead; include a screenshot if useful.

## Checks completed

- **Hosted preview verified:** main and fixed-version build manifests match the
  reviewed local build. Both themes survived reload; keyword/empty search,
  descriptions and all nine size/stroke choices worked. Nine library downloads
  and one single SVG matched the local files byte for byte. Search filtering still
  exported all six symbols. No browser console warnings/errors were observed.
- **25 automated tests passed.** A fresh checkout of the exact staged Git files
  reproduced hosted build `971b3b876b93` (71 files, 54 individual SVGs and nine
  six-symbol libraries), without the original build cache or absolute report paths.
  All 210 local links in the changed documentation resolve; the review ZIP passes
  its file/hash manifest check. Git preserves source/export bytes on Windows.
- **54 browser configurations checked**, plus search, filters, grid toggle,
  description, keyboard navigation, dialog focus and both persisted themes.
  Narrow/desktop layouts had no horizontal overflow. No browser console warnings
  or errors were observed in the Codex in-app browser on Windows.
- **Nine actual library downloads and one individual SVG matched the build.**
  All nine libraries survived Inkscape save/reopen with six symbols, named parts,
  valid references, correct physical page dimensions and no clipping.
- **All 54 individual renderings passed** the accepted-palette checks again.
  The final Small/Thick library showed six entries in Inkscape 1.3.2. Its coil was
  pasted into a fresh document at 14.30 × 1.80 mm, unlinked and saved. Reopening
  through Inkscape's command line retained the body and both named leads.
- Launcher, documentation links and existing preference-gallery checks passed.

**Not yet verified:** the second physical Windows device, Chrome/Edge separately,
profile-wide Symbols installation, or a
fresh GUI grid-snapping walkthrough. Use the checklist above for those reviews.

The initial HTTPS activation error cleared during this run. Cloudflare rejected
the Python HTTP checker with 403/error 1010; its complete remote-file and response-
header sweep did not run. Browser access and the actual downloads passed without
changing security settings.

- [Hosted verification](review/hosted-verification.json) · [Published screenshot](review/viewer-hosted.png)
- [Browser and GUI results](review/viewer-checks.json)
- [Static libraries, file hashes and Inkscape checks](review/site-verification.json)
- [Accepted geometry, all 54 renderings and save/reopen](review/library-verification.json)
- [Dark screenshot](review/viewer-clean-dark.jpg) · [Light screenshot](review/viewer-clean-light.jpg)
- [Narrow layout](review/viewer-clean-narrow.jpg) · [Complete rendering proof](review/library-proof.png)
- [Portable website ZIP](review/web-preview.zip)

## Review boundary and known limits

The user accepted the browsing layout and authorized both this public preview and
the completed batch's commit/push. Await their two-device test results. User-created variants, schematic styles, in-circuit
comparisons, agent connections and an editor are outside this implementation.

Inkscape can wrap labels at its smallest thumbnail size; increase the Symbols
preview size if needed. A placed clone must be unlinked before editing internal
parts. SVG edits do not update TeX/YAML. Browser storage restrictions can prevent
remembering a theme, while the switch itself continues to work.

Earlier rendering-proof, editable-text and placement evidence is retained in
[the previous checkpoint](review/first-batch-checkpoint.md). Those historical checks
do not stand in for a new second-device or hosted test.
