"""Serve the shared viewer against A's isolated dev library on loopback only."""
import argparse
from http.server import ThreadingHTTPServer
import json
from urllib.parse import parse_qs, unquote, urlsplit

from core import ROOT, ValidationError
from server import Handler
from agent_service import AgentService
from build_site import VIEWER_FILES


class IntegrationHandler(Handler):
    def do_GET(self):
        if not self.allowed():
            return self.reply(403, b'{"error":"Local origin required"}')
        url = urlsplit(self.path)
        args = parse_qs(url.query)
        try:
            if url.path == "/integration.js":
                return self.reply(200, b"window.SCHEMATICA_INTEGRATION=true;", "text/javascript")
            if url.path == "/api/viewer":
                data = self.server.service.viewer_data(args.get("session", [None])[0])
                return self.reply(200, json.dumps(data).encode())
            if url.path == "/api/session":
                data = self.server.service.search_result(args["session"][0])
                return self.reply(200, json.dumps(data).encode())
            if url.path.startswith("/artwork/"):
                body = self.server.service.asset(unquote(url.path[len("/artwork/"):]))
                return self.reply(200, body, "image/svg+xml")
            path = url.path.lstrip("/") or "index.html"
            if path not in VIEWER_FILES or path == "_headers":
                return self.reply(404, b'{"error":"Not found"}')
            if path == "index.html":
                html = (ROOT / "viewer/index.html").read_text(encoding="utf-8")
                # External bootstrap is allowed by the static preview CSP.
                html = html.replace('<script src="./theme.js">', '<script src="./integration.js"></script><script src="./theme.js">')
                return self.reply(200, html.encode(), "text/html")
            self.server.site_root = ROOT / "viewer"
            return super().do_GET()
        except (ValueError, KeyError, FileNotFoundError) as exc:
            return self.reply(400, json.dumps({"error": str(exc)}).encode())

    do_HEAD = do_GET

    def do_POST(self):
        if not self.allowed():
            return self.reply(403, b'{"error":"Local origin required"}')
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length < 1 or length > 65536 or self.headers.get("Content-Type") != "application/json":
                raise ValidationError("Expected bounded JSON request")
            data = json.loads(self.rfile.read(length))
            if self.path == "/api/search":
                response = self.server.service.search(**data)
            elif self.path == "/api/select":
                response = self.server.service.select(**data)
            else:
                return self.reply(404, b'{"error":"Not found"}')
            self.reply(200, json.dumps(response).encode())
        except (ValueError, TypeError, KeyError) as exc:
            self.reply(400, json.dumps({"error": str(exc)}).encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--port", type=int, default=8793)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), IntegrationHandler)
    server.service = AgentService(args.data_root, f"http://127.0.0.1:{args.port}")
    print(f"Integration preview: http://127.0.0.1:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
