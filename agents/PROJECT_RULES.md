# Project organization and maintenance

## Authoritative homes

`AGENTS.md` is the short reading entry point. [BEHAVIOR.md](BEHAVIOR.md) owns
interaction in chat. This file owns organization and maintenance; the
[example workflow](../skills/schematica-examples/SKILL.md) owns collection/save
procedures. Link these sources instead of duplicating their instructions.

```text
schematica/
├── AGENTS.md
├── README.md                         # Human overview and category navigation
├── agents/
│   ├── BEHAVIOR.md
│   └── PROJECT_RULES.md
├── preferences/
│   ├── README.md                     # Category previews
│   ├── GENERAL.md                    # Agent index, precedence, inactive proposals
│   ├── assets/                       # Shared colored Good/Bad word labels
│   ├── connections/
│   │   ├── README.md
│   │   └── junction-dots/            # RULE, visual README, source and images
│   └── symbols/
│       ├── README.md                 # Combined rule presentations
│       ├── power-supply-arrows/
│       │   ├── README.md             # Human presentation
│       │   ├── RULE.md               # Authoritative rule and evidence
│       │   └── .                     # Editable source and derived images
│       └── signal-terminal-circles/
│           ├── README.md
│           ├── RULE.md
│           └── .
├── styles/
│   ├── INDEX.md                     # Select a source/style and available domains
│   └── THE_ART_OF_ELECTRONICS/
│       ├── README.md                # Selected SVG highlights
│       ├── STYLE.md                 # Shared guidance, routing, status, inventory
│       ├── SCHEMATICS.md            # Existing circuit guidance
│       ├── PLOTS.md                 # Existing qualitative waveform guidance
│       └── examples/
│           ├── README.md            # Browse all categories
│           ├── schematics/
│           │   ├── README.md
│           │   └── …
│           ├── plots/
│           │   ├── README.md
│           │   └── …
│           └── mixed/
│               ├── README.md
│               └── …
├── scripts/
│   ├── build_preference_galleries.py
│   └── .
└── .
```

## Style collections

Keep one collection per source/style under `styles/`. `INDEX.md` selects a collection;
its `STYLE.md` owns shared guidance, links to available domain guides, current status,
and the full example inventory. Domain guides own their specific rules and selection
cues. Link general preferences and shared guidance instead of duplicating them.
Record domain-specific exceptions in their domain guide and link them from `STYLE.md`;
cross-domain exceptions belong in `STYLE.md`. Preserve provisional/accepted status.

The collection `README.md` is a short showcase of roughly three to six selected
highlights, preferably existing theme-aware SVGs. The user chooses favorites;
temporary selections must not be described as their confirmed favorites. Link
prominently to `examples/README.md`, then category READMEs covering all records.
Keep unavailable images explicit and link their notes without broken previews.

Keep example records/assets under `examples/<category>/<example>/` within that collection.
Store each complete mixed figure once; multiple guides can link to it. Categories
describe the main form, not asset availability or review status. Create only guides
and categories with real content. Writing guidance remains absent until collected.

Reference-image pages may display an original PNG directly; a saved image is a
complete reference without a recreation. Preserve its original bytes/background
and provenance. Optional LaTeX and SVG recreations stay beside that original.
Follow [PRESENTATION.md](../scripts/PRESENTATION.md) for each asset type. Collection
and organization do not authorize new style inference or changes to accepted rules.

Leaf category galleries show available examples with short titles/descriptions and
links to full pages; keep text-only records in a clearly labeled notes list. Around
eight visual examples, review useful subdivisions. When a category has children,
show one available representative preview and link per child rather than every
descendant. If a child has no image, show a link and honest status. Organization
may proceed within delegated scope; do not create empty categories or duplicate
examples. Keep these maintenance instructions out of human galleries.

Source-style galleries are authored Markdown. No new generator or automatic
reorganization is required. The preference-gallery builder below owns only the
general-preference galleries and retains their separate visual requirements.

For a move, rebase links from the containing file, including cross-category examples,
gallery navigation, instruction routes, and export command destinations. Update
historical Markdown links while retaining historical decisions and clearly marked old
paths. Verify all records/assets survived and drawing/image hashes are unchanged.
Installed skill junctions must still resolve to the authoritative repository workflow.

## Preference hierarchy

- Each independent general rule has one folder in a suitable category, a minimal
  human `README.md`, and an authoritative `RULE.md`. Keep stable ID, status, decision
  date, exact instruction, scope, exceptions, evidence, and asset provenance in `RULE.md`.
  Link precedence in [GENERAL.md](../preferences/GENERAL.md); do not copy it.
- Individual READMEs use simple titles, a required **Good** illustration, an optional
  **Bad** illustration, a useful short description, downloads, and navigation.
  Show only the word Good in green and Bad in red, without checkmarks or crosses.
  Use the shared transparent word-label SVGs in `preferences/assets/`, with matching
  Good/Bad alt text, so the color survives GitHub Markdown rendering. Both colors
  must remain readable on light and dark backgrounds; no boxes, badges or icons.
  When both examples exist, place Good on the left and Bad on the right in equal
  columns, at the same drawing scale. Align the images above their captions and
  download links. A Good-only example keeps its single presentation.
  Identify the deficient feature, not the entire circuit. Avoid before/after framing.
  Keep operational explanations and identifiers/status out of human galleries.
- A category contains rules or subcategories, not a mixture. A category of rules
  incorporates their designated individual presentations. A category of subcategories
  shows one selected good example and link per immediate subcategory. Nest as needed.
  The main README's Preferences section exposes the same top-level categories.
- More than eight immediate entries prompts an **agent review** of possible subdivision.
  Consider useful groupings with the user; it is not an automatic split or a reason
  to create empty categories. The agent and user choose organization and representatives.
- [GENERAL.md](../preferences/GENERAL.md) selects accepted `RULE.md` files, defines
  inheritance, and keeps pending/deferred/rejected proposals inactive. Only accepted
  rules with good visuals enter generated galleries. Preserve IDs and decision history
  when splitting or superseding rules, and update incoming references and exceptions.
- Keep editable source and transparent light/dark SVGs with downloadable PNGs from
  the same source. Follow [PRESENTATION.md](../scripts/PRESENTATION.md). New focused
  reconstructions must be identified in the rule record, not passed off as old screenshots.
  Historical drawings need not be redrawn when future guidance changes.

## Deterministic gallery generation

Run from the repository root after approved rule, example, or category changes,
before validation and committing:

```text
python scripts/build_preference_galleries.py
python scripts/build_preference_galleries.py --check
```

The single standard-library script reads the existing hierarchy and authored leaf
READMEs. It makes no AI/network calls, chooses no organization or representative,
and runs only when invoked by the agent. It rewrites marked gallery interiors only;
manual content outside them remains byte-for-byte intact. Ordering is by folder name.

Authoring contract (HTML comments are hidden in rendered READMEs):

- A leaf README wraps its title, description, examples and downloads between
  `<!-- preference-visual:start -->` and `<!-- preference-visual:end -->`.
  Use a level-one title. A Good-only page uses a level-two colored label-image
  heading: `## ![Good](../../assets/good-label.svg)`.
  For Good/Bad pairs, wrap an HTML table in `<!-- preference-comparison:start -->`
  / `<!-- preference-comparison:end -->`. Use four rows with two equal columns:
  shared word-label images (`<img src="..." alt="Good">` / `alt="Bad"`),
  drawing images, captions, and download links. Use HTML links inside the table
  so GitHub renders them reliably. Good is left; Bad is right. Wrap the Bad image
  pair in matching `preference-bad:start` / `preference-bad:end` comments.
  Keep all relative paths correct for the leaf's depth. Wrap just the paired
  light/dark image links of the good example in `<!-- preference-good:start -->`
  and `<!-- preference-good:end -->`. Navigation stays outside the visual section.
- A category README declares `<!-- preference-representative: path/to/README.md -->`,
  pointing to an accepted descendant rule selected by the agent/user. Omit it only
  for categories with no accepted rules. It also contains exactly one
  `<!-- preference-gallery:start level=2 -->` / `<!-- preference-gallery:end -->` pair.
  The main README uses level 3 under its Preferences heading. `preferences/README.md`
  has a gallery pair but needs no representative of its own.
- Each `RULE.md` has plain `ID: ...` and `Status: accepted|proposed|deferred|rejected|superseded`
  lines. Only `accepted` is included. Unknown/missing status is an error, not acceptance.
- Visual sections support ATX headings, inline Markdown links/images, and HTML
  `href`/`src` attributes. Use relative file paths, URL-encoding spaces if needed.
  Reference-style Markdown links and code fences in visual sections are rejected
  instead of being silently copied incorrectly. Theme fragments are preserved.
- `--check` writes nothing and fails on stale galleries, invalid markers/hierarchy,
  missing local references or anchors, or a representative outside its category.
  The builder validates every accepted RULE/README and rendered parent README,
  and requires both SVG themes and a PNG in each Good/Bad section.
  It does not prove image/source agreement or judge visual quality.

## Validate an approved change

Reread shared files before editing. Preserve unrelated edits, existing AOE drawings,
and work from other chats. Update dependent references and existing workflow documents
within scope without creating competing authoritative copies.

After building, check human navigation (main → categories → rule → downloads/back)
and agent selection (entry → GENERAL → RULE + visuals → style exceptions).
Verify pending exclusion, nested categories, heading/link rebasing, repeatability,
missing-reference failures, and preservation of manually authored content when changing
the builder. Compile changed drawings; compare source and exports and inspect both
display themes for contrast, transparency, hollow interiors, labels, and clipping.
Review GitHub theme behavior when available; report any unverified part.

## Context and synchronization

On resume, read [CURRENT.md](../context/CURRENT.md), relevant decisions in
[LOG.md](../context/LOG.md), and actual repository state. Keep a concise current
checkpoint and append consequential decisions/results automatically, including during
discussion and before handoff. Routine context logging and its scoped commits/pushes
are authorized; explicit read-only/no-log requests take precedence.

Keep proposals, confirmed decisions, implementation authorization, completed work,
and verification distinct. Logging never authorizes drawings, imports, feature work,
or personal preference edits. Keep detail in its authoritative record and link it.
Reread shared notes before editing; preserve other sessions' entries. Use public-safe
summaries, excluding private chats, account details, personal paths and working inputs.
This is the self-contained adoption of the shared
[context workflow](https://github.com/DinoDubroja/project-workflow/blob/main/PROJECT_CONTEXT.md).

Check branch/status and synchronize safely before work. For authorized changes,
review the scoped diff, run relevant checks, commit coherent changes, and push.
Stage only this task's changes, including selected context hunks; never blanket-stage
concurrent edits. Do not stash/reset/overwrite others' work. Verify the remote contains
the resulting commit and report synchronization or the exact blocker. An old successful
push is not evidence for the current state. After material reading-route changes,
use a fresh read-only session with only the repository to check context recovery and
rule inheritance; exempt that audit from logging.
