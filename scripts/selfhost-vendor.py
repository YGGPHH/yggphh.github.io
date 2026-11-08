#!/usr/bin/env python3
"""Self-host vendor assets in the built site.

Rewrites third-party CDN references in public/*.html to local copies and
copies the needed asset files from node_modules into public/static/vendor/.

Currently handled:
- KaTeX CSS / fonts / copy-tex extension (hardcoded to jsdelivr by the
  @quartz-community/latex plugin)
- stray cdnjs preconnect hints in <head> (nothing loads from cdnjs)

Run after `npx quartz build`. Prints status in English.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
KATEX_SRC = ROOT / "node_modules" / "katex" / "dist"
VENDOR = PUBLIC / "static" / "vendor" / "katex"

KATEX_CSS_PATTERN = re.compile(
    r"https://cdn\.jsdelivr\.net/npm/katex@[^/\"']+/dist/katex\.min\.css"
)
KATEX_JS_PATTERN = re.compile(
    r"https://cdn\.jsdelivr\.net/npm/katex@[^/\"']+/dist/contrib/copy-tex\.min\.js"
)
CDNJS_PRECONNECT = re.compile(
    r'[ \t]*<link rel="preconnect" href="https://cdnjs\.cloudflare\.com"[^>]*/?>\n?'
)


def main() -> int:
    if not PUBLIC.is_dir():
        print("ERROR: public/ not found. Run 'npx quartz build' first.")
        return 1
    if not (KATEX_SRC / "katex.min.css").is_file():
        print("ERROR: node_modules/katex missing. Run 'npm install' first.")
        return 1

    # 1. copy KaTeX assets
    VENDOR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(KATEX_SRC / "katex.min.css", VENDOR / "katex.min.css")
    shutil.copy2(KATEX_SRC / "contrib" / "copy-tex.min.js", VENDOR / "copy-tex.min.js")
    fonts_dst = VENDOR / "fonts"
    if fonts_dst.exists():
        shutil.rmtree(fonts_dst)
    shutil.copytree(KATEX_SRC / "fonts", fonts_dst)
    print(f"Copied KaTeX assets to {VENDOR.relative_to(ROOT)}/")

    # 2. rewrite HTML references
    patched_files = 0
    remaining: set[str] = set()
    for html in PUBLIC.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        new = KATEX_CSS_PATTERN.sub("/static/vendor/katex/katex.min.css", text)
        new = KATEX_JS_PATTERN.sub("/static/vendor/katex/copy-tex.min.js", new)
        new = CDNJS_PRECONNECT.sub("", new)
        if new != text:
            html.write_text(new, encoding="utf-8")
            patched_files += 1
        for m in re.finditer(r"https?://[^\"'<>\s]+", new):
            url = m.group(0)
            host = re.sub(r"https?://", "", url).split("/")[0]
            if host and host not in ("yggphh.github.io", "www.w3.org"):
                remaining.add(host)
    print(f"Patched {patched_files} HTML files.")

    if remaining:
        # informational only: text links (e.g. footer attribution) are fine
        hosts = ", ".join(sorted(remaining))
        print(f"NOTE: remaining external hosts in HTML: {hosts}")
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
