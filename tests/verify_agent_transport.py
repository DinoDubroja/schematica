"""Real stdio and HTTP MCP checks; test state stays in a unique local store."""
from support import APP, FIXTURES
import asyncio
import base64
from datetime import timedelta
import json
import os
import socket
import subprocess
import sys
import uuid

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client
from core import ROOT
from agent_store import initialize


async def check(client):
    await client.initialize()
    listed = await client.list_tools()
    assert any(t.name == "render_creation" for t in listed.tools)
    result = await client.call_tool("search_symbols", {"query": "normal resistors"})
    assert not result.isError, result
    assert result.structuredContent["count"] == 2
    session_id = result.structuredContent["session_id"]
    for query, expected in (("Only European ones", ["resistor-eu"]), ("Show variable ones instead", ["resistor-variable-eu"]), ("Use a thicker stroke", ["resistor-variable-eu"])):
        result = await client.call_tool("search_symbols", {"query": query, "session_id": session_id})
        assert result.structuredContent["match_ids"] == expected
    resource = await client.read_resource("ui://schematica/viewer.html")
    assert resource.contents[0].mimeType == "text/html;profile=mcp-app"
    selected = await client.call_tool("use_symbol", {"symbol_id": "resistor-variable-eu", "revision": 2,
        "size": "small", "stroke": "thick", "options": {"orientation": "down-left"}, "session_id": session_id})
    svg = await client.read_resource(selected.structuredContent["resource_uri"])
    assert 'data-option-orientation="down-left"' in svg.contents[0].text
    return session_id


async def main():
    root = ROOT / "build" / ("transport-proof-" + uuid.uuid4().hex[:8])
    initialize(root)
    args = [str(ROOT / "agent_server.py"), "--data-root", str(root)]
    env = {k: v for k, v in os.environ.items() if k.startswith("SCHEMATICA_")}
    params = StdioServerParameters(command=sys.executable, args=args, cwd=str(ROOT.parent), env=env)
    with (root / "stdio.log").open("w", encoding="utf-8") as log:
        async with stdio_client(params, errlog=log) as streams:
            async with ClientSession(*streams, read_timeout_seconds=timedelta(minutes=20)) as client:
                stdio_session = await check(client)
                prepared = await client.call_tool("prepare_creation", {"description": "Synthetic ground sketch test", "interpretation": {
                    "meaning": "ground", "elements": "bars and lead", "terminals": "one", "labels": "none", "options": "full or compact"}})
                draft = prepared.structuredContent
                # A real PNG round-trip checks byte access, not semantic vision/OCR.
                png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jT4QAAAAASUVORK5CYII="
                attached = await client.call_tool("attach_reference_image", {"draft_id": draft["draft_id"], "name": "Synthetic pixel transport fixture", "mime_type": "image/png", "data_base64": png})
                ref = attached.structuredContent
                image = await client.call_tool("read_reference_image", {"draft_id": draft["draft_id"], "reference_id": ref["reference"]["id"]})
                assert image.content[0].data == png
                confirmation = await client.call_tool("confirm_creation", {"draft_id": draft["draft_id"], "interpretation_digest": ref["interpretation_digest"], "user_response": "Synthetic transport-test confirmation, not artwork approval."})
                rendered = await client.call_tool("render_creation", {"draft_id": draft["draft_id"], "confirmation_token": confirmation.structuredContent["confirmation_token"],
                    "definition": json.loads((FIXTURES / "individual-ground.json").read_text()), "recipe_tex": (FIXTURES / "individual-ground.tex").read_text(),
                    "alternatives": [{"design": "shorter lead", "practical_effect": "less wiring clearance"}, {"design": "wider bars", "practical_effect": "more width for improved visibility"}]})
                assert not rendered.isError, rendered
                saved = await client.call_tool("save_creation", {"draft_id": draft["draft_id"], "fingerprint": rendered.structuredContent["fingerprint"], "user_request": "Synthetic save to the isolated test library"})
                assert saved.structuredContent["retrieval_verified"]
                preview_session = rendered.structuredContent["session_id"]
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    with (root / "http.log").open("w", encoding="utf-8") as log:
        proc = subprocess.Popen([sys.executable, *args, "--transport", "http", "--port", str(port)], cwd=ROOT.parent,
            stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            async with httpx.AsyncClient() as http:
                for _ in range(100):
                    if proc.poll() is not None:
                        raise RuntimeError("HTTP MCP server exited; inspect http.log")
                    try:
                        await http.get(f"http://127.0.0.1:{port}/mcp")
                        break
                    except httpx.ConnectError:
                        await asyncio.sleep(0.1)
                else:
                    raise RuntimeError("HTTP MCP server did not become ready")
                blocked = await http.post(f"http://127.0.0.1:{port}/mcp", headers={"Origin": "https://untrusted.example"}, json={"jsonrpc": "2.0", "id": 1, "method": "initialize"})
                assert blocked.status_code in (400, 403, 421), blocked.status_code
            async with streamable_http_client(f"http://127.0.0.1:{port}/mcp") as (read, write, _):
                async with ClientSession(read, write) as client:
                    http_session = await check(client)
                    retrieved = await client.call_tool("get_symbol", {"symbol_id": "test-ground", "revision": 1})
                    assert retrieved.structuredContent["verification"]["status"] == "unverified"
        finally:
            proc.terminate()
            proc.wait(timeout=10)
    report = {"stdio": "verified", "streamable_http": "verified", "bad_origin": "rejected", "reference_image_bytes": "verified",
              "creation_over_stdio": "verified", "fresh_http_retrieval": "verified", "rendered_configurations": 18,
              "store": str(root), "preview_session": preview_session,
              "host_embedded_ui": "untested; transport verification is not a host result"}
    (ROOT / "build/agent-transport-proof.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
