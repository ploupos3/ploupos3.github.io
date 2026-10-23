"""Add a CSP matching each rendered page without changing Quarto's scripts."""

import base64
import hashlib
import html
from html.parser import HTMLParser
import os
from pathlib import Path
import re


def script_hash(value):
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


class ScriptInventory(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.hashes = set()
        self.handler_hashes = set()
        self.inline_script = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name, value in attrs.items():
            if name.startswith("on") and value:
                self.handler_hashes.add(script_hash(value))
        if tag == "script" and "src" not in attrs:
            self.inline_script = []

    def handle_data(self, data):
        if self.inline_script is not None:
            self.inline_script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.inline_script is not None:
            self.hashes.add(script_hash("".join(self.inline_script)))
            self.inline_script = None


def harden(source):
    source = re.sub(r'\n?<meta id="site-security-[^"]+"[^>]*>\n?', "\n", source)
    inventory = ScriptInventory()
    inventory.feed(source)
    scripts = ["'self'", *sorted(inventory.hashes)]
    # Quarto's mobile navigation has a small inline click handler.
    if inventory.handler_hashes:
        scripts.extend(["'unsafe-hashes'", *sorted(inventory.handler_hashes)])
    policy = "; ".join([
        "default-src 'self'",
        "script-src " + " ".join(scripts),
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' data: https://fonts.gstatic.com",
        "img-src 'self' data: https:",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests",
    ])
    tags = (
        '\n<meta id="site-security-csp" http-equiv="Content-Security-Policy" '
        f'content="{html.escape(policy, quote=True)}">\n'
        '<meta id="site-security-referrer" name="referrer" '
        'content="strict-origin-when-cross-origin">\n'
    )
    charset = re.search(r'<meta\s+charset=[^>]+>', source, re.IGNORECASE)
    if not charset:
        raise ValueError("Rendered page is missing its charset declaration")
    return source[:charset.end()] + tags + source[charset.end():]


def main():
    output = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
    pages = sorted(output.rglob("*.html"))
    if not pages:
        raise SystemExit(f"No rendered HTML pages in {output}")
    for page in pages:
        if page.is_symlink():
            raise SystemExit(f"Unexpected symlink in site output: {page}")
        source = page.read_text(encoding="utf-8")
        page.write_text(harden(source), encoding="utf-8")
    print(f"Applied browser security policy to {len(pages)} pages")


if __name__ == "__main__":
    main()
