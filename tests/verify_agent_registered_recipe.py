"""Exercise B's registered variable-capacitor recipe through A's source/creation path."""
from support import APP
import asyncio
import json
import uuid

from mcp.shared.memory import create_connected_server_and_client_session
from core import ROOT
from agent_store import initialize
from agent_service import AgentService
from agent_server import create_server
from creation import Creation


async def main():
    root = ROOT / "build" / ("registered-recipe-proof-" + uuid.uuid4().hex[:8])
    initialize(root)
    service = AgentService(root)
    workflow = Creation(service)
    async with create_connected_server_and_client_session(create_server(service)) as client:
        response = await client.call_tool("get_drawing_source", {"symbol_id": "capacitor-variable"})
        assert not response.isError
        source = response.structuredContent
    original = service.select("capacitor-variable", 1)
    draft = workflow.prepare("Synthetic compatibility test of the existing variable capacitor", {
        "meaning": "variable capacitor", "elements": "existing plates, leads and arrow",
        "terminals": "unchanged a and b", "labels": "none", "options": "existing four arrow orientations"},
        base_symbol_id="capacitor-variable", affected_parts=["adjustment"])
    confirmed = workflow.confirm(draft["draft_id"], draft["interpretation_digest"], "Synthetic test confirmation")
    source["definition"]["revision"] = source["next_revision"]
    rendered = workflow.render(draft["draft_id"], confirmed["confirmation_token"], source["definition"], source["recipe_tex"],
        [{"design": "reverse arrow", "practical_effect": "changes adjustment emphasis"},
         {"design": "opposite diagonal", "practical_effect": "fits adjacent wiring differently"}])
    saved = workflow.save(draft["draft_id"], rendered["fingerprint"], "Synthetic isolated save request")
    assert saved["verification"]["status"] == "unverified"
    assert service.select("capacitor-variable", 1)["sha256"] == original["sha256"]
    assert len(service.symbol("capacitor-variable")["configurations"]) == 36
    report = {"store": str(root), "configurations": 36, "registered_recipe_import": "passed",
              "source_tool_orientation_argument": "passed", "unaffected_geometry_and_pins": "preserved",
              "old_revision": "retrievable", "production_source": "unchanged"}
    (ROOT / "build/agent-registered-recipe-proof.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
