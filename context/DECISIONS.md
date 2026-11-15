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

## Approval handoff and nonlinear option B — 14-11-2026

Source: user in **Agent B**, this chat, 14-11-2026 (Europe/Zagreb, UTC+01:00;
original message times were not exposed). The sequence below preserves order,
without substituting recording time for a source timestamp.

- **Confirmed:** the pasted 18-design approval handoff matched exact revisions and
  fingerprints. The original six approvals remain. The user also requested removal
  of both tapped resistors and a less curved nonlinear S.
- **Superseded/rejected:** the first local revision 2 reduced the bend by 29% but
  was rejected as "ugly and discontinuos". The user requested alternatives in chat.
- **Selected and authorized:** "B, implement and push" chose the balanced alternative
  and released the implementation/commit/push hold for these pending fixes. Revision
  3 uses one cubic: at medium size, axial half-length 5.6 mm and lateral controls
  ±3.4 mm at axial coordinates ∓5.6/3 mm, rotated 45°. The renderer matches the chat
  preview across all 18 configurations. Bodies, pins and unrelated artwork stay fixed.

At this earlier checkpoint, the inventory had 26 designs / 342 configurations. Twenty-four designs
have official approval fingerprints; B is the confirmed design choice, while its
new rendered revision 3 still uses the normal verification handoff. No further
shape choice is pending. GitHub synchronization is authorized; Cloudflare deployment
is outside this request. Earlier preview publication permission covered its own run.

**Testing discussion, still proposed:** the user requested less computer use and
asked whether repeated Inkscape exports/tests could be dropped. The proposed
permanent policy keeps exports and focuses checks on affected behavior; a policy
edit is not yet approved. This correction run uses no Inkscape or browser automation.

## Preview publication and completed approvals — 14-11-2026

Source: subsequent user messages in Agent B (original times unavailable):
"Publish the Cloudflare preview too ... Avoid browser automation if possible",
then "Why are verfied componennts still pending, resolve that too".

**Confirmed and completed:** publish the existing B implementation and resolve the
approval status. The 18 pasted approvals must be present on the live site. The
explicit selection of B, followed by the status-correction request, is human
acceptance of the two corrected nonlinear designs; record their exact revision-3
fingerprints rather than require a second browser handoff. All 26 designs are now
Verified. This supersedes the preceding publication hold and B verification gap.

Wrangler 4.162.0 published build `fae9ed42be9d`; the user authorized OAuth once.
No browser automation or Inkscape rerun was used. The live catalog clears saved
Pending entries on reload; the manifest and all 386 served assets match locally.
See [current status](CURRENT.md) for the deployment and two-device review steps.

## Separate symbol and integration work — 14-11-2026

Source: user in **Agent B**, this chat (original message timestamp unavailable;
recorded 14-11-2026, Europe/Zagreb, UTC+01:00).

**Confirmed and authorized:** preserve and claim the existing checkout for B on
`work/agent-b-symbols`; A works separately on `work/agent-a-integration`. Local
backups, branch setup, verification and task-specific checkpoint commits are
authorized. Retain unfinished work in place and preserve ignored evidence.
Each agent owns its handoff record; exact tested commits, not branch tips, signal
integration readiness. A combines ready checkpoints; B adopts agreed shared changes.

B owns symbols and their tests; A owns integration infrastructure, skills, MCP,
search and shared viewer adaptation. Structural format/render/export/viewer
changes require coordination first. Creation tests use A's separate test library.
B remains the sole publisher of the shared preview within current authorization;
this setup does not authorize deployment or pushing new commits. The collection
is the dev library; accounts/personal libraries remain deferred.

**Execution:** a verified external backup preceded B's branch creation at
`477f679c51c699573f0e28f31cfe63f7e4bc01b1`. The source tree was clean; all ignored
candidate, approval and review files were preserved. A's checkout/branch/handoff
were absent at inspection, so A's setup and actual common baseline remain to be
verified. Paths and verification receipts are in B's local handoff.
All accepted designs remain unchanged. No additional batch or unresolved design
was selected. The lighter recurring Inkscape policy remains a proposal.

## Batch 02: broad dev-library expansion — 14-11-2026

Source: user's pasted execution request in **Agent B** (original message timestamp
unavailable; recorded 14-11-2026, Europe/Zagreb, UTC+01:00).

**Authorized:** approximately 80 new designs across the ten named component
families, with a 6–8 hour working budget. Finalize a finite inventory, prioritize
capacitors/diodes/transistors/sources/magnetics, refine representatives, render and
check all combinations, then save completed families. Implementation, tests, docs,
focused commits, pushing B's branch and publishing the tested B library to the
existing shared preview are authorized without further in-scope approval pauses.
This supersedes the setup-only push/publication hold for this batch.

All new designs remain Unverified until human review. Preserve the original 26
approvals and 342 SVGs, accepted UI, and removal of tapped resistors and varistors.
Use current family/batch filters and Variations; do not add review sheets or comment
fields. Each family gets its own stable overnight batch ID. Categorization changes
to existing definitions are editorial and must preserve their geometry approvals.

**Inventory resolution:** 80 new designs / 828 planned configurations. A separate
unidirectional TVS drawing would duplicate the selected Zener form, so the Zener
entry carries that alias; sources/grounds includes 11 distinct requested forms.
See [the inventory](../docs/BATCH_02.md) for IDs, progress and remaining items.

A's isolated checkout now exists and has adopted B's setup commits; the verified
common baseline is `89dbd3efe40a8b79eeb7cfe99f25f32a4cb849d1`. B adds only explicit
recipe registrations and isolated TeX recipes through existing interfaces; A owns
integration and viewer adaptation. No A implementation is assumed ready. B remains
sole preview publisher. The batch explicitly includes command-line Inkscape checks;
the separate long-term testing-policy proposal is not adopted by this request.


## Batch 02 review and corrections — 14-11-2026

Source: user's pasted review request and authoritative 53-record approval JSON in
**Agent B** (original message timestamp unavailable; recorded 14-11-2026,
Europe/Zagreb, UTC+01:00). This supersedes the previous batch's all-Unverified status
and retention of all 80 new designs.

Authorized: retain original 26 plus the union of approved IDs and correction groups;
validate approvals against reviewed artwork before edits; correct both JFETs, four
dot-bearing MOSFETs, three BJTs, chassis ground and XOR/XNOR; remove exactly the
15 named remaining designs. Both bulk MOSFETs already satisfy the no-dot request.
Apply 52 unchanged approvals; old XOR approval cannot approve its replacement.

Fixed 1 mm BJT shortening applies at all sizes; move junctions/leads/pins together,
keep base fixed, place correctly aligned arrows at the outer emitter end. Rebuild
JFETs using CircuitikZ construction and preserve N/P terminal meaning. Trim chassis
bar with cap-aware ends; calculate XOR inputs on the outer curve without masking.

Full configuration render/visual checks, focused regressions, approval/Pending/Undo,
exports, docs, scoped B-branch commit/push and existing-preview publication are
authorized. Preserve A ownership and unrelated research work. Result: 91 designs,
78 Verified and 13 Unverified; corrected revisions require fresh human review.
This request does not approve replacement drawings or authorize another batch.


## Final 13 symbol approvals - 14-11-2026

Source: user's exact 13-record approval JSON in **Brainstorm B**. Original message
timestamp unavailable; recorded 14-11-2026 21:53 +01:00, Europe/Zagreb.

**Human acceptance confirmed; applied locally.** Both JFETs, four three-terminal
MOSFETs, three BJTs, chassis ground and XOR/XNOR are approved at revision 2;
P-bulk enhancement MOSFET is approved unchanged at revision 1. Every supplied
fingerprint matches the current drawing. This supersedes the pending human review
in the previous correction checkpoint; no approval is inferred from test results.

The validator adds exactly 13 entries, preserving all 78 existing entries. Local
build `21ee8da1455d` has 91 Verified / 0 Unverified designs, with all SVG and
complete-library export bytes unchanged. Source and build are saved locally only;
B retains shared-preview publication ownership. No new symbols, geometry changes,
review-service implementation or integration are authorized by this handoff.

**Verified locally:** 62 Python tests, eight JavaScript tests, 90 documentation
links, unchanged artwork/export hashes and repeat handoff validation. Updated the
old regression's 78/13 expectation to 91/0 while preserving rejection of the
superseded XOR fingerprint. The test retry used a writable project temporary
directory after default sandbox-temp permission failures. Hosted publication
and Git synchronization remain pending Agent B.


## Final approval delivery authorization - 14-11-2026

Source: user's **Agent B** request, “Complete publication of my final 13 symbol
approvals.” Original message timestamp unavailable; recorded 14-11-2026,
Europe/Zagreb, UTC+01:00.

Explicitly authorizes reuse of Brainstorm B's prepared changes, current-tree
validation, status documentation, a scoped B-branch commit/push and publication
to the existing shared preview. Supersedes the local-only delivery state above.
Preserve earlier approvals, all artwork/export bytes, unrelated work and A's
isolation. No new symbols, geometry or viewer changes are requested.

**Delivered by Agent B:** 14-11-2026 22:06 +01:00 (verification/recording time).
Source checkpoint `fda51cf00fc2531ec7f83987f5f66a7011ec8cb4` is pushed on
`work/agent-b-symbols`. Cloudflare version `626b5f31-d628-46f2-8554-e26d06a0ede6`
serves build `21ee8da1455d`: hosted catalog confirms 91 Verified / 0 Unverified,
all 13 exact identities, 1,035 configurations and 36 library exports. All 1,079
public assets match local hashes; all 135 removed SVG URLs return 404.
The previous 78 approvals and every artwork/export byte are unchanged. Passed
62 Python tests, eight JavaScript tests and 90 documentation links; real handoff
Pending/Undo reconciliation clears all 13 published approvals. No new rendering,
browser automation or Inkscape run was needed. Physical laptop testing remains
unverified. A and unrelated research remain untouched; no additional batch started.

## GitHub delivery and documentation workflow — 14-11-2026

Source: user's implementation request in Agent A; original message timestamp
unavailable, recorded 14-11-2026 Europe/Zagreb (UTC+01:00).

**Confirmed; adoption authorized:** the [delivery checklist](../DEVELOPMENT.md#delivery-checklist)
is authoritative. Every agent must reach it from `AGENTS.md` before declaring work
finished. Keep authorized branch checkpoints pushed, user setup/tests compact or
visual, and GitHub's `main` README the discoverable entry point. Verify published
links and distinguish backend checks from setup/first-use evidence.

**Agent A is the integration coordinator:** adopt exact ready commits, resolve
conflicts and check the combined result before an authorized `main` update.
Branch pushes, merges and website deployments remain separate actions. Honor
existing authorization without blanket approval pauses; preserve B's active work
and coordinate guidance adoption through the existing owner handoffs.

This task updates guidance only; it does not authorize product-feature merges or
app deployment. Installer simplification and rewriting user guides remain separate
implementation work. [Current status](CURRENT.md#delivery-workflow-adoption) records
branch adoption and outstanding publication/handoff items.

## Agent integration milestone — 14-11-2026

Source: user's attached milestone request in Agent A; original message timestamp
unavailable, recorded 14-11-2026 Europe/Zagreb (UTC+01:00).

**Authorized:** “Local environment setup, implementation, testing, task-specific
checkpoint commits and local integration of ready work are authorized.” Preserve
publication ownership and outstanding design choices. A uses an isolated worktree
from B's committed baseline, and integrates only exact ready checkpoints.

**Confirmed:** search, individual creation and production batches are distinct.
Search always uses the shared viewer, including one/zero matches, with filters
and Browse all. Use this symbol returns exact identity, revision, settings and
SVG. Creation needs short text even with images, explains intent, waits for
confirmation, renders TeX, presents preview and two alternatives, then saves only
on request. Options preserve unrelated parts and connection identities. Saves
remain Unverified; accounts and personal libraries wait.

**Implemented locally:** separate skills, standard MCP Apps resource/bridge,
stdio/HTTP server, isolated durable sessions/drafts/revisions and custom TeX
validation. Rendering, transport and browser checks passed. The server checks
state but cannot prove a quoted response came from a human; skills enforce the
conversation wait. [Platform evidence](../docs/HOST_VERIFICATION.md) remains
separate from protocol tests. B's READY capacitor checkpoint is integrated locally
without transferring its publication ownership; combined checks are recorded in current status.

## Consolidated baseline and Agent A publication — 14-11-2026

Source: user's consolidation request in Agent A (attachment; original message
time unavailable). **Authorized, in progress:** combine exact ready A integration
`8f686fe` and B library `2fedf44`, plus inspected documentation `25d8f54`, `ddbd03f`
and main `131d705`. Resolve integration defects, test, push A's previously local
work, update main without force, deploy the tested combined website and verify
its actual destination. Agent A owns delivery through publication for this task;
this supersedes local-only A and B-only publishing restrictions.

Preserve all 91 approvals, 1,035 configurations, accepted artwork/identities and
intentional removals. Preserve uncommitted and ignored work before cleanup;
retire only fully merged inactive branches or recoverably preserved obsolete
worktrees, accounting for runtime paths. Future tasks branch from the consolidated
main. No Review, website-triggered agent processing, new symbols, categorization
or Library redesign is authorized. [Current status](CURRENT.md) records delivery.


**Delivery verified — 14-11-2026:** combined product `2e2f820` is on main; canonical
website build `c30dfe980c04` is live (Cloudflare version
`f04f7e02-6c66-4a2b-ba2e-1c03ab11ef6b`). All 91 approvals, 1,035 SVGs and 36 exports
are exact. Passed 77 Python/11 JavaScript tests, isolated creation/transport and
targeted UI/download checks; hosted manifest/catalog, 22 representative assets and
135 removed-asset 404s are verified. No embedded-host or laptop completion inferred.
Fully merged inactive task/publication branches and two obsolete publication
worktrees were retired after preservation. The integration folder remains at the
same baseline for installed host paths/stores; the canonical checkout is on main.
Unrelated research and the unmerged historical review branch are retained. See
[current status](CURRENT.md) for future task routing and remaining limitations.
## Live host verification follow-up — 15-11-2026

Source: **Agent A**, chat `01a1d784-a02a-7eb1-9e76-e4a3d2b4692e`, user turn
14-11-2026 23:44:07 +01:00: “Now verify the ChatGPT and Claude integrations so I can
actually search for and create symbols from chat.” Reviewed 15-11-2026 +01:00.

**In progress:** verify actual host use and repair demonstrated integration defects.
Claude required a full exit/reopen; its embedded search exposed singular family
filters returning zero results. The repair normalizes those aliases and includes
session/identity details in model-readable search text. The user reported the same
empty/broadened-result problem in ChatGPT Chat. Corrected host retests remain required.
The user replaced the ground test with a two-port band-pass block. Actual confirmation
authorized rendering three rounded widths; “Revise the drawing first” withheld saving.
A host tool permission is not drawing or save approval. Synthetic tests do not
establish live creation or human acceptance.

**Refinement confirmed — 15-11-2026:** same source chat, turn starting
15-11-2026 00:26:26 +01:00, user message `01a1dc62-3876-7472-9d38-3b88858bac1c`:
“Curve shape should have flat top, rounded edges, and box should be more narrow.”
Confirmation message `01a1dc63-1dd1-73f0-b4a7-ed6d7640d1a9` accepted about 20% less
horizontal width, unchanged height/terminal positions and no save. Review time:
15-11-2026 +01:00. Rendered all 27 configurations and inspected the browser preview;
the earlier draft remains recoverable. Saving and design acceptance are still pending.

The user reported successful ChatGPT search after reload; actual Claude search,
follow-up and selected-identity retrieval passed. Native control was stopped by the
user before the repaired download and creation-guide retest. Record those as pending,
not completed host journeys; source publication remains the focused repair branch.

**Frequency-response artwork correction — 15-11-2026:** same source chat, turn
starting 15-11-2026 18:55:20 +01:00. User message
`01a1e059-72fb-7681-b99b-2721498799d6` requested removal of the lower flat tails;
`01a1e05c-52f0-7623-8ce8-80acca0ac20b` then requested more curved edges. Actual
confirmation replies authorized each render. The latest draft has a flat passband,
broad curved shoulders and sloping lower ends, with no noise-floor plateau.
Each refinement rendered 27 configurations; the box, leads and terminal positions
match the prior draft exactly. Reviewed 15-11-2026 +01:00; remains unsaved, with
earlier drafts recoverable. This is a qualitative symbol, not a calibrated response.
