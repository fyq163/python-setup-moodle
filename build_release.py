#!/usr/bin/env python3
"""
Build a self-contained, dependency-free HTML release.

This produces the `release/` directory: one fully inlined `.html` file per
chapter (plus `index.html`). Each output file:

  * has NO <style> block, NO class/id attributes, NO <script> tags
  * renders the Markdown to plain static HTML (only the tags the Markdown
    itself produces: h1-h6, p, ul/ol, table, pre/code, blockquote, a, img)
  * contains ONLY the links that appear in the Markdown source — no
    auto-generated topnav, sidebar TOC, prev/next pager, hero, cards grid
    or footer chrome is injected.

It is meant for places that only accept raw, minimal HTML (paste the file
content straight into an HTML editor / CMS).

Run it in your own CI (e.g. a local `conda activate nlp-mark` env):
    conda activate nlp-mark
    pip install -r requirements-release.txt
    python3 build_release.py

Requires: Python 3.8+, the `markdown` package.

Image handling in the release build: any image whose URL is already an absolute
`https://` link is kept as-is, while local repo-relative paths (`../assets/img/...`)
are rewritten to a public CDN URL. So the release output is fully self-contained
and needs no bundled `assets/` folder.
"""
import os
import re
import html as _html
import markdown as _md

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "pages")
OUT = os.path.join(ROOT, "release")

# Chapter order / metadata. Mirrors assets/js/site.js but kept here so the
# release build is independent of the live site's JS.
CHAPTERS = [
    ("unix-basics",          "1 · Basic Unix-like Systems", "Skippable", "Command line, terminal, sudo, -h/--help, options vs arguments, exe vs no-extension."),
    ("virtual-environment",  "2 · Virtual Environments",    "Optional",   "Why not just use the system Python. uv vs conda, local vs global environments."),
    ("installation",         "3 · Installing Python",       "Required",   "Standalone installer, conda, and uv — across macOS (arm64), Windows (amd64) and Linux (x86_64)."),
    ("ide-setup",            "4 · Code Editors & IDEs",      "Required",   "VS Code / Cursor / CodeBuddy, PyCharm Community, and GitHub Copilot student access."),
    ("recommended-reading",  "5 · Recommended Reading",      "Optional",   "PEP 8 style, language servers (ty, pyright) and linters (ruff) to level up."),
]

MD_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]


# ---------------------------------------------------------------------------
# Markdown loading
# ---------------------------------------------------------------------------
def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def render_body(md_text):
    """Render markdown to HTML. No heading-id injection, no TOC collection —
    the release output contains only what the Markdown source itself produces."""
    html = _md.markdown(md_text, extensions=MD_EXTENSIONS)
    # Rewrite ONLY local repo-relative image paths (../assets/img/...) to a
    # public URL. Images that already use an absolute https:// URL are left
    # untouched ("detect https -> skip; detect repo path -> render").
    GITHUB_CDN = "https://cdn.jsdelivr.net/gh/fyq163/python-setup-moodle@main"

    def _rewrite_img(mo):
        src = mo.group(1)
        if src.startswith("https://"):
            return mo.group(0)          # already public -> keep as-is
        if src.startswith("../assets/img/"):
            return 'src="%s/assets/img/%s"' % (GITHUB_CDN, src[len("../assets/img/"):])
        return mo.group(0)              # other relative path -> leave alone

    html = re.sub(r'src="([^"]+)"', _rewrite_img, html)
    # Turn any leftover GitHub-style alert markers into emoji callouts.
    html = re.sub(
        r'<blockquote>\s*<p>\s*\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]\s*',
        lambda mo: '<blockquote><p>',
        html,
    )
    return html


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def build_chapter(name, title, tag, desc):
    md_path = os.path.join(PAGES, name + ".md")
    with open(md_path, encoding="utf-8") as f:
        meta, body = parse_frontmatter(f.read())
    title = meta.get("title", title)
    body_html = render_body(body)

    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>
""".format(title=_html.escape(title), body=body_html)
    return doc


def build_index():
    md_path = os.path.join(ROOT, "index.md")
    with open(md_path, encoding="utf-8") as f:
        meta, body = parse_frontmatter(f.read())
    title = meta.get("title", "Python Setup Guide for HKU Beginners")
    body_html = render_body(body)

    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>
""".format(title=_html.escape(title), body=body_html)
    return doc


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    # index
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    # chapters
    for name, title, tag, desc in CHAPTERS:
        out = build_chapter(name, title, tag, desc)
        with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(out)
        print("built release/%s.html" % name)
    print("release build complete -> %s" % OUT)


if __name__ == "__main__":
    main()
