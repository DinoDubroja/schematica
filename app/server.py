"""Serve the generated website on this computer only. No runtime dependencies."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
import webbrowser

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
CSP = "default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Robots-Tag", "noindex, nofollow")
        self.send_header("Content-Security-Policy", CSP)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def allowed(self):
        hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        origin = self.headers.get("Origin")
        return self.headers.get("Host") in hosts and (not origin or origin in {"http://" + h for h in hosts})

    def do_GET(self):
        if not self.allowed():
            self.reply(403, b'{"error":"Local origin required"}')
            return
        path = unquote(urlsplit(self.path).path).lstrip("/") or "index.html"
        base = Path(getattr(self.server, "site_root", DIST)).resolve()
        target = (base / path).resolve()
        if not target.is_relative_to(base) or not target.is_file() or target.name == "_headers":
            self.reply(404, b'{"error":"File not found"}')
            return
        content_type = "text/javascript" if target.suffix == ".js" else mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.reply(200, target.read_bytes(), content_type)

    do_HEAD = do_GET

    def do_POST(self):
        self.reply(405, b'{"error":"This preview serves static files only"}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args()
    if not (DIST / "build.json").is_file():
        parser.error("Build the website first: python build_site.py")
    build_id = json.loads((DIST / "build.json").read_text())["build_id"]
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"Schematica: {url}\nBuild: {build_id}\nPress Ctrl+C to stop.", flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
