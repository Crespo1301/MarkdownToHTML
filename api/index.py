"""Vercel entry point for the Markdown to HTML converter."""

from http.server import BaseHTTPRequestHandler
import json
import mimetypes
from pathlib import Path
import secrets
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from md2html.converter import HTMLConverter
from md2html.parser import MarkdownParser
from md2html.styles import Theme

MAX_REQUEST_BYTES = 1_000_000
MAX_MARKDOWN_CHARS = 750_000
MAX_TITLE_CHARS = 200
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
    "X-Frame-Options": "DENY",
}

DEFAULT_CSP = (
    "default-src 'self'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; "
    "form-action 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; connect-src 'self'; font-src 'self'; upgrade-insecure-requests"
)

ADSENSE_CSP = (
    "default-src 'self' https: data: blob:; base-uri 'none'; object-src 'none'; "
    "frame-ancestors 'none'; form-action 'self'; "
    "script-src 'nonce-{nonce}' 'unsafe-inline' 'unsafe-eval' 'strict-dynamic' https: http:; "
    "style-src 'self' 'unsafe-inline' https:; img-src 'self' data: blob: https:; "
    "connect-src 'self' https:; frame-src https:; font-src 'self' https: data:; "
    "upgrade-insecure-requests"
)


def convert_payload(data):
    """Validate a public API payload and return converted output."""
    if not isinstance(data, dict):
        raise ValueError("The request body must be a JSON object.")

    markdown = data.get("markdown", "")
    title = data.get("title", "Converted Document")
    theme_name = data.get("theme", "light")
    include_toc = data.get("includeToc", True)
    fragment_only = data.get("fragmentOnly", False)

    if not isinstance(markdown, str):
        raise ValueError("markdown must be a string.")
    if len(markdown) > MAX_MARKDOWN_CHARS:
        raise OverflowError("Markdown content is too large.")
    if not isinstance(title, str) or len(title) > MAX_TITLE_CHARS:
        raise ValueError(f"title must be a string up to {MAX_TITLE_CHARS} characters.")
    if theme_name not in {"light", "dark"}:
        raise ValueError("theme must be light or dark.")
    if not isinstance(include_toc, bool) or not isinstance(fragment_only, bool):
        raise ValueError("includeToc and fragmentOnly must be booleans.")

    parser = MarkdownParser()
    tokens = parser.parse(markdown)
    headers = parser.get_headers()
    converter = HTMLConverter(
        theme=Theme.DARK if theme_name == "dark" else Theme.LIGHT,
        include_toc=include_toc,
        include_styles=True,
    )
    output = (
        converter.convert_fragment(tokens)
        if fragment_only
        else converter.convert(tokens, title=title, headers=headers)
    )
    return {
        "html": output,
        "success": True,
        "stats": {"headers": len(headers), "tokens": len(tokens)},
    }


class handler(BaseHTTPRequestHandler):
    """Serve public pages, static assets, and the conversion API."""

    def _send_headers(self, status, content_type, length, cache_control, csp=DEFAULT_CSP):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", cache_control)
        self.send_header("Content-Security-Policy", csp)
        for name, value in SECURITY_HEADERS.items():
            self.send_header(name, value)
        self.end_headers()

    def _send(
        self,
        status,
        body,
        content_type="text/plain; charset=utf-8",
        cache_control="no-store",
        csp=DEFAULT_CSP,
    ):
        payload = body.encode("utf-8") if isinstance(body, str) else body
        self._send_headers(status, content_type, len(payload), cache_control, csp)
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _json(self, status, payload):
        self._send(
            status,
            json.dumps(payload, separators=(",", ":")),
            "application/json; charset=utf-8",
            "no-store",
        )

    def _serve_file(self, path, content_type=None, cache_control="public, max-age=3600"):
        try:
            payload = path.read_bytes()
        except OSError:
            self._serve_404()
            return
        guessed = content_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if guessed.startswith("text/") or guessed in {"application/javascript", "application/xml"}:
            guessed += "; charset=utf-8"
        self._send(status=200, body=payload, content_type=guessed, cache_control=cache_control)

    def _serve_html(self, path, status=200, cache_control="public, max-age=0, must-revalidate"):
        try:
            template = path.read_text(encoding="utf-8")
        except OSError:
            self._send(500, "Unable to load page.")
            return
        nonce = secrets.token_urlsafe(24)
        html = template.replace("{{CSP_NONCE}}", nonce)
        self._send(
            status,
            html,
            "text/html; charset=utf-8",
            cache_control,
            ADSENSE_CSP.format(nonce=nonce),
        )

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/robots.txt":
            self._serve_file(ROOT / "static" / "robots.txt", "text/plain", "public, max-age=3600")
            return
        if path == "/sitemap.xml":
            self._serve_file(ROOT / "static" / "sitemap.xml", "application/xml", "public, max-age=3600")
            return
        if path == "/ads.txt":
            self._serve_file(ROOT / "static" / "ads.txt", "text/plain", "public, max-age=3600")
            return
        if path.startswith("/static/"):
            relative = Path(unquote(path.removeprefix("/static/")))
            static_root = (ROOT / "static").resolve()
            candidate = (static_root / relative).resolve()
            if relative.is_absolute() or not candidate.is_relative_to(static_root) or not candidate.is_file():
                self._serve_html(ROOT / "templates" / "404.html", status=404, cache_control="no-store")
                return
            self._serve_file(candidate)
            return

        pages = {
            "/": "index.html",
            "/about": "about.html",
            "/privacy": "privacy.html",
            "/terms": "terms.html",
            "/support": "support.html",
        }
        template = pages.get(path.rstrip("/") or "/")
        if template:
            self._serve_html(ROOT / "templates" / template)
            return
        self._serve_html(ROOT / "templates" / "404.html", status=404, cache_control="no-store")

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/api/convert":
            self._json(404, {"success": False, "error": "Not found."})
            return
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self._json(415, {"success": False, "error": "Content-Type must be application/json."})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._json(400, {"success": False, "error": "Invalid Content-Length."})
            return
        if content_length <= 0:
            self._json(400, {"success": False, "error": "Request body is required."})
            return
        if content_length > MAX_REQUEST_BYTES:
            self._json(413, {"success": False, "error": "Request is too large."})
            return
        try:
            raw_body = self.rfile.read(content_length)
            data = json.loads(raw_body.decode("utf-8"))
            result = convert_payload(data)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json(400, {"success": False, "error": "Request body must contain valid UTF-8 JSON."})
            return
        except OverflowError as exc:
            self._json(413, {"success": False, "error": str(exc)})
            return
        except ValueError as exc:
            self._json(400, {"success": False, "error": str(exc)})
            return
        except Exception:
            self._json(500, {"success": False, "error": "Conversion failed. Please try again."})
            return
        self._json(200, result)

    def do_PUT(self):
        self._json(405, {"success": False, "error": "Method not allowed."})

    def do_DELETE(self):
        self._json(405, {"success": False, "error": "Method not allowed."})

    def do_PATCH(self):
        self._json(405, {"success": False, "error": "Method not allowed."})

    def do_OPTIONS(self):
        self._send(204, b"", cache_control="no-store")
