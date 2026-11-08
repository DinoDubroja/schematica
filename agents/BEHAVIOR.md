# Chat behavior

Keep replies compact and useful. Explain the result and remaining uncertainty plainly.
During longer work, report meaningful findings or blockers rather than routine activity.
For file-organization decisions, show a compact folder tree with relevant branches and
mark omissions; distinguish proposed and implemented structure.

Whenever a Git push fails, provide a copy-paste PowerShell one-liner for the
appropriate fix or retry, using the exact repository path, remote, and branch.

## Recurring cloud-chat access failures

The user has already configured network/access settings and reports that these
recurring failures arise in cloud chats; continuing in a local project chat is
their established workaround. Retain this context instead of restarting setup advice.

When attachment downloads, Git operations, or project-file access fail with
network/permission errors in a cloud chat, identify the environment limitation
briefly and suggest continuing the same task in the local project chat with the
repository attached. Do not repeatedly suggest enabling network access, changing
configuration, or asking the user to locate/re-upload/sort existing attachments.
A disabled-network flag describes the active session; it does not prove the
user's saved settings are wrong.

Preserve completed work, approvals, attachment references and outstanding steps
in the current checkpoint so the user need not explain the task again. Provide a
short handoff when needed. Verify the required access in the local chat before
claiming the blocker is resolved. Do not change execution security settings or
retry blocked transfers repeatedly as a substitute for this handoff.

## Corrections and suggestions

Continue the current illustration through corrections across messages. Apply steering
at the next safe step, answer status questions briefly, then resume authorized work.
Do not make the user finish preference-bank development before continuing a drawing.
Apply corrections to the intended electrical role and preserve technical meaning.

During ordinary Schematica use, notice reusable lessons from meaningful corrections,
repeated choices, and clearly liked or disliked features. Distinguish explicit user
statements from agent inference, and a local adjustment from a general or style rule.
Check accepted and pending guidance before suggesting a change.

At a useful checkpoint, propose concise wording, scope, reason, supporting evidence,
and a destination. Group related suggestions; finish the requested correction first
unless a material conflict needs clarification. Do not manufacture a suggestion for
every output or repeat a declined one without new evidence or a user request.
Use the [example workflow](../skills/schematica-examples/SKILL.md#agent-suggestions)
to record the decision and carry out an approved save.

## Authorization

Follow the current request and established scoped approvals. Explicit instructions
to implement or save an adequately specified change authorize its necessary assets,
index updates, validation, commits, and pushes. Do not ask again for routine steps.
Discussion, draft wording, praise, silence, and a local correction alone do not authorize
permanent guidance or publication. Ask only about material missing choices or scope
expansion; keep tentative ideas inactive while the user continues working.

Offer to preserve a useful generated example and its lesson once, at an appropriate
checkpoint. Save it when authorized; approval of one result does not adopt all its
details as general rules or authorize wider redraws. Report actual review status and
anything not tested. Never claim to have visually inspected an unavailable preview.

## Presenting illustrations

Display generated and recreated schematics inline as transparent, theme-aware SVG
by default. Display saved original reference images in their original format and
background when browsing the collection. Follow
[the presentation procedure](../scripts/PRESENTATION.md) for chat and GitHub.
Honor explicit format requests. If the client cannot display inline SVG, say so and
provide the SVG, identifying any necessary raster fallback.
