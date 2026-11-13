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
Export one SVG or the whole catalog at the chosen size/stroke; search does not
reduce the exported library. Export selection/cart, Add configuration and in-app creation
are outside the current viewer.

## Future integration

The broader direction includes agentic creation, personal variants, schematic
styles and in-circuit comparison. Shipped symbols remain separate from user work.
MCP/host connections and a persistent create/save/reuse journey are missing;
formats, profiles, grouping and host support remain open. See the
[scope checklist](../docs/ROADMAP.md) before planning a next implementation.

## Resistor batch and review — 13-11-2026

The user authorized a complete finite resistor batch, compact verification controls,
tests/docs, commit/push and deployment to the existing preview. The established
[inventory](../docs/RESISTOR_BATCH.md) has 24 resistor designs: two reused and 22 new.
The six-symbol catalog limit is superseded; complete-library export now covers 28.

Official acceptance is published metadata tied to all nine drawings and semantic
connections. Browser checkboxes store only pending local approvals, copied into
chat for validated application and publication. New designs remain Unverified;
technical success is not human approval. Undo affects pending selections only.
Geometry/connection changes invalidate approval; editorial corrections do not.
Changes and fixes stay in chat, without review sheets or comment fields.

Near-term directions explicitly include accounts/preferences/custom designs,
admin maintenance of supplied originals, separate personal variants, and an
agent-integrated creation skill. None is implemented in this run. Batch production
and future interactive creation share drawing formats/tools and validation while
remaining separate workflows. The broader milestone order is still open.

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
