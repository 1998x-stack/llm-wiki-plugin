#!/usr/bin/env python3
"""Convert wiki/*.md pages to static HTML files.

Usage:
    python3 scripts/build_wiki_pages.py [--output ../static/wiki/]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from wiki_utils import VAULT_DIR, WIKI_DIR, parse_frontmatter, escape_html

try:
    import markdown as md_lib
except ImportError:
    print("Error: 'markdown' package required. Run: pip install markdown")
    raise SystemExit(1)

TYPE_COLORS = {
    "entity": "#4A90D9",
    "concept": "#50C878",
    "synthesis": "#9B59B6",
    "qa-insight": "#E67E22",
}
DEFAULT_COLOR = "#95a5a6"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — LLM Wiki</title>
<style>
:root {{
  --bg: #ffffff; --fg: #1a1a2e; --fg2: #555;
  --surface: rgba(255,255,255,0.85); --border: #e0e0e0;
  --input-bg: #f5f5f5; --code-bg: #f8f8f8;
  --link: #4A90D9; --link-hover: #2a70b9;
}}
.dark {{
  --bg: #1a1a2e; --fg: #e0e0e0; --fg2: #aaa;
  --surface: rgba(30,30,50,0.88); --border: #333;
  --input-bg: #2a2a3e; --code-bg: #2a2a3e;
  --link: #6db3f2; --link-hover: #8cc5ff;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg); color: var(--fg);
  line-height: 1.7; transition: background 0.3s, color 0.3s;
}}
/* Topbar */
nav {{
  position: sticky; top: 0; z-index: 10;
  padding: 10px 20px; background: var(--surface);
  backdrop-filter: blur(10px); border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}}
nav a {{
  color: var(--fg2); text-decoration: none; font-size: 14px;
  padding: 4px 12px; border-radius: 6px; transition: background 0.2s;
}}
nav a:hover {{ background: var(--input-bg); }}
nav a.active {{ color: var(--link); font-weight: 600; }}
.nav-links {{ display: flex; gap: 4px; }}
#theme-btn {{
  padding: 4px 10px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--input-bg); color: var(--fg); cursor: pointer; font-size: 12px;
}}
/* Main content */
.container {{
  max-width: 800px; margin: 0 auto; padding: 30px 20px 60px;
}}
/* Breadcrumb */
.breadcrumb {{
  font-size: 13px; color: var(--fg2); margin-bottom: 16px;
}}
.breadcrumb a {{ color: var(--link); text-decoration: none; }}
.breadcrumb a:hover {{ text-decoration: underline; }}
/* Metadata card */
.meta-card {{
  background: var(--input-bg); border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 8px;
}}
.meta-item {{ font-size: 13px; color: var(--fg2); }}
.meta-item strong {{ color: var(--fg); }}
.badge {{
  display: inline-block; padding: 2px 10px; border-radius: 12px;
  font-size: 11px; color: #fff; font-weight: 600;
}}
.tag {{
  display: inline-block; font-size: 11px; padding: 2px 8px;
  border-radius: 10px; background: var(--surface); border: 1px solid var(--border);
  color: var(--fg2); margin: 2px;
}}
/* Content */
.content h1 {{ font-size: 28px; margin: 24px 0 12px; }}
.content h2 {{ font-size: 20px; margin: 20px 0 10px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
.content h3 {{ font-size: 16px; margin: 16px 0 8px; }}
.content p {{ margin: 8px 0; }}
.content ul, .content ol {{ padding-left: 24px; margin: 8px 0; }}
.content li {{ margin: 4px 0; }}
.content a {{ color: var(--link); text-decoration: none; }}
.content a:hover {{ text-decoration: underline; color: var(--link-hover); }}
.content code {{
  background: var(--code-bg); padding: 2px 6px; border-radius: 4px;
  font-size: 0.9em; font-family: 'SF Mono', monospace;
}}
.content pre {{
  background: var(--code-bg); padding: 14px; border-radius: 8px;
  overflow-x: auto; margin: 10px 0; border: 1px solid var(--border);
}}
.content pre code {{ background: none; padding: 0; }}
.content blockquote {{
  border-left: 3px solid var(--link); padding: 8px 16px;
  margin: 10px 0; color: var(--fg2); background: var(--input-bg);
  border-radius: 0 6px 6px 0;
}}
.content table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
.content th, .content td {{
  border: 1px solid var(--border); padding: 8px 12px; text-align: left; font-size: 14px;
}}
.content th {{ background: var(--input-bg); font-weight: 600; }}
/* Footer nav */
.page-nav {{
  display: flex; justify-content: space-between; margin-top: 40px;
  padding-top: 16px; border-top: 1px solid var(--border); font-size: 13px;
}}
.page-nav a {{ color: var(--link); text-decoration: none; }}
.page-nav a:hover {{ text-decoration: underline; }}
@media (max-width: 640px) {{
  .meta-card {{ grid-template-columns: 1fr; }}
  .container {{ padding: 16px 12px 40px; }}
}}
</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}},{{left:'\\\\(',right:'\\\\)',display:false}},{{left:'\\\\[',right:'\\\\]',display:true}}],throwOnError:false}})"></script>
</head>
<body>
<nav>
  <div class="nav-links">
    <a href="{graph_path}">Graph</a>
    <a href="{stats_path}">Statistics</a>
    <a href="{wiki_index_path}" class="active">Wiki</a>
  </div>
  <button id="theme-btn" onclick="document.body.classList.toggle('dark');this.textContent=document.body.classList.contains('dark')?'Light':'Dark'">Dark</button>
</nav>
<div class="container">
  <div class="breadcrumb">{breadcrumb}</div>
  {meta_card}
  <div class="content">
    {content}
  </div>
  <div class="page-nav">
    {prev_link}
    {next_link}
  </div>
</div>
</body>
</html>"""

WIKI_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wiki Index — LLM Wiki</title>
<style>
:root {{
  --bg: #ffffff; --fg: #1a1a2e; --fg2: #555;
  --surface: rgba(255,255,255,0.85); --border: #e0e0e0;
  --input-bg: #f5f5f5; --link: #4A90D9; --link-hover: #2a70b9;
}}
.dark {{
  --bg: #1a1a2e; --fg: #e0e0e0; --fg2: #aaa;
  --surface: rgba(30,30,50,0.88); --border: #333;
  --input-bg: #2a2a3e; --link: #6db3f2; --link-hover: #8cc5ff;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg); color: var(--fg); line-height: 1.7;
  transition: background 0.3s, color 0.3s;
}}
nav {{
  position: sticky; top: 0; z-index: 10;
  padding: 10px 20px; background: var(--surface);
  backdrop-filter: blur(10px); border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
}}
nav a {{
  color: var(--fg2); text-decoration: none; font-size: 14px;
  padding: 4px 12px; border-radius: 6px; transition: background 0.2s;
}}
nav a:hover {{ background: var(--input-bg); }}
nav a.active {{ color: var(--link); font-weight: 600; }}
.nav-links {{ display: flex; gap: 4px; }}
#theme-btn {{
  padding: 4px 10px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--input-bg); color: var(--fg); cursor: pointer; font-size: 12px;
}}
.container {{ max-width: 800px; margin: 0 auto; padding: 30px 20px 60px; }}
h1 {{ font-size: 28px; margin-bottom: 20px; }}
h2 {{ font-size: 20px; margin: 24px 0 10px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
.page-list {{ list-style: none; }}
.page-list li {{ padding: 6px 0; border-bottom: 1px solid var(--border); }}
.page-list a {{ color: var(--link); text-decoration: none; font-size: 14px; }}
.page-list a:hover {{ text-decoration: underline; }}
.page-type {{
  display: inline-block; font-size: 10px; padding: 1px 6px;
  border-radius: 8px; color: #fff; margin-left: 6px; vertical-align: middle;
}}
.page-conf {{ font-size: 12px; color: var(--fg2); margin-left: 8px; }}
.search-box {{
  width: 100%; padding: 10px 14px; font-size: 14px;
  border: 1px solid var(--border); border-radius: 8px;
  background: var(--input-bg); color: var(--fg); margin-bottom: 20px;
}}
.search-box:focus {{ outline: none; border-color: var(--link); }}
@media (max-width: 640px) {{
  .container {{ padding: 16px 12px; }}
}}
</style>
</head>
<body>
<nav>
  <div class="nav-links">
    <a href="../graph.html">Graph</a>
    <a href="../statistics.html">Statistics</a>
    <a href="index.html" class="active">Wiki</a>
  </div>
  <button id="theme-btn" onclick="document.body.classList.toggle('dark');this.textContent=document.body.classList.contains('dark')?'Light':'Dark'">Dark</button>
</nav>
<div class="container">
  <h1>Wiki Index</h1>
  <input class="search-box" type="text" placeholder="Search pages..." id="search" autocomplete="off" />
  {sections}
</div>
<script>
document.getElementById('search').addEventListener('input', function() {{
  const q = this.value.toLowerCase();
  document.querySelectorAll('.page-list li').forEach(li => {{
    li.style.display = li.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}});
</script>
</body>
</html>"""


def convert_wikilinks(html: str, current_path: str, page_map: dict[str, str]) -> str:
    """Convert [[wikilink]] in HTML to <a> tags."""
    current_dir = Path(current_path).parent

    def replace_link(m):
        name = m.group(1)
        display = m.group(2) if m.group(2) else name
        if name in page_map:
            target_path = page_map[name]
            target_html = target_path.replace(".md", ".html")
            # Use os-independent relative path from current page's dir
            try:
                rel = Path(target_html).relative_to(current_dir)
            except ValueError:
                # Cross-subdir: go up then into target
                up = "../" * len(current_dir.parts)
                rel = up + target_html
            return f'<a href="{escape_html(str(rel))}">{escape_html(display)}</a>'
        return f'<span style="color:#e74c3c" title="broken link">{escape_html(display)}</span>'
    return re.sub(r"\[\[([^\]|]+?)(?:\|([^\]]*?))?\]\]", replace_link, html)


def build_meta_card(fm: dict) -> str:
    page_type = fm.get("type", "unknown")
    color = TYPE_COLORS.get(page_type, DEFAULT_COLOR)
    confidence = fm.get("confidence")
    conf_str = f"{float(confidence):.2f}" if confidence is not None else "\u2014"
    tags = fm.get("tags", []) or []
    created = fm.get("created", "\u2014")
    updated = fm.get("updated", "\u2014")

    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags) if tags else "\u2014"

    return f"""<div class="meta-card">
  <div class="meta-item"><strong>Type:</strong> <span class="badge" style="background:{color}">{page_type}</span></div>
  <div class="meta-item"><strong>Confidence:</strong> {conf_str}</div>
  <div class="meta-item"><strong>Created:</strong> {created}</div>
  <div class="meta-item"><strong>Updated:</strong> {updated}</div>
  <div class="meta-item" style="grid-column: 1/-1"><strong>Tags:</strong> {tags_html}</div>
</div>"""


def main():
    parser = argparse.ArgumentParser(description="Convert wiki/ markdown to static HTML")
    parser.add_argument("--output", type=str, default=str(VAULT_DIR.parent / "static" / "wiki"),
                        help="Output directory for HTML files")
    args = parser.parse_args()
    output_dir = Path(args.output)

    if not WIKI_DIR.exists():
        print(json.dumps({"error": "wiki/ directory not found"}))
        return

    # Build page map: stem -> relative path
    page_map: dict[str, str] = {}
    all_pages: list[dict] = []

    for fp in sorted(WIKI_DIR.rglob("*.md")):
        rel = fp.relative_to(WIKI_DIR)
        page_map[fp.stem] = str(rel)
        text = fp.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        all_pages.append({
            "path": rel,
            "stem": fp.stem,
            "fm": fm or {},
            "body": body,
        })

    # Group pages by subdirectory
    by_subdir: dict[str, list[dict]] = {}
    for p in all_pages:
        subdir = str(p["path"].parent) if p["path"].parent != Path(".") else "root"
        by_subdir.setdefault(subdir, []).append(p)

    md_converter = md_lib.Markdown(extensions=["fenced_code", "tables", "toc"])
    count = 0

    for subdir, pages in by_subdir.items():
        pages_sorted = sorted(pages, key=lambda p: p["stem"])

        for i, p in enumerate(pages_sorted):
            md_converter.reset()
            html_body = md_converter.convert(p["body"])

            # Convert wikilinks in the HTML output
            html_body = convert_wikilinks(html_body, str(p["path"]), page_map)

            # Breadcrumb
            parts = list(p["path"].parts[:-1])
            bc = '<a href="../index.html">wiki</a>'
            for part in parts:
                if part != ".":
                    bc += f' / <a href="../{part}/index.html">{part}</a>'
            bc += f' / {p["stem"]}'

            # Prev/next
            prev_link = ""
            next_link = ""
            if i > 0:
                prev_stem = pages_sorted[i - 1]["stem"]
                prev_link = f'<a href="{prev_stem}.html">&larr; {prev_stem}</a>'
            if i < len(pages_sorted) - 1:
                next_stem = pages_sorted[i + 1]["stem"]
                next_link = f'<a href="{next_stem}.html">{next_stem} &rarr;</a>'

            # Compute relative paths to other static pages
            depth = len(p["path"].parts) - 1
            up = "../" * (depth + 1)  # from static/wiki/subdir/ to static/
            graph_path = f"{up}graph.html"
            stats_path = f"{up}statistics.html"
            wiki_index_path = f"{'../' * depth}index.html"

            page_html = HTML_TEMPLATE.format(
                title=p["stem"],
                graph_path=graph_path,
                stats_path=stats_path,
                wiki_index_path=wiki_index_path,
                breadcrumb=bc,
                meta_card=build_meta_card(p["fm"]),
                content=html_body,
                prev_link=prev_link,
                next_link=next_link,
            )

            # Write file
            out_path = output_dir / p["path"].with_suffix(".html")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(page_html, encoding="utf-8")
            count += 1

    # Build wiki index.html
    sections_html = ""
    type_order = [("entities", "实体"), ("concepts", "概念"), ("syntheses", "综合分析")]
    for subdir_name, label in type_order:
        pages_in = by_subdir.get(subdir_name, [])
        if not pages_in:
            continue
        items = ""
        for p in sorted(pages_in, key=lambda x: x["stem"]):
            t = p["fm"].get("type", "unknown")
            color = TYPE_COLORS.get(t, DEFAULT_COLOR)
            conf = p["fm"].get("confidence")
            conf_str = f'<span class="page-conf">({float(conf):.2f})</span>' if conf is not None else ""
            items += f'<li><a href="{subdir_name}/{p["stem"]}.html">{p["stem"]}</a><span class="page-type" style="background:{color}">{t}</span>{conf_str}</li>\n'
        sections_html += f'<h2>{label} ({len(pages_in)})</h2>\n<ul class="page-list">\n{items}</ul>\n'

    index_html = WIKI_INDEX_TEMPLATE.format(sections=sections_html)
    (output_dir / "index.html").parent.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    print(json.dumps({"status": "ok", "pages_converted": count}))


if __name__ == "__main__":
    main()
