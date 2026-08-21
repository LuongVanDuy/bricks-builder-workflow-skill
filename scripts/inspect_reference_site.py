#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_RE = re.compile(r"rgba?\([^)]*\)", re.I)
HSL_RE = re.compile(r"hsla?\([^)]*\)", re.I)
ROOT_BLOCK_RE = re.compile(r":root\s*\{([^}]*)\}", re.I | re.S)
CSS_VAR_RE = re.compile(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;{}]+)")
FONT_RE = re.compile(r"font-family\s*:\s*([^;{}]+)", re.I)
MAX_WIDTH_RE = re.compile(r"max-width\s*:\s*([0-9.]+(?:px|rem|em))", re.I)
RADIUS_RE = re.compile(r"border-radius\s*:\s*([^;{}]+)", re.I)
IMPORT_RE = re.compile(r"@import\s+(?:url\()?[\"\']?([^\"\')\s;]+)", re.I)
PRIMARY_HINTS = ("primary", "brand", "main", "accent", "theme", "blue", "link")

class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stylesheets: list[str] = []
        self.inline_styles: list[str] = []
        self.title_parts: list[str] = []
        self._in_style = False
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "link" and "stylesheet" in data.get("rel", "").lower() and data.get("href"):
            self.stylesheets.append(data["href"])
        elif tag.lower() == "style":
            self._in_style = True
        elif tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style": self._in_style = False
        elif tag.lower() == "title": self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_style: self.inline_styles.append(data)
        if self._in_title: self.title_parts.append(data)

def fetch_text(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BricksReferenceInspector/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(encoding, errors="replace")

def normalize_hex(value: str) -> str | None:
    raw = value.strip().removeprefix("#")
    if len(raw) == 3: raw = "".join(ch * 2 for ch in raw)
    elif len(raw) == 4: raw = "".join(ch * 2 for ch in raw[:3])
    elif len(raw) == 8: raw = raw[:6]
    if not re.fullmatch(r"[0-9a-fA-F]{6}", raw): return None
    return "#" + raw.upper()

def extract_root_vars(css: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for block in ROOT_BLOCK_RE.findall(css):
        for name, value in CSS_VAR_RE.findall(block): found[name.strip()] = value.strip()
    return found

def resolve_scalar(value: str, root_vars: dict[str, str]) -> str:
    text = value.strip(); seen: set[str] = set()
    while True:
        match = re.fullmatch(r"var\(--([a-zA-Z0-9_-]+)\)", text)
        if not match or match.group(1) in seen or match.group(1) not in root_vars: return text
        seen.add(match.group(1)); text = root_vars[match.group(1)].strip()

def color_counts(css: str) -> collections.Counter[str]:
    result: collections.Counter[str] = collections.Counter()
    for raw in HEX_RE.findall(css):
        value = normalize_hex(raw)
        if value: result[value] += 1
    for raw in RGB_RE.findall(css): result[re.sub(r"\s+", "", raw.lower())] += 1
    for raw in HSL_RE.findall(css): result[re.sub(r"\s+", "", raw.lower())] += 1
    return result

def choose_primary(root_vars: dict[str, str], counts: collections.Counter[str]) -> dict[str, Any] | None:
    ranked: list[tuple[int, str, str]] = []
    for name, raw in root_vars.items():
        value = resolve_scalar(raw, root_vars)
        match = HEX_RE.search(value)
        resolved = normalize_hex(match.group(0)) if match else None
        if not resolved: continue
        score = max((100 - i * 5 for i, hint in enumerate(PRIMARY_HINTS) if hint in name.lower()), default=0)
        if score: ranked.append((score + min(counts.get(resolved, 0), 20), name, resolved))
    if ranked:
        _, name, value = max(ranked)
        return {"value": value, "method": "named-root-variable", "signals": [f"--{name}", f"literal-usage:{counts.get(value, 0)}"], "confidence": 0.99 if ("primary" in name.lower() or "brand" in name.lower()) else 0.94}
    repeated = sorted(((count, value) for value, count in counts.items() if value.startswith("#") and value not in {"#FFFFFF", "#000000"}), reverse=True)
    if repeated and repeated[0][0] >= 6:
        count, value = repeated[0]
        return {"value": value, "method": "repeated-css-literal", "signals": [f"literal-usage:{count}"], "confidence": 0.78}
    return None

def clean_font(value: str, root_vars: dict[str, str]) -> str | None:
    first = resolve_scalar(value, root_vars).split(",")[0].strip().strip("'\"")
    if not first or first.lower() in {"inherit", "initial", "sans-serif", "serif", "system-ui"} or first.startswith("var("): return None
    return first

def choose_root_font(root_vars: dict[str, str]) -> str | None:
    ranked: list[tuple[int, str]] = []
    for name, raw in root_vars.items():
        lname = name.lower()
        if "font" not in lname or not any(h in lname for h in ("body", "primary", "text", "family", "base")): continue
        font = clean_font(raw, root_vars)
        if font: ranked.append((30 if ("body" in lname or "primary" in lname) else 20, font))
    return max(ranked)[1] if ranked else None

def choose_root_width(root_vars: dict[str, str]) -> str | None:
    ranked: list[tuple[int, str]] = []
    for name, raw in root_vars.items():
        lname = name.lower()
        if not any(h in lname for h in ("container", "content", "site-width", "max-width", "boxed-width")): continue
        value = resolve_scalar(raw, root_vars)
        if re.fullmatch(r"[0-9.]+(?:px|rem|em)", value): ranked.append((30 if ("container" in lname or "content" in lname) else 20, value))
    return max(ranked)[1] if ranked else None

def inspect_html_css(source_url: str, html: str, stylesheet_texts: list[tuple[str, str]]) -> dict[str, Any]:
    parser = PageParser(); parser.feed(html)
    css = "\n".join(["\n".join(parser.inline_styles), *(text for _, text in stylesheet_texts)])
    root_vars = extract_root_vars(css); counts = color_counts(css); primary = choose_primary(root_vars, counts)
    fonts: collections.Counter[str] = collections.Counter()
    for raw in FONT_RE.findall(css):
        font = clean_font(raw, root_vars)
        if font: fonts[font] += 1
    widths = collections.Counter(MAX_WIDTH_RE.findall(css)); radii = collections.Counter(v.strip() for v in RADIUS_RE.findall(css))
    root_font = choose_root_font(root_vars); root_width = choose_root_width(root_vars)
    font = root_font or (fonts.most_common(1)[0][0] if fonts else None)
    width = root_width or (widths.most_common(1)[0][0] if widths else None)
    project = " ".join(x.strip() for x in parser.title_parts if x.strip()) or urllib.parse.urlparse(source_url).hostname or "Project"
    evidence = {
        "source_type": "reference_site", "url": source_url,
        "stylesheets": [url for url, _ in stylesheet_texts], "root_variables": root_vars,
        "top_colors": [{"value": value, "count": count} for value, count in counts.most_common(20)],
        "top_fonts": [{"value": value, "count": count} for value, count in fonts.most_common(10)],
        "content_width_candidates": [{"value": value, "count": count} for value, count in widths.most_common(10)],
        "radius_candidates": [{"value": value, "count": count} for value, count in radii.most_common(10)],
        "primary_color": primary,
        "font_family": ({"value": font, "method": "named-root-variable" if root_font else "repeated-css-declaration", "confidence": 0.96 if root_font else 0.90} if font else None),
        "content_width": ({"value": width, "method": "named-root-variable" if root_width else "repeated-css-declaration", "confidence": 0.96 if root_width else 0.90} if width else None),
    }
    result: dict[str, Any] = {"project": project, "layout": {}, "palette": {}, "theme": {}, "evidence": evidence}
    if primary and primary["confidence"] >= 0.9: result["palette"]["color-primary"] = primary["value"]
    if font: result["theme"]["font_family"] = font
    if width: result["layout"]["content_width"] = width
    blockers: list[str] = []
    if not primary or primary["confidence"] < 0.9: blockers.append("No high-confidence primary brand color found in HTML/CSS.")
    if not font: blockers.append("No evidence-backed primary font family found in HTML/CSS.")
    if not width: blockers.append("No evidence-backed content/container width found in HTML/CSS.")
    evidence["status"] = "verified" if not blockers else "blocked"; evidence["blockers"] = blockers
    return result

def inspect_url(url: str) -> dict[str, Any]:
    html = fetch_text(url); parser = PageParser(); parser.feed(html)
    styles: list[tuple[str, str]] = []; seen: set[str] = set()
    def collect(css_url: str, depth: int = 0) -> None:
        if css_url in seen or depth > 2: return
        seen.add(css_url)
        try: css = fetch_text(css_url)
        except Exception as exc:
            styles.append((css_url, f"/* FETCH FAILED: {exc} */")); return
        styles.append((css_url, css))
        for imported in IMPORT_RE.findall(css): collect(urllib.parse.urljoin(css_url, imported), depth + 1)
    for href in parser.stylesheets: collect(urllib.parse.urljoin(url, href))
    return inspect_html_css(url, html, styles)

def self_test() -> None:
    html = "<html><head><title>Demo Spa</title></head></html>"
    css = ":root{--brand-primary:#1268A5}body{font-family:Inter,sans-serif}.a{color:#1268A5}.b{color:#1268A5}.c{color:#1268A5}.d{background:#1268A5}.e{border-color:#1268A5}.f{color:#1268A5}.container{max-width:1200px}"
    data = inspect_html_css("https://demo.test/", html, [("https://demo.test/app.css", css)])
    assert data["palette"]["color-primary"] == "#1268A5" and data["theme"]["font_family"] == "Inter" and data["layout"]["content_width"] == "1200px" and data["evidence"]["status"] == "verified"
    print("SELF-TEST OK")

def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect reference-site HTML/CSS and emit an evidence-backed Bricks foundation spec.")
    parser.add_argument("url", nargs="?"); parser.add_argument("--output"); parser.add_argument("--self-test", action="store_true"); args = parser.parse_args()
    if args.self_test: self_test(); return
    if not args.url: parser.error("url is required unless --self-test is used")
    try: data = inspect_url(args.url)
    except Exception as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2)); sys.exit(2)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.output: Path(args.output).write_text(text, encoding="utf-8")
    else: print(text, end="")
    if data["evidence"]["status"] != "verified": sys.exit(2)

if __name__ == "__main__": main()
