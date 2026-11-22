import hashlib
import html
import json
import os
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data.json")
CHECKS_PATH = os.path.join(ROOT, "source_checks.json")
REPORT_PATH = os.path.join(ROOT, "offer-source-changes.md")

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ("script", "style", "noscript", "svg"):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag.lower() in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            value = " ".join(data.split())
            if value:
                self.parts.append(value)

def fingerprint(url):
    request = Request(url, headers={"User-Agent": "CardWalletOfferMonitor/1.0 (+GitHub Actions)"})
    with urlopen(request, timeout=25) as response:
        payload = response.read(12 * 1024 * 1024 + 1)
        if len(payload) > 12 * 1024 * 1024:
            raise ValueError("Source exceeds 12 MB monitor limit")
        content_type = response.headers.get("Content-Type", "")
        if "html" in content_type.lower() or payload[:100].lstrip().lower().startswith(b"<!doctype html") or b"<html" in payload[:500].lower():
            parser = VisibleText()
            parser.feed(payload.decode("utf-8", errors="replace"))
            canonical = re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()
            material = canonical.encode("utf-8")
            kind = "html-visible-text"
        else:
            material = payload
            kind = "document-bytes"
        return {
            "http_status": getattr(response, "status", 200),
            "content_type": content_type,
            "fingerprint_type": kind,
            "sha256": hashlib.sha256(material).hexdigest(),
            "final_url": response.geturl(),
        }

def write_output(key, value):
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"{key}={str(value).lower()}\n")

with open(DATA_PATH, encoding="utf-8") as handle:
    data = json.load(handle)
try:
    with open(CHECKS_PATH, encoding="utf-8") as handle:
        previous = json.load(handle)
except FileNotFoundError:
    previous = {"sources": {}}

previous_sources = previous.get("sources", {})
urls = sorted({offer.get("source") for offer in data.get("offers", []) if offer.get("source", "").startswith("https://")})
now = datetime.now(timezone.utc).isoformat(timespec="seconds")
current_sources = {}
changes = []

for url in urls:
    old = previous_sources.get(url, {})
    try:
        current = fingerprint(url)
        current["checked_at"] = now
        current["state"] = "reachable"
        current_sources[url] = current
        old_hash = old.get("sha256")
        if old_hash and old_hash != current["sha256"]:
            changes.append((url, "Page/document content changed"))
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"[:300]
        current_sources[url] = {
            "checked_at": now,
            "state": "unreachable",
            "error": message,
            "previous_sha256": old.get("sha256"),
        }
        changes.append((url, f"Source could not be checked: {message}"))

snapshot = {"checked_at": now, "source_count": len(urls), "sources": current_sources}
with open(CHECKS_PATH, "w", encoding="utf-8") as handle:
    json.dump(snapshot, handle, ensure_ascii=False, indent=2)

if changes:
    lines = [
        "# Card Wallet — issuer source changes",
        "",
        f"Checked at: {now} (UTC)",
        "",
        "The monitor detected a source-page change or a source that could not be reached. This is not proof that an offer changed or expired. Review the official page and the corresponding data.json entry manually before editing any card benefit.",
        "",
    ]
    for url, detail in changes:
        lines.append(f"- **{detail}** — {url}")
    lines += ["", "No offer wording or cashback values were automatically changed."]
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
else:
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

write_output("changed", bool(changes))
print(f"Checked {len(urls)} unique official source URLs; {len(changes)} changes/errors.")
