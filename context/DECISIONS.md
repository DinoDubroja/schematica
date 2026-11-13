# New-project decisions

## Symbols and rendering

Confirmed in the first-batch requirements and accepted rendering review: six
appearances, three proportional sizes, three independent strokes, 1 mm connection
grid and stable semantic pins. TeX recipes are authoritative; Python packages their
converter output. The accepted palette supersedes older blanket wire-relative
normalization. The three-pin op-amp makes no hidden-supply electrical promise.

## Browser and exports

Confirmed by the user's later UI review: browsing and later customization are the
purpose. Keep controls and text minimal, dark/light mode functional, and connection
points visible. Read-only description/keywords replace technical accordions.
Export one SVG or all six appearances at the chosen size/stroke; search does not
reduce the exported library. Selection/cart, Add configuration and in-app creation
are outside the current viewer.

## Future integration

The broader direction includes agentic creation, personal variants, schematic
styles and in-circuit comparison. Shipped symbols remain separate from user work.
MCP/host connections and a persistent create/save/reuse journey are missing;
formats, profiles, grouping and host support remain open. See the
[scope checklist](../docs/ROADMAP.md) before planning a next implementation.

## Repository separation — 13-11-2026

The user explicitly authorized a local cleanup: new Schematica only in the active
checkout, old work preserved outside it, no inherited legacy reading routes, no
feature additions or accepted-UI changes. Keep Git history. Generate duplicated
TeX bundles/ZIPs when packaging, retain essential regression inputs, and provide
useful human developer instructions after every implementation run.

After reviewing the cleanup, the user explicitly authorized committing and pushing
it to GitHub. This releases the cleanup's source-publication hold; it does not add
feature work or a new website deployment. Source synchronization and website
deployment remain separate actions.
