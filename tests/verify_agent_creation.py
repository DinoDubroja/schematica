"""Focused real TeX creation/save/retrieval check in a unique isolated store."""
from support import APP, FIXTURES
import json
import os
from pathlib import Path
import uuid

from core import ROOT, ValidationError
from agent_store import initialize
from agent_service import AgentService
from creation import Creation


def main():
    path = ROOT / "build" / ("creation-proof-" + uuid.uuid4().hex[:8])
    initialize(path)
    service = AgentService(path)
    creation = Creation(service)
    intent = {"meaning": "ground test fixture", "elements": "bars and lead", "terminals": "one, a", "labels": "none", "options": "full or compact bars"}
    draft = creation.prepare("Integration test: one-terminal ground mark", intent)
    confirmed = creation.confirm(draft["draft_id"], draft["interpretation_digest"], "Synthetic test confirmation; not human artwork approval.")
    definition = json.loads((FIXTURES / "individual-ground.json").read_text())
    recipe = (FIXTURES / "individual-ground.tex").read_text()
    alternatives = [{"design": "shorter lead", "practical_effect": "reduces height but leaves less wiring clearance"},
                    {"design": "wider bars", "practical_effect": "improves visibility at the cost of horizontal space"}]
    rendered = creation.render(draft["draft_id"], confirmed["confirmation_token"], definition, recipe, alternatives)
    assert service.search("test-ground")["count"] == 0, "Unsaved draft leaked into search"
    saved = creation.save(draft["draft_id"], rendered["fingerprint"], "Synthetic test save in the isolated integration library.")
    restarted = AgentService(path)
    retrieved = restarted.search("test-ground")
    assert retrieved["count"] == 1
    symbol = restarted.symbol("test-ground", 1)
    assert len(symbol["configurations"]) == 18
    assert symbol["verification"]["status"] == "unverified"
    selected = restarted.select("test-ground", 1, "small", "thick", {"bars": "compact"})
    assert b'data-option-bars="compact"' in restarted.asset(selected["asset"])
    assert creation.save(draft["draft_id"], rendered["fingerprint"], "Repeat the same test save")["sha256"] == saved["sha256"]
    # Changed artwork preserves the old revision and invalidates verification.
    next_draft = creation.prepare("Refine the test ground bars", intent, base_symbol_id="test-ground", affected_parts=["earth-mark"])
    next_confirmed = creation.confirm(next_draft["draft_id"], next_draft["interpretation_digest"], "Synthetic refinement confirmation.")
    definition["revision"] = 2
    next_render = creation.render(next_draft["draft_id"], next_confirmed["confirmation_token"], definition,
                                 recipe.replace("{-3*\\SCscale},0", "{-3.2*\\SCscale},0").replace("{3*\\SCscale},0", "{3.2*\\SCscale},0"), alternatives)
    creation.save(next_draft["draft_id"], next_render["fingerprint"], "Synthetic refinement save")
    assert restarted.symbol("test-ground", 1)["revision"] == 1
    assert AgentService(path).symbol("test-ground")["revision"] == 2
    assert restarted.asset(selected["asset"])
    report = {"store": str(path), "configurations_rendered": 36, "initial_preview": rendered["viewer_url"],
              "draft_id": next_draft["draft_id"], "session_id": next_render["session_id"],
              "saved_revision": 2, "previous_revision_retrievable": True, "verification": "unverified",
              "checks": ["confirm gate", "all combinations", "pin stability", "option part isolation", "unsaved isolation", "save", "fresh retrieval", "immutable history", "refinement preserves lead"]}
    (ROOT / "build/agent-creation-proof.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
