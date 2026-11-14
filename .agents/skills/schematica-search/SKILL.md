---
name: schematica-search
description: Find and reuse existing electronic symbols in Schematica's dev library, including natural-language follow-ups, variations, SVG downloads and an explicit agent selection. Use for search or browsing, not creating a replacement symbol or running production batches.
---

Use the connected Schematica MCP tools. If unavailable, follow the project's
`docs/AGENT_INTEGRATION.md` setup; report the missing connection without inventing
results. This skill has no dependency on archived Schematica instructions.

- Call `search_symbols` for every user-facing search. Its prewritten shared MCP
  Apps viewer must open even for one match or no matches. In a host without an
  embedded UI, open/provide `viewer_url` and label this as a browser fallback.
- Translate intent into meaningful filters. “Normal resistor” means the existing
  standard fixed designs. The tool understands common terms; use explicit
  `filters` for richer interpretations, and explain any ambiguity that affects
  results. Never silently substitute a nearby design or create a missing symbol.
- Keep the returned `search_session` across follow-ups (`session_id` remains a
  legacy bridge alias). “Only European ones” sets `style: eu`;
  “variable ones instead” replaces `variant`; “thicker stroke” changes `stroke`.
  Pass null to clear an individual filter; “Browse all” clears them all. A new,
  unrelated search should start a fresh session.
- Keep chat output compact: count, meaningful active filters and viewer link when
  needed. The viewer handles browsing, descriptions, Variations and downloads
  without another model response. Do not generate a new interface.
- When the user presses **Use this symbol**, use `get_selection(search_session=...)` if
  host context has not supplied the choice. Preserve the returned ID, revision,
  configuration, hash and resource/download links. Read the resource or use
  `get_artwork` to retrieve the actual SVG. Never infer a choice from a screenshot
  or from whichever symbol happens to be first.
- An honest zero-result view is a completed search. Offer individual creation
  only as a separate user choice; don't start it automatically.
