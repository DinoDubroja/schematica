# Working on Schematica

## Resume and keep context

Start project work by reading [the current checkpoint](context/CURRENT.md), then [the project direction](DIRECTION.md) and the relevant workflow or collection documents. Use [the context log](context/LOG.md) selectively for decisions, reasoning, and approval history. Verify recorded state against the actual checkout; an old note or completed authorization is not a new instruction to execute it again.

Routine project context logging is authorized. Update `context/CURRENT.md` and `context/LOG.md` after meaningful decisions, corrections, results, or blockers and before handoff, including during discussion. No repeated approval is needed for these notes and their routine commits and pushes. Explicit read-only requests and instructions not to log take precedence. Reread notes before editing to preserve concurrent updates.

Keep user-approved decisions, assistant proposals, authorization to implement, completed work, and verification distinct. Record provisional ideas without promoting them into product direction or style rules. Context logging does not authorize drawings, imports, feature implementation, or changes to personal preferences. Keep domain detail in its existing authoritative document and link it from the checkpoint.

Keep these public notes limited to publication-suitable project information. Do not copy private chats, account details, personal paths, or working screenshots. Follow the commit instructions below for authorized context checkpoints; report if notes remain local rather than synchronized. On another device, synchronize safely before relying on the notes.

This is the project's self-contained adoption of the shared [project context workflow](https://github.com/DinoDubroja/project-workflow/blob/main/PROJECT_CONTEXT.md). Recovery must work from this checkout even when the shared workflow, personal instructions, and old chats are unavailable.

## Select the relevant workflow and style

- When starting or resuming a collection, adding references, recording user feedback, consolidating a style, or preserving a generated example, read [Schematica examples](skills/schematica-examples/SKILL.md). The same workflow applies to new collections from other sources.
- When drawing with a Schematica style, read [the collection index](examples/INDEX.md), then the selected `STYLE.md`, then only the relevant example records and previews. Read their LaTeX sources when helpful. Do not treat examples without a preview as visually inspected.
- During drawing and review, read the workflow's **Preserve a generated example** section when a result or correction seems worth retaining. Offer a concrete saving proposal without waiting for the user to remember documentation. Do not repeatedly offer a declined example.

## Document as we go

At useful checkpoints, proactively propose which examples and lessons to preserve, with concise wording and a suggested location. Save agreed content after approval. Keep inferred design patterns provisional until confirmed, and distinguish good examples, bad examples, and cases still under review.

Keep captions with example records in the repository. Original screenshots are temporary working inputs. Save editable source and its rendered PNG as drawing assets, and keep origin, user feedback, and recreation status distinct. Use full source names in collection titles.

Maintain the human browsing path when saving examples: main `README.md` → collection `README.md` gallery → example `README.md` with a visible PNG, caption/source information, and source links. Keep prose brief and detailed guidance in `STYLE.md` / `EXAMPLE.md`. A metadata-only record is pending, not a finished visual example. Keep unestablished installation and invocation instructions out of the main README. Check both human navigation and agent selection routes after changes.

## Show schematics inline by default

During discussions, display schematics directly in chat, using SVG with a transparent background and theme-aware colors where supported. Explicit requests for another format or save location take precedence.

## Manage commits and pushes

Once the user authorizes implementing or saving a change, handle the relevant checks, commits, and pushes without requiring separate reminders or approvals, unless the user requests otherwise.

- Check the repository state before editing and synchronize safely.
- Review the changes and run relevant checks before committing.
- Commit completed, coherent changes with descriptive messages, then push them to GitHub.
- Include only the approved work; preserve unrelated changes and keep private material out.
- Report what was committed and pushed, or explain any blocker.

Discussion and approval of draft wording alone do not authorize saving or publishing product changes or examples. The routine context notes authorized above may record that discussion with its actual status.
