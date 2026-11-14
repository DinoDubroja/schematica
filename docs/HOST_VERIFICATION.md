# Host verification

Checked 14–15-11-2026. **Live search is verified through local Codex with the browser
fallback and through Claude Desktop's embedded viewer. Full creation/save journeys
remain unverified.** A browser fallback is not evidence of embedded UI support.
No remote endpoint, tunnel or public plugin was published.

## Evidence

Live host testing exposed a structured-filter defect: `family: resistor` overrode
the natural-language parser's `resistors`, producing false empty results. The repair
normalizes known family aliases. Search text now includes the session, active filters
and bounded symbol summaries because Claude's model only received the earlier
count/link text. This second repair still needs a fresh host reload/retest.

- Local Codex: normal → European → variable → thick searches, browser selection
  feedback and an actual SVG download passed. The downloaded EU variable resistor,
  revision 2, Small/Thick/Down-left matched the returned SHA-256 exactly.
- Claude 5.11492.5: a full exit/reopen loaded the configured server. After the user
  allowed the tool and the filter repair was loaded, the original call returned two
  fixed resistors in an actual embedded viewer; Small/Thick controls and **Use this
  symbol** responded. Model feedback and embedded downloads remain under test.
- ChatGPT Chat: the user reported zero results followed by all symbols. The test
  chat labeled all 91 designs as resistors; stored state showed the family filter
  had been cleared. Retest after reloading the corrected connection is pending.
- Creation: interpretation reached the real connected tool. The user requested a
  different test symbol; its description and confirmation are pending. No live test
  drawing was rendered or saved. Earlier synthetic creation evidence stays separate.
- Focused repair checks: 15 agent tests and the MCP transport/resource test passed,
  including aliases, exact identities and session reuse through text-only results.

The consolidation reran stdio/HTTP and isolated creation/refinement proofs (18 +
36 rendered configurations), complete-library search follow-ups, targeted browser
selection and actual SVG downloads. Earlier option/registered-recipe evidence is
retained for unchanged paths; production artwork is verified by exact hashes.


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
| Production geometry | All 1,035 accepted SVGs, all 91 approvals and all 36 library exports match B exactly; combined 77 Python/11 JavaScript tests pass |

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
| ChatGPT Desktop · Chat | Retest pending | Actual chat connected but returned incorrect filtering before the repair; reload and repeat. Embedded rendering not verified |
| ChatGPT Desktop · Work local | Untested | Local launch configuration prepared; reload connection and run the checklist |
| ChatGPT Desktop · Work cloud | Blocked | No approved reachable MCP endpoint/private tunnel; local-computer bridging is workspace-dependent |
| ChatGPT Desktop · Codex local | Partial | Actual connected search, browser selection feedback and exact SVG download passed. No embedded panel observed; creation/save pending |
| ChatGPT Desktop · Codex cloud | Blocked | No approved cloud connector and persistent dev-library destination |
| Claude Desktop | Partial | Version 5.11492.5: connection loaded after full exit/reopen; corrected search, embedded artwork and configuration controls observed. Selection feedback, embedded download and creation/save require completion |

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

1. Start the local integration preview from the consolidated checkout and load its
   MCP connection in a fresh trusted chat. Confirm `storage_status` points to an
   initialized isolated dev store, never the accepted library or approval record. In Codex, select the namespaced
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
   remain retrievable. Saving must not alter the accepted library's official approvals.
8. Record the host/version, transport and each feature as verified, failed,
   blocked or untested. Repeat in each required environment; do not copy a result
   from one host or execution mode to another.

If no embedded UI is available, the browser link and underlying tools remain
usable. Record the embedded test honestly and retain the failure details.
