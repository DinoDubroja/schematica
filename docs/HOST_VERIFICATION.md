# Host verification

Checked 14-11-2026. **Protocol and local browser behavior are verified; embedded
application journeys are not yet verified.** A browser fallback is not evidence
of embedded UI support. No remote endpoint, tunnel or public plugin was published.

## Evidence

| Check | Result |
|---|---|
| stdio MCP | Verified: initialization, search/follow-ups, UI resource, selection, actual SVG resource |
| Streamable HTTP MCP | Verified on loopback; invalid external Origin rejected |
| Creation over stdio | Verified: reference PNG bytes, confirmation, 18 real TeX configurations, save |
| Fresh HTTP retrieval | Verified: saved symbol retrieved after a separate server startup; remains Unverified |
| Revision/refinement proof | Verified: 36 real TeX configurations over two revisions, old revision retained, unchanged lead and terminals preserved |
| Existing-symbol options | Verified: 18 configurations with a new named option; original body/leads/pins and old revision preserved |
| B registered recipe reuse | Verified: source-tool wrapper and all 36 variable-capacitor configurations through refinement; unrelated geometry/pins preserved |
| Browser fallback | Verified: normal → European → variable → thick, single match, Variations, empty result, Browse all, Use this symbol; integrated capacitor and saved custom option preview |
| Browser SVG download | Verified byte-for-byte against the selected accepted SVG |
| MCP Apps bridge | Automated mock-host tests pass: initialization, metadata/artwork access, context feedback and refusal fallback; not a real host claim |
| Production geometry | All original 342 SVG files and 26 approvals match the baseline; combined 59 Python/11 JavaScript tests pass |

Repeatable commands are in [the integration guide](AGENT_INTEGRATION.md#checks).
Machine-specific stores, logs, process IDs and exact commits are in A's local
handoff, not this shared document. Test confirmations are synthetic and are not
human acceptance of any drawing.

## Required environments

All six checks—reference image access, embedded UI, selection feedback, download,
save and fresh retrieval—must pass in a particular host before calling that host
verified. A failed feature must be recorded separately from a connectivity block.

| Environment | Status | Current evidence / next dependency |
|---|---|---|
| ChatGPT Desktop · Chat | Untested | Current docs support MCP Apps; actual installed connector and embedded journey need testing |
| ChatGPT Desktop · Work local | Untested | Local launch configuration prepared; reload connection and run the checklist |
| ChatGPT Desktop · Work cloud | Blocked | No approved reachable MCP endpoint/private tunnel; local-computer bridging is workspace-dependent |
| ChatGPT Desktop · Codex local | Blocked | Namespaced local MCP connection registered; this active chat has not reloaded its tools/UI |
| ChatGPT Desktop · Codex cloud | Blocked | No approved cloud connector and persistent dev-library destination |
| Claude Desktop | Blocked | Version 5.11492.5 observed: Settings → Desktop app → Extensions exposes Local MCP servers/Edit config. Namespaced isolated entry added with existing settings preserved; the running app still shows no servers until reload. Embedded journey untested. |

Windows Computer Use guidance in this development session prohibits automation of
the ChatGPT desktop app UI. Therefore its manual interaction checks were not
silently replaced with browser or protocol assertions. No account authentication
or connector approval was automated.

## Current documentation

- [OpenAI MCP setup](https://learn.chatgpt.com/docs/extend/mcp): local stdio/HTTP,
  project/global configuration, and the local/cloud distinction. Local MCP
  availability does not establish cloud connectivity.
- [OpenAI MCP Apps UI](https://developers.openai.com/plugins/build/chatgpt-ui):
  predeclared resources and the portable `ui/*` bridge; optional host extensions.
- [OpenAI connect/test flow](https://developers.openai.com/plugins/deploy/connect-chatgpt):
  hosted connection requires reachable HTTPS or a supported Secure MCP Tunnel.
- [MCP Apps specification](https://modelcontextprotocol.io/docs/extensions/apps):
  host capability negotiation, resource metadata and variable client support.
- [Claude interactive connectors](https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude)
  and [desktop versus remote](https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors):
  interactive views are supported, but local plugin availability differs from
  remote connectors. Current docs say a plugin referencing local MCP works in
  Cowork/Claude Code, not chat; this does not prove the installed Desktop path.
- [Claude custom desktop extensions](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop):
  current installation guidance uses a desktop-extension developer path.

These are documentation claims, not Schematica host-test results.

## User verification

1. Start A's integration preview and load the local MCP connection in a fresh
   trusted chat. Confirm `storage_status` points to A's integration store. Do not
   reuse B's preview, library or approval record. In Codex, select the namespaced
   `schematica-integration-a` connection when present.
2. Ask **“Show me normal resistor symbols you have.”** Expect the existing EU and
   US fixed designs in the shared viewer. Confirm whether it is actually embedded.
3. Follow with **“Only European ones,” “Show variable ones instead,” “Use a thicker
   stroke.”** Check filters, geometry, independent controls and Variations. Try an
   impossible query and **Browse all**. A single match still opens the viewer.
4. Choose Small / Thick / Down-left and press **Use this symbol**. Ask the agent
   which ID, revision and configuration you selected. Download SVG; inspect that
   it matches and contains no preview grid/pins. Repeat after reopening the chat.
5. Attach a small sketch **without text**. Expect a question asking what it
   represents, with no symbol generation. Add a description, review the
   interpretation and reply with a correction before confirming. Check that the
   image is actually accessible and uncertain markings are not invented.
6. Confirm. Expect a real rendered preview and two meaningful alternatives.
   Request one correction/option; check that unrelated geometry and terminals
   stay fixed. Ask for the proposed name, category and keywords.
7. Ask to save. Expect **Unverified**, download and viewer links. In a fresh chat,
   retrieve the saved symbol and its exact configuration; confirm prior revisions
   remain retrievable. Saving must not alter B's official approvals.
8. Record the host/version, transport and each feature as verified, failed,
   blocked or untested. Repeat in each required environment; do not copy a result
   from one host or execution mode to another.

If no embedded UI is available, the browser link and underlying tools remain
usable. Record the embedded test honestly and retain the failure details.
