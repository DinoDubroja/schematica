# Agent integration

The consolidated source includes natural-language search, one prewritten shared website /
MCP Apps viewer, exact selection handoff, and confirmed individual creation with
isolated save and retrieval. No account or personal-library system is introduced.
See [platform evidence](HOST_VERIFICATION.md) before claiming host support.

## Run locally

Run from your current main checkout (or a task branch based on it), using a
Python 3.12+ environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r app\requirements-agent.txt
.\.venv\Scripts\python.exe app\agent_server.py --data-root "$PWD\app\build\integration-data" --initialize-store
.\.venv\Scripts\python.exe app\integration_preview.py --data-root "$PWD\app\build\integration-data" --port 8793
```

Open [the integration viewer](http://127.0.0.1:8793/). Leave the preview process
running. This local viewer is separate from the canonical static website.

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
```

Open a fresh trusted chat rooted at this checkout, reload its MCP connection if
needed, and use the [search skill](../.agents/skills/schematica-search/SKILL.md) or
[creation skill](../.agents/skills/schematica-create/SKILL.md). The configuration
does not retroactively prove that this currently running chat loaded the tools.
Keep the preview running for browser/download links.

The installed CLI did not discover the generated project configuration during this
check. A separate namespaced global entry, `schematica-integration-a`, was therefore
registered for this machine and recognized by `codex mcp get schematica-integration-a`.
Existing settings were backed up and verified preserved. After source updates, reload the MCP connection or start a fresh chat; registration
alone is not an embedded-host test.
On another machine, inspect project trust/config discovery first. If needed, use
`codex mcp add` with the generated fragment's absolute Python, server and data-root
arguments; do not copy this machine's absolute paths or overwrite existing entries.

Claude's generated JSON fragment is a local launch description. In the observed
Windows 5.11492.5 app, **Settings → Desktop app → Extensions → Local MCP servers →
Edit config** locates the actual configuration; it is not necessarily under the
older Roaming/Claude path. A namespaced `schematica-integration-a` entry was merged
on this machine after backup, preserving all existing settings. The running app
still showed no loaded servers, so restart/reload it before the checklist. No real
embedded journey is established by editing this configuration.

Cloud-hosted Chat/Work/Codex and remote Claude connectors cannot assume access to
this machine's loopback. They need an approved reachable endpoint/private tunnel
and persistence arrangement. This local milestone does not publish a server,
establish a tunnel. The website is published independently.

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

Creation checks need the renderer executables as well as Python dependencies.
If dvisvgm is not discovered in a task worktree, set `SCHEMATICA_DVISVGM` to its
existing absolute executable path before running these commands. Do the same for
`SCHEMATICA_TECTONIC` if needed. Setup fragments preserve those resolved tool paths.


```powershell
.\.venv\Scripts\python.exe -m pip install -r app\requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --test tests\review.test.cjs tests\configurations.test.cjs tests\host.test.cjs
.\.venv\Scripts\python.exe tests\verify_agent_creation.py
.\.venv\Scripts\python.exe tests\verify_agent_transport.py
.\.venv\Scripts\python.exe tests\verify_agent_options.py
.\.venv\Scripts\python.exe tests\verify_agent_registered_recipe.py
.\.venv\Scripts\python.exe app\build_site.py
.\.venv\Scripts\python.exe tests\check_docs.py
```

The real rendering proof creates a unique isolated store under `app/build/`.
Its test confirmations and saves are synthetic; they confer no human artwork
approval. The [host checklist](HOST_VERIFICATION.md#user-verification) covers
the remaining real-host behavior.
