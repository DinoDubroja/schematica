---
name: schematica-create
description: Create one electronic symbol interactively in Schematica from text and optional pictures, screenshots or hand-drawn sketches; refine a draft or add named options to an existing symbol. Use the interpret-confirm-render-review-save workflow, not library-production batches or an unrestricted symbol editor.
---

Use the connected Schematica tools and call `get_creation_guide` for the current
drawing contract and complete example definition/TeX. The same guide is available
at `schematica://guides/creation`. Local fallback: `docs/INDIVIDUAL_CREATION.md` in this
project. Do not load archived Schematica skills or use batch instructions as this
interactive workflow. The collection is the **dev library**; accounts, profiles
and personal libraries are outside this milestone.

1. **Interpret.** Require a short textual description even with an image. If
   absent, ask what the symbol represents and stop before generation. Inspect
   accessible pixels; use OCR when useful, distinguish unclear marks, and explain
   when the host cannot expose the image. Treat images as evidence of meaning,
   elements, terminals, labels and options—not a pixel-copy specification.
2. **Explain and confirm.** Present a concise interpretation, assumptions and
   necessary uncertainties; annotate the reference only when that helps. Use
   `prepare_creation` without generating artwork. Attach accessible image bytes
   with `attach_reference_image` if persistence is useful. Ask for confirmation
   and necessary missing information, then **wait for the user's response**.
   Re-prepare after a substantive correction; resolve necessary uncertainties.
   Only then call `confirm_creation` with the actual response and current digest.
   Never fabricate a confirmation or treat the original creation request as one.
3. **Create.** Check `storage_status`. Build the semantic definition and
   authoritative parameterized TeX recipe; call `render_creation` with the
   confirmation token. It renders every supported size/stroke/option combination.
   For existing-symbol options, first retrieve `get_drawing_source`, preserve
   connection identities and unrelated parts, and declare affected elements.
   The tool rejects incompatible changes and retains recoverable revisions.
4. **Review.** Show the actual rendered shared-viewer preview, with a browser
   fallback explicitly identified when necessary. Invite corrections. Present
   two meaningful design alternatives and their practical effects; do not apply
   them unless requested. A requested correction starts a new interpretation
   using `source_draft_id` (unsaved) or `base_symbol_id` (saved).
5. **Save.** Propose the rendered name, category and keywords. Only after the user
   requests saving call `save_creation` with the current fingerprint and request.
   Return a download and viewer link, then verify fresh search/retrieval. Saving
   does **not** constitute official verification; retain Unverified status.

Unsaved drafts never enter ordinary search. Test fixtures and experimental
symbols stay in an isolated integration store, never a production batch or the
official approval ledger. If a reference, renderer or host capability is missing,
report that specific gap and continue only the independent steps.
