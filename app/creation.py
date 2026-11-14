"""Confirmed individual creation. Never modifies source symbols or approval ledgers."""
import base64
import copy
import hashlib
import json
import uuid

from core import ROOT, ValidationError, configuration_key
from custom_renderer import render_all, preserve_base
from verification import digest


class Creation:
    def __init__(self, service):
        self.service = service
        self.store = service.store

    def prepare(self, description, interpretation, assumptions=None, uncertainties=None,
                base_symbol_id=None, affected_parts=None, source_draft_id=None):
        if not isinstance(description, str) or not description.strip():
            raise ValidationError("What does the symbol represent? A short textual description is required, including for images.")
        if not isinstance(interpretation, dict) or any(not interpretation.get(k) for k in ("meaning", "elements", "terminals", "labels", "options")):
            raise ValidationError("Interpretation must describe meaning, elements, terminals, labels and options (use 'none' explicitly)")
        if source_draft_id and base_symbol_id:
            raise ValidationError("Choose a source draft or a saved design")
        base = self.service.symbol(base_symbol_id) if base_symbol_id else None
        if source_draft_id:
            source = self.store.get("draft", source_draft_id)
            base = source.get("symbol")
            if not base:
                raise ValidationError("Source draft must already be rendered")
        draft = {"description": description.strip(), "interpretation": interpretation,
                 "assumptions": assumptions or [], "uncertainties": uncertainties or [],
                 "stage": "interpreted", "references": [], "base": base,
                 "source_draft_id": source_draft_id, "affected_parts": affected_parts or []}
        if base and not affected_parts:
            raise ValidationError("Declare the parts intentionally affected by refinement or added options")
        from core import ID_RE
        if any(not isinstance(p, str) or not ID_RE.fullmatch(p) for p in (affected_parts or [])):
            raise ValidationError("Invalid affected part identifier")
        draft["interpretation_digest"] = digest(draft)
        did = self.store.create("draft", draft)
        return {"draft_id": did, **{k: draft[k] for k in ("stage", "description", "interpretation", "assumptions", "uncertainties", "interpretation_digest")},
                "next": "Present this interpretation, resolve uncertainties, and wait for the user's confirmation before confirming/rendering."}

    def attach_image(self, draft_id, name, mime_type, data_base64):
        draft = self.store.get("draft", draft_id)
        if draft["stage"] != "interpreted":
            raise ValidationError("Attach references before confirmation; prepare a new interpretation to change it")
        if mime_type not in ("image/png", "image/jpeg", "image/webp"):
            raise ValidationError("Use PNG, JPEG or WebP reference images")
        try:
            data = base64.b64decode(data_base64, validate=True)
        except ValueError:
            raise ValidationError("Invalid image encoding") from None
        if not 1 <= len(data) <= 8 * 1024 * 1024:
            raise ValidationError("Reference images must be at most 8 MiB")
        valid = {"image/png": data.startswith(b"\x89PNG\r\n\x1a\n"), "image/jpeg": data.startswith(b"\xff\xd8\xff"),
                 "image/webp": data[:4] == b"RIFF" and data[8:12] == b"WEBP"}[mime_type]
        if not valid:
            raise ValidationError("Image bytes do not match MIME type")
        rid = uuid.uuid4().hex
        path = self.store.artifact("references/" + rid)
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(data)
        ref = {"id": rid, "name": name, "mime_type": mime_type, "sha256": hashlib.sha256(data).hexdigest()}
        draft["references"].append(ref)
        draft["interpretation_digest"] = digest({k: v for k, v in draft.items() if k != "interpretation_digest"})
        self.store.put("draft", draft_id, draft)
        return {"draft_id": draft_id, "reference": ref, "interpretation_digest": draft["interpretation_digest"]}

    def confirm(self, draft_id, interpretation_digest, user_response):
        draft = self.store.get("draft", draft_id)
        if draft["stage"] != "interpreted" or interpretation_digest != draft["interpretation_digest"]:
            raise ValidationError("Stale interpretation; show the latest interpretation and wait for confirmation")
        if not isinstance(user_response, str) or not user_response.strip():
            raise ValidationError("Record the actual user's confirmation, not an inferred approval")
        if draft["uncertainties"]:
            raise ValidationError("Resolve necessary uncertainties with a revised interpretation before confirming")
        draft["stage"] = "confirmed"
        draft["confirmation"] = {"response": user_response, "digest": interpretation_digest, "token": uuid.uuid4().hex}
        self.store.put("draft", draft_id, draft)
        return {"draft_id": draft_id, "stage": "confirmed", "confirmation_token": draft["confirmation"]["token"]}

    def render(self, draft_id, confirmation_token, definition, recipe_tex, alternatives):
        draft = self.store.get("draft", draft_id)
        if draft["stage"] != "confirmed" or draft.get("confirmation", {}).get("token") != confirmation_token:
            raise ValidationError("Confirm the current interpretation before generating a symbol")
        if not isinstance(alternatives, list) or len(alternatives) != 2 or any(
                not isinstance(a, dict) or not a.get("design") or not a.get("practical_effect") for a in alternatives):
            raise ValidationError("Propose two meaningful alternatives with practical effects; do not apply them")
        base = draft["base"]
        current = next((s for s in self.service.catalog()["symbols"] if s["id"] == definition.get("id")), None)
        if base:
            required_revision = base["revision"] if draft.get("source_draft_id") else base["revision"] + 1
            if definition.get("id") != base["id"] or definition.get("revision") != required_revision:
                raise ValidationError("Refinement preserves ID and uses the next saved revision (or current draft revision)")
        elif current or definition.get("revision") != 1:
            raise ValidationError("A new symbol needs an unused ID and revision 1")
        directory = "renders/" + uuid.uuid4().hex
        output = self.store.artifact(directory)
        symbol = render_all(definition, recipe_tex, output)
        if base:
            base_paths = {}
            previous = output / "previous"
            previous.mkdir()
            for config in base["configurations"]:
                path = previous / (config["key"] + ".svg")
                path.write_bytes(self.service.asset(config["asset"]))
                base_paths[config["key"]] = path
            preserve_base(symbol, base, {c["key"]: output / c["svg"] for c in symbol["configurations"]}, base_paths, draft["affected_parts"])
        for config in symbol["configurations"]:
            config["asset"] = directory + "/" + config["svg"]
        symbol["source"] = {"definition": directory + "/definition.json", "recipe": directory + "/custom.tex"}
        draft.update(stage="rendered", symbol=symbol, alternatives=alternatives,
                     rendered_fingerprint=symbol["verification"]["fingerprint"])
        self.store.put("draft", draft_id, draft)
        session_id = self.store.create("session", {"filters": {"ids": [symbol["id"]]}, "sequence": 1, "draft_id": draft_id})
        return {**self.service.search_result(session_id), "stage": "rendered", "fingerprint": draft["rendered_fingerprint"],
                "alternatives": alternatives, "proposed_save": {"name": symbol["name"], "category": symbol["family"], "keywords": symbol["keywords"]},
                "next": "Show the actual rendered preview, invite corrections and present both alternatives. Save only on a new user request."}

    def save(self, draft_id, fingerprint, user_request):
        draft = self.store.get("draft", draft_id)
        if draft["stage"] not in ("rendered", "saved") or fingerprint != draft.get("rendered_fingerprint"):
            raise ValidationError("Review the current rendered draft before saving")
        if not isinstance(user_request, str) or not user_request.strip():
            raise ValidationError("Saving requires the user's actual request")
        symbol = copy.deepcopy(draft["symbol"])
        for config in symbol["configurations"]:
            self.service.asset(config["asset"])
        if draft["stage"] != "saved":
            base = draft["base"]
            expected = base["revision"] if base and not draft.get("source_draft_id") else None
            # A refinement of a draft carries the original saved base revision.
            if draft.get("source_draft_id"):
                expected = symbol["revision"] - 1 if symbol["revision"] > 1 else None
            self.store.save_version(symbol, expected)
            draft.update(stage="saved", save_request=user_request)
            self.store.put("draft", draft_id, draft)
        # Verify durable retrieval via a fresh service store lookup, not just the draft.
        stored = self.store.version(symbol["id"], symbol["revision"])
        if stored != symbol:
            raise ValidationError("Saved revision could not be retrieved")
        selection = self.service.select(symbol["id"], symbol["revision"])
        return {"stage": "saved", "library": "dev library", "verification": "unverified", "retrieval_verified": True,
                **selection}


def register_tools(mcp, service, result, UI, READ, WRITE):
    workflow = Creation(service)

    @mcp.resource("schematica://guides/creation", mime_type="text/markdown")
    def creation_guide() -> str:
        return (ROOT.parent / "docs/INDIVIDUAL_CREATION.md").read_text(encoding="utf-8")

    @mcp.tool(annotations=READ)
    def get_creation_guide():
        """Read before constructing a new symbol: drawing contract and complete example schema/TeX.
        Available to chat hosts without MCP resource access. The example is a test fixture,
        not a requested design or approval. No artwork is generated by this tool.
        """
        fixtures = ROOT.parent / "tests/fixtures"
        return result({"guide": creation_guide(),
                       "example_definition": json.loads((fixtures / "individual-ground.json").read_text(encoding="utf-8")),
                       "example_recipe_tex": (fixtures / "individual-ground.tex").read_text(encoding="utf-8")})

    @mcp.tool(annotations=WRITE)
    def prepare_creation(description: str, interpretation: dict, assumptions: list[str] | None = None,
                         uncertainties: list[str] | None = None, base_symbol_id: str | None = None,
                         affected_parts: list[str] | None = None, source_draft_id: str | None = None):
        """Prepare one symbol's interpretation without drawing. Require short text even with images.
        interpretation keys: meaning, elements, terminals, labels, options. Explain assumptions and ask
        necessary questions, then WAIT for user confirmation. Use base_symbol_id only for requested
        options/refinement; declare affected_parts and preserve all other geometry/connections.
        """
        return result(workflow.prepare(description, interpretation, assumptions, uncertainties, base_symbol_id, affected_parts, source_draft_id))

    @mcp.tool(annotations=WRITE)
    def attach_reference_image(draft_id: str, name: str, mime_type: str, data_base64: str):
        """Attach accessible PNG/JPEG/WebP reference pixels to an interpreted draft before confirmation.
        A supplied picture, screenshot or hand sketch still needs a short textual description.
        """
        return result(workflow.attach_image(draft_id, name, mime_type, data_base64))

    @mcp.tool(annotations=READ)
    def read_reference_image(draft_id: str, reference_id: str):
        """Read the actual stored reference image for visual interpretation/OCR; never infer inaccessible pixels."""
        from mcp.types import ImageContent, CallToolResult
        draft = workflow.store.get("draft", draft_id)
        ref = next((r for r in draft["references"] if r["id"] == reference_id), None)
        if not ref:
            raise ValidationError("Unknown draft reference")
        data = workflow.store.artifact("references/" + reference_id).read_bytes()
        return CallToolResult(content=[ImageContent(type="image", mimeType=ref["mime_type"], data=base64.b64encode(data).decode())])

    @mcp.tool(annotations=WRITE)
    def confirm_creation(draft_id: str, interpretation_digest: str, user_response: str):
        """Only AFTER the user replies confirming the displayed interpretation, record that response.
        Never call in the same turn as an unanswered confirmation question. This does not authorize saving.
        """
        return result(workflow.confirm(draft_id, interpretation_digest, user_response))

    @mcp.tool(annotations=WRITE, meta=UI)
    def render_creation(draft_id: str, confirmation_token: str, definition: dict, recipe_tex: str, alternatives: list[dict]):
        """Render a confirmed single-symbol draft in authoritative parameterized TeX. Call get_creation_guide first.
        Validate every size/stroke/option combination. Return an actual shared-viewer preview and two
        proposed alternatives, each with design and practical_effect strings. Does not save or grant approval.
        """
        data = workflow.render(draft_id, confirmation_token, definition, recipe_tex, alternatives)
        return result(data)

    @mcp.tool(annotations=WRITE)
    def save_creation(draft_id: str, fingerprint: str, user_request: str):
        """Only on the user's explicit request, save the reviewed current draft to the dev library.
        Preserve prior revisions and return SVG/download/viewer links after durable retrieval verification.
        Saving is not official verification. First check storage_status.
        """
        return result(workflow.save(draft_id, fingerprint, user_request))
