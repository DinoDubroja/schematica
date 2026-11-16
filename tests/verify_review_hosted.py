"""Exercise persistent Review using independent sessions on the validation worker.

Never targets production. Uses the two isolated ground fixtures and migrated baseline.
The real subscription correction is created by review_desktop.py before this check.
"""
from support import APP
import argparse
import http.cookiejar
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from review_client import Client, write_json
from core import SVG, validate_svg_references


class BrowserSession:
    def __init__(self, config):
        self.url = config["url"]
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.request("/review/login", {"password": config["password"]})

    def request(self, path, value=None, key=None, origin=True):
        headers = {"Content-Type": "application/json", "User-Agent": "SchematicaReviewValidation/1.0"}
        if origin: headers["Origin"] = self.url
        if value is not None: headers["Idempotency-Key"] = key or str(uuid.uuid4())
        request = urllib.request.Request(self.url + path, data=None if value is None else json.dumps(value).encode(), headers=headers)
        with self.opener.open(request, timeout=60) as response:
            raw = response.read()
            return json.loads(raw) if "json" in response.headers.get("Content-Type", "") else raw

    def action(self, name, value, **kwargs):
        return self.request("/api/review/actions/" + name, value, **kwargs)

    def confirm_process(self):
        """Explicit test-only confirmation of a freshly read complete summary."""
        summary=self.request('/api/review/processing-summary')
        return self.action('process',{'snapshot':summary['snapshot'],'included':[item['key'] for item in summary['corrections']+summary['publications']]})

    def storage_state(self):
        return {"cookies": [{"name": c.name, "value": c.value, "domain": c.domain, "path": c.path,
                             "expires": c.expires, "httpOnly": True, "secure": True, "sameSite": "Strict"} for c in self.cookies], "origins": []}


def rejected(fn, status):
    try: fn()
    except urllib.error.HTTPError as error: assert error.code == status, (error.code, error.read())
    else: raise AssertionError("Request unexpectedly succeeded")


def run(config_path, output):
    config = json.loads(Path(config_path).read_text())
    host = urllib.parse.urlparse(config["url"]).hostname
    assert host.startswith("schematica-review-validation.") or host == "localhost", "Never run against production Review"
    client = Client(config); a, b = BrowserSession(config), BrowserSession(config); checks = []
    state = client.state()
    first, second = state["symbols"]["test-ground"], state["symbols"]["test-ground-companion"]
    r1, r2 = first["revisions"][0], first["latest"]
    assert r1 != r2 and client.revision(r2)["parent"] == r1
    assert client.revision(r2)["change"]["source_diff"]
    assert any(j["results"] and j.get("approved") for j in state["jobs"].values())
    checks.append("Real subscription correction, source diff, proposal approval and returned revision retained")
    target = [{"symbol": first["id"], "revision": r1, "configurations": []},
              {"symbol": second["id"], "revision": second["latest"], "configurations": []}]
    content = "Synthetic shared review: keep the lead unchanged; shorten only the top bar."
    key = str(uuid.uuid4()); saved = a.action("comment", {"text": content, "targets": target}, key=key)
    assert a.action("comment", {"text": content, "targets": target}, key=key) == saved
    original = b.request("/api/review/state")["comments"][saved["id"]]
    assert original["text"] == content and original["originalTargets"] == target
    b.action("comment", {"comment": saved["id"], "expected": original["edit"], "text": content + " Preserve lower bars too.", "targets": target})
    rejected(lambda: a.action("comment", {"comment": saved["id"], "expected": original["edit"], "text": "stale", "targets": target}), 409)
    checks.append("Independent sessions, shared targets, immutable original text, edits and duplicate request recovery")
    a.action("cursor", {"symbol": first["id"], "revision": r1})
    assert b.request("/api/review/state")["cursor"] == {"symbol": first["id"], "revision": r1}
    a.action("discard", {"symbols": [first["id"], second["id"]]})
    discarded = b.request("/api/review/state")
    assert all(discarded["symbols"][s]["discarded"] for s in [first["id"], second["id"]])
    catalog = client.request("/library/catalog.json", authenticated=False)
    assert any(s["id"] == first["id"] and s["review_revision"] == first["published"] for s in catalog["symbols"])
    a.action("restore", {"symbols": [first["id"], second["id"]]})
    checks.append("Cross-device position, multiple discard/restore and preserved published predecessor")
    a.action("verify", {"symbol": first["id"], "revision": r1})
    state = b.request("/api/review/state")
    assert state["symbols"][first["id"]]["selected"] == r1
    assert state["symbols"][first["id"]]["published"] == first["published"]
    a.action("verify", {"symbol": first["id"], "revision": r2})
    checks.append("Older exact revision can be verified without immediate publication")
    # Historical proposals remain evidence. New direct jobs and stale/duplicate
    # processing are exercised by verify_review_usability.py, never recreated
    # through the superseded routine approval workflow here.
    assert any(j.get("proposal") and j.get("approved") for j in state["jobs"].values())
    checks.append("Legacy proposal and explicit approval history remains retained")
    rejected(lambda: a.action("heartbeat", {"status": "impersonation"}), 403)
    rejected(lambda: a.action("discard", {"symbols": [second["id"]]}, origin=False), 403)
    raw = urllib.request.build_opener()
    for path in ("/api/review/state", "/review/review-app.js", "/review/review.css", "/review/index.html",
                 "/api/review/revisions/" + r1, "/review/assets/" + client.revision(r1)["symbol"]["configurations"][0]["sha256"]):
        rejected(lambda p=path: raw.open(urllib.request.Request(config["url"] + p, headers={"User-Agent": "SchematicaReviewValidation/1.0"})), 401)
    a.request("/review/logout", {}); rejected(lambda: a.request("/api/review/state"), 401)
    assert b.request("/api/review/state")["symbols"]
    checks.append("Server protection includes assets/source/UI, CSRF, actor separation and session-specific logout")
    result_job = next(j for j in state["jobs"].values() if j["results"])
    before = len(client.state()["symbols"][first["id"]]["revisions"])
    client.upload(Path(config["work"]) / "jobs" / result_job["id"] / "test-ground" / "package")
    assert len(client.state()["symbols"][first["id"]]["revisions"]) == before
    checks.append("Return-upload retry does not duplicate an immutable revision")
    for key in ("small-thick", "medium-medium-bars-compact"):
        svg = client.request("/" + catalog["exports"][key], authenticated=False)
        root = ET.fromstring(svg); validate_svg_references(root)
        assert len(root.findall(f"{{{SVG}}}defs/{{{SVG}}}symbol")) == len(catalog["symbols"])
        metadata = [json.loads(s.find(f"{{{SVG}}}metadata").text) for s in root.findall(f"{{{SVG}}}defs/{{{SVG}}}symbol")]
        assert {m['symbol_id'] for m in metadata} == {s['id'] for s in catalog['symbols']}
        assert all(m['pins_mm'] and m['size'] == catalog['export_settings'][key]['size'] for m in metadata)
        assert "test-ground-companion" not in svg.decode()
    checks.append("Whole-library exports include exactly published symbols and independent custom options")
    events, after = [], 0
    while True:
        page = client.request(f"/api/review/evidence?after={after}")
        if not page["events"]: break
        events.extend(page["events"]); after = page["next"]
    for name in ("comment", "proposal", "approve", "upload", "verify", "publication", "published", "discard", "restore"):
        assert any(e["action"] == name for e in events), name
    assert any(e["action"] == "comment" and e["body"]["input"]["text"].startswith("Shorten the top ground bar") for e in events)
    checks.append("Original feedback through correction, acceptance and publication remains privately retrievable")
    output = Path(output);output.mkdir(parents=True, exist_ok=True)
    write_json(output / "browser-a.json", BrowserSession(config).storage_state())
    write_json(output / "browser-b.json", b.storage_state())
    write_json(output / "hosted-checks.json", {"url": config["url"], "checks": checks, "physical_phone": "not tested", "production_mutations": False})
    print(json.dumps({"passed": len(checks), "checks": checks}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser();parser.add_argument("--config", required=True);parser.add_argument("--output", required=True)
    args = parser.parse_args();run(args.config, args.output)
