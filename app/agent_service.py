"""Host-independent symbol tools, shared by MCP and the local integration viewer."""
import copy
import hashlib
import json
from urllib.parse import quote

from core import ROOT, ValidationError
from exports import catalog as source_catalog, LIBRARY, library_selection
from core import definitions
from verification import publication_catalog, read_ledger
from agent_store import Store
from search import interpret, matches


class AgentService:
    def __init__(self, data_root, preview_url="http://127.0.0.1:8793"):
        self.store = Store(data_root)
        self.preview_url = preview_url.rstrip("/")
        # Validate actual source freshness/approvals. No copied approval flags.
        if LIBRARY != (ROOT / "library").resolve():
            raise ValidationError("Agent tools require this checkout's source library")
        self.base = publication_catalog(source_catalog(), definitions(), LIBRARY, read_ledger())
        self.base["exports"] = {}

    def catalog(self, draft_id=None):
        data = copy.deepcopy(self.base)
        by_id = {s["id"]: s for s in data["symbols"]}
        for symbol in by_id.values():
            for config in symbol["configurations"]:
                config["asset"] = "base/" + config["svg"]
        for symbol in self.store.current_versions():
            by_id[symbol["id"]] = symbol
        if draft_id:
            draft = self.store.get("draft", draft_id)
            if draft.get("stage") not in ("rendered", "saved"):
                raise ValidationError("Draft has no rendered preview")
            symbol = copy.deepcopy(draft["symbol"])
            if draft["stage"] == "rendered":
                symbol["draft_id"] = draft_id
            by_id[symbol["id"]] = symbol
        data["symbols"] = list(by_id.values())
        data["library_name"] = "dev library"
        return data

    def search(self, query="", session_id=None, filters=None):
        session = self.store.get("session", session_id) if session_id else {}
        current = interpret(query, session.get("filters"), filters)
        session = {**session, "filters": current, "query": query, "sequence": session.get("sequence", 0) + 1}
        session.pop("draft_id", None)
        session.pop("selection", None)
        if session_id:
            self.store.put("session", session_id, session)
        else:
            session_id = self.store.create("session", session)
        return self.search_result(session_id)

    def search_result(self, session_id):
        session = self.store.get("session", session_id)
        symbols = [s for s in self.catalog(session.get("draft_id"))["symbols"] if matches(s, session["filters"])]
        return {"session_id": session_id, "sequence": session["sequence"], "filters": session["filters"],
                "count": len(symbols), "match_ids": [s["id"] for s in symbols], "matches": [{k: s[k] for k in ("id", "name", "revision")} for s in symbols[:20]],
                "viewer_url": f"{self.preview_url}/?session={session_id}",
                "draft_id": session.get("draft_id"), "selection": session.get("selection")}

    def viewer_data(self, session_id=None):
        session = self.store.get("session", session_id) if session_id else {"filters": {}, "sequence": 0}
        data = self.catalog(session.get("draft_id"))
        if session.get("selection"):
            choice = session["selection"]
            historical = self.symbol(choice["id"], choice["revision"], choice.get("draft_id"))
            data["symbols"] = [s for s in data["symbols"] if s["id"] != historical["id"]] + [historical]
        return {"catalog": data, "session": session,
                "result": self.search_result(session_id) if session_id else None}

    def symbol(self, sid, revision=None, draft_id=None):
        symbol = next((s for s in self.catalog(draft_id)["symbols"] if s["id"] == sid), None)
        if revision is not None and (not symbol or symbol["revision"] != revision):
            symbol = self.store.version(sid, revision)
            if not symbol:
                base = next((s for s in self.catalog_base()["symbols"] if s["id"] == sid and s["revision"] == revision), None)
                symbol = base
        if symbol is None:
            raise ValidationError("Unknown symbol or revision")
        return symbol

    def catalog_base(self):
        data = copy.deepcopy(self.base)
        for s in data["symbols"]:
            for c in s["configurations"]:
                c["asset"] = "base/" + c["svg"]
        return data

    def asset(self, asset):
        # Exact catalog allowlist, never arbitrary paths from clients.
        configs = [c for s in self.catalog_base()["symbols"] for c in s["configurations"]]
        with self.store.connection() as db:
            versions = [json.loads(row[0]) for row in db.execute("SELECT value FROM versions")]
            drafts = [json.loads(row[0]) for row in db.execute("SELECT value FROM documents WHERE kind='draft'")]
        configs += [c for s in versions for c in s["configurations"]]
        configs += [c for d in drafts if "symbol" in d for c in d["symbol"]["configurations"]]
        config = next((c for c in configs if c.get("asset") == asset), None)
        if config is None:
            raise ValidationError("Unknown artwork")
        path = LIBRARY / asset[5:] if asset.startswith("base/") else self.store.artifact(asset)
        body = path.read_bytes()
        if config.get("sha256") and hashlib.sha256(body).hexdigest() != config["sha256"]:
            raise ValidationError("Stored artwork changed; re-render before using")
        return body

    def select(self, symbol_id, revision, size="medium", stroke="medium", options=None, session_id=None, draft_id=None):
        symbol = self.symbol(symbol_id, revision, draft_id)
        # Unlike library_selection, reject unknown explicit options, never drop them.
        from core import resolve_options, resolve_settings
        selected = resolve_options(symbol, options)
        resolve_settings(symbol, size, stroke, selected)
        config = library_selection(symbol, size, stroke, selected)
        body = self.asset(config["asset"])
        result = {"id": symbol["id"], "name": symbol["name"], "revision": symbol["revision"],
                  "configuration": {"key": config["key"], "size": size, "stroke": stroke, "options": selected},
                  "verification": symbol["verification"], "sha256": hashlib.sha256(body).hexdigest(),
                  "asset": config["asset"], "resource_uri": "schematica://artwork/" + quote(config["asset"], safe=""),
                  "download_url": self.preview_url + "/artwork/" + quote(config["asset"], safe="/"),
                  "viewer_url": f"{self.preview_url}/?symbol={quote(symbol_id)}&revision={revision}&size={size}&stroke={stroke}&options={quote(json.dumps(selected))}"}
        if draft_id:
            result["draft_id"] = draft_id
            result["viewer_url"] += "&draft=" + quote(draft_id)
        if session_id:
            session = self.store.get("session", session_id)
            session["selection"] = result
            self.store.put("session", session_id, session)
        return result
