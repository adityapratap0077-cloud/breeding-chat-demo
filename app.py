"""Demo server: salt-tolerant rice breeding chat assistant.

Stdlib only. Serves the chat UI and a JSON chat API backed by
retriever.py (deterministic retrieval) + llm.py (OmniRoute gateway).

Run:  python3 app.py [--port 8471]
Then open http://localhost:8471/
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose
import llm
import retriever

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")

MIME = {".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".md": "text/markdown; charset=utf-8"}


class Handler(BaseHTTPRequestHandler):
    server_version = "BreedingChatDemo/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("breeding-demo: " + fmt % args + "\n")

    def _send(self, code, body, ctype="application/json"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        # Vercel serves this as /api/index with a rewrite; strip the prefix
        # so the same routing works on Render/local and on Vercel.
        if path == "/api/index" or path.startswith("/api/index/"):
            path = path[len("/api/index"):] or "/"
        if path == "/":
            path = "/index.html"
        if path == "/sources":
            return self._send(200, open(os.path.join(BASE, "SOURCES.md"),
                                       encoding="utf-8").read(),
                              "text/markdown; charset=utf-8")
        if path == "/api/varieties":
            rows, _, _ = retriever.load_rows()
            names = [{"variety": r["variety"],
                      "tolerance_class": r["tolerance_class"],
                      "season": r["season"]} for r in rows]
            return self._send(200, json.dumps(names))
        # static files only from ./static, no directory traversal
        rel = os.path.normpath(path.lstrip("/"))
        if rel.startswith("..") or os.path.isabs(rel):
            return self._send(404, "not found", "text/plain")
        full = os.path.join(STATIC, rel)
        if os.path.isfile(full):
            ext = os.path.splitext(full)[1]
            with open(full, "rb") as f:
                return self._send(200, f.read(),
                                  MIME.get(ext, "application/octet-stream"))
        return self._send(404, "not found", "text/plain")

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/index" or path.startswith("/api/index/"):
            path = path[len("/api/index"):] or "/"
        if path != "/api/chat":
            return self._send(404, "not found", "text/plain")
        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            length = 0
        if length > 4000:
            return self._send(413, json.dumps({"error": "question too long"}))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            question = str(payload.get("question", ""))[:1000]
        except Exception:
            return self._send(400, json.dumps({"error": "bad JSON"}))

        result = retriever.retrieve(question)
        if result["mode"] == "glossary":
            # Background knowledge: deterministic, never via the LLM.
            text = compose.compose(question, [], "glossary", result["note"],
                                   result.get("glossary"))
        elif os.environ.get("DEMO_NO_LLM"):
            # Hosting without the local AI gateway (e.g. Vercel): answer
            # deterministically from the retrieved rows.
            text = compose.compose(question, result["rows"],
                                   result["mode"], result["note"])
        else:
            try:
                text = llm.answer(question, result["rows"], result["note"])
            except RuntimeError:
                # Self-contained fallback: deterministic answer from rows.
                text = compose.compose(question, result["rows"],
                                       result["mode"], result["note"])
                result["llm_error"] = True
                result["mode"] = result["mode"] + "+composed"

        used = [{"variety": r["variety"],
                 "yield_saline_tha": r.get("yield_saline_tha", ""),
                 "tolerance_class": r.get("tolerance_class", ""),
                 "sources": r.get("sources", "")} for r in result["rows"]]
        return self._send(200, json.dumps({
            "answer": text,
            "rows_used": used,
            "mode": result["mode"],
        }))


def main():
    port = int(os.environ.get("PORT", "0") or "0")
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    if not port:
        port = 8471
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("breeding-chat-demo on http://127.0.0.1:%d/  (Ctrl+C to stop)" % port,
          flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
