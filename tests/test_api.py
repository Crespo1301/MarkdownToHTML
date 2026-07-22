"""HTTP-level tests for the Vercel handler."""

from http.client import HTTPConnection
from http.server import HTTPServer
import json
import re
from threading import Thread

import pytest

from api.index import MAX_REQUEST_BYTES, handler


@pytest.fixture
def server():
    httpd = HTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield httpd
    httpd.shutdown()
    thread.join()


def request(server, method, path, body=None, headers=None):
    connection = HTTPConnection("127.0.0.1", server.server_port)
    connection.request(method, path, body=body, headers=headers or {})
    response = connection.getresponse()
    payload = response.read()
    result = response.status, dict(response.getheaders()), payload
    connection.close()
    return result


def test_valid_conversion_is_no_store_and_hardened(server):
    body = json.dumps({"markdown": "# Hello"})
    status, headers, payload = request(
        server, "POST", "/api/convert", body, {"Content-Type": "application/json"}
    )
    assert status == 200
    assert headers["Cache-Control"] == "no-store"
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert "frame-ancestors 'none'" in headers["Content-Security-Policy"]
    assert json.loads(payload)["success"] is True


def test_invalid_json_returns_400_without_internal_details(server):
    status, _, payload = request(
        server, "POST", "/api/convert", "{broken", {"Content-Type": "application/json"}
    )
    assert status == 400
    assert json.loads(payload)["error"] == "Request body must contain valid UTF-8 JSON."


def test_wrong_content_type_returns_415(server):
    status, _, _ = request(
        server, "POST", "/api/convert", "{}", {"Content-Type": "text/plain"}
    )
    assert status == 415


def test_oversized_request_returns_413_before_reading_body(server):
    status, _, _ = request(
        server,
        "POST",
        "/api/convert",
        "{}",
        {
            "Content-Type": "application/json",
            "Content-Length": str(MAX_REQUEST_BYTES + 1),
        },
    )
    assert status == 413


def test_unsupported_method_returns_405(server):
    status, _, payload = request(server, "PUT", "/api/convert", "{}")
    assert status == 405
    assert json.loads(payload)["error"] == "Method not allowed."


def test_missing_route_returns_real_404(server):
    status, _, payload = request(server, "GET", "/not-real")
    assert status == 404
    assert b"Page not found" in payload


def test_homepage_has_adsense_code_with_matching_csp_nonce(server):
    status, headers, payload = request(server, "GET", "/")
    html = payload.decode("utf-8")
    nonce_match = re.search(
        r'<script nonce="([^"]+)" async src="https://pagead2\.googlesyndication\.com/',
        html,
    )
    assert status == 200
    assert nonce_match
    assert f"'nonce-{nonce_match.group(1)}'" in headers["Content-Security-Policy"]
    assert "ca-pub-9248605150391626" in html
    assert "{{CSP_NONCE}}" not in html
    assert (
        '<meta name="google-adsense-account" content="ca-pub-9248605150391626">' in html
    )


@pytest.mark.parametrize("path", ["/", "/about", "/privacy", "/terms", "/support"])
def test_adsense_verification_meta_tag_present_on_every_public_page(server, path):
    status, _, payload = request(server, "GET", path)
    assert status == 200
    assert (
        '<meta name="google-adsense-account" content="ca-pub-9248605150391626">'
        in payload.decode("utf-8")
    )


def test_ads_txt_exposes_authorized_publisher(server):
    status, headers, payload = request(server, "GET", "/ads.txt")
    assert status == 200
    assert headers["Content-Type"].startswith("text/plain")
    assert payload == b"google.com, pub-9248605150391626, DIRECT, f08c47fec0942fa0\n"


def test_csolutions_brand_assets_are_public(server):
    status, headers, payload = request(server, "GET", "/static/csolutions-mark.png")
    assert status == 200
    assert headers["Content-Type"].startswith("image/png")
    assert payload.startswith(b"\x89PNG\r\n\x1a\n")

    status, headers, payload = request(server, "GET", "/static/favicon.ico")
    assert status == 200
    assert headers["Content-Type"].startswith("image/")
    assert payload.startswith(b"\x00\x00\x01\x00")


def test_static_path_traversal_is_rejected(server):
    status, _, _ = request(server, "GET", "/static/%2e%2e/pyproject.toml")
    assert status == 404


def test_fragment_mode_includes_toc_when_requested(server):
    body = json.dumps(
        {
            "markdown": "# Title\n\n## Section",
            "includeToc": True,
            "fragmentOnly": True,
        }
    )
    status, _, payload = request(
        server, "POST", "/api/convert", body, {"Content-Type": "application/json"}
    )
    data = json.loads(payload)
    assert status == 200
    assert 'class="toc"' in data["html"]
    assert "<!DOCTYPE" not in data["html"]


def test_adversarial_input_converts_without_hanging(server):
    import time

    body = json.dumps({"markdown": "*a " * 250_000, "includeToc": False})
    start = time.monotonic()
    status, _, payload = request(
        server, "POST", "/api/convert", body, {"Content-Type": "application/json"}
    )
    elapsed = time.monotonic() - start
    assert status == 200
    assert json.loads(payload)["success"] is True
    assert elapsed < 8, f"Adversarial conversion took {elapsed:.2f}s, expected < 8s"


def test_adsense_csp_omits_unsafe_eval_and_plain_http(server):
    status, headers, _ = request(server, "GET", "/")
    csp = headers["Content-Security-Policy"]
    assert status == 200
    assert "unsafe-eval" not in csp
    assert "http:" not in csp
    assert "'strict-dynamic'" in csp
    assert "frame-ancestors 'none'" in csp
