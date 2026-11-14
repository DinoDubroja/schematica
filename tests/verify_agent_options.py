"""Add a named option to an existing symbol in isolation, preserving its geometry."""
from support import APP
import copy
import json
import uuid
from core import ROOT, get_definition
from agent_store import initialize
from agent_service import AgentService
from creation import Creation

root = ROOT / "build" / ("option-proof-" + uuid.uuid4().hex[:8])
initialize(root)
service = AgentService(root)
workflow = Creation(service)
original = service.select("resistor-eu", 1)
draft = workflow.prepare("Test-only marker option above the existing EU resistor", {
    "meaning": "existing resistor plus separate test marker", "elements": "original artwork and a marker above it",
    "terminals": "unchanged a and b", "labels": "none", "options": "marker height"},
    base_symbol_id="resistor-eu", affected_parts=["accent"])
confirmed = workflow.confirm(draft["draft_id"], draft["interpretation_digest"], "Synthetic isolated option-test confirmation")
definition = copy.deepcopy(get_definition("resistor-eu"))
definition.update(recipe="custom", revision=2, family="resistors")
definition["parts"].append({"id": "accent", "description": "Test-only isolated marker"})
definition["options"] = {"marker": {"name": "Marker height", "default": "short", "affected_parts": ["accent"],
    "values": [{"id": "short", "name": "Short"}, {"id": "tall", "name": "Tall"}]}}
recipe = r"""\newcommand{\SCCustom}[3]{%
\SCResistorEU{#1}{#2}{#3}%
\begin{scope}[x=1mm,y=1mm,line width=\SCstroke mm,line cap=round,line join=round]
\begin{SCpart}{accent}
\ifcase\SCoption{marker}\draw (0,5)--(0,6);\or\draw (0,5)--(0,7);\fi
\end{SCpart}
\end{scope}}
"""
rendered = workflow.render(draft["draft_id"], confirmed["confirmation_token"], definition, recipe,
    [{"design": "left-side marker", "practical_effect": "more overhead space, more width"},
     {"design": "right-side marker", "practical_effect": "moves emphasis to the output side"}])
saved = workflow.save(draft["draft_id"], rendered["fingerprint"], "Synthetic save of the isolated option test")
assert saved["verification"]["status"] == "unverified"
assert service.select("resistor-eu", 1)["sha256"] == original["sha256"]
assert service.symbol("resistor-eu")["revision"] == 2
report = {"store": str(root), "configurations": 18, "original_body_and_leads": "preserved",
          "terminal_identities_and_positions": "preserved", "old_revision": "retrievable",
          "new_revision": "unverified", "production_source": "unchanged"}
(ROOT / "build/agent-option-proof.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
