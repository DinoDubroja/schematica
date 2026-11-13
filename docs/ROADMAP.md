# Scope and remaining work

The current product is a reusable symbol core and a read-only symbol browser.
Its accepted UI is the foundation for later customization and schematic styles.

## Requirement checklist

| Status | Requirement | Evidence or gap |
|---|---|---|
| Implemented | Six appearances, 54 preset configurations | Six YAML definitions; 54 SVGs; three sizes × three strokes |
| Implemented | Independent geometry/stroke, 1 mm connections | TeX recipes and grid/path regression checks |
| Implemented | TeX → XDV/dvisvgm → shallow named SVG parts | Shared renderer; part/reference validation; Inkscape checks |
| Implemented | Responsive catalog, search, preview grid, dark/light | Accepted static viewer; persisted theme |
| Implemented | Single SVG and six-symbol library at chosen presets | Minimal viewer actions; nine Inkscape libraries |
| Implemented | ZIP and arranged sheets with column/spacing parameters | Core export API; intentionally absent from the simplified UI |
| Implemented | Standalone TeX with helpers and named connections | Generated when rendering/packaging; native CircuitikZ fixture |
| Implemented | Windows guides and public shared preview | Developer/Inkscape guides; Cloudflare build 971b3b876b93 |
| Partial | Editable text | A bounded label fixture preserves literal text; no general mathematical-text round trip |
| Partial | Two-device readiness | Desktop cleanup checks pass; earlier laptop setup/focused tests reported; updated laptop and full hosted/GUI checklist pending |
| Partial | Reproducible rendering setup | Versions and overrides documented; clean-machine/offline TeX setup not demonstrated |
| Missing | MCP interface and verified Claude/OpenAI host connections | Python core exists; no MCP server, transport, authentication or demonstrated host journey |
| Missing | Persistent personal variants and ownership separation | No user storage, create/save/reuse journey or upgrade migration |
| Deferred | In-app editing and agentic symbol creation | Future capability; creation should initially use agent integrations |
| Deferred | Schematic styles, examples and in-circuit comparison | Product direction accepted; detailed design and implementation remain open |
| Deferred | Full schematics, routing, sketch/PDF interpretation, simulation and sourcing | Outside the first symbol batch and this cleanup |

“Missing” identifies a gap against the broader integration direction. It does not
mean that the feature was authorized in the first batch or during cleanup.
“Partial” distinguishes a bounded demonstration from general support.

## Confirmed decisions and superseded proposals

- The original first-batch requirements selected six definitions, independent
  presets, the accepted palette, TeX rendering, a browser and four core exports.
- Later user decisions made the browser read-only, removed export selection and
  technical detail panels, and exposed only single SVG and six-symbol library
  export. Descriptions and keywords stay read-only. Dark mode and minimal text are
  required. These changes supersede the earlier inspector/cart design.
- The [MCP transition review](https://github.com/DinoDubroja/schematica/blob/docs/mcp-transition-review/context/MCP_TRANSITION_REVIEW.md)
  recorded the broader integration direction. Its proposed host-first sequence,
  ground-symbol prototype, legacy-gallery migration and wire-relative defaults
  were not the implemented first-batch plan. Numeric grid/presets were decided later.
- Default symbols must remain distinguishable from future user-created versions;
  edits must not overwrite shipped originals. Profiles, grouping, storage and
  supported host surfaces still need design and verification.
- The user reviewed the cleanup and authorized its commit/push. It adds no product
  features; website deployment remains a separate action.

## Archive and deliberate reuse

Old Schematica and obsolete implementation reports are preserved in a verified,
dated archive under the workspace's sibling `Archive/` folder, outside this Git
checkout. It includes Git history, original working files, ignored experiments,
both worktree snapshots and a recovery guide. Git history also remains intact.
The archive is consulted only for a specific reuse task; it is not a reading route
or source of defaults for this app. The local archive is not synchronized by Git.

| Material retained | Reason |
|---|---|
| Accepted palette PDF and its TeX source | Independent geometry/stroke regression reference for this batch |
| Frozen accepted paths for 54 configurations | Detect unintended artwork changes during refactors |
| Named-part, repeated-ID and editable-label fixtures | Exercise real converter and serialization failure modes |
| Native CircuitikZ example | Verify generated helpers and named connection coordinates |

No legacy gallery builder, installer, preference skill, AOE collection or legacy
test is required by the new implementation. The retained fixture provenance is
documented [with the fixtures](../tests/fixtures/README.md).
