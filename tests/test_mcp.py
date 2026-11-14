from support import APP
import tempfile
import unittest
from urllib.parse import quote

from mcp.shared.memory import create_connected_server_and_client_session
from core import ROOT
from agent_store import initialize
from agent_service import AgentService
from agent_server import create_server, UI_URI, MIME


class MCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_protocol_search_viewer_selection_and_resource(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "build", prefix="mcp-test-") as path:
            initialize(path)
            server = create_server(AgentService(path))
            async with create_connected_server_and_client_session(server) as client:
                tools = (await client.list_tools()).tools
                search = next(t for t in tools if t.name == "search_symbols")
                self.assertEqual(search.meta["ui"]["resourceUri"], UI_URI)
                found = await client.call_tool("search_symbols", {"query": "normal resistors"})
                self.assertFalse(found.isError)
                self.assertEqual(found.structuredContent["count"], 2)
                session = found.structuredContent["session_id"]
                resource = await client.read_resource(UI_URI)
                self.assertEqual(resource.contents[0].mimeType, MIME)
                self.assertIn("ui/initialize", resource.contents[0].text)
                self.assertNotIn('src="./', resource.contents[0].text)
                data = await client.call_tool("viewer_data", {"session_id": session})
                self.assertNotIn("catalog", data.structuredContent)
                self.assertEqual(len(data.meta["catalog"]["symbols"]), 26)
                selection = await client.call_tool("use_symbol", {"symbol_id": "resistor-eu", "revision": 1, "size": "small", "stroke": "thick", "session_id": session})
                self.assertFalse(selection.isError)
                body = await client.read_resource(selection.structuredContent["resource_uri"])
                self.assertIn('data-size="small"', body.contents[0].text)
                saved = await client.call_tool("get_selection", {"session_id": session})
                self.assertEqual(saved.structuredContent["selection"], selection.structuredContent)
                source = await client.call_tool("get_drawing_source", {"symbol_id": "resistor-variable-eu"})
                self.assertIn("SCResistorVariant", source.structuredContent["recipe_tex"])
                invalid = await client.call_tool("prepare_creation", {"description": "", "interpretation": {}})
                self.assertTrue(invalid.isError)


if __name__ == "__main__":
    unittest.main()
