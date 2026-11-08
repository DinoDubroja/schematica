# Schematica Preferences & Examples in Codex

This setup connects local Codex on Windows to a complete Schematica download.
The workflow, saved preferences, styles, examples and supporting procedures stay
together. It works with an extracted ZIP or a Git checkout; Git is not required.

## Install

1. Download Schematica from [the repository](https://github.com/DinoDubroja/schematica)
   using **Code → Download ZIP**, or use your existing checkout. Extract the whole
   folder to a stable, writable location. Do not install just the skill subfolder.
2. Open that folder in Codex and ask: **"Install this Schematica download for Codex
   using INSTALL.md."** The agent should run the helper below and verify the result.
   Alternatively, open PowerShell 7 in the extracted folder and run it yourself:

   ```powershell
   pwsh -NoProfile -File .\scripts\install-codex.ps1
   ```

3. Start a new Codex chat and look for **Schematica Preferences & Examples** in the
   skill list. If it does not appear, restart Codex. Try:

   ```text
   $schematica-preferences I want to work on amplifiers and op-amp symbols.
   ```

The helper creates one directory link in your user skill folder. On a standard
installation this is `%USERPROFILE%\.agents\skills\schematica-preferences`.
If `CODEX_HOME` is set, it uses that location's `skills` folder instead. It also
checks the standard and older `.codex\skills` locations for conflicting copies.
It preserves an existing correct registration and migrates the former
`schematica-examples` link only when it belongs to this same Schematica copy.
It does not replace ordinary folders or another download's registration.

If Windows blocks the downloaded script, inspect it first. You can unblock that
one reviewed file with `Unblock-File -LiteralPath .\scripts\install-codex.ps1`
and retry. The helper does not change PowerShell policy or Codex permissions.

## Use it naturally

You can explicitly use `$schematica-preferences`, or write:

- "Start Schematica Preferences. I want to work on amplifier symbols."
- "Let's compare a few op-amp symbols in Schematica."
- "Add this example to Schematica."

Codex can match natural requests to the skill's description; mentioning Schematica
makes the intended workflow clear. Use the explicit skill when you want to select
it directly. These are examples, not fixed phrases you must memorize.
[Codex skill discovery and invocation](https://learn.chatgpt.com/docs/build-skills).

A typical session:

1. You name a topic: amplifiers and operational-amplifier symbols.
2. The agent suggests a starting point: "Would you like to start by comparing a
   few op-amp symbols?"
3. You request the options. The agent shows a small visual comparison **in chat**.
4. You choose or change details. The agent refines that preview with you.
5. When you explicitly ask to save, the agent records the agreed preference or
   example in this copy and updates the relevant gallery.

You can start at any step. "Show me three op-amp symbol options" already requests
the preview. "B looks good" is feedback; "save B as the default op-amp symbol"
authorizes the specified permanent change. Existing scoped save approvals still
apply, so the agent should not ask again for an action you already authorized.

Exploration uses temporary rendering files. It does not change accepted rules or
permanent examples. General personal preferences and unrelated electronics
questions are outside this skill's scope.

## Verify or remove the connection

From the same Schematica folder:

```powershell
pwsh -NoProfile -File .\scripts\install-codex.ps1 -Check
```

This checks the required library files and the link. To check actual use, ask the
new chat which Schematica folder it is using, then try the broad-topic prompt above.
It should use this copy and help you choose a starting point without saving a rule.
Rendering a requested comparison also requires the drawing tools below.

To disconnect this copy:

```powershell
pwsh -NoProfile -File .\scripts\install-codex.ps1 -Uninstall
```

Removal deletes only the verified registration link. Your downloaded files,
preferences, examples and other Codex skills remain. The helper refuses to remove
a registration pointing to a different copy.

## Move or update your copy

Keep the downloaded folder in place while it is connected. Before moving it or
switching to a different download, run `-Uninstall` from the original folder.
Move/extract the complete folder, then install from its new location. If the old
folder has already moved or disappeared, ask the agent to inspect the existing
registration and remove only that obsolete link before reconnecting.

Approved customizations live in this copy's `preferences/` and `styles/` library.
Preserve them before replacing a download or updating a checkout. This first
version does not automatically merge personal changes into a newer package.
Installing or saving locally does not publish changes to the Schematica project;
Git operations and publication require their own established authorization.

## Drawing requirements and scope

Registration needs PowerShell 7.2 or newer (`pwsh`) on Windows and local Codex with
file access. Ask Codex to check for its available PowerShell runtime if `pwsh` is
not on your terminal's path. Windows PowerShell 5.1 is not supported by this helper.
The helper installs no rendering tools. To generate editable LaTeX illustrations,
the agent also needs a compatible LaTeX renderer with CircuitikZ/TikZ. Saved SVG/PNG
exports use the tools in [the presentation procedure](scripts/PRESENTATION.md),
including Python and PyMuPDF for the bundled export helper. Installation success
alone is not proof that a new computer can render drawings.

If a needed preview capability is unavailable, the agent should identify the
missing piece and offer the closest supported in-chat preview. It should not
silently replace your visual review with a permanent saved rule.

This helper targets local Codex on Windows. Other platforms and a plugin-directory
release are outside this first installation route. For isolated setup testing,
`-SkillsDirectory` accepts an absolute alternate registration folder; in that mode
the helper examines only that folder and Codex must be configured to scan it.
