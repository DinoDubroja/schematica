"""Schematica MCP server: stdio or loopback Streamable HTTP; no publication."""
import argparse
import json
import re

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent, ToolAnnotations

from core import ROOT, ValidationError
from agent_store import initialize
from agent_service import AgentService

UI_URI = "ui://schematica/viewer.html"
MIME = "text/html;profile=mcp-app"
UI = {"ui": {"resourceUri": UI_URI}}
READ = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)
WRITE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False)


def search_session_id(search_session=None, session_id=None, required=False):
    """Resolve the chat-compatible argument and the original viewer-bridge alias."""
    if search_session is not None and session_id is not None and search_session != session_id:
        raise ValidationError("Conflicting search session identifiers")
    value = search_session if search_session is not None else session_id
    if required and not value:
        raise ValidationError("Provide search_session from the search result")
    return value


def result(data, text=None, meta=None):
    return CallToolResult(content=[TextContent(type="text", text=text or json.dumps(data))],
                          structuredContent=data, **({"_meta": meta} if meta else {}))


def viewer_html():
    html = (ROOT / "viewer/index.html").read_text(encoding="utf-8")
    html = html.replace("<head>", '<head><script>window.SCHEMATICA_EMBEDDED=true;</script>')
    html = html.replace('<link rel="stylesheet" href="./style.css">',
                        "<style>" + (ROOT / "viewer/style.css").read_text(encoding="utf-8") + "</style>")
    def script(match):
        content = (ROOT / "viewer" / match[1]).read_text(encoding="utf-8").replace("</script", "<\\/script")
        # Preserve defer semantics for inlined scripts by placing them at body end.
        scripts.append("<script>" + content + "</script>")
        return ""
    scripts = []
    html = re.sub(r'<script src="\./([a-z-]+\.js)"(?: defer)?></script>', script, html)
    return html.replace("</body>", "\n".join(scripts) + "</body>")


def create_server(service, port=8794):
    mcp = FastMCP("Schematica", instructions=(
        "Search existing symbols with search_symbols; always show its shared viewer, even for one or zero matches. "
        "Reuse search_session for follow-ups. Use get_selection to retrieve the user's choice. "
        "Creation is separate: require a text description, explain intent and wait for confirmation before rendering. "
        "Save only on the user's request. Saving never verifies a design. Read the creation guide resource."),
        host="127.0.0.1", port=port, json_response=True, stateless_http=True, max_request_body_size=12 * 1024 * 1024)

    @mcp.resource(UI_URI, name="Schematica shared viewer", mime_type=MIME,
                  meta={"ui": {"prefersBorder": True, "csp": {"resourceDomains": ["blob:", "data:"]}}})
    def viewer() -> str:
        return viewer_html()

    @mcp.resource("schematica://artwork/{asset}", mime_type="image/svg+xml")
    def artwork_resource(asset: str) -> str:
        from urllib.parse import unquote
        return service.asset(unquote(asset)).decode("utf-8")

    @mcp.tool(annotations=WRITE, meta=UI)
    def search_symbols(query: str = "", session_id: str | None = None, filters: dict | None = None,
                       search_session: str | None = None) -> CallToolResult:
        """Find existing symbols and open the shared interactive viewer, including one or zero results.
        Usually supply query only. Reuse the returned search_session for follow-ups.
        Prefer search_session in chat; session_id is a legacy viewer-bridge alias.
        Optional filters: family (for example resistors/capacitors/diodes), style eu/us, variant fixed/variable/etc,
        terms string[], ids string[], size small/medium/large, stroke thin/medium/thick; null clears a filter.
        'normal resistor' means standard fixed designs. Never creates replacements.
        """
        data = service.search(query, search_session_id(search_session, session_id), filters)
        data["search_session"] = data["session_id"]
        # Some hosts expose only text content to their model. Keep the session,
        # filters and bounded match summaries there as well as in structuredContent.
        summary = {key: data[key] for key in ("search_session", "session_id", "sequence", "filters", "count", "matches", "viewer_url")}
        return result(data, json.dumps(summary))

    @mcp.tool(annotations=READ, meta={"ui": {"visibility": ["app"]}})
    def viewer_data(session_id: str | None = None, search_session: str | None = None) -> CallToolResult:
        """Load the shared viewer catalog and state without sending the catalog to the model."""
        return result({"loaded": True}, meta=service.viewer_data(search_session_id(search_session, session_id)))

    @mcp.tool(annotations=READ)
    def get_symbol(symbol_id: str, revision: int | None = None) -> CallToolResult:
        """Inspect a design's description, pins, supported presets/options and verification without rendering."""
        symbol = service.symbol(symbol_id, revision)
        return result({k: v for k, v in symbol.items() if k not in ("configurations", "source")})

    @mcp.tool(annotations=READ)
    def get_drawing_source(symbol_id: str, revision: int | None = None) -> CallToolResult:
        """Get the authoritative definition and TeX for a requested refinement/options workflow.
        Preserve unrelated parts and connection identities. This does not authorize editing or rendering.
        """
        from core import MACROS, RESISTOR_VARIANTS
        from recipe_registry import BATCH_MACROS
        symbol = service.symbol(symbol_id, revision)
        definition = {k: v for k, v in symbol.items() if k not in ("configurations", "source", "verification", "source_fingerprint")}
        if symbol.get("source"):
            recipe = service.store.artifact(symbol["source"]["recipe"]).read_text(encoding="utf-8")
        else:
            args = ""
            if symbol["recipe"] in BATCH_MACROS:
                args = "{" + (r"\SCoption{orientation}" if "orientation" in symbol.get("options", {}) else "0") + "}"
            if symbol["recipe"] == "resistor-variant":
                drawing = symbol["drawing"]
                orientation = r"\SCoption{orientation}" if "orientation" in symbol.get("options", {}) else "0"
                args = "{%s}{%s}{%s}" % (0 if drawing["body"] == "eu" else 1, RESISTOR_VARIANTS.index(drawing["variant"]), orientation)
            recipe = r"\newcommand{\SCCustom}[3]{" + "\\" + MACROS[symbol["recipe"]] + "{#1}{#2}{#3}" + args + "}\n"
            if "orientation" in definition.get("options", {}):
                definition["options"]["orientation"]["affected_parts"] = ["adjustment"]
        definition["recipe"] = "custom"
        return result({"definition": definition, "recipe_tex": recipe, "next_revision": symbol["revision"] + 1})

    @mcp.tool(annotations=READ)
    def get_artwork(asset: str) -> CallToolResult:
        """Retrieve exact SVG artwork by asset from a selection; SVG is in _meta for the viewer.
        For agents, read the returned schematica://artwork resource to get the actual file.
        """
        from urllib.parse import quote
        body = service.asset(asset).decode("utf-8")
        return result({"asset": asset, "resource_uri": "schematica://artwork/" + quote(asset, safe=""),
                       "download_url": service.preview_url + "/artwork/" + quote(asset, safe="/")}, meta={"svg": body})

    @mcp.tool(annotations=WRITE)
    def use_symbol(symbol_id: str, revision: int, size: str = "medium", stroke: str = "medium",
                   options: dict | None = None, session_id: str | None = None, draft_id: str | None = None,
                   search_session: str | None = None) -> CallToolResult:
        """Make the user's selected identity, exact revision/configuration and retrievable SVG available to the agent."""
        return result(service.select(symbol_id, revision, size, stroke, options,
                                     search_session_id(search_session, session_id), draft_id))

    @mcp.tool(annotations=READ)
    def get_selection(search_session: str | None = None, session_id: str | None = None) -> CallToolResult:
        """Retrieve the latest Use this symbol selection and current filters from an existing viewer.
        Supply search_session from search_symbols. Prefer this name in chat; session_id is a legacy alias.
        """
        return result(service.search_result(search_session_id(search_session, session_id, required=True)))

    @mcp.tool(annotations=READ)
    def storage_status() -> CallToolResult:
        """Verify the actual dev-library storage destination before any create or save action."""
        return result(service.store.status())

    # Creation tools are registered separately, sharing the same store and renderer.
    from creation import register_tools
    register_tools(mcp, service, result, UI, READ, WRITE)
    return mcp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--initialize-store", action="store_true")
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    parser.add_argument("--port", type=int, default=8794)
    parser.add_argument("--preview-url", default="http://127.0.0.1:8793")
    args = parser.parse_args()
    if args.initialize_store:
        print(json.dumps(initialize(args.data_root), indent=2))
        return
    mcp = create_server(AgentService(args.data_root, args.preview_url), args.port)
    mcp.run(transport="streamable-http" if args.transport == "http" else "stdio")


if __name__ == "__main__":
    main()
