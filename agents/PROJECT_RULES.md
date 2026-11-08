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
├── scripts/
│   ├── build_preference_galleries.py
│   └── .
└── .
```

## Preference hierarchy

- Each independent general rule has one folder in a suitable category, a minimal
  human `README.md`, and an authoritative `RULE.md`. Keep stable ID, status, decision
  date, exact instruction, scope, exceptions, evidence, and asset provenance in `RULE.md`.
  Link precedence in [GENERAL.md](../preferences/GENERAL.md); do not copy it.
- Individual READMEs use simple titles, a required **✅ Good** illustration, an optional
  **❌ Bad** illustration, a useful short description, downloads, and navigation.
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
  Use a level-one title and level-two Good/Bad headings. Wrap just the paired
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
