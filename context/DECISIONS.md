# New-project decisions

Source times identify when a discussion/decision occurred; review dates identify
when it was reconciled. Times use Europe/Zagreb with an explicit UTC offset.
Later applicable user decisions supersede earlier proposals; a newer import date
does not. See [current status](CURRENT.md) for the implementation checkpoint.

## Symbols and rendering

Sources: **Brainstorm A**, 13-11-2026 01:17 +01:00 (palette);
**Agent B** (then Agent A), 13-11-2026 01:56 and 11:54 +01:00
(first-batch request and rendering-proof acceptance).

Confirmed in the first-batch requirements and accepted rendering review: six
appearances, three proportional sizes, three independent strokes, 1 mm connection
grid and stable semantic pins. TeX recipes are authoritative; Python packages their
converter output. The accepted palette supersedes older blanket wire-relative
normalization. The three-pin op-amp makes no hidden-supply electrical promise.

## Browser and exports

Sources: **Agent B** (then Agent A), 13-11-2026 12:44–13:11 +01:00
(UI review and authorization). Later batch scope supersedes the six-symbol limit.

Confirmed by the user's later UI review: browsing and later customization are the
purpose. Keep controls and text minimal, dark/light mode functional, and connection
points visible. Read-only description/keywords replace technical accordions.
Export one SVG or the whole catalog at the chosen size/stroke; search does not
reduce the exported library. Export selection/cart, Add configuration and in-app creation
are outside the current viewer.

## Future integration

The broader direction includes agentic creation/search, schematic styles and
in-circuit comparison. The latest planning scope uses a dev library, with personal
libraries and accounts deferred. Required hosts are now specified; their actual
support, transport/storage and the detailed retrieval contract remain unverified.
See [dated creation/search decisions](#individual-creation-and-search-skills),
[release scope](#development-library-release-and-host-requirements) and the
[roadmap](../docs/ROADMAP.md) before proposing implementation.

## Resistor batch and review — 13-11-2026

Sources: **Brainstorm B (cloud)**, 13-11-2026 18:04–18:42 +01:00
(decisions); **Agent B**, 13-11-2026 18:48 +01:00 (implementation request).

The user authorized a complete finite resistor batch, compact verification controls,
tests/docs, commit/push and deployment to the existing preview. The established
[inventory](../docs/RESISTOR_BATCH.md) has 24 resistor designs: two reused and 22 new.
The six-symbol catalog limit is superseded; complete-library export now covers 28.

Official acceptance is published metadata tied to all supported drawings and semantic
connections. Browser checkboxes store only pending local approvals, copied into
chat for validated application and publication. New designs remain Unverified;
technical success is not human approval. Undo affects pending selections only.
Geometry/connection changes invalidate approval; editorial corrections do not.
Changes and fixes stay in chat, without review sheets or comment fields.

At that time, near-term directions included accounts/preferences/custom designs,
admin maintenance of supplied originals, separate personal variants, and an
agent-integrated creation skill. None is implemented in this run. Batch production
and future interactive creation share drawing formats/tools and validation while
remaining separate workflows. The precise delivery order is still open; the later
dev-library-first decision below defers accounts/personal libraries from the immediate creation prototype.

## Resistor corrections and Variations — 14-11-2026

Decision sources: **Brainstorm B (cloud)**, 13-11-2026 23:11–23:40 +01:00;
implementation authorization: **Agent B**, 13-11-2026 23:51 +01:00.
The heading dates the implementation checkpoint, not a new approval.

The user authorized implementation, checks, documentation, commit/push and the
existing preview deployment. The [reference guide](../docs/SYMBOL_REFERENCE.md)
was established before drawing changes; later batches must reuse it. Detailed
IEC/ISO records were inaccessible, so no unreviewed compliance claim is made.

Centered vertical potentiometer wipers, with tips 1 mm above the body, supersede
the earlier angled US wiper. Fixed taps are unchanged. NTC/PTC lettering replaces
the temperature signs; shared symmetric light arrows replace the asymmetric form.
Varistors leave the active catalog; the user-confirmed diagonal S-marked nonlinear
resistors replace them. No arrowhead is used on the S marking.

Four orientations apply only to the diagonal variable/trimmer marking; body and
pin identities stay fixed. Definitions declare options/defaults. There are now
28 designs and 360 configurations. Complete-library exports use the selected
orientation when applicable, otherwise Up-right; single exports use the exact
selected configuration. Search never reduces library exports.

The compact **Variations** window supersedes 3 × 3. Stroke, Size and applicable
option rows each vary only that setting, holding the rest at defaults and using a
common scale. Representative refinement and related-family visual checks precede
production; technical checks cover the full Cartesian product. Changed designs
require new human review; unaffected approvals survive. Creation skills and
account/profile features remain outside this run.

## Repository separation — 13-11-2026

Sources: **Agent B** (then Agent A), 13-11-2026 15:46 +01:00
(cleanup request) and 16:23 +01:00 (commit/push approval).

The user explicitly authorized a local cleanup: new Schematica only in the active
checkout, old work preserved outside it, no inherited legacy reading routes, no
feature additions or accepted-UI changes. Keep Git history. Generate duplicated
TeX bundles/ZIPs when packaging, retain essential regression inputs, and provide
useful human developer instructions after every implementation run.

After reviewing the cleanup, the user explicitly authorized committing and pushing
it to GitHub. This releases the cleanup's source-publication hold; it does not add
feature work or a new website deployment. Source synchronization and website
deployment remain separate actions.

## Product direction recovered from chats

Times below are source turn-start times in Europe/Zagreb (UTC+01:00 in
November), not the time these notes were imported. A follow-up within the same
turn may be later; a separate message timestamp is not always exposed. These
are summaries of user statements unless explicitly marked as assistant proposals.
The 14-11-2026 backfill does not make older decisions new or authorize features.

### Purpose and future schematic creation

**Confirmed direction; future implementation.** Schematica should let an agent
produce useful, beautiful electronic schematics and system/block diagrams from
the first prompt, with useful defaults rather than a blank preference setup.
Engineering documentation, teaching, papers and discussion all matter. Realistic
subsystems should demonstrate the benefit through the same prompt with and
without Schematica; simple toy drawings alone are insufficient.

Sources: **Design template creation skill**, 07-11-2026 19:33, 19:42–19:45 and
22:50 +01:00; **Brainstorm**, 11-11-2026 21:03 +01:00.

**Confirmed future inputs:** text, photographs, screenshots, PDFs and hand-drawn
sketches. The priority hand-drawing experience means photographs of paper and
drawing-tablet exports, not drawing inside a Schematica canvas. For complete
schematics, identify existing symbols, create missing ones when needed, refine
placement/connections/labels, and offer useful saves. Preserve semantic
connections while improving appearance. General CircuitikZ import and
round-tripping remain desired later, not implemented.

Source: **Brainstorm A**, 12-11-2026 00:54 +01:00. Its clarification at
01:06 +01:00 explicitly kept the first implementation focused on the symbol
library/viewer. That superseded the assistant's proposed sketch-first first batch,
not the long-term sketch goal. SPICE, sourcing and later simulation integration
remain deferred (**Brainstorm**, 11-11-2026 evening discussion).

### Reusable symbols and semantic identity

**Agreed design direction.** Use reusable library symbols and placements inside
a drawing; an R1 placement need not be a separate file. Stable identifiers coexist
with simple readable names, searchable types/attributes and descriptions. Avoid
encoding every preset in a human-facing name. Symbols and pins need contextual
descriptions, so an agent can identify a non-inverting input regardless of rotation.
Graphical parts and electrical pins have distinct identities; meaningful part
names should remain traceable through YAML, TeX and SVG.

Sources: **Brainstorm A**, 11-11-2026 22:35–23:15 and
12-11-2026 00:18–00:25 +01:00. Illustrative schemas/helper names from that chat
are proposals; current implementation files define actual interfaces. The accepted
13-11-2026 01:17 +01:00 palette supersedes the earlier blanket wire-normalization
rule and earlier fixed-pins-across-every-size illustrations.

### Individual creation and search skills

**Confirmed planning direction; not implementation authorization.** The individual
symbol-creation skill is separate from batch library filling. It creates one new
symbol from text, an image/screenshot, a sketch, or combined input; PDF input is
also retained from the 12-11-2026 discussion. Both a download and a save visible
in the web library are wanted. A workflow is the reusable sequence; a skill is
its integration into an agent environment.

Sources: **Brainstorm B (cloud)**, 13-11-2026 17:53 and 18:10 +01:00;
**Brainstorm A (cloud)**, 13-11-2026 23:29–23:32 +01:00
(including earlier messages recovered from its cloud backing history).

The requested creation sequence is:

1. Understand the intended meaning and each graphical element, rather than trace
   an image pixel for pixel. Present the interpretation and uncertainties.
2. Ask for confirmation and necessary information before creating.
3. Create and check the symbol, then show an actual rendered preview.
4. Invite refinement and propose two meaningful design changes.
5. Offer to save with a proposed name/category and useful discovery information.

Sources: **Brainstorm A (cloud)**, 14-11-2026 00:06 and 00:22 +01:00.
Visual annotations of a supplied image are approved where useful. Ask for a short
textual description when missing; do not silently guess the intended symbol.
Size and stroke apply to all symbols. User-defined symbol options should be
possible for new and existing symbols. Exact option-definition UI, validation
contract and recoverable version mechanism remain to be designed.

**Search skill requested:** retrieve existing symbols separately from creation.
The user proposed a prewritten interactive viewer shared with the website so the
agent need not generate a new UI for each search (**Brainstorm A (cloud)**,
13-11-2026 23:50 +01:00). Shared code is the preferred proposal, not a verified
host capability. The assistant proposed filtered results, Browse all, preview,
Variations, SVG download and a Use this symbol action returning identity,
revision/configuration and a file reference. Those exact interaction contracts
remain open, including whether even a single match always opens the viewer.

### Development library, release and host requirements

**Latest confirmed scope:** call the current working collection the **dev library**.
Do not introduce personal libraries or user accounts yet. This is planning
terminology, not a catalog-schema migration. On the first release, select and validate material from the dev library to build the first Schematica
default library. Custom options may apply to both new and existing symbols.

Source: **Brainstorm A (cloud)**, 14-11-2026 00:22 +01:00. This supersedes the
13-11-2026 23:32 +01:00 personal-library wording for the immediate creation
prototype and the assistant's account-linking-first proposal. Download and
library-save outcomes remain; the immediate save destination is the dev library.
Future accounts, user-owned variants and admin control of supplied originals
remain desired, as stated in **Brainstorm B (cloud)**,
13-11-2026 18:32 +01:00.

**Required first-version hosts:** ChatGPT Desktop across its environments and
Claude Desktop (**Brainstorm A (cloud)**, 13-11-2026 23:37 +01:00). Test the
actual required surfaces individually, including local/cloud agent environments
where applicable. Ordinary ChatGPT use must not be silently replaced by an
API-only or Codex-only demonstration. Installation, visible previews, downloads,
persistence and fresh-chat retrieval still need end-to-end evidence. The historical
first-release Page also calls for newcomer tests without private instructions or
unlisted developer setup; that clean-environment demonstration remains unverified.

The older readiness check in **Brainstorm B**, 11-11-2026 22:13 +01:00, was
incomplete. No live Schematica host connection was established there. Local versus
hosted transport, hosting/storage, authentication and packaging remain open.
The older first-release Page and MCP transition branch (09–11-11-2026) are
historical: their host-first sequencing, old ground-symbol prototype and test-user
personal library are superseded by the new implementation and later scope above.

**Assistant proposals still open:** keep core/rendering independent of MCP,
expose distinct find/inspect/preview/save actions, return structured versioned
identifiers, persist useful state outside chats, separate preview from save,
protect originals and handle retries/conflicts, provide matching visual/data
results, and test complete journeys in each host.
Source: **Brainstorm B**, 12-11-2026 00:29 +01:00.
These are design candidates, not implemented guarantees.

### Future styles and examples retained from earlier work

**Historical direction, deferred for new Schematica.** The Art of Electronics
collection was intended to cover circuit, plot, equation/writing and mixed
illustrations. Retain captions and specific user feedback; distinguish inferred
style patterns from approved preferences. A good synthetic-example loop would
render a new realistic case, refine it, and offer to save an approved result with
its prompt and useful corrections. Difference-only revision storage was only an
idea, not a decision.

Sources: **Recover Schematica project context**, 07-11-2026 23:07–23:27
and 08-11-2026 00:27 +01:00; **Restructure styles and examples**,
08-11-2026 16:19–16:22 +01:00.

**Later historical correction:** original screenshots plus captions can be complete
references without LaTeX recreation. Use selected favorites for polished SVG
showcases, with all references visibly browsable deeper in the collection.
This superseded the earlier assumption that originals were merely temporary.
Source: **Continue AOE Style**, 08-11-2026 16:24–16:59 +01:00
(including cloud backing history). The explicit 16:33 instruction was to avoid
inferring style generalizations then. The 09-11-2026 13:16 +01:00
**Schematica Progress Check-in** reported 31 records but only five rendered
examples; a validated numeric style and generalization tests were unfinished.
Archiving did not turn those unfinished goals into completed features.

**Archived rules, not current defaults:** old terminal/junction/ground dimensions,
0.65 pt wires, EU-as-default preference, the old preference-bank structure and
installed preference skill belong to old Schematica. The historical values
included 10× junction dots, 12× terminal circles and 25× ground width, with explicit
junctions, straight crossings by default and optional wire bridges.
Sources: **Update color and junction preferences**, 08-11-2026
16:25–18:49 +01:00; **Define passive symbol preferences**,
08-11-2026 18:39–19:18 +01:00. The 13-11-2026 cleanup and accepted palette
supersede automatic application of that collection. Consult it only for deliberate
reuse. Green Good/red Bad, equal-scale alternatives and minimal labels remain
historical presentation feedback, not an instruction to redesign today's viewer.

Earlier schematic-trial feedback emphasized paired differential routing, functional
blocks with visible external supply connections, titles outside circuitry, useful
rather than forced equal box sizes, and explicit overlap checks. The requested
0.8 pt trial stroke and particular title position were example edits, not universal
defaults. Sources: **Design template creation skill**, 07-11-2026
18:07–18:29 +01:00. Mixed circuit-and-waveform examples were explicitly welcomed
(**Recover Schematica project context**, 07-11-2026 23:20–23:22 +01:00).

Graphical CircuitikZ editing and tools such as VisioCirkit were researched in
**Explain Circuitikz workflow** (07-11-2026 23:35 +01:00) and
**Explore Graphical Editing Integration / Explore Integration Solutions**
(08-11-2026 13:15–13:19 +01:00). They remain candidate integrations requiring
fresh evaluation; no editor or round-trip capability was adopted by those reports.

### Chat roles, timestamps and synchronization

**Confirmed working arrangement:** cloud Brainstorm chats hold discussion;
Prompt Generator chats assemble scoped briefs; local Agent chats implement.
Shared repository notes bridge devices. The same chat may be renamed, so use
stable source IDs when tracking history. Sources: **Brainstorm A / Brainstorm B /
Prompt Generator A**, 11-11-2026 evening; **Continue Schematica Across Devices**,
13-11-2026 12:29–12:32 +01:00.

The user requested removal of the blanket “stop before committing/publishing”
sentence from future implementation prompts (**Brainstorm A (cloud)**,
13-11-2026 15:43 +01:00). Honor the actual scope of each task; that correction
alone does not authorize unrelated publication. After a project push, provide a
ready-to-paste laptop-agent update/check prompt (**Agent B**, formerly Agent A,
13-11-2026 16:35 +01:00).

**Authorized context maintenance:** the hourly Schematica task may update context,
commit eligible reviewed work and safely synchronize the named GitHub repository
(**Brainstorm B**, 13-11-2026 12:21–12:29 +01:00).
The **Sync** turn at 14-11-2026 00:28 +01:00 explicitly authorized repairing
the automation, backfilling relevant local/cloud chats, preserving ongoing work
and verifying synchronization; its follow-up requires source timestamps.

Review actual new messages even when Git is clean. Track discovery, reviewed
turns, pending topics, incorporated commits and verified remote commits separately.
Defer shared writes during active editing while retaining pending context locally.
State chat coverage and repository synchronization separately. Saving on this PC
or pushing to GitHub does not prove that the laptop has updated. Newer source
evidence supersedes older notes explicitly; review time must never masquerade as
a new decision date.
