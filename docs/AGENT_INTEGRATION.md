# Agent integration

The local milestone adds natural-language search, one prewritten shared website /
MCP Apps viewer, exact selection handoff, and confirmed individual creation with
isolated save and retrieval. No account or personal-library system is introduced.
See [platform evidence](HOST_VERIFICATION.md) before claiming host support.

## Run locally

Run from Agent A's integration checkout, using its own Python 3.12+ environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r app\requirements-agent.txt
.\.venv\Scripts\python.exe app\agent_server.py --data-root "$PWD\app\build\integration-data" --initialize-store
.\.venv\Scripts\python.exe app\integration_preview.py --data-root "$PWD\app\build\integration-data" --port 8793
```

Open [the integration viewer](http://127.0.0.1:8793/). Leave the preview process
running. The production publisher and its port remain separately owned.

In another terminal, start optional Streamable HTTP:

```powershell
.\.venv\Scripts\python.exe app\agent_server.py --data-root "$PWD\app\build\integration-data" --transport http --port 8794
```

The endpoint is [local MCP](http://127.0.0.1:8794/mcp). It binds only to loopback.
For stdio, omit `--transport http --port 8794`; the host starts that process.
Never use `--initialize-store` in the host's normal launch command.

Creation also needs Tectonic and dvisvgm. Existing tools can be reused read-only;
set `SCHEMATICA_TECTONIC` / `SCHEMATICA_DVISVGM` to their absolute executables when
not on PATH. No API key is required. The local renderer, tool transport and image
access are separate capabilities; test each.

## Connect a local host

Run [the setup helper](../app/setup_agent.py) to generate an ignored local Codex
configuration and a Claude configuration fragment, without changing global host
settings or another checkout:

```powershell
.\.venv\Scripts\python.exe app\setup_agent.py
codex mcp get schematica-integration
```

Open a fresh trusted chat rooted at this checkout, reload its MCP connection if
needed, and use the [search skill](../.agents/skills/schematica-search/SKILL.md) or
[creation skill](../.agents/skills/schematica-create/SKILL.md). The configuration
does not retroactively prove that this currently running chat loaded the tools.
Keep the preview running for browser/download links.

Claude's generated JSON fragment is a local launch description. Current Claude
documentation favors desktop extensions and distinguishes local plugins from
remote connectors; inspect the installed app's supported developer connection
path before merging it. No existing Claude configuration is overwritten.

Cloud-hosted Chat/Work/Codex and remote Claude connectors cannot assume access to
this machine's loopback. They need an approved reachable endpoint/private tunnel
and persistence arrangement. This local milestone does not publish a server,
establish a tunnel or transfer shared-preview ownership.

## Shared interface

`search_symbols` always returns the `ui://schematica/viewer.html` resource, even
for one or zero matches. The HTML bundles the same viewer source used by the
website. A host adapter handles MCP Apps initialization, data loading, lazy artwork,
SVG downloads and `ui/update-model-context` after **Use this symbol**. Normal
browsing doesn't ask the model to generate UI or answer another turn.

Search sessions persist filters and selections. Follow-ups reuse `session_id`.
Local browser views poll their session for updates. Embedded views accept host
tool-result updates; whether a host updates the same view or creates another is
host-dependent. Selection fallback is always `get_selection` and exact artwork
is accessible through MCP resource reads. Failed context feedback is reported.

The website keeps its accepted controls and review workflow. Integration mode
retains Variations, descriptions, preview and downloads, hides approval editing
and adds active filters, **Browse all** and **Use this symbol**. Saved drafts do
not acquire official approvals. Complete-library exports remain in the static
website; the integration viewer exports individual selected symbols.

## Checks

```powershell
.\.venv\Scripts\python.exe -m pip install -r app\requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --test tests\review.test.cjs tests\configurations.test.cjs tests\host.test.cjs
.\.venv\Scripts\python.exe tests\verify_agent_creation.py
.\.venv\Scripts\python.exe tests\verify_agent_transport.py
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe tests\check_docs.py
```

The real rendering proof creates a unique isolated store under `app/build/`.
Its test confirmations and saves are synthetic; they confer no human artwork
approval. The [host checklist](HOST_VERIFICATION.md#user-verification) covers
the remaining real-host behavior.
